"""Generates notebooks/explore.ipynb (run once; the notebook is the deliverable)."""
from pathlib import Path
import nbformat as nbf

nb = nbf.v4.new_notebook()
C = []
md = lambda s: C.append(nbf.v4.new_markdown_cell(s.strip()))  # noqa: E731
code = lambda s: C.append(nbf.v4.new_code_cell(s.strip()))  # noqa: E731

md(r"""
# Does party control matter? Explorer notebook

Every chart and table behind the write-up, built from the files in `data/` and `results/`.
Run top to bottom (**Kernel → Restart & Run All**). Nothing here re-estimates the models;
to regenerate `results/`, run the scripts in `src/` (see README).

**Colour key used throughout:** blue = Democratic, red = Republican, grey = not significant / neutral.

Sections
1. Who governed, 1900–2025
2. Every outcome over time, shaded by the president's party
3. Term-level test: Democratic vs Republican terms
4. Equivalence: which nulls are actually *proven*
5. All 210 primary tests at a glance (naive vs rotation p-values)
6. Why the Congress "effects" are artifacts
7. The alternative hypothesis: inherited conditions
8. Machine-learning check
9. Reverse causality: does the economy pick the party?
10. Full output tables
11. Plot any outcome yourself
""")

code(r"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from IPython.display import display, Markdown

ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
DATA, RES = ROOT / "data", ROOT / "results"
import sys; sys.path.insert(0, str(ROOT / "src"))
from analysis import OUTCOMES   # labels, units, smallest-effect thresholds

# Palette (validated: blue/red pass colour-vision-deficiency separation)
D, R = "#2a78d6", "#e34948"
GREY, INK, INK2, GRID, SURF = "#a8a7a0", "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"
plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "font.size": 10,
    "axes.titlesize": 11, "axes.titleweight": "bold", "axes.titlecolor": INK, "axes.titlelocation": "left",
    "lines.linewidth": 1.6, "figure.dpi": 110,
})
pd.set_option("display.max_rows", 500, "display.max_columns", 50, "display.width", 200)

panel = pd.read_csv(DATA / "panel.csv", index_col=0)
term_tests = pd.read_csv(RES / "term_level_tests.csv")
term_vals = pd.read_csv(RES / "term_level_values.csv")
annual = pd.read_csv(RES / "annual_models.csv")
rot = pd.read_csv(RES / "robust_trend_rotation.csv")
subp = pd.read_csv(RES / "robust_subperiods.csv")
ml = pd.read_csv(RES / "ml_predictive_test.csv")
alt = pd.read_csv(RES / "alternative_inherited_conditions.csv")
stress = pd.read_csv(RES / "alternative_post_wwii_stress.csv")
elec = pd.read_csv(RES / "elections_reverse_causality.csv")
label = {k: v[1] for k, v in OUTCOMES.items()}
units = {k: v[2] for k, v in OUTCOMES.items()}

def shade_presidents(ax, y0=1900, y1=2025, alpha=0.10):
    # Light background band per year: blue = Democratic president, red = Republican
    for yr, party in panel.loc[y0:y1, "pres_party"].items():
        ax.axvspan(yr - 0.5, yr + 0.5, color=D if party == "D" else R, alpha=alpha, lw=0)

def label_points(ax, xs, ys, texts, frac=0.045, **kw):
    # Greedy labelling: skip a label if it would land too close to one already placed
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim(); placed = []
    for x, y, t in sorted(zip(xs, ys, texts), key=lambda r: -abs(r[1])):
        nx, ny = (x - x0) / (x1 - x0), (y - y0) / (y1 - y0)
        if all(abs(nx - px) > 2.2 * frac or abs(ny - py) > frac for px, py in placed):
            ax.annotate(t, (x, y), xytext=(4, 3), textcoords="offset points", fontsize=7.5, color=INK2, **kw)
            placed.append((nx, ny))

display(Markdown("**Headline (results/summary.json)**"))
print(json.dumps(json.load(open(RES / "summary.json")), indent=2))
""")

md("## 1. Who governed, 1900–2025\nEach row is one branch; each cell is one year. The bottom strip marks years when one party held all three.")
code(r"""
p = panel.loc[1900:2025]
fig, ax = plt.subplots(figsize=(12, 2.6))
rows = [("President", "pres_party"), ("House", "house_party"), ("Senate", "senate_party")]
for i, (name, col) in enumerate(rows):
    for yr, party in p[col].items():
        ax.add_patch(mpatches.Rectangle((yr - 0.5, 2 - i), 1, 0.8, color=D if party == "D" else R, lw=0))
for yr, u in p["unified"].items():
    if u:
        ax.add_patch(mpatches.Rectangle((yr - 0.5, -0.9), 1, 0.4, color=INK2, lw=0))
ax.set_yticks([2.4, 1.4, 0.4, -0.7], ["President", "House", "Senate", "Unified"])
ax.set_xlim(1899.5, 2025.5); ax.set_ylim(-1.1, 2.9); ax.grid(False)
for s in ax.spines.values(): s.set_visible(False)
ax.set_title("Party control by year (blue = Democratic, red = Republican)")
plt.show()
print(f"Share of years with a Democratic President {p.dem_pres.mean():.0%}, House {p.dem_house.mean():.0%}, "
      f"Senate {p.dem_senate.mean():.0%}; unified government {p.unified.mean():.0%}")
""")

md("## 2. Every outcome over time\nThese are the exact series tested (annual changes). Background shading = the president's party that year. If party mattered a lot, the line would sit visibly higher or lower in one colour.")
code(r"""
outs = list(OUTCOMES)
fig, axes = plt.subplots(7, 2, figsize=(13, 20), sharex=True)
for ax, y in zip(axes.flat, outs):
    s = panel[y].loc[1900:2025].dropna()
    shade_presidents(ax, s.index.min(), s.index.max())
    ax.plot(s.index, s.values, color=INK, lw=1.2)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_title(label[y], fontsize=10)
    ax.set_ylabel(units[y])
for ax in axes[-1]: ax.set_xlim(1898, 2027)
fig.legend(handles=[mpatches.Patch(color=D, alpha=.3, label="Democratic president"),
                    mpatches.Patch(color=R, alpha=.3, label="Republican president")],
           loc="upper right", ncol=2, frameon=False)
fig.tight_layout(rect=(0, 0, 1, 0.985)); plt.show()
""")

md("## 3. Term-level test (T4)\nEach dot is one 4-year presidential term (years 2–5 after inauguration, so a president is judged on his own economy). Horizontal ticks are the party means. `p` is the 20,000-shuffle permutation p-value; `q` is after Benjamini–Hochberg correction across all 14 outcomes. Nothing reaches q < 0.05.")
code(r"""
fig, axes = plt.subplots(4, 4, figsize=(14, 13))
rng = np.random.default_rng(0)
for ax, (_, r) in zip(axes.flat, term_tests.iterrows()):
    t = term_vals[term_vals.outcome == r.outcome]
    for x, party, col in [(0, "D", D), (1, "R", R)]:
        v = t[t.party == party].value.values
        ax.scatter(x + rng.uniform(-.12, .12, len(v)), v, s=36, color=col, alpha=.85, edgecolor=SURF, lw=1)
        ax.hlines(v.mean(), x - .28, x + .28, color=col, lw=2.5)
    ax.axhline(0, color=INK2, lw=.8)
    ax.set_xticks([0, 1], [f"Dem (n={r.n_D})", f"Rep (n={r.n_R})"]); ax.set_xlim(-.6, 1.6)
    ax.set_title(f"{label[r.outcome].split(' (')[0]}\ngap {r.diff_D_minus_R:+.2f} {units[r.outcome]} · p={r.p_perm:.3f} · q={r.q_bh_perm:.2f}",
                 fontsize=9.5)
for ax in axes.flat[len(term_tests):]: ax.axis("off")
fig.tight_layout(); plt.show()
display(term_tests[["outcome", "n_D", "n_R", "mean_D", "mean_R", "diff_D_minus_R", "p_welch", "p_mannwhitney",
                    "p_perm", "q_bh_perm", "mde80"]].round(3))
""")

md("## 4. Equivalence: which nulls are *proven*?\n\"Not significant\" does not mean \"no effect\". Here each gap is divided by the smallest effect I pre-declared as meaningful, with its 90% confidence interval (the interval used by a TOST equivalence test). A whisker entirely inside the grey band means the effect is provably negligible; only oil and commodity prices get there.")
code(r"""
from scipy import stats
t = term_tests.copy()
dfree = t.n_D + t.n_R - 2
crit = stats.t.ppf(0.95, dfree)
t["gap"] = t.diff_D_minus_R / t.sesoi
t["lo"] = (t.diff_D_minus_R - crit * t.se) / t.sesoi
t["hi"] = (t.diff_D_minus_R + crit * t.se) / t.sesoi
t["inside"] = (t.lo >= -1) & (t.hi <= 1)
t = t.iloc[::-1]
fig, ax = plt.subplots(figsize=(10, 6.5))
ax.axvspan(-1, 1, color=GREY, alpha=.18, lw=0)
ax.axvline(0, color=INK2, lw=.8)
for i, (_, r) in enumerate(t.iterrows()):
    c = D if r.inside else GREY
    ax.plot([r.lo, r.hi], [i, i], color=c, lw=2)
    ax.scatter(r.gap, i, s=50, color=c, zorder=3)
ax.set_yticks(range(len(t)), [label[o].split(" (")[0] for o in t.outcome])
ax.set_xlabel("Democratic minus Republican, in units of the smallest meaningful effect  (← lower under D · higher under D →)")
ax.text(0, len(t) - .3, "no meaningful effect", ha="center", color=INK2, fontsize=9)
ax.set_title("Only oil and commodity prices are provably unaffected by the president's party")
ax.grid(axis="y", visible=False); plt.tight_layout(); plt.show()
display(term_tests[["outcome", "sesoi", "diff_D_minus_R", "p_tost"]].assign(
    verdict=np.where(term_tests.p_tost < .05, "equivalent (null accepted)", "inconclusive")).round(3))
""")

md("## 5. All 210 primary tests at a glance\nLeft: naive p-values from the annual regressions (Newey–West errors). Right: the same coefficients judged by the **rotation test**, which slides the party history against the outcome to build a null that keeps long party runs intact. Darker = smaller p. Cells marked ● survive FDR (q < 0.05). The left panel's dots all disappear on the right.")
code(r"""
prim = annual[annual.model.isin(["T1 base", "T3 unified"])].copy()
prim["col"] = prim.term.str.replace("dem_", "").str.replace("unified_", "unif-") + " L" + prim.lag.astype(str)
r2 = rot.copy(); r2["col"] = r2.term.str.replace("dem_", "").str.replace("unified_", "unif-") + " L" + r2.lag.astype(str)
order = [f"{t} L{k}" for t in ["pres", "house", "senate", "unif-dem", "unif-rep"] for k in (0, 1, 2)]
rows = list(OUTCOMES)
def grid(df, pcol, qcol):
    P = df.pivot_table(index="outcome", columns="col", values=pcol).reindex(index=rows, columns=order)
    Q = df.pivot_table(index="outcome", columns="col", values=qcol).reindex(index=rows, columns=order)
    return P, Q
fig, axes = plt.subplots(1, 2, figsize=(15, 6.5), sharey=True)
for ax, (P, Q), title in [(axes[0], grid(prim, "p", "q_bh_primary"), "Naive HAC p-values (7 survive FDR)"),
                          (axes[1], grid(r2, "p_rotation", "q_rotation"), "Rotation-test p-values (0 survive FDR)")]:
    im = ax.imshow(-np.log10(P.values), cmap="Blues", vmin=0, vmax=4, aspect="auto")
    yy, xx = np.where(Q.values < .05)
    ax.scatter(xx, yy, s=28, color="white", edgecolor=INK, lw=.8)
    ax.set_xticks(range(len(order)), order, rotation=90, fontsize=8); ax.set_title(title); ax.grid(False)
axes[0].set_yticks(range(len(rows)), [label[r].split(" (")[0] for r in rows], fontsize=9)
cb = fig.colorbar(im, ax=axes, shrink=.7); cb.set_label("−log10 p   (1.3 = p 0.05, 2 = p 0.01)")
plt.show()
""")

md("## 6. Why the Congress \"effects\" are artifacts\nThe strongest naive result was *a Democratic House raises high-school attainment growth by 0.62 pp/yr*. But Democrats held the House continuously 1955–1994, exactly when attainment was rising fastest because older, less-schooled cohorts were dying out. The party dummy is just an era marker. Add a time trend and the sign flips.")
code(r"""
s = panel.loc[1965:2025, "hs_attain_change"]
fig, ax = plt.subplots(figsize=(11, 3.8))
for yr, dh in panel.loc[1965:2025, "dem_house"].items():
    ax.axvspan(yr - .5, yr + .5, color=D if dh else R, alpha=.10, lw=0)
ax.bar(s.index, s.values, color=GREY, width=.75)
z = np.polyfit(s.index, s.values, 2); ax.plot(s.index, np.polyval(z, s.index), color=INK, lw=2, label="smooth trend")
ax.set_title("High-school attainment growth (pp/yr) with House control shaded: the decline is a trend, not a party switch")
ax.legend(frameon=False); plt.tight_layout(); plt.show()
display(rot[(rot.outcome == "hs_attain_change") & (rot.term == "dem_house")][["lag", "coef", "coef_trend", "p_trend", "p_rotation"]].round(3))
""")

md("## 7. The alternative hypothesis: inherited conditions\nEach dot is a term. x = unemployment in the inauguration year (what the president inherited); y = average yearly change in unemployment over the term. High starting unemployment tends to fall on its own, and Democrats inherited worse labour markets (7.6% vs 5.2% on average). Lines are the fitted model with a common slope; the vertical gap between them is the party effect *after* adjusting for inheritance.")
code(r"""
t = term_vals[term_vals.outcome == "unemp_change"].copy()
t["u0"] = panel.loc[t.term_start, "unemp"].values
t["Dm"] = (t.party == "D").astype(int)
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), sharey=True)
for ax, (name, mask) in zip(axes, [("All terms 1901–2024", t.term_start >= 1901), ("Post-WWII terms 1949–2024", t.term_start >= 1949)]):
    s = t[mask]
    X = np.column_stack([np.ones(len(s)), s.Dm, s.u0]); b = np.linalg.lstsq(X, s.value, rcond=None)[0]
    xs = np.linspace(s.u0.min(), s.u0.max(), 50)
    for dm, col, lab in [(1, D, "Democratic"), (0, R, "Republican")]:
        ss = s[s.Dm == dm]
        ax.scatter(ss.u0, ss.value, s=55, color=col, edgecolor=SURF, lw=1, label=lab, zorder=3)
        ax.plot(xs, b[0] + b[1] * dm + b[2] * xs, color=col, lw=1.6)
    a = alt[(alt.outcome == "unemp_change") & (alt["sample"].str.startswith("all" if "All" in name else "post"))].iloc[0]
    ax.set_title(f"{name}\nraw gap {a.raw_gap:+.2f} → adjusted {a.gap_adj_inherited:+.2f} pp/yr (perm. p = {a.p_perm_adj:.3f})", fontsize=10)
    ax.axhline(0, color=INK2, lw=.8); ax.set_xlabel("Unemployment rate in inauguration year (%)")
    label_points(ax, s.u0, s.value, [f"{p.split()[-1]} {int(y)}" for p, y in zip(s.president, s.term_start)])
axes[0].set_ylabel("Avg yearly change in unemployment during term (pp)"); axes[0].legend(frameon=False)
plt.tight_layout(); plt.show()
display(Markdown("**Inherited-conditions adjustment, all outcomes tested**")); display(alt.round(3))
display(Markdown("**Post-WWII stress test: + linear trend, and leave-one-term-out range**")); display(stress.round(3))
""")

md("## 8. Machine-learning check (scikit-learn)\nA ridge model forecasts each outcome one year ahead using only its own past, war/depression flags and a trend, retrained every year (expanding window). Then party features are added. Bars show the % reduction in out-of-sample forecast error from adding party; grey ticks are what shuffled (fake) party labels achieve on average. Party information beats fake labels nowhere after correction.")
code(r"""
m = ml.sort_values("oos_gain_pct")
clip = m.oos_gain_pct.clip(lower=-40)
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.barh(range(len(m)), clip, color=[D if (g > 0 and q < .05) else GREY for g, q in zip(m.oos_gain_pct, m.q_bh)], height=.6)
ax.scatter(m.null_mean_gain_pct.clip(lower=-40), range(len(m)), marker="|", s=200, color=INK, label="average with shuffled party labels")
for i, (_, r) in enumerate(m.iterrows()):
    note = f"p={r.p_perm:.2f}, q={r.q_bh:.2f}" + (f"  (actual {r.oos_gain_pct:.0f}%, bar clipped)" if r.oos_gain_pct < -40 else "")
    ax.text(max(clip.iloc[i], 0, r.null_mean_gain_pct) + 1.5, i, note, va="center", fontsize=8, color=INK2)
ax.set_yticks(range(len(m)), [label[o].split(" (")[0] for o in m.outcome]); ax.axvline(0, color=INK2, lw=.8)
ax.set_xlabel("% reduction in forecast error from adding party features (right = party helps)")
ax.set_xlim(-45, 32)
ax.set_title("Knowing who governed does not improve forecasts")
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12))
ax.grid(axis="y", visible=False); plt.tight_layout(); plt.show()
display(ml.round(3))
""")

md("## 9. Reverse causality\nThe economy in an election year vs whether the incumbent party held the White House. Bad years tend to hand power to the challenger, which is why the next president often inherits a recovery.")
code(r"""
fig, ax = plt.subplots(figsize=(10, 3.2))
rng = np.random.default_rng(1)
for kept, col, name in [(1, INK2, "Incumbent party kept the White House"), (0, GREY, "Incumbent party lost")]:
    s = elec[elec.incumbent_kept == kept]
    yv = kept + rng.uniform(-.12, .12, len(s))
    ax.scatter(s.gdp_growth, yv, s=45, color=col, edgecolor=SURF, label=name)
    ax.vlines(s.gdp_growth.mean(), kept - .3, kept + .3, color=col, lw=2.5)
    ax.set_ylim(-.5, 1.5)
    label_points(ax, s.gdp_growth.values, yv, [str(int(e)) for e in s.election], frac=0.06)
ax.set_yticks([0, 1], ["Lost", "Kept"]); ax.axvline(0, color=INK2, lw=.8)
ax.set_xlabel("Real GDP per capita growth in the election year (%)")
ax.set_title(f"Mean growth: kept {elec[elec.incumbent_kept==1].gdp_growth.mean():.1f}%  vs  lost {elec[elec.incumbent_kept==0].gdp_growth.mean():.1f}%")
plt.tight_layout(); plt.show()
""")

md("## 10. Full output tables\nEvery results file, unabridged. Scroll inside each table.")
code(r"""
for f in sorted(RES.glob("*.csv")):
    display(Markdown(f"### `results/{f.name}`"))
    display(pd.read_csv(f).round(4))
""")
code(r"""
display(Markdown("### `data/panel.csv` (the analysis dataset, one row per year)"))
display(panel.round(3))
""")

md("## 11. Plot any outcome yourself\nChange the name in the last line to any column of `panel` (levels like `unemp`, `poverty`, `life_exp`, `gdp_pc`, `oil_nom` work too).")
code(r"""
def plot_outcome(col, y0=1900, y1=2025, shade="pres"):
    s = panel[col].loc[y0:y1].dropna()
    fig, ax = plt.subplots(figsize=(12, 3.6))
    key = {"pres": "dem_pres", "house": "dem_house", "senate": "dem_senate"}[shade]
    for yr, dem in panel.loc[s.index.min():s.index.max(), key].items():
        ax.axvspan(yr - .5, yr + .5, color=D if dem else R, alpha=.10, lw=0)
    ax.plot(s.index, s.values, color=INK)
    ax.set_title(f"{label.get(col, col)}   (shading: {shade} party)"); plt.show()

print("Columns you can plot:", ", ".join(panel.select_dtypes("number").columns))
plot_outcome("unemp", shade="pres")
""")

nb["cells"] = C
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
out = Path(__file__).with_name("explore.ipynb")
nbf.write(nb, out)
print("wrote", out)
