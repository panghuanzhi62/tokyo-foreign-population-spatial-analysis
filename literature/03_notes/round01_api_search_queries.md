# Round 01 API Search Queries

Run id: round01_api

These query groups drive the automated metadata harvest. English query strings
are used for the APIs. Romanized Japanese hints are listed for the human who
later runs CiNii / J-STAGE / SciSpace searches; the file is kept ASCII-safe, so
Japanese is given in romaji plus an English gloss rather than kanji.

## Query groups

1. chinese_migration_japan
   - EN: "Chinese migration to Japan"
   - JP (romaji): "chugokujin imin nihon" (Chinese immigrants Japan)

2. chinese_residents_tokyo
   - EN: "Chinese residents Tokyo"
   - JP (romaji): "tokyo chugokujin jumin" (Tokyo Chinese residents)

3. chinese_immigrants_settlement
   - EN: "Chinese immigrants Japan settlement"
   - JP (romaji): "chugokujin teiju nihon" (Chinese settlement Japan)

4. foreign_residents_segregation
   - EN: "foreign residents Japan residential segregation"
   - JP (romaji): "gaikokujin jumin kyoju bunri" (foreign resident residential separation)

5. tokyo_settlement_assimilation
   - EN: "Tokyo immigrant settlement spatial assimilation"
   - JP (romaji): "tokyo imin kukanteki doka" (Tokyo immigrant spatial assimilation)

6. coethnic_location_choice
   - EN: "co-ethnic networks Tokyo immigrant location choice"
   - JP (romaji): "doho nettowaku ricchi sentaku" (co-ethnic network location choice)

7. arrival_infrastructure
   - EN: "arrival infrastructure migrant settlement infrastructure"
   - JP (romaji): "imin teijaku infura" (migrant settlement infrastructure)

8. housing_discrimination
   - EN: "foreigners Tokyo rental housing discrimination"
   - JP (romaji): "gaikokujin chintai jutaku sabetsu" (foreigner rental housing discrimination)

9. service_accessibility_gis
   - EN: "immigrant service accessibility GIS"
   - JP (romaji): "imin sabisu akusesu GIS" (immigrant service access GIS)

10. disaster_vulnerability
    - EN: "foreign residents Tokyo disaster vulnerability evacuation"
    - JP (romaji): "gaikokujin saigai zeijakusei hinan" (foreigner disaster vulnerability evacuation)

11. opportunity_risk_mismatch
    - EN: "opportunity-risk mismatch immigrant settlement"
    - JP (romaji): "kikai risuku fuicchi" (opportunity risk mismatch)

12. urban_opportunity_structure
    - EN: "urban opportunity structure immigrant housing services risk"
    - JP (romaji): "toshi kikai kozo imin" (urban opportunity structure immigrant)

13. spatial_methods
    - EN: "LISA spatial econometrics 2SFCA MGWR spatial typology immigrants"
    - JP (romaji): "kukan keiryo bunseki" (spatial econometric analysis)

## Notes

- These strings are starting points; the harvester sends the EN string to each
  API. Manual rounds should also try the JP romaji and kanji equivalents.
- Sun 2026 (Cities) is the boundary paper. Groups 5 and 6 (settlement /
  assimilation / co-ethnic location choice) are expected to retrieve work close
  to Sun 2026. The project must NOT claim novelty there; the discriminating
  groups are 7-12 (arrival infrastructure, housing, services, disaster,
  opportunity-risk).
