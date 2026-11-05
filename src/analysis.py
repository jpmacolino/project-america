"""Hypothesis tests: does party control of the Presidency / House / Senate affect outcomes?

H0: party control has no effect on any outcome (all partisan coefficients = 0).
Tests (all pre-specified in this file before results were inspected):
  T1  Annual OLS, Newey-West HAC SEs, lags k = 0, 1, 2:
        y_t = a + bP*DemPres_{t-k} + bH*DemHouse_{t-k} + bS*DemSenate_{t-k} + e
  T2  Same + controls (war year, Great Depression 1930-39, y_{t-1})
  T3  Unified-government model: y_t = a + bUD*UnifiedDem + bUR*UnifiedRep + e  (divided = baseline)
  T4  Term-level test (honest N): mean outcome per 4-year presidential term with a 1-year lag
      (Blinder-Watson convention), D vs R terms; Welch t, Mann-Whitney U, and an exact-style
      permutation test (100k shuffles of term labels).
  T5  Block-permutation p-value for the annual presidential coefficient (shuffle party labels
      across whole 4-year terms, preserving within-series autocorrelation).
  Multiple testing: Benjamini-Hochberg FDR across every T1/T3 coefficient (the primary family),
      and separately across the 14 T4 tests.
  Equivalence: TOST on the T4 difference against a pre-declared smallest effect of interest.
Run:  python src/analysis.py
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)
RNG = np.random.default_rng(20261104)
N_PERM = 20000

# outcome -> (family, label, units, smallest effect size of interest per year, "good" direction)
OUTCOMES = {
    "gdp_pc_growth":          ("Economy & prices", "Real GDP per capita growth", "pp/yr", 0.75, +1),
    "unemp_change":           ("Economy & prices", "Change in unemployment rate", "pp/yr", 0.25, -1),
    "inflation":              ("Economy & prices", "CPI inflation", "pp/yr", 1.00, -1),
    "real_wage_growth":       ("Economy & prices", "Real hourly wage growth (1965+)", "pp/yr", 0.50, +1),
    "real_med_hh_inc_growth": ("Economy & prices", "Real median household income growth (1985+)", "pp/yr", 0.75, +1),
    "poverty_change":         ("Poverty & inequality", "Change in official poverty rate (1960+)", "pp/yr", 0.25, -1),
    "top1_change":            ("Poverty & inequality", "Change in top-1% income share (1914-2022)", "pp/yr", 0.25, -1),
    "gini_change":            ("Poverty & inequality", "Change in family-income Gini x100 (1948+)", "pts/yr", 0.25, -1),
    "real_oil_return":        ("Commodities", "Real crude oil price change", "pp/yr", 10.0, 0),
    "real_commodity_return":  ("Commodities", "Real PPI all-commodities change (1914+)", "pp/yr", 3.00, 0),
    "life_exp_change":        ("Education & health", "Change in life expectancy (1902-2023)", "yrs/yr", 0.10, +1),
    "inf_mort_change":        ("Education & health", "Infant mortality change (1950+)", "log pp/yr", 1.00, -1),
    "hs_attain_change":       ("Education & health", "Change in % adults w/ high school (1965+)", "pp/yr", 0.20, +1),
    "ba_attain_change":       ("Education & health", "Change in % adults w/ BA (1965+)", "pp/yr", 0.10, +1),
}
TREAT = ["dem_pres", "dem_house", "dem_senate"]
LAGS = [0, 1, 2]
START, END = 1900, 2025


def load():
    p = pd.read_csv(ROOT / "data" / "panel.csv", index_col=0)
    p["depression"] = ((p.index >= 1930) & (p.index <= 1939)).astype(int)
    p["war"] = p["war"].fillna(0)  # MeasuringWorth war flag ends 2024; no declared war in 2025
    return p


def lagged(p, k):
    d = p.copy()
    for c in TREAT + ["unified_dem", "unified_rep"]:
        d[c] = p[c].shift(k)
    return d.loc[START:END]


def hac_ols(y, X, maxlags=4):
    X = sm.add_constant(X, has_constant="add")
    return sm.OLS(y, X, missing="drop").fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})


def annual_models(p):
    rows = []
    for y in OUTCOMES:
        for k in LAGS:
            d = lagged(p, k)
            sub = d[[y] + TREAT + ["unified_dem", "unified_rep", "war", "depression"]].copy()
            sub["y_lag"] = d[y].shift(1)
            sub = sub.dropna(subset=[y] + TREAT)
            m1 = hac_ols(sub[y], sub[TREAT])
            for t in TREAT:
                rows.append(dict(outcome=y, lag=k, model="T1 base", term=t, coef=m1.params[t], se=m1.bse[t],
                                 p=m1.pvalues[t], n=int(m1.nobs), years=f"{sub.index.min()}-{sub.index.max()}"))
            s2 = sub.dropna(subset=["y_lag"])
            ctrl = [c for c in ["war", "depression", "y_lag"] if s2[c].nunique() > 1]  # drop controls constant in short samples
            m2 = hac_ols(s2[y], s2[TREAT + ctrl])
            for t in TREAT:
                rows.append(dict(outcome=y, lag=k, model="T2 controls", term=t, coef=m2.params[t], se=m2.bse[t],
                                 p=m2.pvalues[t], n=int(m2.nobs), years=f"{s2.index.min()}-{s2.index.max()}"))
            m3 = hac_ols(sub[y], sub[["unified_dem", "unified_rep"]])
            for t in ["unified_dem", "unified_rep"]:
                rows.append(dict(outcome=y, lag=k, model="T3 unified", term=t, coef=m3.params[t], se=m3.bse[t],
                                 p=m3.pvalues[t], n=int(m3.nobs), years=f"{sub.index.min()}-{sub.index.max()}"))
    r = pd.DataFrame(rows)
    prim = r.model.isin(["T1 base", "T3 unified"])
    r["q_bh_primary"] = np.nan
    r.loc[prim, "q_bh_primary"] = multipletests(r.loc[prim, "p"], method="fdr_bh")[1]
    r["q_bh_all"] = multipletests(r["p"], method="fdr_bh")[1]
    return r


def block_perm_pres(p, y, k, n_perm=N_PERM):
    """Shuffle president-party labels across whole 4-year terms; refit T1; return two-sided p for bP."""
    d = lagged(p, k)
    sub = d[[y] + TREAT + ["term_start"]].dropna()
    X = sm.add_constant(sub[TREAT])
    obs = sm.OLS(sub[y], X).fit().params["dem_pres"]
    # term-level labels (lagged term id so the block structure follows the lag)
    terms = p["term_start"].shift(k).loc[sub.index]
    uniq = terms.unique()
    lab = p.groupby("term_start")["dem_pres"].first().reindex(uniq).values
    Xv = X.values.copy()
    j = list(X.columns).index("dem_pres")
    idx = pd.Series(range(len(uniq)), index=uniq).loc[terms.values].values
    yv = sub[y].values
    null = np.empty(n_perm)
    for i in range(n_perm):
        Xv[:, j] = RNG.permutation(lab)[idx]
        null[i] = np.linalg.lstsq(Xv, yv, rcond=None)[0][j]
    return obs, (np.sum(np.abs(null) >= abs(obs)) + 1) / (n_perm + 1)


def term_level(p):
    """Blinder-Watson style: term outcome = mean of years term_start+1 .. term_start+4."""
    rows, detail = [], []
    terms = sorted(set(p.term_start))
    for y in OUTCOMES:
        recs = []
        for ts in terms:
            yrs = list(range(ts + 1, ts + 5))
            vals = p[y].reindex(yrs).dropna()
            if len(vals) < 3 or ts + 4 > END + 1:
                continue
            recs.append(dict(term_start=ts, party=p.loc[ts, "pres_party"] if ts in p.index else None,
                             president=p.loc[ts, "president"] if ts in p.index else None, value=vals.mean()))
        t = pd.DataFrame(recs).dropna()
        t = t[t.term_start >= 1901]  # first full term inside the 1900+ window
        dvals, rvals = t[t.party == "D"].value.values, t[t.party == "R"].value.values
        diff = dvals.mean() - rvals.mean()
        welch = stats.ttest_ind(dvals, rvals, equal_var=False)
        mw = stats.mannwhitneyu(dvals, rvals, alternative="two-sided")
        allv, nd = t.value.values, len(dvals)
        null = np.array([(lambda s: s[:nd].mean() - s[nd:].mean())(RNG.permutation(allv)) for _ in range(N_PERM)])
        p_perm = (np.sum(np.abs(null) >= abs(diff)) + 1) / (N_PERM + 1)
        # TOST equivalence against +/- SESOI (Welch df)
        sesoi = OUTCOMES[y][3]
        se = np.sqrt(dvals.var(ddof=1) / len(dvals) + rvals.var(ddof=1) / len(rvals))
        df = welch.df if hasattr(welch, "df") else len(allv) - 2
        p_lo = 1 - stats.t.cdf((diff + sesoi) / se, df)
        p_hi = stats.t.cdf((diff - sesoi) / se, df)
        # minimum detectable effect at 80% power, alpha .05 two-sided
        mde = (stats.t.ppf(0.975, df) + stats.t.ppf(0.80, df)) * se
        # Cohen's d
        sp = np.sqrt(((len(dvals) - 1) * dvals.var(ddof=1) + (len(rvals) - 1) * rvals.var(ddof=1)) / (len(allv) - 2))
        rows.append(dict(outcome=y, n_D=len(dvals), n_R=len(rvals), mean_D=dvals.mean(), mean_R=rvals.mean(),
                         diff_D_minus_R=diff, se=se, cohens_d=diff / sp, p_welch=welch.pvalue, p_mannwhitney=mw.pvalue,
                         p_perm=p_perm, sesoi=sesoi, p_tost=max(p_lo, p_hi), mde80=mde,
                         first_term=int(t.term_start.min()), last_term=int(t.term_start.max())))
        t["outcome"] = y
        detail.append(t)
    r = pd.DataFrame(rows)
    r["q_bh_perm"] = multipletests(r.p_perm, method="fdr_bh")[1]
    return r, pd.concat(detail)


def reverse_causality(p):
    """Does the economy in the election year predict whether the incumbent party keeps the White House?"""
    rows = []
    for yr in range(1900, 2025, 4):
        nxt = yr + 1
        if nxt not in p.index:
            continue
        rows.append(dict(election=yr, gdp_growth=p.loc[yr, "gdp_pc_growth"], unemp_change=p.loc[yr, "unemp_change"],
                         inflation=p.loc[yr, "inflation"],
                         incumbent_kept=int(p.loc[yr, "pres_party"] == p.loc[nxt, "pres_party"])))
    e = pd.DataFrame(rows)
    X = sm.add_constant(e[["gdp_growth"]])
    m = sm.Logit(e.incumbent_kept, X).fit(disp=0)
    pb = stats.pointbiserialr(e.incumbent_kept, e.gdp_growth)
    return e, dict(logit_coef_gdp=m.params["gdp_growth"], logit_p=m.pvalues["gdp_growth"], n=len(e),
                   pointbiserial_r=pb.statistic, pointbiserial_p=pb.pvalue,
                   kept_mean_growth=e[e.incumbent_kept == 1].gdp_growth.mean(),
                   lost_mean_growth=e[e.incumbent_kept == 0].gdp_growth.mean())


def main():
    p = load()
    ann = annual_models(p)
    ann.to_csv(OUT / "annual_models.csv", index=False)

    perm_rows = []
    for y in OUTCOMES:
        for k in LAGS:
            obs, pp = block_perm_pres(p, y, k)
            perm_rows.append(dict(outcome=y, lag=k, coef_dem_pres=obs, p_block_perm=pp))
    perm = pd.DataFrame(perm_rows)
    perm["q_bh"] = multipletests(perm.p_block_perm, method="fdr_bh")[1]
    perm.to_csv(OUT / "block_permutation_president.csv", index=False)

    term, term_detail = term_level(p)
    term.to_csv(OUT / "term_level_tests.csv", index=False)
    term_detail.to_csv(OUT / "term_level_values.csv", index=False)

    elec, rc = reverse_causality(p)
    elec.to_csv(OUT / "elections_reverse_causality.csv", index=False)

    summary = dict(
        n_primary_tests=int(ann.model.isin(["T1 base", "T3 unified"]).sum()),
        primary_raw_p_lt_05=int((ann[ann.model.isin(["T1 base", "T3 unified"])].p < 0.05).sum()),
        primary_q_lt_05=int((ann.q_bh_primary < 0.05).sum()),
        primary_q_lt_10=int((ann.q_bh_primary < 0.10).sum()),
        block_perm_q_lt_05=int((perm.q_bh < 0.05).sum()),
        term_q_lt_05=int((term.q_bh_perm < 0.05).sum()),
        term_equivalent_at_05=int((term.p_tost < 0.05).sum()),
        reverse_causality=rc,
    )
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, default=float))
    pd.set_option("display.width", 250)
    print(json.dumps(summary, indent=2, default=float))
    print("\nTERM LEVEL (D minus R, 1-yr lag)\n", term.round(3).to_string())
    print("\nBLOCK PERM president\n", perm.round(4).to_string())
    print("\nPRIMARY q<0.10\n", ann[ann.q_bh_primary < 0.10].round(4).to_string())
    print("\nraw p<0.05 primary\n", ann[(ann.p < 0.05) & ann.model.isin(["T1 base", "T3 unified"])].round(4).to_string())


if __name__ == "__main__":
    main()
