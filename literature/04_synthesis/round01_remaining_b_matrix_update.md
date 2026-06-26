# Round 01 Remaining B-Candidate Matrix Update

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan

## A. Purpose

This note records how the remaining prioritized B candidates from Round 01
verification (the 13 prioritized items minus the three already entered as
R01_HRB_001 / R01_HRB_002 / R01_HRB_003) were reviewed for entry into
literature_matrix.csv and gap_verification_matrix.csv.

## B. Evidence status

- This is based on metadata verification and prior automated verification
  outputs (verified_b_candidates.csv, overlap_risk_scores.csv).
- It is NOT final full-text review.
- It does NOT confirm the research gap.
- It does NOT prove the absence of direct-overlap literature.

## C. Candidate disposition table

| candidate_id | title | year | verification_status | likely_module | matrix_disposition | overlap_category | reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R01_RB_004 | Utilizing Population Distribution Patterns for Disaster Vulnerability Assessment: Foreign Residents in the Tokyo area | 2021 | verified_by_metadata_only | disaster risk / vulnerability | add_to_both_matrices | B_partial_overlap | Strong disaster-module comparator for foreign residents in Tokyo; not Chinese-specific or integrated | optional full-text check of population groups |
| R01_RB_005 | A field experiment on discrimination against foreigners in the rental housing market in Japan (23 wards) | 2023 | verified_by_doi_and_metadata | housing constraint | add_to_both_matrices | B_partial_overlap | Anchors the housing-discrimination module for Tokyo; single module, foreigner-vs-native | use as housing-module citation |
| R01_RB_006 | Discrimination against the atypical type of tenants in the Tokyo private rental housing market | 2022 | verified_by_doi_and_metadata | housing constraint | add_to_both_matrices | B_partial_overlap | Housing-module comparator; foreign/Chinese focus not isolated | confirm foreign-tenant focus in full text |
| R01_RB_007 | Factors enhancing residential satisfaction of foreign residents toward settlement: Toshima City, Tokyo | 2024 | verified_by_doi_and_metadata | housing constraint / settlement | add_to_both_matrices | B_partial_overlap | Links housing to settlement environment in a Tokyo ward; not Chinese-specific | check if Chinese residents separately analyzed |
| R01_RB_008 | Voices of Foreign Residents in Yokohama and Tokyo at the Time of the 1923 Kanto Earthquake | 2023 | verified_by_doi_and_metadata | disaster risk / vulnerability | add_to_both_matrices | B_partial_overlap | Historical disaster-exposure framing; not a contemporary spatial study | verify authorship; historical context only |
| R01_RB_009 | Bolstering disaster preparedness among Japan's foreign residents | 2022 | verified_by_doi_and_metadata | disaster risk (background) | add_to_literature_matrix_only | E_background_only | East Asia Forum commentary, non-peer-reviewed; not Tokyo/Chinese-specific | background framing only |
| R01_RB_010 | The impact of COVID-19 pandemic on public engagement approaches to disaster preparedness for foreign residents | 2022 | verified_by_metadata_only | disaster risk / service (background) | add_to_literature_matrix_only | E_background_only | Japan-wide, not Tokyo or Chinese-specific | background framing only |
| R01_RB_011 | Administrative Services for Foreign Residents | 1997 | verified_by_doi_and_metadata | service accessibility (background) | add_to_literature_matrix_only | E_background_only | Dated (1997), Japan-wide book chapter | service-policy lineage only |
| R01_RB_012 | Potential of mosques to serve as evacuation shelters for foreign Muslims during disasters: Gunma, Japan | 2021 | verified_by_doi_and_metadata | disaster risk / service (background) | add_to_literature_matrix_only | E_background_only | Gunma (not Tokyo), non-Chinese population | service-infrastructure background |
| R01_RB_013 | Disentangling transaction-stage and management-stage discrimination in the rental housing market | 2026 | verified_by_doi_and_metadata | housing constraint | hold_for_manual_check | hold_for_manual_check | Metadata title does not state Japan/Tokyo; geography needs confirmation before entry | manual check of study area before adding |

## D. Matrix additions

Added to literature_matrix.csv (9 rows):
- R01_RB_004, R01_RB_005, R01_RB_006, R01_RB_007, R01_RB_008 (also in gap matrix)
- R01_RB_009, R01_RB_010, R01_RB_011, R01_RB_012 (literature matrix only; background)

Added to gap_verification_matrix.csv (5 rows):
- R01_RB_004, R01_RB_005, R01_RB_006, R01_RB_007, R01_RB_008

## E. Candidates held or excluded

- Held for manual check (1): R01_RB_013 (round01_api-0156). The verified metadata
  title does not state the study area; confirm it is a Japan/Tokyo rental-market
  study before adding it to the matrices.
- Excluded as duplicate/preprint (0): none among the remaining candidates. The
  one preprint (round01_api-0080) was already represented by the published
  version under R01_HRB_002 in the prior task.
- Excluded as false positive / out of scope (0): none. round01_api-0156 was
  flagged false_positive by automated triage but is held rather than excluded,
  because its journal and authorship suggest a likely Japan housing study that
  needs manual geographic confirmation.

## F. Direct-overlap caution

None of the remaining candidates appears, on metadata alone, to approach the
full provisional-topic combination (Chinese residents or Chinese nationals in
Metropolitan Tokyo, plus Chinese vs non-Chinese comparison, plus housing, plus
transit/accessibility, plus services, plus disaster/risk exposure, plus
opportunity-risk typology or mismatch). The added items each cover one or two
modules (housing OR disaster OR services) and are generally not Chinese-specific.

Stated cautiously: this does not prove that no such literature exists, and it
does not confirm the research gap. Full-text reading and additional databases
are still required.

## G. Next steps

- Continue with manual or SciSpace review only for candidates still held for
  manual check (R01_RB_013).
- Begin a second-round API or manual search for Japanese-language sources,
  CiNii, J-STAGE, and official reports.
- Do not write the Introduction yet.
- Do not assert novelty yet.
