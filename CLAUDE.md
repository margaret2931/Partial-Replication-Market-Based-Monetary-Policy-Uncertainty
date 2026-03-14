# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

This repository is a partial replication of **Market-Based Monetary Policy
Uncertainty**. It is organized as a reproducible empirical Python workflow using `pixi`
for environment management and `pytask` for dependency-driven execution.

The project covers three main empirical components:

1. A baseline regression of daily S&P 500 returns on monetary policy uncertainty.
1. A Table 2 replication summarizing uncertainty changes across FOMC and non-FOMC
   periods.
1. A Table 4-style multi-asset event-study replication across yields, equities,
   volatility, and the dollar.

## Common Commands

```bash
# Install project environments
pixi install

# Run the full computational pipeline
pixi run pytask

# Run tests
pixi run pytest

# Run pre-commit hooks
pixi run prek

# Build the paper/documentation
pixi run -e docs docs

# View the paper and presentation interactively
pixi run view-paper
pixi run view-pres

# View documentation locally
pixi run -e docs view-docs
```

## Architecture

### Workflow Pipeline

The project is organized into task-based stages.

1. **Data Management**
   [`src/money_finance/data_management/`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/src/money_finance/data_management)

   - Loads raw CSV inputs
   - Cleans the baseline market dataset
   - Cleans the Table 4 event-study dataset
   - Writes cleaned outputs to `bld/data/`

1. **Analysis**
   [`src/money_finance/analysis/`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/src/money_finance/analysis)

   - Estimates the baseline regression
   - Computes Table 2 summary results
   - Estimates Table 4 multi-asset regressions
   - Writes serialized results to `bld/models/`

1. **Final Outputs**
   [`src/money_finance/final/`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/src/money_finance/final)

   - Creates markdown tables
   - Generates the baseline regression figure
   - Generates Table 4 multi-asset figures
   - Writes outputs to `bld/figures/`, `bld/tables/`, and `documents/tables/`

1. **Documents**
   [`documents/task_documents.py`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/documents/task_documents.py)

   - Builds the paper via Jupyter Book / MyST
   - Uses generated tables and figures as document inputs

### Key Inputs

Tracked raw data files are stored in `data/`:

- `tab4data.csv`
- `mpu.csv`
- `fomc_dates.csv`
- `fomc_actions_clean.csv`

### Key Configuration

- [`pyproject.toml`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/pyproject.toml):
  Pixi, pytask, Ruff, pytest, and tool configuration
- [`myst.yml`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/myst.yml):
  MyST / Jupyter Book configuration
- [`src/money_finance/config.py`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/src/money_finance/config.py):
  Central path definitions

## Directory Conventions

- `src/money_finance/`: hand-written project source code
- `tests/`: unit and integration tests
- `data/`: tracked raw input data
- `bld/`: generated computational artifacts
- `documents/`: paper, references, presentation, and document tasks
- `_build/`: built HTML/document outputs

## Code Quality

- **Python version:** 3.14
- **Linting/formatting:** Ruff
- **Static checks:** ty
- **Pre-commit hooks:** yamlfix, yamllint, mdformat, codespell, Ruff, and related checks
- **Docstrings:** Google style

## Testing

- Test suite is in
  [`tests/`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/tests)
- Uses `pytest` with unit and integration markers
- Tests cover data cleaning, analysis logic, task outputs, and figure generation
