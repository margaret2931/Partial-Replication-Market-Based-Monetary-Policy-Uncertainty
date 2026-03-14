"""Unit tests for multi-asset Table 4 plotting helpers."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import money_finance.final.plot_table4_multiasset as plot_mod

N_ASSETS = len(plot_mod.ASSETS)
N_SPECS = 3


def _make_results() -> dict:
    """Build synthetic multi-asset regression results for plotting tests."""
    cov = pd.DataFrame(
        [[0.04, 0.0, 0.0], [0.0, 0.09, 0.01], [0.0, 0.01, 0.16]],
        index=["mps", "mpu", "interaction"],
        columns=["mps", "mpu", "interaction"],
    )

    out = {}
    for idx, asset in enumerate(plot_mod.ASSETS, start=1):
        out[asset] = {
            "1": {
                "coef": pd.Series({"const": 0.0, "mps": 0.10 * idx}),
                "std_err": pd.Series({"const": 0.01, "mps": 0.02}),
                "cov": cov,
                "r_squared": 0.1 + 0.01 * idx,
                "n_obs": 50,
            },
            "2": {
                "coef": pd.Series({"const": 0.0, "mps": 0.12 * idx, "mpu": 0.01}),
                "std_err": pd.Series({"const": 0.01, "mps": 0.02, "mpu": 0.03}),
                "cov": cov,
                "r_squared": 0.2 + 0.01 * idx,
                "n_obs": 50,
            },
            "3": {
                "coef": pd.Series(
                    {"const": 0.0, "mps": 0.14 * idx, "mpu": 0.01, "interaction": -0.03}
                ),
                "std_err": pd.Series(
                    {"const": 0.01, "mps": 0.02, "mpu": 0.03, "interaction": 0.04}
                ),
                "cov": cov,
                "r_squared": 0.3 + 0.01 * idx,
                "n_obs": 50,
            },
        }
    return out


def _make_data() -> pd.DataFrame:
    """Create synthetic dataframe containing mps, uncertainty, lag, and asset series."""
    n = 80
    x = np.linspace(-1, 1, n)
    df = pd.DataFrame(
        {
            "mps": x,
            "mpu": x * 0.1,
            "mpu_lag": np.linspace(-0.5, 0.5, n),
        }
    )
    for i, asset in enumerate(plot_mod.ASSETS, start=1):
        df[asset] = 0.05 * i + 0.2 * df["mps"] + 0.1 * df["mpu_lag"]
    return df


def test_plot_marginal_effect_curves_missing_lag_raises(monkeypatch) -> None:
    """Marginal-effect plot should fail with a clear error when lag column is absent."""
    captured = {}

    def _fake_save(fig, output_path):
        """Capture saved figure output for assertions."""
        captured["fig"] = fig
        captured["path"] = output_path

    monkeypatch.setattr(plot_mod, "_save", _fake_save)

    df = _make_data().drop(columns=["mpu_lag"])
    with pytest.raises(ValueError, match="Missing lag column"):
        plot_mod.plot_marginal_effect_curves(_make_results(), df, Path("x.png"))


def test_plot_mps_by_spec_panel_builds_one_trace_per_asset(monkeypatch) -> None:
    """MPS-by-spec panel should produce one trace per asset subplot."""
    captured = {}

    def _fake_save(fig, output_path):
        """Capture saved figure output for assertions."""
        captured["fig"] = fig
        captured["path"] = output_path

    monkeypatch.setattr(plot_mod, "_save", _fake_save)

    out = Path("dummy.png")
    plot_mod.plot_mps_by_spec_panel(_make_results(), out)

    assert captured["path"] == out
    assert len(captured["fig"].data) == N_ASSETS


def test_plot_marginal_effect_curves_builds_expected_traces(monkeypatch) -> None:
    """Marginal-effects figure should create expected traces across all asset panels."""
    captured = {}

    def _fake_save(fig, output_path):
        """Capture saved figure output for assertions."""
        captured["fig"] = fig
        captured["path"] = output_path

    monkeypatch.setattr(plot_mod, "_save", _fake_save)

    out = Path("marginal.png")
    plot_mod.plot_marginal_effect_curves(_make_results(), _make_data(), out)

    assert len(captured["fig"].data) == N_ASSETS * N_SPECS
    assert captured["path"] == out


def test_plot_r2_heatmap_has_asset_by_spec_matrix(monkeypatch) -> None:
    """R2 heatmap should encode an assets-by-specifications matrix."""
    captured = {}

    def _fake_save(fig, output_path):
        """Capture saved figure output for assertions."""
        captured["fig"] = fig
        captured["path"] = output_path

    monkeypatch.setattr(plot_mod, "_save", _fake_save)

    out = Path("r2.png")
    plot_mod.plot_r2_heatmap(_make_results(), out)

    z = captured["fig"].data[0]["z"]
    assert len(z) == N_ASSETS
    assert len(z[0]) == N_SPECS
    assert captured["path"] == out


pytestmark = pytest.mark.unit
