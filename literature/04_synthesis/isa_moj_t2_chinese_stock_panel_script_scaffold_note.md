# ISA/MOJ t2 Chinese Stock Panel Build Script Scaffold - Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Script: scripts/11_official_data/isa_moj_t2_chinese_stock_panel_build.py
Summary CSV: literature/02_matrices/isa_moj_t2_chinese_stock_panel_script_scaffold_summary.csv

## A. Purpose

This note documents a script SCAFFOLD for building a LOCAL-ONLY four-period (251 x 4)
MOJ/ISA REGISTERED Chinese foreign-resident STOCK panel from the four verified
China-filtered t2 value Excel files. The scaffold provides safe read-only --dry-run and
--schema-only modes and a guarded (not-run) --write-local-panel mode.

## B. Evidence boundary

- This is a script scaffold.
- No full panel is written (--write-local-panel NOT run; --force NOT used).
- No raw Excel is modified or committed.
- No full municipality value table is committed.
- No modeling is run.
- This is not manuscript text.
- This does not prove novelty.
- These values are MOJ/ISA REGISTERED Chinese foreign residents, NOT Census population.
- Gap status remains: under verification.

## C. Input scope

Four China-filtered t2 value files (one per semi-annual time point):

- 2023-12  -> 23-12-t2_china_values.xlsx
- 2024-06  -> 24-06-t2_china_values.xlsx
- 2024-12  -> 24-12-t2_china_values.xlsx
- 2025-06  -> 25-06-t2_china_values.xlsx

Note: the four files do NOT share a fixed column order (the municipality-code column is
column 0 in 2024-06/2024-12/2025-06 but column 1 in 2023-12; the value column shifts by
one in 2025-06). The scaffold locates columns BY HEADER, not by position, and the files
are nationwide, so rows outside the four target prefectures (11/12/13/14) are filtered out.

## D. Zero-fill rule

- Use the 251 Census municipality-equivalent code frame
  (Tokyo 62 / Saitama 72 / Chiba 59 / Kanagawa 58).
- Observed China values are joined by municipality_code (preserved as 5-character string).
- Missing target-frame codes are set to 0 and flagged zero_filled=1.
- Extra codes (target-prefecture codes not in the frame) are rejected (observed: 0).
- Duplicate codes are rejected (observed: 0).
- Aggregate rows are rejected (observed: 0).

Schema-only confirms per time point: matched 245 / 246 / 245 / 247 of 251; extra 0;
duplicate 0; all values numeric; codes normalize to 5 characters. Zero-fill counts:
6 / 5 / 6 / 4 -> 251 per time point.

## E. Growth implication

- After approved panel writing, 2023-12 to 2025-06 registered Chinese STOCK change is
  feasible.
- This must NOT be called Census population growth; it is MOJ/ISA registered Chinese
  foreign-resident stock change.
- A log-change variable requires explicit handling of zero-filled base values (a zero
  2023-12 base makes a log ratio undefined; this must be handled, e.g. excluded or
  flagged, at the analysis stage).
- Pre-service 2015-2020 ISA growth is NOT feasible now (it depends on the deferred
  name-only wide07 files and a name->JIS crosswalk).
- No modeling should proceed until panel QC is completed.

## F. Safe commands

```
python scripts/11_official_data/isa_moj_t2_chinese_stock_panel_build.py --project-root . --dry-run
python scripts/11_official_data/isa_moj_t2_chinese_stock_panel_build.py --project-root . --schema-only
```

FUTURE-ONLY (requires explicit approval; DO NOT run yet): the panel-writing mode
(--write-local-panel --force --write-qc-summary) writes ONLY to the local-only outdir
(data_processed_official/isa_moj_panel), refuses without --force, refuses a non-local
outdir, and aborts on extra/duplicate/missing-input/frame-size anomalies. It was NOT run
in this scaffold task.

## G. Next step

Recommended next task: "ISA/MOJ t2 zero-filled panel build approval package" before any
local panel is written. Do not recommend modeling. No Introduction; no novelty; gap
remains under verification.
