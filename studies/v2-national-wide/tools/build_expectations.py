"""Builds studies/v2-national-wide/expectations.xlsx (the reviewable expectations + scope sheet)."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.comments import Comment

from pathlib import Path
OUT = str(Path(__file__).resolve().parent / "expectations.xlsx")  # overwrites your edits: only for a fresh copy
PARTY = ["D better", "R better", "No difference", "Unsure"]
IDEO = ["Liberal better", "Conservative better", "No difference", "Unsure"]
NA = "n/a"

# id, family, outcome, units, better_means, left_claim, right_claim, default_party, default_ideo,
# prior, sesoi, suggestion, case_for, case_against, tests, party_options
ROWS = [
 ("A1", "A National averages", "Real GDP per capita growth", "pp/yr", "Faster growth",
  "Public investment and demand support raise growth", "Lower taxes and deregulation raise growth",
  "Unsure", "Unsure", "Both sides claim it. Blinder & Watson: +1.8 pp/yr under D 1947-2013, over half explained by luck. v1: +1.95 raw, not significant after correction.",
  "0.75", "Keep", "Core measure of the economy; the most-cited partisan claim.", "Hard to argue for cutting.", 2, PARTY),
 ("A2", "A National averages", "Change in unemployment rate", "pp/yr", "Falling unemployment",
  "Full employment is a priority", "Growth creates jobs", "D better", "Liberal better",
  "Bartels: 1.5 pp lower under D 1948-2001. v1: the one finding that held post-WWII after adjusting for inheritance (exploratory).",
  "0.25", "Keep", "Central to v1's alternative hypothesis.", "Hard to argue for cutting.", 2, PARTY),
 ("A3", "A National averages", "CPI inflation", "pp/yr", "Lower inflation",
  "Not a central claim", "Fiscal discipline keeps it lower", "R better", "Conservative better",
  "Bartels: no post-war difference. v1: higher under D over the century (world wars under D); none post-WWII.",
  "1.00", "Keep", "Tests a clear right-side claim.", "Hard to argue for cutting.", 2, PARTY),
 ("A4", "A National averages", "Real hourly wage growth (1965+)", "pp/yr", "Faster wage growth",
  "Labor protections and minimum wage raise pay", "Growth and tight labor markets raise pay", "D better", "Liberal better",
  "v1: essentially zero gap (+0.03).", "0.50", "Keep", "Directly what a worker feels.", "Short series (1965+).", 2, PARTY),
 ("A5", "A National averages", "Real median household income growth (1985+)", "pp/yr", "Faster growth",
  "Middle-class policy raises incomes", "Tax cuts raise take-home income", "Unsure", "Unsure",
  "v1: +0.95 under D, not significant; only 10 terms.", "0.75", "Keep", "Best single 'typical family' measure.",
  "Only ~10 terms; A17 covers 1947+.", 2, PARTY),
 ("A6", "A National averages", "Change in official poverty rate (1960+)", "pp/yr", "Falling poverty",
  "Transfers and labor policy lower poverty", "Growth lifts the poor", "D better", "Liberal better",
  "v1: fell 0.52 pp/yr faster under D (raw p=0.054); held after inheritance adjustment (exploratory).",
  "0.25", "Keep", "Directly in the null hypothesis.", "Hard to argue for cutting.", 2, PARTY),
 ("A7", "A National averages", "Change in top-1% income share (1914-2022)", "pp/yr", "Falling top share (more equal)",
  "Progressive taxes shrink it", "No claim to shrink it", "D better", "Liberal better",
  "v1: no gap (-0.02).", "0.25", "Keep", "Long series back to 1914.", "Overlaps B2 (bottom 50% vs top 1%).", 2, PARTY),
 ("A8", "A National averages", "Change in family-income Gini (1948+)", "x100 pts/yr", "Falling Gini (more equal)",
  "Redistribution narrows inequality", "No claim to narrow it", "D better", "Liberal better",
  "v1: fell faster under D; strongest exploratory result after adjustment (p=0.002).", "0.25", "Keep",
  "Consistency check on v1's exploratory finding.", "Same years as v1, so it cannot confirm v1.", 2, PARTY),
 ("A9", "A National averages", "Real crude oil price change", "%/yr", "Lower prices for consumers",
  "No claim", "\"Drill\" policies lower energy prices", "R better", "Conservative better",
  "v1: equivalence shown, party effect within +/-10%/yr. World-market price.", "10", "Keep",
  "Cheap placebo: a world price should show no effect; a 'hit' would warn of a flawed design.",
  "Already settled in v1; one more test in the family.", 2, PARTY),
 ("A10", "A National averages", "Real all-commodities price change (1914+)", "%/yr", "Lower prices",
  "No claim", "No claim", "No difference", "No difference",
  "v1: equivalence shown, within +/-3%/yr.", "3", "Keep", "Second placebo outcome.", "Already settled in v1.", 2, PARTY),
 ("A11", "A National averages", "Change in life expectancy (1902-2023)", "yrs/yr", "Rising life expectancy",
  "Health coverage improves it", "Growth and innovation improve it", "Unsure", "Unsure",
  "v1: +0.08 under D, not significant.", "0.10", "Keep", "The most basic quality-of-life measure.",
  "Driven by medicine and pandemics more than politics.", 2, PARTY),
 ("A12", "A National averages", "Infant mortality change (1950+)", "log %/yr", "Falling infant mortality",
  "Medicaid and maternal care lower it", "Growth and innovation lower it", "D better", "Liberal better",
  "v1: no gap.", "1.00", "Keep", "Sensitive to health policy for the poor.", "Very smooth series; little year-to-year signal.", 2, PARTY),
 ("A13", "A National averages", "Change in % adults with high school (1965+)", "pp/yr", "Faster rise",
  "School funding raises attainment", "School choice raises attainment", "Unsure", "Unsure",
  "v1: apparent D-House effect was an era artifact (sign flipped with a trend).", "0.20", "Keep",
  "Education was in the original null.", "A stock that moves with generations; little room for a 1-4 year effect.", 2, PARTY),
 ("A14", "A National averages", "Change in % adults with bachelor's (1965+)", "pp/yr", "Faster rise",
  "Student aid raises completion", "Market and workforce programs", "D better", "Liberal better",
  "v1: no gap.", "0.10", "Keep", "Education was in the original null.", "Same stock problem as A13.", 2, PARTY),
 ("A15", "A National averages", "Federal debt, % of GDP (change)", "pp/yr", "Falling debt ratio",
  "Not a central claim", "Lower deficits and debt", "R better", "Conservative better",
  "Not tested in v1. Debt ratio rose sharply under several Republican presidents after 1980.", "1.00", "Keep",
  "Burden passed to later citizens; a core right-side claim.", "Moves with growth and inflation, not only policy.", 2, PARTY),
 ("A16", "A National averages", "Federal surplus/deficit, % of GDP (level)", "pp of GDP", "Smaller deficit",
  "Not a central claim", "Lower deficits", "R better", "Conservative better",
  "Not tested in v1.", "0.50", "Cut",
  "Near-duplicate of A15: the deficit is most of the change in debt. Two tests of one idea.",
  "The deficit is what politicians set year to year; debt also moves with growth and inflation, so they differ.", 2, PARTY),
 ("A17", "A National averages", "Real median family income growth (1947+)", "pp/yr", "Faster growth",
  "Middle-class policy raises incomes", "Tax cuts raise take-home income", "Unsure", "Unsure",
  "Not tested in v1. Bartels: middle quintiles grew faster under D 1948-2001.", "0.75", "Keep",
  "Typical-family measure with a long series.", "Overlaps B1 (income by percentile).", 2, PARTY),
 ("A18", "A National averages", "Uninsured rate (change, 1987+)", "pp/yr", "Falling uninsured rate",
  "Coverage expansion lowers it", "Market reforms lower costs; no claim on the rate", "D better", "Liberal better",
  "Not tested in v1. Big drops cluster around the 2014 ACA expansion.", "0.25", "Keep",
  "Direct, measurable result of policy.", "Short series dominated by one law (the ACA).", 2, PARTY),
 ("A19", "A National averages", "Homicide rate (log change)", "%/yr", "Falling homicide",
  "Social programs reduce crime", "Tougher enforcement reduces crime", "R better", "Conservative better",
  "Not tested in v1.", "3", "Keep", "Safety is quality of life; both sides make claims.",
  "Policing is mostly local; demographics and drugs drive trends.", 2, PARTY),
 ("A20", "A National averages", "Real S&P 500 total return", "pp/yr", "Higher returns",
  "Not a central claim", "Business-friendly policy raises returns", "R better", "Conservative better",
  "Santa-Clara & Valkanov ('presidential puzzle'): returns were higher under D. A possible 'against expectation' case.",
  "5", "Keep", "Tests a common claim and a known puzzle.",
  "About half of households own stocks; not 'the average citizen'. Very noisy.", 2, PARTY),
 ("B1", "B Who benefits", "Income growth: 20th vs 95th percentile (1947+)", "pp/yr gap", "Bottom gains relative to top",
  "Policy for working families", "Growth lifts all", "D better", "Liberal better",
  "Bartels: 20th grew 2.0 pp/yr faster under D; 95th no different (1948-2001).", "0.75", "Keep",
  "Bartels' central claim; the main reason for v2.", "Hard to argue for cutting.", 2, PARTY),
 ("B2", "B Who benefits", "Income share: bottom 50% vs top 1% (1913+)", "pp/yr gap", "Bottom gains relative to top",
  "Progressive policy", "Growth lifts all", "D better", "Liberal better",
  "v1 top-1% share: no gap.", "0.25", "Keep", "Longest distributional series (1913+).", "Overlaps A7.", 2, PARTY),
 ("B3", "B Who benefits", "Wage growth: 10th vs 90th percentile (1973+)", "pp/yr gap", "Low-wage gains relative to high",
  "Minimum wage and unions", "Tight labor markets", "D better", "Liberal better",
  "Not tested in v1.", "0.50", "Keep", "Wages, not just income.", "Short series.", 2, PARTY),
 ("B4", "B Who benefits", "Wealth share: bottom 50% vs top 1% (1913+)", "pp/yr gap", "Bottom gains relative to top",
  "Estate and capital taxes", "Ownership and markets", "D better", "Liberal better",
  "Not tested in v1. Wealth estimates are model-based and revised often.", "0.25", "Keep",
  "Wealth is where inequality is largest.", "Data quality is weaker than income data.", 2, PARTY),
 ("B5", "B Who benefits", "Unemployment: Black vs White (1972+)", "pp/yr gap", "Gap narrows",
  "Civil-rights and anti-poverty policy", "Growth and opportunity", "D better", "Liberal better",
  "Not tested in v1.", "0.25", "Keep", "Minority outcomes are a stated interest.", "Hard to argue for cutting.", 2, PARTY),
 ("B6", "B Who benefits", "Poverty: Black vs White (1959+)", "pp/yr gap", "Gap narrows",
  "Anti-poverty programs", "Growth and opportunity", "D better", "Liberal better",
  "Not tested in v1.", "0.25", "Keep", "Longest racial-gap series.", "Gaps in early years (Black annual from 1966).", 2, PARTY),
 ("B7", "B Who benefits", "Median household income: Black vs White (1967+)", "pp/yr gap", "Gap narrows",
  "Equal-opportunity policy", "Growth and opportunity", "D better", "Liberal better",
  "Not tested in v1.", "0.75", "Keep", "Income, not just jobs.", "Overlaps B5 and B6.", 2, PARTY),
 ("B8", "B Who benefits", "Poverty: children vs 65+ (1959+)", "pp/yr gap", "Child poverty falls relative to elderly",
  "Child benefits (e.g. child tax credit)", "Growth; family policy", "Unsure", "Unsure",
  "Not tested in v1. Elderly poverty fell steeply with Social Security under both parties.", "0.25", "Keep",
  "Generational fairness; both sides make claims.", "Driven by Social Security indexing more than party.", 2, PARTY),
 ("B9", "B Who benefits", "Unemployment: women vs men (1948+)", "pp/yr gap", "Women gain relative to men",
  "No specific claim", "No specific claim", "No difference", "No difference",
  "Not tested in v1.", "0.25", "Keep", "Long series; tests sex differences.",
  "Neither side claims an effect, so it may only add a test.", 2, PARTY),
 ("B10", "B Who benefits", "Women-to-men earnings ratio (1960+)", "pp/yr", "Ratio rises (gap narrows)",
  "Equal-pay policy narrows the gap", "No specific claim", "D better", "Liberal better",
  "Not tested in v1. Strong long-run upward trend.", "0.25", "Keep", "Direct measure of a stated policy goal.",
  "Trend-heavy; risk of the era artifact seen in v1 (the rotation test guards against it).", 2, PARTY),
 ("B11", "B Who benefits", "Unemployment: no diploma vs BA+ (1992+)", "pp/yr gap", "Less-educated gain",
  "Worker training, minimum wage", "Growth", "D better", "Liberal better",
  "Not tested in v1. Only ~8 terms of data.", "0.25", "Make descriptive",
  "About 8 terms of data: almost no chance of detecting anything, so it mainly dilutes the family.",
  "Dropping it can look like hiding a group; a low-power test usually just comes back inconclusive.", 2, PARTY),
 ("B12", "B Who benefits", "Per-capita income: poorest vs richest region (1929+)", "pp/yr gap", "Poorest region catches up",
  "Federal investment in poor regions", "Low taxes attract business", "Unsure", "Unsure",
  "Not tested in v1. The South's catch-up spans both parties.", "0.75", "Keep",
  "Region is where party meaning changed (the South).", "Not a direct policy target; catch-up is a century-long trend.", 2, PARTY),
 ("C1", "C Configuration", "Democratic House seat share", "per 10 pp of seats", "Follows the A outcomes",
  "", "", "Unsure", NA, "v1: House 'effects' were era artifacts.", "per outcome", "Keep",
  "Uses margins, not just yes/no control.", "v1 showed Congress effects vanish under the rotation test.", 6, PARTY),
 ("C2", "C Configuration", "Democratic Senate seat share", "per 10 pp of seats", "Follows the A outcomes",
  "", "", "Unsure", NA, "v1: Senate 'effects' were era artifacts.", "per outcome", "Keep",
  "Same as C1.", "Same as C1.", 6, PARTY),
 ("C3", "C Configuration", "President's party is filibuster-proof", "yes/no", "Bigger party effect",
  "", "", "Amplifies", NA, "Not tested in v1. Few years qualify (mostly FDR, LBJ, Obama 2009).", "per outcome", "Keep",
  "Tests whether real legislative power matters.", "Few qualifying years; low power.", 6,
  ["Amplifies", "Weakens", "No difference", "Unsure"]),
 ("C4", "C Configuration", "Unified vs divided government", "yes/no", "Which is better for citizens",
  "Unified government delivers", "Gridlock restrains spending", "Unsure", NA,
  "v1: unified-government effects were era artifacts.", "per outcome", "Keep",
  "Classic question with arguments on both sides.", "Already tested in v1 (T3).", 6,
  ["Unified better", "Divided better", "No difference", "Unsure"]),
 ("D1", "D Horizons", "Effects 4, 8 and 10 years after a party takes over", "core outcomes", "Shape over time",
  "", "", "Fade", NA, "Alesina: partisan effects fade after about 2 years. Blinder & Watson: gap persists across whole terms.",
  "per outcome", "Keep", "Tests slow-acting policy, which v1 could not see.", "Few independent long windows.", 18,
  ["Grow", "Persist", "Fade", "No effect", "Unsure"]),
 ("D2", "D Horizons", "Effects 20 years after a party takes over", "core outcomes", "Shape over time",
  "", "", "Fade", NA, "Only ~6 non-overlapping 20-year windows since 1900.", "per outcome", "Make descriptive",
  "Six independent windows cannot support a confirmatory test.",
  "Long-run effects (education, infrastructure) are the whole point of some policies; dropping it hides them.", 6,
  ["Grow", "Persist", "Fade", "No effect", "Unsure"]),
 ("E1", "E Ideology", "President's ideology score (replaces party for presidents)", "per 0.25 on the scale", "Same as A/B rows",
  "", "", NA, "Same as A/B", "Presidents are strongly partisan, so their score mostly repeats their party.", "per outcome",
  "Make descriptive", "Mostly duplicates the party tests; 32 tests for little new information.",
  "Ideology does vary within a party (Eisenhower vs Reagan; Carter vs LBJ), which party labels cannot capture.", 32,
  IDEO),
 ("F1", "F Timing", "Party gap in quarters 1-8 vs 9-16 of a term (1947+)", "quarterly", "When effects appear",
  "", "", "Bigger early", NA, "Alesina's rational partisan theory predicts early effects only.", "per outcome", "Keep",
  "Cheap (4 tests) and directly tests a named theory.", "Adds timing, not new terms; still ~19 post-war terms.", 4,
  ["Bigger early", "Bigger late", "Same", "Unsure"]),
]

HEAD = ["ID", "Family", "Outcome or contrast", "Units", "\"Better\" means",
        "Left / Democratic claim", "Right / Republican claim",
        "Default: party (D vs R)", "Default: ideology (liberal vs conservative)", "Research prior and v1 result",
        "Meaningful size, hand-set (per yr)",
        "YOUR expectation: party", "YOUR expectation: ideology", "YOUR confidence",
        "Matches default?",
        "Claude's suggestion", "Case for the suggestion", "Case against it",
        "YOUR call", "Notes", "Effective call", "Confirmatory tests"]
WID = [6, 18, 38, 13, 24, 28, 28, 16, 18, 46, 14, 17, 19, 13, 13, 16, 40, 40, 15, 30, 13, 12]

F = "Arial"
hdr_font = Font(name=F, bold=True, color="FFFFFF", size=10)
hdr_fill = PatternFill("solid", fgColor="1F3A5F")
in_fill = PatternFill("solid", fgColor="FFF2B3")
grey_fill = PatternFill("solid", fgColor="EDEDED")
body = Font(name=F, size=10)
thin = Side(style="thin", color="D0D0D0")
border = Border(top=thin, bottom=thin, left=thin, right=thin)
wrap = Alignment(wrap_text=True, vertical="top")

wb = Workbook()
# ---------------- How to use ----------------
h = wb.active
h.title = "How to use"
h.sheet_view.showGridLines = False
h.column_dimensions["A"].width = 30
h.column_dimensions["B"].width = 95
lines = [
    ("Study v2 expectations and scope", None),
    ("What this is", "Every confirmatory test planned for Study v2, with the expected direction written down before any data is pulled. "
     "Fill in your own expectations and your keep/cut decisions; nothing here is a result."),
    ("Where to type", "Only the yellow columns on the Expectations sheet: YOUR expectation (party), YOUR expectation (ideology), "
     "YOUR confidence, YOUR call and Notes. Most have drop-down lists."),
    ("\"Better\" means", "Each row says what direction counts as better, e.g. falling unemployment, or a gap narrowing for the "
     "disadvantaged group. \"D better\" = that direction happens more under Democratic control."),
    ("Defaults", "Default columns record the conventional expectation from each side's own claims (modern parties, ~1970s on). "
     "\"Unsure\" means both sides claim it or neither does. Defaults are context for write-ups, not evidence."),
    ("Matches default?", "Fills itself in once you choose an expectation."),
    ("Keep / cut", "Claude's suggestion is shown with the case for and against. If YOUR call is blank, the suggestion stands."),
    ("Example (row A3)", "YOUR expectation: party = R better · ideology = Conservative better · confidence = Medium · YOUR call = Keep"),
    (None, None),
    ("Meaningful-size rule", "Choose which threshold the equivalence tests use (yellow cell below)."),
    ("Primary threshold", "Data rule, hand-set as check"),
    ("Data rule, defined", "0.3 standard deviations of the outcome's term-average values, computed from the data without "
     "reference to party. 0.3 SD is a conventional 'small but real' effect. Hand-set values are in column K."),
    (None, None),
    ("Confirmatory tests if your calls stand", "=SUMIFS(Expectations!$V:$V,Expectations!$U:$U,\"Keep\")"),
    ("Tests moved to descriptive", "=SUMIFS(Expectations!$V:$V,Expectations!$U:$U,\"Make descriptive\")"),
    ("Tests cut", "=SUMIFS(Expectations!$V:$V,Expectations!$U:$U,\"Cut\")"),
    ("Tests in the original draft", "=SUM(Expectations!$V:$V)"),
    (None, None),
    ("Test counting", "A and B rows count 2 tests (party, Congress ideology). E1 holds the 32 president-ideology tests. "
     "C rows: 6 core outcomes each. D1: 3 horizons x 6. F1: 4 quarterly series."),
]
for i, (a, b) in enumerate(lines, start=1):
    if a and b is None:
        h.cell(i, 1, a).font = Font(name=F, bold=True, size=14, color="1F3A5F")
        continue
    if a:
        h.cell(i, 1, a).font = Font(name=F, bold=True, size=10)
    if b is not None:
        c = h.cell(i, 2, b)
        c.font = body
        c.alignment = Alignment(wrap_text=True, vertical="top")
    h.cell(i, 1).alignment = Alignment(vertical="top", wrap_text=True)
thr = h["B11"]
thr.fill = in_fill
thr.border = border
dv_thr = DataValidation(type="list", formula1='"Data rule, hand-set as check,Hand-set, data rule as check,Larger of the two"', allow_blank=False)
h.add_data_validation(dv_thr)
dv_thr.add("B11")
for r in (14, 15, 16, 17):
    h.cell(r, 2).alignment = Alignment(horizontal="left")
    h.cell(r, 2).font = Font(name=F, bold=True, size=11)

# ---------------- Expectations ----------------
ws = wb.create_sheet("Expectations")
ws.freeze_panes = "D2"
for j, (t, w) in enumerate(zip(HEAD, WID), start=1):
    c = ws.cell(1, j, t)
    c.font = hdr_font
    c.fill = hdr_fill
    c.alignment = Alignment(wrap_text=True, vertical="center")
    ws.column_dimensions[c.column_letter].width = w
ws.row_dimensions[1].height = 42
INPUT_COLS = [12, 13, 14, 19, 20]
for c in INPUT_COLS:
    ws.cell(1, c).fill = PatternFill("solid", fgColor="B8860B")

dv_conf = DataValidation(type="list", formula1='"Low,Medium,High"', allow_blank=True)
dv_call = DataValidation(type="list", formula1='"Keep,Make descriptive,Cut"', allow_blank=True)
dv_ideo = DataValidation(type="list", formula1='"' + ",".join(IDEO) + '"', allow_blank=True)
for dv in (dv_conf, dv_call, dv_ideo):
    ws.add_data_validation(dv)
party_dvs = {}

for i, r in enumerate(ROWS, start=2):
    (rid, fam, out, units, better, lc, rc, dp, di, prior, sesoi, sug, cfor, cagainst, ntests, popts) = r
    vals = [rid, fam, out, units, better, lc, rc, dp, di, prior, sesoi, None, None, None,
            f'=IF(AND(L{i}="",M{i}=""),"",IF(AND(OR(L{i}="",L{i}=H{i}),OR(M{i}="",M{i}=I{i},I{i}="n/a")),"Matches","Differs"))',
            sug, cfor, cagainst, None, None, f'=IF(S{i}="",P{i},S{i})', ntests]
    for j, v in enumerate(vals, start=1):
        c = ws.cell(i, j, v)
        c.font = body
        c.alignment = wrap
        c.border = border
    for c in INPUT_COLS:
        ws.cell(i, c).fill = in_fill
    key = tuple(popts)
    if key not in party_dvs:
        dv = DataValidation(type="list", formula1='"' + ",".join(popts) + '"', allow_blank=True)
        ws.add_data_validation(dv)
        party_dvs[key] = dv
    if rid == "E1":   # president-ideology row: only the ideology column applies
        ws.cell(i, 12).value = NA
        ws.cell(i, 12).fill = grey_fill
        dv_ideo.add(f"M{i}")
    else:
        party_dvs[key].add(f"L{i}")
        if di == NA:
            ws.cell(i, 13).value = NA
            ws.cell(i, 13).fill = grey_fill
        else:
            dv_ideo.add(f"M{i}")
    dv_conf.add(f"N{i}")
    dv_call.add(f"S{i}")
    ws.cell(i, 1).font = Font(name=F, size=10, bold=True)

last = len(ROWS) + 1
ws.conditional_formatting.add(f"O2:O{last}", FormulaRule(formula=[f'O2="Differs"'], font=Font(name=F, bold=True, color="B03A2E")))
ws.conditional_formatting.add(f"O2:O{last}", FormulaRule(formula=[f'O2="Matches"'], font=Font(name=F, color="2E7D32")))
ws.conditional_formatting.add(f"P2:P{last}", FormulaRule(formula=[f'P2<>"Keep"'], font=Font(name=F, bold=True, color="8A5A00")))
ws.auto_filter.ref = f"A1:V{last}"
ws.cell(1, 11).comment = Comment("Hand-set smallest effect worth caring about, per year, in the row's units. "
                                 "Source: Claude's judgment (v1 values reused for v1 outcomes). See How to use for the data-derived rule.", "Claude")
ws.cell(1, 22).comment = Comment("Number of confirmatory tests this row stands for. Used by the totals on How to use.", "Claude")
wb.active = 0
wb.save(OUT)
print("saved", OUT, len(ROWS), "rows")
