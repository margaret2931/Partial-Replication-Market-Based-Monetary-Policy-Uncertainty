# PARTIAL REPLICATION : MARKET-BASED MONETARY POLICY UNCERTAINTY

+++ {"part": "abstract"}

This project studies how monetary policy uncertainty (MPU) is associated with financial
market outcomes. I implement a reproducible Python pipeline that reconstructs three
empirical components from {cite}`BauerLakdawalaMueller2022`: a baseline regression for
daily S&P 500 returns, a Table 2 summary-statistics replication, and a paper-style Table
4 replication of cross-asset event-study regressions around FOMC announcements.

The workflow is organized with `pytask`, covering data loading, cleaning, estimation,
table/figure generation, and written outputs.

The central economic idea is that monetary policy announcements affect financial markets
not only through changes in the expected policy path, but also through changes in
uncertainty about that path. The paper shows that uncertainty tends to be resolved on
FOMC announcement days, that communication-intensive meetings lower uncertainty more
strongly, and that changes in uncertainty have distinct effects on asset prices. My
replication focuses on making those relationships transparent in a modular Python
workflow.

+++

```{raw} latex
\clearpage
```

## 1. Motivation and Research Question

How does monetary policy uncertainty shape the market impact of monetary policy
surprises?

This question matters because event-study evidence on monetary policy transmission has
traditionally focused on first moments: surprise changes in the current or expected path
of policy rates. {cite}`BauerLakdawalaMueller2022` argue that this is incomplete. Around
FOMC announcements, markets also revise second moments, that is, the uncertainty around
the future path of policy rates. These changes in uncertainty are economically
meaningful in their own right and may alter the measured effects of conventional
monetary policy surprises.

I address this question with three empirical components that mirror the logic of the
presentation:

1. A baseline market model linking S&P 500 returns to MPU.
1. A Table 2 replication comparing MPU changes on FOMC, non-FOMC, and press-conference
   days.
1. A multi-asset Table 4-style event-study model where the policy-shock effect varies
   with uncertainty across yields, equities, volatility, and the dollar.

## 2. Data

The analysis combines daily uncertainty data, FOMC event information, and the
event-study dataset from the replication package.

The main inputs are:

- `tab4data.csv`: event-study variables from the replication package, including
  `dSVENY10`, `mps`, `mpu`, and `mpu_lag`.
- `mpu.csv`: MPU series used in the baseline market dataset.
- `fomc_dates.csv`: FOMC meeting dates and scheduling indicators used in Table 2.
- `fomc_actions_clean.csv`: FOMC indicators merged into market data preparation.

Following the original paper, the interpretation of the asset-price responses is
central. For that reason, the dependent variables in the multi-asset regressions are
reported in economic terms rather than only as dataset abbreviations:

- `dSVENY05`: change in the five-year nominal Treasury yield.
- `dSVENY10`: change in the ten-year nominal Treasury yield.
- `dTIPSY10`: change in the ten-year TIPS yield.
- `sp_daily`: daily S&P 500 return.
- `dvix`: change in the VIX.
- `dollar_ret_pm`: return on the US Dollar index.

Throughout the paper, the prefix `d` indicates a change in the corresponding variable.
The two core explanatory variables are `mps`, the monetary policy surprise, and `mpu`,
the change in short-rate uncertainty around the FOMC announcement. In the interaction
specification, lagged uncertainty captures the ex ante uncertainty environment in which
a policy surprise arrives.

## 3. Empirical Strategy

### 3.1 Baseline Specification

The baseline regression is:

$$
\text{sp500\_return}_t = \alpha + \beta \,\text{mpu}_t + \varepsilon_t
$$

estimated with OLS.

This specification is intentionally simple. It provides a benchmark relationship between
changes in monetary policy uncertainty and daily equity returns, but it does not
identify whether uncertainty is concentrated on policy-event days, whether communication
matters, or whether policy surprises transmit differently across asset classes.

### 3.2 What Table 2 Adds

Before turning to the richer regression framework, Table 2 asks a descriptive question:
when does monetary policy uncertainty move the most? This step is important because the
original paper emphasizes an "FOMC uncertainty cycle." On average, uncertainty declines
on FOMC announcement days as policy information is revealed, and then gradually rises
again between meetings.

The replication therefore compares scheduled FOMC days with non-FOMC days in the full
sample and then compares communication-intensive meetings with other meetings in the
2012-2018 subsample. This descriptive evidence is not a substitute for the event-study
regressions, but it motivates them by showing that the timing and type of FOMC
communication matter for uncertainty.

### 3.3 What Table 4 Adds

The Table 4 model is estimated as:

$$
\Delta y_t
= \beta_0
+ \beta_1 \text{mps}_t
+ \beta_2 \text{mpu}_t
+ \beta_3 (\text{mps}_t \times \text{mpu\_lag}_t)
+ \varepsilon_t
$$

with clustered standard errors by date.

This specification extends the baseline and Table 2 in two directions. First, it studies
several asset classes jointly rather than focusing only on equity returns. Second, it
tests whether the effect of a monetary policy surprise depends on the prevailing level
of uncertainty before the announcement. In the language of the original paper, this
allows the data to speak to an uncertainty channel of monetary transmission.

## 4. Results

### 4.1 Baseline Regression Results

```{include} tables/baseline_regression.md
```

The baseline regression should be read as a benchmark rather than as the main result. It
summarizes the average association between daily changes in uncertainty and equity
returns, but it does not distinguish between ordinary days and policy-event days. Nor
can it reveal whether communication-intensive meetings or cross-asset responses drive
the relationship. For those questions, the descriptive evidence in Table 2 and the
event-study evidence in Table 4 are more informative.

### 4.2 Table 2: Descriptive Evidence on Monetary Policy Uncertainty

```{include} tables/table2_summary.md
```

Table 2 shows that MPU falls more on scheduled FOMC days than on non-FOMC days, with the
strongest declines appearing on press-conference meetings.

### 4.3 Comparing the Estimated Table 2 with the Paper-Style Version

```{figure} Table 2.png
---
alt: Screenshot of the paper-style Table 2 summary statistics.
width: 95%
align: center
---
Paper-style screenshot of the Table 2 summary-statistics replication.
```

The generated markdown table and the paper-style screenshot convey the same substantive
message. The markdown version is the direct output of the workflow, and the PNG shows
the paper-style presentation.

### 4.4 Table 4: Event-Study Evidence on Cross-Asset Transmission

```{include} tables/table4_multiasset_regression.md
```

Table 4 shows cross-asset responses to monetary policy surprises and MPU, including
yields, equities, volatility, and the dollar.

### 4.5 Comparing the Estimated Table 4 with the Paper-Style Version

```{figure} Table 4.png
---
alt: Screenshot of the paper-style multi-asset Table 4 replication.
width: 95%
align: center
---
Paper-style screenshot of the multi-asset Table 4 replication.
```

The markdown table reports the estimated coefficients, and the PNG provides the
paper-style version for comparison.

### 4.6 Interpretation

Taken together, the results support a layered interpretation. The baseline regression
shows that uncertainty is empirically relevant for asset-price movements, but by itself
it is too aggregated. Table 2 then shows that uncertainty changes are concentrated on
FOMC announcement days, and especially on communication-rich meetings. Finally, Table 4
shows that these uncertainty dynamics matter for transmission across asset classes and
for the measured effect of policy surprises.

This sequencing mirrors the original paper's argument. First, uncertainty is resolved on
FOMC days and displays systematic variation across meetings. Second, these changes in
uncertainty have distinct financial-market effects. Third, the prevailing level of
uncertainty changes how strongly policy surprises are transmitted. The replication
therefore supports the view that monetary policy uncertainty is both an outcome of Fed
communication and a state variable shaping market responses.

## 5. Reproducibility

From the project root:

```bash
pixi install
pixi run pytask
pixi run pytest
```

To view the documentation outputs interactively:

```bash
pixi run -e docs docs
pixi run -e docs view-docs
pixi run -e docs check-urls
pixi run view-paper
pixi run view-pres
```

Key generated outputs:

- `bld/data/market_data.pkl`
- `bld/data/clean_tab4.pkl`
- `bld/models/regression_results.pkl`
- `bld/models/table2_summary.pkl`
- `bld/tables/regression_summary.md`
- `documents/tables/table2_summary.md`
- `documents/Table 2.png`
- `bld/models/table4_multiasset_results.pkl`
- `documents/tables/baseline_regression.md`
- `documents/tables/table4_multiasset_regression.md`
- `documents/Table 4.png`

## 6. Conclusion

This project provides a reproducible implementation of baseline, Table 2, and
multi-asset event-study analysis for monetary policy uncertainty and financial market
responses. The resulting workflow follows the same economic logic as the original paper:
it first establishes that uncertainty is systematically resolved on FOMC announcement
days, then shows that communication-rich meetings matter particularly strongly, and
finally demonstrates that changes in uncertainty help explain cross-asset financial
market responses to monetary policy surprises. The main contribution of the project is
to translate that argument into a transparent, test-supported Python pipeline.

```{bibliography}
```
