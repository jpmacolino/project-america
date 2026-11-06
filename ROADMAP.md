# Project America: research roadmap

Working question: is party (or ideology) a meaningless label when it comes to improving
the lives of the American people?

## Rules of the road

Claude sessions follow `CLAUDE.md`.

1. **Pre-register before looking.** Each new study gets a `PREREGISTRATION.md` (hypotheses,
   outcomes, groups, tests, thresholds, expected direction per outcome) committed and tagged
   *before* any new data is pulled or analysed. The git timestamp is the proof.
2. **Never edit a finished study.** Each study is frozen with a tag; follow-ups go in new folders.
3. **Every claim traces to a file.** Results tables live in each study's `results/`.

## Status

| Study | Status | Tag |
| --- | --- | --- |
| v1: party control vs 14 national outcomes, 1900-2025 | Done, frozen | `v1.0-party-baseline` |
| v2: wider and more rigorous national test (see below) | Pre-registered (116 confirmatory tests); next: data pull | `v2-prereg` |
| v2b: ideology (DW-NOMINATE) in place of party | After v2, same pipeline | - |
| Luck decomposition (oil, productivity, defense, Fed shocks) | Control layer, applied to v2 and v2b | - |
| State-level study (governors, close elections, state law) | Separate project chat | - |

## v2 scope (agreed 2026-11-04, not yet pre-registered)

- **Who benefits:** outcomes by group (income quintiles and top 5%/1%, wage percentiles,
  race and ethnicity, age, sex, education, region where data exist). Key test is the
  interaction: does the D-R gap differ *between* groups, not just within one.
- **Horizons:** 1 year, term, 5, 8, 10 and 20 years; cumulative party exposure; local
  projections (effect h years after a switch); lead/placebo tests.
- **Quarterly macro data** (1947+) for timing precision; annual elsewhere.
- **Seat margins and all eight President/House/Senate configurations**, plus filibuster-proof
  (60) and veto-proof (2/3) majorities.
- **New outcomes:** federal debt and deficits, uninsured rate, homicide/crime, stock returns,
  plus Bartels' percentile income growth.
- **Same tests, same standards:** HAC + term-level + rotation/permutation, BH-FDR across the
  whole family, TOST equivalence for "no meaningful effect".
