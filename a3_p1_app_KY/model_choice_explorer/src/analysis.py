"""Scoring and chart-layout helpers for the Model Choice Explorer.

Everything here is plain pandas/numpy so each displayed number can be traced:

* ``filter_models`` applies the shared controls (release window, route, developers).
* ``price_points`` keeps the models that can be placed on the price chart (View 1).
* ``three_source`` keeps the models that have a capability score, a price and an LMArena rating (View 2).
* ``percentiles`` turns each criterion into a 0-100 percentile rank among the models shown.
* ``critic_weights`` computes the CRITIC weights (Diakoulaki, Mavrotas and Papayannakis, 1995).
* ``score`` gives the weighted score and each criterion's contribution to it.
* ``first_place_share`` is SMAA's first-rank acceptability: the share of all weightings in which a model ranks first.
* ``price_frontier`` finds the models for which nothing cheaper is stronger.
* ``place_labels`` places chart labels in pixel space so that they do not overlap each other or the dots.
"""

from __future__ import annotations

import itertools
import math
import re

import numpy as np
import pandas as pd

from src import data

# A whole-year start (a number) or a rolling window of n months counted back from the month of the latest release in
# the data, written as ("months", n). Rolling windows start on the 1st of a month and move by themselves when the
# data file is refreshed.
WINDOWS = {
    "2025 to 2026": 2025,
    "2024 to 2026": 2024,
    "2026 only": 2026,
    "Past 12 months": ("months", 12),
    "Past 6 months": ("months", 6),
}
ROUTE_CHOICES = {
    "All models": None,
    "Open weights (can be self-hosted)": "Open weights",
    "Closed weights (API only)": "Closed weights",
}
MATCH_RULES = {
    "same name, or plus a tag such as \"(High)\"": (data.ALL_SAME, data.ALL_TAG),
    "same name only (safest)": (data.ALL_SAME,),
}
CRITERIA = ["capability", "preference", "low_price"]
CRITERION_LABELS = {
    "capability": "Capability (Epoch)",
    "preference": "Human preference (LMArena)",
    "low_price": "Low price (LiteLLM)",
}


def developer_name(frame: pd.DataFrame) -> pd.Series:
    """Epoch leaves the developer blank for a few models; show them as 'Not stated'."""
    return frame["organization"].fillna("").replace("", "Not stated")


def window_start(frame: pd.DataFrame, start: int | tuple) -> pd.Timestamp:
    """First release date inside a window: 1 January of a year, or for a rolling window the 1st of the month that lies
    n months before the month of the latest release in the data (latest release in Oct 2026: 12 months gives 1 Oct 2025
    and 6 months gives 1 Apr 2026)."""
    if isinstance(start, tuple):
        return (frame["release_date"].max().to_period("M") - start[1]).start_time
    return pd.Timestamp(year=start, month=1, day=1)


def filter_models(frame: pd.DataFrame, start: int | tuple, route: str | None, developers: list[str]) -> pd.DataFrame:
    """Models released from a start year (number) or inside a rolling window of months (see ``WINDOWS``)."""
    out = frame.loc[frame["release_date"] >= window_start(frame, start)]
    if route is not None:
        out = out.loc[out["route"] == route]
    out = out.loc[developer_name(out).isin(developers)]
    return out.reset_index(drop=True)


def price_points(frame: pd.DataFrame) -> pd.DataFrame:
    """Models with a LiteLLM price whose version is clear (an unclear version could carry another version's price)."""
    keep = frame["output_price_usd_per_million"].notna() & ~frame["version_unclear"]
    return frame.loc[keep].reset_index(drop=True)


def three_source(frame: pd.DataFrame, statuses: tuple[str, ...]) -> pd.DataFrame:
    keep = (frame["match_status"].isin(statuses) & frame["output_price_usd_per_million"].notna()
            & frame["arena_rating"].notna())
    return frame.loc[keep].reset_index(drop=True)


def percentile(values: pd.Series) -> pd.Series:
    """Percentile rank 0-100: (rank - 1) / (n - 1) x 100, ties share their average rank. One model gets 50."""
    n = len(values)
    if n == 1:
        return pd.Series([50.0], index=values.index)
    return (values.rank(method="average") - 1) / (n - 1) * 100


def percentiles(frame: pd.DataFrame) -> pd.DataFrame:
    """Higher is better for all three. Low price uses the negative price (a cheaper model ranks higher).
    Taking log10 of the price first would give exactly the same ranks, so it is not needed here."""
    return pd.DataFrame({
        "capability": percentile(frame["eci"]),
        "preference": percentile(frame["arena_rating"]),
        "low_price": percentile(-frame["output_price_usd_per_million"]),
    }, index=frame.index)


def critic_table(pct: pd.DataFrame, criteria: tuple[str, ...] | list[str] = tuple(CRITERIA)) -> pd.DataFrame:
    """The CRITIC steps on the percentile columns: spread, correlation, conflict, information and weight."""
    criteria = list(criteria)
    corr = pct[criteria].corr(method="pearson")
    sd = pct[criteria].std(ddof=0)
    conflict = (1 - corr).sum(axis=1)
    info = sd * conflict
    weight = info / info.sum()
    columns = {"Standard deviation": sd}
    for c in criteria:
        columns[f"Correlation with {CRITERION_LABELS[c].split(' (')[0].lower()}"] = corr[c]
    columns.update({"Conflict = sum of (1 - r)": conflict, "Information C = sd x conflict": info, "Weight": weight})
    table = pd.DataFrame(columns)
    table.index = [CRITERION_LABELS[c] for c in criteria]
    return table


def critic_weights(pct: pd.DataFrame, criteria: tuple[str, ...] | list[str] = tuple(CRITERIA)) -> dict[str, float]:
    """CRITIC weights over the chosen criteria (the others get 0). One criterion gets all the weight."""
    criteria = list(criteria)
    out = {c: 0.0 for c in CRITERIA}
    if len(criteria) == 1:
        out[criteria[0]] = 1.0
        return out
    equal = {c: (1 / len(criteria) if c in criteria else 0.0) for c in CRITERIA}
    if len(pct) < 3:
        return equal
    weights = critic_table(pct, criteria)["Weight"].to_numpy()
    if not np.all(np.isfinite(weights)):
        return equal
    out.update(dict(zip(criteria, weights)))
    return out


def normalise(weights: dict[str, float]) -> dict[str, float]:
    total = sum(weights.values())
    return {c: weights[c] / total for c in CRITERIA} if total > 0 else {c: 0.0 for c in CRITERIA}


def score(frame: pd.DataFrame, pct: pd.DataFrame, weights: dict[str, float]) -> pd.DataFrame:
    """Weighted score = sum over criteria of weight x percentile. Each part is that criterion's contribution."""
    out = frame.copy()
    for c in CRITERIA:
        out[f"pct_{c}"] = pct[c]
        out[f"part_{c}"] = weights[c] * pct[c]
    out["score"] = sum(out[f"part_{c}"] for c in CRITERIA)
    out = out.sort_values(["score", "eci"], ascending=False).reset_index(drop=True)
    out["rank"] = np.arange(1, len(out) + 1)
    return out


def weight_grid(step: float = 0.02, k: int = 3) -> np.ndarray:
    """Every weighting over k criteria on a regular grid (non-negative, adding up to 1).
    For three criteria and a step of 0.02 that is 1,326 weightings."""
    n = round(1 / step)
    if k == 1:
        return np.array([[1.0]])
    if k == 2:
        return np.array([(i / n, (n - i) / n) for i in range(n + 1)])
    return np.array([(i / n, j / n, (n - i - j) / n) for i in range(n + 1) for j in range(n + 1 - i)])


def slider_grid(k: int = 3, top: int = 10) -> np.ndarray:
    """Every different weighting that the custom sliders can produce: each of the k criteria is set to 0 .. top
    and the settings are turned into shares. Settings with the same shares (10/10/10, 20/20/20 or 2/1/1 and 4/2/2)
    count once. For three criteria and top 10 that is 1,033 weightings."""
    if k == 1:
        return np.array([[1.0]])
    seen = set()
    for combo in itertools.product(range(top + 1), repeat=k):
        total = sum(combo)
        if total == 0:
            continue
        g = math.gcd(*combo)
        seen.add(tuple(v // g for v in combo))
    return np.array(sorted(tuple(v / sum(c) for v in c) for c in seen))


def first_place_share(frame: pd.DataFrame, pct: pd.DataFrame,
                      criteria: tuple[str, ...] | list[str] = tuple(CRITERIA)) -> pd.Series:
    """First-rank acceptability in the style of SMAA (Lahdelma and Salminen, 2001), computed on the full set of
    slider weightings instead of random draws, so the result is the same on every run: the share of all
    weightings in which each model ranks first."""
    if frame.empty:
        return pd.Series(dtype=float)
    criteria = list(criteria)
    grid = slider_grid(len(criteria))
    scores = pct[criteria].to_numpy() @ grid.T  # models x weightings
    winners = np.argmax(scores, axis=0)
    counts = np.bincount(winners, minlength=len(frame))
    return pd.Series(counts / len(grid) * 100, index=frame.index)


def price_frontier(points: pd.DataFrame) -> pd.DataFrame:
    """Walk from the cheapest model upwards; keep a model when it is stronger than every cheaper model."""
    ordered = points.sort_values(["output_price_usd_per_million", "eci"], ascending=[True, False])
    best, keep = -math.inf, []
    for idx, row in ordered.iterrows():
        if row["eci"] > best:
            keep.append(idx)
            best = row["eci"]
    return points.loc[keep]


# --------------------------------------------------------------------------- #
# Label placement (pixel space)
# --------------------------------------------------------------------------- #
def _overlaps(a: tuple[float, float, float, float], b: tuple[float, float, float, float], pad: float) -> bool:
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


def place_labels(items: list[dict], obstacles: list[tuple[float, float, float]],
                 area: tuple[float, float, float, float], char_px: float = 6.4, line_px: float = 15) -> list[dict]:
    """Greedy label placement.

    ``items``: dicts with ``px``, ``py`` (the dot in pixels) and ``text``; placed in the given order.
    ``obstacles``: (x, y, radius) of every dot, so labels never cover a dot.
    ``area``: (left, top, right, bottom) of the plotting area in pixels.
    Returns each item with ``dx``, ``dy`` (offset of the label anchor from the dot) and ``side``
    ('left' or 'right'), or ``placed=False`` when no free spot was found (the table still lists it).
    """
    left, top, right, bottom = area
    boxes: list[tuple[float, float, float, float]] = []
    dot_boxes = [(x - r, y - r, x + r, y + r) for x, y, r in obstacles]
    # the labelled dots themselves are never covered, even in the relaxed pass
    key_boxes = [(i["px"] - i.get("r", 5), i["py"] - i.get("r", 5), i["px"] + i.get("r", 5), i["py"] + i.get("r", 5))
                 for i in items]
    distances = [14, 26, 40, 56, 74, 94, 116, 140, 170, 200, 240]
    angles = [0, -30, 30, -60, 60, 180, 150, 210, 120, 240, -90, 90]
    placed = []
    for item in items:
        w = len(item["text"]) * char_px + 6
        h = line_px
        result = dict(item, placed=False)
        # Pass 1 avoids every dot; pass 2 only the dots near this one's size class is dropped, so a label may cover
        # a faded dot but never another label.
        for avoid_dots in (True, False):
            for dist in distances:
                for ang in angles:
                    rad = math.radians(ang)
                    ax, ay = item["px"] + dist * math.cos(rad), item["py"] + dist * math.sin(rad)
                    side = "left" if math.cos(rad) >= -1e-9 else "right"
                    x0 = ax if side == "left" else ax - w
                    box = (x0, ay - h / 2, x0 + w, ay + h / 2)
                    if box[0] < left or box[2] > right or box[1] < top or box[3] > bottom:
                        continue
                    if any(_overlaps(box, b, 3) for b in boxes):
                        continue
                    if avoid_dots and any(_overlaps(box, d, 1) for d in dot_boxes):
                        continue
                    if not avoid_dots and any(_overlaps(box, d, 0) for d in key_boxes):
                        continue
                    boxes.append(box)
                    result.update(placed=True, dx=ax - item["px"], dy=ay - item["py"], side=side, box=box)
                    break
                if result["placed"]:
                    break
            if result["placed"]:
                break
        placed.append(result)
    return placed


# --------------------------------------------------------------------------- #
# LMArena effort tags
# --------------------------------------------------------------------------- #
_EFFORT = re.compile(r"[-\s](xhigh|high|medium|low|minimal|thinking|reasoning|non-thinking)\b", re.I)


def effort_tag(model: str, lmarena_match) -> str:
    """The setting of the LMArena entry that supplied the rating, e.g. "High", "xhigh", "Max".
    Empty when the LMArena name equals the model name."""
    if not isinstance(lmarena_match, str) or not lmarena_match:
        return ""
    if data.strict_key(lmarena_match) == data.strict_key(model):
        return ""
    bracket = re.search(r"\(([^)]*)\)\s*$", lmarena_match)
    if bracket:
        return bracket.group(1)
    found = _EFFORT.search(lmarena_match)
    return found.group(1) if found else ""


def arena_entries(arena: pd.DataFrame, lmarena_match) -> pd.DataFrame:
    """All LMArena entries that share a loose name key with the matched entry (the settings of one model)."""
    if not isinstance(lmarena_match, str) or not lmarena_match:
        return arena.iloc[0:0]
    key = data.loose_key(lmarena_match)
    keys = arena["model_name"].map(data.loose_key)
    return arena.loc[keys == key].sort_values("rating", ascending=False)
