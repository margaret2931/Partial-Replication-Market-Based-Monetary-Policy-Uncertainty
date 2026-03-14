"""Estimate the baseline regression used in the project."""

import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.linear_model import RegressionResultsWrapper


def run_base_regression(df: pd.DataFrame) -> RegressionResultsWrapper:
    """Estimate the baseline OLS regression of S&P 500 returns on MPU.

    Args:
        df: DataFrame containing the ``sp500_return`` dependent variable and the
            ``mpu`` regressor.

    Returns:
        Fitted statsmodels regression results object.

    Raises:
        ValueError: If the required regression columns are missing.

    """
    required = {"sp500_return", "mpu"}
    missing = required - set(df.columns)
    if missing:
        msg = f"Missing required columns: {sorted(missing)}"
        raise ValueError(msg)

    y = df["sp500_return"]
    x = sm.add_constant(df["mpu"])
    return sm.OLS(y, x).fit()
