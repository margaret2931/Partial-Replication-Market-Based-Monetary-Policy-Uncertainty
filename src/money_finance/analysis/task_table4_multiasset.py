"""Pytask task for estimating and storing multi-asset Table 4 models."""

from pathlib import Path

import pandas as pd
import pytask

from money_finance.analysis.table4_multiasset import run_table4_models_multiasset
from money_finance.config import BLD


def _serialize_model(model) -> dict:
    """Convert a fitted statsmodels result into a pickle-friendly dictionary.

    Stores coefficients, standard errors, covariance matrix, fit, and sample size.
    """
    return {
        "coef": model.params,
        "std_err": model.bse,
        "cov": model.cov_params(),
        "r_squared": model.rsquared,
        "n_obs": int(model.nobs),
    }


@pytask.task
def task_run_table4_multiasset_regression(
    data: Path = BLD / "data" / "clean_tab4.pkl",
    produces: Path = BLD / "models" / "table4_multiasset_results.pkl",
    *,
    write_text_summary: bool = False,
) -> None:
    """Estimate the Table 4 multi-asset regressions and store serialized results.

    Optionally writes a plain-text summary file alongside the pickle output.
    """
    if not data.exists():
        msg = f"Missing input file: {data}"
        raise FileNotFoundError(msg)

    df = pd.read_pickle(data)
    models_by_asset = run_table4_models_multiasset(df)

    results = {
        asset: {spec: _serialize_model(model) for spec, model in specs.items()}
        for asset, specs in models_by_asset.items()
    }

    produces.parent.mkdir(parents=True, exist_ok=True)
    pd.to_pickle(results, produces)

    if write_text_summary:
        text_output: list[str] = []
        for asset, specs in models_by_asset.items():
            text_output.append(f"\n=== Asset: {asset} ===\n")
            for spec, model in specs.items():
                text_output.append(f"\nSpecification {spec}\n")
                text_output.append(model.summary().as_text())

        text_file = produces.with_suffix(".txt")
        text_file.parent.mkdir(parents=True, exist_ok=True)
        text_file.write_text("\n".join(text_output))
