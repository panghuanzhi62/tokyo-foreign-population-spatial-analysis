# Census 00200521 Bounded 251-Municipality Population Extraction - Run Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
QC summary: literature/02_matrices/census_00200521_2020_municipality_population_qc_summary.csv
Provenance: metadata/official_census_population_extraction_provenance.csv

## A. Purpose

The user EXPLICITLY APPROVED the bounded 251-municipality extraction, and it was run.
This note documents that the approved extraction of Census 00200521 table 0003445244
was executed for exactly the 251 confirmed municipality-equivalent areas in Tokyo,
Saitama, Chiba, and Kanagawa, retrieving only the two required nationality categories.

## B. Evidence boundary

- This is official data extraction only.
- This is NOT manuscript text; NOT a literature gap claim; does NOT prove novelty.
- No modeling was run; no interpretation of the retrieved values is made here.
- No final analysis dataset was created beyond the local processed table.
- ESTAT_APP_ID was read from the environment only; never printed, written, or
  committed; it was verified absent from the raw and processed local outputs.
- Raw API output and the processed value table are LOCAL-ONLY and were NOT committed.
- Gap status remains: under verification.

## C. Extraction scope

- statistics code: 00200521; provider tstat: 000001136464; statsDataId: 0003445244
- census year: 2020; cdTime: 2020000000; cdCat01: 0 (sex total)
- categories: cat02 = 1 (total foreign) and cat02 = 102 (China) ONLY
- area scope: exactly the 251 confirmed municipality-equivalent cdArea codes
  (Tokyo 62, Saitama 72, Chiba 59, Kanagawa 58)
- excluded aggregate rows: 10 (4 prefecture totals, 5 designated-city parents, 1 Tokyo
  special-wards aggregate) - none appeared in the response
- API method: getStatsData, issued in bounded chunks (50 areas/request) restricted to
  the confirmed codes; no all-Japan query; no all-category query
- variable logic: chinese_residents = cat02 102; total_foreign = cat02 1;
  non_chinese_foreign = total_foreign - chinese_residents

## D. QC summary

- expected rows: 502 (251 areas x 2 categories)
- actual rows: 502
- area count returned: 251
- category count returned: 2
- per-prefecture: Tokyo 62, Saitama 72, Chiba 59, Kanagawa 58 (match the confirmed list)
- aggregate rows present: 0
- duplicate area-category rows: 0
- missing area count: 0
- missing category count: 0
- Chinese <= total foreign (every area): YES
- non-Chinese foreign >= 0 (every area): YES
- island municipalities flagged: 9 (Tokyo Izu/Ogasawara; retained, flagged)
- raw output committed: NO
- appId exposed: NO

Census notation note: 6 value cells across 5 small Tokyo island/mountain villages
(Aogashima-mura, Hinohara-mura, Toshima-mura, Miyake-mura, Mikurashima-mura) were
reported as Census "-" (hyphen), which in official Japanese statistics means zero (no
applicable figure). These were treated as 0; with that treatment every area has both
categories and all QC gates pass.

## E. Storage and commit boundary

- Raw API output (local-only, NOT committed):
  data_raw_official/census_00200521_2020_municipality/raw_getStatsData_0003445244_2020000000_2026-06-23.json
  (SHA-256 recorded in the provenance log)
- Processed municipality population table (local-only, NOT committed):
  data_processed_official/population/census_00200521_2020_municipality_population.csv
  (251 rows: municipality_code, prefecture_code, total_foreign, chinese_residents,
  non_chinese_foreign)
- Committed files for this run: the QC summary CSV (aggregate QC only, no per-area
  values), the provenance log (paths + hash, no values, no appId), this run note, and
  the three fixed Claude reports. No raw API output and no per-area value table were
  committed.

Execution note: the committed bounded-extraction script
(scripts/11_official_data/census_00200521_municipality_population_extract.py) currently
exposes the bounded mode as a guarded placeholder; per the approval-package plan and
the task's staging allowlist (which does not include script changes), the approved
extraction was executed by a LOCAL-ONLY runner (kept outside the repo, not committed)
using the IDENTICAL approved parameters, the same confirmed 251-code area list, and the
same guards/abort conditions. The committed script is unchanged.

## F. Next step

Recommended next task: "Census 00200521 population-to-NLNI N03 join validation design".

This should design (not run) the validation of joining the municipality population
table to NLNI N03 boundaries on the 5-digit JIS code (matched/unmatched on both sides,
ward-vs-city aggregation, island handling), still committing only small derived
summaries. Modeling is NOT recommended yet. No Introduction; no novelty; gap remains
under verification.
