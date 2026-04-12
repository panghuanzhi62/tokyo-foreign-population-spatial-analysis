# Variable Log

| Variable | Track | Role | Source | Year | Unit | Transformation | Status | Notes |
|---|---|---|---|---|---|---|---|---|
| foreign_ratio | Explanatory / Predictive | Response / target candidate | Existing Tokyo repo municipal foreign-population dataset | current baseline year | ratio | none | existing | current dependent variable in baseline explanatory workflow |
| log_dist_to_station_m | Explanatory / Predictive | Predictor | Existing station accessibility pipeline | current baseline year | meters | log | existing | current station accessibility variable |
| log_median_land_price_jpy | Explanatory / Predictive | Predictor | Existing land-price integration pipeline | current baseline year | JPY | log | existing | current land-value variable |
| ols_resid | Explanatory | Diagnostic | derived from baseline OLS | current baseline year | residual | none | existing | used in Moran / LISA diagnostics |
| lisa_cluster | Explanatory | Diagnostic / interpretation | derived from Local Moran | current baseline year | class | none | existing | used for cluster interpretation and MGWR-ready export |
| distance_to_central_tokyo | Explanatory / Predictive | Added predictor candidate | Derived from municipal centroid distance to Tokyo Station using existing municipal geometry | current baseline year | km | log available | derived / retained | first confirmed urban-context extension variable; strong and stable negative association in extended OLS |
| population_density | Explanatory / Predictive | Added predictor candidate | Derived from `total_pop` in `tokyo_pop_dissolved.geojson` and municipal area from geometry | current baseline year | persons per km² | log tested | derived / tested candidate | successfully derived from existing merged data, but not retained in current core explanatory specification |
| rental_housing_share | Explanatory / Predictive | Added predictor candidate | External housing statistics table to be harmonized to municipality | current baseline year | share | none | source-pending | settlement capacity / housing structure variable |
| future_foreign_ratio | Predictive | Preferred target | Requires at least two comparable time points | t+1 | ratio | none | target candidate | preferred predictive target if comparable multi-period municipal data can be assembled |
| foreign_population_growth_rate | Predictive | Target candidate | Requires at least two comparable time points | interval | rate | maybe log-difference or pct change | target candidate | second-choice predictive target |
| hotspot_emergence | Predictive | Target candidate | Requires multi-period hotspot definition | interval | binary class | none | target candidate | useful if continuous target is unstable |
| current_hotspot_class | Predictive | Temporary pilot target | Current cross-sectional clustering output | current baseline year | class | none | fallback only | not a true future forecast; only a temporary pipeline pilot if multi-period data are unavailable |

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

## Current post-test decisions

### distance_to_central_tokyo
- derived successfully from existing municipal geometry
- no external source required
- retained as the first confirmed urban-context extension variable
- should remain in the next explanatory specification

### population_density
- derived successfully by merging `tokyo_pop_dissolved.geojson` back to the MGWR-ready municipal layer
- total population and foreign population aligned exactly with the existing `foreign_ratio`
- tested in the extended specification using `log_population_density`
- not retained in the current core explanatory specification because the independent contribution is weak and model improvement is negligible

### rental_housing_share
- still not ready
- do not block the explanatory paper on this variable
- include only if source harmonization is fast and clean

### future_foreign_ratio / growth_rate / hotspot_emergence
- still require target-definition and data-availability audit
- no RF/XGBoost training before this audit is complete

## Immediate next actions by variable

### distance_to_central_tokyo
- keep in the explanatory track
- use in the next round of interpretation and portfolio-facing write-up
- consider helper extraction into `src/` only if the same derivation proves reusable across later notebooks

### population_density
- keep as a documented tested candidate
- do not promote to the current core explanatory model
- revisit only if later model restructuring or additional urban-context variables make density more interpretable

### rental_housing_share
- identify the lightest possible municipal-level source
- stop immediately if harmonization becomes slow or messy

### future_foreign_ratio / foreign_population_growth_rate / hotspot_emergence
- complete data audit in `11_prediction_target_design.ipynb`
- determine whether the current repo has only single-period foreign-population data
- only after target feasibility is confirmed should predictive modeling begin