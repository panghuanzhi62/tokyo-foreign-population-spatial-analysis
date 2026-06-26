# DF_M04 Real-Estate Broker Registry (takken) - M-Source Feasibility Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-26
Source ID: DF_M04_mlit_takken_search (primary), DF_M04_tokyo_takken_license_service (secondary)

## A. Purpose

Verify whether real-estate broker registry data (takchi tatemono torihiki gyosha / takken
operators) can support a municipality-level housing-service / migrant-service infrastructure
variable for Greater Tokyo. Real source metadata was checked against official systems; usability
and migrant orientation are NOT assumed. No modeling; no final M dataset; no commit of raw,
address-level, or geocoded records; no heavy scraping.

## B. Research-design role

In the chain X (Chinese registered stock 2023-12) -> M (service infrastructure 2024 /
observable-by-2024) -> Y (Chinese registered stock change 2024-2025), a real-estate broker
registry could in principle proxy HOUSING-MARKET INTERMEDIATION capacity around 2024. The
central caution is that a GENERIC broker registry measures general housing-market service
capacity, not migrant-oriented service infrastructure. It can enter the design as a main or
partial M component only if a defensible migrant-service interpretation or a reproducible
Chinese/foreign-resident orientation marker exists; otherwise it belongs in housing-service /
urban-opportunity control or robustness, or as descriptive context.

## C. Source identity and access

- Primary authoritative source: Construction and Real Estate Operator Enterprise Information
  Search System (kensetsugyosha takkengyosha to kigyo joho kensaku system), operated by MLIT,
  https://etsuran2.mlit.go.jp/TAKKEN/takkenKensaku.do . The takken-operator search lists each
  licensed broker with license number (menkyo bango), trade name (shogo), representative,
  head-office address (honten shozaichi), branch-office address (shiten shozaichi), capital,
  license date (menkyo nengappi), license validity period (menkyo no yuko kikan), concurrent
  business, and affiliated trade body. Coverage is NATIONAL and includes both MLIT-licensed and
  prefecture-licensed operators, so all four target prefectures (Tokyo, Saitama, Chiba,
  Kanagawa) are reachable through one system. Access date 2026-06-26.
- Format: SEARCHABLE DYNAMIC WEB DATABASE (HTML/.do). NO CSV/Excel/bulk download or API was
  found (the system browsing menu and the MLIT hub pages sosei_const_tk3_000037 and _000038 were
  checked). Saitama's takken-search page redirects to this same national system; physical meibo
  inspection (etsuran) is offered only in person at prefectural offices.
- Secondary source: Tokyo Metropolitan takken license information service
  https://www.takken.metro.tokyo.lg.jp/search (free online), BUT electronic browsing covers only
  NEW or RENEWED licenses received on or after 2025-04-01 and only Tokyo-HQ operators - it cannot
  reconstruct a 2024 active stock and does not cover the other three prefectures.
- Reproducibility: WEAK. There is no stable downloadable file for any of the four prefectures.
  No raw records were acquired; only a local-only metadata/reproducibility note was saved (NOT
  committed). Bulk reuse terms are not stated as open; terms risk medium.

## D. Temporal validity

Classification: B_observable_by_2024_or_2025 (primary MLIT system); the Tokyo online service is
C_current_only (post-2025-04-01 licenses only).

The MLIT detail records carry a license date (menkyo nengappi) and a validity period (menkyo no
yuko kikan), so existence/registration by 2024 and active-as-of inference are possible IN
PRINCIPLE. However, this metadata is not bulk-accessible, and the searchable list reflects
currently-valid licenses (right-censoring of cancelled/expired operators). Can-infer-2024-stock:
PARTIAL (registered-by-2024 inferable per record if acquired; precise 2024 active stock is
imperfect and acquisition-blocked).

## E. Spatial feasibility

Can link to the 251 municipality frame: PARTIAL.

MLIT detail records include a full head-office address (honten shozaichi) with municipality,
which would be municipality-parseable and linkable to the 251 frame via a name-to-JIS crosswalk
(as in DF_M01), and the license number prefix distinguishes MLIT vs prefecture licenses. BUT
this is contingent on acquiring records, which the search-only format blocks. address_available
PARTIAL; municipality_name_available PARTIAL; municipality_code_available NO; geocoding_required
PARTIAL. No municipality parsing was validated because no sample was acquired. Per instruction,
full geocoding was NOT run; municipality-name parsing would be validated first if acquired.

## F. Conceptual fit

Service category: urban_opportunity_control. Recommended use: control_candidate (robustness
fallback); NOT main M.

The official registry is a GENERIC list of all licensed real-estate brokers. It carries no
foreign-resident, Chinese-language, multilingual, international, visa, relocation, or
rental-support orientation marker, and no reproducible marker of Chinese/foreign-resident
orientation can be derived from its fields. It therefore measures general housing-market service
capacity, which tracks general commercial/housing density and population - so it risks
DUPLICATING existing controls (commercial density, population) rather than adding migrant-service
signal. It is closer to general urban opportunity structure / housing-market intermediation than
to migrant arrival infrastructure. Restaurant/food is irrelevant and does not enter this source.

## G. Relation to DF_M01-DF_M03

- DF_M01 registered support organizations (toroku shien kikan): institutional SSW migrant
  support - directly migrant-oriented, clean dated Excel, 99.95 percent municipality link.
- DF_M02 Japanese-language education institutions: migrant-relevant but prefecture-level only.
- DF_M03 licensed employment placement offices: distinct labor-market dimension, search-only.
- DF_M04 real-estate broker registry: adds a HOUSING-MARKET INTERMEDIATION dimension distinct
  from M01-M03, but unlike them it is NOT migrant-oriented at all (M01/M02 are migrant-specific;
  M03 is at least a labor-market service). So while conceptually a new dimension, its value is as
  a general housing-service control, not as part of the migrant-oriented M.

## H. Limitations

- Authoritative national source is search-only; no reproducible bulk download or API.
- NOT migrant-specific; no foreign-resident/Chinese-language orientation marker; likely
  collinear with general commercial/housing density and population controls.
- Per-record license dates exist but are not bulk-accessible; current list right-censors closed
  operators.
- Tokyo online service is right-truncated to post-2025-04-01 licenses; cannot rebuild 2024 stock.
- Saitama/Chiba/Kanagawa offer no downloadable list (redirect to MLIT or physical inspection).
- Acquisition would require fragile per-search scraping with medium terms risk.
- Municipality linkage is unvalidated (no sample acquired) though plausible if acquired.

## I. Decision

USE_AS_ROBUSTNESS_OR_CONTROL.

The registry is a legitimate housing-service / urban-opportunity-structure variable, but it is
NOT a migrant-oriented M component (no foreign-resident marker, high collinearity risk with
existing controls) and the official source lacks a reproducible bulk acquisition path.
Operationally it is parked: it is not needed for the migrant-oriented main M, and even its
control use cannot be built reproducibly until a downloadable list is confirmed. Do not scrape
heavily.

## J. Next step

Single next step: proceed to the next clean-address, ideally bulk-downloadable migrant-oriented
A-class source (or move to composite M from the validated migrant-oriented components), and keep
DF_M04 as a control/robustness candidate to revisit only if a reproducible takken list emerges.

## K. Gap status

Gap status: under verification. No novelty asserted; no causal mediation claimed.
