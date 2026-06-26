# Census 00200521 Exact Table and Category Confirmation - Batch 1 Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Companion file: literature/02_matrices/census_00200521_exact_table_category_confirmation_batch1.csv

## A. Purpose

This note records exact table/category confirmation for the Population Census /
Kokusei Chosa (statistics code 00200521) as the main municipality-level population
source for the Tokyo-China project. Using keyed official e-Stat API metadata
queries (getStatsList and getMetaInfo only), it confirms the exact statsDataId,
the nationality category structure (including China), the total foreign category,
the municipality geography, the time/vintage, and the join-key logic needed to
construct Chinese residents, total foreign residents, and non-Chinese foreign
residents.

## B. Evidence boundary

- This is NOT a literature gap claim.
- This is NOT manuscript text and contains no Introduction.
- This does NOT prove novelty.
- No full statistical dataset was downloaded.
- No full extraction was run (only getStatsList and getMetaInfo metadata calls; no
  getStatsData / no data-value retrieval).
- No preprocessing or modeling was run.
- Confirmation is limited to official e-Stat / Census API metadata and table-search
  pages. ESTAT_APP_ID was used from the environment only; it was never printed,
  written to any file, or committed, and no API URL containing the appId was saved.
- No raw API outputs were saved into or committed to the repo.
- Official sources support data feasibility only; they do not prove the academic
  gap. Gap status remains: under verification.

## C. Confirmation summary table

| item | status | source/evidence route | remaining blocker | recommended next action |
| --- | --- | --- | --- | --- |
| Census statistics code 00200521 | confirmed | e-Stat API getStatsList | none | - |
| Census tstat / provider id | confirmed = 000001136464 (2020 Basic Complete Tabulation) | e-Stat API/metadata | none | - |
| Census year / vintage | confirmed = 2020 (Reiwa 2; SURVEY_DATE 202010; time 2020000000) | getMetaInfo | none | - |
| municipality-level nationality table | confirmed = statsDataId 0003445244 (TITLE 44-1) | getMetaInfo | none | prepare_small_metadata_test |
| exact statsDataId | confirmed = 0003445244 (primary); 0003445245 (DID variant) | getStatsList/getMetaInfo | none | prepare_small_metadata_test |
| China category | confirmed = cat02 code 102 (Chugoku) | getMetaInfo CLASS | none | prepare_small_metadata_test |
| total foreign category | confirmed = cat02 code 1 (Gaikokujin / foreign total) | getMetaInfo CLASS | distinguish from code 0 = all persons | prepare_small_metadata_test |
| non-Chinese construction | feasible = code 1 minus code 102, same table/year/area | derived | none | prepare_small_metadata_test |
| small-area nationality feasibility | not evident (country-detail stops at municipality/DID) | getMetaInfo across tables | small-area by-country source | inspect_small_area_boundary_next |
| municipality code logic | confirmed = 5-digit JIS (area dim n=1965; levels 1/2/4/5/6) | getMetaInfo area CLASS | ward-vs-city aggregation decision | inspect_area_codes_next |
| join-key to NLNI N03 | yes (5-digit JIS == N03 gyosei kuiki code) | code structure | reconcile 2020 vs N03 vintage | inspect_area_codes_next |
| API metadata feasibility | confirmed (keyed getStatsList/getMetaInfo) | e-Stat WebAPI | none | prepare_small_metadata_test |

Exact category codes (table 0003445244, dimension cat02 "kokuseki", 17 categories):
0 = total (all persons); 1 = foreign total; 101 = Korea; 102 = China; 103 =
Philippines; 104 = Thailand; 105 = Indonesia; 106 = Vietnam; 107 = India; 108 =
Nepal; 109 = UK; 110 = USA; 111 = Brazil; 112 = Peru; 113 = other; 2 = Japanese;
3 = unknown. The measurement dimension (tab) is population; cat01 is sex
(0 total, 1 male, 2 female); time is 2020 only.

## D. Population-source decision

Decision status: CONFIRMED.

- Census 00200521, 2020 Basic Complete Tabulation, table 0003445244 ("Foreigners:
  population by sex and nationality - national, prefecture, municipality") IS
  suitable as the MAIN municipality-level population source. It provides, at
  municipality level and for a single consistent year (2020):
  - Chinese residents = cat02 code 102;
  - total foreign residents = cat02 code 1;
  - non-Chinese foreign residents = code 1 minus code 102 (same table, year, and
    spatial unit -> a clean subtraction).
- All four target prefectures (Tokyo, Saitama, Chiba, Kanagawa) are covered;
  municipality area codes are standard 5-digit JIS and join directly to NLNI N03.
- ISA 00250012 remains a PREFECTURE-LEVEL CROSS-CHECK ONLY (it has no
  municipality x nationality table); it can validate the Census prefecture totals.

## E. Analytical implication

- The main comparison must NOT be Chinese residents vs all foreign residents.
- The correct comparison is Chinese residents vs non-Chinese foreign residents,
  where non-Chinese foreign residents = total foreign residents (cat02=1) minus
  Chinese residents (cat02=102) at the same spatial unit and year (2020).
- The Census supports municipality-level nationality but NOT small-area
  nationality-by-country (the country-detail tables stop at municipality / DID).
  Therefore MUNICIPALITY is the main analysis unit, unless another legally usable
  small-area nationality source is later confirmed. Small-area would also require a
  separate Census small-area (chocho-aza) boundary layer rather than N03.
- "Chinese" here is Census-declared nationality, not ethnicity/origin; this matches
  the project's operational definition and must be stated as such.

## F. API / metadata next-step implication

Exact statsDataId (0003445244) and the China (102) and total-foreign (1) category
codes ARE confirmed. Most conservative next step:

Recommended next task: "Census 00200521 small metadata test script scaffold".

This scaffold should design a tiny, parameterized metadata/count test (e.g.
getStatsData with cntGetFlg=Y or a narrow cdArea/cdCat slice) to verify the query
returns the expected municipality x nationality structure for the four target
prefectures - still NOT a full extraction. It must read ESTAT_APP_ID from the
environment only, never print/write/commit it, and never save raw API outputs into
the repo. Municipality-level is the main workflow; small-area remains optional and
is not pursued unless a by-country small-area source is later confirmed.

## G. Safety statement

- No datasets were downloaded.
- No full extraction was run (getStatsList / getMetaInfo metadata only; no
  getStatsData).
- No raw API outputs were saved into or committed to the repo.
- No appId/API key was printed, written, or committed; no API URL containing the
  appId was saved (recorded API URLs omit appId).
- No preprocessing or modeling was run.
- No manuscript text was written; no novelty asserted; no final gap claimed.
- Gap status remains: under verification.
