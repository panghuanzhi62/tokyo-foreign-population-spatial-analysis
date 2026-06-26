# ISA Municipality x Nationality x Residence-Status Table-Data (t2) Verification - Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Companion CSV: literature/02_matrices/isa_municipality_nationality_status_table_verification.csv

## A. Purpose

Verify whether the MOJ / Immigration Services Agency (ISA) Statistics on Foreign
Residents (在留外国人統計, e-Stat statistics code 00250012) "table data" (テーブルデータ)
table 2 - 国籍・地域別 在留資格別 市区町村別 (nationality/region by residence status by
municipality) - can support municipality-level Chinese registered-foreign-resident
STOCK for 2023-2025. The specific files checked: 23-12-t2, 24-06-t2, 24-12-t2, 25-06-t2.

## B. Relationship to the prior ISA conclusion (NOT overwritten)

The earlier batch-2 assessment concluded ISA was "prefecture-only" and selected the
Census (00200521) as the municipality-level source. That conclusion was based on, and
remains correct for, the e-Stat DATABASE / API route, and for recent years:

- ISA survey 00250012 has only 20 DATABASE datasets; NONE have survey dates in
  2023-2025 (recent data is file provision, not DB).
- The only municipality x nationality DATABASE table (statsDataId 0003147283,
  "市区町村別 国籍・地域別 在留外国人") has China at municipality level (code 105) across
  1922 municipalities (verified sample codes 11201, 12101, 13101, 14101), BUT its time
  dimension ends at 2017-06 and it has NO residence-status dimension.

This verification does NOT overwrite that conclusion. It adds a separate finding: the
ISA t2 EXCEL table-data (file provision) is a different, file-based municipality-level
route that requires its own verification. In short:
- DB / API route: prefecture-only for recent years (confirmed).
- t2 Excel table-data route: municipality-level, recent years, file-based - examined
  here and found PARTIALLY USABLE pending file-level confirmation.

## C. What was confirmed (official metadata, keyed where possible)

- ISA publishes municipality x nationality data as a product (the legacy DB table
  proves China-by-municipality was produced through 2017-06; municipality codes are
  standard 5-digit JIS, matching the confirmed 251 Census codes).
- Recent periods (2023-12, 2024-06, 2024-12, 2025-06) exist as files under 00250012;
  the e-Stat file-search reports EXCEL (484), PDF (415), and DB (143) provision and the
  2023/2024/2025 June/December periods are present.
- For 2018+ municipality x nationality (and the nationality x residence-status x
  municipality cross-tab), the route is the t2 Excel table-data, NOT the DB/API.

## D. What was NOT confirmed (needs file-level inspection)

- The exact t2 table number/title and the precise per-file structure for each period
  were not read directly: the MOJ page (toukei_ichiran_touroku.html) was blocked by a
  network/security policy in this environment, and the e-Stat file-search pages are
  JS-driven and did not expose individual file titles.
- Therefore the presence of the residence-status (在留資格別) dimension AND a total
  (総数) status (or safe aggregation across statuses) at municipality level, and the
  exact publication dates, require opening the actual Excel file.

## E. Conservative conclusion (per the controlled set)

For all four t2 files (23-12-t2, 24-06-t2, 24-12-t2, 25-06-t2): PARTIALLY USABLE.

- usable for recent municipality-level Chinese registered-resident stock: PARTIALLY -
  the product and municipality x nationality structure are confirmed in principle and
  the period Excel files exist, but the exact t2 schema (residence-status + total,
  municipality column, China category code in the table-data classification) must be
  confirmed by opening the Excel.
- 2023-to-2025 growth: supported (ISA-to-ISA, same source and definition).
- 2020-to-2024/2025 growth: PARTIAL with a caveat - do NOT mix Census 2020 (00200521)
  with ISA 00250012; they are different population concepts (Census usual-residence
  enumeration vs ISA registered residents). For an ISA growth series, use ISA-to-ISA
  (ISA also publishes 2020 table-data); the Census remains the main municipality source
  per the prior decision, with ISA as cross-check / alternative recent-stock series.

For the legacy DB table 0003147283: NOT USABLE for 2023-2025 (time ends 2017-06; no
residence-status dimension); retained as evidence only.

## F. Definitional caution

- "Chinese" here is registered nationality (在留カード / 在留資格 registration), not
  ethnicity/origin. ISA stock and Census population are NOT the same measure; any joint
  use must state the definitional difference explicitly and avoid implying equivalence.
- ISA municipality coverage and designated-city ward representation must be checked
  against the confirmed 251 Census ward-level units before any join.

## G. Recommended next step

If the t2 Excel route is to be pursued: "ISA t2 table-data municipality schema
inspection" - download ONE t2 Excel (e.g. 25-06-t2 or 24-12-t2) to a LOCAL-ONLY raw
folder (data_raw_official/, never committed) and confirm: the 市区町村 column and
5-digit code; the 国籍・地域 classification and the China category; the 在留資格 dimension
and a 総数 (total) status; and coverage of the 4 target prefectures. Do not commit the
Excel or any raw values. Commit only a small schema-confirmation summary.

This task did not download or commit any Excel/PDF/raw data. No modeling was run. This
is not manuscript text, not a novelty claim, and not a gap-confirmation. Gap status
remains: under verification.
