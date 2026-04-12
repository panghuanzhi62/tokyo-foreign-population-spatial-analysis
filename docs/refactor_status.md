# Refactor Status

## Current repository position

This repository remains notebook-centered by design.

- The notebooks are still the reference orchestration and interpretation layer.
- Reusable helper logic has been extracted into `src/tokyo_foreigners/`.
- `data_raw/` remains the canonical raw-data directory.
- The current engineering goal is reproducibility and maintainability, not platformization.

## Completed engineering hardening

### Week 1
- Added `pyproject.toml`
- Added `uv.lock`
- Switched the primary environment entry point to `uv`
- Confirmed that notebooks and `src/tokyo_foreigners/` can run from the same `.venv`

### Week 2
- Added minimal `ruff`
- Applied formatting and lint checks to `src/tokyo_foreigners/` only

### Week 3
- Added minimal `pytest`
- Added tests for stable helper modules such as paths, boundaries, OLS preparation, station-attribute attachment, and land-price filtering

### Week 4
- Added lightweight GitHub Actions CI
- CI now runs `uv sync --locked`, `ruff check`, and `pytest` on push / pull request

## What this repository is now

This is a research-oriented spatial analysis repository with:

- a notebook-based analytical workflow
- reusable helper modules under `src/tokyo_foreigners/`
- reproducible environment setup with `uv`
- minimal linting and tests
- lightweight CI for routine validation

## What this repository is not trying to be right now

This stage does not:

- replace notebooks with a fully packaged pipeline
- migrate `data_raw/` to `data/raw/`
- introduce Docker or PostGIS
- add an application layer or agent layer
- run the full notebook workflow automatically in CI

## Next maintenance principle

Prefer small, reviewable engineering improvements that strengthen reproducibility without disrupting the existing notebook workflow.
