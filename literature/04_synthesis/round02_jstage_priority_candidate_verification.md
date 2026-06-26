# Round 02 J-STAGE Priority-Candidate Verification

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (Japanese-source verification - J-STAGE priority candidates)

## A. Purpose

This note verifies the four priority J-STAGE candidates identified from the
Round 02 J-STAGE metadata-only search (R02_JSTAGE_002, R02_JSTAGE_007,
R02_JSTAGE_011, R02_JSTAGE_021). Its main task is to determine whether
R02_JSTAGE_002 and the existing CiNii record R02_CINII_001 refer to the same
study and, if so, whether the J-STAGE DOI should supplement the existing record
rather than create a duplicate matrix row. Verification used public metadata
only (J-STAGE stable URLs and locally saved J-STAGE metadata, the DOI resolver,
and the Crossref / OpenAlex APIs). No PDFs were downloaded, no J-STAGE HTML
pages were scraped, no Google Scholar was scraped, no browser automation was
used, and no credentials were stored.

## B. Evidence status

- This is metadata / source-level verification only.
- It is NOT a full-text review (no PDFs read).
- It does NOT confirm the research gap.
- It does NOT prove the absence of direct-overlap literature.
- Japanese-language translation and full-text reading may still be required
  before any item is treated as confirmed evidence.
- Current status: gap under verification.

## C. Candidate verification table

| source_id | original_title | english_working_title | year | doi | verification_status | likely_module | matrix_disposition | overlap_category | reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R02_JSTAGE_002 | 公的住宅団地における高学歴技術職の中国籍住民の居住実態と地域との関わりに関する研究―首都圏2団地の住民インタビュー調査から― | Living Conditions and Community Involvement of Highly-Educated, Technically-Skilled Chinese in Public Housing: A Survey of Residents in Two Public Housing Estates in the Tokyo Metropolitan Area | 2021 | 10.24528/lifology.40.0_54 | verified_by_doi_and_jstage_metadata; duplicate_or_complementary_record | housing / community (settlement) | supplement_existing_record (no new row) | B_partial_overlap_candidate | Same study as R02_CINII_001 (identical title/subtitle, same year, same first author Wang, same journal/society); J-STAGE supplies the DOI the CiNii record lacked. | Translate/read full text; treat R02_CINII_001 as the canonical record now carrying the DOI. |
| R02_JSTAGE_007 | 1920年代の東京府における中国人労働者の就業構造と居住分化 | The Occupational Structure and Residential Differentiation of Chinese Workers in Tokyo Prefecture during the 1920s | 1999 | 10.4200/jjhg1948.51.23 | verified_by_doi_and_jstage_metadata (Crossref-confirmed) | housing / residential differentiation (historical) | add_to_literature_matrix_only | B_partial_overlap_candidate | Tokyo Prefecture, Chinese-worker residential differentiation, but historical (1920s) and single-module; weak for contemporary gap verification. Distinct paper from R02_CINII_019 (Abe 2000). | Optional translation; keep as historical background/comparator. |
| R02_JSTAGE_011 | 大阪市中央区「心斎橋地区」の中国系ニューカマーにみる分散居住とエスニック・コミュニティ | Dispersed Residence and Ethnic Communities Among Chinese Newcomers in the "Shinsaibashi Area" of Chuo Ward, Osaka City | 2026 | 10.4200/jjhg.78.01_023 | verified_by_doi_and_jstage_metadata (Crossref-confirmed) | residence / ethnic community | add_to_literature_matrix_only | B_partial_overlap_candidate | Chinese-newcomer dispersed residence and ethnic community, but the study area is Osaka, not Metropolitan Tokyo; comparator only. | Keep as a non-Tokyo thematic comparator; do not use for Tokyo gap verification. |
| R02_JSTAGE_021 | 非集住地域における在日中国人ニューカマーのホーム意識 | "Homes" of Chinese Newcomers in a Less Concentrated Area of Chinese Residents | 2016 | 10.20790/easoc.2016.8_92 | verified_by_doi_and_jstage_metadata (source); coding held | belonging / home consciousness (qualitative) | keep_hold_for_translation_or_manual_check | B_partial_overlap_candidate | Source bibliographically verified (DOI resolves to J-STAGE), but the study area is unclear from metadata ("non-concentrated area", Tokyo not confirmed) and the module is a weak qualitative "home consciousness" theme. | Translate to confirm study area and content, then decide matrix placement. |

Verification routes (public metadata only):
- R02_JSTAGE_002: J-STAGE metadata + DOI resolver (doi.org 302 -> J-STAGE
  lifology/40/0/40_54). Crossref/OpenAlex have no record (JaLC-registered DOI).
- R02_JSTAGE_007: Crossref confirms title, author (Yasuhisa Abe), journal
  (Japanese Journal of Human Geography), 1999, vol. 51, pp. 23-48.
- R02_JSTAGE_011: Crossref confirms title, author (Zihao Wang), journal
  (Japanese Journal of Human Geography), 2026, vol. 78, pp. 23-43; study area
  Osaka.
- R02_JSTAGE_021: J-STAGE metadata + DOI resolver (doi.org 302 -> J-STAGE
  easoc/2016/8/2016_92). Crossref/OpenAlex have no record (JaLC-registered DOI).

## D. R02_JSTAGE_002 and R02_CINII_001 equivalence check

Decision: A. supplement_existing_record. They appear to be the SAME study.

Evidence:
- Title: identical main title and subtitle; the only difference is the subtitle
  separator (J-STAGE uses an em-dash, CiNii uses a colon). Title:
  "公的住宅団地における高学歴技術職の中国籍住民の居住実態と地域との関わりに関する研究"
  with subtitle "首都圏2団地の住民インタビュー調査から".
- Year: both 2021.
- Author: same first author 王 爽 (Wang Shuang). CiNii lists co-author
  藤井 さやか (Fujii Sayaka); the J-STAGE WebAPI metadata captured the first
  author only - a metadata-capture difference, not a different study.
- Source: CiNii records the publisher as the Japan Society of Lifology
  (日本生活学会); J-STAGE places the article in that society's journal
  生活学論叢 (Journal of Lifology), vol. 40, p. 54. Consistent.
- DOI: J-STAGE supplies 10.24528/lifology.40.0_54, which resolves via doi.org
  (302) to the J-STAGE article page. The CiNii record had DOI = NA.

Action taken:
- The existing R02_CINII_001 rows in literature_matrix.csv and
  gap_verification_matrix.csv were SUPPLEMENTED: the DOI
  (10.24528/lifology.40.0_54) and the J-STAGE URL were added (literature_matrix
  doi field + notes; gap_verification_matrix verified_source + notes), and the
  notes record that R02_JSTAGE_002 is the same study and supplies the DOI. The
  literature_matrix "verified" flag was raised from "partial" to "yes" because
  the DOI now resolves.
- NO duplicate matrix row was created for R02_JSTAGE_002. The tracking-CSV row
  for R02_JSTAGE_002 already flags the complementary relationship in its notes.

## E. Matrix additions or updates

- Added to literature_matrix.csv: 2
  - R02_JSTAGE_007 (historical Tokyo Chinese-worker residential differentiation;
    background/comparator).
  - R02_JSTAGE_011 (Osaka Chinese-newcomer dispersed residence; non-Tokyo
    comparator).
- Added to gap_verification_matrix.csv: 0.
- Used to supplement existing R02_CINII_001: 1 (R02_JSTAGE_002), in both
  literature_matrix.csv and gap_verification_matrix.csv.
- Held for translation/manual check: 1 (R02_JSTAGE_021).
- Excluded as duplicate/complementary (no new matrix row): 1 (R02_JSTAGE_002,
  folded into R02_CINII_001).

## F. Direct-overlap caution

None of the four candidates approaches the full provisional topic combination
(Chinese residents/nationals in Metropolitan Tokyo + Chinese-vs-non-Chinese
comparison + housing + transit/accessibility + services + disaster/risk
exposure + opportunity-risk typology or mismatch).

- R02_JSTAGE_002 / R02_CINII_001 covers Chinese residents in Greater Tokyo and a
  housing/community module only - a single- to partial-module item, not the
  integrated combination.
- R02_JSTAGE_007 is historical (1920s) and single-module.
- R02_JSTAGE_011 is Osaka, not Tokyo.
- R02_JSTAGE_021 is a qualitative belonging study with an unclear study area.

No item is coded as final A_direct_overlap, and none is coded
A_direct_overlap_candidate. No Chinese-vs-non-Chinese comparison, transit
accessibility integration, or opportunity-risk typology is present in the
metadata. No gap claim is made; the gap is neither confirmed nor refuted.
Status remains: gap under verification.

## G. Next steps

- Manually translate / read R02_CINII_001 (= R02_JSTAGE_002) if it is to be used
  as housing-module evidence.
- Manually check the held item R02_JSTAGE_021 (confirm study area and content).
- Then proceed to the NDL metadata-only search.
- Do not write the Introduction yet.
- Do not assert novelty yet.
