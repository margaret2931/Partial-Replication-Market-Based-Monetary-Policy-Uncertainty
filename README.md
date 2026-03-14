# Partial Replication: Market-Based Monetary Policy Uncertainty

Final project for **Effective Programming Practices for Economists**.

## Author

Margaret Vincent, University of Bonn

## Project Overview

This project is a reproducible Python workflow that partially replicates core empirical
results from Bauer, Lakdawala, and Mueller (2022), *Market-Based Monetary Policy
Uncertainty*. The repository combines data preparation, econometric analysis, tables,
figures, tests, and project documentation in one `pixi` + `pytask` pipeline.

The project focuses on three empirical components:

- a baseline regression linking daily S&P 500 returns to monetary policy uncertainty
- a Table 2 replication summarizing how uncertainty changes differ across FOMC and
  non-FOMC days
- a Table 4-style multi-asset event-study replication that studies how policy surprises
  and uncertainty interact across asset classes

## Research Components

### Baseline Regression

The baseline analysis estimates a simple linear relationship between daily S&P 500
returns and changes in monetary policy uncertainty. It serves as the benchmark model for
the rest of the project.

### Table 2 Replication

The Table 2 analysis produces summary statistics for changes in monetary policy
uncertainty across scheduled FOMC days, non-FOMC days, and press-conference versus
non-press-conference meetings in the later subsample. This component is descriptive and
shows that uncertainty changes are concentrated around policy communication events.

### Table 4 Multi-Asset Replication

The Table 4 analysis estimates multi-asset event-study regressions for Treasury yields,
equity returns, the VIX, and the dollar. It relates asset-price responses to monetary
policy surprises, changes in monetary policy uncertainty, and the interaction between
policy surprises and lagged uncertainty. This is the main econometric component of the
project.

## Data Files Used

The project uses the following tracked input files in
[`data/`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/data):

- `tab4data.csv` Event-study dataset used for the Table 4 multi-asset replication. It
  contains the dependent variables, monetary policy surprises, uncertainty measures, and
  lagged uncertainty used in the event-study models.
- `mpu.csv` Daily monetary policy uncertainty series used in the baseline regression and
  Table 2 workflow.
- `fomc_dates.csv` FOMC meeting dates and scheduling indicators used for the Table 2
  replication.
- `fomc_actions_clean.csv` FOMC event indicators merged into the baseline market
  dataset.

## Code Structure

The source code is organized by workflow stage.

- [`src/money_finance/data_management/`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/src/money_finance/data_management)
  Loaders and cleaning functions for market data, MPU data, FOMC data, and the Table 4
  event-study dataset.
- [`src/money_finance/analysis/`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/src/money_finance/analysis)
  Core empirical analysis code: baseline regression, Table 2 summary-statistics logic,
  and Table 4 multi-asset regression estimation.
- [`src/money_finance/final/`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/src/money_finance/final)
  Final output code for markdown tables and figures, including the baseline regression
  plot and the Table 4 multi-asset visualizations.
- [`documents/`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/documents)
  Project paper, references, presentation, and documentation build tasks.
- [`tests/`](/Users/margaretvincent/Documents/advanced_modules/sem_3/EPPE/final-project-margaret2931/tests)
  Unit and integration tests for the data-management, analysis, and final-output
  modules.

## Research Workflow

The pipeline performs the following steps:

1. Clean and validate the raw market, uncertainty, and FOMC event data.
1. Build the baseline market dataset and the cleaned Table 4 event-study dataset.
1. Estimate the baseline regression, compute the Table 2 summary-statistics replication,
   and fit the Table 4 multi-asset regression models.
1. Produce publication-ready outputs, including:
   - serialized regression and summary result files
   - markdown tables for the baseline regression, Table 2, and Table 4
   - summary text outputs
   - figures for the baseline regression and Table 4 multi-asset results

### Output Conventions

Generated artifacts are stored in `bld/`, while selected publication-facing tables are
also written to `documents/tables/` for direct inclusion in the paper and for quick
reference. Compiled documentation outputs are written to `_build/`.

## Main Technologies and Libraries

- Python
- `pixi` for environment and task management
- `pytask` and `pytask-parallel` for workflow orchestration
- `pandas` and `numpy` for data handling
- `statsmodels` for econometric estimation
- `matplotlib`, `plotly`, and `python-kaleido` for figure generation and export
- `jupyter-book` and `mystmd` for documentation and paper rendering
- `pytest`, `pytest-cov`, and `pytest-xdist` for testing
- `ruff`, `ty`, `pre-commit`, and `codespell` for quality checks
- `tabulate` for markdown table rendering

## Version History

- `v0`: Began the project and set up the money-finance repository.
- `v1`: Built the baseline regression workflow, including data loading and cleaning.
- `v2`: Started the main Table 4 workflow and organized the project structure.
- `v3`: Implemented the Table 4 regression specifications and model outputs.
- `v4`: Refined the baseline regression workflow and fixed table/summary generation.
- `v5`: Debugged and refined the Table 4 regression outputs.
- `v6`: Improved the documentation and project configuration.
- `v7`: Strengthened test coverage for the Table 4 regression workflow.
- `v8`: Added the multi-asset model for the Table 4 replication.
- `v9`: Applied final codebase polishing.
- `v10`: Added the Table 2 replication.

## Reproducibility

Run all commands from the project root.

### 1. Install the environment

```bash
pixi install
```

### 2. Run the full workflow

```bash
pixi run pytask
```

### 3. Run the test suite

```bash
pixi run pytest
```

### 4. Build the documentation

```bash
pixi run -e docs docs
```

### 5. View the presentation

```bash
pixi run view-pres
```

## Key Generated Outputs

After `pixi run pytask`, key artifacts include:

- `bld/data/market_data.pkl`
- `bld/data/clean_tab4.pkl`
- `bld/models/regression_results.pkl`
- `bld/models/table2_summary.pkl`
- `bld/models/table4_multiasset_results.pkl`
- `bld/figures/regression_plot.png`
- `bld/figures/table4_multiasset_mps_by_spec_panel.png`
- `bld/figures/table4_multiasset_marginal_effects.png`
- `bld/figures/table4_multiasset_r2_heatmap.png`
- `bld/tables/regression_summary.md`
- `bld/tables/table2_summary.md`
- `bld/tables/table4_multiasset_regression.md`
- `documents/tables/baseline_regression.md`
- `documents/tables/table2_summary.md`
- `documents/tables/table4_multiasset_regression.md`

## Clean Reproduction From Build Artifacts Removed

```bash
rm -rf bld
rm -rf documents/tables
rm -rf _build
pixi install
pixi run pytask
pixi run pytest
pixi run -e docs docs
```
