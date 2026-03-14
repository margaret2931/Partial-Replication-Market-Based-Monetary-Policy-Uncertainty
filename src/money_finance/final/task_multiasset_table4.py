"""Pytask task to write multi-asset Table 4 markdown."""

from pathlib import Path
from typing import Annotated

import pytask

from money_finance.config import BLD, DOCUMENTS
from money_finance.final.multiasset_table4 import save_multiasset_table4_markdown


@pytask.task
def task_create_multiasset_table4(
    results_path: Path = BLD / "models" / "table4_multiasset_results.pkl",
    document_table: Annotated[Path, pytask.Product] = DOCUMENTS
    / "tables"
    / "table4_multiasset_regression.md",
    bld_table: Annotated[Path, pytask.Product] = BLD
    / "tables"
    / "table4_multiasset_regression.md",
) -> None:
    """Render the saved multi-asset Table 4 results as markdown in both locations.

    Writes identical markdown tables under ``documents/tables`` and ``bld/tables``.
    """
    if not results_path.exists():
        msg = f"Missing input file: {results_path}"
        raise FileNotFoundError(msg)

    save_multiasset_table4_markdown(results_path, document_table)
    save_multiasset_table4_markdown(results_path, bld_table)
