# Fast ISA/e-Stat Exact-Table Confirmation Guide - DDL_001 and DDL_002

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan
Tokyo (provisional working title).
Repo: E:\rsch\laborJapan
Round: 02 (fast exact-table confirmation for the two core population inputs)
Companion template: metadata/isa_estat_ddL001_ddL002_fast_confirmation_template.csv

## A. Purpose

This is a fast, focused guide for confirming the EXACT official table/source for
the two core population-baseline inputs - DDL_001 (Chinese resident count) and
DDL_002 (total foreign resident count) - BEFORE any download or API extraction.
It is deliberately narrow: only these two rows.

## B. Why this is needed

The existing-data inventory and reuse audit found old Tokyo baseline data that
support an ALL-foreign-resident workflow, but NO confirmed Chinese-nationality
breakdown. Therefore DDL_001 must be confirmed directly from the official source
before acquisition; it cannot be assumed reusable from the old baseline. DDL_002
must be confirmed in the same source family so the two are compatible.

## C. What to confirm for DDL_001 (Chinese resident count)

- official page URL (ISA statistics / e-Stat dataset listing)
- exact table or dataset name (Zairyu Gaikokujin Tokei nationality-by-area)
- dataset / table ID (e-Stat)
- year or reference date (biannual Jun/Dec; choose vintage)
- geographic unit (municipality, and prefecture)
- whether "Chinese" means nationality-based Chinese nationals / Chinese residents
  BY NATIONALITY (NOT Chinese-origin residents)
- admin code or join key (JIS municipality code + vintage)
- download / API route (e-Stat table download or WebAPI with application ID)
- license / terms URL (Government Standard Terms / Seifu Hyojun Riyo Kiyaku)
- file format and encoding (Excel/CSV or WebAPI JSON/XML; UTF-8 vs Shift-JIS)

## D. What to confirm for DDL_002 (total foreign resident count)

- official page URL (same ISA / e-Stat family as DDL_001)
- exact table or dataset name (total foreign-resident table)
- dataset / table ID (e-Stat)
- SAME year / reference date as DDL_001
- SAME geographic unit as DDL_001
- definition of total foreign residents (total row vs sum over nationalities)
- admin code or join key (JIS municipality code matching DDL_001 vintage)
- download / API route (e-Stat table download or WebAPI)
- license / terms URL (Government Standard Terms)
- file format and encoding

## E. Compatibility rule

DDL_001 and DDL_002 may be approved only if their source family, year, geography,
category definitions, and join key are compatible.

Non-Chinese foreign residents must NOT be computed until DDL_001 and DDL_002 are
both confirmed, approved, acquired, and metadata-recorded.

## F. User action

1. Manually open the ISA / e-Stat pages.
2. Fill the CSV template
   (metadata/isa_estat_ddL001_ddL002_fast_confirmation_template.csv), setting
   manual_confirmation_status to confirmed / partially_confirmed / not_found /
   unclear and recording the exact table name, dataset ID, year, geography,
   category label, join key, route, license, and format.
3. Once both rows are confirmed and compatible, request a NARROW acquisition
   script for DDL_001 and DDL_002 ONLY.

## G. What not to do yet

- Do not download data yet.
- Do not call the API yet.
- Do not approve in the decision log yet.
- Do not compute derived variables (non-Chinese, shares).
- Do not handle DDL_010 (total population denominator) yet.
- Do not handle density, hazard, service, housing, or railway yet.
- Do not write the final Introduction.
- Do not assert novelty.

Status remains: gap under verification.
