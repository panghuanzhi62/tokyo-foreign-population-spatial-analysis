# Census 00200521 Controlled Value-Extraction Test - Batch 1 Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Script: scripts/11_official_data/census_00200521_municipality_population_extract.py
Summary CSV: literature/02_matrices/census_00200521_controlled_value_test_batch1_summary.csv

## A. Purpose

This note documents a very small, controlled getStatsData value-path test for Census
00200521 table 0003445244. The test retrieves only the two needed categories for four
sample municipalities to validate the value-retrieval path and the QC gates before any
larger bounded extraction.

## B. Evidence boundary

- This is a controlled value-path test only.
- It is NOT full extraction.
- It is NOT the 251-area bounded extraction.
- It is NOT final analysis data.
- It is NOT preprocessing/modeling.
- This is NOT a literature gap claim; NOT manuscript text; does NOT prove novelty.
- ESTAT_APP_ID was read from the environment only; never printed, written, or
  committed; no API URL containing it was saved.
- No raw API response was saved into or committed to the repo; retrieved values were
  used in memory for QC only and were NOT written or committed.
- Gap status remains: under verification.

## C. Test parameters

- statsDataId: 0003445244
- cdTime: 2020000000 (2020)
- cdCat01: 0 (sex total)
- cat02 total foreign: 1
- cat02 China: 102
- test areas: 13101 (Chiyoda-ku), 11201 (Kawagoe-shi), 12101 (Chiba-shi Chuo-ku),
  14101 (Yokohama-shi Tsurumi-ku)
- expected maximum rows: 8 (4 areas x 2 categories)

## D. Result summary (sanitized)

- API reached: YES
- response status: 0
- actual rows retrieved: 8
- area count returned: 4
- category count returned: 2
- raw output saved: NO
- appId exposed: NO
- QC Chinese <= total foreign: YES
- QC non-Chinese foreign >= 0: YES
- missing areas: 0; missing categories: 0

Raw appId, the raw API response, and the full value table are intentionally NOT
reported. Only Boolean QC results and counts are recorded (here and in the summary CSV).

## E. Script change summary

The bounded-extraction script was extended with a safe controlled-test mode:

- Added flags: --run-controlled-value-test, --test-areas, --max-test-areas (default 10).
- The controlled test runs getStatsData ONCE for the supplied test areas and the two
  categories (cat02 = 1 and 102) only; it parses values in memory for QC and prints a
  sanitized summary; it saves no raw output.
- Every test area must exist in the confirmed area-code CSV with
  included_in_target_scope=yes; non-confirmed or arbitrary codes are refused (verified:
  code 99999 was refused).
- The controlled test refuses if the test-area count exceeds --max-test-areas, and
  refuses a near-full (>=200) area set, so it cannot become the 251-area run.
- All-Japan extraction remains blocked (the bounded mode still requires prefectures
  13,11,12,14 and --force; the controlled mode is restricted to confirmed in-scope codes).
- Full 251-area extraction remains deferred (requires a later, explicitly authorized task).
- Raw output remains local-only and is never written by --dry-run/--metadata-only/
  --run-controlled-value-test.

## F. Next step

The controlled test passed. Recommended next task: "Census 00200521 bounded
251-municipality extraction approval package".

That package should request EXPLICIT approval before running the 251-area extraction,
specify local-only raw storage (gitignored), define the post-extraction QC gates
(chinese <= total_foreign; non_chinese_foreign >= 0; all 251 areas present; no
duplicate area rows), and commit only small derived summaries after QC. Full
extraction must not be run without that approval. No Introduction; no novelty; gap
remains under verification.
