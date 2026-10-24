"""Acquire, transform and validate the dashboard's dataset.

One module holds the whole data pipeline so its lineage is inspectable:
`acquire()` fetches the raw source, `transform()` shapes it, `validate()`
checks the result, and `main()` runs all three. Presentation lives in
`views.py`.
"""

from __future__ import annotations

import json
import argparse
import os
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample.csv"
RAW = ROOT / "data" / "raw.json"
PROCESSED = ROOT / "data" / "processed.csv"

URL = (
    "https://api.worldbank.org/v2/country/AUS;NZL/indicator/SP.POP.TOTL"
    "?format=json&date=2019:2023&per_page=100"
)
REQUIRED = {"date", "country_code", "country", "population", "unit"}


def acquire() -> None:
    """Download the raw source to data/raw.json."""
    try:
        with urlopen(URL, timeout=30) as response:
            payload = json.load(response)
    except (URLError, TimeoutError, json.JSONDecodeError) as error:
        sys.exit(
            f"Could not fetch {URL}: {error}. "
            "Check your connection, or rerun with DASHBOARD_SAMPLE_MODE=1 "
            "to use the bundled sample."
        )
    RAW.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {RAW}")


def transform(payload_path: Path) -> pd.DataFrame:
    """Turn the raw API response into the tidy dashboard dataset."""
    records = json.loads(payload_path.read_text(encoding="utf-8"))[1]
    return pd.DataFrame(
        {
            "date": [f"{record['date']}-12-31" for record in records],
            "country_code": [record["countryiso3code"] for record in records],
            "country": [record["country"]["value"] for record in records],
            "population": [record["value"] for record in records],
            "unit": "people",
        }
    )


def validate(frame: pd.DataFrame) -> None:
    """Stop the pipeline if the dataset breaks a documented expectation."""
    missing_columns = REQUIRED.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {sorted(missing_columns)}")
    if len(frame) < 10:
        raise ValueError("The sample must contain at least ten observations")
    if frame.duplicated(["date", "country_code"]).any():
        raise ValueError("Duplicate date and country keys found")
    if frame[list(REQUIRED)].isna().any().any():
        raise ValueError("Unexpected missing values found")
    parsed_dates = pd.to_datetime(frame["date"], errors="raise")
    if parsed_dates.dt.year.min() < 2019 or parsed_dates.dt.year.max() > 2023:
        raise ValueError("Date outside the documented period")
    if not set(frame["country_code"]).issubset({"AUS", "NZL"}):
        raise ValueError("Unexpected country code")
    countries = {"AUS": "Australia", "NZL": "New Zealand"}
    if not (frame["country_code"].map(countries) == frame["country"]).all():
        raise ValueError("Country name does not match its code")
    population = pd.to_numeric(frame["population"], errors="raise")
    if not ((population % 1 == 0) & population.between(0, 100000000)).all():
        raise ValueError("Population must be an integer between 0 and 100000000")
    if set(frame["unit"]) != {"people"}:
        raise ValueError("Unexpected unit")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--acquire", action="store_true", help="Refresh data/raw.json and stop")
    parser.add_argument("--validate", action="store_true", help="Validate data/processed.csv and stop")
    args = parser.parse_args()
    sample_mode = os.getenv("DASHBOARD_SAMPLE_MODE", "0") == "1"
    if args.acquire:
        if sample_mode:
            parser.error("Unset DASHBOARD_SAMPLE_MODE before acquiring live data")
        acquire()
        return
    if args.validate:
        validate(pd.read_csv(PROCESSED))
        print("Processed data valid")
        return
    if sample_mode:
        frame = pd.read_csv(SAMPLE)
    else:
        if not RAW.exists():
            acquire()
        frame = transform(RAW)
    frame["date"] = pd.to_datetime(frame["date"], errors="raise").dt.strftime("%Y-%m-%d")
    frame = frame.sort_values(["country", "date"]).reset_index(drop=True)
    validate(frame)
    PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(PROCESSED, index=False)
    print(f"Validated and wrote {len(frame)} rows to {PROCESSED}")


if __name__ == "__main__":
    main()
