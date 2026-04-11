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
- Research question:
- This week's task:
- Why now:
- Expected paper contribution:
- Status: Not started / In progress / Blocked / Done

### Predictive track
- Research question:
- This week's task:
- Why now:
- Expected paper contribution:
- Status: Not started / In progress / Blocked / Done

### Shared engineering layer
- This week's engineering task:
- Why needed for reproducibility:
- Affected files:
- Status: Not started / In progress / Blocked / Done

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