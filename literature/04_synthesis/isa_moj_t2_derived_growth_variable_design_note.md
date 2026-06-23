# ISA/MOJ t2 Derived-Growth Variable Design - Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Design CSV: literature/02_matrices/isa_moj_t2_derived_growth_variable_design.csv
QC/design summary: literature/02_matrices/isa_moj_t2_derived_growth_qc_design_summary.csv

## A. Purpose

This note designs compact derived-growth variables from the LOCAL-ONLY MOJ/ISA t2
zero-filled registered Chinese foreign-resident stock panel, capturing 2023-12 to 2025-06
registered Chinese foreign-resident STOCK change. It is a design and QC-specification task;
no municipality-level derived values are created or committed.

## B. Evidence boundary

- This task does not commit the full panel.
- This task does not commit municipality-level derived values.
- This task does not create final analysis data.
- No modeling is run.
- No manuscript text is written.
- No novelty is claimed.
- These variables measure MOJ/ISA REGISTERED Chinese foreign-resident stock change, NOT
  Census population growth.
- Gap status remains: under verification.

## C. Input panel status

- Local-only panel: data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv
  (gitignored; read-only inspected; NOT committed).
- 4 time points: 2023-12, 2024-06, 2024-12, 2025-06.
- 251 rows per time point; total 1004 rows.
- municipality_code sets identical across all four time points.
- zero-fill counts: 2023-12 = 6; 2024-06 = 5; 2024-12 = 6; 2025-06 = 4.
- read-only design facts: base (2023-12) value==0 in 6 municipalities; end (2025-06)
  value==0 in 4; absolute change defined for all 251; pct change feasible for 245 (base>0);
  raw log-difference undefined for 6 (zero base/end); log1p change defined for all 251;
  negative values: 0.

## D. Recommended variables

- Primary descriptive variable:
  chinese_registered_change_2023_12_to_2025_06
  = chinese_registered_2025_06 - chinese_registered_2023_12  (defined for all 251).
- Primary model candidate:
  chinese_registered_log1p_change_2023_12_to_2025_06
  = log(end + 1) - log(base + 1)  (defined for all 251; describe as log1p registered-stock
  change, NOT percentage growth).
- Mandatory flag:
  chinese_registered_zero_base_2023_12
  = 1 if 2023-12 base == 0 else 0  (6 municipalities flagged).

Raw log-difference (log(end) - log(base)) is NOT recommended as the default because a zero
base or zero end makes it undefined. Percent change is robustness-only and requires the
zero-base flag (feasible for 245 of 251).

## E. Interpretation

These variables capture short-term MOJ/ISA registered Chinese foreign-resident STOCK change
between 2023-12 and 2025-06. They should NOT be interpreted as Census population growth or
as causal settlement growth. The "stock" is the registered foreign-resident count, not a
demographic population estimate.

## F. Model implication

These variables can support the POST-SERVICE growth side of the later mechanism model AFTER
a separate service-infrastructure dataset is constructed. They do NOT solve the 2015-2020
PRE-SERVICE growth side, which remains pending the wide07 name->JIS code crosswalk. No
modeling should proceed yet.

## G. Next step

Recommended next task: "Create local-only derived-growth table approval package." Do not
recommend modeling yet. No Introduction; no novelty; gap remains under verification.
