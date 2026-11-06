# Project America: instructions for Claude

## The question
Is party (or ideology) a meaningless label when it comes to improving the lives of the American people?
The researcher's expectation is the null (no difference) on every outcome. Work as an impartial data
scientist: no side is favoured, and a result that surprises either side is reported plainly.

## Where things are
- Repo: `C:\dev\project-america` (GitHub `jpmacolino/project-america`). Start every session by reading
  `ROADMAP.md`, then the current study's `PREREGISTRATION.md` and `DEVIATIONS.md`.
- Study v1 (repo root, tag `v1.0-party-baseline`): frozen. Never modify its files.
- Study v2 (`studies/v2-national-wide/`, tag `v2-prereg`): pre-registered, 116 confirmatory tests.
  `conventional_wisdom.xlsx` holds per-outcome context and keep/cut decisions.

## Rules
1. Pre-register before looking. A study's plan is committed and tagged before its data is pulled.
2. After the tag, any change to the plan goes in `DEVIATIONS.md` (date, change, reason, whether results
   had been seen). Never silently edit a frozen plan.
3. Never edit a finished study. Follow-ups go in a new folder under `studies/`.
4. Confirmatory vs exploratory: anything not named in the pre-registration is exploratory and labelled so
   in every table and write-up.
5. Prior research and conventional wisdom are context only. They never set a threshold, test or decision.
6. Primary p-values respect long party runs (term-level permutation for presidents, rotation tests for
   Congress, margins and ideology). Benjamini-Hochberg FDR within families. TOST for "no meaningful effect".
7. Every number in a write-up must trace to a file in that study's `results/`.

## Data
- Store raw pulls in the study's `data/raw/` with source URL, series ID and pull date for each series.
- The cloud sandbox blocks most data sites. What has worked: raw.githubusercontent.com (e.g. Rdatasets),
  and the built-in browser with same-origin `fetch()` on FRED, Our World in Data and Census (Excel files
  parsed with SheetJS). Ask the researcher before using a new site.
- Values copied out of the browser must be written to files verbatim, then spot-checked.

## Code and git
- Python (pandas, statsmodels, scipy, scikit-learn, matplotlib). Fix random seeds so results reproduce.
- Re-run key scripts on the researcher's machine before calling a result final.
- Small, descriptive commits. Freeze points get annotated tags. Remind the researcher to push tags
  (VS Code: Git: Push Tags, or `"git.followTagsWhenSync": true`).

## Writing
Plain language for a general reader. Lead with the answer. Say "fail to reject" rather than "proved no
effect" unless an equivalence test supports it. Flag results that run against conventional wisdom as
context, not evidence.
