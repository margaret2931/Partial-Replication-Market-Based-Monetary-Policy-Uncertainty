"""Tests for the baseline regression plot helper."""

from pathlib import Path

import numpy as np
import pandas as pd

from money_finance.final.base_regression_plot import base_regression_plot_fit


def test_base_regression_plot_creates_file(tmp_path: Path) -> None:
    """Test that the baseline regression plotting helper writes an output file."""
    rng = np.random.default_rng(0)

    df = pd.DataFrame(
        {
            "sp500_return": rng.normal(size=20),
            "mpu": rng.normal(size=20),
        }
    )

    output_file = tmp_path / "plot.png"

    base_regression_plot_fit(df, output_file)

    assert output_file.exists()
