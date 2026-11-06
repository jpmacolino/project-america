"""Builds conventional_wisdom.xlsx for Study v2.

One row per confirmatory test group: what each side claims, what conventional wisdom expects,
the meaningful-effect size, and the keep/cut decision. The researcher's own expectation is the
null (no difference) for every row, so it is recorded once on the How to use sheet, not per row.
Prior research is kept on a separate context sheet and is not used by any test.
"""
import sys
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.comments import Comment

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rows_v2 import ROWS, NA  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent.parent / "conventional_wisdom.xlsx")

PARTY = ["D better", "R better", "No difference", "Contested"]
IDEO = ["Liberal better", "Conservative better", "No difference", "Contested"]
REMAP = {"Unsure": "Contested", "Fade": "Contested", "Bigger early": "Contested"}

def cw(v):
    return REMAP.get(v, v)

def opts(o):
    return [("Contested" if x == "Unsure" else x) for x in o]

HEAD = ["ID", "Family", "Outcome or contrast", "Units", "\"Better\" means",
        "What the left / Democrats claim", "What the right / Republicans claim",
        "Conventional wisdom: which party does better", "Conventional wisdom: which ideology does better",
        "Meaningful size, hand-set (per yr)",
        "Claude's suggestion", "Case for the suggestion", "Case against it",
        "YOUR call", "Notes", "Effective call", "Confirmatory tests"]
WID = [6, 18, 38, 13, 24, 30, 30, 20, 22, 14, 16, 40, 40, 15, 32, 13, 12]
EDIT = [8, 9, 14, 15]          # yellow, editable

F = "Arial"
body = Font(name=F, size=10)
hdr_font = Font(name=F, bold=True, color="FFFFFF", size=10)
hdr_fill = PatternFill("solid", fgColor="1F3A5F")
edit_hdr = PatternFill("solid", fgColor="B8860B")
in_fill = PatternFill("solid", fgColor="FFF2B3")
grey = PatternFill("solid", fgColor="EDEDED")
thin = Side(style="thin", color="D0D0D0")
border = Border(top=thin, bottom=thin, left=thin, right=thin)
wrap = Alignment(wrap_text=True, vertical="top")

wb = Workbook()
h = wb.active
h.title = "How to use"
h.sheet_view.showGridLines = False
h.column_dimensions["A"].width = 32
h.column_dimensions["B"].width = 95
lines = [
    ("Study v2: conventional wisdom and scope", None),
    ("Researcher's expectation", "No difference between the parties (or ideologies) on any outcome: the null hypothesis. "
     "Recorded once here, for every row."),
    ("What this file records", "What conventional wisdom says each side delivers, written down before any data is pulled. "
     "It is context for write-ups only: a result that runs against conventional wisdom gets flagged as a surprise. "
     "It does not change any test."),
    ("Where to type", "Yellow columns on the Conventional wisdom sheet: the two conventional-wisdom columns (pre-filled "
     "by Claude from each side's own claims; change any you disagree with), YOUR call, and Notes."),
    ("\"Better\" means", "Each row says which direction counts as better, e.g. falling unemployment, or a gap narrowing for "
     "the disadvantaged group. \"D better\" = conventional wisdom says that happens more under Democrats."),
    ("\"Contested\"", "Both sides claim the same benefit (e.g. GDP growth), so conventional wisdom has no single answer."),
    ("Keep / cut", "Claude's suggestion is shown with the case for and against. Leave YOUR call blank to accept it."),
    ("Example (row A16)", "YOUR call = Keep · Notes = deficits are set each year by Congress; worth testing separately from debt"),
    (None, None),
    ("Meaningful-size rule", "Which threshold the equivalence tests use (yellow cell below)."),
    ("Primary threshold", "Data rule, hand-set as check"),
    ("Data rule, defined", "0.3 standard deviations of the outcome's term-average values, computed from the data without "
     "reference to party. Hand-set values are in column J."),
    (None, None),
    ("Confirmatory tests if your calls stand", "=SUMIFS('Conventional wisdom'!$Q:$Q,'Conventional wisdom'!$P:$P,\"Keep\")"),
    ("Tests moved to descriptive", "=SUMIFS('Conventional wisdom'!$Q:$Q,'Conventional wisdom'!$P:$P,\"Make descriptive\")"),
    ("Tests cut", "=SUMIFS('Conventional wisdom'!$Q:$Q,'Conventional wisdom'!$P:$P,\"Cut\")"),
    ("Tests in the original draft", "=SUM('Conventional wisdom'!$Q:$Q)"),
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
        h.cell(i, 1).alignment = Alignment(vertical="top", wrap_text=True)
    if b is not None:
        c = h.cell(i, 2, b)
        c.font = body
        c.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left")
h["B11"].fill = in_fill
h["B11"].border = border
dv_thr = DataValidation(type="list", formula1='"Data rule, hand-set as check,Hand-set, data rule as check,Larger of the two"')
h.add_data_validation(dv_thr)
dv_thr.add("B11")
for r in (14, 15, 16, 17):
    h.cell(r, 2).font = Font(name=F, bold=True, size=11)

ws = wb.create_sheet("Conventional wisdom")
ws.freeze_panes = "D2"
for j, (t, w) in enumerate(zip(HEAD, WID), start=1):
    c = ws.cell(1, j, t)
    c.font = hdr_font
    c.fill = edit_hdr if j in EDIT else hdr_fill
    c.alignment = Alignment(wrap_text=True, vertical="center")
    ws.column_dimensions[c.column_letter].width = w
ws.row_dimensions[1].height = 44

dv_call = DataValidation(type="list", formula1='"Keep,Make descriptive,Cut"', allow_blank=True)
dv_ideo = DataValidation(type="list", formula1='"' + ",".join(IDEO) + '"', allow_blank=True)
ws.add_data_validation(dv_call)
ws.add_data_validation(dv_ideo)
dvs = {}

ctx = wb.create_sheet("Prior research (context)")
ctx["A1"] = "Prior research and v1 results: context only"
ctx["A1"].font = Font(name=F, bold=True, size=14, color="1F3A5F")
ctx["A2"] = ("Not used in any test, threshold or decision rule. Kept only so a write-up can say when a result agrees "
             "or disagrees with earlier studies. Delete this sheet if you prefer not to see it.")
ctx["A2"].font = Font(name=F, italic=True, size=10)
ctx.merge_cells("A2:C2")
ctx["A2"].alignment = wrap
ctx.row_dimensions[2].height = 30
for j, (t, w) in enumerate([("ID", 6), ("Outcome or contrast", 40), ("Prior research and v1 result", 100)], start=1):
    c = ctx.cell(4, j, t)
    c.font = hdr_font
    c.fill = hdr_fill
    ctx.column_dimensions[c.column_letter].width = w

for i, r in enumerate(ROWS, start=2):
    (rid, fam, out, units, better, lc, rc, dp, di, prior, sesoi, sug, cfor, cagainst, ntests, popts) = r
    vals = [rid, fam, out, units, better, lc or "-", rc or "-", cw(dp), cw(di), sesoi, sug, cfor, cagainst,
            None, None, f'=IF(N{i}="",K{i},N{i})', ntests]
    for j, v in enumerate(vals, start=1):
        c = ws.cell(i, j, v)
        c.font = body
        c.alignment = wrap
        c.border = border
    ws.cell(i, 1).font = Font(name=F, size=10, bold=True)
    for j in EDIT:
        ws.cell(i, j).fill = in_fill
    po = tuple(opts(popts))
    if po not in dvs:
        dvs[po] = DataValidation(type="list", formula1='"' + ",".join(po) + '"', allow_blank=True)
        ws.add_data_validation(dvs[po])
    if dp == NA:
        ws.cell(i, 8).fill = grey
    elif rid != "E1":
        dvs[po].add(f"H{i}")
    if di == NA:
        ws.cell(i, 9).fill = grey
    else:
        dv_ideo.add(f"I{i}")
    dv_call.add(f"N{i}")
    k = i + 3
    for j, v in enumerate([rid, out, prior], start=1):
        c = ctx.cell(k, j, v)
        c.font = body
        c.alignment = wrap
        c.border = border

last = len(ROWS) + 1
ws.conditional_formatting.add(f"K2:K{last}", FormulaRule(formula=['K2<>"Keep"'], font=Font(name=F, bold=True, color="8A5A00")))
ws.auto_filter.ref = f"A1:Q{last}"
ws.cell(1, 8).comment = Comment("Pre-filled by Claude from each side's own claims (modern parties, ~1970s on). "
                                "Edit any value you think misstates conventional wisdom.", "Claude")
ws.cell(1, 10).comment = Comment("Hand-set smallest effect worth caring about, per year, in the row's units "
                                 "(Claude's judgment; v1 values reused for v1 outcomes).", "Claude")
wb.active = 0
wb.save(OUT)
print("saved", OUT)
