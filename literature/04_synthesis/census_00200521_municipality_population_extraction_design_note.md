# Census 00200521 Municipality Population Extraction Design - Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Companion file: literature/02_matrices/census_00200521_municipality_population_extraction_design.csv
Optional template: metadata/official_census_population_extraction_provenance_template.csv

## A. Purpose

This note designs a safe, reproducible, BOUNDED municipality-level population
extraction workflow for Census 00200521 table 0003445244 (Tokyo, Saitama, Chiba,
Kanagawa). It specifies extraction parameters, local-only folder layout,
metadata/provenance plan, future script interface, and quality checks. It does NOT
run any extraction.

## B. Evidence boundary

- This is NOT a literature gap claim.
- This is NOT manuscript text and contains no Introduction.
- This does NOT prove novelty.
- No full statistical dataset was downloaded.
- No full extraction was run; no data values were retrieved.
- No preprocessing or modeling was run.
- This is a design stage only. ESTAT_APP_ID was checked for presence only (never
  printed, written, or committed).
- Official sources support data feasibility only; they do not prove the academic
  gap. Gap status remains: under verification.

## C. Confirmed source parameters

- statistics code: 00200521
- provider tstat: 000001136464 (2020 Basic Complete Tabulation)
- statsDataId: 0003445244 ("Foreigners: population by sex and nationality -
  national, prefecture, municipality")
- year / cdTime: 2020 / 2020000000
- sex total: cdCat01 = 0
- foreign total: cat02 = 1
- China: cat02 = 102
- main unit: municipality (5-digit JIS area codes)
- ISA 00250012 role: PREFECTURE-LEVEL CROSS-CHECK ONLY

## D. Extraction design summary table

| component | confirmed parameter | future extraction action | blocking issue | quality check |
| --- | --- | --- | --- | --- |
| Chinese residents | cat02=102, cdCat01=0, cdTime=2020000000 | getStatsData bounded to target municipalities | municipality area-code list not yet enumerated | chinese <= total_foreign |
| total foreign residents | cat02=1, cdCat01=0, cdTime=2020000000 | getStatsData bounded; use code 1 not code 0 | same | non-negative; municipality coverage |
| non-Chinese foreign residents | derived = total(1) - China(102) | computed, no API call | depends on both terms (same unit/year) | non_chinese_foreign >= 0 |
| target prefecture scope | Tokyo(13), Saitama(11), Chiba(12), Kanagawa(14) | restrict cdArea to these prefectures | area-code list pending | all four prefectures covered |
| municipality code list | 5-digit JIS, prefix per prefecture | enumerate from getMetaInfo area dim | NOT yet fixed -> confirm next | code length + leading zeros preserved |
| join to N03 | 5-digit JIS == N03 gyosei kuiki code | post-extraction spatial join | ward-vs-city aggregation; vintage merges | unmatched on both sides reported |
| raw local storage | data_raw_official/census_00200521_2020_municipality/ | save raw JSON locally only | must stay gitignored | never committed |
| processed output | data_processed_official/population/ | build clean municipality table | - | commit only small summaries if approved |
| provenance log | metadata templates | record every extracted file | - | license/provenance present per file |
| safety checks | bounded scope; appId env-only | refuse all-Japan by default | - | all QC gates pass before modeling |

## E. Proposed sequence

1. Confirm or generate the municipality area-code list for Tokyo, Saitama, Chiba,
   Kanagawa (from the official getMetaInfo area dimension of 0003445244).
2. Design the bounded extraction script (spec only; see section below).
3. Run dry-run and metadata-only checks.
4. Run the bounded extraction ONLY after explicit authorization.
5. Store raw API outputs locally only (never committed).
6. Build the processed municipality population table.
7. Run the QC checks (section in the design CSV, EXD_011).
8. Join to NLNI N03 boundaries.
9. Commit only small derived summaries if explicitly approved.

## F. Future script specification (not created in this task)

Recommended future script: scripts/11_official_data/census_00200521_municipality_population_extract.py

Planned flags: --project-root, --target-prefectures, --stats-data-id, --cd-time,
--cd-cat01, --cat02-total, --cat02-china, --dry-run, --metadata-only,
--run-bounded-extraction, --outdir, --timeout-seconds.

Requirements: read ESTAT_APP_ID from environment only; never print/write/commit the
appId; save raw outputs locally only if explicitly permitted; create small processed
summaries only after validation; expose safety caps; refuse all-Japan extraction
unless explicitly authorized.

## G. Public repo safety

- No raw Census API output is committed.
- No appId is printed or saved.
- Raw outputs are local-only (gitignored folders).
- Future committed files are limited to scripts, run notes, metadata/provenance
  templates, and small derived summaries only if explicitly approved as safe.

## H. Next step

Recommended next task: "Census 00200521 municipality area-code list confirmation".

This should confirm/derive the target municipality area codes for Tokyo, Saitama,
Chiba, and Kanagawa (from the official getMetaInfo area dimension of table
0003445244) before the actual bounded extraction script is written. It remains a
metadata-only step: no data values retrieved, no raw output committed, appId from
the environment only, no Introduction, no novelty; gap status remains under
verification.
