# ISA/e-Stat 24-12-t2 Local Excel Validation - DDL_001 and DDL_002

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan
Tokyo (provisional working title).
Repo: E:\rsch\laborJapan
Round: 02 (local Excel value-export validation for the two core population inputs)
Companion template: metadata/isa_estat_ddL001_ddL002_fast_confirmation_template_filled.csv

## A. Purpose

This note validates the user-provided local Excel exports of the ISA/e-Stat
24-12-t2 table for DDL_001 (Chinese resident count) and DDL_002 (total foreign
resident count), and records the resulting confirmation evidence. It is a
local-file validation task, not a web acquisition.

## B. Evidence boundary

- This is local-file validation and confirmation evidence.
- It is NOT data acquisition from the web.
- It is NOT API extraction.
- It is NOT final cleaning.
- It is NOT analysis.
- It does NOT confirm the research gap.
- It does NOT establish novelty.
- No new datasets were downloaded by Claude.
- Raw Excel files were NOT committed (data_raw/ remains ignored).
- No raw Excel file was modified, moved, renamed, deleted, or copied.
- No decision was approved; the decision log was NOT modified.
- Current status remains: gap under verification.

## C. Source and table identity

- Provider: e-Stat / Immigration Services Agency (出入国在留管理庁)
- Table ID: 24-12-t2
- Table: 在留外国人統計テーブルデータ（国籍・地域別　在留資格別　市区町村別）
- Reference period: 2024年12月 (令和6年12月末)
- Official page: https://www.e-stat.go.jp/stat-search/files?layout=datalist&lid=000001462230
- Terms of use: https://www.e-stat.go.jp/terms-of-use

## D. Local files validated

Four local files were placed by the user under data_raw/isa_estat/ (all ignored,
none committed):

- 24-12-t2_all_pivot.xlsx (PivotTable workbook, ~4.69 MB)
- 24-12-t2_all_values.xlsx (values export) - PRIMARY machine-readable input for DDL_002
- 24-12-t2_china_pivot.xlsx (PivotTable workbook, ~4.70 MB)
- 24-12-t2_china_values.xlsx (values export) - PRIMARY machine-readable input for DDL_001

Only the two *_values.xlsx files were read for structural validation (read-only).
The two *_pivot.xlsx workbooks are the source pivots and were not parsed.

## E. File structure checks

Both values files share an identical structure (sheet "Sheet1", header in row 1):

Columns (4): 市区町村コード | 都道府県 | 市区町村 | 合計 / 在留外国人数

| file | rows incl header | data rows | code non-empty | counts numeric | total sum |
| --- | --- | --- | --- | --- | --- |
| 24-12-t2_all_values.xlsx | 1892 | 1891 | yes | yes | 3,768,977 |
| 24-12-t2_china_values.xlsx | 1763 | 1762 | yes | yes | 873,247 |

Required columns present in both files: 市区町村コード, 都道府県, 市区町村,
合計 / 在留外国人数 (all YES).

First rows (all / china), e.g. 01101 札幌市中央区: all = 4021, china = 1035.
Both files end with a special aggregate row 99999 (48：未定・不詳 / 未定・不詳):
all = 5313, china = 1122. This is an "undetermined/unknown municipality"
aggregate, NOT a real municipality, and must be handled explicitly in cleaning.

## F. Compatibility checks (join key = 市区町村コード)

- all_values code count: 1891
- china_values code count: 1762
- overlapping codes: 1762
- china-only codes: 0
- all-only codes: 129
- rows where China count exceeds All count: 0
- all-only Tokyo (code prefix 13) codes: 13307, 13362, 13364, 13382
- left-join china_values -> all_values by 市区町村コード: FEASIBLE (china is a
  strict subset of all; china_only = 0)

No anomaly was found: every Chinese-count municipality also appears in the
all-foreign list, and no Chinese count exceeds the corresponding total.

## G. Interpretation for DDL rows

- DDL_001 (Chinese resident count) is SUPPORTED by 24-12-t2_china_values.xlsx as
  Chinese residents BY NATIONALITY/REGION (category 01_023：中国), NOT
  Chinese-origin residents.
- DDL_002 (total foreign resident count) is SUPPORTED by 24-12-t2_all_values.xlsx
  as total foreign residents across nationality/region categories in the same
  table family.

Both are from the same table (24-12-t2), same reference period (2024-12), same
geographic unit (市区町村), and share the join key 市区町村コード - so they are
mutually compatible.

## H. Cleaning assumptions for next task

- all_values should be the MASTER municipality list (1891 codes incl. the 99999
  aggregate).
- china_values should be LEFT-JOINED to all_values by 市区町村コード.
- The 129 all-only municipalities (including Tokyo codes 13307, 13362, 13364,
  13382) have no Chinese row. Per the interpretation rule, these rows must NOT be
  silently deleted: keep the all_values row and treat the missing Chinese count
  as a CANDIDATE ZERO only after documenting this assumption explicitly. This is
  a cleaning assumption requiring explicit report documentation.
- The 99999 未定・不詳 aggregate row must be handled explicitly (excluded from
  municipality-level spatial joins; retained only if a national reconciliation
  check is wanted).
- Non-Chinese foreign residents must NOT yet be computed; DDL_001 and DDL_002
  must first be formally approved and metadata-recorded.

## I. Recommended next action

Validation passes. Recommended next task: a NARROW acquisition/processing script
for DDL_001 and DDL_002 ONLY:

- read the two local values xlsx (read-only);
- create a processed population-baseline table (all + china by 市区町村コード,
  with the keep-and-flag rule for all-only municipalities and the 99999 row
  excluded from spatial joins);
- compute SHA-256 checksums for the raw xlsx files;
- create a metadata draft in the metadata template (source, table ID, year,
  geography, license, file names, checksums);
- do NOT commit the raw xlsx;
- do NOT compute derived variables (non-Chinese, shares) yet unless separately
  approved.

Do not write the final Introduction. Do not assert novelty. Status remains: gap
under verification.
