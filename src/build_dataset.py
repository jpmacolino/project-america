"""Build the annual analysis panel (1900-2025): party control + outcome series.

Inputs (data/raw/):
  USGDPpresidents.csv  - Rdatasets mirror of R package Ecdat::USGDPpresidents
                         (MeasuringWorth real GDP per capita & CPI; Romer/Coen/BLS unemployment)
  incomeInequality.csv - Ecdat::incomeInequality (Census family income quintiles, 1947-2012) [reference only]
  browser_series.txt   - FRED / OWID / Census series retrieved 2026-11-04 (see header of that file)
Output:
  data/panel.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

# ---------------------------------------------------------------------------
# 1. Party control. Presidents: the party holding the office for most of the
#    calendar year (inauguration year goes to the incoming president).
#    Congress: majority party of each chamber for the Congress sitting in that year.
# ---------------------------------------------------------------------------
PRESIDENTS = [  # (first year, last year, name, party)
    (1897, 1901, "McKinley", "R"), (1902, 1908, "T. Roosevelt", "R"), (1909, 1912, "Taft", "R"),
    (1913, 1920, "Wilson", "D"), (1921, 1922, "Harding", "R"), (1923, 1928, "Coolidge", "R"),
    (1929, 1932, "Hoover", "R"), (1933, 1944, "F. Roosevelt", "D"), (1945, 1952, "Truman", "D"),
    (1953, 1960, "Eisenhower", "R"), (1961, 1962, "Kennedy", "D"), (1963, 1968, "L. Johnson", "D"),
    (1969, 1974, "Nixon", "R"), (1975, 1976, "Ford", "R"), (1977, 1980, "Carter", "D"),
    (1981, 1988, "Reagan", "R"), (1989, 1992, "G.H.W. Bush", "R"), (1993, 2000, "Clinton", "D"),
    (2001, 2008, "G.W. Bush", "R"), (2009, 2016, "Obama", "D"), (2017, 2020, "Trump", "R"),
    (2021, 2024, "Biden", "D"), (2025, 2028, "Trump", "R"),
]
# Congress number -> (House majority, Senate majority). Congress n sits in years
# 1789+2(n-1) and the following year. Sources: House Clerk "Party Divisions",
# Senate Historical Office "Party Division". Notes: 65th House organised by
# Democrats despite a GOP plurality; 72nd House flipped D after special
# elections; 107th Senate was D for most of 2001-02 (Jeffords switch, June 2001).
CONGRESS = {
    56: "RR", 57: "RR", 58: "RR", 59: "RR", 60: "RR", 61: "RR", 62: "DR", 63: "DD",
    64: "DD", 65: "DD", 66: "RR", 67: "RR", 68: "RR", 69: "RR", 70: "RR", 71: "RR",
    72: "DR", 73: "DD", 74: "DD", 75: "DD", 76: "DD", 77: "DD", 78: "DD", 79: "DD",
    80: "RR", 81: "DD", 82: "DD", 83: "RR", 84: "DD", 85: "DD", 86: "DD", 87: "DD",
    88: "DD", 89: "DD", 90: "DD", 91: "DD", 92: "DD", 93: "DD", 94: "DD", 95: "DD",
    96: "DD", 97: "DR", 98: "DR", 99: "DR", 100: "DD", 101: "DD", 102: "DD", 103: "DD",
    104: "RR", 105: "RR", 106: "RR", 107: "RD", 108: "RR", 109: "RR", 110: "DD",
    111: "DD", 112: "RD", 113: "RD", 114: "RR", 115: "RR", 116: "DR", 117: "DD",
    118: "RD", 119: "RR",
}


def party_table(y0=1897, y1=2026):
    rows = []
    for y in range(y0, y1 + 1):
        pres = next(p for p in PRESIDENTS if p[0] <= y <= p[1])
        cong = (y - 1789) // 2 + 1
        h, s = CONGRESS.get(cong, "??")
        rows.append(dict(year=y, president=pres[2], pres_party=pres[3], congress=cong,
                         house_party=h, senate_party=s))
    df = pd.DataFrame(rows)
    df["dem_pres"] = (df.pres_party == "D").astype(int)
    df["dem_house"] = (df.house_party == "D").astype(int)
    df["dem_senate"] = (df.senate_party == "D").astype(int)
    df["unified"] = ((df.pres_party == df.house_party) & (df.house_party == df.senate_party)).astype(int)
    df["unified_dem"] = (df.unified & df.dem_pres).astype(int)
    df["unified_rep"] = (df.unified & (1 - df.dem_pres)).astype(int)
    # presidential term id (4-year elective terms; successions stay in the term they inherited)
    df["term_start"] = 1897 + 4 * ((df.year - 1897) // 4)
    return df


def read_browser_series():
    out = {}
    for line in (RAW / "browser_series.txt").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        sid, _src, _units, data = line.split("|")
        out[sid] = pd.Series({int(k): float(v) for k, v in (t.split(":") for t in data.split())})
    return out


def build():
    party = party_table()
    mw = pd.read_csv(RAW / "USGDPpresidents.csv").set_index("Year")
    s = read_browser_series()
    years = pd.Index(range(1897, 2026), name="year")
    lv = pd.DataFrame(index=years)
    lv["cpi"] = mw["CPI"]
    lv["gdp_pc"] = mw["realGDPperCapita"]
    lv["unemp"] = mw["unemployment"]
    lv["fed_outlays_gdp"] = mw["fedOutlays_pGDP"] * 100
    lv["war"] = mw["war"].notna().astype(int)
    for k, name in [("FRED_PPIACO", "ppi_all"), ("FRED_AHETPI", "wage_nom"), ("FRED_MEHOINUSA672N", "med_hh_inc"),
                    ("OWID_OIL", "oil_nom"), ("FRED_GINIALLRF", "gini"), ("OWID_TOP1", "top1"),
                    ("CENSUS_POVERTY", "poverty"), ("OWID_LIFEEXP", "life_exp"), ("OWID_INFMORT", "inf_mort"),
                    ("CENSUS_HS", "hs_attain"), ("CENSUS_BA", "ba_attain")]:
        lv[name] = s[k]
    lv = lv.reset_index()

    d = lv.set_index("year")
    o = pd.DataFrame(index=d.index)
    dl = lambda x: 100 * np.log(x).diff()  # noqa: E731  annual log growth, percent
    # --- Economy & prices
    o["gdp_pc_growth"] = dl(d.gdp_pc)
    o["unemp_change"] = d.unemp.diff()
    o["inflation"] = dl(d.cpi)
    o["real_wage_growth"] = dl(d.wage_nom / d.cpi)
    o["real_med_hh_inc_growth"] = dl(d.med_hh_inc)
    # --- Poverty & inequality
    o["poverty_change"] = d.poverty.diff()
    o["top1_change"] = d.top1.diff()
    o["gini_change"] = 100 * d.gini.diff()
    o.loc[1993, "gini_change"] = np.nan  # Census CPS methodology break (computer-assisted interviewing, topcode change)
    # --- Commodities (real = deflated by CPI)
    o["real_oil_return"] = dl(d.oil_nom / d.cpi)
    o["real_commodity_return"] = dl(d.ppi_all / d.cpi)
    # --- Education & health
    o["life_exp_change"] = d.life_exp.diff()
    o["inf_mort_change"] = dl(d.inf_mort)
    # attainment published for non-consecutive years before 1964: annualise only consecutive pairs
    for c in ["hs_attain", "ba_attain"]:
        ser = d[c].dropna()
        ch = ser.diff() / pd.Series(ser.index, index=ser.index).diff()
        ch[pd.Series(ser.index, index=ser.index).diff() != 1] = np.nan
        o[c + "_change"] = ch
    panel = party.set_index("year").join(d).join(o).loc[1898:2025]
    panel.to_csv(ROOT / "data" / "panel.csv")
    return panel


if __name__ == "__main__":
    p = build()
    print(p.loc[1900:2025, ["president", "pres_party", "house_party", "senate_party", "unified"]].to_string())
