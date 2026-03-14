"""Replicate Table 2 summary statistics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict

import numpy as np
import pandas as pd
import statsmodels.api as sm

MIN_SKEW_OBS = 2
ROW_INDEX: list[str] = [
    "Obs",
    "Mean",
    "tstat_mean",
    "Std. Dev.",
    "Skewness",
    "Cumulative change",
]


@dataclass(frozen=True)
class Table2Results:
    baseline: pd.DataFrame
    press_conference: pd.DataFrame
    p_values: pd.DataFrame


class Table2Payload(TypedDict):
    """Serialized Table 2 tables stored in the intermediate pickle."""

    sumtab: pd.DataFrame
    sumtab_pc: pd.DataFrame
    ptab_ss: pd.DataFrame


def _robust_mean_test(series: pd.Series) -> tuple[float, float]:
    """Estimate a robust test of whether the sample mean equals zero.

    Returns the p-value and t-statistic from an intercept-only regression.
    """
    clean = series.dropna()
    if clean.empty:
        return np.nan, np.nan

    x = np.ones((len(clean), 1))
    model = sm.OLS(clean.to_numpy(), x).fit(cov_type="HC1")
    return float(model.pvalues[0]), float(model.tvalues[0])


def _summary_column(series: pd.Series, name: str) -> pd.DataFrame:
    """Summarize one series as a single Table 2 output column.

    Computes the observation count, central moments, and cumulative change.
    """
    clean = series.dropna()
    _pval, t_stat = _robust_mean_test(clean)

    values = [
        float(clean.shape[0]),
        float(clean.mean()) if not clean.empty else np.nan,
        t_stat,
        float(clean.std(ddof=1)) if clean.shape[0] > 1 else np.nan,
        float(clean.skew()) if clean.shape[0] > MIN_SKEW_OBS else np.nan,
        float(clean.sum()) if not clean.empty else np.nan,
    ]
    return pd.DataFrame({name: values}, index=ROW_INDEX)


def _prepare_mpu_data(mpu_raw: pd.DataFrame) -> pd.DataFrame:
    """Prepare the daily MPU input for the Table 2 calculations.

    Converts dates and values, preserves the level series, and computes daily changes.
    """
    mpu_tt = mpu_raw.copy()
    mpu_tt["date"] = pd.to_datetime(mpu_tt["date"], format="mixed", errors="coerce")
    mpu_tt = mpu_tt.sort_values("date").drop_duplicates("date")
    mpu_tt["mpu"] = pd.to_numeric(mpu_tt["mpu"], errors="coerce")
    mpu_tt["mpu_level"] = mpu_tt["mpu"]
    mpu_tt["mpu"] = mpu_tt["mpu_level"].diff()
    return mpu_tt


def _build_baseline_tables(
    alldata: pd.DataFrame,
    strt_con: pd.Timestamp,
    last_con: pd.Timestamp,
    crisis_start: pd.Timestamp,
    crisis_last: pd.Timestamp,
    excluded_dates: set[pd.Timestamp],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Construct the baseline-sample FOMC and non-FOMC summary tables.

    Args:
        alldata: Merged daily dataset containing FOMC indicators and MPU measures.
        strt_con: Inclusive start date for the baseline sample.
        last_con: Inclusive end date for the baseline sample.
        crisis_start: Inclusive start of the crisis period to exclude.
        crisis_last: Inclusive end of the crisis period to exclude.
        excluded_dates: Individual dates excluded from the effective sample.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Effective FOMC sample used
        downstream, the baseline summary-statistics table, and the table of p-values
        for mean tests.

    """
    allfomcdata = alldata.loc[alldata["mp1"].notna()].copy()
    tmpdata = allfomcdata.loc[allfomcdata["date"].between(strt_con, last_con)].copy()
    tmpdata = tmpdata.loc[
        ~tmpdata["date"].between(crisis_start, crisis_last)
        & ~tmpdata["date"].isin(excluded_dates)
    ].copy()
    tmpdata = tmpdata.loc[tmpdata["unscheduled"] != 1].copy()

    fomcdataeff = tmpdata.copy()
    fomcdataeff["fomcdum"] = 1

    alldata = alldata.merge(fomcdataeff[["date", "fomcdum"]], on="date", how="left")
    alldata["fomcdum"] = alldata["fomcdum"].fillna(0).astype(int)

    allfomcind = alldata["mp1"].notna()
    alldata["fomc_notin_sample"] = (allfomcind & (alldata["fomcdum"] == 0)).astype(int)
    alldata["allfomc"] = allfomcind.astype(int)

    mpufomcinsample = fomcdataeff["mpu"]
    sumtabfomc = _summary_column(mpufomcinsample, "mpu_fomc")

    alldataeff1 = alldata.loc[alldata["date"].between(strt_con, last_con)].copy()
    alldataeff1 = alldataeff1.loc[
        ~alldataeff1["date"].between(crisis_start, crisis_last)
        & ~alldataeff1["date"].isin(excluded_dates)
    ].copy()
    nonfomc_mask = (alldataeff1["fomcdum"] == 0) & (
        alldataeff1["fomc_notin_sample"] == 0
    )
    mpunotfomc = alldataeff1.loc[nonfomc_mask, "mpu"]
    sumtabnonfomc = _summary_column(mpunotfomc, "mpu_nonfomc")

    pfomc, _ = _robust_mean_test(mpufomcinsample)
    pnfomc, _ = _robust_mean_test(mpunotfomc)
    pfnf = float(
        sm.stats.ttest_ind(
            mpufomcinsample.dropna(),
            mpunotfomc.dropna(),
            usevar="unequal",
        )[1]
    )

    sumtab = pd.concat([sumtabfomc, sumtabnonfomc], axis=1)
    ptab_ss = pd.DataFrame(
        {"p_value": [pfomc, pnfomc, pfnf]},
        index=["fomc_mean_eq_0", "nonfomc_mean_eq_0", "fomc_vs_nonfomc"],
    )
    return fomcdataeff, sumtab, ptab_ss


def _to_indicator(series: pd.Series) -> pd.Series:
    """Convert a raw flag column into a clean integer indicator.

    Non-numeric values are coerced and missing values are treated as zero.
    """
    return pd.to_numeric(series, errors="coerce").fillna(0).astype(int)


def _build_press_conference_table(
    fomcdataeff: pd.DataFrame,
    fomc_actions: pd.DataFrame,
    strt_con: pd.Timestamp,
    last_con: pd.Timestamp,
) -> pd.DataFrame:
    """Construct the press-conference subsample summary table.

    Args:
        fomcdataeff: Effective scheduled FOMC sample with MPU changes.
        fomc_actions: Raw FOMC action indicators loaded from the replication data.
        strt_con: Inclusive start date for the full analysis window.
        last_con: Inclusive end date for the full analysis window.

    Returns:
        pd.DataFrame: Summary-statistics table for all FOMC dates, press-conference
        dates, and non-press-conference dates in the 2012-2018 subsample.

    """
    tmp = fomc_actions.copy()
    tmp["date"] = pd.to_datetime(tmp.iloc[:, 0], format="mixed", errors="coerce")
    datafomcactions = tmp.iloc[:, 2:].copy()

    schedfomcdum = _to_indicator(datafomcactions.iloc[:, 1])
    sepdum = _to_indicator(datafomcactions.iloc[:, 3])
    confdum = _to_indicator(datafomcactions.iloc[:, 0])

    factions = pd.DataFrame(
        {
            "date": tmp["date"],
            "SEP": sepdum,
            "SchedFOMC_noSEP": schedfomcdum & (1 - sepdum),
            "PC": confdum,
            "SchedFOMC_noPC": schedfomcdum & (1 - confdum),
            "SchedFOMC_pc": schedfomcdum & confdum,
        }
    )
    factions = factions.loc[factions["date"].between(strt_con, last_con)].copy()

    mpu_vars = fomcdataeff[["date", "mpu", "fomcdum"]].copy()
    mpu_fomcactions = mpu_vars.merge(factions, on="date", how="outer")
    mpu_fomcactions = mpu_fomcactions.loc[mpu_fomcactions["fomcdum"].notna()].copy()

    fomc_sep = mpu_fomcactions.loc[
        mpu_fomcactions["date"].between(
            pd.Timestamp("2012-01-01"), pd.Timestamp("2018-12-31")
        )
    ].copy()
    fomc_sep["noSEP"] = fomc_sep["SchedFOMC_noSEP"]
    fomc_sep["noPC"] = fomc_sep["SchedFOMC_noPC"]

    sumtaballfomc = _summary_column(fomc_sep["mpu"], "mpuall")
    sumtabpc = _summary_column(fomc_sep.loc[fomc_sep["PC"] == 1, "mpu"], "mpupc")
    sumtabnopc = _summary_column(fomc_sep.loc[fomc_sep["noPC"] == 1, "mpu"], "mpunopc")
    return pd.concat([sumtaballfomc, sumtabpc, sumtabnopc], axis=1)


def run_table2_summary(
    fomc_dates: pd.DataFrame,
    mpu_raw: pd.DataFrame,
    fomc_actions: pd.DataFrame,
) -> Table2Results:
    """Replicate the summary statistics reported in Table 2.

    Args:
        fomc_dates: Daily FOMC-date dataset with meeting surprise and scheduling
            indicators.
        mpu_raw: Daily monetary policy uncertainty series before differencing.
        fomc_actions: FOMC action file used to identify press conferences and SEP
            releases.

    Returns:
        Table2Results: Baseline-sample summary statistics, press-conference-subsample
        summary statistics, and p-values for the reported mean tests.

    """
    strt_con = pd.Timestamp("1994-01-01")
    last_con = pd.Timestamp("2020-09-30")

    crisis_start = pd.Timestamp("2007-07-01")
    crisis_last = pd.Timestamp("2009-06-30")
    excluded_dates = {pd.Timestamp("2001-09-17")}

    tight = fomc_dates.copy()
    mpu_tt = _prepare_mpu_data(mpu_raw)

    alldata = tight.merge(mpu_tt[["date", "mpu", "mpu_level"]], on="date", how="outer")
    alldata = alldata.sort_values("date").reset_index(drop=True)

    fomcdataeff, sumtab, ptab_ss = _build_baseline_tables(
        alldata=alldata,
        strt_con=strt_con,
        last_con=last_con,
        crisis_start=crisis_start,
        crisis_last=crisis_last,
        excluded_dates=excluded_dates,
    )
    sumtab_pc = _build_press_conference_table(
        fomcdataeff=fomcdataeff,
        fomc_actions=fomc_actions,
        strt_con=strt_con,
        last_con=last_con,
    )

    return Table2Results(
        baseline=sumtab,
        press_conference=sumtab_pc,
        p_values=ptab_ss,
    )
