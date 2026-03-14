"""Clean the event-study dataset used for the Table 4 replication."""

import pandas as pd

REQUIRED_COLUMNS = {
    "date",
    "dSVENY10",
    "mps",
    "mpu",
    "mpu_lag",
}


def clean_tab4(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean event-study dataset for Table 4 replication.

    Args:
        raw: Raw event-study DataFrame loaded from the replication dataset.

    Returns:
        Cleaned DataFrame with standardized column names, parsed dates, numeric
        regression columns, and crisis-period observations removed.

    Raises:
        TypeError: If ``raw`` is not a pandas DataFrame.
        ValueError: If required columns are missing, dates cannot be parsed, or
            the cleaned dataset is empty.

    """
    if not isinstance(raw, pd.DataFrame):
        msg = "Input must be a pandas DataFrame."
        raise TypeError(msg)

    df = raw.copy()

    df = df.rename(
        columns={
            "Time": "date",
            "mpu_level_lag": "mpu_lag",
        }
    )

    df.columns = df.columns.str.strip()

    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        msg = f"Missing required columns: {missing_cols}"
        raise ValueError(msg)

    df["date"] = pd.to_datetime(df["date"], format="mixed", errors="coerce")

    if df["date"].isna().any():
        msg = "Some dates could not be parsed."
        raise ValueError(msg)

    numeric_cols = ["dSVENY10", "mps", "mpu", "mpu_lag"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=numeric_cols)

    crisis_start = pd.Timestamp("2007-07-01")
    crisis_end = pd.Timestamp("2009-06-30")

    df = df.loc[~df["date"].between(crisis_start, crisis_end)]

    if df.empty:
        msg = "Dataset is empty after cleaning."
        raise ValueError(msg)

    df = df.sort_values("date").reset_index(drop=True)

    return df
