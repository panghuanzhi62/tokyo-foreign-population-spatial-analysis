# DF_M01 Registered Support Organizations - M-Source Feasibility Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Date: 2026-06-25

## A. Purpose

This note verifies whether DF_M01 - the Immigration Services Agency registry of REGISTERED
SUPPORT ORGANIZATIONS (toroku shien kikan torokubo) - can serve as a dated, reproducible,
official component of migrant-oriented SERVICE INFRASTRUCTURE for Greater Tokyo
municipalities. This is a real source-validation task. No modeling is run, no final M dataset
is built, and no raw/address-level/geocoded records are committed. No novelty and no causal
mediation are claimed.

## B. Research-design role

In the design chain
  X (Chinese registered stock, 2023-12)
  -> M (migrant-oriented service infrastructure, 2024 / observable-by-2024)
  -> Y (Chinese registered stock change, 2024-06/2024-12 to 2025-06),
DF_M01 is a candidate measure of the M layer: registered support organizations are
institutional migrant-support providers tied to the Specified Skilled Worker (tokutei ginou)
system. Each organization carries an official registration date, so its existence by/around
2024 can be dated - the property M requires to act as a temporally ordered predictor sitting
after X (2023) and before Y (2024-2025).

## C. Source identity and access

- Official name: Registered support organizations registry (toroku shien kikan torokubo);
  English: List of Registered Support Organization.
- Provider: Immigration Services Agency of Japan (Shutsunyukoku Zairyu Kanricho), Ministry of
  Justice. Official status: official.
- URL: https://www.moj.go.jp/isa/applications/ssw/nyuukokukanri07_00205.html
- Access date: 2026-06-25. Format: Excel (Japanese ~2.5MB; English ~1.8MB). Current edition
  as of 2026-06-18, 11,439 organizations.
- Reproducibility: strong. The file is an official, publicly downloadable government registry
  with a clear as-of date and a stable per-record registration number. No explicit restrictive
  terms of use are stated on the page (standard government-content reuse assumed; low risk).
- Local-only sample: the full current file was downloaded to
  data_raw_official/service_infrastructure/DF_M01_registered_support_organizations/ for field
  inspection only. It is NOT committed.

Observed fields (header row, 10 columns): 1 Registration number; 2 Date of Registration
(toroku nengappi); 3 Name; 4 Address (postal code + prefecture-prefixed org address + phone);
5 Representative; 6 Office implementing support (separate support-office address); 7 Detail of
support and method; 8 Date of starting support; 9 Language (supported languages / consultation
capacity); 10 Note.

## D. Temporal validity

Classification: B_observable_by_2024_or_2025.

Reason: every record carries an official Date of Registration, so existence/registration by a
given year is directly datable (11,439 of 11,439 records have a registration date; 11,376
parse cleanly; the rest use non-standard date text). On the current national file, 9,135 of
11,439 organizations were registered by 2024-12-31 and 8,018 by 2024-06-30. HOWEVER, the
public file is a CURRENT-active snapshot and contains NO cancellation or deletion date and no
explicit status column: organizations whose registration lapsed or was withdrawn before
2026-06-18 are simply absent. A registration-date filter on the current file therefore
identifies organizations registered by 2024 AND still active in 2026 - which UNDERCOUNTS the
true 2024 active stock (right-censoring). This is why the strict class is
B_observable_by_2024_or_2025 and NOT A_2024_stock. The class can be upgraded to A_2024_stock
by additionally acquiring an archived registry snapshot dated around 2024-12 (the agency
publishes periodic editions; dated editions are independently mirrored), which would directly
observe the active stock as of 2024.

## E. Spatial feasibility

Can link to the 251 Greater Tokyo municipality frame: YES (via address parse + name-to-code
crosswalk; no coordinate geocoding required).

Evidence: filtering org addresses to the four Greater Tokyo prefectures yields 3,737
organizations (Tokyo 2,330; Chiba 514; Saitama 462; Kanagawa 431). 100 percent of these
parse to a municipality token (ku/shi/cho/son) directly from the address string, spanning
about 173 distinct municipalities; the remaining municipalities in the 251 frame are genuine
zeros. Municipality CODE is not provided and must be derived by a prefecture + municipality
name to JIS-code crosswalk (the same name-to-code crosswalk already noted as needed elsewhere
in the project). A parallel support-office address field (col 9) gives a near-identical
3,712 Greater Tokyo records and can be used as the service-POINT alternative to the
organization HQ address.

## F. Conceptual fit

Recommended use: partial_M_component_with_limitations.

DF_M01 is an explicitly migrant-oriented, official, dated, spatially linkable institutional
service infrastructure - a strong CORE subcomponent of M and a valid main-model candidate.
But it measures one slice of migrant support (Specified Skilled Worker employment/settlement
support), is not China-specific, and distinguishes an HQ address from the actual support
office. It is therefore best treated as one dated subcomponent of a broader migrant-service
infrastructure measure rather than the whole M variable.

## G. Limitations

- Not China-specific: it serves all Specified Skilled Worker nationalities; Chinese
  orientation can only be approximated via the supported-language column or name markers.
- Scope skew: represents employment/legal/SSW settlement support, not broad daily-life ethnic
  services; it will omit informal Chinese-oriented services.
- Right-censoring: the current file has no cancellation/deletion date, so a single current pull
  undercounts true 2024 active stock; an archived ~2024-12 snapshot is needed for A-class.
- HQ vs service point: organization address (col 4) and support-office address (col 9) differ;
  the choice affects municipality assignment.
- Requires address parsing and a name-to-JIS-code crosswalk (no coordinate geocoding, but
  normalization is non-trivial for ~6 records with missing addresses and date-text edge cases).
- One subcomponent: a defensible M layer needs multiple A-class sources (takken real-estate
  brokers, designated Japanese-language institutions, licensed employment placement) plus a
  public-support layer.

## H. Decision

USE_AS_PARTIAL_M_COMPONENT_WITH_LIMITATIONS.

DF_M01 is validated as a dated, reproducible, official, spatially linkable migrant-oriented
service source for Greater Tokyo, suitable as a core but partial subcomponent of M. It is not,
on its own and from the current file alone, a perfect 2024 active-stock measure, and it is not
China-specific.

## I. Next step

Single next step: BUILD THE FULL LOCAL-ONLY COLLECTION/PARSER for DF_M01 - a local-only
script that (1) reads the official registry file, (2) parses org and support-office addresses
to prefecture + municipality, (3) crosswalks municipality names to JIS codes on the 251 frame,
(4) filters by registration date to construct an observable-by-2024 organization count per
municipality, and (5) additionally ingests an archived ~2024-12 registry snapshot to upgrade
the measure toward A_2024_stock. Keep DF_M01 as one M subcomponent and, in parallel, proceed
to the second A-class source. Produce only compact local-only municipality counts; do not
commit raw, address-level, or geocoded records.

## J. Gap status

Gap status: under verification. No novelty asserted; no causal mediation claimed.
