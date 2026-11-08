"""Data and calculations for Views 3 to 5 (licence classes, capability gap, reported incidents).

The three views reuse the processed model table (``data/models.csv``) and add two small source extracts that were
built by the project notebooks and copied here unchanged:

- ``data/source/licence_check.csv``: the five open-weight licences the group read by hand (notebook 01).
- ``data/source/aiid_incidents.csv`` and ``aiid_incident_developers.csv``: AI Incident Database export of
  12 October 2026 (notebook 10), one row per incident and one row per incident and named company.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "source"
READ = {"keep_default_na": False, "na_values": [""]}

US = "United States of America"
DATA_END = pd.Timestamp("2026-10-07")  # latest release date in the Epoch file

# --------------------------------------------------------------------------- #
# View 3: what the licence allows
# --------------------------------------------------------------------------- #
# Epoch's accessibility label, read as what it means for a bank that wants to run the model on its own servers.
# Order = top to bottom on the chart, from "can be self-hosted" to "cannot".
LICENCE_CLASSES = {
    "Open weights, unrestricted": ("Can be self-hosted, commercial use allowed", ["Open weights (unrestricted)"]),
    "Open weights, restricted use": ("Can be self-hosted after a legal review of the terms",
                                     ["Open weights (restricted use)"]),
    "Open weights, non-commercial": ("Cannot be used by a bank for its business", ["Open weights (non-commercial)"]),
    "API or hosted only": ("Cannot be self-hosted, used as a service", ["API access", "Hosted access (no API)"]),
    "Unknown or not released": ("Access not known", ["Unknown", "Limited access", "Unreleased"]),
}
OUR_READING = {
    "mit": "MIT licence: commercial use and self-hosting allowed",
    "apache_2_0": "Apache 2.0 licence: commercial use and self-hosting allowed",
    "custom_threshold": "Own licence: commercial use allowed, a separate agreement is needed above a revenue threshold",
}
COUNTRY_GROUPS = ["United States", "China", "Other countries", "Not stated"]


def country_group(country: pd.Series) -> pd.Series:
    out = country.map({US: "United States", "China": "China"})
    out = out.where(out.notna(), country.where(country.isna(), "Other countries"))
    return out.fillna("Not stated")


def licence_class(accessibility: pd.Series) -> pd.Series:
    lookup = {label: name for name, (_, labels) in LICENCE_CLASSES.items() for label in labels}
    return accessibility.map(lookup).fillna("Unknown or not released")


def load_licence_check() -> pd.DataFrame:
    return pd.read_csv(SOURCE / "licence_check.csv", **READ)


def with_licence(models: pd.DataFrame, check: pd.DataFrame) -> pd.DataFrame:
    """Model table plus licence class (from Epoch's label), country group and the group's own licence reading."""
    out = models.assign(licence_class=licence_class(models["epoch_accessibility"]),
                        country_group=country_group(models["country"]))
    out = out.merge(check[["model", "licence_class_ours", "licence_basis"]], on="model", how="left")
    out["our_reading"] = out["licence_class_ours"].map(OUR_READING)
    return out


def best_per_class(frame: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name in LICENCE_CLASSES:
        part = frame.loc[frame["licence_class"] == name]
        if part.empty:
            continue
        best = part.sort_values(["eci", "release_date"], ascending=[False, False]).iloc[0]
        rows.append(best.to_dict() | {"n_in_class": len(part)})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# View 4: capability gap to the restricted US models
# --------------------------------------------------------------------------- #
ACCESS_OPTIONS = {
    "Open weights (self-hosted)": "open",
    "Non-US API or hosted services": "api",
}


def access_group(models: pd.DataFrame) -> pd.Series:
    """Restricted = a US developer and no downloadable weights (the leading closed US models of the question).
    Accessible = open weights from any country, or a service from a developer outside the US.
    Excluded = no open weights and no stated country (17 older models), so neither side can be claimed."""
    us = models["country"].eq(US)
    open_w = models["route"].eq("Open weights")
    group = pd.Series("excluded", index=models.index)
    group[us & ~open_w] = "restricted"
    group[open_w] = "open"
    group[~open_w & models["country"].notna() & ~us] = "api"
    return group


def frontier(frame: pd.DataFrame, dates: pd.DatetimeIndex) -> pd.DataFrame:
    """Best score released on or before each date, with the model that holds it (NaN before the first model)."""
    ordered = frame.sort_values(["release_date", "eci"])
    best = ordered.assign(best=ordered["eci"].cummax())
    holder = best.loc[best["eci"] == best["best"]].drop_duplicates("best", keep="first")
    holder = holder[["release_date", "best", "model"]].groupby("release_date").last()
    out = holder.reindex(dates.union(holder.index)).ffill().reindex(dates)
    return out


def gap_summary(models: pd.DataFrame, accessible: list[str], at: pd.Timestamp = DATA_END) -> dict:
    """Gap in points and lag in months between the restricted and the accessible frontier at one date."""
    group = access_group(models)
    restricted = models.loc[group == "restricted"]
    access = models.loc[group.isin(accessible)]
    r_now = restricted.loc[restricted["release_date"] <= at]
    a_now = access.loc[access["release_date"] <= at]
    if r_now.empty or a_now.empty:
        return {}
    r_best = r_now.sort_values("eci").iloc[-1]
    a_best = a_now.sort_values("eci").iloc[-1]
    reached = r_now.sort_values("release_date")
    reached = reached.loc[reached["eci"].cummax() >= a_best["eci"]]
    lag = None
    if not reached.empty:
        first = reached.iloc[0]["release_date"]
        lag = (at.year - first.year) * 12 + (at.month - first.month) + (at.day - first.day) / 30.4
    return {"restricted": r_best, "accessible": a_best, "gap": r_best["eci"] - a_best["eci"],
            "reached_on": reached.iloc[0]["release_date"] if not reached.empty else None,
            "reached_by": reached.iloc[0]["model"] if not reached.empty else None,
            "lag_months": lag,
            "intervals_overlap": a_best["eci_ci_high"] >= r_best["eci_ci_low"]}


# --------------------------------------------------------------------------- #
# View 5: reported incidents
# --------------------------------------------------------------------------- #
# AIID company name -> Epoch developer names, to count each company's models in the Epoch list.
EPOCH_NAMES = {
    "Google": ["Google", "Google DeepMind"], "Meta": ["Meta AI"], "Microsoft": ["Microsoft", "Microsoft Research"],
    "Mistral": ["Mistral AI"], "Z.ai (Zhipu)": ["Z.ai (Zhipu AI)"],
}
INCIDENT_KINDS = ["All AI incidents", "Generative AI only"]
AIID_EXPORT = "12 Oct 2026"
AIID_LATEST = "3 Oct 2026"


def load_incidents() -> tuple[pd.DataFrame, pd.DataFrame]:
    incidents = pd.read_csv(SOURCE / "aiid_incidents.csv", **READ)
    named = pd.read_csv(SOURCE / "aiid_incident_developers.csv", **READ)
    for frame in (incidents, named):
        for col in ("is_generative_related", "is_china_based", "genai_flag"):
            if col in frame:
                frame[col] = frame[col].astype(str).str.lower().eq("true")
    named = named.merge(incidents[["incident_id", "date", "title", "is_generative_related"]], on="incident_id",
                        how="left")
    return incidents, named


def per_year(incidents: pd.DataFrame, kind: str, first_year: int = 2012) -> pd.DataFrame:
    frame = incidents.loc[incidents["year"] >= first_year]
    out = frame.groupby("year").agg(generative=("is_generative_related", "sum"),
                                    total=("incident_id", "count"))
    out["other"] = out["total"] - out["generative"]
    if kind == INCIDENT_KINDS[1]:
        out["other"] = 0
        out["total"] = out["generative"]
    return out.reindex(range(first_year, int(incidents["year"].max()) + 1), fill_value=0).reset_index()


def epoch_models_by_company(models: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for company in sorted(set(EPOCH_NAMES) | set(models["organization"].dropna())):
        names = EPOCH_NAMES.get(company, [company])
        part = models.loc[models["organization"].isin(names)]
        rows.append({"developer_clean": company, "epoch_models": len(part),
                     "best_eci": part["eci"].max() if len(part) else float("nan")})
    return pd.DataFrame(rows)


def per_developer(named: pd.DataFrame, models: pd.DataFrame, kind: str, from_year: int,
                  developers: list[str]) -> pd.DataFrame:
    rows = filter_named(named, kind, from_year, developers)
    if rows.empty:
        return pd.DataFrame(columns=["developer_clean", "incidents", "generative", "other", "is_china_based",
                                     "epoch_models", "best_eci"])
    out = rows.groupby("developer_clean").agg(incidents=("incident_id", "nunique"),
                                              generative=("is_generative_related", "sum"),
                                              is_china_based=("is_china_based", "max")).reset_index()
    out["other"] = out["incidents"] - out["generative"]
    out = out.merge(epoch_models_by_company(models), on="developer_clean", how="left")
    out["epoch_models"] = out["epoch_models"].fillna(0).astype(int)
    return out.sort_values(["incidents", "developer_clean"], ascending=[False, True]).reset_index(drop=True)


def filter_named(named: pd.DataFrame, kind: str, from_year: int, developers: list[str]) -> pd.DataFrame:
    rows = named.loc[(named["year"] >= from_year) & named["developer_clean"].isin(developers)]
    if kind == INCIDENT_KINDS[1]:
        rows = rows.loc[rows["is_generative_related"]]
    return rows
