# ISA/MOJ t2 Derived-Growth Table Build (Dependent Variable) - Run Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Script: scripts/11_official_data/isa_moj_t2_derived_growth_table_build.py
Run date: 2026-06-24

## A. Purpose

This run built the LOCAL-ONLY ISA/MOJ t2 derived-growth table - the dependent variable - from
the validated four-period zero-filled registered Chinese foreign-resident STOCK panel. The
approved command was run exactly:

  python scripts/11_official_data/isa_moj_t2_derived_growth_table_build.py --project-root . --write-local-derived-table --force --write-qc-summary

## B. Evidence boundary

- The local-only derived-growth table was built.
- The full table is LOCAL-ONLY and is NOT committed (gitignored under data_processed_official).
- The full local panel and local QC remain uncommitted.
- No municipality-level derived values are committed.
- No modeling is run.
- This is not manuscript text.
- No novelty is claimed.
- The dependent variable measures MOJ/ISA REGISTERED Chinese foreign-resident STOCK change,
  NOT Census population growth and NOT causal settlement growth.
- Gap status remains: under verification.

## C. Output scope (local-only; NOT committed)

- Derived table: data_processed_official/isa_moj_panel/isa_moj_t2_derived_growth_2023_12_2025_06.csv
- Derived QC:    data_processed_official/isa_moj_panel/isa_moj_t2_derived_growth_qc.csv

Columns: municipality_code, prefecture_code, municipality_name, chinese_registered_2023_12,
chinese_registered_2025_06, chinese_registered_change_2023_12_to_2025_06,
chinese_registered_log1p_change_2023_12_to_2025_06, chinese_registered_zero_base_2023_12,
chinese_registered_pct_change_2023_12_to_2025_06,
chinese_registered_growth_positive_2023_12_to_2025_06, base_zero_filled, end_zero_filled.

## D. QC result (all gates passed)

- rows: 251 (exactly one per master-frame municipality).
- municipality_code: 5-character string; all in the 251 master frame; extra 0; duplicate 0;
  aggregate rows 0.
- base and end values numeric; negative base/end values: 0.
- absolute change defined for all 251; log1p change defined for all 251.
- zero-base flag count: 6.
- percent change is NA (blank) for exactly the 6 zero-base municipalities.
- variable formulas verified (change, log1p, zero_base, growth_positive).

## E. Recommended dependent variable

- Recommended dependent variable for modeling: chinese_registered_log1p_change_2023_12_to_2025_06
  (described as log1p registered-stock change, NOT percentage growth).
- Absolute change (chinese_registered_change_2023_12_to_2025_06) is the primary DESCRIPTIVE
  variable.
- The chinese_registered_zero_base_2023_12 flag MUST be retained (6 municipalities) for
  interpretation and for any percent-change robustness analysis.
- Raw log-difference is NOT used as a default (undefined at zero base/end).

## F. Scope boundary

- 2015-2020 pre-service ISA growth remains PENDING the wide07 name-to-JIS code crosswalk and
  is NOT feasible now.
- No modeling proceeds in this task.

## G. Next step

Recommended next task: CORE EXPLANATORY-VARIABLE construction - migrant-oriented service
infrastructure, rail accessibility, housing cost, and commercial density. Do not run modeling
yet. No Introduction; no novelty; gap remains under verification.
