"""Load and validate FOMC meeting dates used for Table 2."""

from pathlib import Path

import pandas as pd


def load_fomc_dates(path: Path) -> pd.DataFrame:
    """Load FOMC meeting dates used in the Table 2 replication.

    Args:
        path: Path to the FOMC meeting-dates CSV file.

    Returns:
        DataFrame with standardized ``date``, ``mp1``, and ``unscheduled``
        columns, sorted by date.

    Raises:
        ValueError: If required columns are missing or dates cannot be parsed.

    """
    df = pd.read_csv(path)

    required_cols = {"Date", "MP1", "Unscheduled"}
    if not required_cols.issubset(df.columns):
        msg = "FOMC dates file must contain 'Date', 'MP1', and 'Unscheduled'."
        raise ValueError(msg)

    out = df.rename(
        columns={"Date": "date", "MP1": "mp1", "Unscheduled": "unscheduled"}
    )
    out["date"] = pd.to_datetime(out["date"], format="mixed", errors="coerce")
    if out["date"].isna().any():
        msg = "FOMC dates file contains unparsable dates."
        raise ValueError(msg)

    out["mp1"] = pd.to_numeric(out["mp1"], errors="coerce")
    out["unscheduled"] = (
        pd.to_numeric(out["unscheduled"], errors="coerce").fillna(0).astype(int)
    )

    return (
        out[["date", "mp1", "unscheduled"]].sort_values("date").drop_duplicates("date")
    )
