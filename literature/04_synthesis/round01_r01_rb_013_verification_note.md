# Round 01 R01_RB_013 Verification Note

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Candidate: R01_RB_013 (discovery id: round01_api-0156)

## A. Purpose

This note verifies the previously held Round 01 B candidate R01_RB_013, which
the remaining-B-candidate matrix update (round01_remaining_b_matrix_update.md)
held for manual check because its metadata title did not state the study area
(Japan/Tokyo). This task verifies only this single candidate and decides its
matrix disposition. It does not start a new broad literature search.

## B. Bibliographic verification

- Title (verified, full): Disentangling transaction-stage and management-stage
  discrimination in the rental housing market: evidence from a correspondence
  experiment in Tokyo
- Author-year: Sugasawa and Harano 2026 (Takeru Sugasawa; Kei Harano)
- Publication year: 2026
- Source / venue: Journal of Housing Economics
- Document type: journal article
- DOI: 10.1016/j.jhe.2026.102134
- Stable URL: https://doi.org/10.1016/j.jhe.2026.102134
- Publisher landing page: https://linkinghub.elsevier.com/retrieve/pii/S105113772600015X
- Verified source type: peer-reviewed journal article
- verification_status: verified_by_doi_and_metadata

Verification method (public metadata only):
- DOI resolver: resolves.
- Crossref: matched by DOI; returned the full title that includes the study
  area phrase "evidence from a correspondence experiment in Tokyo", confirming
  authors (Sugasawa; Harano), year (2026), and venue (Journal of Housing
  Economics).
- OpenAlex: matched by DOI; same title, authors, year, venue, type = article;
  topic concepts include rental housing, property management, landlord, and
  ethnic discrimination.
- Semantic Scholar: matched in the prior automated run.

No PDFs were downloaded, no paid APIs were used, no credentials were stored,
and no raw API output files were modified. The hold reason (unknown geography)
is now resolved: the published title states the study is a correspondence
experiment in Tokyo.

## C. Scope and overlap assessment

What the item covers, relative to the provisional Tokyo-China topic:
- Housing: yes (rental housing discrimination; transaction-stage vs
  management-stage).
- Metropolitan Tokyo / Tokyo: yes (correspondence experiment in Tokyo).
- Japan more broadly: yes (Japanese rental market).
- Foreign / ethnic-minority rental applicants: partial (OpenAlex concept
  "ethnic discrimination" and the companion 23-wards study by the same authors
  indicate a foreigner/ethnic-minority discrimination focus; the abstract was
  not available from metadata, so the exact target group is to be confirmed in
  full text).
- GIS / spatial statistics / public spatial data: no (audit/correspondence
  experiment design, not a spatial analysis).

What the item does not cover:
- Chinese residents or Chinese nationals: unclear (not identified as a
  Chinese-specific sample from metadata).
- Chinese vs non-Chinese comparison: no.
- Transit / accessibility: no.
- Service accessibility: no.
- Disaster risk or vulnerability: no.
- Arrival or settlement infrastructure: no.
- Opportunity-risk mismatch or typology: no.

This is a single-module (housing-discrimination) comparator for Tokyo, in the
same cluster as R01_RB_005 (Sugasawa and Harano 2023, 23-wards field
experiment) and R01_RB_006 (Suzuki et al. 2022, atypical tenants). It is the
most recent (2026) item in that cluster. It is a distinct publication, not a
duplicate or preprint of R01_RB_005 (different title, DOI, year, and journal).

## D. Matrix disposition

Disposition: add_to_both_matrices.

- Added to literature_matrix.csv as record_id R01_RB_013.
- Added to gap_verification_matrix.csv as record_id R01_RB_013, coded
  B_partial_overlap.

Reason: the geography is now confirmed as Tokyo, and the item anchors the
housing-discrimination module for Tokyo with current (2026) evidence, matching
the treatment given to the other verified Tokyo housing-discrimination items
(R01_RB_005, R01_RB_006, R01_RB_007), which were all added to both matrices.
Overlap coding is kept cautious (covers_chinese_residents = unclear;
covers_non_chinese_comparison = no), pending full-text confirmation of the
target group.

## E. Gap caution

This single item does not confirm or invalidate the research gap. It covers one
module (housing discrimination) in Tokyo and is not, on metadata, an integrated
Chinese-resident opportunity-risk mismatch study. The absence of an
integrated direct-overlap item among the Round 01 B candidates does not prove
that no such literature exists. The research gap remains unconfirmed and
requires further databases and full-text reading.

## F. Next step

R01_RB_013 was added to both matrices. Proceed to the Japanese-language /
CiNii / J-STAGE / official-source search round. In addition, when full text is
available, confirm the exact target group of the correspondence experiment
(whether foreign or ethnic-minority applicants, and whether Chinese applicants
are included). Do not write the Introduction and do not assert novelty yet.
