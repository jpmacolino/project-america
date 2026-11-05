# Does party control matter? A hypothesis test, 1900–2025

**Study v1 (frozen, tag `v1.0-party-baseline`).** Later studies live in their own folders and never modify v1.
Write-up: "Does Party Control Matter? A Hypothesis Test, 1900–2025" (Claude doc, Nov 2026).

Tests H0: the party controlling the Presidency, House and Senate (and unified vs divided
government) has no effect on national outcomes for the average American — economy & prices,
poverty & inequality, commodity prices, and education & health.

## Run

```
pip install -r requirements.txt
python src/build_dataset.py    # data/raw/* -> data/panel.csv
python src/analysis.py         # primary tests T1-T5 -> results/          (~30 s)
python src/robustness.py       # trend, rotation, sub-period, ML checks   (~15 min, ML step dominates)
python src/alternative.py      # exploratory inherited-conditions follow-up
```

## Explore the results visually

- **No install:** open `notebooks/explore.html` in any browser. It is the executed notebook with every chart and full results table.
- **Interactive:** `pip install -r requirements.txt`, then `jupyter notebook notebooks/explore.ipynb`
  (or open the .ipynb in VS Code with the Jupyter extension) and choose Run All.
  Section 11 has a `plot_outcome()` helper for plotting any series with party shading.
- `notebooks/make_notebook.py` regenerates the notebook from scratch.

## Layout

| Path | Contents |
| --- | --- |
| `data/raw/USGDPpresidents.csv` | MeasuringWorth real GDP per capita, CPI, unemployment (Romer/Coen/BLS), via R package Ecdat |
| `data/raw/browser_series.txt` | FRED, Our World in Data and Census series pulled 2026-11-04, with source notes per line |
| `data/raw/incomeInequality.csv` | Ecdat Census family-income percentiles 1947-2012 (reference, not used in tests) |
| `src/build_dataset.py` | Party-control coding by year (presidents and Congress majorities) and outcome transformations |
| `src/analysis.py` | Pre-specified tests: annual HAC regressions (T1-T3), term-level tests (T4), block permutation (T5), BH-FDR, TOST equivalence |
| `src/robustness.py` | Cubic-trend models, rotation test, sub-periods, scikit-learn out-of-sample test |
| `src/alternative.py` | Exploratory: Democratic-term gaps adjusted for inherited unemployment, post-WWII stress tests |
| `results/` | Every table cited in the write-up (`summary.json` is the headline) |

## Headline

- 0 of 210 primary annual coefficients survive FDR once long party runs are respected (rotation test);
  0 of 14 term-level presidential tests survive FDR.
- Equivalence (TOST) is shown only for real oil and all-commodity prices: the president's party
  provably has no meaningful effect there. Other outcomes are inconclusive (underpowered: ~31 terms).
- Exploratory alternative: post-WWII, unemployment and family-income inequality fell faster under
  Democratic presidents even after adjusting for inherited unemployment (p = 0.008 and 0.002);
  over the full century the Democratic edge is mostly inherited conditions.
