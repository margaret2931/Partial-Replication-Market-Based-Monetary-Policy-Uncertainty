# GEMINI.md

## Project Overview

This repository is a reproducible Python project that partially replicates empirical
results from **Market-Based Monetary Policy Uncertainty**. It combines raw data
preparation, econometric analysis, tables, figures, tests, and document generation in
one workflow.

The project focuses on:

- a baseline regression of S&P 500 returns on monetary policy uncertainty
- a Table 2 replication of uncertainty movements across FOMC and non-FOMC periods
- a Table 4-style multi-asset event-study replication

## Key Technologies and Tools

- **Language:** Python 3.14
- **Environment and dependency management:** Pixi
- **Workflow orchestration:** pytask, pytask-parallel
- **Data handling:** pandas, numpy
- **Econometrics:** statsmodels
- **Figures:** matplotlib, plotly, python-kaleido
- **Documentation:** MyST, Jupyter Book
- **Presentation:** Slidev
- **Testing:** pytest, pytest-cov, pytest-xdist
- **Code quality:** Ruff, ty, pre-commit, codespell

## Directory Structure

- `src/money_finance/`
  Main Python package containing the project logic.
- `src/money_finance/data_management/`
  Data loading, validation, and cleaning functions.
- `src/money_finance/analysis/`
  Baseline regression, Table 2, and Table 4 estimation logic.
- `src/money_finance/final/`
  Final markdown-table and figure generation code.
- `documents/`
  Source files for the paper, bibliography, presentation, and document build tasks.
- `tests/`
  Unit and integration tests for the project modules.
- `data/`
  Tracked raw inputs used by the workflow.
- `bld/`
  Generated data, models, tables, and figures.

## Input Data Files

The project uses the following tracked raw data files:

- `data/tab4data.csv`
- `data/mpu.csv`
- `data/fomc_dates.csv`
- `data/fomc_actions_clean.csv`

## Workflow

### 1. Install the environment

```bash
pixi install
```

### 2. Run the full analysis pipeline

```bash
pixi run pytask
```

### 3. Run the tests

```bash
pixi run pytest
```

### 4. Build the paper/documentation

```bash
pixi run -e docs docs
```

### 5. View the presentation

```bash
pixi run view-pres
```

## Development Conventions

- All reproducible outputs should be generated through `pytask`.
- Source code lives under `src/money_finance/`.
- Generated artifacts belong in `bld/` or `_build/`, not in source modules.
- Project-level configuration is in `pyproject.toml`, `myst.yml`, and
  `.pre-commit-config.yaml`.
- Public-facing functions should use Google-style docstrings.
