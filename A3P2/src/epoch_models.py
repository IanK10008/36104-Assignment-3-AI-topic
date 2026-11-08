"""Epoch-only tables for stories 1b and 2.

Views 3 and 4 need only Epoch columns (name, date, developer, country, access label, capability score and its
interval) plus the group's own licence readings. This module builds them from the story's own copy of
``model_capability.csv``, the table written by the eci_scores notebook. The result has the same columns, the same
types and the same row order as the matching columns of ``models.csv`` in the A3P1 app, so the view code is
unchanged.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from src import data

EPOCH_COLUMNS = ["model", "release_date", "release_year", "organization", "country", "route",
                 "epoch_accessibility", "eci", "eci_ci_low", "eci_ci_high"]
LICENCE_COLUMNS = ["model", "epoch_accessibility", "licence_class_ours", "licence_basis"]
_TEXT = ["model", "release_date", "organization_primary", "country", "epoch_accessibility",
         "epoch_accessibility_group", "licence_class_ours", "licence_basis"]


def _read(path) -> pd.DataFrame:
    return pd.read_csv(path, dtype={column: str for column in _TEXT}, **data.READ_OPTIONS)


def load_epoch_models(path) -> pd.DataFrame:
    """One row per Epoch model, highest capability first (the order of the A3P1 table)."""
    table = _read(path)
    frame = pd.DataFrame({
        "model": table["model"],
        "release_date": table["release_date"],
        "organization": table["organization_primary"],
        "country": table["country"],
        "route": table["epoch_accessibility_group"].map(lambda g: data.ROUTES.get(g, data.ROUTES["Other"])),
        "epoch_accessibility": table["epoch_accessibility"],
        "eci": table["eci"].astype("float64"),
        "eci_ci_low": table["eci_ci_low"].astype("float64"),
        "eci_ci_high": table["eci_ci_high"].astype("float64"),
    })
    frame["release_year"] = pd.to_datetime(frame["release_date"], format="%Y-%m-%d", errors="raise").dt.year.astype("int64")
    frame["release_date"] = pd.to_datetime(frame["release_date"], format="%Y-%m-%d", errors="raise")
    frame = frame.sort_values("eci", ascending=False, kind="stable")
    return frame[EPOCH_COLUMNS].reset_index(drop=True)


def load_licence_check(path) -> pd.DataFrame:
    """The models whose licence page the group read (the rows with a licence basis written)."""
    table = _read(path)
    return table.loc[table["licence_basis"].notna(), LICENCE_COLUMNS].reset_index(drop=True)
