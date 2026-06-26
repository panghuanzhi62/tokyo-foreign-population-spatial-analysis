# ISA/MOJ t2 Zero-Filled Panel Build - Run Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Script: scripts/11_official_data/isa_moj_t2_chinese_stock_panel_build.py
Run date: 2026-06-24

## A. Purpose

This run built a LOCAL-ONLY four-period (251 x 4) MOJ/ISA REGISTERED Chinese foreign-resident
STOCK panel from the four verified t2 China-filtered value files, under explicit user
approval. The approved command was run exactly:

  python scripts/11_official_data/isa_moj_t2_chinese_stock_panel_build.py --project-root . --write-local-panel --force --write-qc-summary

## B. Evidence boundary

- The full panel is LOCAL-ONLY.
- The full panel is NOT committed (it is gitignored under data_processed_official).
- Raw Excel files are NOT committed and were NOT modified (opened read-only).
- No modeling is run.
- No manuscript text is written.
- No novelty is claimed.
- These values are MOJ/ISA REGISTERED Chinese foreign residents, NOT Census population.
- Gap status remains: under verification.

## C. Input scope

Four China-filtered t2 value files (one per semi-annual period):

- 2023-12  -> data_raw/isa_estat/23-12-t2_china_values.xlsx
- 2024-06  -> data_raw/isa_estat/24-06-t2_china_values.xlsx
- 2024-12  -> data_raw/isa_estat/24-12-t2_china_values.xlsx
- 2025-06  -> data_raw/isa_estat/25-06-t2_china_values.xlsx

## D. Output scope

Local-only outputs (NOT committed; gitignored under data_processed_official/isa_moj_panel):

- Panel: data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv
- QC:    data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_panel_qc.csv

Panel columns: survey_time, municipality_code, prefecture_code, municipality_name,
chinese_registered, zero_filled, source_file, source_type, master_frame_included.

## E. QC result

- survey_time values: 2023-12, 2024-06, 2024-12, 2025-06 (count = 4).
- rows per time point: 251 each.
- total rows: 1004 (= 251 x 4).
- municipality_code x survey_time: UNIQUE (0 duplicate pairs).
- municipality_code: preserved as 5-character string.
- each time point covers exactly the 251-code master frame.
- extra codes: 0; duplicate codes: 0; aggregate rows: 0.
- zero-fill counts: 2023-12 = 6; 2024-06 = 5; 2024-12 = 6; 2025-06 = 4.
- all zero-filled rows flagged zero_filled=1 (with chinese_registered = 0); observed rows
  flagged zero_filled=0; flag domain = {0,1}.
- all chinese_registered values numeric; negative values: 0.

All mandatory QC gates PASSED.

## F. Growth implication

- 2023-12 to 2025-06 registered Chinese STOCK change can be derived AFTER local QC review.
- This is NOT Census population growth; it is MOJ/ISA registered Chinese foreign-resident
  stock change.
- A log-change variable requires explicit handling of municipalities with a zero 2023-12
  base (a zero base makes a log ratio undefined; handle at the analysis stage, e.g. exclude
  or flag). 2023-12 has 6 zero-filled municipalities.
- Pre-service 2015-2020 ISA growth remains INFEASIBLE until the name->JIS crosswalk for the
  wide07 files is validated.
- Do NOT run modeling yet.

## G. Next step

Recommended next task: "Review local panel QC and approve compact derived-growth variable
design." Do not recommend direct modeling yet. No Introduction; no novelty; gap remains under
verification.
