# ISA/MOJ t2 Local-Only Derived-Growth Table - Approval Package

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Design CSV: literature/02_matrices/isa_moj_t2_derived_growth_variable_design.csv
Design note: literature/04_synthesis/isa_moj_t2_derived_growth_variable_design_note.md

## A. Purpose

This is an APPROVAL PACKAGE for a FUTURE LOCAL-ONLY derived-growth table built from the
four-period ISA/MOJ t2 zero-filled registered Chinese foreign-resident STOCK panel. It
captures 2023-12 to 2025-06 registered Chinese foreign-resident STOCK change.

- This task does NOT build the derived-growth table.
- User approval is REQUIRED before any local derived-growth table is written.

## B. Evidence boundary

- This task does not create municipality-level derived-growth values.
- This task does not create final analysis data.
- This task does not commit the full local panel.
- This task does not commit local-only QC.
- No modeling is run.
- This is not manuscript text.
- This does not prove novelty.
- All variables measure MOJ/ISA REGISTERED Chinese foreign-resident STOCK change, NOT Census
  population growth and NOT causal settlement growth.
- Gap status remains: under verification.

## C. Candidate input scope

- Local-only panel: data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv
  (gitignored; NOT committed).
- base time: 2023-12
- end time: 2025-06
- 251 municipalities (master frame).
- 1004 panel rows (251 x 4 time points).
- zero-base municipality count: 6 (2023-12 value == 0).

## D. Approved candidate variables, pending user confirmation

1. chinese_registered_change_2023_12_to_2025_06
   - formula: chinese_registered_2025_06 - chinese_registered_2023_12
   - recommended as PRIMARY DESCRIPTIVE variable (defined for all 251).

2. chinese_registered_log1p_change_2023_12_to_2025_06
   - formula: log(chinese_registered_2025_06 + 1) - log(chinese_registered_2023_12 + 1)
   - recommended as PRIMARY MODEL CANDIDATE (defined for all 251); describe as log1p
     registered-stock change, NOT percentage growth.

3. chinese_registered_zero_base_2023_12
   - formula: 1 if chinese_registered_2023_12 == 0 else 0
   - MANDATORY interpretation flag (6 municipalities flagged).

Optional robustness variables:

4. chinese_registered_pct_change_2023_12_to_2025_06
   - only where 2023-12 base > 0 (feasible for 245 of 251);
   - MUST use the zero-base flag.

5. chinese_registered_growth_positive_2023_12_to_2025_06
   - optional binary descriptive flag.

Raw log-difference (log(end) - log(base)) is NOT recommended as the default because a zero
base or zero end makes it undefined.

## E. Future local-only output

Future local-only derived-growth table path (NOT committed):

  data_processed_official/isa_moj_panel/isa_moj_t2_derived_growth_2023_12_2025_06.csv

This file must NOT be committed unless explicitly approved later.

## F. Future local-only QC output

Future local-only QC path (NOT committed):

  data_processed_official/isa_moj_panel/isa_moj_t2_derived_growth_qc.csv

This QC output should be reviewed locally before creating any compact commit-safe summary.

## G. Future script/command status

- No derived-growth table script exists yet (a search of scripts/ returned none).
- A script SCAFFOLD should be created before any derived-growth table is generated.
- Do NOT run any table-generation command in this approval-package task.
- If a safe script is later created locally, document its path but do not run it without
  explicit approval.

## H. Mandatory future QC gates

The future derived-growth table generation must verify:

- Exactly 251 municipality rows.
- municipality_code is a 5-character string.
- All municipality codes are in the 251 master frame.
- No extra codes.
- No duplicate municipality_code rows.
- No aggregate rows.
- Base and end values are numeric.
- Absolute change is defined for all 251.
- log1p change is defined for all 251.
- Raw logdiff is NOT used as default.
- Zero-base flag count = 6.
- No negative base/end values.
- No municipality-level values are committed unless later explicitly approved.
- Full local panel remains uncommitted.
- No modeling is run.

## I. User approval checklist

- [ ] I approve deriving only 2023-12 to 2025-06 registered Chinese stock change.
- [ ] I approve using the local-only t2 zero-filled panel as input.
- [ ] I approve creating a local-only derived-growth table.
- [ ] I approve absolute change as the primary descriptive variable.
- [ ] I approve log1p change as the primary model candidate.
- [ ] I approve zero-base flag as mandatory.
- [ ] I do NOT approve raw logdiff as the default variable.
- [ ] I do NOT approve committing municipality-level derived values.
- [ ] I do NOT approve committing the full local panel.
- [ ] I do NOT approve running modeling.
- [ ] I understand this is registered foreign-resident stock change, NOT Census population growth.
- [ ] I understand 2015-2020 pre-service ISA growth remains pending the name->JIS crosswalk.

## J. Next step

Recommended next task: "Create ISA/MOJ t2 derived-growth table script scaffold" (no script
exists yet), then a build approval, then "Run approved local-only derived-growth table build"
- ONLY after explicit user approval. Do not run modeling yet. No Introduction; no novelty;
gap remains under verification.
