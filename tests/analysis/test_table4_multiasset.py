"""Unit tests for the multi-asset Table 4 regression analysis."""

import numpy as np
import pandas as pd
import pytest

from money_finance.analysis.table4_multiasset import (
    ASSET_NAMES,
    _get_lag_column,
    run_table4_models_multiasset,
)


def _make_multiasset_df(n: int = 12) -> pd.DataFrame:
    """Create synthetic multi-asset regression input data."""
    rng = np.random.default_rng(7)
    data = pd.DataFrame(
        {
            "date": pd.date_range("2008-01-01", periods=n),
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
    data.loc[[0, 1], "dTIPSY10"] = np.nan
    data.loc[[2, 3, 4], "dollar_ret_pm"] = np.nan
    return data


def test_get_lag_column_prefers_level_lag() -> None:
    """Prefer 'mpu_level_lag' when both lag-column names are present."""
    df = _make_multiasset_df().rename(columns={"mpu_lag": "mpu_level_lag"})
    df["mpu_lag"] = 0.0
    assert _get_lag_column(df) == "mpu_level_lag"


def test_run_table4_models_multiasset_returns_all_assets_and_specs() -> None:
    """Return one model bundle per asset with exactly specs 1, 2, and 3."""
    models = run_table4_models_multiasset(_make_multiasset_df())
    assert set(models.keys()) == set(ASSET_NAMES)
    for asset in ASSET_NAMES:
        assert set(models[asset].keys()) == {"1", "2", "3"}


def test_run_table4_models_multiasset_uses_asset_specific_nonmissing_rows() -> None:
    """Fit each asset on its own non-missing rows and reflect this in nobs."""
    df = _make_multiasset_df()
    models = run_table4_models_multiasset(df)

    n_dsveny10 = int(df[["dSVENY10", "mps", "mpu", "mpu_lag"]].dropna().shape[0])
    n_tips = int(df[["dTIPSY10", "mps", "mpu", "mpu_lag"]].dropna().shape[0])

    assert int(models["dSVENY10"]["3"].nobs) == n_dsveny10
    assert int(models["dTIPSY10"]["3"].nobs) == n_tips
    assert int(models["dTIPSY10"]["3"].nobs) < int(models["dSVENY10"]["3"].nobs)


def test_run_table4_models_multiasset_missing_required_column_raises() -> None:
    """Raise a clear error when a required asset column is absent."""
    df = _make_multiasset_df().drop(columns=["dSVENY10"])
    with pytest.raises(ValueError, match="Missing required columns"):
        run_table4_models_multiasset(df)


pytestmark = pytest.mark.unit
