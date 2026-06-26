# Round 02 Japanese-Language and Official-Source Search Protocol

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Round: 02 (Japanese-language / CiNii / J-STAGE / official-source setup)

## A. Purpose

Round 02 searches Japanese-language academic and official sources to reduce
English-language database bias. Round 01 used English-facing APIs (OpenAlex,
Crossref, Semantic Scholar) and produced no confirmed A_direct_overlap item.
Because the provisional topic concerns Chinese and foreign residents in
Metropolitan Tokyo, a large share of the relevant literature, statistics, and
policy material is likely published in Japanese or by Japanese institutions and
is under-represented in English-facing databases. Round 02 corrects for that
gap before any final topic decision.

## B. Evidence status

- Round 02 is still gap verification, NOT final gap confirmation.
- The final research gap must not be asserted until it is supported by verified
  literature-matrix records and deep-reading notes.
- Current status: gap under verification.
- This task is a search setup (protocol, query list, tracking templates). It is
  not a completed review and does not populate findings.
- 0 confirmed A_direct_overlap items so far does NOT prove that no direct-overlap
  literature exists.

## C. Search source categories

Academic and bibliographic:
- CiNii Research (NII) - Japanese academic articles, theses, books.
- J-STAGE - Japanese society and journal full-text platform (metadata use only).
- NDL Search / National Diet Library - books, reports, government publications.
- Japanese university institutional repositories (e.g. via JAIRO Cloud / IRDB).
- Google Scholar - MANUAL browser search by a human only; no scraping.

Official statistics, policy, and spatial data:
- Tokyo Metropolitan Government (TMG) portals and statistics.
- e-Stat (Japanese government statistics portal).
- Ministry of Justice / Immigration Services Agency (zairyu / foreign-resident
  statistics).
- MLIT (Ministry of Land, Infrastructure, Transport and Tourism) - housing,
  transit, land use.
- GSI (Geospatial Information Authority of Japan) - base maps and spatial data.
- Ward / city government pages for Tokyo-area municipalities.
- Disaster-prevention and multilingual-support official pages.
- Housing or rental-market official or academic sources.

API and access note:
- If an official API requires an application ID or key that is not available in
  the environment, skip that API and record it as skipped (do not store keys).
- CiNii Research API requires CINII_APP_ID, which is not present in this
  environment; CiNii is therefore handled by manual search this round.
- If a source does not clearly permit automated access, do not scrape it.
  Create a manual search checklist entry instead.

## D. Source handling rules

- Academic records (peer-reviewed articles, theses, book chapters) may be
  entered into literature_matrix.csv AFTER bibliographic verification
  (DOI / publisher / CiNii / NDL record), using the same caution as Round 01.
- Official data or policy sources (statistics, ministry/municipal pages,
  hazard maps) are documented SEPARATELY in official_source_registry.csv and
  must NOT be confused with peer-reviewed literature.
- PDFs are NOT downloaded and NOT committed to this public repository. Only
  bibliographic metadata and stable URLs are recorded.
- Copyrighted full text is never committed.
- Japanese titles should be recorded in Japanese when available; ASCII
  transliteration or an English working note may be used in repo notes where an
  encoding risk exists. Files containing Japanese are written as UTF-8 with LF.
- Any translation is marked as a working translation (not an official title).
- No Google Scholar scraping, no browser automation, no paid APIs.

## E. Search domains

1. Chinese residents in Tokyo / Japan.
2. Chinese nationals in Tokyo / Japan.
3. Foreign residents (zairyu gaikokujin) in Tokyo / Japan.
4. Residential concentration / segregation (ethnic residential differentiation).
5. Rental housing discrimination.
6. Public housing or rental constraints / access.
7. Disaster vulnerability / evacuation / earthquake / flood exposure.
8. Multilingual disaster support.
9. Municipal foreign-resident support services.
10. Healthcare, education, childcare, and administrative service access.
11. Rail / transit accessibility.
12. Arrival infrastructure / settlement support.
13. Opportunity structure / urban risk / vulnerability.

## F. Decision logic (overlap coding for Japanese-source items)

Code each item with exactly one category:

- A_direct_overlap - integrates Chinese/foreign residents in Metropolitan Tokyo
  with the opportunity-risk mismatch combination (housing + accessibility +
  services + disaster exposure + typology). Triggers careful manual review.
- B_partial_overlap - covers one or two modules in a Tokyo/Japan foreign-resident
  context but is not the integrated combination.
- C_theoretical_support - conceptual framing (opportunity structure, spatial
  assimilation, vulnerability theory) without direct Tokyo-China data.
- D_method_support - GIS / spatial statistics / accessibility methods usable for
  the analysis, regardless of population.
- E_background_only - context, dated, or non-empirical commentary.
- official_data_source - statistics or spatial datasets (e-Stat, ISA, MLIT,
  GSI, TMG); goes to official_source_registry.csv.
- official_policy_context - ministry/municipal policy or support-program pages;
  goes to official_source_registry.csv.
- exclude_not_relevant - out of scope or geographic/topic false positive.
- hold_for_translation_or_manual_check - relevance plausible but cannot be coded
  until translated or manually verified.

Boundary condition (Sun 2026, Cities): Sun 2026 already covers Tokyo immigrant
location choice, co-ethnic networks, spatial assimilation, Chinese / Vietnamese
/ Filipino / Brazilian immigrants, Tokyo-area municipalities, and dynamic
spatial Durbin modeling. Round 02 items overlapping that scope are positioned
against Sun 2026 and are NOT claimed as novel ground.

## G. Minimum evidence before final topic decision

- The Japanese-language and official-source search (this Round 02 plus its
  follow-up population task) MUST be completed before any final gap claim.
- A final gap statement additionally requires: verified literature-matrix
  records, deep-reading notes, and explicit positioning against Sun 2026.
- Until then the status remains: gap under verification. Do not write the
  Introduction and do not assert novelty.
