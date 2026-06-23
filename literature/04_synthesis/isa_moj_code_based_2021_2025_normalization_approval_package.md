# ISA/MOJ Code-Based 2021-12 to 2025-06 Normalization - Approval Package

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Script: scripts/11_official_data/isa_moj_chinese_stock_panel_normalize.py
Dry-run/QC inputs: literature/02_matrices/isa_moj_code_based_normalization_dryrun_qc_summary.csv ;
literature/04_synthesis/isa_moj_code_based_normalization_dryrun_qc_note.md

## A. Purpose

This is an APPROVAL PACKAGE for a FUTURE code-based ISA/MOJ 2021-12 to 2025-06 registered
Chinese foreign-resident STOCK panel normalization run.

- This task does NOT run normalization.
- User approval is REQUIRED before writing any local panel.

## B. Evidence boundary

- This is not final analysis data.
- No normalized panel is created.
- No raw Excel is modified or committed.
- No full municipality value table is committed.
- No modeling is run.
- This is not manuscript text.
- This does not prove novelty.
- These values are MOJ/ISA REGISTERED Chinese foreign residents, NOT Census population.
  Any growth variable is registered Chinese foreign-resident STOCK change, NOT Census
  population growth.
- Gap status remains: under verification.

## C. Approved candidate scope, pending user confirmation

Eight code-based semi-annual time points:

- 2021-12
- 2022-06
- 2022-12
- 2023-06
- 2023-12
- 2024-06
- 2024-12
- 2025-06

Parser routes:

- wide_03 for 2021-12 to 2023-06 (4 files): municipality code + total foreign + China.
- china_values for 2023-12 to 2025-06 (4 files): municipality code + Chinese value.
- all_values: VALIDATION ONLY (2024-12, 1 file): total foreign, not Chinese.
- t2_long: VALIDATION ONLY (2023-12/2024-06/2025-06, 3 files): cross-check vs china_values.

## D. Spatial frame

- Master spatial frame: 251 Census municipality-equivalent codes.
  - Tokyo: 62
  - Saitama: 72
  - Chiba: 59
  - Kanagawa: 58
  - Total: 251
- Aggregate rows (prefecture/ward totals) must be filtered out.
- Missing target codes must be zero-filled and flagged (zero_filled=YES).

## E. Future local-only output

Future local-only output path (NOT committed):

  data_processed_official/isa_moj_panel/isa_moj_chinese_stock_code_based_2021_12_2025_06.csv

This file must NOT be committed unless explicitly approved later.

## F. Commit-safe outputs after future run

A future approved run may commit ONLY:

- QC summary CSV
- run note
- provenance record
- fixed reports (outputs/claude_reports/latest_*.txt)

No full municipality value table or full normalized panel should be committed.

## G. Future command - DO NOT RUN YET

DO NOT RUN UNTIL USER EXPLICITLY APPROVES.

Suggested future command (matches the scaffold's --help flags):

  python scripts/11_official_data/isa_moj_chinese_stock_panel_normalize.py --project-root . --code-based-only --write-local-panel --force --write-qc-summary

Notes:
- --write-local-panel refuses without --force.
- --code-based-only restricts to wide_03 + china_values (all_values/t2_long for validation).
- Output goes ONLY to the local-only outdir (data_processed_official/isa_moj_panel).
- Do NOT add --include-name-only-wide07 / --name-crosswalk (wide07 deferred).
- This command is NOT run in this task.

## H. Mandatory QC gates for future run

The future normalization must verify:

- 8 code-based time points produced.
- Target area count = 251 for each time point after zero-fill.
- No aggregate rows included.
- No duplicate municipality_code x survey_time rows.
- municipality_code preserved as 5-character string.
- Missing target codes zero-filled and flagged.
- Zero-filled count matches known expected ranges (wide_03: 1 missing each; china_values:
  6/5/6/4 for 2023-12/2024-06/2024-12/2025-06).
- Raw Excel not modified.
- Raw Excel not committed.
- Normalized panel local-only.
- appId/API key not relevant and not exposed.
- Post-service growth variables can be derived from 2023-12 and 2025-06 after local panel QC.
- No modeling run.

## I. Abort conditions

The future normalization must ABORT or report FAILURE if:

- Raw folder missing.
- Master code frame missing or not 251 codes.
- Any parser fails.
- Any time point missing.
- Any unexpected extra code appears.
- Aggregate rows remain after filtering.
- Duplicate municipality_code x survey_time rows appear.
- Normalized panel path points to a tracked public-repo output.
- Raw Excel or full panel is staged.
- Crosswalk-required wide07 files are included without --name-crosswalk.

## J. User approval checklist

- [ ] I approve normalizing only the 8 code-based periods.
- [ ] I approve using the 251 Census municipality-equivalent frame.
- [ ] I approve zero-filling missing target codes and flagging them.
- [ ] I approve writing a local-only normalized panel under data_processed_official/isa_moj_panel.
- [ ] I do NOT approve committing the full normalized panel.
- [ ] I do NOT approve including 2012-12..2021-06 wide07 files yet.
- [ ] I understand pre-service 2015-2020 ISA growth is still not feasible until the
      name->JIS crosswalk is validated.
- [ ] I approve committing only QC/provenance/run-note summaries after validation.

## K. Next step

Recommended next task: "Run approved ISA/MOJ code-based 2021-12 to 2025-06 normalization" -
ONLY after explicit user approval. Do not run modeling. No Introduction; no novelty; gap
remains under verification.
