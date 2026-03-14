"""Estimate multi-asset Table 4 regressions with clustered standard errors."""

import pandas as pd
import statsmodels.api as sm

ASSET_NAMES = (
    "dSVENY05",
    "dSVENY10",
    "dTIPSY10",
    "sp_daily",
    "dvix",
    "dollar_ret_pm",
)

ASSET_SCALES = {
    "dSVENY05": 1.0,
    "dSVENY10": 1.0,
    "dTIPSY10": 1.0,
    "sp_daily": 100.0,
    "dvix": 1.0,
    "dollar_ret_pm": -100.0,
}


def _get_lag_column(data: pd.DataFrame) -> str:
    """Return the lagged MPU column available in the cleaned Table 4 data.

    Prefers ``mpu_level_lag`` when both lag conventions are present.
    """
    if "mpu_level_lag" in data.columns:
        return "mpu_level_lag"
    if "mpu_lag" in data.columns:
        return "mpu_lag"

    msg = "Missing required columns: ['mpu_lag' or 'mpu_level_lag']"
    raise ValueError(msg)


def _fit_asset_models(data: pd.DataFrame, *, asset: str, lag_col: str) -> dict:
    """Estimate the three Table 4 specifications for a single asset.

    Fits OLS models with standard errors clustered by date.
    """
    specs = {
        "1": ["mps"],
        "2": ["mps", "mpu"],
        "3": ["mps", "mpu", lag_col, "interaction"],
    }

    models = {}
    for spec, regressors in specs.items():
        cols = ["date", asset, *regressors]
        sample = data[cols].dropna()

        y = sample[asset] * ASSET_SCALES[asset]
        x = sm.add_constant(sample[regressors])

        models[spec] = sm.OLS(y, x).fit(
            cov_type="cluster",
            cov_kwds={"groups": sample["date"]},
        )

    return models


def run_table4_models_multiasset(df: pd.DataFrame) -> dict:
    """Estimate the full Table 4 regression set across all assets.

    Returns fitted models indexed first by asset name and then by specification.
    """
    data = df.copy()
    lag_col = _get_lag_column(data)

    required = {"date", "mps", "mpu", lag_col, *ASSET_NAMES}
    missing = required - set(data.columns)
    if missing:
        msg = f"Missing required columns: {sorted(missing)}"
        raise ValueError(msg)

    data["interaction"] = data["mps"] * data[lag_col]

    all_models = {}
    for asset in ASSET_NAMES:
        all_models[asset] = _fit_asset_models(data, asset=asset, lag_col=lag_col)

    return all_models
