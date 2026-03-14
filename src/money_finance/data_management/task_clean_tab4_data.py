"""Clean Table 4 replication dataset."""

from pathlib import Path

import pandas as pd
import pytask

from money_finance.config import BLD, ROOT
from money_finance.data_management.clean_tab4 import clean_tab4


@pytask.task
def task_clean_tab4(
    raw_data: Path = ROOT / "data" / "tab4data.csv",
    produces: Path = BLD / "data" / "clean_tab4.pkl",
) -> None:
    """Clean tab4 dataset and store as pickle."""
    df = pd.read_csv(raw_data)
    df_clean = clean_tab4(df)

    produces.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_pickle(produces)
