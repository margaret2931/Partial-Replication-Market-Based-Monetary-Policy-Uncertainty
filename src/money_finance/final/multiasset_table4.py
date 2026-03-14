"""Create paper-style Table 4 (multi-asset) as markdown."""

from pathlib import Path

import pandas as pd

TOP_PANEL = [
    ("Five-year nominal yield", "dSVENY05"),
    ("Ten-year nominal yield", "dSVENY10"),
    ("Ten-year TIPS yield", "dTIPSY10"),
]

BOTTOM_PANEL = [
    ("S&P 500", "sp_daily"),
    ("VIX", "dvix"),
    ("Dollar index", "dollar_ret_pm"),
]

SPECS = ("1", "2", "3")


def _get_t_stat(result: dict, param: str) -> float | None:
    """Compute a t-statistic from stored coefficient and standard-error values.

    Returns ``None`` when the coefficient is unavailable or not identified.
    """
    coef = result["coef"].get(param)
    se = result["std_err"].get(param)
    if coef is None or se is None or se == 0:
        return None
    return coef / se


def _fmt_coef_t(result: dict, param: str, digits: int = 2) -> str:
    """Format one coefficient entry for the markdown Table 4 output.

    Includes the t-statistic in brackets when it can be computed.
    """
    coef = result["coef"].get(param)
    t_stat = _get_t_stat(result, param)
    if coef is None:
        return ""
    if t_stat is None:
        return f"{coef:.{digits}f}"
    return f"{coef:.{digits}f} [{t_stat:.{digits}f}]"


def _panel_markdown(
    results: dict, panel_assets: list[tuple[str, str]], panel_title: str
) -> str:
    """Build one markdown panel for the multi-asset Table 4 output.

    Expands the selected assets across all three reported specifications.
    """
    columns = ["Variable"]
    for label, _asset in panel_assets:
        columns.extend([f"{label} ({spec})" for spec in SPECS])

    rows: list[dict[str, str]] = []

    def row_for(param_label: str, param_name: str) -> dict[str, str]:
        """Construct one formatted row across all assets and specifications.

        Each cell contains the stored coefficient display for one model.
        """
        row = {"Variable": param_label}
        for label, asset in panel_assets:
            for spec in SPECS:
                key = f"{label} ({spec})"
                row[key] = _fmt_coef_t(results[asset][spec], param_name)
        return row

    rows.append(row_for("MPS", "mps"))
    rows.append(row_for("MPU", "mpu"))
    rows.append(row_for("MPS * SRU_{-1}", "interaction"))

    r2_row = {"Variable": "R^2"}
    for label, asset in panel_assets:
        for spec in SPECS:
            key = f"{label} ({spec})"
            r2_row[key] = f"{results[asset][spec]['r_squared']:.2f}"
    rows.append(r2_row)

    panel_df = pd.DataFrame(rows, columns=columns).fillna("")
    return f"### {panel_title}\n\n" + panel_df.to_markdown(index=False) + "\n"


def build_multiasset_table4_markdown(results: dict) -> str:
    """Assemble the full markdown version of the multi-asset Table 4.

    Args:
        results: Serialized regression results grouped by asset and specification.

    Returns:
        Markdown string containing both Table 4 panels and the table note.

    """
    top = _panel_markdown(results, TOP_PANEL, "Panel A")
    bottom = _panel_markdown(results, BOTTOM_PANEL, "Panel B")
    title = "# Table 4. Transmission of Monetary Policy Uncertainty "
    "to Financial Markets\n\n"
    note = (
        "\n**Notes:** Entries show coefficient estimates with "
        "t-statistics in brackets. "
        "Standard errors are clustered by date.\n"
    )
    return title + top + "\n" + bottom + note


def save_multiasset_table4_markdown(results_path: Path, output_path: Path) -> None:
    """Load serialized Table 4 results and write the markdown table to disk.

    Args:
        results_path: Path to the serialized multi-asset regression results.
        output_path: Destination path for the markdown table.

    Returns:
        None. The function writes the rendered markdown file to disk.

    """
    results = pd.read_pickle(results_path)
    markdown = build_multiasset_table4_markdown(results)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown)
