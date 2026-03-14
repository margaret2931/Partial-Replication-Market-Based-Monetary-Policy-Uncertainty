---
theme: academic
class: text-center
highlighter: shiki
lineNumbers: false
transition: fade
title: "PARTIAL REPLICATION : MARKET-BASED MONETARY POLICY UNCERTAINTY"
mdc: true
defaults:
  layout: center
---

# PARTIAL REPLICATION : MARKET-BASED MONETARY POLICY UNCERTAINTY

MARGARET VINCENT

UNIVERSITY OF BONN

---

# Motivation

How does monetary policy uncertainty change financial market responses to policy surprises?

This project provides a reproducible empirical pipeline to study:

- Baseline relation: `sp500_return ~ mpu`
- Table 2 replication: how MPU differs across FOMC, non-FOMC, and press-conference days
- Multi-asset Table 4 replication: heterogeneous responses across financial markets
- Reproducible outputs: cleaned data, models, tables, figures, and tests

The Table 4 replication follows Bauer, Lakdawala, and Mueller (2022) and uses event-study
data collected from the paper's replication package.

---

# Data

Main inputs:

- `data/tab4data.csv` (event-study variables)
- `data/mpu.csv` (MPU series)
- `data/fomc_dates.csv` (FOMC schedule and meeting indicators)
- `data/fomc_actions_clean.csv` (FOMC indicators)

---

# Dependent Variables

The multi-asset regressions use six dependent variables:

- `dSVENY05`: change in 5-year nominal Treasury yield
- `dSVENY10`: change in 10-year nominal Treasury yield
- `dTIPSY10`: change in 10-year TIPS yield
- `sp_daily`: daily S&P 500 return
- `dvix`: change in the VIX
- `dollar_ret_pm`: US Dollar index return

- These variables let the analysis compare transmission across rates, equities, volatility, and exchange rates.

---

# Independent Variables

Core regressors in the Table 4 specification:

- `mps`: monetary policy surprise
- `mpu`: monetary policy uncertainty
- `mpu_lag`: lagged uncertainty level

Main interaction term:

- `mps * mpu_lag`

- `mps` captures first-moment policy surprises.
- `mpu` captures changes in uncertainty around FOMC announcements.
- The interaction term tests whether the market response to policy surprises depends on the uncertainty environment.

---

# Pipeline Design

`data_management` -> `analysis` -> `final`

- Load + validate schemas
- Clean and prepare datasets
- Estimate baseline and multi-asset Table 4 models
- Produce:
  - `documents/tables/*.md`
  - `bld/models/*.pkl` and markdown summaries
  - `bld/figures/*.png`

---

# Baseline Specification

$$
\text{sp500\_return}_t = \alpha + \beta\,\text{mpu}_t + \varepsilon_t
$$

- OLS estimation
- Output table: `documents/tables/baseline_regression.md`
- Output summary: `bld/tables/regression_summary.md`
- Useful benchmark, but it may not fully capture cross-asset heterogeneity or state-dependent transmission.

---

# Baseline Results (Table)

<div class="text-left text-sm leading-tight border rounded-lg p-4 shadow-sm bg-white">

## Baseline Regression

| Term  | Coef | Std. Err. | t-stat | p-value |
|:------|-----:|----------:|-------:|--------:|
| const | 0.0013 | 0.0019 | 0.6960 | 0.4873 |
| mpu   | 0.0005 | 0.0021 | 0.2585 | 0.7963 |

</div>

<p class="text-xs mt-3 opacity-70">Source: <code>documents/tables/baseline_regression.md</code></p>

---

# What Table 2 Adds

- Table 2 asks a descriptive question before the regressions: when does MPU move the most?
- Panel A compares scheduled FOMC days with non-FOMC days in the baseline sample.
- Panel B compares press-conference and non-press-conference meetings in the later subsample.
- This matters because policy announcements and communication are the moments when uncertainty is most likely to be revised.

---

# Estimated Table 2 From Python Pipeline

<div class="text-left text-[11px] leading-tight border rounded-lg p-4 shadow-sm bg-white overflow-hidden">

<table class="w-full border-collapse text-[10px]">
  <thead>
    <tr>
      <th class="border px-2 py-1"></th>
      <th class="border px-2 py-1" colspan="2">Panel A : Jan. 1994 to Sept. 2020</th>
      <th class="border px-2 py-1" colspan="3">Panel B : Jan. 2012 to Dec. 2018</th>
    </tr>
    <tr>
      <th class="border px-2 py-1">Statistic</th>
      <th class="border px-2 py-1">mpu_fomc</th>
      <th class="border px-2 py-1">mpu_nonfomc</th>
      <th class="border px-2 py-1">mpuall</th>
      <th class="border px-2 py-1">mpupc</th>
      <th class="border px-2 py-1">mpunopc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="border px-2 py-1">Obs</td>
      <td class="border px-2 py-1">197</td>
      <td class="border px-2 py-1">6033</td>
      <td class="border px-2 py-1">56</td>
      <td class="border px-2 py-1">29</td>
      <td class="border px-2 py-1">27</td>
    </tr>
    <tr>
      <td class="border px-2 py-1">Mean</td>
      <td class="border px-2 py-1">-0.0160</td>
      <td class="border px-2 py-1">0.0003</td>
      <td class="border px-2 py-1">-0.0078</td>
      <td class="border px-2 py-1">-0.0130</td>
      <td class="border px-2 py-1">-0.0022</td>
    </tr>
    <tr>
      <td class="border px-2 py-1">tstat_mean</td>
      <td class="border px-2 py-1">-8.9124</td>
      <td class="border px-2 py-1">1.3735</td>
      <td class="border px-2 py-1">-4.5628</td>
      <td class="border px-2 py-1">-5.0317</td>
      <td class="border px-2 py-1">-1.3295</td>
    </tr>
    <tr>
      <td class="border px-2 py-1">Std. Dev.</td>
      <td class="border px-2 py-1">0.0252</td>
      <td class="border px-2 py-1">0.0195</td>
      <td class="border px-2 py-1">0.0128</td>
      <td class="border px-2 py-1">0.0140</td>
      <td class="border px-2 py-1">0.0088</td>
    </tr>
    <tr>
      <td class="border px-2 py-1">Skewness</td>
      <td class="border px-2 py-1">-1.6571</td>
      <td class="border px-2 py-1">1.3057</td>
      <td class="border px-2 py-1">-0.5707</td>
      <td class="border px-2 py-1">-0.3473</td>
      <td class="border px-2 py-1">0.7202</td>
    </tr>
    <tr>
      <td class="border px-2 py-1">Cumulative change</td>
      <td class="border px-2 py-1">-3.1584</td>
      <td class="border px-2 py-1">2.0779</td>
      <td class="border px-2 py-1">-0.4387</td>
      <td class="border px-2 py-1">-0.3783</td>
      <td class="border px-2 py-1">-0.0605</td>
    </tr>
  </tbody>
</table>

</div>

<p class="text-sm mt-3 leading-relaxed">
This is the estimated Table 2 produced by the Python pipeline. The main pattern is that
MPU moves much more sharply on scheduled FOMC days than on ordinary days, and the later
subsample suggests stronger adjustments on press-conference meetings.
</p>

<p class="text-xs mt-3 opacity-70">Source: <code>documents/tables/table2_summary.md</code></p>

---

# Comparing Estimated Table 2 And Paper Table

<div class="text-left text-sm leading-relaxed border rounded-lg p-4 shadow-sm bg-white">

<div class="flex justify-center mb-4">
  <img src="./Table 2.png" alt="Paper-style Table 2" class="max-h-[380px] rounded-lg shadow-lg border bg-white" />
</div>

- The estimated markdown table and the paper-style Table 2 tell the same story.
- Panel A highlights that uncertainty changes are concentrated on scheduled FOMC dates rather than on ordinary days.
- Panel B suggests that press conferences are an important part of that adjustment in the later sample.
- Any visible differences are presentation differences, not a change in the substantive interpretation.

</div>

<p class="text-xs mt-3 opacity-70">Sources: <code>documents/tables/table2_summary.md</code> and <code>documents/Table 2.png</code></p>

---

# What Table 4 Adds

$$
\Delta y_t =
\beta_0 + \beta_1 \text{mps}_t + \beta_2 \text{mpu}_t
+ \beta_3 (\text{mps}_t \times \text{mpu\_lag}_t) + \varepsilon_t
$$

- The baseline result gives an average relation, and Table 2 tells us when MPU tends to move more.
- Table 4 adds the cross-asset question: how do policy surprises transmit across yields, equities, volatility, and the dollar?
- It also adds state dependence by testing whether the effect of a policy surprise changes with lagged uncertainty.
- This is the step from descriptive timing evidence to a structural interpretation of transmission.

---

# Multi-Asset Table 4 From Pipeline

<div class="text-left text-[6px] leading-[1.05] border rounded-lg p-2 shadow-sm bg-white overflow-hidden">

<div class="text-[9px] font-semibold mb-1">Research paper-style replication</div>


<table class="w-full border-collapse text-[8px]">
  <thead>
    <tr>
      <th class="border px-1 py-1"></th>
      <th class="border px-1 py-1" colspan="3">Five-year nominal yield</th>
      <th class="border px-1 py-1" colspan="3">Ten-year nominal yield</th>
      <th class="border px-1 py-1" colspan="3">Ten-year TIPS yield</th>
    </tr>
    <tr>
      <th class="border px-1 py-1">Variable</th>
      <th class="border px-1 py-1">1</th>
      <th class="border px-1 py-1">2</th>
      <th class="border px-1 py-1">3</th>
      <th class="border px-1 py-1">1</th>
      <th class="border px-1 py-1">2</th>
      <th class="border px-1 py-1">3</th>
      <th class="border px-1 py-1">1</th>
      <th class="border px-1 py-1">2</th>
      <th class="border px-1 py-1">3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="border px-1 py-1">MPS</td>
      <td class="border px-1 py-1">0.65 [8.60]</td>
      <td class="border px-1 py-1">0.53 [6.28]</td>
      <td class="border px-1 py-1">1.26 [6.43]</td>
      <td class="border px-1 py-1">0.46 [7.38]</td>
      <td class="border px-1 py-1">0.32 [4.75]</td>
      <td class="border px-1 py-1">0.74 [4.36]</td>
      <td class="border px-1 py-1">0.44 [6.02]</td>
      <td class="border px-1 py-1">0.33 [4.30]</td>
      <td class="border px-1 py-1">1.25 [3.51]</td>
    </tr>
    <tr>
      <td class="border px-1 py-1">MPU</td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1">0.60 [2.74]</td>
      <td class="border px-1 py-1">0.81 [3.44]</td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1">0.68 [2.80]</td>
      <td class="border px-1 py-1">0.86 [3.29]</td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1">0.72 [3.10]</td>
      <td class="border px-1 py-1">0.88 [3.57]</td>
    </tr>
    <tr>
      <td class="border px-1 py-1">MPS * SRU_{-1}</td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1">-0.66 [-3.50]</td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1">-0.38 [-2.30]</td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1">-0.97 [-2.64]</td>
    </tr>
    <tr>
      <td class="border px-1 py-1">R^2</td>
      <td class="border px-1 py-1">0.46</td>
      <td class="border px-1 py-1">0.51</td>
      <td class="border px-1 py-1">0.57</td>
      <td class="border px-1 py-1">0.27</td>
      <td class="border px-1 py-1">0.34</td>
      <td class="border px-1 py-1">0.38</td>
      <td class="border px-1 py-1">0.20</td>
      <td class="border px-1 py-1">0.26</td>
      <td class="border px-1 py-1">0.36</td>
    </tr>
  </tbody>
</table>

<table class="w-full border-collapse text-[8px]">
  <thead>
    <tr>
      <th class="border px-1 py-1"></th>
      <th class="border px-1 py-1" colspan="3">S&amp;P 500</th>
      <th class="border px-1 py-1" colspan="3">VIX</th>
      <th class="border px-1 py-1" colspan="3">Dollar index</th>
    </tr>
    <tr>
      <th class="border px-1 py-1">Variable</th>
      <th class="border px-1 py-1">1</th>
      <th class="border px-1 py-1">2</th>
      <th class="border px-1 py-1">3</th>
      <th class="border px-1 py-1">1</th>
      <th class="border px-1 py-1">2</th>
      <th class="border px-1 py-1">3</th>
      <th class="border px-1 py-1">1</th>
      <th class="border px-1 py-1">2</th>
      <th class="border px-1 py-1">3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="border px-1 py-1">MPS</td>
      <td class="border px-1 py-1">-3.31 [-3.30]</td>
      <td class="border px-1 py-1">-1.60 [-1.25]</td>
      <td class="border px-1 py-1">-11.22 [-3.09]</td>
      <td class="border px-1 py-1">4.07 [2.82]</td>
      <td class="border px-1 py-1">-0.28 [-0.12]</td>
      <td class="border px-1 py-1">16.95 [2.95]</td>
      <td class="border px-1 py-1">2.51 [3.81]</td>
      <td class="border px-1 py-1">1.79 [2.54]</td>
      <td class="border px-1 py-1">12.30 [4.33]</td>
    </tr>
    <tr>
      <td class="border px-1 py-1">MPU</td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1">-8.66 [-1.74]</td>
      <td class="border px-1 py-1">-10.88 [-2.13]</td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1">22.06 [1.72]</td>
      <td class="border px-1 py-1">26.60 [1.92]</td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1">3.66 [1.92]</td>
      <td class="border px-1 py-1">6.01 [3.96]</td>
    </tr>
    <tr>
      <td class="border px-1 py-1">MPS * SRU_{-1}</td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1">8.73 [2.78]</td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1">-15.63 [-2.72]</td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1"></td>
      <td class="border px-1 py-1">-9.53 [-4.36]</td>
    </tr>
    <tr>
      <td class="border px-1 py-1">R^2</td>
      <td class="border px-1 py-1">0.05</td>
      <td class="border px-1 py-1">0.09</td>
      <td class="border px-1 py-1">0.13</td>
      <td class="border px-1 py-1">0.04</td>
      <td class="border px-1 py-1">0.14</td>
      <td class="border px-1 py-1">0.21</td>
      <td class="border px-1 py-1">0.11</td>
      <td class="border px-1 py-1">0.14</td>
      <td class="border px-1 py-1">0.32</td>
    </tr>
  </tbody>
</table>

</div>

<p class="text-sm mt-3 leading-relaxed">
This slide shows the generated Table 4 replication produced directly by the project
pipeline from <code>task_table4_multiasset.py</code> and the final table writer.
</p>

<p class="text-xs mt-3 opacity-70">Source: <code>documents/tables/table4_multiasset_regression.md</code></p>

---

# Multi-Asset Table 4 Screenshot

<div class="flex justify-center">
  <img src="./Table 4.png" alt="Paper-style multi-asset Table 4" class="max-h-[540px] rounded-lg shadow-lg border bg-white" />
</div>

<p class="text-sm mt-4 leading-relaxed">
This screenshot is the paper-style presentation version of the same result. It is useful
for visual comparison with the generated table in the previous slide.
</p>

<p class="text-xs mt-3 opacity-70">Source: <code>documents/tables/table4_multiasset_regression.md</code> and <code>documents/Table 4.png</code></p>

---

# Comparing Generated Table And Table from the Research Paper

- The coefficient values and signs match across the generated markdown table and the screenshoted paper table.
- The main pattern is the same in both: yields react positively to MPS, equity responses are negative, and the interaction term shows state dependence under higher uncertainty.
- Any visible differences are presentation differences rather than estimation differences.
- Those differences come from formatting choices such as line breaks, labels, panel layout, and rounding to two decimals.

---

# Interpretation

- Table 2 shows that MPU is not moving uniformly through time; it is concentrated around policy-event dates, especially in meeting windows with richer communication.
- That descriptive result motivates looking beyond the baseline average relationship and studying transmission on event days.
- Table 4 then shows that policy shocks do not transmit uniformly across financial markets.
- In the yield regressions, positive MPS coefficients indicate higher yields after contractionary surprises, while the interaction term shows that the strength of this response changes with uncertainty.
- Equity, volatility, and dollar responses follow different patterns, so uncertainty changes both the size and direction of transmission across asset classes.

---

# Reproducibility

From project root:

```bash
pixi install
pixi run pytask
pixi run pytest
```

Key artifacts:

- `bld/data/*.pkl`
- `bld/models/*.pkl`
- `bld/models/table2_summary.pkl`
- `bld/tables/regression_summary.md`
- `documents/tables/table2_summary.md`
- `bld/figures/*.png`
- `documents/Table 2.png`
- `documents/tables/*.md`

---

# Conclusion

- Reproducible pipeline is fully integrated across data, analysis, and outputs.
- Baseline relation is estimated and documented, but it does not explain the variation on its own.
- Table 2 adds the key descriptive result that uncertainty shifts are concentrated around FOMC and communication events.
- The multi-asset Table 4 replication builds on that result and shows uncertainty-dependent transmission across markets.
- Project is ready for extension (additional controls, robustness, alternative event windows).

---

# Thank You
