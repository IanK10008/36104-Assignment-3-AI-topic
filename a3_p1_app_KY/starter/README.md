# Student starter dashboard

This small World Development Indicators example demonstrates the required submission contract. It is intentionally modest and is not a model of the analytical scope expected in the final assignment.

## Run in sample mode

```bash
export DASHBOARD_SAMPLE_MODE=1
streamlit run app.py
```

## Rebuild the processed sample

```bash
export DASHBOARD_SAMPLE_MODE=1
python -m src.data
```

## Acquire a current API response

```bash
unset DASHBOARD_SAMPLE_MODE
python -m src.data --acquire
```

This refreshes `data/raw.json`. Review its metadata before replacing the assessed snapshot. Then run `python -m src.data` to transform and validate it. Without `--acquire`, an existing raw file is reused.

## Validate

```bash
python -m src.data --validate
```

Python 3.11 is required. Direct dependencies are pinned in `pyproject.toml`.

Install them with `pip install -r requirements.txt`. The matching requirements file is supplied for a straightforward installation without packaging the app as a Python library.

If you change dependencies, update both declarations consistently (or supply only one supported declaration). The requirements file must include the project's active dependencies and extras with agreeing exact pins; additional pinned packages are allowed. For assessment, install dashboard and checker requirements together using the command in the pack README, then resolve any dependency or environment flags before relying on the score.

The `population_trend` container matches the manifest view ID. Keep the heading, source, unit, date, controls and outputs inside that container. Its `dataset_id` identifies the record-level data exported by its CSV download; chart aggregation may differ from those records.
