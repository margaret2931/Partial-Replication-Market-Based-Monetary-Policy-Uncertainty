"""Integration tests for the full data management pipeline."""

from pathlib import Path

import pandas as pd
import pytest

from money_finance.data_management.load_fomc import load_fomc
from money_finance.data_management.load_market_data import load_market_data
from money_finance.data_management.load_mpu import load_mpu
from money_finance.data_management.load_sp500 import load_sp500

# ---------------------------------------------------------------------
# 1. SP500
# ---------------------------------------------------------------------


EXPECTED_ROWS = 2
EXPECTED_FIRST_RETURN = 0.01


def test_load_sp500_success(tmp_path: Path) -> None:
    """Test successful loading and standardization of SP500 data."""
    file = tmp_path / "sp500.csv"

    pd.DataFrame(
        {
            "Time": ["2020-01-01", "2020-01-02"],
            "sp_daily": [EXPECTED_FIRST_RETURN, 0.02],
        }
    ).to_csv(file, index=False)

    df = load_sp500(file)

    assert list(df.columns) == ["date", "sp500_return"]
    assert len(df) == EXPECTED_ROWS
    assert df["sp500_return"].iloc[0] == EXPECTED_FIRST_RETURN


def test_load_sp500_failure(tmp_path: Path) -> None:
    """Test that invalid SP500 input raises a validation error."""
    file = tmp_path / "sp500.csv"

    pd.DataFrame({"date": ["2020-01-01"]}).to_csv(file, index=False)

    with pytest.raises(ValueError, match="must contain"):
        load_sp500(file)


# ---------------------------------------------------------------------
# 2. MPU
# ---------------------------------------------------------------------


def test_load_mpu_success(tmp_path: Path) -> None:
    """Test successful loading of MPU data."""
    file = tmp_path / "mpu.csv"

    pd.DataFrame(
        {
            "date": ["2020-01-01"],
            "mpu": [1.2],
        }
    ).to_csv(file, index=False)

    df = load_mpu(file)

    assert "mpu" in df.columns
    assert len(df) == 1


# ---------------------------------------------------------------------
# 3. FOMC
# ---------------------------------------------------------------------


def test_load_fomc_success(tmp_path: Path) -> None:
    """Test successful loading of FOMC event data."""
    file = tmp_path / "fomc.csv"

    pd.DataFrame(
        {
            "Date": ["2020-01-01"],
            "Type": ["Statement"],
        }
    ).to_csv(file, index=False)

    df = load_fomc(file)

    assert "is_fomc" in df.columns
    assert df["is_fomc"].iloc[0] == 1


# ---------------------------------------------------------------------
# 4. Full Merge
# ---------------------------------------------------------------------


def test_full_merge_pipeline(tmp_path: Path) -> None:
    """Test full merge pipeline with minimal valid inputs."""
    sp500 = tmp_path / "sp500.csv"
    mpu = tmp_path / "mpu.csv"
    fomc = tmp_path / "fomc.csv"

    pd.DataFrame(
        {
            "Time": ["2020-01-01", "2020-01-02"],
            "sp_daily": [0.01, 0.02],
        }
    ).to_csv(sp500, index=False)

    pd.DataFrame(
        {
            "date": ["2020-01-01"],
            "mpu": [2.0],
        }
    ).to_csv(mpu, index=False)

    pd.DataFrame(
        {
            "Date": ["2020-01-01"],
            "Type": ["Statement"],
        }
    ).to_csv(fomc, index=False)

    df = load_market_data(sp500, mpu, fomc)

    assert "sp500_return" in df.columns
    assert "mpu" in df.columns
    assert "date" in df.columns
