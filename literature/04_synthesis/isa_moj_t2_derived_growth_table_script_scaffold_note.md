# ISA/MOJ t2 Derived-Growth Table Build Script Scaffold - Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Script: scripts/11_official_data/isa_moj_t2_derived_growth_table_build.py
Summary CSV: literature/02_matrices/isa_moj_t2_derived_growth_table_script_scaffold_summary.csv

## A. Purpose

This note documents a script SCAFFOLD for a FUTURE LOCAL-ONLY derived-growth table built from
the existing local-only ISA/MOJ t2 zero-filled registered Chinese foreign-resident STOCK
panel. The scaffold provides safe read-only --dry-run and --schema-only modes and a guarded
(not-run) --write-local-derived-table mode.

## B. Evidence boundary

- This is a script scaffold only.
- No derived-growth table is created.
- No municipality-level derived values are committed.
- No full panel is committed.
- No local QC output is committed.
- No modeling is run.
- This is not manuscript text.
- No novelty is claimed.
- All variables measure MOJ/ISA REGISTERED Chinese foreign-resident STOCK change, NOT Census
  population growth and NOT causal settlement growth.
- Gap status remains: under verification.

## C. Input scope

- Input panel (local-only): data_processed_official/isa_moj_panel/isa_moj_chinese_stock_t2_2023_12_2025_06.csv
  (gitignored; read-only inspected; NOT committed).
- base time: 2023-12
- end time: 2025-06
- 251 municipalities expected (master frame).

## D. Candidate variables

- chinese_registered_change_2023_12_to_2025_06 = end - base (PRIMARY DESCRIPTIVE).
- chinese_registered_log1p_change_2023_12_to_2025_06 = log(end+1) - log(base+1)
  (PRIMARY MODEL CANDIDATE; describe as log1p registered-stock change, NOT percentage growth).
- chinese_registered_zero_base_2023_12 = 1 if base == 0 else 0 (MANDATORY FLAG).
- chinese_registered_pct_change_2023_12_to_2025_06 = (end-base)/base where base>0 (OPTIONAL
  ROBUSTNESS; with zero-base flag).
- chinese_registered_growth_positive_2023_12_to_2025_06 = 1 if end > base else 0 (optional binary).
- Raw log-difference (log(end) - log(base)) is NOT recommended as the default (undefined at
  zero base/end).

All five candidate variables are implemented in the scaffold's write path (compute_record),
but that path is guarded by --force and is NOT run in this scaffold task.

## E. Safety gates

Future table generation must verify:

- Exactly 251 rows.
- municipality_code is a 5-character string.
- No extra codes (all in the 251 master frame).
- No duplicate municipality_code rows.
- No aggregate rows.
- Base and end values numeric.
- Zero-base flag count expected to be 6.
- log1p change defined for all 251.
- No negative base/end values.
- Full derived table remains LOCAL-ONLY (under data_processed_official/isa_moj_panel).
- No modeling run.

The scaffold's --write-local-derived-table path enforces these (refuses without --force,
refuses a non-local outdir, aborts on missing columns / wrong row counts / mismatched code
sets / non-numeric / negative values; warns if zero-base count != 6).

## F. Safe commands

```
python scripts/11_official_data/isa_moj_t2_derived_growth_table_build.py --project-root . --dry-run
python scripts/11_official_data/isa_moj_t2_derived_growth_table_build.py --project-root . --schema-only
```

FUTURE-ONLY (requires explicit approval; DO NOT run yet): the table-writing mode
(--write-local-derived-table --force --write-qc-summary) writes ONLY to the local-only outdir
(data_processed_official/isa_moj_panel) and refuses without --force. It was NOT run in this
scaffold task.

## G. Next step

Recommended next task: "ISA/MOJ t2 derived-growth table build approval package" before any
local derived table is written. Do not recommend modeling yet. No Introduction; no novelty;
gap remains under verification.
