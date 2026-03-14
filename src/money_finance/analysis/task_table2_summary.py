"""Pytask task for computing Table 2 summary statistics."""

from pathlib import Path

import pandas as pd
import pytask

from money_finance.analysis.table2_summary import Table2Payload, run_table2_summary
from money_finance.config import BLD, ROOT
from money_finance.data_management.load_fomc_dates import load_fomc_dates
from money_finance.data_management.load_mpu import load_mpu


@pytask.task
def task_run_table2_summary(
    fomc_dates_path: Path = ROOT / "data" / "fomc_dates.csv",
    mpu_path: Path = ROOT / "data" / "mpu.csv",
    fomc_actions_path: Path = ROOT / "data" / "fomc_actions_clean.csv",
    produces: Path = BLD / "models" / "table2_summary.pkl",
) -> None:
    """Compute and store the intermediate Table 2 results pickle.

    Args:
        fomc_dates_path: Path to the cleaned FOMC meeting-date input file.
        mpu_path: Path to the raw daily MPU series.
        fomc_actions_path: Path to the FOMC actions file used for subsample flags.
        produces: Output path for the serialized Table 2 results dictionary.

    Returns:
        None: The task writes a pickle containing the baseline table, the
        press-conference table, and the p-value table.

    """
    tight = load_fomc_dates(fomc_dates_path)
    mpu_raw = load_mpu(mpu_path)
    fomc_actions = pd.read_csv(fomc_actions_path)

    results = run_table2_summary(
        fomc_dates=tight,
        mpu_raw=mpu_raw,
        fomc_actions=fomc_actions,
    )

    produces.parent.mkdir(parents=True, exist_ok=True)
    payload: Table2Payload = {
        "sumtab": results.baseline,
        "sumtab_pc": results.press_conference,
        "ptab_ss": results.p_values,
    }
    pd.to_pickle(payload, produces)
