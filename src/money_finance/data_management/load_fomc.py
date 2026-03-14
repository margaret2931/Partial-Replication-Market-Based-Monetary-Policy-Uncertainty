"""Load and normalize FOMC event data for downstream analysis."""

from pathlib import Path

import pandas as pd


def load_fomc(path: Path) -> pd.DataFrame:
    """Load FOMC events and create normalized indicator columns.

    Args:
        path: Path to the raw FOMC events CSV file.

    Returns:
        DataFrame with one row per date, an ``is_fomc`` indicator, and
        event-type dummy columns.

    Raises:
        ValueError: If required columns are missing or dates cannot be parsed.

    """
    df = pd.read_csv(path)

    required_cols = {"Date", "Type"}
    if not required_cols.issubset(df.columns):
        msg = "FOMC file must contain 'Date' and 'Type' columns."
        raise ValueError(msg)

    renamed = df.rename(columns={"Date": "date", "Type": "event_type"})
    out = renamed[["date", "event_type"]].copy()

    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    if out["date"].isna().any():
        msg = "FOMC file contains unparsable dates."
        raise ValueError(msg)

    out["event_type"] = (
        out["event_type"]
        .astype("string")
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )

    out["is_fomc"] = 1
    out = pd.get_dummies(out, columns=["event_type"], prefix="fomc")
    out = out.groupby("date", as_index=False).max()

    return out
