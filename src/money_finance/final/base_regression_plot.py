"""Create the baseline regression figure for the final outputs."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm


def base_regression_plot_fit(
    df: pd.DataFrame,
    produces: Path,
) -> None:
    """Create the baseline regression scatter plot with fitted line.

    Args:
        df: DataFrame containing ``mpu`` and ``sp500_return`` columns.
        produces: Output path for the saved figure.

    Returns:
        None. The function writes the figure to disk.

    Raises:
        ValueError: If the required plotting columns are missing.

    """
    required_cols = {"mpu", "sp500_return"}
    missing = required_cols - set(df.columns)

    if missing:
        msg = f"Missing required columns for regression plot: {missing}"
        raise ValueError(msg)

    y = df["sp500_return"]
    x = df["mpu"]

    x_with_const = sm.add_constant(x)
    model = sm.OLS(y, x_with_const).fit()

    plt.figure()
    plt.scatter(x, y)

    x_sorted = x.sort_values()
    x_sorted_const = sm.add_constant(x_sorted)
    y_fitted = model.predict(x_sorted_const)

    plt.plot(x_sorted, y_fitted)

    plt.xlabel("Monetary Policy Uncertainty (MPU)")
    plt.ylabel("S&P 500 Return")
    plt.title("MPU and S&P 500 Returns")

    produces.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(produces)
    plt.close()
