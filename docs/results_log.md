# Results Log

| Date | Track | Notebook / Script | Model | Main finding | Candidate for | Follow-up |
|---|---|---|---|---|---|---|
| 2026-04-11 | Explanatory | baseline workflow (00–08) | baseline OLS + Moran/LISA + MGWR | Foreign population concentration is spatially clustered; baseline OLS explains part of the pattern but residual spatial structure remains; MGWR indicates local heterogeneity. | main text | use as fixed baseline for all expanded-model comparison |
| 2026-04-11 | Explanatory | current interpretation stage | discussion memo | Kawaguchi cannot be reduced to a low-land-value story; Edogawa cannot be reduced to a simple cost-exclusion story. | main text | preserve this as the current interpretation anchor when new variables are added |
| 2026-04-11 | Explanatory | current interpretation stage | discussion memo | Clustered areas should be interpreted as land-system units where demographic concentration, housing, transport dependence, and environmental exposure may overlap. | main text / discussion | link future explanatory expansion to socio-environmental variables |
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

### Do not append when:
- you only did code cleanup with no research result
- you only rearranged notebook cells without producing a new finding