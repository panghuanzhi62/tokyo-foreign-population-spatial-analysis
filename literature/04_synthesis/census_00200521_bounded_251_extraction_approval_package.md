# Census 00200521 Bounded 251-Municipality Extraction - Approval Package

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Script: scripts/11_official_data/census_00200521_municipality_population_extract.py
Checklist: literature/02_matrices/census_00200521_bounded_251_extraction_approval_checklist.csv
Command preview: literature/04_synthesis/census_00200521_bounded_251_extraction_command_preview.txt

## A. Purpose

This is an APPROVAL PACKAGE for a future bounded 251-municipality value extraction
from Census 00200521 table 0003445244. It defines the exact scope, parameters,
storage, provenance, QC gates, and abort conditions for that extraction.

- This task does NOT run the extraction.
- Explicit user approval is required before any 251-area value extraction.

## B. Evidence boundary

- This is NOT a literature gap claim; NOT manuscript text; does NOT prove novelty.
- No 251-area values were retrieved in this task.
- No full extraction was run; no all-Japan retrieval.
- No final analysis data was created.
- No preprocessing/modeling was run.
- getStatsData was NOT called in this task (only --help and --dry-run were run).
- ESTAT_APP_ID was checked for presence only; never printed, written, or committed.
- Gap status remains: under verification.

## C. Confirmed source parameters

- statistics code: 00200521
- provider tstat: 000001136464
- statsDataId: 0003445244
- census year: 2020
- cdTime: 2020000000
- cdCat01: 0 (sex total)
- cat02 total foreign: 1
- cat02 China: 102
- target area count: 251 municipality-equivalent units
- prefecture counts: Tokyo 62, Saitama 72, Chiba 59, Kanagawa 58
- aggregate rows excluded: 10 (4 prefecture totals, 5 designated-city parents, 1 Tokyo
  special-wards aggregate)
- island municipalities flagged: 9 (Tokyo Izu/Ogasawara; included but flagged)
- expected join key: 5-digit JIS municipality code -> NLNI N03 (direct)
- ISA 00250012 role: prefecture-level cross-check only

## D. Controlled test evidence (already completed)

- test areas: 13101, 11201, 12101, 14101 (4 areas)
- categories: 2 (cat02 = 1 and 102)
- rows expected and retrieved: 8 / 8
- API response status: 0
- QC Chinese <= total foreign: passed
- QC non-Chinese >= 0: passed
- raw output saved: NO
- appId exposed: NO

## E. Future extraction scope requiring approval

The future approved extraction would retrieve ONLY:

- the 251 confirmed municipality-equivalent cdArea codes;
- cat02 = 1 and cat02 = 102 only;
- cdCat01 = 0 only;
- cdTime = 2020000000 only;
- statsDataId = 0003445244 only.

It would NOT issue any all-Japan query, any all-category query, or any unrelated
variables.

Expected maximum rows: 251 areas x 2 categories = 502 rows.

## F. Future command (DO NOT RUN YET)

DO NOT RUN UNTIL USER EXPLICITLY APPROVES.

```
python scripts/11_official_data/census_00200521_municipality_population_extract.py --project-root . --run-bounded-extraction --force --allow-write-raw --stats-data-id 0003445244 --cd-time 2020000000 --cd-cat01 0 --cat02-total 1 --cat02-china 102 --target-prefectures 13,11,12,14 --area-code-csv literature/02_matrices/census_00200521_municipality_area_code_confirmation.csv --outdir data_raw_official/census_00200521_2020_municipality --max-areas 300 --timeout-seconds 120
```

The full preview (with line-wrapped form and preconditions) is in
literature/04_synthesis/census_00200521_bounded_251_extraction_command_preview.txt.
This command is NOT run in this task. Note: the script's --run-bounded-extraction path
is currently a guarded placeholder; enabling the actual getStatsData bounded call is
part of the separately approved run task.

## G. Local-only raw storage

- Raw output directory (local-only, gitignored): data_raw_official/census_00200521_2020_municipality/
- Raw API output must be gitignored or otherwise kept out of the public repo.
- Raw output file names should include the date, statsDataId, cdTime, and scope, e.g.
  2020_00200521_2020000000_4pref_municipality_china_total.json (local-only).
- The raw output hash (e.g. SHA-256) must be recorded in the provenance log.
- Raw output must NOT be committed.

## H. Derived output plan (not created in this task)

- Future local processed output (local-only):
  data_processed_official/population/census_00200521_2020_municipality_population.csv
- Potential safe commit later (only after QC and explicit approval):
  literature/02_matrices/census_00200521_2020_municipality_population_qc_summary.csv
- No raw value table should be committed unless explicitly approved and small enough.

## I. Provenance log requirements

Use or extend metadata/official_census_population_extraction_provenance_template.csv.
Future provenance fields:

run_id; source_id; statistics_code; statsDataId; cdTime; cdCat01; cat02_codes;
target_prefectures; area_code_source; api_method; raw_output_local_path;
raw_output_hash; processed_output_path; query_date; license_terms; script_path;
raw_output_committed; appId_exposed; notes.

Do NOT record the appId in any provenance field.

## J. QC gates before any commit

- actual rows retrieved = 502;
- area count = 251;
- category count = 2;
- every confirmed included area appears;
- no excluded aggregate rows appear;
- no duplicate area-category rows;
- all municipality codes preserved as strings (leading zeros where applicable);
- Chinese residents <= total foreign residents for every area;
- non_chinese_foreign >= 0 for every area;
- missing value count reported;
- island municipalities flagged;
- prefecture counts match the confirmed area-code list;
- join key to N03 check planned;
- provenance log completed;
- raw output not committed;
- appId not exposed.

## K. Abort conditions

The future extraction must ABORT if:

- ESTAT_APP_ID is missing or invalid;
- target area count differs from 251;
- any area code is not in the confirmed list;
- API response row count differs from 502;
- category count differs from 2;
- any Chinese > total foreign;
- any non_chinese_foreign < 0;
- the raw output path points to a tracked public-repo file unless explicitly authorized;
- the appId appears in any saved file or diff;
- an all-Japan query would be triggered;
- the query would include more than the two required categories.

## L. User approval checklist

The user is asked to confirm (see the companion checklist CSV; all items PENDING):

- [ ] I approve running bounded extraction for exactly 251 confirmed municipalities.
- [ ] I approve retrieving only cat02 = 1 and cat02 = 102.
- [ ] I approve local-only raw output storage (gitignored).
- [ ] I understand raw API output will NOT be committed.
- [ ] I approve committing only QC summaries / small derived summaries after validation.
- [ ] I do NOT approve full all-Japan extraction.

## M. Next step

Recommended next task (only after explicit user approval): "Run approved Census
00200521 bounded 251-municipality extraction".

Until the user explicitly approves, no 251-area value extraction is run. No
Introduction; no novelty; gap remains under verification.
