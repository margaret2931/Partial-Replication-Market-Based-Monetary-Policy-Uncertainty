git ## Release Notes

## Unreleased

- Add the full Table 2 replication workflow, including:
  - validated FOMC meeting-date loading,
  - summary-statistics estimation,
  - intermediate pickle output,
  - final markdown table generation.
- Add unit and integration tests for the Table 2 analysis and output tasks.
- Improve Table 2 type hints, test expectations, and markdown formatting.
- Expand paper and presentation content for the Table 2 replication.
- Add the paper-style Table 2 image and update documentation commands.
- Improve Table 4 docstrings and presentation styling.
- Restore a previously deleted file and refine project documentation.

## v10

- Add the raw input file needed to replicate Table 2.

## v9

- Introduce the multi-asset Table 4 implementation with date-clustered standard errors.
- Add pytask tasks to estimate, serialize, tabulate, and plot the multi-asset regressions.
- Replace missing markdown entries with blanks in the generated Table 4 output.
- Remove the earlier single-asset Table 4 workflow in favor of the multi-asset version.

## v8

- Track required raw inputs explicitly in the reproducible pipeline.

## v7

- Add unit tests for Table 4 regression validation and specification coverage.

## v6

- Generate the final Table 4 markdown table and wire it into the document tasks.
- Improve the document-compilation task.

## v5

- Clean up the Table 4 task implementation and make summary-output behavior explicit.

## v4

- Standardize the MPU loader so the replication uses a consistent `mpu` column.

## v3

- Implement clustered Table 4 regressions with multiple specifications.
- Add text-summary export for regression results.

## v2

- Improve Table 4 cleaning logic and formatting behavior.

## v1

- Implement the S&P 500 loader and establish the clean data layer.

## v0

- Begin the money-finance final project repository.
