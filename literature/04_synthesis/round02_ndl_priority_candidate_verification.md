# Round 02 NDL Priority-Candidate Verification

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (Japanese-source verification - NDL priority candidates and official sources)

## A. Purpose

This note verifies the priority academic candidates (R02_NDL_043, R02_NDL_087,
R02_NDL_088, R02_NDL_068) and the priority official-source candidates
(R02_NDL_OFF_002, R02_NDL_OFF_001) identified from the Round 02 NDL metadata-only
search. Verification used public metadata only (NDL stable URLs and locally
saved NDL metadata, the DOI resolver, and the Crossref / OpenAlex APIs). No PDFs
were downloaded, no NDL HTML pages were scraped, no Google Scholar was scraped,
no browser automation was used, and no credentials were stored.

## B. Evidence status

- This is metadata / source-level verification only.
- It is NOT a full-text review (no PDFs read).
- It does NOT confirm the research gap.
- It does NOT prove the absence of direct-overlap literature.
- Japanese-language translation and full-text reading may still be required
  before any item is treated as confirmed evidence.
- Official-source suitability and licensing still require manual checking where
  metadata is incomplete.
- Current status: gap under verification.

## C. Academic candidate verification table

| source_id | original_title | english_working_title | year | verification_status | likely_module | matrix_disposition | overlap_category | reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R02_NDL_043 | 「移民」の住む場所 : 日本の住宅市場における居住格差の実証分析 | Where Migrants Live: an empirical analysis of residential disparity in Japan's housing market | 2026 | verified_by_ndl_metadata | housing / residential disparity | add_to_both_matrices | B_partial_overlap_candidate | Recent empirical housing-market residential-disparity book on immigrants in Japan; relevant to the housing module, though Japan-wide and not Chinese/Tokyo-specific. | Translate/read; confirm whether Chinese residents or Tokyo are separately analyzed. |
| R02_NDL_087 | 外国人児童生徒教育フォーラム : 報告書 | Forum on the Education of Foreign Children and Students: report | 2006 | verified_by_ndl_metadata | service / education access | add_to_literature_matrix_only | B_partial_overlap_candidate | Forum report on foreign-children education; non-empirical background, not Chinese-specific; weak for gap verification. | Translate; keep as service-access background. |
| R02_NDL_088 | 外国人児童生徒の就学前教育を考える | Considering Pre-school Education for Foreign Children and Students | 2006 | verified_by_ndl_metadata | service / childcare-education access | add_to_literature_matrix_only | B_partial_overlap_candidate | Pre-school education for foreign children; non-empirical background, not Chinese-specific; weak for gap verification. | Translate; keep as service-access background. |
| R02_NDL_068 | 岡山県総社市に暮らすブラジル人住民の言語生活 : 外国人住民の日本語学習支援を考える | Language Life of Brazilian Residents in Soja City, Okayama: Considering Japanese-Learning Support for Foreign Residents | 2014 | verified_by_doi_and_metadata | service / language support | add_to_literature_matrix_only | B_partial_overlap_candidate | DOI 10.19024/jajls.17.1_36 and year 2014 confirmed via OpenAlex (W571395046; The Japanese Journal of Language in Society 17(1):36); but Okayama (not Tokyo) and Brazilian (not Chinese); comparator/background only. | Keep as non-Tokyo, non-Chinese service/language-support comparator. |

Verification routes (public metadata only):
- R02_NDL_043, _087, _088: not found in OpenAlex/Crossref (Japanese books/reports);
  verified by NDL library records (stable NDL "books" permalinks).
- R02_NDL_068: exact title match in OpenAlex (W571395046) supplied the DOI
  (10.19024/jajls.17.1_36) and year (2014) that the NDL harvest lacked.

## D. Official-source verification table

| source_id | institution | source_title | year | verification_status | domain | use_in_analysis | registry_disposition | reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R02_NDL_OFF_002 | 自治体国際化協会 (CLAIR) | 自治体国際化フォーラム | 2005 | verified_by_institution_metadata | multilingual support; municipal multicultural/international policy | service_infrastructure_context | update_official_source_registry_row (kept/updated) | CLAIR is a recognized quasi-official local-government international-relations body; the periodical provides national municipal multilingual/multicultural context. | Consider for municipal multilingual/administrative service context; check specific issues manually. |
| R02_NDL_OFF_001 | 法務省民事局 (MOJ Civil Affairs Bureau) | 訓令・通達・回答(5273) ... 中国人夫婦 ... 養子縁組 ... (法務省民一第1540号) | 2010 | weak_relevance | administrative / family-registration law (adoption) | weak_background_only | update_official_source_registry_row (marked weak relevance) | MOJ adoption-registration directive referencing a Chinese couple residing in Japan; off-topic for the opportunity-risk modules; the earlier "housing" flag was a false positive from the word 居住 (residing). | Low priority; optional manual check; do not use as a substantive source. |

## E. Matrix additions or updates

Academic:
- Added to literature_matrix.csv: 4 (R02_NDL_043, R02_NDL_087, R02_NDL_088,
  R02_NDL_068).
- Added to gap_verification_matrix.csv: 1 (R02_NDL_043).
- Held: 0.
- Excluded: 0.

Official:
- Kept/updated in official_source_registry.csv: 1 (R02_NDL_OFF_002 - updated
  institution, year, domain, use_in_analysis = service_infrastructure_context,
  verified_status = verified_by_institution_metadata).
- Marked weak relevance (kept in registry): 1 (R02_NDL_OFF_001 -
  use_in_analysis = weak_background_only, verified_status = weak_relevance;
  institution/year corrected, false-positive housing domain corrected).
- Neither official source was moved into literature_matrix.csv or
  gap_verification_matrix.csv.

Tracking correction:
- round02_japanese_source_tracking.csv R02_NDL_068 was corrected (year NA -> 2014;
  doi NA -> 10.19024/jajls.17.1_36) with a note recording the OpenAlex source.

## F. Direct-overlap caution

None of the four academic candidates approaches the full provisional topic
combination (Chinese residents/nationals in Metropolitan Tokyo + Chinese-vs-non-
Chinese comparison + housing + transit/accessibility + services + disaster/risk
exposure + opportunity-risk typology or mismatch).

- R02_NDL_043 covers immigrants + housing in Japan (single module, Japan-wide,
  not Chinese-specific).
- R02_NDL_087 and R02_NDL_088 cover foreign-children education services
  (non-empirical background).
- R02_NDL_068 covers Brazilian residents' language support in Okayama (non-Tokyo,
  non-Chinese).

No item is coded as final A_direct_overlap, and none is coded
A_direct_overlap_candidate. No Chinese-vs-non-Chinese comparison, accessibility
integration, or opportunity-risk typology is present in the metadata. The two
official sources are context/background only. No gap claim is made; the gap is
neither confirmed nor refuted. Status remains: gap under verification.

## G. Next steps

- Manually translate / read the NDL candidates added to the matrices, starting
  with R02_NDL_043 (housing module).
- Manually check R02_NDL_OFF_002 (CLAIR) if it is used as official municipal
  multilingual / administrative-service context.
- Consider a targeted official-source search for Tokyo metropolitan
  municipalities, disaster prevention, multilingual services, housing support,
  and welfare/education/health access.
- Do not write the Introduction yet.
- Do not assert novelty yet.
