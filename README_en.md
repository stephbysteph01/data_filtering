# CzRM analysis for Roma Capitale (English)

This project analyzes complaints/reports from Roma Capitale's CzRM using the Open Data datasets provided by the Municipality of Rome.

## Objective

- load CSV files containing open and closed reports;
- clean and normalize the data;
- aggregate by municipality, theme, origin, and month;
- compare the volume of open vs closed reports;
- produce meaningful charts and a final Excel report.

## Data source

The data are taken from the Municipality of Rome Open Data portal, dataset "CzRM di Roma Capitale - Dati delle segnalazioni anno 2026".

License: CC BY 4.0 (https://w3id.org/italia/controlled-vocabulary/licences/A21_CCBY40)

## Project structure

- `data/` (or `data/raw/` for compatibility): directory where to place the original CSV files
- `data/processed/`: outputs produced by the project (reports and charts)
- `src/czrm_analysis/`: Python package containing the analysis code
- `tests/`: automated tests

## Main requirements

- pandas
- numpy
- matplotlib
- openpyxl

Or use the provided `requirements.txt`.

## Quick start

1. create a virtual environment
2. install dependencies
3. place the CSV files into `data/` (or `data/raw/` if you prefer)
4. run:

```bash
python -m czrm_analysis
```

This command will load the CSV files, clean the data, generate charts, and save a report into `data/processed/`.

## Notes on the data

- Open and closed files do not share a single case ID. For this reason the project does not join rows by ID; it aggregates and compares counts at an aggregated level instead.

- Date parsing: the loader attempts to detect common date formats (e.g. DD/MM/YYYY) and parses accordingly. Records with non-parseable dates are excluded from month-based aggregations.

## What the code provides

- A robust CSV loader that handles common encodings (UTF-8, UTF-8-SIG, CP1252, Latin-1) and uses `;` as the default separator when appropriate.
- Preprocessing utilities that normalize text, fill missing category values, parse dates into monthly periods, and clean coordinates.
- Aggregation functions that count cases by theme, month, municipality, and origin.
- Comparison utilities that align aggregated counts of open vs closed reports per theme and month, producing a delta (open - closed).
- Plotting utilities that produce:
  - a monthly trend chart (open vs closed), and
  - separate top-categories charts for open and closed datasets (top N categories).
- An Excel exporter that writes multi-sheet reports (summary and comparison tables) using openpyxl.

## Recommendations

- Avoid committing raw CSV files or large generated outputs (charts, reports) into the repository. Use `.gitignore` to exclude `data/` or specific paths.
- If you need to include data in the repository, consider adding a small example subset instead of the full dataset.

## Next steps (suggested)

- Add more unit tests for parsing and cleaning functions.
- Build a Jupyter notebook for interactive exploration and visualization.
- Add a mapping layer to canonicalize theme labels between open and closed datasets.

If you need the README translated into another language or want me to commit this English README to the repository, tell me and I'll do it.