# Census 00200521 Municipality Area-Code Confirmation - Note

Project: Chinese Residents and Opportunity-Risk Environments in Metropolitan Tokyo
(provisional working title): A Public-Data Analysis of Housing, Accessibility,
Services, and Disaster Exposure.

Repo: E:\rsch\laborJapan
Branch: agentic-upgrade
Companion file: literature/02_matrices/census_00200521_municipality_area_code_confirmation.csv
Summary CSV: literature/02_matrices/census_00200521_municipality_area_code_summary.csv

## A. Purpose

This note confirms the municipality cdArea list for Census 00200521 table 0003445244
before the bounded extraction script is written. It enumerates and classifies every
municipality-equivalent area code in the four target prefectures (Tokyo, Saitama,
Chiba, Kanagawa), derived from the official e-Stat getMetaInfo area dimension.

## B. Evidence boundary

- This is metadata-only (getMetaInfo area dimension; no getStatsData).
- No population values were retrieved.
- No full extraction was run; no all-Japan retrieval.
- No preprocessing or modeling was run.
- This is NOT a literature gap claim; NOT manuscript text; does NOT prove novelty.
- ESTAT_APP_ID was read from the environment only; never printed, written, or
  committed; no API URL containing it was saved. No raw API output was saved into or
  committed to the repo (the confirmation CSV is classified metadata: area codes,
  names, and classification only).
- Gap status remains: under verification.

## C. Confirmed source parameters

- statistics code: 00200521
- provider tstat: 000001136464
- statsDataId: 0003445244
- census year / cdTime: 2020 / 2020000000
- cdCat01: 0 (sex total)
- cat02: 1 (foreign total), 102 (China)
- target prefectures: 13 (Tokyo), 11 (Saitama), 12 (Chiba), 14 (Kanagawa)
- main unit: municipality
- expected join key: 5-digit JIS municipality code (to NLNI N03)

## D. Area-code summary table

| prefecture | prefecture_code | confirmed municipality rows | special / designated wards note | island municipalities note | join-key status | remaining issue |
| --- | --- | --- | --- | --- | --- | --- |
| Tokyo | 13 | 62 | 23 special wards (13101-13123); special-wards aggregate 13100 excluded | 9 island municipalities flagged (Izu/Ogasawara) | expected_direct_5digit_join | island inclusion decision deferred |
| Saitama | 11 | 72 | Saitama-shi 10 designated-city wards; parent 11100 excluded | none | expected_direct_5digit_join | ward-vs-city aggregation choice |
| Chiba | 12 | 59 | Chiba-shi 6 designated-city wards; parent 12100 excluded | none | expected_direct_5digit_join | ward-vs-city aggregation choice |
| Kanagawa | 14 | 58 | Yokohama 18 + Kawasaki 7 + Sagamihara 3 wards; parents 14100/14130/14150 excluded | none | expected_direct_5digit_join | ward-vs-city aggregation choice |
| ALL FOUR | 13;11;12;14 | 251 | designated-city wards used instead of parents | 9 flagged (Tokyo only) | expected_direct_5digit_join | confirm ward-level matches N03 |

Composition of the 251 included units: special wards 23; designated-city wards 44
(Saitama 10, Chiba 6, Yokohama 18, Kawasaki 7, Sagamihara 3); cities 117; towns 56;
villages 11. Excluded aggregate rows (not municipalities): 4 prefecture totals,
5 designated-city parents (11100, 12100, 14100, 14130, 14150), and 1 Tokyo
special-wards aggregate (13100) - 10 aggregate rows total. CSV has 261 rows (251
included + 10 excluded aggregates).

## E. Join-key implications

- e-Stat municipality codes here are standard 5-digit JIS codes and appear DIRECTLY
  compatible with NLNI N03 administrative-area codes (gyosei kuiki code). join-key
  status for all 251 included units is expected_direct_5digit_join.
- Tokyo special wards are represented correctly as individual municipality-level
  areas (13101-13123); their aggregate 13100 (tokubetsu-ku-bu) is excluded to avoid
  double counting.
- Designated cities are represented BOTH as a parent aggregate (excluded) AND as
  individual wards (included). N03 also represents these wards individually, so
  ward-level is the consistent join unit. The ward-vs-whole-city aggregation choice
  is recorded for the extraction step; default is ward-level to match N03.
- Island municipalities (9, Tokyo Izu/Ogasawara) are INCLUDED but flagged; final
  exclusion is deferred to a study-area-definition task (not silently removed).
- All codes are handled as STRINGS to preserve exact 5-digit form. For the four
  target prefectures (codes 11xxx-14xxx) no leading zero is required, but the code
  must stay a string so that any later national join (e.g. Hokkaido 01xxx) does not
  drop leading zeros.

## F. Extraction implication

This confirmed list of 251 municipality-equivalent cdArea codes is the required
input for the future bounded extraction script
(scripts/11_official_data/census_00200521_municipality_population_extract.py). That
script must restrict cdArea to these codes and MUST refuse all-Japan extraction by
default. Bounded extraction retrieves, per included municipality, only the China
(cat02=102) and foreign-total (cat02=1) values for cdCat01=0, cdTime=2020000000.

## G. Next step

Recommended next task: "Census 00200521 bounded municipality extraction script
scaffold".

This should be created only now that the area-code list is confirmed. The next
script must still begin with --dry-run and --metadata-only modes before any bounded
value retrieval, read ESTAT_APP_ID from the environment only, never print/write/
commit the appId, store raw outputs locally only if explicitly permitted, and refuse
all-Japan extraction by default. No Introduction; no novelty; gap remains under
verification.
