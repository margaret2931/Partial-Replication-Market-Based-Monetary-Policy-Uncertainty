"""Load and validate MPU data."""

from pathlib import Path

import pandas as pd


def load_mpu(path: Path) -> pd.DataFrame:
    """Load the raw MPU series and standardize its schema.

    Args:
        path: Path to the raw MPU CSV file.

    Returns:
        DataFrame with standardized ``date`` and ``mpu`` columns, sorted by date.

    Raises:
        ValueError: If the required columns are not present in the input file.

    """
    df = pd.read_csv(path)

    df = df.rename(
        columns={
            "mpu10": "mpu",
        }
    )

    required_cols = {"date", "mpu"}
    if not required_cols.issubset(df.columns):
        msg = "MPU file must contain 'date' and 'mpu' columns."
        raise ValueError(msg)

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").drop_duplicates(subset="date")

    return df[["date", "mpu"]]
