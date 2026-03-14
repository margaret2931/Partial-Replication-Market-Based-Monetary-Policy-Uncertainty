"""Tasks for compiling the paper."""

import subprocess
from pathlib import Path

import pytask

from money_finance.config import DOCUMENTS, ROOT


@pytask.task(id="paper-html")
def task_compile_paper_html(
    paper_md: Path = DOCUMENTS / "paper.md",
    myst_yml: Path = ROOT / "myst.yml",
    baseline_table: Path = DOCUMENTS / "tables" / "baseline_regression.md",
    table2_table: Path = DOCUMENTS / "tables" / "table2_summary.md",
    table2_figure: Path = DOCUMENTS / "Table 2.png",
    table4_table: Path = DOCUMENTS / "tables" / "table4_multiasset_regression.md",
    table4_figure: Path = DOCUMENTS / "Table 4.png",
    produces: Path = ROOT / "_build" / "html" / "index.html",
) -> None:
    """Compile the paper (HTML only)."""
    subprocess.run(
        ("jupyter", "book", "build", "--html"),
        check=True,
        cwd=ROOT,
    )
