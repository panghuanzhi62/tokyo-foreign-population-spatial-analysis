# e-Stat/ISA Exact statsDataId and API-Parameter Discovery - Batch 1 Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Companion file: literature/02_matrices/estat_isa_api_parameter_discovery_batch1.csv

## A. Purpose

This note records batch 1 of e-Stat/ISA exact statsDataId and API-parameter
discovery for the Tokyo-China population module, before any data extraction. It
identifies confirmed table identity, area-code logic, time-code logic,
nationality/total category logic, and a feasible API-parameter plan for
constructing Chinese residents, total foreign residents, and non-Chinese foreign
residents (= total foreign - Chinese).

## B. Evidence boundary

- This is NOT a literature gap claim.
- This is NOT manuscript text and contains no Introduction.
- This does NOT prove novelty.
- No full statistical dataset was downloaded.
- No full extraction was run.
- No preprocessing or modeling was run.
- Discovery is limited to official e-Stat table-search/database pages, the official
  e-Stat WebAPI metadata-endpoint design, and the official ISA statistics page. No
  raw API outputs were saved or committed. No appId was printed, written, or
  committed (ESTAT_APP_ID was not set in this environment).

## C. Discovery summary table

| item | status | evidence/source | remaining blocker | recommended next action |
| --- | --- | --- | --- | --- |
| statistics code 00250012 | confirmed | e-Stat database search; ISA page | none | - |
| survey/dataset name | confirmed (Zairyu Gaikokujin Tokei / Statistics on Foreign Residents) | e-Stat; ISA | none | - |
| provider statistic id (tstat) | confirmed = 000001018034 | e-Stat database search | none | - |
| table family 24-12-t2 | partial (nationality x prefecture family; t-number is ISA table numbering) | local obs + ISA page | exact statsDataId | manual_browser_check |
| candidate statsDataId | NOT confirmed (not exposed on JS search pages; appId unset) | e-Stat search pages | resolve via getStatsList or manual DB drill | manual_browser_check |
| China category code | partial (01_023 from local observation) | local obs | verify via live getMetaInfo cdCat | inspect_fields_before_download |
| total foreign category | partial (total/sosu exists) | e-Stat classification | exact cdCat code | inspect_fields_before_download |
| area code logic | partial (prefecture JIS confirmed; municipality x nationality unavailable) | e-Stat; ISA | municipality source | inspect_area_codes_next |
| time code logic | partial (biannual Jun/Dec; latest 2025-06) | e-Stat; ISA | exact cdTime codes | inspect_time_codes_next |
| API endpoint/parameter plan | designed (getStatsList -> getMetaInfo -> getStatsData) | e-Stat WebAPI design | ESTAT_APP_ID not set | prepare_small_metadata_test |
| non-Chinese construction | feasible at prefecture; pending at municipality | derived logic | municipality source | inspect_fields_before_download |

## D. Population construction assessment

Conservative reading:

- Chinese resident extraction: FEASIBLE at PREFECTURE level. The survey
  (statistics code 00250012, provider tstat 000001018034) provides foreign
  residents by nationality/region (incl. China) crossed with prefecture and
  residence status; the flexible 2019+ tables add age and sex but remain capped at
  prefecture.
- Total foreign resident extraction: FEASIBLE. A total (sosu) category exists in
  the same survey; municipality totals also exist but only as total foreign, not
  split by nationality.
- Non-Chinese foreign residents (= total foreign - Chinese): FEASIBLE at PREFECTURE
  level when both terms are taken from the same table, vintage, and geography.
- Consistency across Tokyo, Saitama, Chiba, Kanagawa: YES at the prefecture level
  (codes 13, 11, 12, 14).
- What still needs confirmation before extraction: the exact statsDataId; the live
  cdCat codes for China and total; the exact cdTime codes; and - the key issue -
  whether a MUNICIPALITY x nationality table exists at all.

Key finding / decision point: ISA Zairyu Gaikokujin Tokei (00250012) does not appear to offer
a municipality-by-nationality cross-tab; nationality is published at prefecture
level, and municipality data is total-foreign only. A prefecture-level analysis
gives only four spatial units for the metropolitan area, which is too coarse for
the intended spatial opportunity-risk analysis. The likely municipality-level
source for Chinese residents is the Population Census (kokuseki-betsu by
municipality/small-area, a different survey, statistics code 00200521), with ISA
retained for prefecture-level cross-check. Confirming this is the main task for the
next batch and is NOT resolved here.

## E. API design sketch (no secrets)

1. Provide ESTAT_APP_ID via environment variable only; never print, write, or
   commit it. If absent (as now), use official HTML database pages for discovery
   instead of keyed calls.
2. Query official metadata for statistics code 00250012 (getStatsList with
   statsCode=00250012), or open the e-Stat database listing under tstat
   000001018034.
3. Filter for the relevant ISA table family / table title (nationality x
   prefecture; and any municipality x nationality table if present).
4. Identify the candidate statsDataId (10-digit id) for the chosen table.
5. Inspect metadata dimensions with getMetaInfo: cdArea (area), cdTime (time),
   cdCat (nationality incl. China, and total/sosu).
6. Run only a tiny metadata or count test later (cntGetFlg=Y), not full extraction.
7. Design full extraction (getStatsData) only after statsDataId, category codes,
   and area codes are fixed.

Endpoints (official): rest/3.0/app/json/getStatsList, .../getMetaInfo,
.../getStatsData. No appId value appears in any committed file.

## F. Blocking issues

- statsDataId still pending (not exposed on JS search pages; ESTAT_APP_ID unset, so
  getStatsList could not be run; manual DB drill or provisioning the appId needed).
- Table-title/family precision: ISA t-number (24-12-t2) is ISA's own table
  numbering and must be matched to the e-Stat statsDataId.
- Municipality-level availability: a municipality x nationality table is NOT
  confirmed in ISA 00250012 (this is the dominant blocker).
- Area-code to N03 join: e-Stat cdArea to NLNI N03 administrative code join is only
  relevant once a municipality-level nationality source is confirmed.
- Time/vintage: exact cdTime codes pending; vintage must align across the Chinese
  and total terms and reasonably with the spatial layer years.
- Category-code ambiguity: China (01_023) and total (sosu) codes need live
  getMetaInfo verification.
- API appId/environment: ESTAT_APP_ID not set; keyed metadata calls deferred.
- Analytical caution: do not use Chinese-vs-all-foreigners as the final contrast;
  the comparator is non-Chinese foreign residents (total minus Chinese) at the same
  unit and period.

## G. Recommended next step

Recommended next task: "e-Stat/ISA manual table-search confirmation batch 2".

Rationale (conservative): the statistics code, survey, and provider tstat are
confirmed, and prefecture-level construction is feasible, but two blockers remain
unresolved: (1) the exact statsDataId is not yet captured (the search pages do not
expose it and ESTAT_APP_ID is unset), and (2) - more important - a
municipality-by-nationality table is not confirmed to exist in ISA 00250012, while
the project needs a municipality-level Chinese-resident measure. Batch 2 should, by
manual official table-search: (a) capture the exact statsDataId(s) for the
nationality tables under tstat 000001018034; (b) determine definitively whether any
ISA municipality x nationality table exists; and (c) if it does not, evaluate the
Population Census 2020 municipality/small-area nationality table (statistics code
00200521) as the municipality-level source, keeping ISA for prefecture cross-check.

Only once statsDataId and the municipality-level source are fixed should the work
move to "e-Stat/ISA small metadata test script scaffold" (a tiny metadata/count
test, still no full extraction). No large dataset download, no full extraction, no
preprocessing/modeling, no Introduction, no novelty claim; gap status remains under
verification.
