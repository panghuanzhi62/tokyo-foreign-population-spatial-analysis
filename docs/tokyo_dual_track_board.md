# Tokyo Foreign Population Project: Dual-Track Research Board

## 0. Project framing

This project now advances along two parallel research tracks.

### Track A: Explanatory
Goal: explain why foreign population concentration forms, which factors matter, and why mechanisms vary across municipalities.

Core logic:  
station accessibility + land value + local urban context  
→ baseline / expanded OLS  
→ residual Moran's I and LISA  
→ selected MGWR interpretation

### Track B: Predictive
Goal: forecast where foreign population concentration may intensify in the future, and simulate possible spatial trajectories under different urban conditions.

Core logic:  
municipal feature panel or multi-period dataset  
→ Random Forest / XGBoost prediction  
→ scenario-oriented spatial prediction  
→ possible CA-Markov / Logistic-CA-Markov extension  
→ later agent-based / multi-agent extension if justified

---

## 1. Operating rule

For every meaningful research increment, produce all of the following:

1. one data increment  
2. one engineering increment  
3. one result increment  
4. one writing increment  

That means each round should generate:

- a new variable / dataset / model
- a helper update or test update
- at least one table or figure
- a short memo paragraph for the future paper draft

---

## 2. Weekly board overview

## This week

### Explanatory track
- Research question: Does adding a small set of urban-context variables improve the current explanation of foreign population concentration?
- This week's task: define and collect 2–3 additional municipality-level variables for expanded OLS
- Why now: the current repo already has a stable baseline OLS → Moran/LISA → MGWR workflow
- Expected paper contribution: move from a two-variable baseline toward a more paper-ready explanatory model
- Status: In progress

### Predictive track
- Research question: What should the first prediction target be for future foreign population concentration?
- This week's task: define prediction target candidates and data requirements
- Why now: prediction should begin with a clear target definition before model training
- Expected paper contribution: establish the design logic for a future RF/XGBoost forecasting paper
- Status: In progress

### Shared engineering layer
- This week's engineering task: document new variables and keep all additions aligned with helper/test/doc structure
- Why needed for reproducibility: research additions should not remain notebook-only
- Affected files:
  - docs/paper_questions.md
  - docs/variable_log.md
  - docs/results_log.md
  - docs/baseline_snapshot.md
- Status: In progress

---

## 3. Task register template

### Task ID
- ID:
- Date opened:
- Track: Explanatory / Predictive / Shared engineering
- Priority: High / Medium / Low
- Owner:
- Status: Backlog / Ready / In progress / Review / Done

### Research aim
- Question this task answers:
- Hypothesis or expectation:
- Why it matters for the paper:

### Data work
- New variable(s):
- Source(s):
- Temporal scope:
- Spatial unit:
- Cleaning / harmonization needed:
- Output dataset or file:

### Model work
- Model/notebook involved:
- Baseline comparison target:
- New specification:
- Key metric(s) to compare:
- Expected risks:

### Engineering work
- Helper to add or modify:
- Test to add or update:
- Command(s) to run:

```bash
uv sync --locked
uv run ruff check src/tokyo_foreigners tests
uv run pytest -q
git status
```

### Outputs
- Figure(s) expected:
- Table(s) expected:
- Output path(s):
- Whether candidate for main text or appendix:

### Writing linkage
- Paper section affected:
  - Introduction / Data / Methods / Results / Discussion / Appendix
- Paragraph to draft:
- Key sentence or claim to test:

### Completion check
- What counts as done:
- What would invalidate the result:
- Next dependent task:

---

## 4. Explanatory track board

## A. Current explanatory paper question
How do station accessibility, land value, and additional local urban-context variables jointly shape the spatial concentration of foreign residents across municipalities in the Tokyo metropolitan mainland area?

## B. Current explanatory narrative anchor
- foreign population concentration is spatially clustered
- baseline OLS captures part of the relationship
- residual spatial autocorrelation remains
- MGWR reveals local heterogeneity
- Kawaguchi and Edogawa indicate that simple cost-only explanations are insufficient

## C. Explanatory backlog

### EX-01 Expand OLS with new urban-context variables
- This week's task:
  - choose 2–3 added variables
  - identify data sources
  - define harmonization rules
  - prepare a first expanded OLS-ready dataset
- Candidate variables:
  - population density
  - distance to central Tokyo
  - rental housing share
- Output:
  - expanded OLS-ready table
  - variable dictionary update
  - one short model design memo
- Helper:
  - `ols.py`
  - possible new data-prep helper
- Paper section:
  - Methods
  - Results

### EX-02 Re-run residual Moran's I and LISA after expanded OLS
- This week's task:
- Output:
  - updated residual Moran result
  - updated LISA cluster map
- Helper:
  - `spatial_diagnostics.py`
- Paper section:
  - Results
  - Discussion

### EX-03 Select one added variable for MGWR extension
- This week's task:
- Selection rationale:
  - strongest theoretical meaning
  - spatially plausible heterogeneity
  - not just a generic control
- Output:
  - local coefficient map
  - short interpretation note
- Helper:
  - `mgwr.py`
- Paper section:
  - Results
  - Discussion

### EX-04 Case-based interpretation memo
- This week's task:
- Focus areas:
  - Kawaguchi
  - Edogawa
  - eastern inner metropolitan municipalities
- Output:
  - one discussion memo
- Helper:
  - none required unless a reusable extraction step appears
- Paper section:
  - Discussion

### EX-05 Robustness check block
- This week's task:
- Robustness types:
  - alternative accessibility measure
  - alternative land-price transformation
  - sample sensitivity
- Output:
  - appendix table
  - appendix note
- Helper:
  - `ols.py`
  - `spatial_diagnostics.py`
- Paper section:
  - Appendix
  - Limitations

---

## 5. Predictive track board

## A. Current predictive paper question
Can municipality-level urban, accessibility, and land-related features help predict future foreign population concentration or concentration growth patterns in metropolitan Tokyo?

## B. Current predictive narrative anchor
- current explanatory model identifies plausible drivers
- next step is to test whether these and additional features improve predictive performance
- prediction should begin with municipality-level supervised learning before moving to scenario simulation

## C. Predictive backlog

### PR-01 Build prediction-ready dataset
- This week's task:
  - define candidate prediction targets
  - list required multi-period variables
  - assess whether current data are cross-sectional only or can support temporal prediction
- Prediction target candidates:
  - future_foreign_ratio
  - foreign_population_growth
  - hotspot_emergence
- Output:
  - target definition note
  - prediction data requirements note
- Helper:
  - likely a new dataset-prep helper
- Paper section:
  - Data
  - Methods

### PR-02 Random Forest baseline
- This week's task:
- Output:
  - baseline RF performance table
  - feature importance figure
- Helper:
  - possible new `prediction.py`
- Paper section:
  - Methods
  - Results

### PR-03 XGBoost comparison
- This week's task:
- Output:
  - model comparison table
  - error summary
- Helper:
  - `prediction.py` or notebook-first prototype
- Paper section:
  - Results

### PR-04 Spatial error diagnosis of predictions
- This week's task:
- Questions:
  - where are large prediction errors clustered?
  - which municipalities are systematically underpredicted?
- Output:
  - prediction error map
  - high-error municipality list
- Helper:
  - possible diagnostics helper
- Paper section:
  - Results
  - Discussion

### PR-05 Scenario simulation extension
- This week's task:
- Scenario type:
  - accessibility improvement
  - housing-market change
  - vulnerability exposure change
- Output:
  - scenario comparison figure
  - scenario assumptions note
- Helper:
  - possible simulation helper
- Paper section:
  - Discussion
  - Future research

### PR-06 Dynamic simulation extension
- This week's task:
- Candidate methods:
  - CA-Markov
  - Logistic-CA-Markov
- Preconditions:
  - multi-period data
  - stable transition logic
- Output:
  - simulation workflow note
  - feasibility memo
- Helper:
  - future module, not mandatory now
- Paper section:
  - Future work / second paper design

### PR-07 Agent-based extension (longer-term)
- This week's task:
- Research purpose:
  - mechanism-oriented scenario simulation
- Preconditions:
  - behavior rules clearly specified
  - prior explanatory and predictive findings stabilized
- Output:
  - conceptual design only
- Helper:
  - none for now
- Paper section:
  - Future agenda only

---

## 6. Shared engineering board

### ENG-01 Keep helper layer stable
- Target:
  - avoid breaking `src/tokyo_foreigners/`
- Files:
  - `paths.py`
  - `boundaries.py`
  - `station_accessibility.py`
  - `land_price.py`
  - `ols.py`
  - `spatial_diagnostics.py`
  - `mgwr.py`
- Done when:
  - new research additions do not silently break existing workflow

### ENG-02 Add small tests whenever a reusable step is added
- Rule:
  - every stable helper addition should get at least one small pytest
- Output:
  - tests under `tests/`

### ENG-03 Keep outputs fixed and reusable
- Rule:
  - every result intended for paper discussion must be exported to `outputs/figures/` or `outputs/tables/`
- Avoid:
  - results that exist only inside notebook cell outputs

### ENG-04 Update docs with each meaningful change
- Files to update when needed:
  - `README.md`
  - `docs/refactor_status.md`
  - `docs/paper_questions.md`
  - `docs/variable_log.md`
  - `docs/results_log.md`
  - `docs/baseline_snapshot.md`

### ENG-05 Keep CI green
- Weekly command checklist:

```bash
uv sync --locked
uv run ruff check src/tokyo_foreigners tests
uv run pytest -q
git status
```

---

## 7. Paper linkage map

## Explanatory paper

### Introduction
- Why foreign population concentration matters in metropolitan Tokyo
- Why station accessibility and land value alone may not fully explain clustering
- Why local urban context and spatial heterogeneity matter

### Data and Methods
- municipal dataset construction
- station accessibility variables
- land-price integration
- added urban-context variables
- baseline OLS
- Moran's I / LISA
- MGWR

### Results
- baseline OLS
- expanded OLS
- residual Moran / LISA
- selected MGWR findings
- Kawaguchi / Edogawa interpretation

### Discussion
- local mechanism differences
- why cost-only narratives are insufficient
- land-system and socio-environmental implications

### Appendix
- robustness checks
- alternative specifications
- extra figures

## Predictive paper

### Introduction
- why explanation alone is insufficient
- why future concentration forecasting matters for planning and policy

### Data and Methods
- target construction
- feature set
- train/test strategy
- Random Forest / XGBoost
- evaluation metrics
- later scenario simulation design

### Results
- prediction performance
- feature importance
- error geography
- scenario contrasts if available

### Discussion
- predictive drivers vs explanatory drivers
- where uncertainty remains
- planning implications

---

## 8. Variable log template

### Variable name
- Name:
- Track used in:
- Theoretical role:
- Source:
- Year:
- Unit:
- Expected sign or role:
- Transformation:
- Missing-data handling:
- Used in which notebook / helper:
- Used in which paper section:

---

## 9. Results log template

### Result entry
- Date:
- Track:
- Notebook / script:
- Model:
- Main finding:
- Does it strengthen or weaken the main narrative?
- Candidate for:
  - main text
  - appendix
  - dropped result
- Follow-up action:

---

## 10. Weekly review template

## End-of-week review

### Explanatory track
- What was completed:
- What changed in the paper narrative:
- What remains unclear:

### Predictive track
- What was completed:
- What changed in the prediction design:
- What remains unclear:

### Engineering layer
- What helper/test/doc was added:
- Did CI remain green:
- Any fragile parts discovered:

### Next week
- One main task:
- One supporting engineering task:
- One expected figure or table:
- One paragraph to draft: