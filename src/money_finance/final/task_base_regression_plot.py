"""Pytask task for generating the baseline regression plot."""

from pathlib import Path

import pandas as pd
import pytask

from money_finance.config import BLD
from money_finance.final.base_regression_plot import base_regression_plot_fit


@pytask.task
def task_base_regression_plot(
    data: Path = BLD / "data" / "market_data.pkl",
    produces: Path = BLD / "figures" / "regression_plot.png",
) -> None:
    """Create regression visualization."""
    if not data.exists():
        msg = f"Missing input file: {data}"
        raise FileNotFoundError(msg)
    df = pd.read_pickle(data)
    base_regression_plot_fit(df, produces)
