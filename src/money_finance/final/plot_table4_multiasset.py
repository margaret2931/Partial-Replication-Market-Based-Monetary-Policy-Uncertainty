"""Create multi-asset Table 4 figures from stored regression outputs."""

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ASSETS = (
    "dSVENY05",
    "dSVENY10",
    "dTIPSY10",
    "sp_daily",
    "dvix",
    "dollar_ret_pm",
)

ASSET_LABELS = {
    "dSVENY05": "5Y nominal yield",
    "dSVENY10": "10Y nominal yield",
    "dTIPSY10": "10Y TIPS yield",
    "sp_daily": "S&P 500",
    "dvix": "VIX",
    "dollar_ret_pm": "Dollar index",
}


def _lag_col_from_df(df: pd.DataFrame) -> str:
    """Return the lagged uncertainty column available in the plotting data.

    Accepts either of the lag naming conventions used in the cleaned dataset.
    """
    if "mpu_lag" in df.columns:
        return "mpu_lag"
    if "mpu_level_lag" in df.columns:
        return "mpu_level_lag"
    msg = "Missing lag column: expected 'mpu_lag' or 'mpu_level_lag'."
    raise ValueError(msg)


def _save(fig: go.Figure, output_path: Path) -> None:
    """Write a Plotly figure to disk and create parent directories if needed.

    Figures are exported as static image files.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_image(str(output_path), scale=2)


def plot_mps_by_spec_panel(results: dict, output_path: Path) -> None:
    """Plot the MPS coefficient path across specifications for each asset.

    Args:
        results: Serialized regression results grouped by asset and specification.
        output_path: Destination path for the exported figure.

    Returns:
        None. The figure is written to disk.

    """
    fig = make_subplots(
        rows=2,
        cols=3,
        subplot_titles=[ASSET_LABELS[a] for a in ASSETS],
        horizontal_spacing=0.08,
        vertical_spacing=0.12,
    )

    x_specs = [1, 2, 3]
    x_labels = ["Spec 1", "Spec 2", "Spec 3"]

    for i, asset in enumerate(ASSETS):
        row = i // 3 + 1
        col = i % 3 + 1

        y = []
        err = []
        for spec in ("1", "2", "3"):
            model = results[asset][spec]
            coef = model["coef"].get("mps", np.nan)
            se = model["std_err"].get("mps", np.nan)
            y.append(coef)
            err.append(1.96 * se if pd.notna(se) else np.nan)

        fig.add_trace(
            go.Scatter(
                x=x_specs,
                y=y,
                mode="lines+markers",
                marker={"size": 7},
                error_y={"type": "data", "array": err, "visible": True},
                showlegend=False,
            ),
            row=row,
            col=col,
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=row, col=col)
        fig.update_xaxes(
            tickmode="array",
            tickvals=x_specs,
            ticktext=x_labels,
            row=row,
            col=col,
        )

    fig.update_layout(
        template="simple_white",
        title="MPS Coefficient by Specification, by Dependent Variable",
        height=780,
        width=1180,
    )
    _save(fig, output_path)


def plot_marginal_effect_curves(
    results: dict,
    df: pd.DataFrame,
    output_path: Path,
) -> None:
    """Plot the specification (3) marginal effect of MPS over lagged uncertainty.

    Args:
        results: Serialized regression results grouped by asset and specification.
        df: Cleaned event-study dataset used to define the lagged-uncertainty grid.
        output_path: Destination path for the exported figure.

    Returns:
        None. The figure is written to disk.

    Raises:
        ValueError: If the cleaned data does not contain a recognized lag column.

    """
    lag_col = _lag_col_from_df(df)
    x_min = df[lag_col].quantile(0.05)
    x_max = df[lag_col].quantile(0.95)

    fig = make_subplots(
        rows=2,
        cols=3,
        subplot_titles=[ASSET_LABELS[a] for a in ASSETS],
        horizontal_spacing=0.08,
        vertical_spacing=0.12,
    )

    for i, asset in enumerate(ASSETS):
        row = i // 3 + 1
        col = i % 3 + 1
        spec3 = results[asset]["3"]

        sample = df[[asset, "mps", lag_col]].dropna()
        if sample.empty:
            fig.add_annotation(
                x=0.5,
                y=0.5,
                xref=f"x{i + 1} domain",
                yref=f"y{i + 1} domain",
                text="No valid sample",
                showarrow=False,
            )
            continue

        lag_grid = np.linspace(x_min, x_max, 200)

        b1 = spec3["coef"].get("mps", np.nan)
        b3 = spec3["coef"].get("interaction", np.nan)
        cov = spec3["cov"]

        v11 = cov.loc["mps", "mps"]
        v33 = cov.loc["interaction", "interaction"]
        v13 = cov.loc["mps", "interaction"]

        marginal = b1 + b3 * lag_grid
        var_marginal = v11 + (lag_grid**2) * v33 + 2 * lag_grid * v13
        se_marginal = np.sqrt(np.maximum(var_marginal, 0.0))
        upper = marginal + 1.96 * se_marginal
        lower = marginal - 1.96 * se_marginal

        finite = np.isfinite(marginal) & np.isfinite(upper) & np.isfinite(lower)
        if not finite.any():
            fig.add_annotation(
                x=0.5,
                y=0.5,
                xref=f"x{i + 1} domain",
                yref=f"y{i + 1} domain",
                text="Non-finite estimates",
                showarrow=False,
            )
            continue

        x = lag_grid[finite]
        y = marginal[finite]
        lo = lower[finite]
        up = upper[finite]

        fig.add_trace(
            go.Scatter(x=x, y=up, mode="lines", line={"width": 0}, showlegend=False),
            row=row,
            col=col,
        )
        fig.add_trace(
            go.Scatter(
                x=x,
                y=lo,
                mode="lines",
                fill="tonexty",
                line={"width": 0},
                name="95% CI" if i == 0 else None,
                showlegend=i == 0,
            ),
            row=row,
            col=col,
        )
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                name="Marginal effect" if i == 0 else None,
                showlegend=i == 0,
            ),
            row=row,
            col=col,
        )
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=row, col=col)

    fig.update_layout(
        template="simple_white",
        title="Spec (3) Marginal Effect of MPS Across SRU_{-1}",
        height=780,
        width=1180,
    )
    _save(fig, output_path)


def plot_r2_heatmap(results: dict, output_path: Path) -> None:
    """Plot a heatmap of R-squared values by asset and specification.

    Args:
        results: Serialized regression results grouped by asset and specification.
        output_path: Destination path for the exported figure.

    Returns:
        None. The figure is written to disk.

    """
    z = [
        [results[asset][spec]["r_squared"] for spec in ("1", "2", "3")]
        for asset in ASSETS
    ]

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=["Spec 1", "Spec 2", "Spec 3"],
            y=[ASSET_LABELS[a] for a in ASSETS],
            text=np.round(np.array(z), 2),
            texttemplate="%{text}",
            colorscale="Blues",
        )
    )
    fig.update_layout(
        template="simple_white",
        title="R² by Asset and Specification",
        xaxis_title="Specification",
        yaxis_title="Asset",
    )
    _save(fig, output_path)
