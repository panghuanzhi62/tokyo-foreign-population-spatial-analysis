# Round 01 B-Candidate Literature Review Note

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Run id reviewed: round01_api

## 1. Purpose

This note reviews the 21 preliminary B_partial_overlap_candidate records
produced by Round 01 of the API-based literature metadata discovery pipeline
(OpenAlex, Crossref, Semantic Scholar). It is a source-light, public synthesis
intended for the repository. It uses only metadata already retrieved by the
automated harvester; it does not reproduce raw API payloads.

## 2. Evidence status

- This is metadata-based screening only.
- It is NOT a final literature review.
- It does NOT confirm the research gap.
- It does NOT replace manual deep reading of full text.
- It does NOT include Google Scholar, SciSpace Deep Review, CiNii (no app id was
  available), manual J-STAGE search, or full-text PDF review.
- 0 preliminary A_direct_overlap_candidate items is NOT evidence that no
  direct-overlap literature exists. It only means the strict automated keyword
  filter flagged none in this small run.

## 3. Round 01 search coverage

- APIs reached: OpenAlex, Crossref, Semantic Scholar.
- APIs skipped: CiNii (no CINII_APP_ID in environment). Google Scholar was never
  queried (automated scraping is prohibited and out of scope).
- Semantic Scholar returned HTTP 429 (rate limited) on part of the run, so its
  contribution (27 normalized records) is partial.
- Unique candidates after deduplication: 262.
- Preliminary A_direct_overlap_candidate records: 0.
- Preliminary B_partial_overlap_candidate records: 21.
- Why raw API outputs are not committed: the raw JSONL payloads and candidate
  tables under outputs/literature_discovery/round01_api/ are bulk third-party
  metadata of uncertain redistribution status and are large/noisy. The
  repository is public, so only this curated, source-light note is committed;
  the raw outputs remain local and uncommitted.

## 4. B-candidate table

All 21 B_partial_overlap_candidate records are listed below using available
metadata only. NA indicates the field was not available from the API metadata.
The preliminary_overlap_reason column reports the automated keyword flags; the
likely_module column is a cautious analyst hint, not a verified classification.

| record_id | title | year | venue | doi_or_url | source_api | query_group | preliminary_overlap_reason | likely_module | needs_manual_verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| round01_api-0001 | Educationally Channeled International Labor Mobility: Contemporary Student Migration from China to Japan | 2009 | International Migration Review | 10.1111/j.1747-7379.2008.01152.x | openalex | chinese_migration_japan | keyword flags: chinese, service, tokyo_japan | Chinese migration / Chinese residents | yes |
| round01_api-0004 | Ethnic Enterprise in America: Business and Welfare among Chinese, Japanese and Blacks | 1972 | International Migration Review | 10.2307/3002830 | openalex | chinese_migration_japan | keyword flags: chinese, service, tokyo_japan | unclear | yes |
| round01_api-0018 | Chinese Newcomers in Japan: Migration Trends, Profiles and the Impact of the 2011 Earthquake | 2013 | Asian and Pacific Migration Journal | 10.1177/011719681302200204 | crossref | chinese_migration_japan | keyword flags: chinese, disaster, tokyo_japan | Chinese migration / Chinese residents | yes |
| round01_api-0033 | Contributing factors to the underestimation of fire following earthquake damage among residents in Tokyo, Japan | 2026 | NA | 10.2139/ssrn.6688593 | crossref | chinese_residents_tokyo | keyword flags: disaster, tokyo_japan | disaster risk / vulnerability | yes |
| round01_api-0080 | Residential Segregation in Japan: Ethnic Stratification in a Global New Destination | 2024 | NA | 10.31235/osf.io/beh43 | crossref | foreign_residents_segregation | keyword flags: housing, theory, tokyo_japan | spatial assimilation / co-ethnic networks | yes |
| round01_api-0081 | Residential Segregation in Japan: Ethnic Stratification in a Global New Destination (v2) | 2025 | NA | 10.31235/osf.io/beh43_v2 | crossref | foreign_residents_segregation | keyword flags: housing, theory, tokyo_japan | spatial assimilation / co-ethnic networks | yes |
| round01_api-0086 | Administrative Services for Foreign Residents | 1997 | Immigration Policy and Foreign Workers in Japan | 10.1057/9780230374522_8 | crossref | foreign_residents_segregation | keyword flags: non_chinese_comparison, service, tokyo_japan | service accessibility | yes |
| round01_api-0146 | A field experiment on discrimination against foreigners in the rental housing market in Japan examining the 23 wards | 2023 | Journal of the Japanese and International Economies | 10.1016/j.jjie.2023.101273 | openalex | housing_discrimination | keyword flags: housing, tokyo_japan | housing constraint | yes |
| round01_api-0147 | A Field Experiment on Discrimination Against Foreigners in the Rental Housing Market in Japan Examining the 23 Wards (preprint) | 2022 | SSRN Electronic Journal | 10.2139/ssrn.4192485 | openalex | housing_discrimination | keyword flags: housing, tokyo_japan | housing constraint | yes |
| round01_api-0149 | Discrimination against the atypical type of tenants in the Tokyo private rental housing market | 2022 | Journal of Housing Economics | 10.1016/j.jhe.2022.101879 | openalex | housing_discrimination | keyword flags: housing, tokyo_japan | housing constraint | yes |
| round01_api-0153 | Rental housing discrimination against Chinese minorities in Spain: a new instant messaging correspondence test | 2025 | Social Forces | 10.1093/sf/soaf140 | openalex | housing_discrimination | keyword flags: chinese, housing | housing constraint | yes |
| round01_api-0155 | Factors enhancing residential satisfaction of foreign residents toward settlement: A case study of Toshima City, Tokyo | 2024 | Journal of Housing and the Built Environment | 10.1007/s10901-024-10160-3 | openalex | housing_discrimination | keyword flags: housing, non_chinese_comparison, tokyo_japan | housing constraint | yes |
| round01_api-0156 | Disentangling transaction-stage and management-stage discrimination in the rental housing market | 2026 | Journal of Housing Economics | 10.1016/j.jhe.2026.102134 | crossref | housing_discrimination | keyword flags: housing, tokyo_japan | housing constraint | yes |
| round01_api-0157 | Supply Management of Rental Housing Facilities: Effect of Changes in the Quality of Housing Equipment in the Tokyo Housing market | 2020 | Modern Perspectives in Business Applications | 10.5772/intechopen.86163 | crossref | housing_discrimination | keyword flags: housing, tokyo_japan | housing constraint | yes |
| round01_api-0167 | Adult Education for a Multiethnic Community: Japan's Challenge | 1996 | NA | NA | semantic_scholar | housing_discrimination | keyword flags: service, tokyo_japan | service accessibility | yes |
| round01_api-0199 | The 2011 eastern Japan great earthquake disaster: Overview and comments | 2011 | International Journal of Disaster Risk Science | 10.1007/s13753-011-0004-9 | openalex | disaster_vulnerability | keyword flags: disaster, opportunity_risk, tokyo_japan | disaster risk / vulnerability | yes |
| round01_api-0200 | Utilizing Population Distribution Patterns for Disaster Vulnerability Assessment: Case of Foreign Residents in the Tokyo area | 2021 | International Journal of Environmental Research and Public Health | 10.3390/ijerph18084061 | openalex | disaster_vulnerability | keyword flags: disaster, non_chinese_comparison, tokyo_japan | disaster risk / vulnerability | yes |
| round01_api-0202 | Potential of mosques to serve as evacuation shelters for foreign Muslims during disasters: a case study in Gunma, Japan | 2021 | Natural Hazards | 10.1007/s11069-021-04883-7 | openalex | disaster_vulnerability | keyword flags: disaster, tokyo_japan | disaster risk / vulnerability | yes |
| round01_api-0210 | Voices of Foreign Residents in Yokohama and Tokyo at the Time of the 1923 Kanto Earthquake | 2023 | Journal of Disaster Research | 10.20965/jdr.2023.p0598 | crossref | disaster_vulnerability | keyword flags: disaster, non_chinese_comparison, tokyo_japan | disaster risk / vulnerability | yes |
| round01_api-0212 | Bolstering disaster preparedness among Japan's foreign residents | 2022 | NA | 10.59425/eabc.1647381639 | crossref | disaster_vulnerability | keyword flags: disaster, non_chinese_comparison, tokyo_japan | disaster risk / vulnerability | yes |
| round01_api-0215 | The impact of COVID-19 pandemic on public engagement approaches to disaster preparedness for foreign residents | 2022 | International Journal of Disaster Resilience in the Built Environment | 10.1108/ijdrbe-08-2021-0095 | crossref | disaster_vulnerability | keyword flags: disaster, non_chinese_comparison, tokyo_japan | disaster risk / vulnerability | yes |

## 5. Direct-overlap risk assessment

The provisional topic requires the integration, in Metropolitan Tokyo, of:
Chinese residents or Chinese nationals, plus a Chinese vs non-Chinese foreign
resident comparison, plus housing, plus transit/accessibility, plus services,
plus disaster/risk exposure, plus an opportunity-risk typology or mismatch.

Assessment of the 21 B candidates:

- The housing cluster (round01_api-0146, 0147, 0149, 0155, 0156, 0157) covers
  rental housing discrimination or housing constraints for foreigners in Tokyo,
  but addresses the housing module alone and is not Chinese-specific.
- The disaster cluster (round01_api-0199, 0200, 0202, 0210, 0212, 0215) covers
  disaster vulnerability or preparedness for foreign residents in/around Tokyo,
  but addresses the disaster module alone and is generally not Chinese-specific.
- The Chinese-focused items (round01_api-0001, 0018) cover student migration and
  newcomer profiles, not the full opportunity-risk environment combination.
- The segregation items (round01_api-0080, 0081) are closest to the Sun 2026
  spatial-assimilation line and should be positioned against it, not claimed as
  novel ground.
- Two items are likely geographic false positives (round01_api-0004 is US-based;
  round01_api-0153 is Spain-based) flagged only by surface keywords.

Conclusions, stated cautiously:

- No clear direct-overlap item was identified in this preliminary metadata
  screen.
- This does not prove that no such literature exists.
- Manual deep review and additional databases (CiNii, J-STAGE, SciSpace, and
  full-text reading) are still required before any gap claim.

## 6. Prioritized manual verification list

The following 13 items are the highest priority for manual verification, chosen
because each touches a core module of the provisional topic in a Japan/Tokyo
context.

1. round01_api-0200 - Disaster vulnerability assessment of foreign residents in
   the Tokyo area; closest single item to the disaster module for the target
   population and geography.
2. round01_api-0018 - Chinese newcomers in Japan and the 2011 earthquake; rare
   item pairing the Chinese population with disaster exposure.
3. round01_api-0146 - Field experiment on rental housing discrimination against
   foreigners across Tokyo's 23 wards; anchors the housing module.
4. round01_api-0149 - Discrimination against atypical tenants in the Tokyo
   private rental market; complements the housing-discrimination evidence.
5. round01_api-0155 - Residential satisfaction and settlement of foreign
   residents in Toshima City, Tokyo; links housing to settlement environment.
6. round01_api-0080 - Residential segregation and ethnic stratification in
   Japan; must be positioned against the Sun 2026 assimilation line.
7. round01_api-0210 - Foreign residents in Yokohama and Tokyo during the 1923
   Kanto earthquake; historical disaster-exposure framing for foreigners.
8. round01_api-0212 - Disaster preparedness among Japan's foreign residents;
   directly addresses the disaster-services interface.
9. round01_api-0215 - COVID-era public engagement for foreign-resident disaster
   preparedness; recent service/disaster crossover.
10. round01_api-0086 - Administrative services for foreign residents; anchors the
    service-accessibility module.
11. round01_api-0001 - Student migration from China to Japan; foundational
    Chinese-migration context for the target population.
12. round01_api-0156 - Recent rental-market discrimination study; checks how
    current the housing-discrimination evidence is.
13. round01_api-0202 - Mosques as evacuation shelters for foreign residents;
    connects disaster risk to community service infrastructure.

Lower-priority or likely false positives (round01_api-0004 US, 0153 Spain, 0033
general Tokyo fire risk, 0157 general housing supply, 0199 earthquake overview,
0147 preprint duplicate of 0146, 0167 1996 education essay) should be checked
only after the items above.

## 7. Next action

- Manually verify the highest-risk B candidates through DOI, publisher page,
  OpenAlex, Crossref, Semantic Scholar, CiNii, J-STAGE, or uploaded PDF
  metadata.
- Use SciSpace Deep Review for the highest-risk candidates.
- Then populate literature_matrix.csv and gap_verification_matrix.csv with the
  verified records and full overlap coding, positioned against Sun 2026.
- Do not write the manuscript introduction yet. The final research gap must not
  be asserted until it is supported by a verified literature matrix and
  deep-reading notes.
