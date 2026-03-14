"""Merge SP500, MPU, and FOMC datasets into a single DataFrame."""

from pathlib import Path

import pandas as pd

from money_finance.data_management.load_fomc import load_fomc
from money_finance.data_management.load_mpu import load_mpu
from money_finance.data_management.load_sp500 import load_sp500


def load_market_data(
    sp500_path: Path,
    mpu_path: Path,
    fomc_path: Path,
) -> pd.DataFrame:
    """Load and merge the baseline market-analysis datasets.

    Args:
        sp500_path: Path to the raw S&P 500 return file.
        mpu_path: Path to the raw monetary policy uncertainty file.
        fomc_path: Path to the raw FOMC events file.

    Returns:
        Merged DataFrame keyed on ``date`` containing market returns, MPU values,
        and FOMC indicators.

    """
    sp500 = load_sp500(sp500_path)
    mpu = load_mpu(mpu_path)
    fomc = load_fomc(fomc_path)

    df = sp500.merge(mpu, on="date", how="left")
    df = df.merge(fomc, on="date", how="left")

    return df
