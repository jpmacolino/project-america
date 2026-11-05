# Pre-registration: Study v2 — Who benefits, how long, and does ideology matter?

**Status: DRAFT for review. Not yet frozen.**
When approved, this file is committed and tagged `v2-prereg` *before any new data is pulled*.
After the tag, the only allowed changes are entries in `DEVIATIONS.md`, each dated and explained.

| | |
| --- | --- |
| Project | Project America (`C:\dev\project-america`) |
| Builds on | Study v1, tag `v1.0-party-baseline` |
| Drafted | 2026-11-05 |
| Folder for this study | `studies/v2-national-wide/` (v1 files at the repo root are never modified) |

---

## 1. Why this study exists

Study v1 tested whether the party controlling the Presidency, House and Senate moved 14 national
averages between 1900 and 2025. It failed to reject the null. It showed equivalence (no meaningful effect)
only for oil and commodity prices. It surfaced one exploratory pattern: after WWII, unemployment and
inequality fell faster under Democratic presidents, even after adjusting for inherited conditions.

v1 left five gaps that this study closes:

1. It measured **averages**, not **who benefits**. Bartels' central claim is distributional.
2. It looked only **0–2 years ahead**. Slow-acting policy was invisible.
3. It used **annual** data. That blurs when a president's economy actually begins.
4. It treated control as **yes/no** and lumped all divided governments together.
5. It used **party labels**, which changed meaning over the century (the Southern Democrats; the
   realignment of the 1960s–90s).

It also adds outcomes v1 left out, and a "luck" layer (oil shocks, productivity, defense, Fed policy)
to separate party effects from good or bad fortune.

**A note on honesty about v1's finding.** The post-WWII unemployment and inequality pattern came from
looking at 1949–2024 data. Re-testing it on the same years cannot confirm it. In this study it is a
**consistency check** only. True confirmation must come from data that did not exist when it was found:
future years (a living test) and the separate state-level study.

---

## 2. Hypotheses

The overarching null, in plain words: **party is a meaningless label when it comes to the well-being of
the American people.**

Formally, once inherited conditions are accounted for:

| ID | Null hypothesis (H0) | Alternative (H1, two-sided) |
| --- | --- | --- |
| H0-A | Party control has no effect on any **national average** outcome. | It affects at least one. |
| H0-B | The party effect is the **same for every group** (no group gains more under one party than another). | It differs between at least one pair of groups. |
| H0-C | The **configuration** of control (which branches, by what margin) has no effect. | It does. |
| H0-D | Party control has no **cumulative** effect at 4–20 year horizons. | It does. |
| H0-E | **Ideology** (DW-NOMINATE) of the President and Congress has no effect on averages or on group gaps. | It does. |
| H0-F | Partisan effects are the **same early and late** in a term (no "first-two-years" effect). | They differ. |

The strict null "party is meaningless" is rejected if **any** confirmatory test survives the decision
rules in Section 9. It cannot be proven true. We can only show, outcome by outcome, that effects are smaller
than a pre-declared meaningful size (equivalence).

---

## 3. Treatments

### 3.1 Party (Parts A–D, F)

| Variable | Definition |
| --- | --- |
| `dem_pres` | 1 if a Democrat is President (inauguration year goes to the incoming president, as in v1) |
| `dem_house`, `dem_senate` | 1 if Democrats hold the chamber majority (v1 coding, including its edge cases) |
| `n_dem_branches` | 0–3: how many of the three Democrats hold. Summary measure for configuration |
| `config` | 8-level President-House-Senate pattern (e.g. `RDD`). Reference level: `RRR`. Seven occur 1900–2025; `DDR` never has |
| `house_dem_share`, `senate_dem_share` | Democratic share of seats, centred at 50% (from Voteview member lists) |
| `filibuster_proof` | 1 if the President's party holds enough Senate seats to end a filibuster under the rule in force that year (two-thirds of those voting 1917–1974; 60 of 100 from 1975) |
| `veto_proof_opposition` | 1 if the party opposing the President holds two-thirds of both chambers |

### 3.2 Ideology (Part E)

**Source.** Voteview DW-NOMINATE, first dimension, as published in Voteview's member file. That file
puts members of both chambers and presidents on one scale across Congresses.

**What the scale means.** Dimension 1 runs from about −1 to +1 and is estimated purely from roll-call
votes. Researchers read it as views on **government's role in the economy**:

- **Liberal (negative):** more federal spending, redistribution, regulation and labor protection.
- **Conservative (positive):** lower taxes, less spending, lighter regulation, more reliance on markets.

Dimension 2 historically captured splits over **civil rights and region**. It is what made 1950s
Southern Democrats vote with Republicans on some issues. Dimension 2 is reported descriptively only.

**Treatments:**

| Variable | Definition |
| --- | --- |
| `pres_dim1` | The President's score |
| `house_median_dim1`, `senate_median_dim1` | Score of the median member of each chamber (the pivotal vote) |
| `congress_dim1` | Average of the two chamber medians (primary Congress measure) |
| `polarization` | Distance between the Democratic and Republican medians, averaged over the chambers |

**Named bins.** These are for description and write-ups only. Inference always uses the continuous score,
so the cut-points cannot be tuned to produce a result. They are fixed now:

| Score | Label |
| --- | --- |
| ≤ −0.40 | Strongly liberal |
| −0.40 to −0.15 | Liberal |
| −0.15 to +0.15 | Moderate |
| +0.15 to +0.40 | Conservative |
| ≥ +0.40 | Strongly conservative |

---

## 4. Outcomes

All outcomes are tested as annual changes (or growth rates), as in v1, unless stated. "SESOI" is the
smallest effect size of interest per year, used for equivalence tests. Sources are named here. If a
source cannot be obtained, the outcome is dropped and logged in `DEVIATIONS.md`. No substitute is added
as confirmatory after data has been seen.

### 4.1 Family A — national averages (20 outcomes)

The 14 v1 outcomes, with their v1 definitions and thresholds, plus:

| Outcome | Source | From | SESOI |
| --- | --- | --- | --- |
| Federal debt held by public, % GDP (change) | MeasuringWorth via Ecdat; OMB Historical Tables | 1900 | 1.0 pp/yr |
| Federal surplus/deficit, % GDP (level) | Same | 1900 | 0.5 pp |
| Real median family income growth | Census Table F-7 / F-1 | 1947 | 0.75 pp/yr |
| Uninsured rate (change) | Census CPS/ACS health insurance tables | 1987 | 0.25 pp/yr |
| Homicide rate (log change) | CDC/NCHS vital statistics (historical series via HSUS or OWID) | 1900 | 3 %/yr |
| Real S&P total stock return | Shiller long-run data | 1900 | 5 pp/yr |

### 4.2 Family B — who benefits (group gaps)

For each dimension, every group's own D−R gap is reported, but the **confirmatory test is one contrast
per dimension**: the difference in the party effect between the two pre-named groups below. This is the
test of whether one party favours one group *relative to* another.

| # | Dimension | Measure | Groups reported | Confirmatory contrast | Source, start |
| --- | --- | --- | --- | --- | --- |
| B1 | Family income | Real income growth at percentile cut-offs | 20th, 40th, 60th, 80th, 95th | 20th vs 95th | Census F-1/F-3, 1947 |
| B2 | Top/bottom shares | Pre-tax income share (change) | Bottom 50%, middle 40%, top 10%, top 1% | Bottom 50% vs top 1% | WID, 1913 |
| B3 | Wages | Real hourly wage growth | 10th, 50th, 90th percentile | 10th vs 90th | EPI State of Working America data (CPS), 1973 |
| B4 | Wealth | Wealth share (change) | Bottom 50%, top 1% | Bottom 50% vs top 1% | WID (Saez–Zucman), 1913 |
| B5 | Race & ethnicity | Unemployment rate (change) | White, Black, Hispanic | Black vs White | BLS, Black 1972 (Black-and-other 1954) |
| B6 | Race & ethnicity | Poverty rate (change) | White, Black, Hispanic | Black vs White | Census poverty Table 2, 1959 |
| B7 | Race & ethnicity | Real median household income growth | White, Black, Hispanic | Black vs White | Census H-5, 1967 |
| B8 | Age | Poverty rate (change) | Under 18, 18–64, 65+ | Under 18 vs 65+ | Census poverty Table 3, 1959 |
| B9 | Sex | Unemployment rate (change) | Men, women | Women vs men | BLS, 1948 |
| B10 | Sex | Women-to-men median earnings ratio (change) | — | Ratio itself | Census, 1960 |
| B11 | Education | Unemployment rate (change) | No HS diploma, HS, some college, BA+ | No diploma vs BA+ | BLS, 1992 |
| B12 | Region | Real per-capita personal income growth | 8 BEA regions | Poorest vs richest region in 1929 | BEA, 1929 |

B11 starts in 1992 and has very little power. It is included so a null cannot be blamed on omission.

### 4.3 Core outcomes (used where a family needs a short list)

Real GDP per capita growth, unemployment change, CPI inflation, poverty-rate change, 20th-percentile
family income growth, life-expectancy change.

---

## 5. Horizons (Family D)

v1 tested effects 0–2 years out. Here:

| Method | Horizons | What it asks |
| --- | --- | --- |
| Local projections: change in outcome from year t−1 to t+h, regressed on party at t, with inherited conditions | h = 4, 8, 10, 20 years | How far does an outcome move h years after a party takes over? |
| Cumulative exposure: share of the past N years with a Democratic President, against the N-year change | N = 4, 8, 10, 20 | Do long stretches of one-party rule accumulate? |
| Placebo leads: party at t+1 … t+4 against the change in year t | — | Future party control must *not* predict the past. A "hit" means reverse causality or confounding |

Confirmatory tests: local projections for the 6 core outcomes at h = 4, 8, 10, 20 (24 tests).
Exposure and placebo results are reported but not confirmatory.

**Caveat, stated in advance.** 125 years contain about six non-overlapping 20-year windows.
Horizons of 10 and 20 years count as **descriptive** unless they also pass the rotation test.

---

## 6. Timing precision (Family F, quarterly)

Quarterly data from 1947Q1 for: real GDP per capita growth, unemployment (monthly averaged to quarters),
CPI inflation and payroll employment growth. Sources: BEA and BLS via FRED.

Convention (following Blinder & Watson): the inauguration quarter belongs to the outgoing President.
Confirmatory test (4 tests): is the D−R gap in quarters 1–8 of a term different from quarters 9–16?
This tests the "rational partisan" theory that partisan effects appear only early in a term.

Quarterly data adds timing precision, not many new independent observations (still about 19 post-war terms).

---

## 7. Configuration and margins (Family C)

Confirmatory tests: 4 measures × 6 core outcomes, attributed with a 1-year lag (24 tests):
`house_dem_share`, `senate_dem_share`, `filibuster_proof`, and unified versus divided government.

Each `config` level's mean is reported descriptively, with its year count. Levels with fewer than 8 years
(`DRD` 6, `RRD` 2) are never interpreted on their own.

---

## 8. Luck controls (Part C, applied to every family)

Every confirmatory model is run twice, without and with these controls. Results are reported side by side.

| Control | Definition | Source | From |
| --- | --- | --- | --- |
| Oil shock | Hamilton "net oil price increase": log real oil price minus its 3-year maximum, if positive | Computed from the v1 oil series | 1900 |
| Productivity | Total factor productivity growth | Banque de France Long-Term Productivity Database (1890+); Fernald (1947+) as a check | 1890 |
| Defense spending | Defense outlays, % GDP | OMB Historical Tables (1940+); war-year flags before | 1900 |
| Monetary policy shocks | Romer–Romer shocks, as extended in later research | Published series | 1969 |
| World growth | Real GDP per capita growth outside the US | Maddison Project | 1900 |

The question this answers: once luck is removed, how much of any party gap is left?

---

## 9. Statistical plan and decision rules

**Inherited conditions.** Primary models adjust for unemployment in the year a President takes office and
for the outcome's own lagged value. This is the lesson of v1, where inheritance explained most of the
century-long Democratic edge. Unadjusted results are reported as secondary.

**Primary p-values respect long party runs.** v1 showed that ordinary regression p-values are badly
over-confident when a party holds a branch for decades. The primary p-value for every test is therefore
one of these:

- **Presidential treatments:** a permutation test that shuffles party labels across whole 4-year terms.
- **Congress, margin and ideology treatments:** a rotation test that slides the treatment history
  against the outcome.

Newey–West (HAC) p-values are reported alongside.

**Multiple testing.**

- Benjamini–Hochberg false-discovery rate, q < 0.05, within each family: A (20), B (12), C (24),
  D (24), E (64: 2 ideology treatments × 20 averages + 2 × 12 group contrasts), F (4), 148 in all.
- Also reported: one global correction across all 148 tests.

**Equivalence.** TOST at α = 0.05 against each outcome's SESOI. An outcome is "no meaningful effect" only
if its 90% confidence interval lies entirely inside ±SESOI.

**Where SESOI comes from (to be settled in `expectations.xlsx`, "How to use" sheet).** Two rules:
(a) hand-set per outcome, as in v1 (column K of the workbook); (b) data rule: 0.3 standard deviations of the
outcome's term-average values, computed from the data without reference to party. Because the data rule never
looks at party, it can be computed after the data pull without biasing the test. The workbook records which rule
is primary and which is the sensitivity check.

**Verdicts, fixed now:**

| Result | Verdict |
| --- | --- |
| A test survives within-family FDR **and** its primary (permutation/rotation) p is below 0.05 **and** it keeps its sign with luck controls | **Reject H0** for that outcome or contrast |
| Survives FDR but loses significance with luck controls | Association real, **not attributable** to party |
| Fails FDR, equivalence shown | **No meaningful effect** (null accepted for that outcome) |
| Fails FDR, no equivalence | **Inconclusive** |
| Survives global FDR across all 148 | Flagged as the study's **headline** finding |

The overarching "party is meaningless" null is rejected if at least one test earns **Reject H0**.

**Power, stated in advance.** v1's smallest reliably detectable presidential effects were about
3.2 pp/yr for GDP growth and 0.95 pp/yr for unemployment change. Distributional contrasts have fewer years
and will be weaker. Inconclusive results are expected and will be reported as such, not as "no effect".

---

## 10. Expectations table (context, not evidence)

**The authoritative, row-by-row version is `expectations.xlsx`** (one row per confirmatory test group, with
defaults, the researcher's own expectations, and keep/cut decisions). It is frozen with this file. The table below
is the summary.

This records what each side commonly *claims* its policies deliver, written down before the results.
A result that runs against a side's own claim is flagged **"against expectation"** in write-ups, as human
context only. It adds no statistical weight.

The labels below describe the modern parties (roughly the 1970s onward). Before the realignment, party
labels mapped poorly onto these positions. That is exactly why Part E uses ideology scores.

| Outcome | Commonly claimed by the left / Democrats | Commonly claimed by the right / Republicans |
| --- | --- | --- |
| GDP growth | Public investment and demand support raise growth | Lower taxes and deregulation raise growth |
| Unemployment | Full employment is a priority; falls faster | Growth creates jobs; falls faster |
| Inflation | Not a central claim | Fiscal discipline keeps it lower |
| Poverty, bottom-quintile income | Transfers and labour policy lower poverty | Growth lifts the poor; dependence is reduced |
| Top income and wealth shares | Progressive taxes shrink them | No claim to shrink them |
| Racial gaps (unemployment, poverty, income) | Civil-rights and anti-poverty policy narrow them | Economic growth and opportunity narrow them |
| Child vs elderly poverty | Both fall | Both fall through growth |
| Women-to-men earnings | Equal-pay policy narrows the gap | No specific claim |
| Debt and deficits | Not a central claim | Lower deficits and debt |
| Stock returns | Not a central claim | Business-friendly policy raises returns |
| Homicide | Social programs reduce crime | Tougher enforcement reduces crime |
| Uninsured rate | Lower (coverage expansion) | Market reforms lower costs; no claim on rate |
| Oil and commodity prices | No claim | "Drill" policies lower energy prices |
| Life expectancy, infant mortality | Health coverage improves them | Growth and innovation improve them |

Where both sides claim the same direction (GDP, unemployment), any result supports one side's claim
*more than* the other's, not one side alone.

---

## 11. What counts as exploratory

Anything not named above as confirmatory is exploratory. That includes per-group gaps beyond the 12
contrasts, Dimension 2 analyses, config-level means, machine-learning checks, and any sub-period split.
Exploratory results are labelled as such in every table and write-up, and can only seed future
pre-registrations.

## 12. Procedure

1. Approve this draft (edits welcome before the freeze).
2. Commit it, then tag `v2-prereg`. Push the tag to GitHub so the timestamp is public.
3. Only then pull new data into `studies/v2-national-wide/data/raw/`, recording every source and pull date.
4. Run the confirmatory analysis exactly as written. Log any forced change in `DEVIATIONS.md`.
5. Write up: confirmatory results first, then exploratory.
6. Freeze the finished study with a tag (`v2.0`).
