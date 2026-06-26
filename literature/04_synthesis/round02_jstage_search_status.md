# Round 02 J-STAGE Metadata-Only Search Status

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (Japanese-source verification - J-STAGE metadata pass)
Search platform: J-STAGE WebAPI (service=3 article search, text parameter; metadata only)

## A. Purpose

This note summarizes the first J-STAGE metadata-only search round for the
Tokyo-China opportunity-risk mismatch project. It follows the completed Round 02
CiNii metadata pass and continues the effort to reduce the English-language
database bias of Round 01 by surveying Japanese-language and Japan-based
academic records. It records what was retrieved via the J-STAGE WebAPI and how
each item was provisionally triaged. It does not perform a literature review.

## B. Evidence status

This is metadata discovery ONLY. It is:

- NOT a final literature review,
- NOT a full-text review (no PDFs were downloaded),
- NOT confirmation of the research gap.

Current status: gap under verification. No item is asserted as a confirmed
direct-overlap source, and no novelty claim is made. Only the public J-STAGE
WebAPI metadata endpoint was used; no API key or credential was required,
stored, printed, or committed. No J-STAGE HTML page was scraped and no browser
automation was used.

## C. Search coverage

- Query groups attempted: 7 (QG-A through QG-G).
- Queries attempted: 21 (R02-Q01 through R02-Q21), via the J-STAGE WebAPI
  article-search "text" parameter (the closest metadata-supported search mode;
  see Section E).
- Candidate records retrieved (post within-run dedup): 294.
- Records appended to round02_japanese_source_tracking.csv: 278
  (16 within/cross-source duplicates were dropped; see below).
- A_direct_overlap_candidate: 0.
- B_partial_overlap_candidate: 30 retrieved (25 appended).
- D_method_support_candidate: 9 appended.
- E_background_candidate: 68 appended.
- official_policy_context: 9 appended.
- Held for translation/manual check: 175 retrieved (167 appended).
- Excluded as not relevant: 0 (cautious triage holds rather than excludes).
- Duplicate or overlapping with prior CiNii records: 11. Of these, 10 were
  auto-detected (matching CiNii title/DOI) and dropped as duplicates because the
  J-STAGE record added no stronger DOI or publisher metadata; 1 (R02_JSTAGE_002)
  was appended as a complement because it carries a DOI that the matching CiNii
  record (R02_CINII_001) lacked, and was flagged in its notes for manual
  confirmation of the duplicate relationship.

Per the protocol, no item is coded as final A_direct_overlap in a metadata-only
pass. A_direct_overlap_candidate is reserved for items whose metadata alone
suggests possible direct overlap; none reached that bar this round.

## D. Important candidates

Only two appended J-STAGE candidates couple Chinese residents with a Tokyo /
Greater Tokyo study area in the metadata (all require manual verification and
translation):

- R02_JSTAGE_002 | 2021 | B_partial_overlap_candidate | DOI 10.24528/lifology.40.0_54
  "Living Conditions and Community Involvement of Highly-Educated,
  Technically-Skilled Chinese in Public Housing: A Survey of Residents in Two
  Public Housing Estates in the Tokyo Metropolitan Area" (J-STAGE English title).
  Why it matters: directly couples Chinese-nationality residents with public
  housing estates in the Greater Tokyo area (housing module + target
  population). This appears to be the SAME study as the CiNii candidate
  R02_CINII_001; the J-STAGE record complements it by supplying a DOI that the
  CiNii record lacked (CiNii DOI was NA). The duplicate/complementary
  relationship is flagged in the tracking notes and must be confirmed manually.

- R02_JSTAGE_007 | 1999 | B_partial_overlap_candidate | DOI 10.4200/jjhg1948.51.23
  "The Occupational Structure and Residential Differentiation of Chinese Workers
  in Tokyo Prefecture during the 1920s" (J-STAGE English title).
  Why it matters: historical Chinese-worker residential differentiation in
  Tokyo Prefecture; concentration/segregation signal with background/comparator
  value. Likely dated for the current frame; complements the historical CiNii
  items (e.g. R02_CINII_019) rather than the contemporary analysis.

Two further Chinese-flagged B_partial candidates touch newcomer dispersal /
ethnic community themes (R02_JSTAGE_011, 2026; R02_JSTAGE_021, 2016) but their
study area is not clearly Tokyo from metadata alone and they require manual
checking.

None of the above integrates the full opportunity-risk mismatch combination
(housing + accessibility + services + disaster exposure + typology). They are
single- or partial-module signals and are positioned against Sun 2026, not
claimed as novel ground.

## E. Limitations

- The J-STAGE WebAPI has no single space-separated AND search field equivalent
  to the CiNii OpenSearch "q" parameter. The closest metadata-supported mode
  (the WebAPI article-search "text" parameter) was used. This indexed search has
  high recall and returns many partial/contextual matches, which is the main
  reason a large share of records (175 of 294) were held for
  translation/manual check rather than coded. Recall and ranking therefore
  differ from the CiNii pass; this is recorded as a limitation, not worked
  around by scraping.
- J-STAGE metadata may be incomplete (missing year, DOI, or author fields);
  such records are marked verified_status = partial.
- Japanese titles and abstracts require translation and manual checking before
  any coding is treated as evidence. Where J-STAGE supplied an official English
  title it was stored in english_working_title; this is the publisher's title,
  not a working translation, but the record still requires manual verification.
- Full text was not downloaded; coding is based on titles and limited metadata
  fields only.
- Keyword triage produces geographic and population false positives; study_area
  and population_group must be confirmed manually.
- No Google Scholar scraping, no J-STAGE HTML scraping, no browser automation,
  and no paid APIs were used.
- NDL metadata search, institutional-repository search, and official-source
  registry checks are still required before any gap claim.

## F. Next steps

- Manually verify the high-priority J-STAGE candidates (Section D first),
  starting with confirming the R02_JSTAGE_002 / R02_CINII_001 relationship and
  whether the DOI-bearing J-STAGE record should supersede the CiNii row.
- Decide which verified items should enter literature_matrix.csv and which
  belong in gap_verification_matrix.csv; route official statistics/policy items
  to official_source_registry.csv.
- Continue the NDL metadata-only search.
- Continue the official-source registry search.
- Do not write the Introduction yet.
- Do not assert novelty yet. Status remains: gap under verification.
