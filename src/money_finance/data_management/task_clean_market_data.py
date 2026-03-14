"""Load and validate S&P 500 data."""

from pathlib import Path

import pytask

from money_finance.config import BLD, ROOT
from money_finance.data_management.load_market_data import load_market_data


@pytask.task
def task_clean_market_data(
    sp500_path: Path = ROOT / "data" / "tab4data.csv",
    mpu_path: Path = ROOT / "data" / "mpu.csv",
    fomc_path: Path = ROOT / "data" / "fomc_actions_clean.csv",
    produces: Path = BLD / "data" / "market_data.pkl",
) -> None:
    """Load, clean, and store the baseline market dataset."""
    df = load_market_data(sp500_path, mpu_path, fomc_path)

    df = df.sort_values("date")
    df = df.dropna(subset=["sp500_return"])

    df["mpu"] = df["mpu"].fillna(0)
    df["is_fomc"] = df["is_fomc"].fillna(0).astype(int)
    fomc_cols = [c for c in df.columns if c.startswith("fomc_")]
    df[fomc_cols] = df[fomc_cols].fillna(0).astype(int)

    produces.parent.mkdir(parents=True, exist_ok=True)
    df.to_pickle(produces)
