# DF_M02 Japanese-Language Education Institutions - M-Source Feasibility Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-25
Source ID: DF_M02_japanese_language_education_institutions

## A. Purpose

Verify whether Japanese-language education institutions can serve as a dated, reproducible
migrant-oriented service-infrastructure subcomponent for Greater Tokyo municipalities, using
the same standard applied to DF_M01. No modeling; no final M dataset; no commit of raw,
address-level, or geocoded records.

## B. Research-design role

In the chain X (Chinese registered stock 2023-12) -> M (migrant-oriented service infrastructure
2024 / observable-by-2024) -> Y (Chinese registered stock change 2024-2025), Japanese-language
schools are a strong CONCEPTUAL migrant-education subcomponent of M (arguably among the most
migrant-specific service types). The question is whether the official lists support a dated,
municipality-level measure.

## C. Source identity and access

Two official lists exist:
- PRIMARY (comprehensive): MOJ/ISA notified institutions list (homusho kokuji nihongo kyoiku
  kikan), https://www.moj.go.jp/isa/applications/resources/nyuukokukanri07_00217.html ;
  published as PDF (60 pages, ~280KB), current as of 2026-05-12 (latest amendment, Reiwa 8).
  This is the student-visa eligibility list.
- COMPLEMENT (date-anchored, new): MEXT certified institutions list (nintei nihongo kyoiku
  kikan) under the 2024 accreditation system (effective 2024-04-01),
  https://www.mext.go.jp/a_menu/nihongo_kyoiku/1420729_00022.htm ; PDF, published per
  certification round with round-level certification dates; coverage is still transitional.

A local-only copy of the kokuji PDF was acquired for inspection (data_raw_official/...). It is
NOT committed. Terms: no explicit restrictive terms stated; official government content (low
risk).

## D. Temporal validity

Classification: B_observable_by_2024_or_2025.

The kokuji list is a CURRENT snapshot (as of 2026-05-12) with a list-level amendment date but
NO per-institution designation date, and no explicit status/closure field. Existence by 2024 is
plausible for established institutions but cannot be dated per record from this list. The MEXT
nintei list carries round-level certification dates from FY2024 onward and could date a subset
to 2024-2025, but its coverage is incomplete during the transition. Can-infer-2024-stock:
PARTIAL.

## E. Spatial feasibility

Can link to the 251 municipality frame: PARTIAL (NO directly from the official list; PARTIAL
only via per-institution geocoding).

Direct inspection of the kokuji PDF shows the address column (shozaichi) is PREFECTURE-LEVEL
ONLY: the table lists name plus prefecture, with ZERO municipality (ku/shi/cho/son) tokens in
the address column. Approximate extracted counts: ~1,390 institutions nationally and ~670 in
Greater Tokyo (Tokyo 488, Saitama 69, Chiba 68, Kanagawa 45; counts approximate because the PDF
uses vertical text that extracts imperfectly). Because no municipality field exists, linkage to
the 251 frame is not possible from the official list alone and requires geocoding each
institution by name/address (some institution NAMES carry locality markers such as branch
campus names, but that is not a structured municipality field).

## F. Conceptual fit

Recommended use: partial_M_component_with_limitations.

Japanese-language schools are conceptually a core migrant-education service (service_category =
core_migrant_service), but the official data does not deliver a dated, municipality-level
measure without substantial geocoding. Main-model candidacy is therefore PARTIAL; the source is
a solid robustness/secondary subcomponent and a good visibility layer.

## G. Limitations

- Prefecture-only address in the kokuji list; municipality requires geocoding (geocoding_required = YES).
- No per-institution designation date in the kokuji list (timestamp_fields_available = NO).
- Vertical-text PDF (no Excel/CSV); structured parsing is fragile (reproducibility medium-weak).
- Student-visa institutions only; excludes non-visa community Japanese-language classes and informal Chinese-oriented language services.
- Not China-specific.
- The nintei complement is date-anchored but transitional/incomplete.

## H. Decision

USE_AS_PARTIAL_M_COMPONENT_WITH_LIMITATIONS.

The source is official and conceptually strong, but as published it cannot yield a dated,
municipality-level count without per-institution geocoding; it is a partial/robustness
subcomponent, not a clean main component like DF_M01.

## I. Next step

Single next step: proceed to the next clean-address A-class source (licensed employment
placement offices or real-estate brokers, which carry full municipality addresses like DF_M01)
for the composite M; in parallel, evaluate the MEXT nintei list for municipality and
certification-date fields, and if DF_M02 is to be used at municipality level, build a
geocoding step keyed to the 251 frame.

## J. Gap status

Gap status: under verification. No novelty asserted; no causal mediation claimed.
