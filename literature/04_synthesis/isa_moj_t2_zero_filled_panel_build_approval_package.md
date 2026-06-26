# ISA/MOJ t2 Zero-Filled Panel Build - Approval Package

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Script: scripts/11_official_data/isa_moj_t2_chinese_stock_panel_build.py
Scaffold note: literature/04_synthesis/isa_moj_t2_chinese_stock_panel_script_scaffold_note.md

## A. Purpose

This is an APPROVAL PACKAGE for a FUTURE LOCAL-ONLY build of the four-period (251 x 4)
ISA/MOJ registered Chinese foreign-resident STOCK panel from the verified t2 China-filtered
value files.

- This task does NOT build the panel.
- User approval is REQUIRED before any local panel is written.

## B. Evidence boundary

- This task does not build the panel.
- No normalized panel is created.
- No raw Excel is modified or committed.
- No full municipality value table is committed.
- No modeling is run.
- This is not manuscript text.
- This does not prove novelty.
- These values are MOJ/ISA REGISTERED Chinese foreign residents, NOT Census population.
  Any derived growth variable is registered Chinese foreign-resident STOCK change, NOT
  Census population growth.
- Gap status remains: under verification.

## C. Candidate panel scope

Four approved candidate semi-annual periods:

- 2023-12
- 2024-06
- 2024-12
- 2025-06

Four candidate input files:

- data_raw/isa_estat/23-12-t2_china_values.xlsx
- data_raw/isa_estat/24-06-t2_china_values.xlsx
- data_raw/isa_estat/24-12-t2_china_values.xlsx
- data_raw/isa_estat/25-06-t2_china_values.xlsx

## D. Spatial frame and zero-fill rule

- Master spatial frame = 251 Census municipality-equivalent codes.
  - Tokyo: 62
  - Saitama: 72
  - Chiba: 59
  - Kanagawa: 58
  - Total: 251
- Observed China values are joined by municipality_code (preserved as 5-character string).
- Missing target-frame codes are set to 0 and flagged zero_filled=1.
- Extra codes (target-prefecture codes not in the frame) are rejected (observed: 0).
- Duplicate codes are rejected (observed: 0).
- Aggregate rows are rejected (observed: 0).

Schema-only confirmed per period: matched 245 / 246 / 245 / 247 of 251; extra 0; duplicate 0;
all values numeric; codes normalize to 5 characters. Zero-fill counts: 6 / 5 / 6 / 4.

## E. Future local-only output

Future local-only panel output path (NOT committed):

  data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv

This full panel must NOT be committed.

## F. Future local-only QC output

Future local-only QC output path (NOT committed):

  data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_panel_qc.csv

This local QC output should be reviewed before deciding whether a compact, commit-safe QC
summary can be created.

## G. Future command preview

DO NOT RUN UNTIL USER EXPLICITLY APPROVES.

  python scripts/11_official_data/isa_moj_t2_chinese_stock_panel_build.py --project-root . --write-local-panel --force --write-qc-summary

This command is NOT run in this task.

## H. Mandatory future QC gates

The future build must verify:

- Four survey_time values produced.
- 251 rows per survey_time.
- Total rows = 1004.
- municipality_code x survey_time is unique.
- municipality_code remains a 5-character string.
- No extra codes.
- No duplicate codes.
- No aggregate rows.
- Zero-fill counts match 6, 5, 6, 4 (2023-12 / 2024-06 / 2024-12 / 2025-06).
- All zero-filled rows flagged zero_filled=1.
- All observed rows flagged zero_filled=0.
- Output remains LOCAL-ONLY under data_processed_official/isa_moj_panel.
- Raw Excel files are not modified.
- Raw Excel files are not committed.
- Full panel is not committed.
- No modeling is run.

## I. Growth implication

- After approved panel writing and QC, 2023-12 to 2025-06 registered Chinese STOCK change
  is feasible.
- A log-change variable needs explicit handling of municipalities with a zero 2023-12 base
  (a zero base makes a log ratio undefined; handle at the analysis stage, e.g. exclude or
  flag).
- This is NOT Census population growth; it is MOJ/ISA registered Chinese foreign-resident
  stock change.
- Pre-service 2015-2020 ISA growth remains INFEASIBLE until the name->JIS crosswalk for the
  wide07 files is validated.
- No modeling should proceed before panel QC is reviewed.

## J. User approval checklist

- [ ] I approve building only the four t2 China-filtered periods.
- [ ] I approve using the 251 Census municipality-equivalent frame.
- [ ] I approve zero-filling missing target codes and flagging them.
- [ ] I approve writing the panel only to data_processed_official/isa_moj_panel.
- [ ] I do NOT approve committing the full panel.
- [ ] I do NOT approve committing raw Excel.
- [ ] I do NOT approve running modeling.
- [ ] I understand this measures registered Chinese foreign-resident stock, NOT Census population.
- [ ] I understand 2015-2020 pre-service ISA growth remains pending the name->JIS crosswalk.

## K. Next step

Recommended next task: "Run approved ISA/MOJ t2 zero-filled panel build" - ONLY after
explicit user approval. Do not run modeling. No Introduction; no novelty; gap remains under
verification.
