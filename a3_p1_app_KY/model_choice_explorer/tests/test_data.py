"""Tests for the Model Choice Explorer data pipeline (src/data.py)."""

from __future__ import annotations

import hashlib
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src import data  # noqa: E402


PROTOTYPE = data.DATA / "_prototype_models.csv"
RAW_DIR = Path(os.getenv("MODEL_EXPLORER_RAW_DIR", ROOT.parent / "_raw_inputs"))


@pytest.fixture(scope="module")
def rebuilt() -> pd.DataFrame:
    return data.build_models(data.read_sources())


@pytest.fixture(scope="module")
def sample() -> pd.DataFrame:
    return data.read_dataset(data.SAMPLE)


def row(frame: pd.DataFrame, model: str) -> pd.Series:
    matches = frame.loc[frame["model"] == model]
    assert len(matches) == 1, f"{model!r} should appear exactly once"
    return matches.iloc[0]


# --- Rebuild and contract -------------------------------------------------

def test_rebuild_equals_sample(rebuilt, sample):
    assert len(rebuilt) == 277
    assert list(rebuilt.columns) == data.COLUMNS
    assert data.same_dataset(rebuilt, sample)


@pytest.mark.skipif(not PROTOTYPE.exists(), reason="prototype table not present")
def test_rebuild_equals_prototype(rebuilt):
    assert data.same_dataset(rebuilt, data.read_dataset(PROTOTYPE))


def test_validate_passes(rebuilt, sample):
    data.validate(rebuilt)
    data.validate(sample)
    if data.PROCESSED.exists():
        data.validate(data.read_dataset(data.PROCESSED))


def test_recent_three_way_counts(sample):
    recent = sample.loc[sample["release_year"].between(2025, 2026), "match_status"]
    assert recent.isin([data.ALL_SAME, data.ALL_TAG]).sum() == 84
    assert (recent == data.ALL_SAME).sum() == 44


def test_read_dataset_types(sample):
    assert sample["model"].dtype == "str"
    assert pd.api.types.is_datetime64_any_dtype(sample["release_date"])
    assert sample["price_providers"].dtype == "Int64"
    assert sample["arena_votes"].dtype == "Int64"
    assert sample["version_unclear"].dtype == bool
    assert sample["eci"].dtype == "float64"
    # Missing text stays missing (not the string "nan").
    assert sample["country"].isna().sum() == 17
    assert not sample["country"].eq("nan").any()


@pytest.mark.skipif(not RAW_DIR.exists(), reason="raw source files not available")
def test_extract_reproduces_source_files(tmp_path):
    data.extract_sources(RAW_DIR, tmp_path)
    for path in data.SOURCE_FILES.values():
        assert (tmp_path / path.name).read_bytes() == path.read_bytes(), path.name


# --- Spot checks of known matches -----------------------------------------

SPOT_CHECKS = {
    # Same name in LiteLLM; LMArena only lists the "(High)" effort setting.
    "Claude Opus 5.5": {
        "litellm_match_type": "same_name", "price_providers": 4,
        "output_price_usd_per_million": 20.0,
        "lmarena_match": "Claude Opus 5.5 (High)", "lmarena_match_type": "tag_stripped",
        "match_status": data.ALL_TAG,
    },
    "GPT-5.5": {
        "litellm_match_type": "same_name", "litellm_match": "azure_ai/gpt-5.5",
        "lmarena_match": "gpt-5.5", "lmarena_match_type": "same_name",
        "match_status": data.ALL_SAME,
    },
    # Three Epoch snapshots share the loose key "gemini25pro".
    "Gemini 2.5 Pro (Mar 2025)": {
        "litellm_match_type": "tag_stripped", "lmarena_match": "gemini-2.5-pro",
        "lmarena_match_type": "tag_stripped", "version_unclear": True,
        "match_status": data.ALL_UNCLEAR,
    },
    # Only found by dropping "-max": a person must check it.
    "GPT-6.1 Sol": {
        "litellm_match_type": "same_name", "lmarena_match": "gpt-6.1-sol-max",
        "lmarena_match_type": "max_tag_review", "match_status": data.MAX_REVIEW,
    },
    "Claude Haiku 5.5": {
        "litellm_match_type": "same_name", "lmarena_match_type": "none",
        "arena_rating": None, "match_status": data.LITELLM_ONLY,
    },
    # Two LMArena settings match; the higher-rated "(Max)" wins, although
    # "(High)" has more votes.
    "Claude Opus 5": {"lmarena_match": "Claude Opus 5 (Max)", "arena_votes": 32495},
    "GPT-4o (Aug 2024)": {
        "litellm_match": "azure/eu/gpt-4o-2024-08-06", "price_providers": 21,
        "lmarena_match": "gpt-4o-2024-05-13", "match_status": data.ALL_UNCLEAR,
    },
    # A $0 Ollama row is the example key, but is not counted as a price.
    "Llama 3-70B": {
        "litellm_match": "ollama/llama3:70b", "price_providers": 2,
        "output_price_usd_per_million": 1.77,
    },
    # The Bedrock version suffix "-v1:0" is a tag.
    "Amazon Nova Pro": {
        "litellm_match": "amazon.nova-pro-v1:0", "litellm_match_type": "tag_stripped",
        "price_providers": 3, "output_price_usd_per_million": 3.84,
    },
    # "+" is spelled "plus" before comparing names.
    "Command R+": {
        "litellm_match": "azure/command-r-plus", "lmarena_match": "command-r-plus",
        "match_status": data.ALL_SAME,
    },
    # "grok-4-0709" is not stripped to "grok-4": four-digit codes are kept.
    "Grok 4": {"lmarena_match_type": "none", "match_status": data.LITELLM_ONLY},
    "Qwen 3.5 Flash (hosted 35B-A3B)": {
        "lmarena_match": "qwen3.5-flash", "match_status": data.LMARENA_ONLY,
    },
}


@pytest.mark.parametrize("model", SPOT_CHECKS)
def test_spot_checks(sample, model):
    record = row(sample, model)
    for column, expected in SPOT_CHECKS[model].items():
        actual = record[column]
        if expected is None:
            assert pd.isna(actual), f"{model}: {column}"
        elif isinstance(expected, float):
            assert math.isclose(actual, expected, abs_tol=1e-9), f"{model}: {column}"
        else:
            assert actual == expected, f"{model}: {column} is {actual!r}"


# --- Name keys -------------------------------------------------------------

@pytest.mark.parametrize(
    ("function", "name", "key"),
    [
        (data.strict_key, "Command R+", "commandrplus"),
        (data.strict_key, "GPT-4o mini", "gpt4omini"),
        (data.loose_key, "Gemini 2.5 Pro (Mar 2025)", "gemini25pro"),
        (data.loose_key, "claude-opus-4-5-20251101", "claudeopus45"),
        (data.loose_key, "o3-2025-04-16", "o3"),
        (data.loose_key, "claude-3-5-sonnet@20240620", "claude35sonnet"),
        (data.loose_key, "Kimi K2 Thinking", "kimik2"),
        (data.loose_key, "grok-4-fast-reasoning", "grok4fast"),
        (data.loose_key, "deepseek-v4-pro-high-20260813", "deepseekv4pro"),
        (data.loose_key, "amazon.nova-pro-v1:0", "amazonnovapro"),
        (data.loose_key, "deepseek-v4-flash-0731", "deepseekv4flash0731"),
        (data.loose_key, "qwen3.6-max-preview", "qwen36maxpreview"),
        (data.loose_key, "gpt-6-sol-max", "gpt6solmax"),
        (data.max_key, "gpt-6-sol-max", "gpt6sol"),
        (data.model_stem, "azure/eu/gpt-4o-2024-08-06", "gpt-4o-2024-08-06"),
    ],
)
def test_name_keys(function, name, key):
    assert function(name) == key


# --- Validation rejects broken data ---------------------------------------

def _first(frame, **conditions):
    mask = pd.Series(True, index=frame.index)
    for column, value in conditions.items():
        mask &= frame[column] == value
    return frame.index[mask][0]


def _duplicate(frame):
    return pd.concat([frame, frame.iloc[[0]]], ignore_index=True)


def _set(column, value, **conditions):
    def mutate(frame):
        frame = frame.copy()
        frame.loc[_first(frame, **conditions) if conditions else 0, column] = value
        return frame
    return mutate


BROKEN = {
    "missing columns": (lambda frame: frame.drop(columns="eci"), "missing columns"),
    "duplicate model": (_duplicate, "Duplicate model"),
    "early release": (_set("release_date", pd.Timestamp("2023-01-01")), "release_date"),
    "ECI too high": (_set("eci", 250.0), "ECI"),
    "negative price": (_set("output_price_min", -1.0, litellm_match_type="same_name"), "Negative"),
    "arena too low": (
        _set("arena_rating", 700.0, lmarena_match_type="same_name"), "LMArena values"),
    "unknown status": (_set("match_status", "Maybe"), "match_status"),
    "price without match": (
        _set("output_price_usd_per_million", 1.0, litellm_match_type="none"),
        "Price present without a LiteLLM match"),
    "rating without match": (
        _set("arena_rating", 1200.0, lmarena_match_type="none"),
        "Rating present without an LMArena match"),
    "count changed": (
        _set("match_status", data.EPOCH_ONLY, match_status=data.ALL_SAME, release_year=2025),
        "three-way matches"),
}


@pytest.mark.parametrize("case", BROKEN)
def test_validate_rejects(sample, case):
    mutate, message = BROKEN[case]
    with pytest.raises(ValueError, match=message):
        data.validate(mutate(sample))


# --- Command line modes ---------------------------------------------------

def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture()
def project_copy(tmp_path):
    """A disposable copy of the dashboard without its processed output."""
    copy = tmp_path / "dashboard"
    shutil.copytree(ROOT / "src", copy / "src", ignore=shutil.ignore_patterns("__pycache__"))
    (copy / "data").mkdir()
    shutil.copytree(data.SOURCE, copy / "data" / "source")
    shutil.copy2(data.SAMPLE, copy / "data" / data.SAMPLE.name)
    return copy


def _run(copy: Path, *args: str, sample_mode: bool = True) -> subprocess.CompletedProcess:
    env = {**os.environ, "DASHBOARD_SAMPLE_MODE": "1" if sample_mode else "0"}
    return subprocess.run(
        [sys.executable, "-m", "src.data", *args], cwd=copy, env=env,
        capture_output=True, text=True, timeout=60,
    )


def test_offline_mode_writes_only_processed(project_copy):
    inputs = [p for p in (project_copy / "data").rglob("*") if p.is_file()]
    before = {path: _digest(path) for path in inputs}
    result = _run(project_copy)
    assert result.returncode == 0, result.stderr
    processed = project_copy / "data" / data.PROCESSED.name
    assert data.same_dataset(data.read_dataset(processed), data.read_dataset(data.SAMPLE))
    after = {p for p in (project_copy / "data").rglob("*") if p.is_file()}
    assert after == set(inputs) | {processed}
    assert all(_digest(path) == digest for path, digest in before.items())


def test_sample_mode_refuses_refresh(project_copy):
    assert _run(project_copy, "--write-sample").returncode == 2
    assert _run(project_copy, "--extract", str(RAW_DIR)).returncode == 2


def test_offline_mode_rejects_a_changed_sample(project_copy):
    sample_path = project_copy / "data" / data.SAMPLE.name
    frame = data.read_dataset(sample_path)
    frame.loc[0, "eci"] += 1
    frame.to_csv(sample_path, index=False, date_format="%Y-%m-%d")
    result = _run(project_copy)
    assert result.returncode != 0
    assert "differs" in result.stderr
    assert not (project_copy / "data" / data.PROCESSED.name).exists()
