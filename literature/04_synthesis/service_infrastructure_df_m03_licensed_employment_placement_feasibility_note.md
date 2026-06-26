# DF_M03 Licensed Employment Placement Offices - M-Source Feasibility Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
Repo: E:\\rsch\\laborJapan   Branch: agentic-upgrade   Date: 2026-06-25
Source ID: DF_M03_licensed_employment_placement_offices

## A. Purpose

Verify whether licensed fee-charging employment placement offices (yuryo shokugyo shokai
jigyosha) can serve as a migrant-oriented service-infrastructure source for Greater Tokyo
municipalities. Real source metadata was checked; usability is NOT assumed. No modeling; no
final M dataset; no commit of raw, address-level, or geocoded records; no heavy scraping.

## B. Research-design role

In the chain X (Chinese registered stock 2023-12) -> M (migrant-oriented service infrastructure
2024 / observable-by-2024) -> Y (Chinese registered stock change 2024-2025), employment
placement offices are conceptually relevant to migrant OPPORTUNITY STRUCTURE and settlement
pathways (job brokerage), and would add a distinct labor-market dimension to M. The question is
whether the official source supports a dated, reproducible, municipality-level measure.

## C. Source identity and access

- Authoritative source: Jinzai Service Comprehensive Site (jinzai service sogo site), operated
  by MHLW, https://jinzai.hellowork.mhlw.go.jp/JinzaiWeb/ ; the employment-placement search
  (shokugyo shokai jigyosho kensaku) lists licensed offices with permit number, address, and
  permit/expiration dates in per-office detail records. Prefectural Labour Bureaus issue the
  permits.
- Format: SEARCHABLE DYNAMIC WEB DATABASE (HTML/.do). NO CSV/Excel/bulk download or API was
  found (portal homepage, Tokyo Labour Bureau page, and the site help page were all checked).
  The site is reported as congested. Access date 2026-06-25.
- Reproducibility: WEAK. There is no stable downloadable file; acquisition would require
  systematic per-prefecture form queries plus per-office detail extraction (scraping a dynamic,
  congested site), which is fragile and possibly terms-restricted. No raw records were
  acquired; only a local-only metadata/reproducibility note was saved (NOT committed).
- Terms: no open-data license stated; bulk reuse risk is medium.

## D. Temporal validity

Classification: B_observable_by_2024_or_2025.

Per-office detail records carry a permit date (kyoka nengappi) and an expiration date (yuko
kikan manryobi), so existence/registration by 2024 and active-as-of inference are possible IN
PRINCIPLE. However, this metadata is not available in any bulk/downloadable form, and the
searchable list reflects currently-valid permits (right-censoring of cancelled/expired offices).
Can-infer-2024-stock: PARTIAL (registered-by-2024 inferable per record if acquired; a precise
2024 active stock is imperfect and acquisition-blocked).

## E. Spatial feasibility

Can link to the 251 municipality frame: PARTIAL.

Per-office detail records include a full office address (shozaichi) with municipality, which
would be municipality-parseable and linkable to the 251 frame (via a name-to-JIS crosswalk,
like DF_M01), and the permit number's first two digits encode the issuing prefecture. BUT this
is contingent on acquiring the records, which the search-only format blocks. address_available
PARTIAL; municipality_name_available PARTIAL; municipality_code_available NO; geocoding_required
PARTIAL. No municipality parsing was validated because no sample was acquired.

## F. Conceptual fit

Recommended use: robustness_component.

Employment placement is conceptually a core labor-market/opportunity-structure service, but the
list is GENERIC (all licensed placement offices; no foreign-worker-specific marker or filter),
so it is not migrant-specific. Combined with the weak reproducibility, it is best treated as a
robustness/opportunity-structure layer rather than a main or core component.

## G. Relation to DF_M01 and DF_M02

DF_M03 adds a DISTINCT labor-market/employment-brokerage dimension not covered by DF_M01
(registered support organizations; institutional SSW migrant support) or DF_M02
(Japanese-language education). Conceptually additive. However, unlike DF_M01 (clean Excel,
dated, 99.95 percent municipality link) and even DF_M02 (downloadable PDF), DF_M03 is NOT
reproducibly downloadable, and it is not migrant-specific - so its practical contribution is
weaker than its conceptual appeal.

## H. Limitations

- No reproducible bulk download or API (searchable web database only); congested site.
- Not migrant-specific (no foreign-worker filter); generic placement/staffing firms dominate.
- Per-record dates exist but are not bulk-accessible; current list right-censors closed offices.
- Acquisition would require fragile per-search scraping with medium terms risk.
- Municipality linkage is unvalidated (no sample acquired) though plausible if acquired.

## I. Decision

HOLD_PENDING_SOURCE_VALIDATION.

The data is conceptually valuable and field-rich, but the source as published lacks a confirmed
reproducible acquisition path. Validate a reproducible list (a CSV export within the search
results, a prefectural Labour Bureau published list, or a periodic official file) before any use;
do not scrape heavily.

## J. Next step

Single next step: proceed to the next clean-address, bulk-downloadable A-class source - the real
estate broker (takken) license search (MLIT/prefectures), which provides downloadable
municipality-level records like DF_M01 - and keep DF_M03 on HOLD pending confirmation of a
reproducible employment-placement list.

## K. Gap status

Gap status: under verification. No novelty asserted; no causal mediation claimed.
