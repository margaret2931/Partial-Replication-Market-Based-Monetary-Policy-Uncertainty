"""Integration tests for the multi-asset plotting task."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import money_finance.final.task_plot_table4_multiasset as task_mod


def _make_multiasset_df(n: int = 20) -> pd.DataFrame:
    """Create synthetic clean_tab4-like data for plotting task tests."""
    rng = np.random.default_rng(101)
    return pd.DataFrame(
        {
            "date": pd.date_range("2012-01-01", periods=n),
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


def _make_results() -> dict:
    """Create synthetic serialized model results consumed by plotting task."""
    cov = pd.DataFrame(
        [[0.04, 0.0, 0.0], [0.0, 0.09, 0.01], [0.0, 0.01, 0.16]],
        index=["mps", "mpu", "interaction"],
        columns=["mps", "mpu", "interaction"],
    )

    assets = ("dSVENY05", "dSVENY10", "dTIPSY10", "sp_daily", "dvix", "dollar_ret_pm")
    out = {}
    for asset in assets:
        out[asset] = {
            "1": {
                "coef": pd.Series({"const": 0.0, "mps": 0.1}),
                "std_err": pd.Series({"const": 0.01, "mps": 0.02}),
                "cov": cov,
                "r_squared": 0.11,
                "n_obs": 20,
            },
            "2": {
                "coef": pd.Series({"const": 0.0, "mps": 0.1, "mpu": 0.01}),
                "std_err": pd.Series({"const": 0.01, "mps": 0.02, "mpu": 0.03}),
                "cov": cov,
                "r_squared": 0.21,
                "n_obs": 20,
            },
            "3": {
                "coef": pd.Series(
                    {"const": 0.0, "mps": 0.1, "mpu": 0.01, "interaction": -0.02}
                ),
                "std_err": pd.Series(
                    {"const": 0.01, "mps": 0.02, "mpu": 0.03, "interaction": 0.04}
                ),
                "cov": cov,
                "r_squared": 0.31,
                "n_obs": 20,
            },
        }
    return out


def test_task_plot_multiasset_missing_model_pickle_raises(tmp_path: Path) -> None:
    """Plot task should raise FileNotFoundError when model results are missing."""
    missing_models = tmp_path / "missing.pkl"
    data_path = tmp_path / "clean_tab4.pkl"
    pd.to_pickle(_make_multiasset_df(), data_path)

    with pytest.raises(FileNotFoundError):
        task_mod.task_table4_multiasset_figures(
            models_path=missing_models,
            data_path=data_path,
            mps_by_spec_plot=tmp_path / "mps.png",
            marginal_plot=tmp_path / "marginal.png",
            r2_plot=tmp_path / "r2.png",
        )


def test_task_plot_multiasset_calls_all_plot_builders(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Plot task should call each plotting function with expected output paths."""
    models_path = tmp_path / "table4_multiasset_results.pkl"
    data_path = tmp_path / "clean_tab4.pkl"
    pd.to_pickle(_make_results(), models_path)
    pd.to_pickle(_make_multiasset_df(), data_path)

    calls = {"mps": None, "marginal": None, "r2": None}

    def _fake_mps(_results, output):
        """Record the MPS-by-spec output path passed to the plotting helper."""
        calls["mps"] = output

    def _fake_marginal(_results, _df, output):
        """Record the marginal-effects output path passed to the plotting helper."""
        calls["marginal"] = output

    def _fake_r2(_results, output):
        """Record the heatmap output path passed to the plotting helper."""
        calls["r2"] = output

    monkeypatch.setattr(task_mod, "plot_mps_by_spec_panel", _fake_mps)
    monkeypatch.setattr(task_mod, "plot_marginal_effect_curves", _fake_marginal)
    monkeypatch.setattr(task_mod, "plot_r2_heatmap", _fake_r2)

    out_mps = tmp_path / "mps.png"
    out_marginal = tmp_path / "marginal.png"
    out_r2 = tmp_path / "r2.png"
    task_mod.task_table4_multiasset_figures(
        models_path=models_path,
        data_path=data_path,
        mps_by_spec_plot=out_mps,
        marginal_plot=out_marginal,
        r2_plot=out_r2,
    )

    assert calls["mps"] == out_mps
    assert calls["marginal"] == out_marginal
    assert calls["r2"] == out_r2


pytestmark = pytest.mark.integration
