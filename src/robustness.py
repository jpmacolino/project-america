"""Robustness checks for the primary tests in analysis.py.

R1  Trend-adjusted models: T1/T3 plus a cubic in year (removes slow secular drift that party
    control can proxy for, e.g. the Democratic House of 1955-1994).
R2  Rotation (circular-shift) test for every primary coefficient: the party series is shifted
    cyclically against the outcome by every offset >= 4 years; this keeps the long runs of party
    control and the autocorrelation of the outcome, so it is the right null for persistent
    treatments such as House control.
R3  Sub-period term-level tests: post-WWII only (1949+ terms, the Blinder-Watson window), and
    excluding the Depression/WWII terms (1929-1948).
R4  Machine-learning predictive test (scikit-learn): does adding party features improve
    out-of-sample (expanding-window) prediction of each outcome beyond its own history, war and
    depression flags and a time trend? Null distribution by shuffling party labels across whole
    presidential terms.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.multitest import multipletests
from sklearn.linear_model import RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from analysis import OUTCOMES, TREAT, LAGS, START, END, load, lagged, hac_ols, RNG

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"


def trend_terms(idx):
    t = (np.asarray(idx) - 1960) / 50.0
    return pd.DataFrame({"t1": t, "t2": t ** 2, "t3": t ** 3}, index=idx)


def r1_r2(p):
    rows = []
    for y in OUTCOMES:
        for k in LAGS:
            d = lagged(p, k)
            for model, terms in [("T1", TREAT), ("T3", ["unified_dem", "unified_rep"])]:
                sub = d[[y] + terms].dropna()
                tr = trend_terms(sub.index)
                m_tr = hac_ols(sub[y], pd.concat([sub[terms], tr], axis=1))
                # rotation test on the untrended model
                yv = sub[y].values
                full = p[terms].loc[START - 3:END]  # party series to rotate
                X0 = sm.add_constant(sub[terms]).values
                obs = np.linalg.lstsq(X0, yv, rcond=None)[0][1:]
                # rotate the full party history, then align to the outcome years with lag k
                years = sub.index.values
                base_years = np.arange(full.index.min(), full.index.max() + 1)
                L = len(base_years)
                pos = years - k - base_years[0]
                null = []
                for s in range(4, L - 3):
                    rot = np.roll(full.values, s, axis=0)[pos]
                    Xs = np.column_stack([np.ones(len(yv)), rot])
                    null.append(np.linalg.lstsq(Xs, yv, rcond=None)[0][1:])
                null = np.array(null)
                for j, t in enumerate(terms):
                    p_rot = (np.sum(np.abs(null[:, j]) >= abs(obs[j])) + 1) / (len(null) + 1)
                    rows.append(dict(outcome=y, lag=k, model=model, term=t, coef_trend=m_tr.params[t],
                                     p_trend=m_tr.pvalues[t], coef=obs[j], p_rotation=p_rot, n=len(yv)))
    r = pd.DataFrame(rows)
    r["q_trend"] = multipletests(r.p_trend, method="fdr_bh")[1]
    r["q_rotation"] = multipletests(r.p_rotation, method="fdr_bh")[1]
    return r


def r3(p):
    tv = pd.read_csv(OUT / "term_level_values.csv")
    rows = []
    for label, mask in [("post-WWII terms (1949+)", tv.term_start >= 1949),
                        ("excl. Depression/WWII terms (1929-1948)", ~tv.term_start.between(1929, 1948)),
                        ("all terms 1901+", tv.term_start >= 1901)]:
        for y in OUTCOMES:
            t = tv[mask & (tv.outcome == y)]
            dv, rv = t[t.party == "D"].value.values, t[t.party == "R"].value.values
            if len(dv) < 3 or len(rv) < 3:
                continue
            diff = dv.mean() - rv.mean()
            allv, nd = t.value.values, len(dv)
            null = np.array([(lambda s: s[:nd].mean() - s[nd:].mean())(RNG.permutation(allv)) for _ in range(10000)])
            rows.append(dict(sample=label, outcome=y, n_D=len(dv), n_R=len(rv), diff_D_minus_R=diff,
                             p_perm=(np.sum(np.abs(null) >= abs(diff)) + 1) / 10001,
                             p_welch=stats.ttest_ind(dv, rv, equal_var=False).pvalue))
    r = pd.DataFrame(rows)
    r["q_bh_within_sample"] = r.groupby("sample").p_perm.transform(lambda s: multipletests(s, method="fdr_bh")[1])
    return r


def ml_test(p, n_null=200, min_train=30):
    rows = []
    party_cols = ["dem_pres", "dem_house", "dem_senate"]
    for y in OUTCOMES:
        d = p.loc[:END].copy()
        d["y1"], d["y2"] = d[y].shift(1), d[y].shift(2)
        for c in party_cols:
            d[c + "_l1"] = p[c].shift(1)
        d["trend"] = (d.index - 1960) / 50
        d = d.loc[START:].dropna(subset=[y, "y1", "y2"] + [c + "_l1" for c in party_cols])
        if len(d) < min_train + 15:
            continue
        base = ["y1", "y2", "war", "depression", "trend"]
        pcols = [c + "_l1" for c in party_cols]

        def oos_mse(Xp):
            X = d[base].values if Xp is None else np.column_stack([d[base].values, Xp])
            yv, err = d[y].values, []
            for i in range(min_train, len(d)):
                m = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-2, 3, 20)))
                m.fit(X[:i], yv[:i])
                err.append((m.predict(X[i:i + 1])[0] - yv[i]) ** 2)
            return np.mean(err)

        mse_base = oos_mse(None)
        mse_party = oos_mse(d[pcols].values)
        gain = 1 - mse_party / mse_base  # >0 means party features help
        # null: shuffle the president/house/senate triple across whole terms (keeps their joint pattern)
        terms = (p.term_start.shift(1)).loc[d.index].values
        uniq = np.unique(terms)
        trip = pd.DataFrame(d[pcols].values, index=terms).groupby(level=0).first().reindex(uniq).values
        idx = pd.Series(range(len(uniq)), index=uniq).loc[terms].values
        null = []
        for _ in range(n_null):
            null.append(1 - oos_mse(trip[RNG.permutation(len(uniq))][idx]) / mse_base)
        null = np.array(null)
        rows.append(dict(outcome=y, n_oos=len(d) - min_train, mse_base=mse_base, mse_with_party=mse_party,
                         oos_gain_pct=100 * gain, null_mean_gain_pct=100 * null.mean(),
                         p_perm=(np.sum(null >= gain) + 1) / (n_null + 1)))
    r = pd.DataFrame(rows)
    r["q_bh"] = multipletests(r.p_perm, method="fdr_bh")[1]
    return r


def main():
    p = load()
    a = r1_r2(p)
    a.to_csv(OUT / "robust_trend_rotation.csv", index=False)
    b = r3(p)
    b.to_csv(OUT / "robust_subperiods.csv", index=False)
    c = ml_test(p)
    c.to_csv(OUT / "ml_predictive_test.csv", index=False)
    pd.set_option("display.width", 250)
    print("R1/R2: q_trend<.10 or q_rotation<.10\n", a[(a.q_trend < .10) | (a.q_rotation < .10)].round(4).to_string())
    print("\nR2 count q_rotation<.05:", int((a.q_rotation < .05).sum()), "of", len(a))
    print("R1 count q_trend<.05:", int((a.q_trend < .05).sum()))
    print("\nR3\n", b[b.outcome.isin(["gdp_pc_growth", "unemp_change", "inflation", "poverty_change", "gini_change", "life_exp_change"])].round(3).to_string())
    print("\nR4 ML\n", c.round(3).to_string())
    json.dump(dict(rotation_q05=int((a.q_rotation < .05).sum()), trend_q05=int((a.q_trend < .05).sum()),
                   ml_q05=int((c.q_bh < .05).sum())), open(OUT / "robust_summary.json", "w"))


if __name__ == "__main__":
    main()
