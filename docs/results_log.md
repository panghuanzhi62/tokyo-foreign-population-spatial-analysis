# Results Log

| Date | Track | Notebook / Script | Model | Main finding | Candidate for | Follow-up |
|---|---|---|---|---|---|---|
| 2026-04-11 | Explanatory | baseline workflow (00–08) | baseline OLS + Moran/LISA + MGWR | Foreign population concentration is spatially clustered; baseline OLS explains part of the pattern but residual spatial structure remains; MGWR indicates local heterogeneity. | main text | use as fixed baseline for all expanded-model comparison |
| 2026-04-11 | Explanatory | current interpretation stage | discussion memo | Kawaguchi cannot be reduced to a low-land-value story; concentration there appears to reflect near-core accessibility and settlement capacity. | main text | preserve this as a current interpretation anchor when new variables are added |
| 2026-04-11 | Explanatory | current interpretation stage | discussion memo | Edogawa cannot be reduced to a simple cost-exclusion story; higher land value does not straightforwardly suppress foreign concentration. | main text | preserve this as a second interpretation anchor when model expansion changes coefficients |
| 2026-04-11 | Explanatory | current interpretation stage | discussion memo | Clustered municipalities should be interpreted as land-system units where demographic concentration, housing, transport dependence, and environmental exposure may overlap. | main text / discussion | connect later explanatory expansion to socio-environmental variables |
| 2026-04-11 | Predictive | planning stage | target design | Prediction target is not yet fixed; current repository is stronger as a cross-sectional explanatory workflow than as a finished forecasting workflow. | methods note | first complete target-definition and data-availability audit |
| 2026-04-11 | Predictive | planning stage | methods design | Random Forest / XGBoost should begin only after a municipality-level future target is defined; CA-Markov and agent-based extensions are later-stage methods. | methods note / future work | keep predictive line staged rather than jumping to full simulation |

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
1. whether `distance_to_central_tokyo` was successfully derived
2. whether `population_density` was added or delayed
3. whether the expanded OLS improves on the baseline
4. whether residual Moran's I decreases after model expansion
5. whether multi-period foreign-population data can support a genuine future target