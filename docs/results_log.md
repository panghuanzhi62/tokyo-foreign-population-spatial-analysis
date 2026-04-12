# Results Log

| Date | Track | Notebook / Script | Model | Main finding | Candidate for | Follow-up |
|---|---|---|---|---|---|---|
| 2026-04-11 | Explanatory | baseline workflow (00–08) | baseline OLS + Moran/LISA + MGWR | Foreign population concentration is spatially clustered; baseline OLS explains part of the pattern but residual spatial structure remains; MGWR indicates local heterogeneity. | main text | use as fixed baseline for all expanded-model comparison |
| 2026-04-11 | Explanatory | current interpretation stage | discussion memo | Kawaguchi cannot be reduced to a low-land-value story; concentration there appears to reflect near-core accessibility and settlement capacity. | main text | preserve this as a current interpretation anchor when new variables are added |
| 2026-04-11 | Explanatory | current interpretation stage | discussion memo | Edogawa cannot be reduced to a simple cost-exclusion story; higher land value does not straightforwardly suppress foreign concentration. | main text | preserve this as a second interpretation anchor when model expansion changes coefficients |
| 2026-04-11 | Explanatory | current interpretation stage | discussion memo | Clustered municipalities should be interpreted as land-system units where demographic concentration, housing, transport dependence, and environmental exposure may overlap. | main text / discussion | connect later explanatory expansion to socio-environmental variables |
| 2026-04-11 | Predictive | planning stage | target design | Prediction target is not yet fixed; current repository is stronger as a cross-sectional explanatory workflow than as a finished forecasting workflow. | methods note | first complete target-definition and data-availability audit |
| 2026-04-11 | Predictive | planning stage | methods design | Random Forest / XGBoost should begin only after a municipality-level future target is defined; CA-Markov and agent-based extensions are later-stage methods. | methods note / future work | keep predictive line staged rather than jumping to full simulation |
| 2026-04-12 | Explanatory | 09_extended_ols_variable_prep.ipynb | variable derivation | `distance_to_central_tokyo` was successfully derived from municipal centroid distance to Tokyo Station using the existing municipal geometry. | appendix / methods note | retain as the first confirmed urban-context extension variable |
| 2026-04-12 | Explanatory | 09_extended_ols_variable_prep.ipynb | extended OLS (baseline + centrality) | `log_distance_to_central_tokyo` shows a clear negative and statistically significant association with `foreign_ratio`, indicating that relative position within the metropolitan core-periphery structure matters beyond the baseline specification. | main text | keep this variable in the next explanatory specification and reflect it in README / project memo |
| 2026-04-12 | Explanatory | 09_extended_ols_variable_prep.ipynb | case interpretation memo | The new centrality result strengthens the current reading that Kawaguchi and Edogawa should not be interpreted through a simple low-cost or cost-exclusion story, but through near-core metropolitan position and broader urban opportunity structure. | main text / discussion | preserve as an updated interpretation anchor in later write-up |
| 2026-04-12 | Explanatory | 09_extended_ols_variable_prep.ipynb | data validation | `tokyo_pop_dissolved.geojson` was successfully merged back to the MGWR-ready municipal layer; `total_pop`, `foreign_pop`, and recomputed `foreign_ratio` aligned exactly with the existing ratio field. | appendix / methods note | use this as the validated source for any later population-based extensions |
| 2026-04-12 | Explanatory | 09_extended_ols_variable_prep.ipynb | variable derivation | `population_density` was successfully derived from `total_pop` and municipal area using existing merged data. | appendix | keep as a tested candidate variable |
| 2026-04-12 | Explanatory | 09_extended_ols_variable_prep.ipynb | extended OLS (baseline + centrality + density) | `log_population_density` did not show a statistically significant independent association and produced negligible model improvement; it should not be promoted to the current core explanatory specification. | dropped result / internal record | keep documented, but do not make it part of the current headline explanatory story |
| 2026-04-12 | Explanatory | 09_extended_ols_variable_prep.ipynb | model comparison memo | After adding both centrality and density, the explanatory story is better framed as a metropolitan structure story rather than a simple accessibility-plus-cost story; centrality remains stable while density does not materially strengthen the specification. | main text / discussion | next priority is consolidation of outputs and write-up, not mechanical variable accumulation |
| 2026-04-12 | Predictive | 11_prediction_target_design.ipynb | target audit stage | Predictive work remains at the audit stage; no genuine future target should be claimed until multi-period municipal foreign-population data are confirmed to be comparable and available. | methods note | complete data inventory and target-feasibility judgment before any RF/XGBoost work |

---

## How to use this log

For every real research increment, append one new row.

### Append when:
- a new explanatory variable is added
- an expanded OLS is estimated
- residual Moran / LISA changes
- a MGWR extension is run
- a predictive target is fixed
- a RF / XGBoost baseline is trained
- a new figure or table becomes candidate for the paper
- a robustness result materially strengthens or weakens the current narrative

### Do not append when:
- you only did code cleanup with no research result
- you only rearranged notebook cells without producing a new finding
- you only changed formatting, comments, or filenames

---

## Result entry template

| Date | Track | Notebook / Script | Model | Main finding | Candidate for | Follow-up |
|---|---|---|---|---|---|---|

---

## Interpretation rule

### main text
Use this label only when the result:
- materially advances the paper argument
- changes the explanatory or predictive narrative
- is likely to appear in the final Results or Discussion section

### appendix
Use this label when the result:
- is useful for robustness
- supports but does not drive the main argument
- documents alternative specifications or sensitivity checks

### dropped result
Use this label when the result:
- is not stable
- is not theoretically interpretable
- does not improve the paper
- may still be worth keeping as internal record, but should not shape the narrative

---

## Immediate next entries expected

The next few rows should most likely record:
1. whether the README / portfolio note was updated to reflect the centrality finding
2. whether a new figure or coefficient table from Round 09 becomes paper-candidate material
3. whether expanded residual Moran's I is tested after the new explanatory specification
4. whether `rental_housing_share` is added or deliberately deferred
5. whether multi-period foreign-population data can support a genuine future target in notebook 11