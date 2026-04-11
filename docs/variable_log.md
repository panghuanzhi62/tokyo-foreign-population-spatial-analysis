# Variable Log

| Variable | Track | Role | Source | Year | Unit | Transformation | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| foreign_ratio | Explanatory / Predictive | Response / target candidate | Existing Tokyo repo municipal foreign-population dataset | current baseline year | ratio | none | existing | current dependent variable in baseline explanatory workflow |
| log_dist_to_station_m | Explanatory / Predictive | Predictor | Existing station accessibility pipeline | current baseline year | meters | log | existing | current station accessibility variable |
| log_median_land_price_jpy | Explanatory / Predictive | Predictor | Existing land-price integration pipeline | current baseline year | JPY | log | existing | current land-value variable |
| ols_resid | Explanatory | Diagnostic | derived from baseline OLS | current baseline year | residual | none | existing | used in Moran / LISA diagnostics |
| lisa_cluster | Explanatory | Diagnostic / interpretation | derived from Local Moran | current baseline year | class | none | existing | used for cluster interpretation and MGWR-ready export |
| distance_to_central_tokyo | Explanatory / Predictive | Added predictor candidate | To be derived from municipal centroid to Tokyo Station (or fixed central-Tokyo point) | current baseline year | meters / km | likely log | ready to derive | separates near-core location from simple nearest-station accessibility |
| population_density | Explanatory / Predictive | Added predictor candidate | To be derived if total population and municipal area are available in current or mergeable data | current baseline year | persons per km² | maybe log | candidate | urban scale / built-up intensity proxy |
| rental_housing_share | Explanatory / Predictive | Added predictor candidate | External housing statistics table to be harmonized to municipality | current baseline year | share | none | source-pending | settlement capacity / housing structure variable |
| future_foreign_ratio | Predictive | Preferred target | Requires at least two comparable time points | t+1 | ratio | none | target candidate | preferred predictive target |
| foreign_population_growth_rate | Predictive | Target candidate | Requires at least two comparable time points | interval | rate | maybe log-difference or pct change | target candidate | second-choice predictive target |
| hotspot_emergence | Predictive | Target candidate | Requires multi-period hotspot definition | interval | binary class | none | target candidate | useful if continuous target is unstable |
| current_hotspot_class | Predictive | Temporary pilot target | Current cross-sectional clustering output | current baseline year | class | none | fallback only | not a true future forecast, only pipeline pilot |

## Variable decisions already fixed

### Fixed explanatory baseline variables
- foreign_ratio
- log_dist_to_station_m
- log_median_land_price_jpy

### First-round explanatory expansion variables
1. distance_to_central_tokyo
2. population_density
3. rental_housing_share if a clean municipal table can be assembled without delaying the paper too much

### First-round predictive target design priority
1. future_foreign_ratio
2. foreign_population_growth_rate
3. hotspot_emergence
4. current_hotspot_class only as a temporary pipeline test

## Immediate next actions by variable

### distance_to_central_tokyo
- derive directly from municipal centroid geometry
- no waiting for external source
- should be implemented first

### population_density
- check whether total population is already available in the merged municipal dataset
- if yes, derive density immediately
- if no, identify the minimal additional population table needed

### rental_housing_share
- do not block the explanatory paper on this variable
- only include in phase 1 if source harmonization is fast and clean

### future_foreign_ratio / growth_rate / hotspot_emergence
- first audit whether comparable multi-period foreign-population data can be assembled at the same municipal unit
- no RF/XGBoost training before this audit is complete