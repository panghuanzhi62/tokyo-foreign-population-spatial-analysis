# ISA/MOJ Chinese Stock Panel Normalization Script Scaffold - Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Script: scripts/11_official_data/isa_moj_chinese_stock_panel_normalize.py
Summary CSV: literature/02_matrices/isa_moj_chinese_stock_panel_normalization_script_scaffold_summary.csv

## A. Purpose

This note documents a normalization script SCAFFOLD for the ISA/MOJ registered Chinese
foreign-resident STOCK panel, built on the completed 2012-2025 raw-file inventory and
schema audit. The scaffold routes the 32 local Excel files to parsers and provides safe
--dry-run / --schema-only modes plus a guarded (not-run) panel-writing mode.

## B. Evidence boundary

- This is a script scaffold.
- No final normalized panel is created or committed.
- No full municipality value table is committed.
- No raw Excel is modified or committed.
- No modeling is run; no manuscript text is written; no novelty is claimed.
- These values are MOJ/ISA REGISTERED residents, not Census population.
- Gap status remains: under verification.

## C. Parser scope

- wide_03 parser: code-based, 2021-12 .. 2023-06 (4 files). Reads municipality code +
  total foreign + China; filters 10 aggregate rows; restricts to the 251 frame;
  zero-fills the 1 missing target code. DEFAULT-enabled (code-based).
- china_values parser: code-based, 2023-12 .. 2025-06 (4 files). Reads code + Chinese
  value (already filtered); restricts to 251; zero-fills the 4-6 small-village codes
  (flagged). DEFAULT-enabled (code-based).
- all_values parser: 2024-12 (+future, 1 file). Total foreign only (not China);
  excludes aggregate code 99999; VALIDATION ONLY; not default-enabled.
- t2_long parser: 2023-12 .. 2025-06 (3 files). Filters nationality = China; handles
  residence-status total or aggregation; VALIDATION route against china_values; not
  default-enabled.
- wide_07 name-only parser: 2012-12 .. 2021-06 (18 files). China column but NO code;
  requires a hierarchical name -> JIS crosswalk; DEFERRED - refused unless
  --include-name-only-wide07 AND --name-crosswalk are supplied.

Dry-run routing confirmed: wide_03=4, china_values=4, all_values=1, t2_long=3,
wide_07=18, other=2 (pivots) of the 32 inventoried files.

## D. Recommended first normalization route

- First normalize the DIRECT CODE-BASED files only: 2021-12 .. 2025-06 (8 semi-annual
  periods) from wide_03 + china_values (with all_values/t2_long for validation).
- Produce a LOCAL-ONLY panel under data_processed_official/isa_moj_panel.
- Commit only a QC summary after approval; never commit the raw Excel or the full panel.
- Do NOT include the name-only 2012-12 .. 2021-06 wide "07" files until the name -> JIS
  crosswalk is built and validated.

## E. Model implication

- Post-service Chinese REGISTERED STOCK change 2023-12 to 2025-06 is directly feasible
  after code-based normalization.
- Pre-service 2015-06 to 2020-06 ISA registered stock change requires the name-only
  wide "07" crosswalk and is therefore NOT feasible now.
- Consequently, the strongest 2015-2020 -> service -> 2023-2025 mechanism remains
  PENDING crosswalk validation.
- All growth variables must be labelled MOJ/ISA registered Chinese foreign-resident
  STOCK change, NOT Census population growth.
- No modeling should proceed before panel normalization and QC.

## F. Safe commands

```
python scripts/11_official_data/isa_moj_chinese_stock_panel_normalize.py --project-root . --dry-run
python scripts/11_official_data/isa_moj_chinese_stock_panel_normalize.py --project-root . --schema-only
python scripts/11_official_data/isa_moj_chinese_stock_panel_normalize.py --project-root . --dry-run --code-based-only
```

FUTURE-ONLY (requires explicit approval; DO NOT run yet): the panel-writing mode
(--write-local-panel --force) writes ONLY to the local-only outdir
(data_processed_official/isa_moj_panel) and refuses without --force, refuses a
non-local outdir, and refuses name-only inclusion without --name-crosswalk. It was NOT
run in this scaffold task.

## G. Next step

Recommended next task: "Run code-based normalization dry-run and QC summary" (the
scaffold's dry-run and schema-only checks pass), then "ISA/MOJ code-based 2021-12-2025-06
normalization approval package" before any local panel is written. Do not run modeling.
No Introduction; no novelty; gap remains under verification.
