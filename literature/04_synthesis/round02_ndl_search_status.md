# Round 02 NDL Metadata-Only Search Status

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (Japanese-source verification - NDL metadata pass)
Search platform: NDL Search OpenSearch API (any free-word; metadata only)
Endpoint used: https://ndlsearch.ndl.go.jp/api/opensearch

## A. Purpose

This note summarizes the first NDL Search (National Diet Library) metadata-only
search round for the Tokyo-China opportunity-risk mismatch project. It follows
the completed Round 02 CiNii and J-STAGE metadata passes and extends the
Japanese-source survey to books, reports, theses, institutional records, and
official/public materials indexed by NDL Search. It records what was retrieved
via the NDL OpenSearch API and how each item was provisionally triaged. It does
not perform a literature review.

## B. Evidence status

This is metadata discovery ONLY. It is:

- NOT a final literature review,
- NOT a full-text review (no PDFs were downloaded),
- NOT confirmation of the research gap.

Current status: gap under verification. No item is asserted as a confirmed
direct-overlap source, and no novelty claim is made. Only the public NDL Search
OpenSearch metadata endpoint was used; no API key or credential was required,
stored, printed, or committed. No NDL HTML page was scraped and no browser
automation was used.

## C. Search coverage

- Query groups attempted: 7 (QG-A through QG-G).
- Queries attempted: 21 (R02-Q01 through R02-Q21), via the NDL OpenSearch
  free-word "any" parameter (the closest metadata-supported search mode; see
  Section F).
- Candidate records retrieved (post within-run dedup): 123.
- Academic rows appended to round02_japanese_source_tracking.csv: 106.
- Official rows appended to official_source_registry.csv: 2.
- A_direct_overlap_candidate: 0.
- B_partial_overlap_candidate: 9 retrieved (4 appended; 5 were duplicates of
  prior CiNii/J-STAGE records and dropped).
- E_background_candidate: 15 appended.
- Held for translation/manual check: 87 retrieved (85 appended).
- Excluded as not relevant: 0 (cautious triage holds rather than excludes).
- Duplicate or overlapping with prior CiNii/J-STAGE records: 15 (all dropped as
  duplicates; none provided stronger metadata, so none was added as a
  complement).
- Official data/policy sources identified (by triage category): 6. Of these, 2
  records with a clear official/quasi-official publisher were routed to
  official_source_registry.csv; 2 are academic-style records on foreign-resident
  services coded official_policy_context (publisher was not an official body) and
  kept in the tracking CSV pending manual routing; 2 duplicated prior CiNii/
  J-STAGE records and were dropped.

Per the protocol, no item is coded as final A_direct_overlap in a metadata-only
pass. A_direct_overlap_candidate is reserved for items whose metadata alone
suggests possible direct overlap; none reached that bar this round.

## D. Important candidates

The most relevant academic candidates by metadata (all require manual
verification and translation; none is Chinese-specific to Metropolitan Tokyo):

- R02_NDL_043 | 2026 | B_partial_overlap_candidate
  「移民」の住む場所 : 日本の住宅市場における居住格差の実証分析
  (working gloss: "Where Migrants Live: an empirical analysis of residential
  disparity in Japan's housing market")
  Why it matters: recent empirical housing-market / residential-disparity study
  of migrants in Japan; supports the housing module. Japan-wide and not
  Chinese-specific; complements the housing-discrimination comparators rather
  than the Tokyo-China focus.

- R02_NDL_087 | 2006 | B_partial_overlap_candidate
  外国人児童生徒教育フォーラム : 報告書
  (working gloss: "Forum on the Education of Foreign Children and Students:
  report")
  Why it matters: service/education-access material for foreign residents with a
  Tokyo signal; background for the service-access module.

- R02_NDL_088 | 2006 | B_partial_overlap_candidate
  外国人児童生徒の就学前教育を考える
  (working gloss: "Considering Pre-school Education for Foreign Children and
  Students")
  Why it matters: childcare/pre-school service-access angle for foreign
  residents; background for the service-access module.

- R02_NDL_068 | year NA | B_partial_overlap_candidate
  岡山県総社市に暮らすブラジル人住民の言語生活 : 外国人住民の日本語学習支援を考える
  Why it matters: foreign-resident language-support/services case study, but in
  Soja City, Okayama (not Tokyo); comparator/background only.

None of the above integrates the full opportunity-risk mismatch combination
(housing + accessibility + services + disaster exposure + typology). They are
single- or partial-module signals and are positioned against Sun 2026, not
claimed as novel ground. Several strong Chinese-in-Tokyo titles surfaced by NDL
(e.g. the Wang and Fujii public-housing study and the Nishikawaguchi Chinatown
study) duplicated existing CiNii/J-STAGE records and were dropped, not re-added.

## E. Important official sources

- R02_NDL_OFF_002 | 自治体国際化協会 (CLAIR) | 自治体国際化フォーラム | 2005 |
  domain: multilingual / municipal international support
  Why it matters: a quasi-official local-government international-relations body
  publication; relevant to the multilingual/administrative service-access
  context for foreign residents. Suitability and licensing require manual check.

- R02_NDL_OFF_001 | institution NA | 訓令・通達・回答(5273) ... 中国人 ... | year NA |
  domain: administrative/legal directive
  Why it matters: an administrative/legal directive referencing Chinese
  residents in Japan; weak topical relevance, low priority; kept as an
  official-context candidate pending manual check.

## F. Limitations

- NDL OpenSearch has no single space-separated AND search field equivalent to
  the CiNii OpenSearch "q" parameter. The free-word "any" parameter was used as
  the closest metadata-supported mode; recall and ranking therefore differ from
  the CiNii and J-STAGE passes. This is recorded as a limitation, not worked
  around by scraping.
- NDL metadata may be incomplete (missing year, author, or publisher fields);
  such records are marked verified_status = partial.
- Title/abstract translation requires manual checking before any coding is
  treated as evidence.
- Full text was not downloaded; coding is based on titles and limited metadata.
- Official-source detection is heuristic (publisher/institution and
  document-type markers, with academic/commercial publishers excluded); the
  official/academic split and the suitability and licensing of official sources
  still require manual checking.
- No Google Scholar scraping and no NDL HTML scraping were performed.

## G. Next steps

- Verify the high-priority NDL candidates manually (Section D first), then the
  remaining B_partial and held items.
- Verify the high-priority official sources manually (Section E), including
  their access and licensing terms.
- Decide which academic items should enter literature_matrix.csv and which
  belong in gap_verification_matrix.csv.
- Decide which official items should support the later data-source registry or
  the analysis design.
- Continue official-source targeted search where needed.
- Do not write the Introduction yet.
- Do not assert novelty yet. Status remains: gap under verification.
