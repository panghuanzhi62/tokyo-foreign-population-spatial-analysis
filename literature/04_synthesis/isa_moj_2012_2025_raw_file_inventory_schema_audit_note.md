# ISA/MOJ 2012-2025 Raw-File Inventory and Schema Audit - Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Companion CSVs:
- literature/02_matrices/isa_moj_2012_2025_raw_file_inventory.csv (32 files)
- literature/02_matrices/isa_moj_2012_2025_schema_code_match_audit.csv
- literature/02_matrices/isa_moj_2012_2025_panel_normalization_design.csv
- literature/02_matrices/isa_moj_2012_2025_panel_inventory_qc_summary.csv

## A. Purpose

This note inventories the local ISA/MOJ Statistics on Foreign Residents Excel files in
data_raw/isa_estat and audits whether they can support a municipality-level REGISTERED
Chinese foreign-resident panel from ~2012/2013 to 2025, against the confirmed 251-code
Census master spatial frame.

## B. Evidence boundary

- This is inventory and schema audit only.
- It is NOT final analysis data; NOT modeling; NOT manuscript text.
- It does NOT prove novelty; it does NOT confirm the gap.
- No raw Excel was modified or committed; no full municipality value table and no full
  normalized panel were committed. The committed CSVs hold schema facts, counts, and
  design - not value tables.
- Gap status remains: under verification.

## C. Relationship to prior ISA findings

- The earlier DB/API route remains prefecture-only for recent years (and the only
  municipality x nationality DB table, 0003147283, ends 2017-06).
- The file-based Excel route provides municipality-level historical and recent tables.
- This task audits the local raw Excel structure and 251-code compatibility directly.

## D. File-type summary (32 files)

| source_format | count |
| --- | --- |
| wide_municipality_nationality_table | 22 |
| long_t2_municipality_nationality_status_table | 3 |
| china_values_extracted_table | 4 |
| all_values_extracted_table | 1 |
| pivot_all_table | 1 |
| pivot_china_table | 1 |

Two distinct wide-table generations were found:
- "07" wide tables (2012-12 .. 2021-06, 18 files): "Dai-7-hyo shikuchoson-betsu
  kokuseki-chiiki-betsu". Header at row 4; columns sosu (total), Chugoku (China) and
  other nationalities. GEOGRAPHY IS BY NAME ONLY (prefecture / city / ward, merged
  cells) - there is NO municipality-code column.
- "03" wide tables (2021-12 .. 2023-06, 4 files): header at row 2; these DO have a
  shikuchoson-code (municipality code) column plus sosu (total) and Chugoku (China).

## E. Time coverage (semi-annual, June/December)

- 2012-12 to 2021-06 (18 periods): wide "07", China present, NO code -> PARTIALLY USABLE
  (requires a hierarchical name -> JIS-code crosswalk).
- 2021-12 to 2023-06 (4 periods): wide "03", code + China + total -> USABLE.
- 2023-12 to 2025-06 (4 periods): china_values extracts (code-based) -> USABLE; raw t2
  long files and pivots also present as source/intermediate.
- earliest survey time: 2012-12; latest survey time: 2025-06.

## F. Code-frame compatibility (code-bearing files; vs 251 master frame)

- china_values (2023-12/2024-06/2024-12/2025-06): matched 245/246/245/247 of 251;
  missing 6/5/6/4 (small island/mountain villages -> zero-fill); 0 extra, 0 duplicate,
  0 aggregate.
- wide "03" (2021-12/2022-06/2022-12/2023-06): matched 250 of 251; missing 1 (verify -
  likely a 0-foreigner village); 0 extra, 0 duplicate, but 10 AGGREGATE rows present
  (prefecture totals + designated-city parents + Tokyo special-wards aggregate) that the
  parser must filter.
- 24-12 all_values: matched 250 of 251 (TOTAL foreign, not China).
- minimum matched codes: 245; maximum missing target codes: 6; extra codes present: NO;
  duplicate codes present: NO.
- The 18 wide "07" name-only files cannot be code-matched until a name->code crosswalk is
  applied; their China column is present and the geography (prefecture/city/ward) is
  reconstructable from the merged-cell hierarchy.

Usability for Chinese stock: 8 files directly code-usable (4 china_values + 4 wide "03");
22 partially usable (18 name-only wide + 3 t2 raw + 1 china pivot); 2 not usable
(all_values + all_pivot, which are all-foreigner, not China).

## G. Model implication

- Normalization is feasible. A CODE-BASED registered Chinese stock panel is directly
  feasible for 2021-12 .. 2025-06 (8 semi-annual periods) from the wide "03" + china_values
  files. Extending back to 2012-12 (18 earlier periods) is PARTIAL and requires the
  name->code crosswalk.
- Growth variables:
  - Preferred PRE-service trend: a multi-year pre-2020 series (e.g. 2015-06 to 2020-06) -
    feasible only after the name->code mapping of the "07" files.
  - Preferred POST-service growth: 2023-12 to 2025-06 - directly feasible (clean,
    code-based).
- All growth variables MUST be described as MOJ/ISA REGISTERED Chinese foreign-resident
  STOCK change, NOT Census population growth. The Census 2020 table (00200521) remains
  the main municipality population source; this ISA series is a registered-stock panel
  and cross-check.
- No modeling before normalization and QC.

## H. Next step

Recommended next task: "ISA/MOJ 2012-2025 Chinese stock normalization script scaffold".

The future scaffold should implement: (1) the wide "03" parser (code + China + total,
filter the 10 aggregates, restrict to 251, zero-fill); (2) the china_values parser
(already verified, zero-fill the small village set); (3) optionally the t2 long parser
(filter China, aggregate statuses) as a validation route; and (4) the name->code
crosswalk for the "07" files as a separate, clearly-flagged extension. The full
normalized panel stays LOCAL-ONLY until approval; commit only QC/derived summaries.
Do not run modeling yet. No Introduction; no novelty; gap remains under verification.
