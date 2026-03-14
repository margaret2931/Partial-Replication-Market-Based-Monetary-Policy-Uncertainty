"""Integration tests for the Table 2 markdown task."""

from pathlib import Path

import pandas as pd
import pytest

from money_finance.final.task_table2 import task_create_table2_table


def test_task_create_table2_table_writes_both_markdown_outputs(tmp_path: Path) -> None:
    """Write identical markdown outputs to the documents and build directories."""
    results_path = tmp_path / "models" / "table2_summary.pkl"
    document_table = tmp_path / "documents" / "tables" / "table2_summary.md"
    bld_table = tmp_path / "bld" / "tables" / "table2_summary.md"
    results_path.parent.mkdir(parents=True, exist_ok=True)

    pd.to_pickle(
        {
            "sumtab": pd.DataFrame({"mpu_fomc": [2.0]}, index=["Obs"]),
            "sumtab_pc": pd.DataFrame({"mpuall": [1.0]}, index=["Obs"]),
            "ptab_ss": pd.DataFrame({"p_value": [0.1]}, index=["fomc_mean_eq_0"]),
        },
        results_path,
    )

    task_create_table2_table(
        results_path=results_path,
        document_table=document_table,
        bld_table=bld_table,
    )

    assert document_table.exists()
    assert bld_table.exists()
    content = bld_table.read_text()
    assert document_table.read_text() == content
    assert "**Panel A. Baseline Sample: January 1994 to September 2020**" in content
    assert "**Mean Tests**" in content


pytestmark = pytest.mark.integration
