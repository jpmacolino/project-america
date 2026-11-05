"""Exploratory follow-up (NOT part of the pre-specified family): is the Democratic-term
advantage in unemployment/GDP/poverty/inequality explained by the conditions each president inherited?

Model (term level):  outcome_term = a + b*DemTerm + c*Unemployment_in_inauguration_year + e
p-values by permutation of the D/R labels across terms with the inherited-unemployment control
held fixed (20,000 shuffles), for all terms 1901+ and for post-WWII terms 1949+.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(7)


def coef_D(y, D, u0):
    X = np.column_stack([np.ones(len(y)), D, u0])
    return np.linalg.lstsq(X, y, rcond=None)[0][1]


def main(n=20000):
    p = pd.read_csv(ROOT / "data" / "panel.csv", index_col=0)
    tv = pd.read_csv(ROOT / "results" / "term_level_values.csv")
    rows = []
    for y in ["gdp_pc_growth", "unemp_change", "inflation", "poverty_change", "gini_change", "real_med_hh_inc_growth"]:
        t = tv[tv.outcome == y].copy()
        t["u0"] = p.loc[t.term_start, "unemp"].values
        t["D"] = (t.party == "D").astype(int)
        for lab, m in [("all terms 1901+", t.term_start >= 1901), ("post-WWII terms 1949+", t.term_start >= 1949)]:
            s = t[m]
            yv, D, u0 = s.value.values, s.D.values, s.u0.values
            raw = yv[D == 1].mean() - yv[D == 0].mean()
            obs = coef_D(yv, D, u0)
            null = np.array([coef_D(yv, RNG.permutation(D), u0) for _ in range(n)])
            rows.append(dict(outcome=y, sample=lab, n_terms=len(s), inherited_unemp_D=s[s.D == 1].u0.mean(),
                             inherited_unemp_R=s[s.D == 0].u0.mean(), raw_gap=raw, gap_adj_inherited=obs,
                             p_perm_adj=(np.sum(np.abs(null) >= abs(obs)) + 1) / (n + 1)))
    r = pd.DataFrame(rows)
    r["q_bh"] = multipletests(r.p_perm_adj, method="fdr_bh")[1]
    r.to_csv(ROOT / "results" / "alternative_inherited_conditions.csv", index=False)
    print(r.round(3).to_string())


def stress_post_wwii(n=10000):
    """Post-WWII terms: add a linear time trend and run leave-one-term-out influence checks."""
    import statsmodels.api as sm
    p = pd.read_csv(ROOT / "data" / "panel.csv", index_col=0)
    tv = pd.read_csv(ROOT / "results" / "term_level_values.csv")
    rng, rows = np.random.default_rng(1), []
    for y in ["unemp_change", "gdp_pc_growth", "gini_change", "poverty_change"]:
        t = tv[(tv.outcome == y) & (tv.term_start >= 1949)].copy()
        t["u0"] = p.loc[t.term_start, "unemp"].values
        t["D"] = (t.party == "D").astype(int)
        t["tr"] = (t.term_start - 1985) / 40
        X = np.column_stack([np.ones(len(t)), t.D, t.u0, t.tr])
        b = np.linalg.lstsq(X, t.value, rcond=None)[0][1]
        null = [np.linalg.lstsq(np.column_stack([np.ones(len(t)), rng.permutation(t.D.values), t.u0, t.tr]),
                                t.value, rcond=None)[0][1] for _ in range(n)]
        loo = [np.linalg.lstsq(sm.add_constant(t.drop(i)[["D", "u0"]]).values, t.drop(i).value.values,
                               rcond=None)[0][1] for i in t.index]
        rows.append(dict(outcome=y, gap_adj_inherited_and_trend=b,
                         p_perm=(np.sum(np.abs(null) >= abs(b)) + 1) / (n + 1), loo_min=min(loo), loo_max=max(loo)))
    r = pd.DataFrame(rows)
    r.to_csv(ROOT / "results" / "alternative_post_wwii_stress.csv", index=False)
    print(r.round(3).to_string())


if __name__ == "__main__":
    main()
    stress_post_wwii()
