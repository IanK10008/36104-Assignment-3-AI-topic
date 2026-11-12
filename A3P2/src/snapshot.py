"""Dates and headline figures of the data in use, so that page text follows a refreshed download.

The three notebooks of Story 1a write notebooks/<source>/raw/retrieval_log.json (when the file was downloaded)
and notebooks/<source>/processed/data_currency.csv (which dates the data covers). This module reads them. When a
record is missing, the text says "date not recorded" and the latest model date is read from the data itself.
The figures that page text quotes (the correlation of capability with preference, the typical width of the ECI
interval) are computed here from the data at the default settings.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd

NOT_RECORDED = "date not recorded"
SOURCES = {"epoch": "eci_scores", "litellm": "litellm_prices", "lmarena": "lmarena_leaderboard"}

current: dict = {}


def day_text(value) -> str:
    """'2026-11-12T19:04:51Z' or a Timestamp -> '12 Nov 2026'."""
    try:
        stamp = pd.Timestamp(str(value)[:10])
    except (ValueError, TypeError):
        return NOT_RECORDED
    if pd.isna(stamp):
        return NOT_RECORDED
    return f"{stamp.day} {stamp:%b %Y}"


def _retrieved(folder: Path, source: str) -> str:
    path = folder / "notebooks" / SOURCES[source] / "raw" / "retrieval_log.json"
    try:
        log = json.loads(path.read_text(encoding="utf-8"))
        stamps = [entry["retrieved_utc"] for entry in log.values() if entry.get("how") == "downloaded"]
        stamps = stamps or [entry["retrieved_utc"] for entry in log.values()]
        return day_text(max(stamps))
    except (OSError, ValueError, KeyError):
        return NOT_RECORDED


def _covers(folder: Path, source: str) -> tuple[str, str]:
    path = folder / "notebooks" / SOURCES[source] / "processed" / "data_currency.csv"
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            row = next(csv.DictReader(handle))
        return day_text(row["data_covers_from"]), day_text(row["data_covers_to"])
    except (OSError, StopIteration, KeyError):
        return NOT_RECORDED, NOT_RECORDED


def _default_selection(models: pd.DataFrame):
    from src import analysis as an
    base = an.filter_models(models, an.WINDOWS[list(an.WINDOWS)[0]], None, list(an.developer_name(models).unique()))
    three = an.three_source(base, an.MATCH_RULES[list(an.MATCH_RULES)[0]])
    return base, three


def load(folder: Path, models: pd.DataFrame) -> dict:
    """Read the dates and compute the figures. The result is also stored in `current`."""
    first, last = _covers(folder, "epoch")
    if last == NOT_RECORDED:
        first, last = day_text(models["release_date"].min()), day_text(models["release_date"].max())
    published = _covers(folder, "lmarena")[1]
    base, three = _default_selection(models)
    width = (models["eci_ci_high"] - models["eci_ci_low"])[pd.to_datetime(models["release_date"]).dt.year == 2026]
    corr = three["eci"].corr(three["arena_rating"]) if len(three) > 2 else np.nan
    result = {
        "epoch_retrieved": _retrieved(folder, "epoch"), "epoch_first": first, "epoch_last": last,
        "litellm_retrieved": _retrieved(folder, "litellm"),
        "lmarena_retrieved": _retrieved(folder, "lmarena"), "lmarena_published": published,
        "corr": None if pd.isna(corr) else round(float(corr), 2),
        "ci_low": int(round(width.quantile(0.25))) if width.notna().any() else None,
        "ci_high": int(round(width.quantile(0.75))) if width.notna().any() else None,
    }
    current.clear()
    current.update(result)
    return result


def get(key: str) -> str:
    value = current.get(key)
    return NOT_RECORDED if value is None else str(value)


def corr_text() -> str:
    """'0.79' or 'a high value' when it could not be computed."""
    value = current.get("corr")
    return "a high value" if value is None else f"{value:.2f}"


def ci_text() -> str:
    low, high = current.get("ci_low"), current.get("ci_high")
    if low is None or high is None:
        return "several"
    return f"{low}" if low == high else f"{low} to {high}"
