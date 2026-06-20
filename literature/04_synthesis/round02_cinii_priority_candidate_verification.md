# Round 02 CiNii Priority Candidate Verification

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (Japanese-source verification - CiNii priority candidate check)

## A. Purpose

This note verifies the five high-priority CiNii candidates identified from the
Round 02 CiNii metadata search (status note:
round02_cinii_search_status.md), and records a matrix-entry decision for each:

- R02_CINII_001, R02_CINII_022, R02_CINII_018, R02_CINII_015, R02_CINII_019.

Verification used public metadata only: the locally saved CiNii records, CiNii
stable URLs, and the Crossref DOI resolver for the two candidates that carry a
DOI. No PDFs were downloaded, no Google Scholar scraping, no browser
automation, no paid APIs, and no credentials were used or written.

## B. Evidence status

- This is metadata/source-level verification only.
- It is NOT a full-text review; no full text was read.
- It does NOT confirm the research gap.
- It does NOT prove the absence of direct-overlap literature.
- Japanese-language translation and full-text reading are still required before
  any candidate is treated as confirmed evidence.
- No item is coded as final A_direct_overlap. Status: gap under verification.

## C. Candidate verification table

| source_id | original_title | english_working_title | year | verification_status | likely_module | matrix_disposition | overlap_category | reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R02_CINII_001 | 公的住宅団地における高学歴技術職の中国籍住民の居住実態と地域との関わりに関する研究 | Living conditions and community involvement of highly-educated Chinese-nationality residents in public housing estates (working) | 2021 | verified_by_cinii_metadata | housing + community involvement | add_to_both_matrices | B_partial_overlap_candidate | Chinese-nationality residents in Greater Tokyo public housing; housing and settlement modules, qualitative single-combination | translate and read full text; confirm study area and service/community dimensions |
| R02_CINII_022 | 東京大都市圏における中国人ホワイトカラー層の住宅の購入動機と選好パターン | The Residence Purchasing Motives, Preference and Patterns of Chinese White Collar Residents in the Tokyo Metropolitan Area (official, Crossref) | 2020 | verified_by_doi_and_metadata | housing | add_to_both_matrices | B_partial_overlap_candidate | Chinese white-collar housing choice in metropolitan Tokyo; strong housing-module, qualitative (n=22) | read full text; extract housing-choice determinants |
| R02_CINII_018 | 西川口チャイナタウンの形成要因に関する研究 : 東京圏における中国人集住地域に着目して | A study on the formation factors of Nishikawaguchi Chinatown (working) | 2020 | verified_by_cinii_metadata | residential concentration / ethnic enclave | add_to_both_matrices | B_partial_overlap_candidate | Chinese concentration-area formation in greater Tokyo; study area is Kawaguchi (Saitama) within greater Tokyo | translate and read; confirm method and study-area boundary vs Metropolitan Tokyo |
| R02_CINII_019 | 昭和初期の東京とその周辺地域における中国人労働者の排除と集住地区の衰退 | The Exclusion of Chinese Workers and the Decline of Their Residential Segregation during the Early Showa Era in and around Tokyo (official, Crossref) | 2000 | verified_by_doi_and_metadata | residential concentration (historical) | add_to_literature_matrix_only | B_partial_overlap_candidate | Historical (1920s-1930s) exclusion/concentration in Tokyo; useful background, weak for contemporary gap verification | retain as historical background; no full-text priority |
| R02_CINII_015 | 東京圏における中国人集住地域における中国人人口 | Chinese population in Chinese concentration areas in the Tokyo region (working) | NA | partially_verified | population/distribution data | keep_hold_for_translation_or_manual_check | hold_for_translation_or_manual_check | On-topic title but Dataset record with no author/year/publisher and an unrelated linked identifier; metadata insufficient | manual check of CiNii dataset record; if census aggregation, route to official_source_registry.csv |

## D. Matrix additions

Added to literature_matrix.csv (4):

- R02_CINII_001 (Wang and Fujii 2021) - verified = partial
- R02_CINII_022 (Zhang 2020) - verified = yes
- R02_CINII_018 (Takamatsu 2020) - verified = partial
- R02_CINII_019 (Abe 2000) - verified = yes (historical background)

Added to gap_verification_matrix.csv (3):

- R02_CINII_001 (Wang and Fujii 2021)
- R02_CINII_022 (Zhang 2020)
- R02_CINII_018 (Takamatsu 2020)

All three gap-matrix items are coded overlap_with_our_topic = B_partial_overlap.
R02_CINII_019 was kept out of the gap matrix because it is historical and weak
for verifying a contemporary opportunity-risk gap; it remains in
literature_matrix.csv as background.

## E. Candidates held or excluded

Held for translation/manual check (1):

- R02_CINII_015 - CiNii Dataset record titled "Chinese population in Chinese
  concentration areas in the Tokyo region". No author, year, or publisher in
  the metadata, and the linked identifier points to an unrelated foreign
  repository. The title is on-topic, but the record cannot be coded as
  literature from metadata alone. If a manual check confirms it is an aggregated
  census/public-statistics dataset, it should be routed to
  official_source_registry.csv rather than the literature matrices.

Excluded (0): none.

## F. Direct-overlap caution

None of the five candidates approaches the full provisional topic combination
(Chinese residents in Metropolitan Tokyo PLUS Chinese-vs-non-Chinese comparison
PLUS housing PLUS transit/accessibility PLUS services PLUS disaster/risk
exposure PLUS an opportunity-risk typology or mismatch). Each verified item is a
single- or partial-module study:

- R02_CINII_022 and R02_CINII_001 cover the housing module for Chinese residents
  in metropolitan/greater Tokyo (R02_CINII_001 also touches community
  involvement), but neither integrates accessibility, services, disaster
  exposure, or an opportunity-risk typology, and neither uses a Chinese-vs-
  non-Chinese comparison.
- R02_CINII_018 covers residential concentration (ethnic enclave formation) in
  greater Tokyo (Kawaguchi, Saitama), again single-module.
- R02_CINII_019 is historical and does not address the contemporary
  opportunity-risk combination.

No A_direct_overlap is asserted. These items are positioned against Sun 2026 and
do not, individually or together, establish or refute the integrated gap.
Status remains: gap under verification.

## G. Next steps

- Manually translate and read the held candidate (R02_CINII_015) and the three
  gap-matrix items before treating any coding as confirmed evidence.
- Continue J-STAGE metadata-only search.
- Then continue NDL metadata-only search.
- Do not write the Introduction yet.
- Do not assert novelty yet.
