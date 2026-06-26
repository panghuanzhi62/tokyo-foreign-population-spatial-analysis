# Tokyo Project Handoff for New Chat

## What this file is for

Upload this file at the start of the new conversation in the same project so the new assistant can continue the work without re-deriving the full context.

This handoff is the operational source of truth for the current engineering and research state of the Tokyo foreign population project.

---

## Project identity

**Repository title**  
Spatial Concentration and Heterogeneous Mechanisms of Foreign Population Distribution in the Tokyo Metropolitan Mainland Area

**Repository purpose**  
A notebook-centered municipal-scale spatial analysis repository on foreign population concentration in the Tokyo metropolitan mainland area, framed as an academic/research portfolio and being upgraded into a more reproducible and reviewable research codebase.

---

## Non-negotiable project constraints

The new assistant must respect all of the following:

1. **Use this handoff as source of truth.**
2. **Notebook path-centralization is already done.**
3. **Notebook-to-module extraction is already completed through notebooks 00–08.**
4. **Reusable helpers already exist under `src/tokyo_foreigners/`.**
5. **`data_raw/` is canonical.**
6. **Do not propose migration to `data/raw/`.**
7. **Do not propose bulk notebook rewrite scripts.**
8. **Do not redo completed extraction work.**
9. **Preserve the notebook workflow.**
10. **Do not push the repo into premature Docker / PostGIS / Streamlit / app-layer expansion unless explicitly requested later.**

---

## Current repository engineering state

All of the following have already been completed on branch `agentic-upgrade`:

### Week 1 completed
- `uv` adopted as primary environment entry point
- `pyproject.toml` added
- `uv.lock` added
- `.venv` and Jupyter kernel confirmed usable
- smoke check for `src/tokyo_foreigners` confirmed

### Week 2 completed
- `ruff` added as minimal lint/format baseline
- formatting/linting limited to `src/tokyo_foreigners/` and related test scope
- no bulk notebook formatting

### Week 3 completed
- `pytest` added
- stable helper tests added
- minimal tests currently pass

### Week 4 completed
- lightweight GitHub Actions CI added
- CI runs:
  - `uv sync --locked`
  - `uv run ruff check src/tokyo_foreigners tests`
  - `uv run pytest -q`
- CI has already passed on GitHub

### Week 5 completed
- README refined
- `docs/refactor_status.md` added
- repository narrative and engineering status now better aligned with portfolio use

---

## Current branch / cleanliness status

At the last confirmed point:
- local and remote branch were synchronized
- working tree was clean
- recent work had been committed and pushed successfully

The new assistant should still ask the user to run `git status` before any new change round, but should assume the repo is in a healthy engineering state.

---

## Existing helper layer under `src/tokyo_foreigners/`

These modules already exist and should be treated as the current stable reusable layer:

- `paths.py`
- `boundaries.py`
- `station_accessibility.py`
- `land_price.py`
- `ols.py`
- `spatial_diagnostics.py`
- `mgwr.py`

The new assistant should build on these, not recreate them.

---

## Current substantive research baseline

### Current explanatory baseline
The project already supports the following claims:

- foreign population concentration is spatially clustered
- baseline OLS captures part of the relationship
- residual spatial autocorrelation remains
- MGWR reveals substantial local heterogeneity

### Current interpretation anchors
- **Kawaguchi**: concentration appears related to near-core accessibility and settlement capacity, not simply low land value
- **Edogawa**: higher land value does not straightforwardly suppress foreign concentration
- clusters should be interpreted as **land-system units** where demographic concentration, housing conditions, transport dependence, and environmental exposure may overlap

These interpretation anchors should be preserved unless later model expansion clearly weakens them.

---

## Current dual-track research structure

The project has already been reframed into **two parallel research tracks**.

### Track A: Explanatory
Goal:
- explain why foreign population concentration forms
- identify which variables matter
- explain why mechanisms vary across municipalities

Core logic:
- station accessibility + land value + local urban context
- baseline / expanded OLS
- residual Moran's I and LISA
- selected MGWR interpretation

### Track B: Predictive
Goal:
- forecast where foreign population concentration may intensify in the future
- later simulate possible spatial trajectories under different urban conditions

Core logic:
- municipality-level feature panel or multi-period dataset
- Random Forest / XGBoost prediction
- scenario-oriented spatial prediction
- possible CA-Markov / Logistic-CA-Markov extension
- much later, only if justified, agent-based / multi-agent extension

Important:
- predictive work should not start with full modeling before target definition and data audit
- multi-agent modeling is explicitly a later-stage extension, not the immediate next step

---

## Current planning documents that should now exist or be created/updated

These docs are part of the intended next-phase workflow:

- `docs/tokyo_dual_track_board.md`
- `docs/paper_questions.md`
- `docs/variable_log.md`
- `docs/results_log.md`
- `docs/baseline_snapshot.md`

The new assistant should assume these are the correct planning docs and continue using them.

---

## Current intended contents of those docs

### 1. `docs/tokyo_dual_track_board.md`
This should contain:
- full dual-track board
- explanatory backlog items EX-01 to EX-05
- predictive backlog items PR-01 to PR-07
- shared engineering board
- paper linkage map
- variable log template
- results log template
- weekly review template

Important:
In the earlier conversation, the user noticed incomplete copies that omitted later sections. The new assistant should verify that the file in the repo is the **full** version, not a truncated version.

### 2. `docs/paper_questions.md`
This should now describe:

**Explanatory paper**
- current baseline already established
- immediate expansion question: add a small set of urban-context variables
- phase-1 added variables:
  - `distance_to_central_tokyo`
  - `population_density`
  - `rental_housing_share` only if source harmonization is fast
- explanatory hypotheses H1–H4
- immediate explanatory outputs

**Predictive paper**
- current repo stronger as cross-sectional explanatory workflow than as a finished forecasting workflow
- immediate task is target-definition and data-availability audit
- phase-1 target candidates:
  - `future_foreign_ratio`
  - `foreign_population_growth_rate`
  - `hotspot_emergence`
  - fallback only: `current_hotspot_class`
- methods priority:
  - Random Forest
  - XGBoost
  - CA-Markov / Logistic-CA-Markov later
  - agent-based / multi-agent much later

### 3. `docs/variable_log.md`
This should be more complete than the user's earlier short version.
It should include at least:

Existing variables:
- `foreign_ratio`
- `log_dist_to_station_m`
- `log_median_land_price_jpy`
- `ols_resid`
- `lisa_cluster`

Added explanatory candidates:
- `distance_to_central_tokyo`
- `population_density`
- `rental_housing_share`

Predictive target candidates:
- `future_foreign_ratio`
- `foreign_population_growth_rate`
- `hotspot_emergence`
- `current_hotspot_class` (fallback only)

And it should include stronger status labels such as:
- `existing`
- `ready to derive`
- `candidate`
- `source-pending`
- `target candidate`
- `fallback only`

### 4. `docs/results_log.md`
This should already record:
- baseline explanatory findings
- Kawaguchi interpretation
- Edogawa interpretation
- land-system interpretation
- predictive line not yet target-fixed
- RF/XGBoost should wait until target definition and data audit are complete

### 5. `docs/baseline_snapshot.md`
This should freeze:
- current study focus
- baseline workflow
- current explanatory baseline variables
- current explanatory interpretation anchors
- current predictive baseline status (not yet target-fixed)
- current engineering baseline

The new assistant should preserve the idea that this file is a **freeze file**, not a daily note.

---

## The immediate next concrete work after docs

The earlier conversation narrowed the next steps to the following sequence.

### Step A: confirm / finalize the docs
Before any new modeling round, ensure these docs are complete and committed:
- `docs/tokyo_dual_track_board.md`
- `docs/paper_questions.md`
- `docs/variable_log.md`
- `docs/results_log.md`
- `docs/baseline_snapshot.md`

### Step B: create two new notebooks
The next real research work should start in two new notebooks:

1. `notebooks/09_extended_ols_variable_prep.ipynb`
2. `notebooks/11_prediction_target_design.ipynb`

### Step C: explanatory track first
The first real modeling-extension step should be explanatory, not predictive.

#### Highest-priority explanatory variable
Start with:
- `distance_to_central_tokyo`

Reason:
- easiest to derive
- no external table required
- directly relevant to the current Kawaguchi / near-core interpretation

#### Second explanatory variable
Try next:
- `population_density`

Reason:
- likely derivable if total population and geometry are already available or easily merged
- more practical than starting immediately with `rental_housing_share`

#### Third explanatory variable
Only if fast and clean:
- `rental_housing_share`

Rule:
- do not block the explanatory paper on this variable if harmonization is slow

### Step D: predictive track should only do target audit first
`11_prediction_target_design.ipynb` should not jump straight to RF/XGBoost.

It should first answer:
1. does the current repo only contain single-period foreign population data?
2. can comparable multi-period municipal foreign-population data be assembled?
3. what is the most realistic first predictive target?

Decision rule:
- if multi-period data exist → prefer `future_foreign_ratio` or `foreign_population_growth_rate`
- if multi-period data do not yet exist → do not pretend to do a true future forecast; at most define a pilot classification target like `current_hotspot_class`

---

## Concrete implementation priorities for the next assistant

The next assistant should proceed in this order:

1. verify docs completeness
2. verify working tree clean (`git status`)
3. verify CI baseline still green locally:
   - `uv sync --locked`
   - `uv run ruff check src/tokyo_foreigners tests`
   - `uv run pytest -q`
4. create / populate:
   - `notebooks/09_extended_ols_variable_prep.ipynb`
   - `notebooks/11_prediction_target_design.ipynb`
5. implement `distance_to_central_tokyo`
6. check whether `population_density` can be derived from existing merged data
7. audit predictive target feasibility before any RF/XGBoost training
8. append results to `docs/results_log.md`
9. only after a step proves reusable, consider helper extraction into `src/`

---

## What the next assistant should NOT do

The next assistant should not:
- suggest `data_raw/` → `data/raw/` migration
- propose bulk notebook rewrite scripts
- redo 00–08 extraction
- push Docker / PostGIS / Streamlit / app-layer expansion unless explicitly requested
- start RF/XGBoost before target-definition audit
- jump to agent-based / multi-agent modeling as the immediate next step
- change the project into a fully packaged pipeline
- erase or overwrite the existing notebook-centered workflow

---

## Standing engineering operating rule

For every meaningful research increment, also produce:

1. one data increment
2. one engineering increment
3. one result increment
4. one writing increment

In practice, every new round should generate:
- a new variable / dataset / model
- a helper update or test update if reusable logic appears
- at least one figure or table
- a short memo paragraph for future paper writing

And every round should end with:

```bash
uv sync --locked
uv run ruff check src/tokyo_foreigners tests
uv run pytest -q
git status
```

---

## Best starter prompt for the new chat

Use something close to this after uploading this handoff file:

> Please use this handoff file as the source of truth. Continue the Tokyo project from the current state without redoing completed extraction or changing the canonical `data_raw/` policy. First verify whether `docs/tokyo_dual_track_board.md`, `docs/paper_questions.md`, `docs/variable_log.md`, `docs/results_log.md`, and `docs/baseline_snapshot.md` are complete and aligned with the handoff. Then guide me through the next concrete step: creating `notebooks/09_extended_ols_variable_prep.ipynb` and implementing `distance_to_central_tokyo` as the first added explanatory variable.

---

## Even better option than uploading this file

If convenient, do both:
1. upload this handoff file to the new chat
2. also say in the first message:
   - branch: `agentic-upgrade`
   - engineering baseline through Week 5 is complete
   - the next concrete work is docs verification + `09_extended_ols_variable_prep.ipynb` + `11_prediction_target_design.ipynb`

That will reduce ambiguity further.
