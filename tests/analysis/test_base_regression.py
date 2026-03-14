"""Unit tests for the baseline regression analysis."""

import numpy as np
import pandas as pd
import pytest

from money_finance.analysis.base_regression import run_base_regression


def test_run_base_regression_structure():
    """Test that regression returns a statsmodels results object."""

    rng = np.random.default_rng(0)

    df = pd.DataFrame(
        {
            "sp500_return": rng.normal(size=50),
            "mpu": rng.normal(size=50),
        }
    )

    model = run_base_regression(df)

    assert hasattr(model, "params")
    assert "mpu" in model.params.index
    assert "const" in model.params.index


def test_run_base_regression_missing_columns():
    """Test that the regression raises an error if required columns are missing."""

    df = pd.DataFrame(
        {
            "mpu": [0.1, 0.2, 0.3],
        }
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        run_base_regression(df)
