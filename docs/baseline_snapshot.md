# Baseline Snapshot

## Purpose
This file freezes the current Tokyo project baseline before explanatory expansion and predictive-track development.

It should not be edited every day.  
It should only be updated when the project baseline itself changes in a meaningful way.

---

## Current repository baseline

### Study focus
The current Tokyo project examines whether foreign population concentration in the Tokyo metropolitan mainland area is spatially clustered and whether its association with station accessibility and residential land price is globally stable or locally heterogeneous.

### Study area
- mainland Tokyo metropolitan area
- outlying islands excluded to avoid distortion in accessibility and distance-based measures

### Analytical unit
- municipality-level spatial unit

### Current baseline data categories
- administrative boundaries
- foreign population statistics
- railway station data
- official residential land-price data

### Current baseline workflow
1. boundary processing
2. population merge
3. station accessibility feature engineering
4. exploratory spatial analysis
5. land-price integration
6. baseline OLS
7. residual Moran's I / LISA
8. MGWR

---

## Current explanatory baseline

### Response
- `foreign_ratio`

### Core predictors
- `log_dist_to_station_m`
- `log_median_land_price_jpy`

### Diagnostic variables already in workflow
- `ols_resid`
- `lisa_cluster`

### Current explanatory position
The current project already demonstrates that:
- foreign population concentration is spatially clustered
- baseline OLS captures a meaningful global relationship
- residual spatial autocorrelation remains
- MGWR reveals substantial local heterogeneity

### Current municipality-level interpretation anchors
- Kawaguchi suggests near-core accessibility and settlement capacity rather than a simple low-land-value explanation
- Edogawa suggests that higher land value does not straightforwardly suppress foreign concentration
- clustered municipalities should be interpreted as land-system units where demographic concentration, housing conditions, transport dependence, and environmental exposure may overlap

---

## Current predictive baseline

### Current status
The predictive line is conceptually justified but not yet operationalized as a full forecasting workflow.

### What already exists
- a municipality-level feature structure built for explanatory modeling
- spatially meaningful accessibility and land-related variables
- a reproducible analysis architecture suitable for later predictive extension

### What does not yet exist as a stable baseline
- a finalized future prediction target
- a confirmed multi-period foreign-population panel
- a finished RF / XGBoost benchmark
- a simulation-ready transition framework

### Current predictive rule
No full predictive modeling should be treated as part of the project baseline until:
1. a municipality-level future target is fixed
2. comparable multi-period data are confirmed
3. the first prediction-ready dataset is assembled

---

## Current engineering baseline

### Environment and workflow
- `uv` is the primary environment entry point
- `pyproject.toml` and `uv.lock` are in place
- notebooks remain the reference orchestration layer
- reusable helpers are under `src/tokyo_foreigners/`

### Quality baseline
- `ruff` checks pass for `src/tokyo_foreigners/`
- `pytest` passes for the current stable test set
- GitHub Actions CI runs lint + tests

### Documentation baseline
- README has been refined to reflect the notebook-centered workflow and current engineering state
- `docs/refactor_status.md` records engineering hardening
- the dual-track board and related planning docs define the next research phase

---

## Immediate comparison baseline for next phase

### Explanatory next-phase comparison
All expanded OLS and post-OLS diagnostics should be compared against:
- response: `foreign_ratio`
- predictors:
  - `log_dist_to_station_m`
  - `log_median_land_price_jpy`

### Predictive next-phase comparison
The immediate predictive baseline is not a trained model, but the current explanatory dataset structure plus the present absence of a finalized future target.

That means the first predictive contribution should be judged against:
- clarity of target definition
- feasibility of multi-period data assembly
- readiness of a prediction-oriented feature table

---

## Freeze rule

Update this file only when one of the following happens:
- the baseline explanatory variable set changes
- the baseline workflow changes materially
- the predictive line obtains a confirmed future target and prediction-ready baseline dataset
- the project interpretation anchor changes in a major way