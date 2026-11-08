"""AI Incident Database tables for Story 3, built from the notebook's own output.

The aiid_incidents notebook writes two tables and the story keeps them as written in ``data/``:

- ``incidents.csv``: one row per incident.
- ``incident_developers.csv``: one row per incident and developer name, including generic categories such as
  "Large Language Model Developers" that are not companies.

This module does the work that was done by hand for the A3P1 app: it keeps the named companies, removes repeated
rows for the same incident and company, keeps the columns the page uses and joins the two tables. The result is the
same pair of tables that A3P1 reads from ``aiid_incidents.csv`` and ``aiid_incident_developers.csv``.
The page then joins the companies to the Epoch table (``src/context.py``, function ``epoch_models_by_company``).
"""
from __future__ import annotations

import pandas as pd

READ = {"keep_default_na": False, "na_values": [""]}
INCIDENT_COLUMNS = ["incident_id", "date", "year", "title", "is_generative_related", "named_developers"]
DEVELOPER_COLUMNS = ["incident_id", "year", "developer_clean", "is_china_based", "genai_flag"]


def load_incidents(incidents_path, developers_path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (incidents, named): one row per incident, and one row per incident and named company."""
    incidents = pd.read_csv(incidents_path, **READ)[INCIDENT_COLUMNS]
    developers = pd.read_csv(developers_path, **READ)
    named = (developers.loc[developers["entity_kind"].eq("named_company")]
             .drop_duplicates(["incident_id", "developer_clean"])[DEVELOPER_COLUMNS].reset_index(drop=True))
    for frame in (incidents, named):
        for col in ("is_generative_related", "is_china_based", "genai_flag"):
            if col in frame:
                frame[col] = frame[col].astype(str).str.lower().eq("true")
    named = named.merge(incidents[["incident_id", "date", "title", "is_generative_related"]], on="incident_id",
                        how="left")
    return incidents, named
