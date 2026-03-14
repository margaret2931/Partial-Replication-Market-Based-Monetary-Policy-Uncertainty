"""Pytask tasks for writing baseline regression table outputs."""

from pathlib import Path

import pandas as pd
import pytask

from money_finance.analysis.base_regression import run_base_regression
from money_finance.config import BLD, DOCUMENTS


@pytask.task
def task_create_regression_table(
    results_path: Path = BLD / "models" / "regression_results.pkl",
    produces: Path = DOCUMENTS / "tables" / "baseline_regression.md",
) -> None:
    """Create journal-style regression table from saved results."""
    df = pd.read_pickle(results_path)

    produces.parent.mkdir(parents=True, exist_ok=True)

    with produces.open("w") as f:
        f.write("# Baseline Regression Results\n\n")
        f.write(df.to_markdown())


@pytask.task
def task_regression_summary(
    data: Path = BLD / "data" / "market_data.pkl",
    produces: Path = BLD / "tables" / "regression_summary.md",
) -> None:
    """Write the statsmodels baseline regression summary to a markdown file."""
    df = pd.read_pickle(data)

    model = run_base_regression(df)

    summary_text = model.summary().as_text()

    produces.parent.mkdir(parents=True, exist_ok=True)
    produces.write_text(summary_text)
