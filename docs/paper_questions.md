# Paper Questions

## Explanatory paper

### Working title
Spatial Concentration, Accessibility, Land Value, and Local Urban Context in the Foreign Population Geography of Metropolitan Tokyo

### Main question
How do station accessibility, land value, and additional local urban-context variables jointly shape the spatial concentration of foreign residents across municipalities in the Tokyo metropolitan mainland area?

### Why this paper is needed
The current Tokyo project already establishes that foreign population concentration is spatially clustered, that a baseline OLS model captures part of the relationship, that residual spatial autocorrelation remains, and that MGWR reveals substantial local heterogeneity. The next paper-stage step is therefore not to repeat the baseline, but to test whether adding a small set of theoretically meaningful urban-context variables improves explanatory power and sharpens local interpretation.

### Current baseline already established
- Study area: mainland Tokyo metropolitan area, excluding outlying islands
- Analytical unit: municipality-level spatial unit
- Existing workflow:
  - boundary processing
  - population merge
  - station accessibility feature engineering
  - exploratory spatial analysis
  - land-price integration
  - baseline OLS
  - residual Moran's I / LISA
  - MGWR
- Current baseline explanatory variables:
  - `foreign_ratio`
  - `log_dist_to_station_m`
  - `log_median_land_price_jpy`

### Current interpretation anchor
- Foreign population concentration is spatially clustered rather than randomly distributed.
- Kawaguchi suggests that concentration is supported by near-core accessibility and settlement capacity rather than by low land value alone.
- Edogawa suggests that higher land value does not straightforwardly suppress foreign concentration.
- Clustered municipalities should be interpreted as land-system units in which demographic concentration, housing conditions, transport dependence, and environmental exposure may overlap.

### Immediate explanatory expansion question
Does adding a small set of urban-context variables improve model fit, reduce residual spatial autocorrelation, and produce a more defensible paper narrative?

### Phase-1 added variables
1. `distance_to_central_tokyo`
2. `population_density`
3. `rental_housing_share` (only if source harmonization is fast and clean)

### Why these variables
- `distance_to_central_tokyo` separates near-core location from simple nearest-station accessibility.
- `population_density` captures urban scale / built-up intensity.
- `rental_housing_share` captures settlement capacity and housing structure.

### Hypotheses
- H1: Adding urban-context variables will improve explanatory power relative to the two-variable baseline.
- H2: Residual Moran's I should decrease, but not disappear completely.
- H3: Some local heterogeneity will remain, especially in municipalities such as Kawaguchi and Edogawa.
- H4: The explanatory story will shift from a simple accessibility + land-value account toward a broader land-system and local urban-context interpretation.

### Immediate explanatory outputs
- one expanded OLS comparison table
- one updated residual Moran / LISA result
- one variable-selection memo for MGWR extension
- one discussion note on Kawaguchi / Edogawa after model expansion

### What would count as a paper-quality gain
- clearer theoretical justification for added variables
- measurable improvement over the baseline model
- stronger discussion of local mechanism differences
- a more convincing bridge from empirical pattern to policy-relevant interpretation

---

## Predictive paper

### Working title
Forecasting Future Foreign Population Concentration in Metropolitan Tokyo Using Municipality-Level Spatial Features

### Main question
Can municipality-level accessibility, land-related, and urban-context features help predict future foreign population concentration or concentration growth patterns in metropolitan Tokyo?

### Why this paper is needed
The explanatory paper answers why concentration forms and varies locally. The predictive paper should answer where concentration is likely to intensify next, which municipalities are most likely to grow as concentration areas, and which feature sets have practical predictive value for planning and policy discussion.

### Current predictive reality check
The present repository is strong as a cross-sectional explanatory workflow. It is not yet a finished multi-period forecasting workflow. Therefore, the first predictive task is not model training, but target design and data-availability audit.

### Immediate predictive design question
Which prediction target is most feasible given the data that can realistically be assembled in the near term?

### Phase-1 target candidates
1. `future_foreign_ratio` (preferred if at least two comparable time points can be assembled)
2. `foreign_population_growth_rate`
3. `hotspot_emergence`
4. fallback if multi-period assembly is delayed:
   `current_hotspot_class` as a methodological pilot rather than a true future forecast

### Priority order
- first priority: future continuous target
- second priority: growth rate
- third priority: hotspot emergence
- temporary fallback: current class prediction for pipeline testing only

### Candidate methods in order
1. Random Forest
2. XGBoost
3. CA-Markov / Logistic-CA-Markov (after target and transition logic stabilize)
4. Agent-based / multi-agent extension only after explanatory and predictive foundations become stable

### Predictive hypotheses
- P1: A broader urban-context feature set will outperform a simple two-feature baseline for prediction.
- P2: Accessibility and land-related variables will remain important, but predictive importance may differ from explanatory significance.
- P3: Prediction errors will also have geography, revealing municipalities whose dynamics are not captured well by standard feature sets.
- P4: A future forecasting paper should begin with municipality-level supervised learning before moving to scenario simulation.

### Immediate predictive outputs
- one target-definition memo
- one data-availability audit note
- one first-stage prediction-ready dataset design

### What would count as a paper-quality gain
- a clearly justified prediction target
- transparent feature-set design
- defensible train/test logic
- interpretable predictive output, not just a black-box score
- a clear distinction between prediction and explanation