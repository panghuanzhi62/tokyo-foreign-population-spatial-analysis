# Census 00200521 Bounded Municipality Extraction Script Scaffold - Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Script: scripts/11_official_data/census_00200521_municipality_population_extract.py
Summary CSV: literature/02_matrices/census_00200521_bounded_extraction_script_scaffold_summary.csv

## A. Purpose

This note documents a BOUNDED municipality population extraction script scaffold for
Census 00200521 table 0003445244. The scaffold reads the confirmed 251
municipality-equivalent area codes for Tokyo, Saitama, Chiba, and Kanagawa and
provides safe --dry-run and --metadata-only modes plus a guarded (not-run)
value-retrieval mode.

## B. Evidence boundary

- This is a scaffold task.
- No population values were retrieved.
- No bounded extraction was run.
- No full extraction was run; no all-Japan value retrieval.
- No preprocessing or modeling was run.
- This is NOT a literature gap claim; NOT manuscript text; does NOT prove novelty.
- ESTAT_APP_ID was read from the environment only (for --metadata-only); never
  printed, written, or committed; no API URL containing it was saved. No raw API
  output was saved into or committed to the repo.
- Gap status remains: under verification.

## C. Confirmed inputs

- statsDataId: 0003445244
- cdTime: 2020000000 (2020)
- cdCat01: 0 (sex total)
- cat02 foreign total: 1
- cat02 China: 102
- confirmed target area codes: 251 municipality-equivalent units
- prefecture counts: Tokyo 62, Saitama 72, Chiba 59, Kanagawa 58
- aggregate rows excluded: 10 (4 prefecture totals, 5 designated-city parents, 1 Tokyo
  special-wards aggregate)
- island municipalities flagged: 9 (Tokyo Izu/Ogasawara; included but flagged)
- expected join key: 5-digit JIS municipality code (direct to NLNI N03)
- ISA 00250012 role: prefecture-level cross-check only

## D. Script interface

Safe commands (no value retrieval):

```
python scripts/11_official_data/census_00200521_municipality_population_extract.py --project-root . --dry-run
python scripts/11_official_data/census_00200521_municipality_population_extract.py --project-root . --metadata-only
```

Flags: --project-root, --dry-run, --metadata-only, --run-bounded-extraction,
--stats-data-id (0003445244), --cd-time (2020000000), --cd-cat01 (0), --cat02-total
(1), --cat02-china (102), --area-code-csv (default the confirmation CSV),
--target-prefectures (13,11,12,14), --outdir
(data_raw_official/census_00200521_2020_municipality), --max-areas (300),
--timeout-seconds, --allow-write-raw, --force.

FUTURE-ONLY (requires explicit authorization; do NOT run yet):
--run-bounded-extraction --force [--allow-write-raw]. This mode refuses to run
without --force, refuses any prefecture set other than the confirmed 13,11,12,14,
refuses if the area count exceeds --max-areas, and refuses to write raw output unless
--allow-write-raw is given and the output path is a known local-only/gitignored path.

## E. Safety design

- All-Japan extraction is refused by default; only the confirmed 251 cdArea codes are
  eligible (target prefectures must equal 13,11,12,14).
- appId is read from ESTAT_APP_ID only; never printed/written/committed.
- Raw output is NOT saved by default; raw output is local-only if later explicitly
  authorized (--allow-write-raw) and only under a gitignored path.
- The public repo must not contain raw Census API output.
- Value extraction is deferred to a separate, explicitly authorized task.

Variable logic (in the script comments):
- chinese_residents = value for cat02=102 at cdCat01=0, cdTime=2020000000.
- total_foreign = value for cat02=1 at cdCat01=0, cdTime=2020000000.
- non_chinese_foreign = total_foreign - chinese_residents.
- Future QC must verify chinese_residents <= total_foreign and non_chinese_foreign >= 0.

## F. Result of this run (2026-06-23)

- script --help passed: YES (exit 0; works without ESTAT_APP_ID)
- script --dry-run passed: YES (loaded 251 target areas; Tokyo 62, Saitama 72,
  Chiba 59, Kanagawa 58; no API call; no appId required)
- metadata-only test run: YES
- API reached: YES (getMetaInfo STATUS 0)
  - cat01 code 0 present: yes; cat02 China 102 present: yes; cat02 foreign-total 1
    present: yes; time 2020000000 present: yes
  - confirmed target areas present in live area dimension: 251/251
- run-bounded-extraction: NOT run (guard refuses without --force; exit 11)
- raw output saved: NO
- population values retrieved: NO

## G. Next step

Recommended next task: "Census 00200521 controlled bounded value-extraction test
batch 1".

This should perform a small, explicitly authorized bounded value retrieval (e.g. a
handful of municipalities first) to validate the extraction path and the QC gates
(chinese <= total_foreign; non_chinese_foreign >= 0), still storing any raw output
locally only and committing only small derived summaries if approved. Full extraction
is NOT recommended yet. No Introduction; no novelty; gap remains under verification.
