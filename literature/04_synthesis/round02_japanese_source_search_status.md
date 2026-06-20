# Round 02 Japanese-Source Search Status

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (Japanese-language / CiNii / J-STAGE / official-source)

## A. Status

- Round 02 has been INITIALIZED.
- This task delivered a search setup and tracking structure only: a protocol,
  a Japanese-language query list, and two empty (header-only) tracking CSVs.
- It is NOT a completed review. No items have been verified or coded yet.

## B. Evidence and gap status

- No final gap claim is allowed. Status remains: gap under verification.
- The final research gap must not be asserted until it is supported by verified
  literature-matrix records and deep-reading notes, positioned against Sun 2026.
- Round 01 produced 0 confirmed A_direct_overlap items; this does not prove that
  no direct-overlap literature exists, especially in Japanese-language sources.

## C. Why Japanese-language and official sources are necessary

- Round 01 relied on English-facing APIs (OpenAlex, Crossref, Semantic Scholar),
  which under-represent Japanese-language academic work and Japanese official
  statistics and policy material.
- The target population (Chinese and foreign residents in Metropolitan Tokyo)
  and the relevant housing, accessibility, service, and disaster-exposure
  evidence are substantially documented in Japanese sources (CiNii, J-STAGE,
  NDL, e-Stat, ISA, MLIT, GSI, TMG, ward/city pages).
- Searching these sources reduces English-database bias before any gap decision.

## D. Optional feasibility test (metadata-only)

- A small metadata-only test was run against OpenAlex (a public API that permits
  automated access with a mailto), counts only, for a few English working
  translations of Round 02 queries. No PDFs were downloaded; no pages were
  scraped; Google Scholar was not queried.
- Result: the API responds (e.g. a broad "foreigners rental housing
  discrimination Japan" query returned a non-zero count), but narrow
  Tokyo-and-foreign-resident multi-term queries returned near-zero counts on the
  English index. This reinforces the rationale for Japanese-source search rather
  than substituting for it.
- CiNii Research API was NOT used: it requires CINII_APP_ID, which is absent in
  this environment. CiNii is therefore recorded as skipped (API) and handled by
  manual search. J-STAGE and NDL were not API-queried this round.
- The test was a feasibility check only; no results were entered into the
  tracking CSVs.

## E. Deliverables created this round

- literature/03_notes/round02_japanese_source_search_protocol.md
- literature/03_notes/round02_japanese_search_queries.md (21 queries, 7 groups)
- literature/02_matrices/round02_japanese_source_tracking.csv (header only)
- literature/02_matrices/official_source_registry.csv (header only)
- literature/04_synthesis/round02_japanese_source_search_status.md (this note)

## F. Next task

- Run the targeted Japanese-source search using the query list, via CiNii
  (manual), J-STAGE, NDL, and the official portals (e-Stat, ISA, MLIT, GSI, TMG,
  ward/city pages).
- Populate round02_japanese_source_tracking.csv and official_source_registry.csv,
  separating peer-reviewed academic records from official data/policy sources.
- Bibliographically verify academic records before any entry into
  literature_matrix.csv or gap_verification_matrix.csv.
- Do NOT begin manuscript writing. Do NOT assert novelty or confirm the gap.
