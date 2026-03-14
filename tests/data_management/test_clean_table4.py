"""Tests for clean_tab4 data cleaning logic."""

import pandas as pd
import pytest

from money_finance.data_management.clean_tab4 import clean_tab4

CRISIS_START = pd.Timestamp("2007-07-01")
CRISIS_END = pd.Timestamp("2009-06-30")


def make_valid_df() -> pd.DataFrame:
    """Create minimal valid raw dataset."""
    return pd.DataFrame(
        {
            "Time": ["2006-01-01", "2008-01-01", "2010-01-01"],
            "dSVENY10": [0.1, 0.2, 0.3],
            "mps": [1.0, 1.1, 1.2],
            "mpu": [2.0, 2.1, 2.2],
            "mpu_level_lag": [1.5, 1.6, 1.7],
        }
    )


def test_clean_tab4_success() -> None:
    """Valid dataset is cleaned and crisis period removed."""
    df = clean_tab4(make_valid_df())

    assert isinstance(df, pd.DataFrame)
    assert "date" in df.columns
    assert "mpu_lag" in df.columns

    assert not df["date"].between(CRISIS_START, CRISIS_END).any()


def test_clean_tab4_drops_missing_values() -> None:
    """Rows with missing regression variables are dropped."""
    raw = make_valid_df()
    raw.loc[0, "mps"] = None

    df = clean_tab4(raw)

    assert len(df) == 1


def test_clean_tab4_missing_columns() -> None:
    """Missing required columns raises error."""
    raw = pd.DataFrame({"Time": ["2006-01-01"]})

    with pytest.raises(ValueError, match="Missing required columns"):
        clean_tab4(raw)


def test_clean_tab4_invalid_date() -> None:
    """Unparsable dates raise error."""
    raw = make_valid_df()
    raw.loc[0, "Time"] = "invalid"

    with pytest.raises(ValueError, match="could not be parsed"):
        clean_tab4(raw)


pytestmark = pytest.mark.unit
