# ISA/MOJ Code-Based Normalization Dry-Run and QC - Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Script: scripts/11_official_data/isa_moj_chinese_stock_panel_normalize.py
QC summary CSV: literature/02_matrices/isa_moj_code_based_normalization_dryrun_qc_summary.csv

## A. Purpose

This note documents a CODE-BASED dry-run and QC summary for the ISA/MOJ registered
Chinese foreign-resident STOCK panel normalization scaffold. It validates the safe
code-based 2021-12 to 2025-06 route via the scaffold's --dry-run, --schema-only, and
--dry-run --code-based-only modes, and records commit-safe QC only. No full normalized
panel was written.

## B. Evidence boundary

- This is dry-run / QC only.
- No full normalized panel was written (--write-local-panel NOT run; --force NOT used).
- No raw Excel was modified or committed.
- No full municipality value table was committed.
- No modeling was run.
- No manuscript text was written.
- No novelty was claimed.
- These values are MOJ/ISA REGISTERED Chinese foreign residents, NOT Census population.
  Any growth variable is registered Chinese foreign-resident STOCK change, NOT Census
  population growth.
- Gap status remains: under verification.

## C. Code-based scope

Eight semi-annual code-based periods (confirmed in dry-run routing):

- 2021-12
- 2022-06
- 2022-12
- 2023-06
- 2023-12
- 2024-06
- 2024-12
- 2025-06

Parser types:

- wide_03 for 2021-12 to 2023-06 (4 files): municipality code + total foreign + China;
  matched 250/251 each; 10 prefecture/ward aggregate rows filtered; 1 missing target code
  zero-filled.
- china_values for 2023-12 to 2025-06 (4 files): municipality code + Chinese value
  (already China-filtered); matched 245/246/245/247 of 251; 4-6 small-village codes
  zero-filled (flagged).
- all_values: validation only (2024-12, 1 file) - total foreign, not Chinese.
- t2_long: validation only (2023-12/2024-06/2025-06, 3 files) - cross-check against
  china_values; not the primary route.

Master frame: 251 target municipality codes (Tokyo/Saitama/Chiba/Kanagawa).

## D. Deferred scope

- The 2012-12 to 2021-06 wide "07" name-only files (18 periods) remain DEFERRED.
- They carry a China column but NO municipality-code column; geography is by
  prefecture/city/ward name in merged cells.
- They require a hierarchical name -> JIS code crosswalk.
- They are NOT included by default (refused unless --include-name-only-wide07 AND
  --name-crosswalk are supplied).
- Therefore 2015-2020 pre-service ISA registered-stock growth is NOT yet feasible.

## E. Growth implication

- Post-service registered Chinese foreign-resident STOCK change 2023-12 to 2025-06 is
  feasible AFTER an approved code-based normalization run.
- The stronger 2015-2020 -> service -> 2023-2025 chain remains PENDING name->JIS
  crosswalk validation.
- All growth variables must be labelled MOJ/ISA registered Chinese foreign-resident
  STOCK change, NOT Census population growth.
- Do NOT run modeling yet.

## F. Next step

Recommended next task: "ISA/MOJ code-based 2021-12-2025-06 normalization approval
package" before any local panel is written. Do not recommend direct modeling. No
Introduction; no novelty; gap remains under verification.
