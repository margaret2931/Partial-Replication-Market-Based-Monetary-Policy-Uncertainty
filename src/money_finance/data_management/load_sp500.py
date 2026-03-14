"""Load and validate S&P 500 daily return data."""

from pathlib import Path

import pandas as pd


def load_sp500(path: Path) -> pd.DataFrame:
    """Load S&P 500 daily returns from replication dataset.

    Args:
        path: Path to the raw S&P 500 CSV file.

    Returns:
        DataFrame with standardized ``date`` and ``sp500_return`` columns, sorted
        by date.

    Raises:
        ValueError: If the required columns are not present in the input file.

    """
    df = pd.read_csv(path)

    df = df.rename(
        columns={
            "Time": "date",
            "sp_daily": "sp500_return",
        }
    )

    required_cols = {"date", "sp500_return"}
    if not required_cols.issubset(df.columns):
        msg = f"SP500 file must contain columns {required_cols}"
        raise ValueError(msg)

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").drop_duplicates(subset="date")

    return df[["date", "sp500_return"]]
