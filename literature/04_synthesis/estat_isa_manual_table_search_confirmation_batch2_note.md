# e-Stat/ISA Manual Table-Search Confirmation - Batch 2 Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Companion file: literature/02_matrices/estat_isa_manual_table_search_confirmation_batch2.csv

## A. Purpose

This note records batch 2 manual official table-search confirmation for the
population module. It focuses on whether ISA Statistics on Foreign Residents
(statistics code 00250012, provider tstat 000001018034) offers a
municipality-by-nationality table, and on whether the Population Census / Kokusei
Chosa (statistics code 00200521) can serve as a municipality/small-area
alternative for constructing Chinese residents, total foreign residents, and
non-Chinese foreign residents.

## B. Evidence boundary

- This is NOT a literature gap claim.
- This is NOT manuscript text and contains no Introduction.
- This does NOT prove novelty.
- No full statistical dataset was downloaded.
- No full extraction was run.
- No preprocessing or modeling was run.
- Confirmation is limited to official e-Stat / ISA / Census metadata and
  table-search pages. ESTAT_APP_ID was not set, so keyed WebAPI metadata
  enumeration (getStatsList) could not be run; only official non-key table-search
  pages were used.
- Official sources support data feasibility only; they do not prove the academic
  gap. Gap status remains: under verification.

## C. Confirmation summary table

| item | status | source/evidence route | remaining blocker | recommended next action |
| --- | --- | --- | --- | --- |
| ISA statistics code 00250012 | confirmed | e-Stat database search; ISA page | none | - |
| ISA provider tstat 000001018034 | confirmed | e-Stat database search | none | - |
| ISA nationality x prefecture table | confirmed (exists) | e-Stat classification metadata | exact statsDataId | use_ISA_for_prefecture_crosscheck_only |
| ISA municipality x nationality table | NOT FOUND | e-Stat DB listing + classification (nationality x residence-status x prefecture) | exhaustive title enumeration needs appId/manual browser | use_ISA_for_prefecture_crosscheck_only |
| ISA municipality total-foreign table | confirmed (exists, total only) | ISA/e-Stat | exact statsDataId | use_ISA_for_prefecture_crosscheck_only |
| Census 00200521 candidate nationality table | confirmed (nationality/foreign tables exist) | e-Stat Census file-search | exact statsDataId; China-at-municipality field check | evaluate_census_00200521 |
| Census municipality geography | confirmed (municipality tabulation available) | e-Stat Census search (6,740 municipality files) | exact table | evaluate_census_00200521 |
| Census small-area geography | partial (small-area category exists; nationality-by-country there not evident) | e-Stat Census search | small-area nationality detail | manual_browser_check |
| China category | ISA: yes (prefecture, code 01_023); Census: needs field check | ISA local obs + Census metadata | Census China code at municipality | evaluate_census_00200521 |
| total foreign category | ISA: yes (sosu); Census: yes (foreign total) | ISA + Census | exact codes | inspect_fields_before_download |
| non-Chinese construction | feasible at prefecture (ISA); partial pending field check at municipality (Census) | derived logic | Census exact table/codes | evaluate_census_00200521 |
| join-key to N03 | yes at municipality (JIS X 0402 == N03 code); small-area needs Census boundary | area-code logic | ward-vs-city aggregation decision | inspect_area_codes_next |

## D. Population-source decision

Decision status: PARTIAL.

- ISA 00250012 is NOT suitable as the main spatial-analysis population source
  unless a municipality-by-nationality table is later found. Across batch 1 and
  batch 2 the ISA classification is consistently nationality/region x
  residence-status x prefecture; no municipality x nationality table was found in
  the database listing. A municipality total-foreign table exists but cannot
  isolate Chinese residents.
- ISA should therefore be treated as a PREFECTURE-LEVEL CROSS-CHECK ONLY (Tokyo 13,
  Saitama 11, Chiba 12, Kanagawa 14), not the main model scale.
- The Population Census 2020 (Kokusei Chosa, statistics code 00200521) is the LIKELY
  MAIN MUNICIPALITY-LEVEL SOURCE. Official search confirmed that the 2020 census is
  the latest complete round, that nationality/foreign-population tables exist, and
  that municipality-level (shikuchoson) tabulation is available. However, the exact
  Chinese/category statsDataId and the field structure (confirming China as a
  discrete category at municipality level, and the exact vintage and codes) still
  require a dedicated Census confirmation batch. This is NOT resolved here.
- Small-area (shochiiki / chocho-aza) nationality to a specific country (China) is
  generally not published and was not evident; municipality is the finest unit that
  currently looks feasible for the Chinese-resident measure.

Net: use Census 00200521 as the main municipality-level source and ISA 00250012 as
a prefecture-level cross-check, conditional on the Census field check passing.

## E. Analytical implication

- The main comparison must NOT be Chinese residents vs all foreign residents.
- The correct comparison is Chinese residents vs non-Chinese foreign residents,
  where non_chinese_foreign = total_foreign - chinese_residents at the SAME spatial
  unit and year.
- If only prefecture-level ISA data were available, the metropolitan area would
  reduce to four spatial units, which is too coarse for the intended spatial
  opportunity-risk analysis. This is the core reason for moving the main population
  measure to the Census municipality level.

## F. API / metadata next-step implication

Most conservative next step: "Census 00200521 exact table and category confirmation
batch".

Rationale: the exact statsDataId is still unresolved for both ISA and Census (the
search pages do not expose 10-digit ids and ESTAT_APP_ID is unset), and the Census
is now the indicated main source. The next batch should confirm, from official
Census metadata, the exact nationality table under the 2020 Basic Complete
Tabulation, that China is a discrete category at municipality level, the total
foreign category, the exact statsDataId(s), and the municipality area-code join to
NLNI N03 - all before any small metadata test. A keyed "small metadata test script
scaffold" should follow only once the Census statsDataId and category codes are
fixed (and, ideally, ESTAT_APP_ID is provisioned). No full extraction in either
step.

## G. Safety statement

- No datasets were downloaded.
- No full extraction, preprocessing, or modeling was run.
- No raw API outputs were saved into or committed to the repo.
- No appId/API key was printed, written, or committed (ESTAT_APP_ID was not set;
  only the environment-variable placeholder is referenced in the design).
- No manuscript text was written; no novelty asserted; no final gap claimed.
- Gap status remains: under verification.
