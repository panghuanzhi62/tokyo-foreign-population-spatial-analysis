# Census 00200521 Population-to-NLNI N03 Join Validation Design - Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Companion CSV: literature/02_matrices/census_00200521_population_to_nlni_n03_join_validation_design.csv
Checklist CSV: literature/02_matrices/census_00200521_population_n03_join_validation_checklist.csv

## A. Purpose

This note designs the validation workflow for joining the local-only Census 2020
municipality population table (251 municipality-equivalent rows) to official NLNI N03
municipality boundaries, on the 5-digit JIS municipality code. It defines the checks,
key logic, special cases, future outputs, and abort conditions. It does NOT run the
join.

## B. Evidence boundary

- This is a design task only.
- The join was NOT run.
- No GIS output was created.
- No boundary data were downloaded; an existing local N03 file was inspected only at
  the metadata level (CRS/encoding); no geometry was processed.
- No local processed population value table was committed.
- No raw Census API output was committed.
- No modeling was run.
- This is NOT manuscript text; NOT a literature gap claim; does NOT prove novelty.
- Gap status remains: under verification.

## C. Inputs

Committed:
- QC summary: literature/02_matrices/census_00200521_2020_municipality_population_qc_summary.csv
- provenance log: metadata/official_census_population_extraction_provenance.csv
- area-code confirmation: literature/02_matrices/census_00200521_municipality_area_code_confirmation.csv
- extraction run note: literature/04_synthesis/census_00200521_2020_municipality_population_extraction_run_note.md

Local-only (NOT committed):
- processed Census population table:
  data_processed_official/population/census_00200521_2020_municipality_population.csv
  (inspected this task: 251 rows; fields municipality_code, prefecture_code,
  total_foreign, chinese_residents, non_chinese_foreign; municipality_code str len 5)
- raw Census API output:
  data_raw_official/census_00200521_2020_municipality/raw_getStatsData_0003445244_2020000000_2026-06-23.json

Boundary (local-only, present in repo's gitignored data_raw/):
- NLNI N03: data_raw/N03-20250101_GML/ (N03-20250101.shp/.geojson/.dbf/.prj/.cpg)
  - vintage: 2025-01-01 (Reiwa 7) - to reconcile against Census 2020
  - CRS: JGD2011 geographic, EPSG:6668 (confirmed from .prj)
  - attribute encoding: UTF-8 (confirmed from .cpg)
  - expected code field: N03_007 (gyosei kuiki code; confirm in schema-only step)

## D. Join key logic

- Census municipality_code is a 5-digit JIS-compatible code; N03 code (N03_007) is the
  same 5-digit administrative-area code.
- Both sides must be read/handled as STRING; leading zeros preserved (the four target
  prefectures use 11xxx-14xxx so no leading zero is dropped, but string typing is still
  required for any later national extension).
- Tokyo 23 special wards must align as ward-level features (codes 13101-13123); the
  Tokyo special-wards aggregate (13100) must NOT be a join target.
- Designated-city wards (Saitama, Chiba, Yokohama, Kawasaki, Sagamihara) must align at
  ward level; designated-city parent aggregates must NOT be join targets. If N03
  represents some designated cities only at city level, the unit is incompatible and
  this becomes a blocking issue (resolve aggregation policy).
- Island municipalities (9, Tokyo Izu/Ogasawara) are retained and flagged at this
  stage; they must not be silently dropped during validation.
- Boundary-year reconciliation: the local N03 is 2025-01-01 while the Census is 2020;
  municipality code/merger stability for the four prefectures over 2020->2025 must be
  confirmed, or a 2020/2021-era N03 vintage obtained, before the join is relied upon.

## E. Validation checklist

| validation item | population-side check | boundary-side check | expected result | blocking issue | future output |
| --- | --- | --- | --- | --- | --- |
| row/feature counts | 251 rows | N03 features for 4 prefectures | 251 ward-level units matched | counts off | join summary |
| code format | str, len 5, no dup | N03_007 str, len 5 | clean 5-digit string keys | length/dup error | join summary |
| unmatched population codes | list pop codes with no N03 | - | 0 (or explained) | unmatched > 0 unexplained | unmatched list (summary) |
| unmatched boundary codes | - | list N03 target codes with no pop | 0 (or explained) | unmatched > 0 unexplained | unmatched list (summary) |
| ward/city handling | 251 ward-level units | wards present, no aggregates | ward-level alignment | city-level-only designated cities | join summary |
| island handling | 9 flagged retained | island features present | islands joined, flagged | islands dropped | flagged list (summary) |
| geometry validity | n/a | N03 geometry valid | valid geometries | invalid geometry | validity report (summary) |
| CRS | n/a | EPSG:6668 recorded | CRS consistent | CRS missing/mismatch | provenance |
| provenance | inputs recorded | N03 vintage/code field recorded | provenance complete | provenance missing | provenance entry |

## F. Future script recommendation

Recommended future task: "Census 00200521 population-to-NLNI N03 join validation script
scaffold".

The future script should expose: --project-root, --population-csv, --area-code-csv,
--n03-boundary, --target-prefectures, --dry-run, --schema-only, --run-join-validation,
--outdir, --write-gis-output, --force. It should default to --dry-run / --schema-only
and refuse to write GIS outputs unless explicitly authorized (--write-gis-output
--force), keeping any GIS output local-only and committing only small derived summaries.

## G. Next step

Recommended next task (conservative, given the boundary-year mismatch):
"Confirm NLNI N03 boundary source/year and schema for Tokyo, Saitama, Chiba, Kanagawa".

Although a local N03 file is already present (N03-20250101), its vintage (2025-01-01)
differs from the Census reference year (2020). The conservative step is to confirm the
N03 source/year and schema (code field N03_007, CRS EPSG:6668, encoding UTF-8 already
recorded) and reconcile municipality code stability 2020->2025 - or obtain a 2020/2021
N03 vintage - before creating the join validation script scaffold. No join, no GIS
output, no modeling. No Introduction; no novelty; gap remains under verification.
