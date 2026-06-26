# Round 02 Japanese-Language Search Queries

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02

Notes on use:
- English lines are working translations only, not official titles.
- "Source priority" lists where to run each query first.
- "Matrix target" is the expected destination if a result verifies; it is a
  hint, not a commitment. Final coding follows the protocol decision logic.
- CiNii Research API needs CINII_APP_ID (absent here), so CiNii queries are run
  by manual search. J-STAGE and NDL are searched manually or via permitted
  metadata access only. No Google Scholar scraping; no PDF download.
- This file is UTF-8 with LF. Japanese strings are recorded in Japanese.

## Query group QG-A: Chinese residents in Tokyo / Japan

| query_id | japanese_query | english_working_translation | source_priority | expected_relevance | matrix_target |
| --- | --- | --- | --- | --- | --- |
| R02-Q01 | 中国人 住民 東京 居住 | Chinese residents Tokyo housing/residence | CiNii, J-STAGE, NDL | high (target population) | gap_verification_matrix |
| R02-Q02 | 中国人 東京 集住 | Chinese Tokyo residential concentration | CiNii, J-STAGE | high (concentration; position vs Sun 2026) | gap_verification_matrix |
| R02-Q03 | 中国籍 住民 東京 | Chinese-nationality residents Tokyo | CiNii, e-Stat, ISA | high (nationality-based) | gap_verification_matrix |
| R02-Q04 | 中国人 移民 日本 居住 | Chinese immigrants Japan residence | CiNii, NDL | medium-high (migration context) | literature_matrix |

## Query group QG-B: Foreign-resident distribution / segregation

| query_id | japanese_query | english_working_translation | source_priority | expected_relevance | matrix_target |
| --- | --- | --- | --- | --- | --- |
| R02-Q05 | 在留外国人 東京 居住 分布 | Resident foreigners Tokyo residential distribution | CiNii, e-Stat, ISA | high (spatial distribution) | gap_verification_matrix |
| R02-Q06 | 外国人住民 東京 居住分離 | Foreign residents Tokyo residential segregation | CiNii, J-STAGE | high (segregation; vs Sun 2026) | gap_verification_matrix |
| R02-Q18 | 居住分離 エスニック 日本 | Residential segregation ethnic Japan | CiNii, J-STAGE | medium-high (theory/comparator) | literature_matrix |

## Query group QG-C: Housing discrimination / rental constraint

| query_id | japanese_query | english_working_translation | source_priority | expected_relevance | matrix_target |
| --- | --- | --- | --- | --- | --- |
| R02-Q07 | 外国人 住宅 差別 東京 | Foreigners housing discrimination Tokyo | CiNii, J-STAGE | high (housing module) | gap_verification_matrix |
| R02-Q08 | 外国人 賃貸住宅 差別 日本 | Foreigners rental housing discrimination Japan | CiNii, J-STAGE | high (housing module) | gap_verification_matrix |

## Query group QG-D: Disaster vulnerability / evacuation

| query_id | japanese_query | english_working_translation | source_priority | expected_relevance | matrix_target |
| --- | --- | --- | --- | --- | --- |
| R02-Q09 | 外国人住民 東京 防災 避難 | Foreign residents Tokyo disaster-prevention evacuation | CiNii, TMG, J-STAGE | high (disaster module) | gap_verification_matrix |
| R02-Q10 | 在留外国人 災害 脆弱性 東京 | Resident foreigners disaster vulnerability Tokyo | CiNii, J-STAGE | high (disaster module) | gap_verification_matrix |
| R02-Q21 | 避難所 アクセス 外国人 東京 | Evacuation-shelter access foreigners Tokyo | CiNii, TMG, GSI | high (disaster + accessibility) | gap_verification_matrix |

## Query group QG-E: Service access (multilingual / administrative / health / childcare / livelihood)

| query_id | japanese_query | english_working_translation | source_priority | expected_relevance | matrix_target |
| --- | --- | --- | --- | --- | --- |
| R02-Q11 | 外国人住民 多言語 支援 東京 | Foreign residents multilingual support Tokyo | TMG, ward pages, CiNii | medium-high (service module) | official_source_registry |
| R02-Q12 | 外国人住民 行政サービス 東京 | Foreign residents administrative services Tokyo | TMG, ward pages, CiNii | medium-high (service module) | official_source_registry |
| R02-Q13 | 外国人 医療 アクセス 日本 | Foreigners healthcare access Japan | CiNii, J-STAGE | medium (service module) | literature_matrix |
| R02-Q14 | 外国人 子育て 教育 支援 東京 | Foreigners childcare/education support Tokyo | TMG, ward pages, CiNii | medium (service module) | official_source_registry |
| R02-Q15 | 外国人 生活支援 サービス 東京 | Foreigners livelihood-support services Tokyo | TMG, ward pages, CiNii | medium (service module) | official_source_registry |

## Query group QG-F: Arrival infrastructure / settlement support

| query_id | japanese_query | english_working_translation | source_priority | expected_relevance | matrix_target |
| --- | --- | --- | --- | --- | --- |
| R02-Q16 | 到着インフラ 移民 日本 | Arrival infrastructure immigrants Japan | CiNii, NDL | medium (concept) | hold |
| R02-Q17 | 移民 生活基盤 都市 日本 | Immigrants living-base urban Japan | CiNii, NDL | medium (concept) | literature_matrix |

## Query group QG-G: Spatial method / GIS

| query_id | japanese_query | english_working_translation | source_priority | expected_relevance | matrix_target |
| --- | --- | --- | --- | --- | --- |
| R02-Q19 | 空間分析 在留外国人 日本 | Spatial analysis resident foreigners Japan | CiNii, J-STAGE | medium-high (method support) | literature_matrix |
| R02-Q20 | GIS 外国人住民 東京 | GIS foreign residents Tokyo | CiNii, J-STAGE, GSI | medium-high (method support) | literature_matrix |

## Coverage summary

- 21 queries across 7 groups (QG-A..QG-G).
- Target population coverage: Chinese residents/nationals (QG-A), foreign
  residents broadly (QG-B..QG-G).
- Module coverage: housing (QG-C), disaster (QG-D), services (QG-E),
  distribution/segregation (QG-B), arrival/settlement (QG-F), spatial method
  (QG-G).
- Official-source-leaning queries (QG-E, parts of QG-B/QG-D) route to
  official_source_registry.csv, not the peer-reviewed literature matrix.
- No query is expected, by itself, to confirm the integrated opportunity-risk
  mismatch combination; results are coded individually per the protocol.
