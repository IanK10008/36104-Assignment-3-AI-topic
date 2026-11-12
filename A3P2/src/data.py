"""Build, validate and load the Model Choice Explorer dataset.

The dashboard needs one table with one row per AI model scored by Epoch AI's
Epoch Capabilities Index (ECI). Each row adds two other public sources:

* LiteLLM's model price file: what API providers charge for output tokens.
* The LMArena text leaderboard: how people rate the model's answers.

The three sources spell model names differently (for example "Claude Opus 4.5",
"azure_ai/claude-opus-4-5" and "claude-opus-4-5-20251101"), so rows are
matched by a normalised *name key*. `build_models()` explains each matching
rule in plain English.

Modes (run from the dashboard folder):

* ``python -m src.data`` (offline, the default; also when
  ``DASHBOARD_SAMPLE_MODE=1``): read the slim extracts in ``data/source/``,
  rebuild the table, validate it, confirm that it equals
  ``data/models_sample.csv`` and write only ``data/models.csv``.
* ``python -m src.data --extract RAW_DIR`` (live refresh): re-cut the slim
  extracts in ``data/source/`` from the three full source files in RAW_DIR.
* ``python -m src.data --write-sample``: like offline mode, but also
  (re)writes ``data/models_sample.csv``. Use it only after a deliberate refresh.
* ``python -m src.data --validate``: validate ``data/models.csv`` and stop.

The pipeline makes no network connections and runs in about a second.
"""

from __future__ import annotations

import argparse
import io
import os
import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SOURCE = DATA / "source"
DATASETS = {"models": (DATA / "models_sample.csv", DATA / "models.csv")}
SAMPLE, PROCESSED = DATASETS["models"]

# Full source files as downloaded (the live inputs for --extract).
RAW_FILES = {
    "epoch": "model_capability.csv",
    "litellm": "model_price.csv",
    "lmarena": "lmarena_ratings.csv",
}
# Slim extracts kept with the dashboard (the offline inputs).
SOURCE_FILES = {
    "epoch": SOURCE / "epoch_eci_scores.csv",
    "litellm": SOURCE / "litellm_chat_prices.csv",
    "lmarena": SOURCE / "lmarena_overall.csv",
}
# Columns kept in each extract: only what build_models() uses.
SOURCE_COLUMNS = {
    "epoch": [
        "model", "release_date", "organization_primary", "country",
        "epoch_accessibility", "epoch_accessibility_group",
        "eci", "eci_ci_low", "eci_ci_high",
    ],
    "litellm": ["model_key", "output_usd_per_million"],
    "lmarena": ["model_name", "rating", "rating_lower", "rating_upper", "vote_count"],
}
SOURCE_DTYPES = {
    "epoch": {
        "model": str, "release_date": str, "organization_primary": str,
        "country": str, "epoch_accessibility": str,
        "epoch_accessibility_group": str,
        "eci": "float64", "eci_ci_low": "float64", "eci_ci_high": "float64",
    },
    "litellm": {"model_key": str, "output_usd_per_million": "float64"},
    "lmarena": {
        "model_name": str, "rating": "float64", "rating_lower": "float64",
        "rating_upper": "float64", "vote_count": "Int64",
    },
}

COLUMNS = [
    "model", "release_date", "release_year", "organization", "country",
    "route", "epoch_accessibility", "eci", "eci_ci_low", "eci_ci_high",
    "litellm_match", "litellm_match_type", "price_providers",
    "output_price_usd_per_million", "output_price_min", "output_price_max",
    "lmarena_match", "lmarena_match_type", "arena_rating",
    "arena_rating_lower", "arena_rating_upper", "arena_votes",
    "version_unclear", "match_status",
]
STRING_COLUMNS = [
    "model", "release_date", "organization", "country", "route",
    "epoch_accessibility", "litellm_match", "litellm_match_type",
    "lmarena_match", "lmarena_match_type", "match_status",
]
FLOAT_COLUMNS = [
    "eci", "eci_ci_low", "eci_ci_high", "output_price_usd_per_million",
    "output_price_min", "output_price_max", "arena_rating",
    "arena_rating_lower", "arena_rating_upper",
]
PRICE_COLUMNS = ["output_price_usd_per_million", "output_price_min", "output_price_max"]
ARENA_COLUMNS = ["arena_rating", "arena_rating_lower", "arena_rating_upper"]

# Epoch's accessibility group, relabelled for the dashboard's "route" filter.
ROUTES = {
    "Open weights": "Open weights",
    "Closed weights": "Closed weights",
    "Other": "Other or unknown",
}
LITELLM_MATCH_TYPES = ("same_name", "tag_stripped", "none")
LMARENA_MATCH_TYPES = ("same_name", "tag_stripped", "max_tag_review", "none")

ALL_SAME = "All three: same name"
ALL_TAG = "All three: same name plus a tag"
ALL_UNCLEAR = "All three: unclear version"
MAX_REVIEW = "Needs a manual check (-max tag)"
LITELLM_ONLY = "Epoch and LiteLLM only"
LMARENA_ONLY = "Epoch and LMArena only"
EPOCH_ONLY = "Epoch only"
MATCH_STATUSES = (
    ALL_SAME, ALL_TAG, ALL_UNCLEAR, MAX_REVIEW, LITELLM_ONLY, LMARENA_ONLY, EPOCH_ONLY,
)

# Documented coverage and plausibility bounds checked by validate().
# The end date is a guard against parsing errors, not the latest model of a snapshot,
# so that a refreshed Epoch download passes. The latest release date is read from the data.
RELEASE_DATE_RANGE = ("2023-02-24", "2030-12-31")
# ECI is a positive score: the frontier is about 170, while 24 older models in
# this snapshot score below 100 (lowest 56), so 0..200 (not 100..200) is the
# bound that catches unit or parsing errors without rejecting real rows.
ECI_RANGE = (0.0, 200.0)
ARENA_RANGE = (800.0, 1700.0)
# Headline counts of the 17 Oct 2026 snapshot: models released in 2025-2026 that
# match in all three sources (with or without a stripped tag) / by same name.
# They are kept as a reference only. A refreshed download changes them, so validate()
# no longer requires them and only checks that the counts are plausible.
RECENT_YEARS = (2025, 2026)
SNAPSHOT_RECENT_ALL_THREE = 84
SNAPSHOT_RECENT_SAME_NAME = 44

# Only empty fields are missing; text such as "NA" stays text.
RAW_READ_OPTIONS = {"keep_default_na": False, "na_values": [""]}
# Files this module writes are re-read exactly ("round_trip" float parsing).
READ_OPTIONS = {**RAW_READ_OPTIONS, "float_precision": "round_trip"}


# ---------------------------------------------------------------------------
# Name keys
# ---------------------------------------------------------------------------

# Text in brackets is never part of the product name. Epoch uses it for
# snapshots ("Gemini 2.5 Pro (Mar 2025)") and hosting notes ("(hosted
# 35B-A3B)"); LMArena uses it for effort settings ("Claude Opus 5.5 (High)").
_BRACKETS = re.compile(r"\([^)]*\)")
# Amazon Bedrock version suffix, e.g. "amazon.nova-pro-v1:0".
_BEDROCK_VERSION = re.compile(r"[-_ ]v\d+:\d+$")
# A full date at the end: "o3-2025-04-16", "claude-opus-4-5-20251101",
# "claude-3-5-sonnet@20240620". Four-digit codes such as "-0731" or "-0528"
# are deliberately kept: they often name a different checkpoint.
_FULL_DATE = re.compile(r"[-_@ ]20\d{2}-?\d{2}-?\d{2}$")
# Reasoning-effort or mode tags at the end: "gpt-5-high", "grok-4.7-xhigh",
# "kimi-k2.5-thinking", "grok-4-fast-reasoning", "Kimi K2 Thinking".
_EFFORT_TAG = re.compile(r"[-_ ](?:minimal|low|medium|high|xhigh|thinking|reasoning)$")
# "-max" at the end is ambiguous: an effort level on LMArena ("gpt-6-sol-max")
# but part of some product names ("qwen3.8-max"). Used only for review flags.
_MAX_SUFFIX = re.compile(r"[-_ ]max$")


def strict_key(name: str) -> str:
    """Same-name key: lower case, "+" spelled "plus", only letters and digits.

    "GPT-4o mini", "gpt-4o-mini" and "GPT 4o Mini" all become "gpt4omini";
    "Command R+" and "command-r-plus" both become "commandrplus".
    """
    return re.sub(r"[^a-z0-9]", "", name.lower().replace("+", "plus"))


def _without_tags(name: str) -> str:
    """Lower-case name with brackets, dates, version and effort tags removed."""
    text = _BRACKETS.sub(" ", name.lower()).strip()
    previous = None
    while text != previous:  # repeat: "deepseek-v4-pro-high-20260813" has two
        previous = text
        text = _BEDROCK_VERSION.sub("", text)
        text = _FULL_DATE.sub("", text)
        text = _EFFORT_TAG.sub("", text).strip()
    return text


def loose_key(name: str) -> str:
    """Same name plus a tag: the strict key after removing tags.

    "Gemini 2.5 Pro (Mar 2025)" -> "gemini25pro";
    "claude-opus-4-5-20251101" -> "claudeopus45"; "gpt-5-high" -> "gpt5".
    """
    return strict_key(_without_tags(name))


def max_key(name: str) -> str:
    """Loose key after also removing a final "-max" (review-only matches)."""
    return strict_key(_MAX_SUFFIX.sub("", _without_tags(name)))


def model_stem(model_key: str) -> str:
    """LiteLLM key without its provider and region prefixes.

    "azure/eu/gpt-4o-2024-08-06" -> "gpt-4o-2024-08-06".
    """
    return model_key.rsplit("/", 1)[-1].lower()


# ---------------------------------------------------------------------------
# Source extracts
# ---------------------------------------------------------------------------

def extract_sources(raw_dir: Path, source_dir: Path = SOURCE) -> dict[str, pd.DataFrame]:
    """Cut slim, redistributable extracts from the full source files.

    Writes ``data/source/*.csv`` (or into ``source_dir``) and returns the
    three extracts. Rows keep the order of the original files, which matters
    for LiteLLM (see build_models, rule 3). Raw numbers are parsed with
    pandas' default float converter, as in the original analysis: a price
    stored as "1.5999999999999999" reads as 1.6. The difference (under 1e-15)
    is noise from converting per-token prices to per-million prices.
    """
    raw_dir = Path(raw_dir)
    read = {name: raw_dir / file for name, file in RAW_FILES.items()}
    missing = [str(path) for path in read.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Raw source files not found: {missing}")

    # Epoch AI: every model, only the columns the dashboard uses.
    epoch = pd.read_csv(read["epoch"], dtype=SOURCE_DTYPES["epoch"], **RAW_READ_OPTIONS)
    _require_columns(epoch, SOURCE_COLUMNS["epoch"], "Epoch file")
    epoch = epoch[SOURCE_COLUMNS["epoch"]]

    # LiteLLM: chat models with a listed output price. Rows with no price
    # cannot price anything; embedding, image and "responses"-only entries are
    # not chat models. A listed price of $0 (local runtimes such as Ollama) is
    # kept because it still names the model; build_models() ignores it when
    # summarising prices.
    litellm = pd.read_csv(
        read["litellm"],
        dtype={"model_key": str, "mode": str, "output_usd_per_million": "float64"},
        usecols=["model_key", "mode", "output_usd_per_million"],
        **RAW_READ_OPTIONS,
    )
    keep = litellm["mode"].eq("chat") & litellm["output_usd_per_million"].notna()
    litellm = litellm.loc[keep, SOURCE_COLUMNS["litellm"]]

    # LMArena: only the overall text leaderboard (not per-category boards).
    lmarena = pd.read_csv(
        read["lmarena"],
        dtype={"model_name": str, "category": str, "leaderboard_publish_date": str},
        **RAW_READ_OPTIONS,
    )
    _require_columns(lmarena, SOURCE_COLUMNS["lmarena"] + ["is_overall"], "LMArena file")
    is_overall = lmarena["is_overall"].astype(str).eq("True")
    lmarena = lmarena.loc[is_overall, SOURCE_COLUMNS["lmarena"]].copy()
    lmarena["vote_count"] = _whole_numbers(lmarena["vote_count"], "LMArena vote_count")

    sources = {"epoch": epoch, "litellm": litellm, "lmarena": lmarena}
    source_dir = Path(source_dir)
    source_dir.mkdir(parents=True, exist_ok=True)
    for name, frame in sources.items():
        frame.to_csv(source_dir / SOURCE_FILES[name].name, index=False)
    return {name: frame.reset_index(drop=True) for name, frame in sources.items()}


def read_sources(source_dir: Path = SOURCE) -> dict[str, pd.DataFrame]:
    """Read the three slim extracts with explicit column types."""
    sources = {}
    for name, path in SOURCE_FILES.items():
        path = Path(source_dir) / path.name
        frame = pd.read_csv(path, dtype=SOURCE_DTYPES[name], **READ_OPTIONS)
        _require_columns(frame, SOURCE_COLUMNS[name], path.name)
        sources[name] = frame[SOURCE_COLUMNS[name]]
    return sources


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------

def _price_summary(prices: pd.DataFrame, key: str) -> pd.DataFrame:
    """One row per name key: representative LiteLLM key and price summary."""
    positive = prices["output_usd_per_million"].where(prices["output_usd_per_million"] > 0)
    return (
        prices.assign(positive_price=positive)
        .groupby(key, sort=False)
        .agg(
            litellm_match=("model_key", "first"),
            price_providers=("positive_price", "count"),
            output_price_usd_per_million=("positive_price", "median"),
            output_price_min=("positive_price", "min"),
            output_price_max=("positive_price", "max"),
        )
    )


def _best_rated(arena: pd.DataFrame, key: str) -> pd.DataFrame:
    """One row per name key: the highest-rated LMArena entry carrying it."""
    ranked = arena.sort_values("rating", ascending=False, kind="stable")
    return ranked.drop_duplicates(key).set_index(key)


def _find(levels: list[tuple[str, pd.DataFrame, str]]) -> tuple[str, pd.Series | None]:
    """Try each (match type, lookup table, key) in order; first hit wins."""
    for match_type, table, key in levels:
        if key in table.index:
            return match_type, table.loc[key]
    return "none", None


def _match_status(litellm_type: str, lmarena_type: str, version_unclear: bool) -> str:
    """Human label summarising how a model was matched."""
    if lmarena_type == "max_tag_review":
        return MAX_REVIEW
    in_litellm = litellm_type != "none"
    in_lmarena = lmarena_type != "none"
    if in_litellm and in_lmarena:
        if version_unclear:
            return ALL_UNCLEAR
        if litellm_type == "same_name" and lmarena_type == "same_name":
            return ALL_SAME
        return ALL_TAG
    if in_litellm:
        return LITELLM_ONLY
    if in_lmarena:
        return LMARENA_ONLY
    return EPOCH_ONLY


def build_models(sources: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Match the three sources and return one row per Epoch model.

    Matching rules, in plain English:

    1. Name keys. Every name is reduced to a *strict key*: lower case, "+"
       spelled "plus", and everything except letters and digits removed.
       A *loose key* first removes tags that are not part of the product
       name: anything in brackets, a full date at the end, a Bedrock version
       ("-v1:0"), and effort or mode tags at the end ("-high", "-xhigh",
       "-thinking", "-reasoning", ...). Words that can name a different
       product are kept: "Preview", "Instruct", "Chat", "Mini", "Turbo" and
       four-digit codes such as "0731" or "0528". For LiteLLM only the part
       after the last "/" is used; the rest names the provider and region.
    2. "same_name" means the strict keys are equal. Only when that fails do we
       try "tag_stripped": equal loose keys.
    3. LiteLLM: all chat price rows with the matching key count. The first of
       them in LiteLLM's file is shown as the example key. The price is the
       median output price (US$ per million tokens) across those rows, with
       the cheapest and dearest; "price_providers" counts the rows (one row
       per provider and region). A $0 listing (e.g. a local Ollama build)
       still names the model and can be the example key, but $0 is not a
       market price, so it is left out of the price summary and the count.
    4. LMArena (overall leaderboard only): if several entries match at the
       same level (e.g. "Claude Opus 5 (High)" and "Claude Opus 5 (Max)"),
       the highest-rated one is used: the best rating the model achieves.
    5. "max_tag_review": a match found only by also dropping a final "-max"
       from the LMArena name ("gpt-6-sol-max" for "GPT-6 Sol"). "Max" may be
       an effort setting or part of a different product, so a person should
       check it; these rows are not counted as three-way matches.
    6. "version_unclear": several Epoch models share a loose key (three
       "GPT-4o (...)" snapshots) and this one was matched through that loose
       key, so the price or rating cannot be tied to one snapshot.
    """
    epoch = sources["epoch"].copy()
    prices = sources["litellm"].copy()
    arena = sources["lmarena"].copy()

    epoch["strict_key"] = epoch["model"].map(strict_key)
    epoch["loose_key"] = epoch["model"].map(loose_key)
    shares_loose_key = epoch["loose_key"].duplicated(keep=False)

    stems = prices["model_key"].map(model_stem)
    prices["strict_key"] = stems.map(strict_key)
    prices["loose_key"] = stems.map(loose_key)
    price_by_strict = _price_summary(prices, "strict_key")
    price_by_loose = _price_summary(prices, "loose_key")

    arena["strict_key"] = arena["model_name"].map(strict_key)
    arena["loose_key"] = arena["model_name"].map(loose_key)
    arena["max_key"] = arena["model_name"].map(max_key)
    arena_by_strict = _best_rated(arena, "strict_key")
    arena_by_loose = _best_rated(arena, "loose_key")
    arena_by_max = _best_rated(arena, "max_key")

    records = []
    for model, shared in zip(epoch.itertuples(index=False), shares_loose_key, strict=True):
        litellm_type, price = _find([
            ("same_name", price_by_strict, model.strict_key),
            ("tag_stripped", price_by_loose, model.loose_key),
        ])
        lmarena_type, rated = _find([
            ("same_name", arena_by_strict, model.strict_key),
            ("tag_stripped", arena_by_loose, model.loose_key),
            ("max_tag_review", arena_by_max, model.loose_key),
        ])
        via_loose_key = litellm_type == "tag_stripped" or lmarena_type in (
            "tag_stripped", "max_tag_review")
        version_unclear = bool(shared and via_loose_key)
        record = {
            "model": model.model,
            "release_date": model.release_date,
            "organization": model.organization_primary,
            "country": model.country,
            "route": ROUTES.get(model.epoch_accessibility_group, ROUTES["Other"]),
            "epoch_accessibility": model.epoch_accessibility,
            "eci": model.eci,
            "eci_ci_low": model.eci_ci_low,
            "eci_ci_high": model.eci_ci_high,
            "litellm_match": None,
            "litellm_match_type": litellm_type,
            "price_providers": 0,
            "output_price_usd_per_million": None,
            "output_price_min": None,
            "output_price_max": None,
            "lmarena_match": None,
            "lmarena_match_type": lmarena_type,
            "arena_rating": None,
            "arena_rating_lower": None,
            "arena_rating_upper": None,
            "arena_votes": None,
            "version_unclear": version_unclear,
            "match_status": _match_status(litellm_type, lmarena_type, version_unclear),
        }
        if price is not None:
            record.update(price[[
                "litellm_match", "price_providers", "output_price_usd_per_million",
                "output_price_min", "output_price_max",
            ]].to_dict())
        if rated is not None:
            record.update({
                "lmarena_match": rated["model_name"],
                "arena_rating": rated["rating"],
                "arena_rating_lower": rated["rating_lower"],
                "arena_rating_upper": rated["rating_upper"],
                "arena_votes": rated["vote_count"],
            })
        records.append(record)

    frame = pd.DataFrame.from_records(records)
    frame["release_year"] = pd.to_datetime(
        frame["release_date"], format="%Y-%m-%d", errors="raise").dt.year
    for column in STRING_COLUMNS:
        frame[column] = frame[column].astype("str")
    for column in FLOAT_COLUMNS:
        frame[column] = pd.to_numeric(frame[column]).astype("float64")
    # Ratings are shown to one decimal place; finer detail is noise.
    frame[ARENA_COLUMNS] = frame[ARENA_COLUMNS].round(1)
    frame["price_providers"] = frame["price_providers"].astype("Int64")
    frame["arena_votes"] = frame["arena_votes"].astype("Int64")
    frame["version_unclear"] = frame["version_unclear"].astype(bool)
    # Highest ECI first; ties keep Epoch's order.
    frame = frame.sort_values("eci", ascending=False, kind="stable")
    return frame[COLUMNS].reset_index(drop=True)


# ---------------------------------------------------------------------------
# Validation and loading
# ---------------------------------------------------------------------------

def validate(frame: pd.DataFrame) -> None:
    """Raise ValueError if the dataset breaks a documented expectation."""
    _require_columns(frame, COLUMNS, "Dataset")
    if frame["model"].isna().any():
        raise ValueError("Every row needs a model name")
    duplicates = frame.loc[frame["model"].duplicated(), "model"].tolist()
    if duplicates:
        raise ValueError(f"Duplicate model names: {duplicates[:5]}")

    dates = frame["release_date"]
    if not pd.api.types.is_datetime64_any_dtype(dates):
        dates = pd.to_datetime(dates, format="%Y-%m-%d", errors="raise")
    low, high = (pd.Timestamp(day) for day in RELEASE_DATE_RANGE)
    if dates.isna().any() or not dates.between(low, high).all():
        raise ValueError(f"release_date outside {RELEASE_DATE_RANGE[0]}..{RELEASE_DATE_RANGE[1]}")
    if not (pd.to_numeric(frame["release_year"]) == dates.dt.year).all():
        raise ValueError("release_year does not match release_date")

    eci = frame[["eci", "eci_ci_low", "eci_ci_high"]].apply(pd.to_numeric)
    if eci["eci"].isna().any() or not eci.stack().dropna().between(*ECI_RANGE).all():
        raise ValueError(f"ECI values outside {ECI_RANGE[0]:g}..{ECI_RANGE[1]:g}")

    prices = frame[PRICE_COLUMNS].apply(pd.to_numeric)
    if (prices < 0).any().any():
        raise ValueError("Negative output price")
    arena = frame[ARENA_COLUMNS].apply(pd.to_numeric)
    if not arena.stack().dropna().between(*ARENA_RANGE).all():
        raise ValueError(f"LMArena values outside {ARENA_RANGE[0]:g}..{ARENA_RANGE[1]:g}")
    votes = pd.to_numeric(frame["arena_votes"])
    if (votes.dropna() <= 0).any():
        raise ValueError("arena_votes must be positive")

    for column, allowed in (
        ("route", set(ROUTES.values())),
        ("litellm_match_type", set(LITELLM_MATCH_TYPES)),
        ("lmarena_match_type", set(LMARENA_MATCH_TYPES)),
        ("match_status", set(MATCH_STATUSES)),
    ):
        unexpected = set(frame[column].dropna()) - allowed
        if unexpected or frame[column].isna().any():
            raise ValueError(f"Unexpected {column} values: {sorted(map(str, unexpected))}")
    if not pd.api.types.is_bool_dtype(frame["version_unclear"]):
        raise ValueError("version_unclear must be True or False")

    no_litellm = frame["litellm_match_type"].eq("none")
    if (no_litellm != frame["litellm_match"].isna()).any():
        raise ValueError("litellm_match and litellm_match_type disagree")
    if (no_litellm & prices.notna().any(axis=1)).any():
        raise ValueError("Price present without a LiteLLM match")
    if (no_litellm & pd.to_numeric(frame["price_providers"]).ne(0)).any():
        raise ValueError("price_providers present without a LiteLLM match")
    no_lmarena = frame["lmarena_match_type"].eq("none")
    if (no_lmarena != frame["lmarena_match"].isna()).any():
        raise ValueError("lmarena_match and lmarena_match_type disagree")
    if (no_lmarena & (arena.notna().any(axis=1) | votes.notna())).any():
        raise ValueError("Rating present without an LMArena match")

    recent = frame.loc[pd.to_numeric(frame["release_year"]).between(*RECENT_YEARS), "match_status"]
    all_three = int(recent.isin([ALL_SAME, ALL_TAG]).sum())
    same_name = int(recent.eq(ALL_SAME).sum())
    if all_three == 0 or same_name > all_three:
        raise ValueError(
            f"Implausible three-way matches for {RECENT_YEARS[0]}-{RECENT_YEARS[1]} releases: "
            f"{all_three} in all three sources, {same_name} by same name"
        )


def read_dataset(path) -> pd.DataFrame:
    """Read models.csv (or its sample) with explicit, lossless column types.

    Only empty fields are missing; text such as "NA" stays text. Integers
    that may be missing use pandas' nullable Int64; release_date is a date.
    """
    frame = pd.read_csv(
        path,
        dtype={
            **{column: str for column in STRING_COLUMNS + ["version_unclear"]},
            **{column: "float64" for column in FLOAT_COLUMNS},
            "release_year": "int64",
            "price_providers": "Int64",
            "arena_votes": "Int64",
        },
        **READ_OPTIONS,
    )
    _require_columns(frame, COLUMNS, str(path))
    flags = frame["version_unclear"].map({"True": True, "False": False})
    if flags.isna().any():
        raise ValueError("version_unclear must be True or False")
    frame["version_unclear"] = flags.astype(bool)
    frame["release_date"] = pd.to_datetime(frame["release_date"], format="%Y-%m-%d", errors="raise")
    return frame[COLUMNS]


def dataset_path() -> Path:
    """The file the app should show: the sample in sample mode or if needed."""
    sample_mode = os.getenv("DASHBOARD_SAMPLE_MODE", "0") == "1"
    return SAMPLE if sample_mode or not PROCESSED.exists() else PROCESSED


def load(path=None) -> pd.DataFrame:
    """Load the dashboard dataset (default: see dataset_path())."""
    return read_dataset(dataset_path() if path is None else path)


def same_dataset(left: pd.DataFrame, right: pd.DataFrame) -> bool:
    """True when two datasets hold the same rows (floats within 1e-9)."""
    def tidy(frame: pd.DataFrame) -> pd.DataFrame:
        if not pd.api.types.is_datetime64_any_dtype(frame["release_date"]):
            frame = read_dataset(io.StringIO(frame.to_csv(index=False)))
        return frame[COLUMNS].sort_values("model").reset_index(drop=True)

    try:
        pd.testing.assert_frame_equal(
            tidy(left), tidy(right), check_exact=False, rtol=0, atol=1e-9,
            check_dtype=False,
        )
    except AssertionError:
        return False
    return True


# ---------------------------------------------------------------------------
# Helpers and command line
# ---------------------------------------------------------------------------

def _require_columns(frame: pd.DataFrame, columns: list[str], label: str) -> None:
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise ValueError(f"{label} is missing columns: {missing}")


def _whole_numbers(values: pd.Series, label: str) -> pd.Series:
    numbers = pd.to_numeric(values)
    if not (numbers.dropna() % 1 == 0).all():
        raise ValueError(f"{label} must hold whole numbers")
    return numbers.astype("Int64")


def _write(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    print(f"Wrote {len(frame)} rows to {path.relative_to(ROOT)}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--extract", metavar="RAW_DIR", type=Path,
                        help="refresh data/source/ from the full source files in RAW_DIR and stop")
    parser.add_argument("--write-sample", action="store_true",
                        help="also (re)write data/models_sample.csv from the rebuild")
    parser.add_argument("--validate", action="store_true",
                        help="validate data/models.csv and stop")
    args = parser.parse_args(argv)
    sample_mode = os.getenv("DASHBOARD_SAMPLE_MODE", "0") == "1"

    if args.extract:
        if sample_mode:
            parser.error("Unset DASHBOARD_SAMPLE_MODE before refreshing data/source/")
        sources = extract_sources(args.extract)
        for name, frame in sources.items():
            print(f"Wrote {len(frame)} rows to {SOURCE_FILES[name].relative_to(ROOT)}")
        return
    if args.validate:
        validate(read_dataset(PROCESSED))
        print(f"{PROCESSED.relative_to(ROOT)} is valid")
        return
    if args.write_sample and sample_mode:
        parser.error("Sample mode never rewrites the sample; unset DASHBOARD_SAMPLE_MODE")

    frame = build_models(read_sources())
    validate(frame)
    if args.write_sample:
        _write(frame, SAMPLE)
    elif SAMPLE.exists() and not same_dataset(frame, read_dataset(SAMPLE)):
        raise SystemExit(
            f"The rebuild differs from {SAMPLE.relative_to(ROOT)}. If the change is "
            "intended, review it and rerun with --write-sample."
        )
    _write(frame, PROCESSED)


if __name__ == "__main__":
    main()
