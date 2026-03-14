"""Pytask task for generating multi-asset Table 4 figure outputs."""

from pathlib import Path
from typing import Annotated

import pandas as pd
import pytask

from money_finance.config import BLD
from money_finance.final.plot_table4_multiasset import (
    plot_marginal_effect_curves,
    plot_mps_by_spec_panel,
    plot_r2_heatmap,
)


@pytask.task
def task_table4_multiasset_figures(
    models_path: Path = BLD / "models" / "table4_multiasset_results.pkl",
    data_path: Path = BLD / "data" / "clean_tab4.pkl",
    mps_by_spec_plot: Annotated[Path, pytask.Product] = BLD
    / "figures"
    / "table4_multiasset_mps_by_spec_panel.png",
    marginal_plot: Annotated[Path, pytask.Product] = BLD
    / "figures"
    / "table4_multiasset_marginal_effects.png",
    r2_plot: Annotated[Path, pytask.Product] = BLD
    / "figures"
    / "table4_multiasset_r2_heatmap.png",
) -> None:
    """Load the Table 4 model results and create the figure outputs.

    Writes the coefficient-path, marginal-effect, and R-squared figures to disk.
    """
    results = pd.read_pickle(models_path)
    df = pd.read_pickle(data_path)

    plot_mps_by_spec_panel(results, mps_by_spec_plot)
    plot_marginal_effect_curves(results, df, marginal_plot)
    plot_r2_heatmap(results, r2_plot)
