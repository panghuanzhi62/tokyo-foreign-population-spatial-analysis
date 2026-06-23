# Census 00200521 Small Metadata/Count Test Scaffold - Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Script: scripts/11_official_data/census_00200521_small_metadata_test.py
Summary CSV: literature/02_matrices/census_00200521_small_metadata_test_scaffold_summary.csv

## A. Purpose

This note documents a small, safe, reproducible scaffold that verifies - with the
smallest possible official e-Stat API touch - that the confirmed 2020 Population
Census table (statsDataId 0003445244) can support the population module:

    chinese_residents   = cat02 == 102 (China)
    total_foreign       = cat02 == 1   (foreign total)
    non_chinese_foreign = total_foreign - chinese_residents

It is a metadata/count test only. It does NOT perform a full extraction, does NOT
retrieve all municipalities or all categories, and does NOT save raw API output.

## B. Evidence boundary

- This is NOT a literature gap claim.
- This is NOT manuscript text and contains no Introduction.
- This does NOT prove novelty.
- No full statistical dataset was downloaded.
- No full extraction was run (no data values retrieved).
- No preprocessing or modeling was run.
- ESTAT_APP_ID was read from the environment only; it was never printed, written to
  a file, or committed, and no API URL containing it was saved.
- No raw API output was saved into or committed to the repo.
- Official sources support data feasibility only; they do not prove the academic
  gap. Gap status remains: under verification.

## C. Script interface

`python scripts/11_official_data/census_00200521_small_metadata_test.py [options]`

Flags:
- `--project-root` (default `.`): repo root for path anchoring; no data written by default.
- `--dry-run`: print planned parameters only; NO API call; NO appId required or printed.
- `--run-count-test`: run getMetaInfo + getStatsData(cntGetFlg=Y).
- `--stats-data-id` (default `0003445244`)
- `--cd-time` (default `2020000000`)
- `--cd-cat01` (default `0`, sex total)
- `--china-cat02` (default `102`)
- `--foreign-total-cat02` (default `1`)
- `--test-areas` (default `13101,11201,12101,14101`)
- `--timeout-seconds` (default `60`)

Safety behaviours:
- `--dry-run` makes no API call and needs no appId.
- `--run-count-test` uses `cntGetFlg=Y`, which returns ONLY a record count (no data
  values). A hard cap (20) on `--test-areas` refuses anything resembling a bulk pull.
- The appId is read from `ESTAT_APP_ID` (environment only) and is never printed,
  written, or included in any printed URL.

## D. Test run result (2026-06-23)

Command: `--run-count-test` with the default parameters (appId supplied from the
environment only).

- getMetaInfo STATUS = 0
  - China code 102 present in cat02: True
  - Foreign-total code 1 present in cat02: True
  - Time code 2020000000 present: True
  - Test areas present in area dimension: 4/4
- getStatsData (cntGetFlg=Y) STATUS = 0
  - matching cell COUNT (no values retrieved): 8 (= 4 areas x 2 categories; expected 8)
- COUNT TEST RESULT: PASS
- construction feasibility (China and total codes present, count > 0): YES

No data values were retrieved; no raw output was saved.

## E. Interpretation

The scaffold confirms that table 0003445244 returns the expected municipality x
nationality structure for the four target sample municipalities (Chiyoda-ku,
Kawagoe-shi, Chiba-shi Chuo-ku, Yokohama-shi Tsurumi-ku), with China (102) and
foreign-total (1) both present for 2020. The population construction
(non_chinese_foreign = total_foreign - chinese_residents) is therefore feasible at
municipality level from a single table, year, and spatial unit.

Census 00200521 (table 0003445244) is confirmed as the MAIN municipality-level
population source. ISA 00250012 remains a PREFECTURE-LEVEL CROSS-CHECK ONLY.

Reminder: the main comparison must be Chinese residents vs non-Chinese foreign
residents (not vs all foreign residents), at the same spatial unit and year.

## F. Next step

Recommended next task: "Census 00200521 municipality population extraction design"
(or, when extraction is explicitly authorised, a bounded extraction limited to the
four target prefectures only). Any future extraction must still: read ESTAT_APP_ID
from the environment only; never print/write/commit it; store raw outputs locally
only (outside the public repo); and commit only small, reproducible derived
summaries if explicitly approved.

## G. Safety statement

- No datasets downloaded.
- No full extraction run (count/metadata only; no data values retrieved).
- No all-municipality or all-category retrieval.
- No raw API outputs saved or committed.
- No appId/API key printed, written, or committed.
- No preprocessing or modeling run.
- No manuscript text; no novelty asserted; no final gap claimed.
- Gap status remains: under verification.
