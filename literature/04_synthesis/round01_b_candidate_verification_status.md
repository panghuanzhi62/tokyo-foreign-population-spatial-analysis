# Round 01 B-Candidate Verification Status

Project: Tokyo-China opportunity-risk mismatch (provisional working title)
Repo: E:\rsch\laborJapan
Run id: round01_b_verify

## A. Purpose

This note summarizes automated bibliographic and overlap-risk
verification of the 13 prioritized B_partial_overlap_candidate records
from literature/04_synthesis/round01_b_candidate_review.md.

## B. Evidence status

- This is automated metadata verification.
- It is NOT final deep reading.
- It does NOT confirm the research gap.
- It does NOT prove absence of direct-overlap literature.
- It must be followed by SciSpace and manual full-text verification.

## C. Verification coverage

- Candidates processed: 13
- Endpoints attempted: crossref, doi_resolver, openalex, semantic_scholar
- CiNii used: no (no CINII_APP_ID)
- Verified by DOI and metadata: 8
- Verified by metadata only: 4
- Partially verified: 0
- Not verified: 0
- Duplicates or preprints: 1
- Network skipped: 0

Note: 0 preliminary A_direct_overlap_candidate items in Round 01 does
NOT confirm the research gap and does NOT prove that no direct-overlap
literature exists.

## D. Candidate verification table

| priority_rank | record_id | short_title | doi | verification_status | likely_module | recommended_overlap_category | direct_overlap_risk_score | manual_deep_read_priority | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | round01_api-0200 | Utilizing Population Distribution Patterns for Disaster Vuln... | 10.3390/ijerph18084061 | verified_by_metadata_only | disaster risk / vulnerability | B_partial_overlap_verified | 1 | medium | manual publisher/abstract check |
| 2 | round01_api-0018 | Chinese Newcomers in Japan: Migration Trends, Profiles and t... | 10.1177/011719681302200204 | verified_by_metadata_only | Chinese migration / Chinese residents | B_partial_overlap_verified | 4 | medium | manual publisher/abstract check |
| 3 | round01_api-0146 | A field experiment on discrimination against foreigners in t... | 10.1016/j.jjie.2023.101273 | verified_by_doi_and_metadata | housing constraint | B_partial_overlap_verified | 1 | medium | manual publisher/abstract check |
| 4 | round01_api-0149 | Discrimination against the atypical type of tenants in the T... | 10.1016/j.jhe.2022.101879 | verified_by_doi_and_metadata | housing constraint | B_partial_overlap_verified | 1 | medium | manual publisher/abstract check |
| 5 | round01_api-0155 | Factors enhancing residential satisfaction of foreign reside... | 10.1007/s10901-024-10160-3 | verified_by_doi_and_metadata | housing constraint | B_partial_overlap_verified | 2 | medium | manual publisher/abstract check |
| 6 | round01_api-0080 | Residential Segregation in Japan: Ethnic Stratification in a... | 10.31235/osf.io/beh43 | duplicate_or_preprint | spatial assimilation / co-ethnic networks | duplicate_or_preprint | 3 | low | low-priority manual check |
| 7 | round01_api-0210 | Voices of Foreign Residents in Yokohama and Tokyo at the Tim... | 10.20965/jdr.2023.p0598 | verified_by_doi_and_metadata | disaster risk / vulnerability | B_partial_overlap_verified | 1 | medium | manual publisher/abstract check |
| 8 | round01_api-0212 | Bolstering disaster preparedness among Japan's foreign resid... | 10.59425/eabc.1647381639 | verified_by_doi_and_metadata | disaster risk / vulnerability | E_background_only | 2 | low | low-priority manual check |
| 9 | round01_api-0215 | The impact of COVID-19 pandemic on public engagement approac... | 10.1108/ijdrbe-08-2021-0095 | verified_by_metadata_only | disaster risk / vulnerability | E_background_only | 1 | low | low-priority manual check |
| 10 | round01_api-0086 | Administrative Services for Foreign Residents | 10.1057/9780230374522_8 | verified_by_doi_and_metadata | service accessibility | E_background_only | 2 | low | low-priority manual check |
| 11 | round01_api-0001 | Educationally Channeled International Labor Mobility: Contem... | 10.1111/j.1747-7379.2008.01152.x | verified_by_metadata_only | Chinese migration / Chinese residents | B_partial_overlap_verified | 4 | medium | manual publisher/abstract check |
| 12 | round01_api-0156 | Disentangling transaction-stage and management-stage discrim... | 10.1016/j.jhe.2026.102134 | verified_by_doi_and_metadata | housing constraint | false_positive_or_out_of_scope | 1 | low | low-priority manual check |
| 13 | round01_api-0202 | Potential of mosques to serve as evacuation shelters for for... | 10.1007/s11069-021-04883-7 | verified_by_doi_and_metadata | disaster risk / vulnerability | E_background_only | 2 | low | low-priority manual check |

## E. High-risk items for SciSpace Deep Review

- round01_api-0018 (rank 2, risk 4): Chinese Newcomers in Japan: Migration Trends, Profiles and the Impact of the 201...
- round01_api-0080 (rank 6, risk 3): Residential Segregation in Japan: Ethnic Stratification in a Global New Destinat...
- round01_api-0001 (rank 11, risk 4): Educationally Channeled International Labor Mobility: Contemporary Student Migra...

Compact SciSpace prompts for these items are generated locally in
outputs/literature_verification/round01_b_verify/scispace_deep_review_prompts.md
(not committed).

## F. Direct-overlap caution

No B candidate appears, on metadata alone, to approach the full
provisional-topic combination (Chinese residents in Metropolitan
Tokyo, plus Chinese vs non-Chinese comparison, plus housing, plus
transit/accessibility, plus services, plus disaster/risk exposure,
plus opportunity-risk typology or mismatch). The verified items
cluster on single modules (housing OR disaster OR services).

Stated cautiously: this does not prove that no such literature exists.
Manual deep review and additional databases are still required.

## G. Next steps

- Use SciSpace Deep Review on the highest-risk items.
- Manually check publisher pages and abstracts.
- Update literature_matrix.csv and gap_verification_matrix.csv only
  after verification.
- Do not write the introduction yet.
