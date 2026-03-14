"""Integration tests for the Table 2 summary task."""

from pathlib import Path

import pandas as pd
import pytest

import money_finance.analysis.task_table2_summary as task_mod
from money_finance.analysis.table2_summary import Table2Results


def test_task_run_table2_summary_writes_expected_pickle(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Serialize baseline, press-conference, and p-value tables to the output pickle."""
    baseline = pd.DataFrame({"mpu_fomc": [2.0]}, index=["Obs"])
    press_conference = pd.DataFrame({"mpuall": [1.0]}, index=["Obs"])
    p_values = pd.DataFrame({"p_value": [0.1]}, index=["fomc_mean_eq_0"])

    monkeypatch.setattr(task_mod, "load_fomc_dates", lambda _: pd.DataFrame())
    monkeypatch.setattr(task_mod, "load_mpu", lambda _: pd.DataFrame())
    monkeypatch.setattr(task_mod.pd, "read_csv", lambda _: pd.DataFrame())
    monkeypatch.setattr(
        task_mod,
        "run_table2_summary",
        lambda **_: Table2Results(
            baseline=baseline,
            press_conference=press_conference,
            p_values=p_values,
        ),
    )

    out = tmp_path / "models" / "table2_summary.pkl"
    task_mod.task_run_table2_summary(
        fomc_dates_path=tmp_path / "fomc_dates.csv",
        mpu_path=tmp_path / "mpu.csv",
        fomc_actions_path=tmp_path / "fomc_actions_clean.csv",
        produces=out,
    )

    assert out.exists()
    results = pd.read_pickle(out)
    assert results["sumtab"].equals(baseline)
    assert results["sumtab_pc"].equals(press_conference)
    assert results["ptab_ss"].equals(p_values)


pytestmark = pytest.mark.integration
