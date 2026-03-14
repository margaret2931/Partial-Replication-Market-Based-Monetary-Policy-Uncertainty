"""Write Table 2 markdown output."""

from pathlib import Path
from typing import Annotated

import pandas as pd
import pytask

from money_finance.analysis.table2_summary import Table2Payload
from money_finance.config import BLD, DOCUMENTS


@pytask.task
def task_create_table2_table(
    results_path: Path = BLD / "models" / "table2_summary.pkl",
    document_table: Annotated[Path, pytask.Product] = DOCUMENTS
    / "tables"
    / "table2_summary.md",
    bld_table: Annotated[Path, pytask.Product] = BLD / "tables" / "table2_summary.md",
) -> None:
    """Render the saved Table 2 results as markdown in both output locations.

    Args:
        results_path: Path to the pickle produced by the Table 2 analysis task.
        document_table: Markdown output path under ``documents/tables``.
        bld_table: Markdown output path under ``bld/tables``.

    Returns:
        None: The task writes identical markdown tables to both destinations.

    """
    results: Table2Payload = pd.read_pickle(results_path)

    sumtab = results["sumtab"]
    sumtab_pc = results["sumtab_pc"]
    ptab_ss = results["ptab_ss"]

    content = (
        "**Panel A. Baseline Sample: January 1994 to September 2020**\n\n"
        f"{sumtab.to_markdown()}\n\n"
        "**Panel B. Press Conference Sample: January 2012 to December 2018**\n\n"
        f"{sumtab_pc.to_markdown()}\n\n"
        "**Mean Tests**\n\n"
        f"{ptab_ss.to_markdown()}\n"
    )

    document_table.parent.mkdir(parents=True, exist_ok=True)
    bld_table.parent.mkdir(parents=True, exist_ok=True)

    document_table.write_text(content)
    bld_table.write_text(content)
