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
| `voteview/HSall_members.csv` | Voteview | static/data/out/members/HSall_members.csv (complete file) | C, E treatments | 2026-11-06 |
| `voteview/HSall_parties.csv` | Voteview | static/data/out/parties/HSall_parties.csv (complete file) | C, E cross-check | 2026-11-06 |
| `omb/OMB_hist01z2_fy2027.xlsx` | OMB Historical Tables, FY2027 Budget | Table 1.2, receipts/outlays/surplus as % of GDP (complete file; see `omb/omb_provenance.json`) | A16, A21 check | 2026-11-06 |
| `omb/OMB_hist03z1_fy2027.xlsx` | OMB Historical Tables, FY2027 Budget | Table 3.1, outlays by function incl. national defense, $ and % GDP, 1940+ (complete file) | defense luck control | 2026-11-06 |
| `omb/OMB_hist07z1_fy2027.xlsx` | OMB Historical Tables, FY2027 Budget | Table 7.1, federal debt at end of year, incl. held by the public % GDP, 1940-2025 (complete file) | A15 (1940+) | 2026-11-06 |
| `wid/WID_data_US__sptinc992j_shweal992j_4groups.csv` | World Inequality Database (bulk download) | `sptinc992j` and `shweal992j`, p0p50 / p50p90 / p90p100 / p99p100, verbatim lines (see `wid/wid_provenance.json`) | B2, B4; A7 check | 2026-11-06 |
| `wid/WID_data_US.csv.gz`, `wid/WID_metadata_US.csv.gz`, `wid/WID_README.md` | World Inequality Database (bulk download) | complete US data and metadata members of `wid_all_data.zip` (gzip-compressed), and its README | source for the extract above | 2026-11-06 |
| `bls/BLS_pr.data.1.AllData__PRS85006092_093_annual.txt` | BLS Productivity and Costs (PR database) | download.bls.gov/pub/time.series/pr/pr.data.1.AllData: `PRS85006093` (nonfarm business output per hour, index 2017=100) and `PRS85006092` (% change), period Q05 = annual, verbatim lines (see `bls/bls_provenance.json`) | A24 (primary; FRED OPHNFB kept as check) | 2026-11-06 |
| `bea/BEA_SAINC1__ALL_AREAS_1929_2025__regions_line3.csv` | BEA Regional Accounts, SAINC1 | apps.bea.gov/regional/zip/SAINC.zip, member SAINC1__ALL_AREAS_1929_2025.csv: per capita personal income (LineCode 3, current dollars), US and 8 BEA regions, verbatim lines (see `bea/bea_provenance.json`) | B12 | 2026-11-06 |
| `fernald/FERNALD_quarterly_tfp__annual_colsA_L_M_N.csv` | John Fernald, FRBSF quarterly TFP (vintage 2026-10-01) | frbsf.org/wp-content/uploads/quarterly_tfp.xlsx, sheet annual: dtfp, dutil, dtfp_util, 1947-2025 (see `fernald/fernald_provenance.json`) | productivity luck control (check) | 2026-11-06 |
| `bdf_ltp/BDF_LTP_BCLDatabase_v2.7__TFP_USA.csv` | Banque de France Long-Term Productivity Database v2.7 (Bergeaud, Cette, Lecat), Feb 2026 | longtermproductivity.com/download/BCLDatabase_online_v2.7.xlsx, sheet TFP, column USA, 1890-2024 (see `bdf_ltp/bdf_ltp_provenance.json`) | productivity luck control (primary) | 2026-11-06 |
| `epi/EPI_hourly_wage_percentiles__national_real_wage_2025_p10_p50_p90.csv` | EPI State of Working America Data Library (CPS, EPI extracts; deflated with extended C-CPI-U) | data.epi.org API, indicator `hourly_wage_percentiles`, measure `real_wage_2025`, national, p10/p50/p90, 1973-2025 (see `epi/epi_provenance.json`) | B3 | 2026-11-06 |
| `maddison/MADDISON_mpd2023_web.xlsx` | Maddison Project Database 2023 (Bolt & van Zanden 2024), Dataverse doi:10.34894/INZBF2 | dataverse.nl/api/access/datafile/421302 (complete file; SHA-1 equals Dataverse's; see `maddison/maddison_provenance.json`) | world-growth luck control (sheet `Full data`) | 2026-11-06 |
| `wieland_yang/RR_monetary_shock_{annual,quarterly,monthly}.txt` | Wieland & Yang updated Romer-Romer shocks, GitHub `johanneswieland/RomerShocks` at commit b0092c4 (linked from johanneswieland.github.io; stable copy on openICPSR 135741) | complete files, plus Wieland's `RR_monetary_shock_update.do` and readme (`WY_readme.md`); see `wieland_yang/wieland_yang_provenance.json` | monetary-shock luck control, 1969-2007 | 2026-11-06 |
| `wonder/WONDER_*__by_year.xml` (10 files) | CDC WONDER (NCHS): Compressed Mortality 1968-78 (D74) and 1979-98 (D16), Underlying Cause of Death 1999-2020 (D76) and 2018-2024 (D158) | WONDER XML API, national, by year: homicide deaths, population, crude rate; ICD-8/9 E960-E969, ICD-10 *U01-*U02, X85-Y09, Y87.1 (plus X85-Y09, Y87.1 without terrorism codes for 1999-2024, and legal intervention E970-E978 / Y35, Y89.0 for 1968-2024); verbatim response extracts (see `wonder/wonder_provenance.json`, which also records the data use terms) | A19, 1968-2024 | 2026-11-06 |
| `nchs/NCHS_homicide_rate_1933-1967_transcribed.csv` | NCHS published rates: Linder & Grove (1943) *Vital Statistics Rates in the United States, 1900-1940*, Table 15; HIST290 tables 1940-49, 1950-59, 1960-67 (cdc.gov) | typed by hand, one decimal as printed; source PDFs' SHA-256 in `nchs/nchs_provenance.json` | A19, 1933-1967 | 2026-11-06 |

FRED annual and quarterly aggregates are FRED's own (`fam=avg`); FRED leaves incomplete periods blank (e.g. 2026).

`_transcripts/` keeps the exact text copied out of the browser and the two scripts that rebuilt the files from it
(`decode_fred.py`, `decode_owid.py`, `decode_bls.py`, and `decode_lines.py` for the BEA, Fernald, BdF and EPI extracts), so each rebuild can be re-run and re-checked.

**Large and binary files** (Voteview, OMB, WID, Maddison) were fetched the same way, then saved through the browser's own download (approved by the researcher
2026-11-06) and copied here; the copy's SHA-256 equals the hash the browser computed on the fetched bytes.

## Still to pull (all sites approved by the researcher on 2026-11-06)

| Item | Planned source | Status |
| --- | --- | --- |
| A19 homicide rate 1900-1932 | Eckberg (1995) adjusted estimates, or death-registration-States rates from Linder & Grove (1943) Table 15 | Not yet decided. 1933-2024 is pulled (rows above). |
| (All other planned sources are pulled.) | | |

## Decisions on data issues

Six places where the data and the frozen plan did not line up exactly were put to the researcher on
2026-11-06 and decided before any analysis. They are logged in `../../DEVIATIONS.md`: A15 debt definition,
carried-forward values treated as missing, quarterly unemployment from 1948Q1, Hispanic unemployment from 1974,
BLS annual productivity, and the Wieland & Yang (2020) Romer-Romer extension.

## Decided after part 4 (logged in `../../DEVIATIONS.md`, 2026-11-06)

- **A18:** CPS changes 1987-2008 (within consistent pieces), ACS changes 2009-2025; changes touching 2020 missing.
- **B10:** ratio computed from P-38 medians for all years; P-40 is the check (they differ only in 1969: 60.5 vs 58.9).

## Decided during part 9 (logged in `../../DEVIATIONS.md`, 2026-11-06)

- **World growth (Maddison):** chain-linked growth of aggregate GDP per capita over non-US countries present in both years.
- **B12 deflator:** the A3 CPI (Ecdat/MeasuringWorth) for all regions; 2024-25 from FRED CPIAUCSL annual average.

## Data notes (no results)

- A19 (homicide): WONDER's two 1999-2024 series differ only by terrorism deaths (*U01-*U02): 2,922 in 2001 (September 11); in other years the difference is 9 or fewer deaths, which CDC WONDER's terms forbid publishing. UCD 1999-2020 and UCD 2018-2024 agree exactly on deaths and population for 2018-2020. Pre-1968 NCHS rates are rounded to one decimal. NCHS's own published 'homicide' rates include legal intervention: HIST290 for 1968-78 (mx196878.pdf, cdc.gov) prints HOMICIDE E960-E978 at 7.4 (1968) and 9.2 (1978), which matches WONDER homicide plus legal intervention (7.36 and 9.20), while WONDER E960-E969 alone gives 7.18 and 9.08. So the 1933-67 published rates very likely include police-intervention deaths (about 0.1-0.2 per 100,000 in 1968-78), and the 1967/68 join needs one definition on both sides. Linder & Grove's homicide includes legal executions for 1921-29 only.

- BLS annual productivity index vs FRED OPHNFB (annual average of the quarterly index): largest gap 0.24 index points over 1947-2025 (e.g. 2025: 118.434 vs 118.601).
- BEA SAINC1 is in current dollars; B12 needs a deflator (the plan says "real" but names none). Far West excludes Alaska and Hawaii before 1950 (BEA footnote). In 1929 the Mideast had the highest per-capita income ($972) and the Southeast the lowest ($363); these fix B12's pre-named contrast.
- BdF LTP TFP ends in 2024; Fernald's annual TFP runs to 2025.
- EPI 2025 wage values look rounded (e.g. p90 = 65.375, p10 = 14.557999992370608, a single-precision 14.558); earlier years are not.

- WID (pulled direct, 5 Nov 2026 release) has distinct top-1% income shares for 2022, 2023 and 2024 (0.2081, 0.2048, 0.2051),
  so the 20.73 repeated in OWID's copy was carried forward, as suspected. A7 can use WID's own values for those years.
- WID's `data_quality` column is 0 for the latest wealth-share years (e.g. 2024); worth a look before use.

