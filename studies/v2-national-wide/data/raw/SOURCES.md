# Study v2 raw data: source manifest

Pull began 2026-11-06 (after tag `v2-prereg`, which is on GitHub). Every file in this folder is listed here with
its source URL, series ID and pull date. Files are stored exactly as the source served them, or, where a source
serves a large multi-country file or an Excel workbook, as a verbatim row/column extract with the full file's SHA-256
recorded (`owid/owid_provenance.json`, `census/census_provenance.json`). Census workbooks are read in the browser by a
small hand-written reader (unzip + sheet XML), so cell values are exactly as stored in the workbook. The one legacy `.xls` (HIB-1)
is read by a hand-written OLE/BIFF8 reader; its numbers are written in JavaScript's shortest round-trip form. `checksums.sha256` covers every file.

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
| `census/CENSUS_hstpov2__colsA_D.csv` | Census CPS ASEC Historical Poverty Table 2 | hstpov2.xlsx, cols A and D, race blocks (see `census/census_provenance.json`) | A6, B6 | 2026-11-06 |
| `census/CENSUS_hstpov3__colsA_E_M_Q.csv` | Census CPS ASEC Historical Poverty Table 3 | hstpov3.xlsx, All Races, under 18 / 18-64 / 65+ | B8 | 2026-11-06 |
| `census/CENSUS_f01ar__2025dollars_colsA_C-G.csv` | Census Table F-1 | f01ar.xlsx, 2025-dollar block: 20th/40th/60th/80th/95th percentile limits | B1 | 2026-11-06 |
| `census/CENSUS_f07ar__AllFamilies_colsA_D.csv` | Census Table F-7 | f07ar.xlsx, all families, median income, 2025 dollars (first-listed row in duplicate years matches FRED for all 72 overlapping years) | A17 | 2026-11-06 |
| `census/CENSUS_h05__colsA_D.csv` | Census Table H-5 | h05.xlsx, median household income, 2025 dollars, race blocks (see `census/census_provenance.json`) | B7 | 2026-11-06 |
| `census/CENSUS_p40__colsA_B.csv` | Census Table P-40 | p40.xlsx, all races, women's median earnings as % of men's (full-time, year-round) | B10 | 2026-11-06 |
| `census/CENSUS_p38ar__colsA_C_D_F_G.csv` | Census Table P-38 | p38ar.xlsx, median earnings of men and women (full-time, year-round), current and 2025 dollars | B10 check | 2026-11-06 |
| `census/CENSUS_hst_attain02__25plus_colsA_B.csv` | Census CPS Table A-2 | hst_attain02.xlsx, % of people 25+ with 4 yrs high school or more / 4 yrs college or more | A13, A14 | 2026-11-06 |
| `census/CENSUS_orghihistt1__lines70-133.txt` | Census Table HI-1 (original CPS estimates, 1987-2005) | time-series/original/orghihistt1.txt, all races both sexes, % not covered (verbatim lines) | A18 | 2026-11-06 |
| `census/CENSUS_hihistt1b__AllRacesBothSexes_pct_cols0_10.csv` | Census Table HIB-1 (CPS, 1999-2012) | time-series/hib/hihistt1b.xls, all races both sexes, % not covered | A18 | 2026-11-06 |
| `census/CENSUS_hhi01__AllRacesBothSexes_colsA_B_V_W.csv` | Census Table HHI-01 (CPS, 2017-2025) | time-series/hic/hhi01.xlsx, all persons, uninsured number and % | A18 | 2026-11-06 |
| `census/CENSUS_hic04_acs__US_Uninsured.csv` | Census Table HIC-4_ACS (ACS, 2008-2025) | time-series/acs/hic04_acs.xlsx, United States, uninsured number and % | A18 | 2026-11-06 |
| `census/CENSUS_bds2023.csv` | Census Business Dynamics Statistics, 2023 release | bds/tables/time-series/2023/bds2023.csv (complete file, byte-identical) | A23 (`estabs_entry_rate`) | 2026-11-06 |
| `eia/EIA_MER_T01.01__TEPRBUS_annual.csv` | EIA Monthly Energy Review, Table 1.1 | csv.php?tbl=T01.01, MSN `TEPRBUS` total primary energy production, annual (YYYY13) rows (see `eia/eia_provenance.json`) | A25 | 2026-11-06 |
| `shiller/SHILLER_ie_data__JanDec_1899plus.csv` | Robert Shiller, `ie_data.xls` (now hosted at shillerdata.com, linked from his Yale data page) | sheet Data: January and December rows, P, D, CPI, real total return price (see `shiller/shiller_provenance.json`) | A20 | 2026-11-06 |
| `voteview/HSall_members.csv` | Voteview | static/data/out/members/HSall_members.csv (complete file) | `voteview/HSall_parties.csv` | Voteview | static/data/out/parties/HSall_parties.csv (complete file) | C, E cross-check | 2026-11-06 |
| `omb/OMB_hist01z2_fy2027.xlsx` | OMB Historical Tables, FY2027 Budget | Table 1.2, receipts/outlays/surplus as % of GDP (complete file; see `omb/omb_provenance.json`) | A16, A21 check | 2026-11-06 |
| `omb/OMB_hist03z1_fy2027.xlsx` | OMB Historical Tables, FY2027 Budget | Table 3.1, outlays by function incl. national defense, $ and % GDP, 1940+ (complete file) | defense luck control | 2026-11-06 |
| `omb/OMB_hist07z1_fy2027.xlsx` | OMB Historical Tables, FY2027 Budget | Table 7.1, federal debt at end of year, incl. held by the public % GDP, 1940-2025 (complete file) | A15 (1940+) | 2026-11-06 |

FRED annual and quarterly aggregates are FRED's own (`fam=avg`); FRED leaves incomplete periods blank (e.g. 2026).

`_transcripts/` keeps the exact text copied out of the browser and the two scripts that rebuilt the files from it
(`decode_fred.py`, `decode_owid.py`), so each rebuild can be re-run and re-checked.

**Large and binary files** (Voteview, OMB) were fetched the same way, then saved through the browser's own download (approved by the researcher
2026-11-06) and copied here; the copy's SHA-256 equals the hash the browser computed on the fetched bytes.

## Still to pull (all sites approved by the researcher on 2026-11-06)

| Item | Planned source |
| --- | --- |
| A19 homicide rate 1900+ | CDC/NCHS vital statistics (HSUS for early years); no long-run US series found on OWID |
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

## Decided after part 4 (logged in `../../DEVIATIONS.md`, 2026-11-06)

- **A18:** CPS changes 1987-2008 (within consistent pieces), ACS changes 2009-2025; changes touching 2020 missing.
- **B10:** ratio computed from P-38 medians for all years; P-40 is the check (they differ only in 1969: 60.5 vs 58.9).
