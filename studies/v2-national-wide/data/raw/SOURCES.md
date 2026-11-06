# Study v2 raw data: source manifest

Pull began 2026-11-06 (after tag `v2-prereg`, which is on GitHub). Every file in this folder is listed here with
its source URL, series ID and pull date. Files are stored exactly as the source served them, or, where a source
serves a large multi-country file, as a verbatim row extract with the full file's SHA-256 recorded
(`owid/owid_provenance.json`). `checksums.sha256` covers every file.

**How browser pulls were checked.** FRED, OWID and Census block scripted downloads, so (as in v1) they were
fetched with same-origin `fetch()` in the built-in browser. The browser computed a SHA-256 of the exact text it
received; the file written here was rebuilt from that text and its SHA-256 was required to match. Every file
below matched.

## Pulled

| File | Source | Series / URL | Used for | Pulled |
| --- | --- | --- | --- | --- |
| `RDATASETS_Ecdat_USGDPpresidents.csv` | Rdatasets mirror of R `Ecdat::USGDPpresidents` (MeasuringWorth; Treasury debt) | raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/Ecdat/USGDPpresidents.csv | A1, A2, A3, A15, A21; inherited unemployment; war flags | 2026-11-06 (byte-identical to v1 copy) |
| `RDATASETS_Ecdat_USGDPpresidents_doc.html` | Rdatasets documentation page for the above | .../doc/Ecdat/USGDPpresidents.html | definitions | 2026-11-06 |
| `fred/FRED_PPIACO.csv` | FRED, BLS PPI all commodities | `PPIACO`, `fq=Annual&fam=avg` | A10 | 2026-11-06 |
| `fred/FRED_AHETPI.csv` | FRED, BLS avg hourly earnings, prod. & nonsupervisory | `AHETPI`, annual avg | A4 | 2026-11-06 |
| `fred/FRED_MEHOINUSA672N.csv` | FRED, Census real median household income | `MEHOINUSA672N` | A5 | 2026-11-06 |
| `fred/FRED_GINIALLRF.csv` | FRED, Census Gini, all families | `GINIALLRF` | A8 | 2026-11-06 |
| `fred/FRED_MEFAINUSA672N.csv` | FRED, Census real median family income (1953+) | `MEFAINUSA672N` | A17 check (primary: Census F-7, 1947+) | 2026-11-06 |
| `fred/FRED_GPDICA.csv` | FRED, BEA real gross private domestic investment, chained 2017 $ | `GPDICA` | A22 | 2026-11-06 |
| `fred/FRED_OPHNFB.csv` | FRED, BLS nonfarm business output per hour | `OPHNFB`, annual avg of quarterly index | A24 | 2026-11-06 |
| `fred/FRED_LNU04000001.csv` / `...02` | FRED, BLS unemployment rate, men / women 16+ (NSA) | annual avg | B9 | 2026-11-06 |
| `fred/FRED_LNU04000003.csv` / `...06` / `...09` | FRED, BLS unemployment rate, White / Black / Hispanic | annual avg | B5 | 2026-11-06 |
| `fred/FRED_LNU04027659.csv` / `...660` / `...689` / `...662` | FRED, BLS unemployment 25+, no diploma / HS / some college / BA+ | annual avg | B11 (descriptive) | 2026-11-06 |
| `fred/FRED_A939RX0Q048SBEA.csv` | FRED, BEA real GDP per capita, quarterly | native quarterly | F | 2026-11-06 |
| `fred/FRED_UNRATE.csv` | FRED, BLS unemployment rate | `fq=Quarterly&fam=avg` | F | 2026-11-06 |
| `fred/FRED_CPIAUCSL.csv` | FRED, BLS CPI-U, SA | `fq=Quarterly&fam=avg` | F | 2026-11-06 |
| `fred/FRED_PAYEMS.csv` | FRED, BLS total nonfarm payrolls | `fq=Quarterly&fam=avg` | F | 2026-11-06 |
| `owid/OWID_crude-oil-prices__OWID_WRL.csv` | OWID / Energy Institute Statistical Review 2026 | grapher `crude-oil-prices` | A9; oil-shock luck control | 2026-11-06 |
| `owid/OWID_life-expectancy__USA.csv` | OWID (Riley; Zijdeman; HMD; UN WPP) | grapher `life-expectancy` | A11 | 2026-11-06 |
| `owid/OWID_infant-mortality__USA.csv` | OWID / UN IGME | grapher `infant-mortality` | A12 | 2026-11-06 |
| `owid/OWID_income-share-top-1-before-tax-wid__USA.csv` | OWID / WID | grapher `income-share-top-1-before-tax-wid` | A7 | 2026-11-06 |

FRED annual and quarterly aggregates are FRED's own (`fam=avg`); FRED leaves incomplete periods blank (e.g. 2026).

`_transcripts/` keeps the exact text copied out of the browser and the two scripts that rebuilt the files from it
(`decode_fred.py`, `decode_owid.py`), so each rebuild can be re-run and re-checked.

## Still to pull (all sites approved by the researcher on 2026-11-06)

| Item | Planned source |
| --- | --- |
| A6 poverty; B6 poverty by race; B8 poverty by age | Census CPS historical poverty Tables 2 and 3 (`www2.census.gov/programs-surveys/cps/tables/time-series/historical-poverty-people/hstpov2.xlsx`, `hstpov3.xlsx`) |
| A13, A14 attainment | Census CPS Table A-2 (`hst_attain02.xlsx`) |
| A17 median family income 1947+ | Census Table F-7 (`.../historical-income-families/f07ar.xlsx`) |
| B1 family income at percentile cut-offs | Census Table F-1 (`.../historical-income-families/f01ar.xlsx`) |
| B7 household income by race | Census Table H-5 (`.../historical-income-households/h05.xlsx`) |
| B10 women-to-men earnings ratio | Census Table P-38 / P-40 (`.../historical-income-people/p38.xlsx`, `p40.xlsx`) |
| A18 uninsured rate | Census historical health insurance tables (CPS 1987+, ACS) |
| A23 establishment entry rate | Census Business Dynamics Statistics, national file |
| A19 homicide rate 1900+ | CDC/NCHS vital statistics (HSUS for early years); no long-run US series found on OWID |
| A20 real S&P total return | Shiller long-run data (`ie_data.xls`) |
| A25 primary energy production | EIA Monthly Energy Review Table 1.1 |
| A15/A21 check; defense % GDP | OMB Historical Tables 1.2, 3.1, 7.1 |
| B2, B4 income and wealth shares | WID (`sptinc`, `shweal`, p0p50 / p50p90 / p90p100 / p99p100) |
| B3 wage percentiles | EPI State of Working America Data Library |
| B12 regional per-capita income | BEA regional accounts (SAINC1, 8 regions) |
| C, E treatments | Voteview `HSall_members.csv` |
| Luck controls | Banque de France LTP; Fernald (FRBSF); Maddison Project 2023; Romer–Romer shocks |

## Decisions on data issues

Six places where the data and the frozen plan did not line up exactly were put to the researcher on
2026-11-06 and decided before any analysis. They are logged in `../../DEVIATIONS.md`: A15 debt definition,
carried-forward values treated as missing, quarterly unemployment from 1948Q1, Hispanic unemployment from 1974,
BLS annual productivity, and the Wieland & Yang (2020) Romer-Romer extension.
