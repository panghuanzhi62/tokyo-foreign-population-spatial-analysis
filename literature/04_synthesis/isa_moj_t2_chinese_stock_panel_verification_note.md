# ISA/MOJ t2 Chinese Registered-Resident Stock Panel - Local File Verification Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Companion CSVs:
- literature/02_matrices/isa_moj_t2_chinese_values_file_verification.csv
- literature/02_matrices/isa_moj_t2_chinese_stock_zero_fill_panel_design.csv
- literature/02_matrices/isa_moj_t2_chinese_stock_panel_qc_summary.csv

## A. Purpose

This note verifies four LOCAL MOJ/ISA t2 China-filtered value Excel files (prepared by
the user under data_raw/isa_estat/) for building a municipality-level registered
Chinese foreign-resident STOCK panel for Tokyo, Saitama, Chiba, and Kanagawa at four
time points (2023-12, 2024-06, 2024-12, 2025-06), against the confirmed 251-code
Census master frame.

## B. Evidence boundary

- This is file-structure verification and zero-fill design.
- It is NOT final analysis data; NOT modeling; NOT manuscript text.
- It does NOT prove novelty; it does NOT confirm the gap.
- No raw Excel, no full municipality value table, and no full 251x4 panel were
  committed. The committed CSVs contain only counts, schema facts, and small
  zero-fill code lists - not value tables.
- Gap status remains: under verification.

## C. Relationship to the previous cc5eb0a task

The previous task (commit cc5eb0a) verified the ISA/MOJ t2 Excel table-data route at
metadata level and concluded PARTIALLY USABLE because the Excel files had not been
opened. This task performs that next local file-level inspection using the
user-prepared China-filtered Excel files. The earlier "needs Excel opened" limitation
is now resolved by direct inspection.

## D. File-level findings

All four files have one sheet (Sheet1) with columns: municipality code
(shikuchoson_code, 5-char string), prefecture, municipality name, and a single value
field "sum of foreign-resident count" which - because each file is pre-filtered to
China - equals the registered Chinese resident count per municipality. (25-06 adds a
designated-city column; column order differs across files; mapping is by header name.)

| time | rows read | observed target codes | matched (of 251) | missing (zero-fill) | extra | duplicate | aggregate | numeric |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-12 | 1805 | 245 | 245 | 6 | 0 | 0 | 0 | yes |
| 2024-06 | 1756 | 246 | 246 | 5 | 0 | 0 | 0 | yes |
| 2024-12 | 1762 | 245 | 245 | 6 | 0 | 0 | 0 | yes |
| 2025-06 | 1764 | 247 | 247 | 4 | 0 | 0 | 0 | yes |

- China-filtering CONFIRMED: on the 2024-12 file, every China value is < the parallel
  all-foreigners value (e.g. Shinjuku 18,892 vs 49,182; Kawagoe 2,776 vs 11,496), with
  zero violations; the national China sum (~873k) is ~23% of the all-foreigner sum
  (~3.77M), consistent with Chinese being the largest foreign nationality.
- Every observed target-prefecture code is within the 251 Census frame (extra = 0); no
  aggregate rows (prefecture totals / designated-city parents / special-wards
  aggregate) appear in the target prefectures; no duplicate codes; all target values
  numeric.
- Missing target codes (per period) are the small island/mountain villages:
  2023-12: 13307,13362,13364,13381,13382,13402; 2024-06: 13307,13362,13364,13382,13402;
  2024-12: 11369,13307,13362,13364,13382,13402; 2025-06: 13307,13362,13382,13402.

## E. Zero-fill interpretation

A target code that is in the 251 Census frame but absent from a China-filtered ISA/MOJ
file is treated as ZERO registered Chinese residents (zero-fill), NOT as an error,
because: (1) the files are confirmed China-filtered; (2) the missing codes are tiny
island/mountain villages (e.g. Aogashima-mura, Mikurashima-mura, Hinohara-mura,
Higashichichibu-mura) that plausibly have 0 registered Chinese; and (3) these same
villages appeared as Census "-" (=0) cells in the earlier extraction. Any future local
panel must FLAG zero-filled rows (zero_filled=1) so they are not confused with observed
zeros.

## F. Model implication

All four time points pass. A provisional 2023-12 to 2025-06 registered Chinese stock
change is feasible at municipality level (251-code frame after zero-fill). This MUST be
described as MOJ/ISA REGISTERED Chinese foreign-resident STOCK change, NOT Census
population growth - they are different sources and measures. A log-change variable
requires a positive base period; zero-filled bases must be handled explicitly. The
Census 2020 table (00200521) remains the main municipality population source per the
prior decision; this ISA series is a recent registered-stock panel and cross-check.

## G. Next step

Recommended next task: "ISA/MOJ t2 zero-filled Chinese stock panel script scaffold".

The future script should read the four local China-value Excel files, normalize codes
to 5-char strings, restrict to the 251 target codes, zero-fill the small set of absent
village codes (flagged), and assemble the local-only 251 x 4 panel plus the growth
variables - storing the panel local-only and committing only small QC/derived
summaries unless explicitly approved. Do not run modeling yet. No Introduction; no
novelty; gap remains under verification.
