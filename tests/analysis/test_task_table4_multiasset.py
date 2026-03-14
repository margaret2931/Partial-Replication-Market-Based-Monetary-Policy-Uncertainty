"""Integration tests for the multi-asset Table 4 regression task."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from money_finance.analysis.task_table4_multiasset import (
    task_run_table4_multiasset_regression,
)


def _make_multiasset_df(n: int = 14) -> pd.DataFrame:
    """Create synthetic multi-asset input data for task-level regression tests."""
    rng = np.random.default_rng(11)
    data = pd.DataFrame(
        {
            "date": pd.date_range("2010-01-01", periods=n),
            "mps": rng.normal(size=n),
            "mpu": rng.normal(size=n),
            "mpu_lag": rng.normal(size=n),
            "dSVENY05": rng.normal(size=n),
            "dSVENY10": rng.normal(size=n),
            "dTIPSY10": rng.normal(size=n),
            "sp_daily": rng.normal(size=n),
            "dvix": rng.normal(size=n),
            "dollar_ret_pm": rng.normal(size=n),
        }
    )
    data.loc[[0, 3], "dollar_ret_pm"] = np.nan
    return data


def test_task_table4_multiasset_missing_input_raises(tmp_path: Path) -> None:
    """Raise FileNotFoundError when the task input pickle is missing."""
    missing = tmp_path / "missing.pkl"
    out = tmp_path / "table4_multiasset_results.pkl"
    with pytest.raises(FileNotFoundError, match="Missing input file"):
        task_run_table4_multiasset_regression(data=missing, produces=out)


def test_task_table4_multiasset_writes_pickle_with_expected_structure(
    tmp_path: Path,
) -> None:
    """Write a results pickle with expected asset/spec keys and serialized fields."""
    data = tmp_path / "clean_tab4.pkl"
    out = tmp_path / "models" / "table4_multiasset_results.pkl"
    pd.to_pickle(_make_multiasset_df(), data)

    task_run_table4_multiasset_regression(data=data, produces=out)

    assert out.exists()
    results = pd.read_pickle(out)
    assert "dSVENY10" in results
    assert set(results["dSVENY10"].keys()) == {"1", "2", "3"}
    assert {"coef", "std_err", "cov", "r_squared", "n_obs"}.issubset(
        results["dSVENY10"]["1"].keys()
    )


def test_task_table4_multiasset_optional_text_summary_written(tmp_path: Path) -> None:
    """Write a text summary file when write_text_summary is enabled."""
    data = tmp_path / "clean_tab4.pkl"
    out = tmp_path / "models" / "table4_multiasset_results.pkl"
    pd.to_pickle(_make_multiasset_df(), data)

    task_run_table4_multiasset_regression(
        data=data,
        produces=out,
        write_text_summary=True,
    )

    text_file = out.with_suffix(".txt")
    assert text_file.exists()
    text = text_file.read_text()
    assert "Asset: dSVENY10" in text
    assert "Specification 3" in text


pytestmark = pytest.mark.integration
