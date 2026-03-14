"""Unit tests for Table 2 summary analysis."""

import pandas as pd
import pytest

from money_finance.analysis.table2_summary import run_table2_summary


def test_run_table2_summary_returns_expected_tables() -> None:
    """Build baseline and press-conference tables with the expected columns."""
    fomc_dates = pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "1994-02-04",
                    "2001-09-17",
                    "2012-01-25",
                    "2012-03-13",
                    "2012-06-20",
                ]
            ),
            "mp1": [1.0, 1.0, 1.0, 1.0, 1.0],
            "unscheduled": [0, 0, 0, 1, 0],
        }
    )
    mpu_raw = pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "1994-02-03",
                    "1994-02-04",
                    "2001-09-16",
                    "2001-09-17",
                    "2012-01-24",
                    "2012-01-25",
                    "2012-03-12",
                    "2012-03-13",
                    "2012-06-19",
                    "2012-06-20",
                    "2012-06-21",
                ]
            ),
            "mpu": [1.00, 1.10, 1.20, 1.60, 1.70, 1.90, 2.00, 2.10, 2.30, 2.45, 2.55],
        }
    )
    fomc_actions = pd.DataFrame(
        {
            "date": ["2012-01-25", "2012-03-13", "2012-06-20"],
            "label": ["a", "b", "c"],
            "Press Conference": [1, 0, 1],
            "Scheduled FOMC": [1, 1, 1],
            "Unscheduled FOMC": [0, 1, 0],
            "SEP": [0, 0, 1],
            "Dotplot": [0, 0, 1],
            "Monetary Policy Report": [0, 0, 0],
            "Minutes Released": [0, 0, 0],
        }
    )

    results = run_table2_summary(
        fomc_dates=fomc_dates,
        mpu_raw=mpu_raw,
        fomc_actions=fomc_actions,
    )

    assert list(results.baseline.columns) == ["mpu_fomc", "mpu_nonfomc"]
    assert list(results.press_conference.columns) == ["mpuall", "mpupc", "mpunopc"]
    assert list(results.p_values.index) == [
        "fomc_mean_eq_0",
        "nonfomc_mean_eq_0",
        "fomc_vs_nonfomc",
    ]
    assert results.baseline.loc["Obs", "mpu_fomc"] == pytest.approx(3.0)
    assert results.baseline.loc["Obs", "mpu_nonfomc"] == pytest.approx(5.0)
    assert results.press_conference.loc["Obs", "mpuall"] == pytest.approx(2.0)
    assert results.press_conference.loc["Obs", "mpupc"] == pytest.approx(2.0)
    assert results.press_conference.loc["Obs", "mpunopc"] == pytest.approx(0.0)


pytestmark = pytest.mark.unit
