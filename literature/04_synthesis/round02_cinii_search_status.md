# Round 02 CiNii Metadata-Only Search Status

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (Japanese-source verification - CiNii metadata pass)
Search platform: CiNii Research OpenSearch (metadata only)

## A. Purpose

This note summarizes the first CiNii metadata-only search round for the
Tokyo-China opportunity-risk mismatch project. Its goal is to reduce the
English-language database bias of Round 01 by surveying Japanese-language and
Japan-based academic records via CiNii Research OpenSearch. It records what was
retrieved and how each item was provisionally triaged; it does not perform a
literature review.

## B. Evidence status

This is metadata discovery ONLY. It is:

- NOT a final literature review,
- NOT a full-text review (no PDFs were downloaded),
- NOT confirmation of the research gap.

Current status: gap under verification. No item is asserted as a confirmed
direct-overlap source, and no novelty claim is made. The CiNii application id
(CINII_APP_ID) was read only from the environment variable and was never
written to any output, report, or committed file.

## C. Search coverage

- Query groups attempted: 7 (QG-A through QG-G).
- Queries attempted: 21 (R02-Q01 through R02-Q21).
- Candidate records retrieved (post within-run dedup): 102.
- Records appended to round02_japanese_source_tracking.csv: 102.
- A_direct_overlap_candidate: 0.
- B_partial_overlap_candidate: 32.
- D_method_support_candidate: 2.
- E_background_candidate: 32.
- official_policy_context: 1.
- Held for translation/manual check: 35.
- Excluded as not relevant: 0.
- CiNii appid handling: read from CINII_APP_ID environment variable only; not
  printed, not written to files, not committed.

Per the protocol, no item is coded as final A_direct_overlap in a metadata-only
pass. A_direct_overlap_candidate is reserved for items whose metadata alone
suggests possible direct overlap; none reached that bar this round.

## D. Important candidates

The most relevant candidates by metadata (all Tokyo / Greater Tokyo plus
Chinese-resident signals; all require manual verification and translation):

- R02_CINII_001 | 2021 | B_partial_overlap_candidate
  公的住宅団地における高学歴技術職の中国籍住民の居住実態と地域との関わりに関する研究 : 首都圏2団地の住民インタビュー調査から
  Why it matters: directly couples Chinese-nationality residents with public
  housing estates in the Greater Tokyo area (housing module + target
  population). Closest single-study housing-module signal so far.

- R02_CINII_022 | 2020 | B_partial_overlap_candidate
  東京大都市圏における中国人ホワイトカラー層の住宅の購入動機と選好パターン
  Why it matters: Chinese white-collar residents' housing choice in the Tokyo
  metropolitan area; housing-module overlap, positions against Sun 2026
  location-choice scope.

- R02_CINII_018 | 2020 | B_partial_overlap_candidate
  西川口チャイナタウンの形成要因に関する研究 : 東京圏における中国人集住地域に着目して
  Why it matters: formation of a Chinese concentration area (Nishikawaguchi) in
  the Tokyo region; residential-concentration/segregation signal.

- R02_CINII_015 | year NA | B_partial_overlap_candidate
  東京圏における中国人集住地域における中国人人口
  Why it matters: Chinese population within Chinese concentration areas in the
  Tokyo region; concentration/distribution signal (metadata incomplete - year
  missing, verified_status partial).

- R02_CINII_019 | 2000 | B_partial_overlap_candidate
  昭和初期の東京とその周辺地域における中国人労働者の排除と集住地区の衰退
  Why it matters: historical Chinese concentration/exclusion in Tokyo and its
  periphery; background/comparator value, likely dated for the current frame.

None of the above integrates the full opportunity-risk mismatch combination
(housing + accessibility + services + disaster exposure + typology). They are
single- or partial-module signals and are positioned against Sun 2026, not
claimed as novel ground.

## E. Limitations

- CiNii metadata may be incomplete (missing year, DOI, or author fields);
  such records are marked verified_status = partial.
- Japanese titles and abstracts require translation and manual checking before
  any coding is treated as evidence; translation_needed = yes is set on the
  candidate rows.
- Full text was not downloaded; coding is based on titles and limited metadata
  fields only.
- Keyword triage produces geographic and population false positives (for
  example, a Tokyo-based publisher can flag a study area as Tokyo even when the
  case study is elsewhere); study_area and population_group must be confirmed
  manually.
- No Google Scholar scraping, no browser automation, and no paid APIs were
  used.
- Additional J-STAGE, NDL, institutional-repository, and official-source
  searches plus manual checks are still required before any gap claim.

## F. Next steps

- Manually verify the high-priority CiNii candidates (Section D first), then the
  remaining B_partial and held items.
- Decide which verified items should enter literature_matrix.csv and which
  belong in gap_verification_matrix.csv; route official statistics/policy items
  to official_source_registry.csv.
- Continue the Japanese-source search on J-STAGE and NDL (metadata only).
- Do not write the Introduction yet.
- Do not assert novelty yet. Status remains: gap under verification.
