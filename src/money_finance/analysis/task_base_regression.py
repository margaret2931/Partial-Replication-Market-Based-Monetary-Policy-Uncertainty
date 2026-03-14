"""Pytask task for estimating and storing the baseline regression."""

from pathlib import Path

import pandas as pd
import pytask

from money_finance.analysis.base_regression import run_base_regression
from money_finance.config import BLD


@pytask.task
def task_run_base_regression(
    data: Path = BLD / "data" / "market_data.pkl",
    produces: Path = BLD / "models" / "regression_results.pkl",
) -> None:
    """Run baseline regression and store regression output."""
    if not data.exists():
        msg = f"Missing input file: {data}"
        raise FileNotFoundError(msg)

    df = pd.read_pickle(data)

    model = run_base_regression(df)

    results = pd.DataFrame(
        {
            "coef": model.params,
            "std_err": model.bse,
            "t_stat": model.tvalues,
            "p_value": model.pvalues,
        }
    )

    results.attrs["r_squared"] = model.rsquared
    results.attrs["n_obs"] = int(model.nobs)

    produces.parent.mkdir(parents=True, exist_ok=True)
    results.to_pickle(produces)
