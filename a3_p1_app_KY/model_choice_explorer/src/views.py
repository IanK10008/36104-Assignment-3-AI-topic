"""Streamlit views of the Model Choice Explorer.

View 1 (cost against capability) and View 2 (ranked options) each render inside
``st.container(key=<view id>)`` with a title, unit, controls, chart, how-to-read note, limitations,
filtered records, CSV download, sources and latest-observation line.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src import analysis as an
from src import data

# Okabe-Ito colours (safe for colour vision deficiency). Route colours are used in View 1,
# criterion colours in View 2, and never swap meaning.
ROUTE_COLOURS = {"Open weights": "#0072B2", "Closed weights": "#D55E00", "Other or unknown": "#8C8C8C"}
CRITERION_COLOURS = {"capability": "#6FD0A8", "preference": "#C9A8E8", "low_price": "#F5B759"}
INK, MUTED, GRID = "#1f2328", "#5b6470", "#e6e8eb"
DOWNLOAD_LABEL = "Download filtered data (CSV)"
SOURCES = {
    "epoch": ("Epoch Capabilities Index (eci_scores.csv), Benchmarking Hub", "Epoch AI",
              "https://epoch.ai/benchmarks/eci", "retrieved 17 Oct 2026, models released to 7 Oct 2026, CC BY 4.0"),
    "litellm": ("model_prices_and_context_window.json", "BerriAI LiteLLM (community-maintained)",
                "https://github.com/BerriAI/litellm", "retrieved 17 Oct 2026, current list prices, MIT licence"),
    "lmarena": ("Text leaderboard, overall category", "LMArena (now Arena)",
                "https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset",
                "snapshot published 15 Oct 2026, CC BY 4.0"),
}
CHART_W = 1200
# Toolbar on the chart: zoom box, pan, zoom in/out, autoscale, reset (double-click also resets), save as PNG.
PLOT_CONFIG = {"displayModeBar": True, "displaylogo": False, "scrollZoom": False, "doubleClick": "reset",
               "modeBarButtonsToRemove": ["select2d", "lasso2d"]}
RECORD_COLUMNS = {
    "model": "Model (Epoch name)", "release_date": "Release date", "organization": "Developer", "route": "Route",
    "eci": "Capability (ECI points)", "eci_ci_low": "ECI 90% low", "eci_ci_high": "ECI 90% high",
    "output_price_usd_per_million": "Output price (USD per million tokens, median)",
    "output_price_min": "Price min", "output_price_max": "Price max", "price_providers": "Price rows",
    "litellm_match": "LiteLLM entry", "arena_rating": "LMArena rating", "arena_rating_lower": "Rating low",
    "arena_rating_upper": "Rating high", "arena_votes": "Votes", "lmarena_match": "LMArena entry",
    "match_status": "Found in",
}


# --------------------------------------------------------------------------- #
# Shared helpers
# --------------------------------------------------------------------------- #
def money(value: float) -> str:
    """Dollar amount with two decimals everywhere, and three only for prices under one cent."""
    if value < 0.01:
        return f"${value:,.3f}"
    return f"${value:,.2f}"


def help_button(title: str, body: str) -> None:
    with st.popover(f"? {title}"):
        st.markdown(body)


def _pick(key: str, option: str) -> None:
    st.session_state[key] = option


def choice_row(title: str, key: str, options: list[str], helps: list[str], widths: list[float]) -> str:
    """One-of-several choice where every option carries its own help symbol (the circled "?") beside its label.
    The choice lives in st.session_state[key]; a stale value falls back to the first option."""
    if st.session_state.get(key) not in options:
        st.session_state[key] = options[0]
    st.markdown(f"<div style='font-size:0.875rem;margin-bottom:2px'>{title}</div>", unsafe_allow_html=True)
    cols = st.columns(widths)
    for i, (option, body) in enumerate(zip(options, helps)):
        box = f"{key}_opt{i}"
        st.session_state[box] = st.session_state[key] == option  # keeps the boxes behaving like one-of-several
        with cols[i]:
            st.checkbox(option, key=box, help=body, on_change=_pick, args=(key, option))
    return st.session_state[key]


def footer(source_keys: list[str], latest: str) -> None:
    lines = "\n".join(f"- **{SOURCES[k][0]}**, {SOURCES[k][1]}, [{SOURCES[k][2]}]({SOURCES[k][2]}), {SOURCES[k][3]}"
                      for k in source_keys)
    st.caption(f"Sources:\n\n{lines}")
    st.caption(f"Latest observation: {latest}")


def records(frame: pd.DataFrame, columns: list[str], key: str, file_name: str, note: str) -> None:
    table = frame[columns].rename(columns=RECORD_COLUMNS)
    with st.expander("**Filtered records** (the rows behind this chart)"):
        st.caption(f"{len(table):,} models match the current selection. {note} The CSV download holds the same rows.")
        st.dataframe(table, hide_index=True, height=min(35 * (len(table) + 1) + 3, 390), key=f"{key}_table")
    st.download_button(DOWNLOAD_LABEL, data=table.to_csv(index=False).encode("utf-8"), file_name=file_name,
                       mime="text/csv", key=f"{key}_download")


def axis_style(fig: go.Figure, height: int, x_title: str, y_title: str) -> None:
    fig.update_layout(width=CHART_W, height=height, plot_bgcolor="white", paper_bgcolor="white",
                      margin={"l": 70, "r": 20, "t": 20, "b": 60}, showlegend=False,
                      font={"family": "Arial, sans-serif", "size": 12, "color": INK},
                      hoverlabel={"bgcolor": "white", "font": {"size": 12, "color": INK}})
    fig.update_xaxes(title_text=x_title, showgrid=True, gridcolor=GRID, zeroline=False, linecolor="#9aa1a9",
                     ticks="outside")
    fig.update_yaxes(title_text=y_title, showgrid=True, gridcolor=GRID, zeroline=False, linecolor="#9aa1a9",
                     ticks="outside")


def legend_line(items: list[tuple[str, str]]) -> None:
    spans = " ".join(f"<span style='white-space:nowrap;margin-right:18px'><span style='display:inline-block;"
                     f"width:11px;height:11px;border-radius:50%;background:{c};margin-right:6px;"
                     f"vertical-align:-1px'></span>{label}</span>" for c, label in items)
    st.markdown(f"<div style='font-size:0.9rem;color:{MUTED}'>{spans}</div>", unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
# Weighting controls (inside View 1, used by both views)
# --------------------------------------------------------------------------- #
CRITIC_HELP = """
**CRITIC (data-driven weights)**

- **Idea:** a criterion earns more weight when it differs most from the other criteria, because it then adds
  new information that the other criteria lack.
- **In this data:** price usually moves against capability and preference, since stronger models tend to cost more,
  so price tends to receive the largest weight. Capability and preference agree closely, so they share the rest.
- **Reading the weights:** they describe the data, and the priorities of the committee are expressed with Custom
  weights.
- **Numbers:** the table under "Show the CRITIC calculation" lists the spread and the correlations behind each weight.
"""

EQUAL_HELP = """
**Custom weights (start equal)**

- **Idea:** weights say how much each criterion counts in the ranking, and the sliders let the committee decide that
  instead of the data.
- **Start point:** all sliders begin at 5, so each criterion counts for a third. Moving one slider up gives that
  criterion more say, and the shares are always rescaled to add up to 100%.
"""

PERCENTILE_HELP = """
**How the ranking is calculated**

- **Step 1:** each criterion becomes a 0 to 100 score by percentile rank among the models in all three sources
  under the current settings, so 80 means better than about 80% of them. A lower price counts as better.
- **Step 2:** the score of a model is the weighted sum of its criterion scores, and the highest score ranks first.
"""


def weight_controls(pct: pd.DataFrame, prefix: str = "",
                    criteria: tuple[str, ...] | list[str] = tuple(an.CRITERIA)) -> tuple[str, dict[str, float]]:
    criteria = list(criteria)
    st.markdown("**Ranking weights** (used by the dot sizes and the ranking in this view)" if not prefix
                else "**Ranking weights** (used by the ranking in this view)")
    method = choice_row("Weighting method", prefix + "weight_method", ["CRITIC (data-driven)", "Custom weights (start equal)"],
                        [CRITIC_HELP, EQUAL_HELP + "\n\n" + PERCENTILE_HELP],
                        [1.6, 2.1, 4.0])

    if method.startswith("CRITIC"):
        weights = an.critic_weights(pct, criteria)
    else:
        slider_labels = {"capability": "Weight: capability (Epoch)", "preference": "Weight: human preference (LMArena)",
                         "low_price": "Weight: low price (LiteLLM)"}
        raw = {c: 0 for c in an.CRITERIA}
        for col, c in zip(st.columns(len(criteria)), criteria):
            raw[c] = col.slider(slider_labels[c], 0, 10, 5, key=prefix + "w_" + c)
        weights = an.normalise(raw)
    shares = " · ".join(f"{an.CRITERION_LABELS[c]} **{weights[c] * 100:.0f}%**" for c in criteria)
    st.markdown(f"Weights in use: {shares}")
    if method.startswith("CRITIC") and len(pct) >= 3 and len(criteria) >= 2:
        shown = st.checkbox("Show the CRITIC calculation for the models shown", key=prefix + "show_critic") if prefix \
            else True
        if prefix and not shown:
            pass
        else:
            with (st.container() if prefix else st.expander("Show the CRITIC calculation for the models shown")):
                table = an.critic_table(pct, criteria)
                st.dataframe(table.style.format("{:.3f}").format("{:.1%}", subset=["Weight"]),
                             key=prefix + "critic_table")
                st.caption(f"Computed on {len(pct)} models in all three sources. Percentile columns, Pearson "
                           "correlation, population standard deviation.")
    return method, weights


# --------------------------------------------------------------------------- #
# View 1: cost against capability
# --------------------------------------------------------------------------- #
V1_HOW = """
- **Each dot is one model** with a LiteLLM price. Right = more expensive (log scale: each grid step is about 3 times
  the price). Up = more capable on the Epoch Capabilities Index.
- **Colour** is the route: blue models have downloadable weights and can be self-hosted, orange are API only, grey
  are other or unknown.
- **The black step line is the price frontier:** Walking from left to right, a model joins the line only when it is
  stronger than every cheaper model. Nothing is both cheaper and stronger than a model on the line. A dot far below
  the line is beaten on both price and capability by a model on it.
- **Ringed dots** are also on LMArena and in the ranking.
- **"Weighted ranking"** makes those ringed dots bigger as their weighted score rises and numbers the top 10 (the same
  order as View 2 when both views use the same settings). **"Best value only"** names the frontier models and ignores the weights.
- Values without hovering: every labelled model is listed with its numbers in the table under the chart.
"""

DOTS_HELP = "Choose what the chart emphasises. The question marks beside the options explain each one."
DOTS_RANK_HELP = """
**Weighted ranking** uses the weights above. Dots that are also on LMArena (ringed) grow with their weighted score,
and the top 10 are numbered in the same order as View 2 when both views use the same settings. Models that are not in all three sources are faded.
"""
DOTS_VALUE_HELP = """
**Best value only** ignores the weights. It names the models on the price frontier: each is stronger than every
cheaper model, so nothing is both cheaper and stronger.
"""

V1_LIMITS = """
- **A gap of a few points may mean nothing:** Each Epoch score has a 90% interval, typically 4 to 5 points wide for
  2026 models, and neighbouring models overlap.
- **Price is not cost:** It is the median list price per million output tokens across provider rows on one day. It
  leaves out input and cached tokens, batch discounts, regional premiums, enterprise rates and self-hosting costs.
  Reasoning models produce many more (billed) tokens per answer, so a cheaper token can cost more per task.
- **Best setting against base price:** Epoch keeps each model's best result across settings such as high reasoning
  effort, while the price is the base model's list price.
- **Not measured:** where a provider is offered (the restriction is the premise of the story), licence terms beyond
  "open weights", data handling, and usefulness for the bank's own tasks.
- **Unclear versions are left out** (one price row could belong to several dated Epoch versions).
"""


def chart_view1(points: pd.DataFrame, ranked: pd.DataFrame, mode: str, width: int = CHART_W,
                height: int = 720) -> tuple[go.Figure, pd.DataFrame]:
    chart_w = width
    margin = {"l": 70, "r": 20, "t": 20, "b": 60}
    lx = np.log10(points["output_price_usd_per_million"])
    x0, x1 = math.floor(lx.min() * 4) / 4 - 0.08, math.ceil(lx.max() * 4) / 4 + 0.08
    y0, y1 = math.floor(points["eci"].min() / 5) * 5 - 2, math.ceil(points["eci"].max() / 5) * 5 + 3
    plot_w, plot_h = chart_w - margin["l"] - margin["r"], height - margin["t"] - margin["b"]

    def px(price):
        return margin["l"] + (math.log10(price) - x0) / (x1 - x0) * plot_w

    def py(eci):
        return margin["t"] + (1 - (eci - y0) / (y1 - y0)) * plot_h

    rank_mode = mode == "Weighted ranking" and not ranked.empty
    score_of = dict(zip(ranked["model"], ranked["score"])) if not ranked.empty else {}
    rank_of = dict(zip(ranked["model"], ranked["rank"])) if not ranked.empty else {}

    s_lo = min(score_of.values()) if score_of else 0.0
    s_span = ((max(score_of.values()) - s_lo) if score_of else 0.0) or 1.0

    def radius(model: str) -> float:
        if rank_mode and model in score_of:
            return 4.0 + (score_of[model] - s_lo) / s_span * 7
        return 5.0

    fig = go.Figure()
    frontier = an.price_frontier(points)
    fx = list(frontier["output_price_usd_per_million"])
    fy = list(frontier["eci"])
    step_x, step_y = [], []
    for i, (xv, yv) in enumerate(zip(fx, fy)):
        if i:
            step_x.append(xv)
            step_y.append(fy[i - 1])
        step_x.append(xv)
        step_y.append(yv)
    step_x.append(10 ** x1)
    step_y.append(fy[-1])
    fig.add_trace(go.Scatter(x=step_x, y=step_y, mode="lines", line={"color": INK, "width": 1.6},
                             hoverinfo="skip", name="Price frontier"))

    in_ranking = points["model"].isin(score_of)
    for route, colour in ROUTE_COLOURS.items():
        part = points.loc[points["route"] == route]
        if part.empty:
            continue
        faded = rank_mode & ~part["model"].isin(score_of)
        sizes = [2 * radius(m) for m in part["model"]]
        rings = part["model"].isin(score_of)
        fig.add_trace(go.Scatter(
            x=part["output_price_usd_per_million"], y=part["eci"], mode="markers", name=route,
            marker={"size": sizes, "color": colour, "opacity": np.where(faded, 0.28, 0.95),
                    "line": {"color": np.where(rings, INK, "white"), "width": np.where(rings, 1.2, 0.8)}},
            customdata=np.stack([part["model"], part["route"], part["organization"].fillna("")], axis=1),
            hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[2]}, %{customdata[1]}<br>"
                          "Capability %{y:.1f} points<br>Output price $%{x:,.3g} per million tokens<extra></extra>"))

    # Which dots get a label
    if rank_mode:
        top = ranked.head(10)
        label_rows = [(m, m) for m in top["model"]]
        tp = points.set_index("model").loc[top["model"]]
        # the numbered dots are drawn last so no other dot hides them
        fig.add_trace(go.Scatter(
            x=tp["output_price_usd_per_million"], y=tp["eci"], mode="markers+text", text=[str(int(r)) for r in top["rank"]],
            textfont={"size": 10, "color": "white"}, textposition="middle center",
            marker={"size": [max(16, 2 * radius(m)) for m in top["model"]],
                    "color": [ROUTE_COLOURS[r] for r in tp["route"]], "line": {"color": INK, "width": 1.4}},
            customdata=np.stack([top["model"], top["score"]], axis=1),
            hovertemplate="<b>%{customdata[0]}</b><br>Weighted score %{customdata[1]:.1f}<extra></extra>"))
    else:
        label_rows = [(m, f"{m} ({e:.0f}, {money(p)})") for m, e, p in
                      zip(frontier["model"], frontier["eci"], frontier["output_price_usd_per_million"])]

    obstacles = [(px(p), py(e), radius(m) + 1) for m, p, e in
                 zip(points["model"], points["output_price_usd_per_million"], points["eci"])]
    # the frontier line is an obstacle too, so labels are never struck through by it
    path = [(px(a), py(b)) for a, b in zip(step_x, step_y)]
    for (xa, ya), (xb, yb) in zip(path, path[1:]):
        n = max(1, int(max(abs(xb - xa), abs(yb - ya)) // 6))
        obstacles += [(xa + (xb - xa) * k / n, ya + (yb - ya) * k / n, 2.0) for k in range(n + 1)]
    items = []
    for model, text in label_rows:
        prow = points.loc[points["model"] == model].iloc[0]
        items.append({"model": model, "text": text, "px": px(prow["output_price_usd_per_million"]),
                      "py": py(prow["eci"]), "r": max(9, radius(model)) if rank_mode else radius(model)})
    placed = an.place_labels(items, obstacles, (margin["l"] + 4, margin["t"] + 2, chart_w - margin["r"] - 4,
                                                height - margin["b"] - 2),
                            char_px=7.0 if rank_mode else 6.4)
    for item in placed:
        if not item["placed"]:
            continue
        prow = points.loc[points["model"] == item["model"]].iloc[0]
        # leader line from the edge of the dot to the label
        fig.add_annotation(
            x=math.log10(prow["output_price_usd_per_million"]), y=prow["eci"], xref="x", yref="y",
            ax=item["dx"], ay=item["dy"], text=f"<b>{item['text']}</b>" if rank_mode else item["text"], showarrow=True, arrowhead=0, arrowwidth=0.8,
            arrowcolor="#7d858f", standoff=item["r"] + 1, startstandoff=1,
            xanchor="left" if item["side"] == "left" else "right", yanchor="middle",
            font={"size": 11, "color": INK}, bgcolor="rgba(255,255,255,0.85)", borderpad=1)

    ticks = [t for t in [0.03, 0.1, 0.3, 1, 3, 10, 30, 100] if x0 <= math.log10(t) <= x1]
    axis_style(fig, height, "Output price ($ per million tokens, median across providers, log scale)",
               "Capability, Epoch Capabilities Index (points)")
    fig.update_xaxes(type="log", range=[x0, x1], tickvals=ticks, ticktext=[f"{t:g}" for t in ticks])
    fig.update_yaxes(range=[y0, y1], dtick=5)
    fig.update_layout(dragmode="zoom", width=chart_w, height=height)
    labelled = pd.DataFrame([{"model": i["model"], "placed": i["placed"]} for i in placed])
    return fig, labelled


def render_view1(models: pd.DataFrame, points: pd.DataFrame, ranked: pd.DataFrame, pct: pd.DataFrame,
                 window_label: str) -> tuple[str, dict[str, float]]:
    st.caption("Unit: capability in Epoch Capabilities Index points, price in US dollars per million output tokens.")
    method, weights = weight_controls(pct)
    mode = choice_row("What the dots show", "v1_mode", ["Weighted ranking", "Best value only"],
                      [DOTS_RANK_HELP, DOTS_VALUE_HELP], [1.4, 1.4, 5.0])
    if points.empty:
        st.info("No models match the selected filters. Choose more developers or a wider release window.")
        footer(["epoch", "litellm", "lmarena"], "7 Oct 2026 (latest Epoch release date in the file)")
        return method, weights

    dots = {"Open weights": "🔵 Open weights", "Closed weights": "🟠 Closed weights",
            "Other or unknown": "⚪ Other or unknown"}
    present = [r for r in dots if (points["route"] == r).any()]
    st.session_state["v1_routes"] = [r for r in st.session_state.get("v1_routes", present) if r in present]
    picked = st.pills("Select the groups of dots to display", present, selection_mode="multi",
                      format_func=lambda r: dots[r], key="v1_routes",
                      help="Ringed dots are also on LMArena and in the ranking. Hiding a group also removes it from "
                           "the price frontier and the numbered top 10 on this chart. The ranking in View 2 does not change.")
    points = points.loc[points["route"].isin(picked)].reset_index(drop=True)
    if points.empty:
        st.info("All groups are hidden. Click a group above to show its dots.")
        return method, weights
    ranked = ranked.loc[ranked["model"].isin(points["model"])]
    fig, labelled = chart_view1(points, ranked, mode)
    frontier = an.price_frontier(points)
    st.markdown(f"**{len(points)} models with a price**, released {window_label.split(' (')[0]}. "
                f"**{len(frontier)}** are on the price frontier, and **{len(ranked)}** are in all three sources.")
    st.caption("Chart toolbar (top right): drag a box to zoom, use pan, + / - or Autoscale, double-click resets.")
    st.plotly_chart(fig, width="content", key="v1_chart", config=PLOT_CONFIG)

    shown = labelled.loc[labelled["placed"], "model"].tolist() if not labelled.empty else []
    if mode == "Weighted ranking" and not ranked.empty:
        table = ranked.head(10)[["rank", "model", "route", "eci", "output_price_usd_per_million", "arena_rating",
                                 "score"]]
        table = table.rename(columns={"rank": "Rank", "model": "Model", "route": "Route", "eci": "Capability (points)",
                                      "output_price_usd_per_million": "Price (USD / M output tokens)",
                                      "arena_rating": "LMArena rating", "score": "Weighted score (0-100)"})
        caption = "Values of the 10 numbered models"
    else:
        table = frontier[["model", "route", "eci", "output_price_usd_per_million"]].rename(columns={
            "model": "Model", "route": "Route", "eci": "Capability (points)",
            "output_price_usd_per_million": "Price (USD / M output tokens)"})
        caption = "Values of the models on the price frontier, cheapest first"
    missing = set(table["Model"]) - set(shown)
    st.caption(caption + (". Labels that did not fit without overlapping: " + ", ".join(sorted(missing))
                          if missing else "."))
    st.dataframe(table.round(1), hide_index=True, key="v1_values")

    with st.expander("**How to read this chart**"):
        st.markdown(V1_HOW)
    with st.expander("**What this chart cannot show**"):
        st.markdown(V1_LIMITS)
    records(points, ["model", "release_date", "organization", "route", "eci", "eci_ci_low", "eci_ci_high",
                     "output_price_usd_per_million", "output_price_min", "output_price_max", "price_providers",
                     "litellm_match", "match_status"],
            "v1", "view1_models_with_price.csv", "Models with an unclear version are left out.")
    footer(["epoch", "litellm", "lmarena"], "7 Oct 2026 (latest Epoch release date), prices as listed on 17 Oct 2026")
    return method, weights


# --------------------------------------------------------------------------- #
# View 2: ranked options
# --------------------------------------------------------------------------- #
V2_HOW = """
- **One bar per model:** the best weighted score is at the top, and the bar length is the weighted score from 0 to 100.
- **The three coloured parts show why:** each part is weight × percentile for capability (green), human preference
  (purple) and low price (orange). A long orange part means the model ranks high mainly because it is cheap.
- **The end of each bar:** the number is the score, and the label beside the name gives the developer and the route.
- **"Wins under any weighting":** the share of all different weightings that the 0 to 10 sliders can produce (1,033 with
  three criteria) under which the model comes first. A model that wins under many mixes is a safe pick when the
  committee's priorities are unclear.
"""

V2_LIMITS = """
- **Percentile ranks are relative:** they depend on which models are in the comparison, and a small gap counts the
  same as a large one when it moves a model by one place.
- **Ties:** when the Epoch intervals or the LMArena intervals of two models overlap, the data cannot say which one is
  better, so nearby bars should be read as roughly equal.
- **Capability counted twice:** capability and preference agree at about 0.85, so giving both full weight tilts the
  ranking towards quality. CRITIC lowers both automatically.
- **Name matching:** "same name plus a tag" pairs, for example, a "(High)" LMArena entry with the base model's price.
  High effort produces more billed tokens, so the real cost can be higher. Switching the name-match rule to "same
  name only" checks this, and the top pick changes when capability carries most of the weight.
- **LMArena covers stated preference only:** voters are self-selected and favour longer, well-formatted answers, and
  safety, compliance and accuracy on banking tasks lie outside what the score measures.
- **Route labels are Epoch AI's:** open, closed and other come from the accessibility group in the Epoch file and
  describe whether the weights can be downloaded. A model in Other or unknown may become open or closed once Epoch
  classifies it, and "closed" says nothing about where the service can legally be used.
- **The ranking supports a shortlist:** licence terms, data handling and availability in Hong Kong must be checked
  separately before any approval.
"""

V2_DECISION = """
**Visual task:** Rank the candidate models and show *why* each one ranks where it does, so the architect can explain
the order to the risk committee.

**Form chosen:** A sorted horizontal bar chart (Visual Vocabulary: *ranking*), with each bar split into its
weighted parts (*part-to-whole*). Bars share one baseline, so lengths are compared accurately, long model names fit
on the left, and the score is printed at the end of each bar. Hovering a part shows its original value.

**Alternative rejected:** showing the ranking on the View 1 bubble chart (a scatter plot of price against capability,
with dot size = weighted score and the top 10 numbered). A small version is shown below. Reasons:

- **Two of the three factors dominate the picture:** the axes are Epoch capability and LiteLLM price, so the eye
  reads the chart as capability for the price. Human preference (LMArena) appears only as dot size, which is the
  weakest visual channel, so the third factor is easy to overlook and the three are not weighed fairly.
- **Size cannot be compared accurately:** two bubbles with scores of 71 and 74 look the same, yet the order of the
  top 1, 2 and 3 is exactly what the committee needs to explain.
- **Too many points hide the signal:** with 84 or more models, the dots overlap, only about 10 can be labelled and
  the rest stay unnamed, so the top ranks are hard to find and compare.
- **Ranking and correlation are mixed in one chart:** the scatter plot is good for seeing how capability and price
  relate (the price frontier). Adding a ranking on top makes the chart more complicated and weakens both messages.
- **The reason for a rank is hidden:** a bubble shows the total only, not how much capability, preference and price
  each contributed. The stacked bars above show that, so the explanation of the order belongs here.

View 1 keeps the bubble overlay as an option for readers who want to see where the top models sit relative to the
price frontier.
"""


def _route_short(route: str) -> str:
    return "Open" if route == "Open weights" else "Closed" if route == "Closed weights" else "Other"


def _original_text(frame: pd.DataFrame, criterion: str) -> list[str]:
    """Hover text with the original (unscaled) number behind one criterion for each row."""
    out = []
    for r in frame.itertuples():
        if criterion == "capability":
            out.append(f"{r.eci:.1f} points")
        elif criterion == "preference":
            out.append(f"{r.arena_rating:.0f} rating")
        else:
            out.append(f"{money(r.output_price_usd_per_million)} per M output tokens")
    return out


def chart_view2(ranked: pd.DataFrame, top_n: int, criteria: list[str], show_overall: bool = False) -> go.Figure:
    top = ranked.head(top_n).iloc[::-1]
    labels = [f"r{int(r.rank)}" for r in top.itertuples()]  # unique row keys, the visible text is drawn as columns
    fig = go.Figure()
    for c in criteria:
        values = top[f"part_{c}"]
        fig.add_trace(go.Bar(
            y=labels, x=values, orientation="h", name=an.CRITERION_LABELS[c],
            marker={"color": CRITERION_COLOURS[c], "line": {"color": "white", "width": 1}},
            text=[f"{v:.0f}" if v >= 2.5 else "" for v in values], textposition="inside", insidetextanchor="middle",
            textangle=0, constraintext="none",
            textfont={"size": 11, "color": "#1f2328"},
            customdata=np.stack([top["model"], top[f"pct_{c}"], _original_text(top, c)], axis=1),
            hovertemplate=f"<b>%{{customdata[0]}}</b><br>{an.CRITERION_LABELS[c]}: "
                          "<b>%{customdata[2]}</b><br>Percentile %{customdata[1]:.0f} · weighted part %{x:.1f}"
                          "<extra></extra>"))
    end_text = [f"<b>{r.score:.1f}</b>" for r in top.itertuples()]
    fig.add_trace(go.Scatter(y=labels, x=top["score"] + 1.2, mode="text", text=end_text, textposition="middle right",
                             textfont={"size": 12, "color": INK}, hoverinfo="skip", showlegend=False))
    row = 30 if len(top) <= 20 else 24  # compact rows when many models are shown
    height = 100 + row * len(top)
    axis_style(fig, height, "Weighted score (0-100): sum of weight × percentile rank", "")
    fig.update_layout(barmode="stack", margin={"l": 462, "r": 20, "t": 34, "b": 50}, bargap=0.28, dragmode="zoom",
                      clickmode="event+select")
    # fixed columns left of the bars: rank and model | developer | route (pixel offsets from the plot edge)
    cut = lambda text, n: text if len(text) <= n else text[: n - 1] + "…"
    columns = [(-436, "Rank and model"), (-208, "Developer"), (-83, "Route · overall" if show_overall else "Route")]
    notes = []  # all annotations are collected and set once, which is much faster than adding them one by one
    for x, head in columns:
        notes.append(dict(xref="paper", yref="paper", x=0, y=1, xshift=x, yshift=8, text=f"<b>{head}</b>",
                          showarrow=False, xanchor="left", yanchor="bottom", font={"size": 11, "color": MUTED}))
    for key, r in zip(labels, top.itertuples()):
        org = r.organization if isinstance(r.organization, str) else "Not stated"
        released = str(r.release_date)[:10]
        for x, text, colour in [(-436, cut(f"{int(r.rank)}. {r.label}", 31), INK), (-208, cut(org, 18), MUTED),
                                (-83, _route_short(r.route) + (f" · #{int(r.overall_rank)}" if show_overall else ""), MUTED)]:
            notes.append(dict(xref="paper", yref="y", x=0, y=key, xshift=x, text=text, showarrow=False,
                              xanchor="left", yanchor="middle", font={"size": 12, "color": colour}))
        # an info mark in front of the name: hovering or tapping it shows the release date
        notes.append(dict(xref="paper", yref="y", x=0, y=key, xshift=-452, text="ⓘ", showarrow=False,
                          xanchor="left", yanchor="middle", font={"size": 12, "color": "#7a8591"},
                          hovertext=f"<b>{r.model}</b><br>Released {released}", captureevents=True))
    fig.update_layout(annotations=notes)
    fig.update_traces(unselected={"marker": {"opacity": 1}, "textfont": {"color": "#1f2328"}}, selector={"type": "bar"})
    fig.update_xaxes(range=[0, max(60.0, float(top["score"].max()) * 1.15 + 6)])
    fig.update_yaxes(showgrid=False, showticklabels=False, ticks="", fixedrange=True,
                     range=[-0.6, len(top) - 0.4])
    return fig


CRITERION_PILLS = {"capability": "🟢 Capability (Epoch)", "preference": "🟣 Human preference (LMArena)",
                   "low_price": "🟠 Low price (LiteLLM)"}
CRITERIA_HELP = ("Click a criterion to leave it out and rank with the others only, for example capability + "
                 "preference (no price) or preference + price (no capability). The weights, including CRITIC, are "
                 "recalculated for the criteria that stay. The set of models stays the same: those in all three "
                 "sources.")


def _match_text(match_type) -> str:
    return {"same_name": "same name", "tag_stripped": "same name plus a tag",
            "max_tag_review": "needs a manual check"}.get(str(match_type), "none")


def render_origin(row: pd.Series, criteria: list[str]) -> None:
    """Where each number comes from: the name used in each source, how it matched, the column and the file."""
    litellm_name = row.get("litellm_match")
    arena_name = row.get("lmarena_match")
    providers = row.get("price_providers")
    rows = [{"Source": "Epoch AI (capability)", "Name in that source": row["model"], "Match": "same name",
             "Column read": "eci, eci_ci_low, eci_ci_high", "File": "epoch_eci_scores.csv",
             "Retrieved": "17 Oct 2026"},
            {"Source": "LMArena (human preference)", "Name in that source": arena_name if isinstance(arena_name, str) else "",
             "Match": _match_text(row.get("lmarena_match_type")),
             "Column read": "rating, rating_lower, rating_upper, vote_count", "File": "lmarena_overall.csv",
             "Retrieved": "snapshot 15 Oct 2026"},
            {"Source": "LiteLLM (list price)", "Name in that source": (litellm_name if isinstance(litellm_name, str) else "")
             + (f" and {int(providers) - 1} more rows" if pd.notna(providers) and int(providers) > 1 else ""),
             "Match": _match_text(row.get("litellm_match_type")),
             "Column read": "output_usd_per_million, median of the rows", "File": "litellm_chat_prices.csv",
             "Retrieved": "17 Oct 2026"}]
    st.markdown("**Where each number comes from**")
    st.dataframe(pd.DataFrame(rows), hide_index=True, key="v2_origin_table")
    st.caption("The three files are in the app folder data/source. The joined row for this model is in data/models.csv, "
               "built by the notebook \"11 Dataset combination\". Percentile = (rank − 1) / (n − 1) × 100 among the "
               "models compared, and contribution = weight × percentile.")


def render_detail(row: pd.Series, criteria: list[str], weights: dict[str, float], arena: pd.DataFrame) -> None:
    """The original numbers behind one model's bar: raw value, percentile, weight and contribution per criterion."""
    st.markdown(f"**{row['label']}** · {row['organization'] if isinstance(row['organization'], str) else 'Not stated'}"
                f" · {row['route']} · released {str(row['release_date'])[:10]} · rank {int(row['rank'])} "
                f"(overall rank {int(row['overall_rank'])}) · "
                f"weighted score **{row['score']:.1f}**")
    raw = {"capability": f"{row['eci']:.1f} points (90% interval {row['eci_ci_low']:.0f} to {row['eci_ci_high']:.0f})",
           "preference": f"{row['arena_rating']:.0f} rating ({row['arena_votes']:,.0f} votes)",
           "low_price": f"{money(row['output_price_usd_per_million'])} per million output tokens "
                        f"(range {money(row['output_price_min'])} to {money(row['output_price_max'])})"}
    table = pd.DataFrame([{
        "Criterion": an.CRITERION_LABELS[c], "Original value": raw[c], "Percentile (0-100)": round(row[f"pct_{c}"], 1),
        "Weight": f"{weights[c] * 100:.1f}%", "Contribution to score": round(row[f"part_{c}"], 1)} for c in criteria])
    st.dataframe(table, hide_index=True, key="v2_detail_table")
    render_origin(row, criteria)
    entries = an.arena_entries(arena, row.get("lmarena_match"))
    if len(entries) > 1:
        used = row.get("lmarena_match")
        lines = [f"{'**' if n == used else ''}{n}: {r:.0f}{'  (used)**' if n == used else ''}"
                 for n, r in zip(entries["model_name"], entries["rating"])]
        st.caption("LMArena lists several settings for this model, and the one used is shown in bold: "
                   + " · ".join(lines))
    elif isinstance(row.get("lmarena_match"), str):
        st.caption(f"LMArena entry used: {row['lmarena_match']}.")


def wins_help(k: int, mixes: int) -> str:
    """Help text for the "Wins under any weighting" line, with the number of weightings for the criteria in use."""
    return (
        "**How to read this line**\n\n"
        "- **What a weighting is:** one way of dividing 100% of the weight between the criteria in use, as the "
        "Custom weights sliders do. Each slider runs from 0 to 10 and the settings are turned into shares, so "
        "10 / 5 / 5 means 50% / 25% / 25%.\n"
        f"- **How {mixes:,} arises:** with {k} criteria, the sliders can be set in 11 × " + " × ".join(["11"] * (k - 1)) +
        f" = {11 ** k:,} ways, one of them (all at 0) has no meaning, and settings with the same shares count once, "
        "for example 10 / 10 / 10 and 5 / 5 / 5 are both 33% each. "
        f"What remains is {mixes:,} different weightings.\n"
        "- **What is counted:** for each weighting, every model gets its weighted score and the model with the "
        f"highest score ranks first. The percentage is the number of weightings in which a model ranks first, divided "
        f"by {mixes:,}.\n"
        "- **Example:** a model at 79% ranks first under about four in five of all slider settings, so the choice is "
        "robust. A model at 11% ranks first only under a narrow range of settings, for example when price carries "
        "almost no weight.\n"
        "- **Limit:** every weighting counts equally, including extreme ones such as 100% on price. The percentage "
        "measures robustness to the choice of weights and gives no probability of being the best model."
    )


def mini_view1(ranked: pd.DataFrame, pct: pd.DataFrame, points: pd.DataFrame) -> None:
    """Small version of the View 1 bubble chart: weighting choice only, the dots follow the View 2 selection."""
    if points is None or points.empty or ranked.empty:
        return
    st.markdown("**Small version of that chart:** Bubble size follows the weighted score and the numbers 1 to 10 "
                "are the top ranks. The models are the ones selected in this view.")
    method = choice_row("Weighting", "mini_weight_method", ["CRITIC (data-driven)", "Custom weights (start equal)"],
                        [CRITIC_HELP, EQUAL_HELP], [1.2, 2.0, 3.0])
    if method.startswith("CRITIC"):
        w = an.critic_weights(pct, list(an.CRITERIA))
    else:
        raw = {}
        for col, c in zip(st.columns(3), an.CRITERIA):
            raw[c] = col.slider(f"Weight: {an.CRITERION_LABELS[c]}", 0, 10, 5, key="mini_w_" + c)
        w = an.normalise(raw)
        if sum(raw.values()) == 0:
            st.info("Set at least one weight above zero.")
            return
    r = ranked.copy()
    r["score"] = sum(w[c] * r[f"pct_{c}"] for c in an.CRITERIA)
    r = r.sort_values(["score", "eci"], ascending=False).reset_index(drop=True)
    r["rank"] = np.arange(1, len(r) + 1)
    fig, _ = chart_view1(points, r, "Weighted ranking", width=760, height=440)
    st.plotly_chart(fig, width="content", key="mini_chart", config=PLOT_CONFIG)


def render_view2(ranked: pd.DataFrame, pct: pd.DataFrame, rule_label: str, arena: pd.DataFrame,
                 criteria: list[str], advanced=None, summary=None, points=None) -> None:
    # the weight settings sit above, and every clickable control sits directly above the chart it changes
    weights_slot = advanced if advanced is not None else st.container()
    head = st.container()
    with head:
        st.session_state.setdefault("v2_criteria", list(an.CRITERIA))
        picked = st.pills("Criteria in the ranking (click to leave one out)", list(an.CRITERIA),
                          selection_mode="multi", format_func=lambda c: CRITERION_PILLS[c],
                          key="v2_criteria", help=CRITERIA_HELP)
        groups_slot = st.container()
    if not picked:
        st.info("Select at least one criterion to rank the models.")
        return
    criteria = [c for c in an.CRITERIA if c in picked]
    if ranked.empty:
        st.info("No models match the selected filters. Choose more developers, a wider release window or the "
                "broader name-match rule.")
        footer(["epoch", "litellm", "lmarena"], "7 Oct 2026 (latest Epoch release date in the file)")
        return
    group = lambda r: r if r in ("Open weights", "Closed weights") else "Other or unknown"
    dots = {"Open weights": "🔵 Open weights", "Closed weights": "🟠 Closed weights", "Other or unknown": "⚪ Other or unknown"}
    present = [g for g in dots if (ranked["route"].map(group) == g).any()]
    with groups_slot:
        st.session_state["v2_routes"] = [g for g in st.session_state.get("v2_routes", present) if g in present]
        shown_groups = st.pills("Select the groups of models to display", present, selection_mode="multi", format_func=lambda g: dots[g], key="v2_routes",
                                help="**Groups come from Epoch AI**, not from this page.\n\n"
                                     "- **Open weights:** Epoch records the weights as downloadable (unrestricted, restricted use or "
                                     "non-commercial), so an organisation can host the model itself.\n"
                                     "- **Closed weights:** Epoch records the model as API access, hosted access without an API or "
                                     "unreleased, so the weights cannot be downloaded.\n"
                                     "- **Other or unknown:** Epoch has not placed the model in either group, for example "
                                     "\"Unknown\" or \"Limited access\". Epoch does not define these two labels in its public "
                                     "documentation.\n\n"
                                     "The groups chosen define the comparison: percentiles, CRITIC weights, scores, ranks and \"Wins "
                                     "under any weighting\" are recalculated among them. The rank in the full comparison stays "
                                     "visible as the overall rank, so a model can be compared with the groups that are switched off.")
        if not shown_groups:
            st.info("All groups are hidden. Click a group above to show its bars.")
            return
    # The groups chosen define the comparison set: percentiles, CRITIC weights, scores and ranks are recalculated
    # among them, and the rank in the full comparison is kept as "overall rank".
    ranked = ranked.assign(overall_rank=ranked["rank"])
    subset = len(shown_groups) < len(present)
    if subset:
        base = ranked.loc[ranked["route"].map(group).isin(shown_groups)]
        pct = an.percentiles(base)
    with weights_slot:
        method, weights = weight_controls(pct, "v2_", criteria)
    if subset:
        base = base.drop(columns=[c for c in base.columns if c.startswith(("pct_", "part_"))] + ["score", "rank"])
        ranked = an.score(base, pct, weights)
    view = ranked
    with head:
        ss = st.session_state
        w_text = " / ".join(f"{weights[c] * 100:.0f}" for c in criteria)
        st.caption(f"Chart settings: {str(ss.get('v2_window', '')).split(' (')[0]} · "
                   f"{str(ss.get('v2_route', '')).split(' (')[0]} · {len(ranked)} models in all three sources and the groups shown · "
                   f"weights {method.split(' (')[0]} {w_text} "
                   f"({', '.join(an.CRITERION_LABELS[c].split(' (')[0].lower() for c in criteria)}). "
                   "Unit: weighted score from 0 to 100 (weight × percentile rank among the models shown).")
        n = len(view)
        pages, start = [], 0  # pages of 25 rows, and the last page takes up to 40 rows so no tiny page is left over
        while n - start > 40:
            pages.append((start, start + 25))
            start += 25
        pages.append((start, n))
        if len(pages) > 1:
            page_names = [f"{a + 1}–{b}" for a, b in pages]
            saved = st.session_state.get("v2_page")
            if saved not in page_names:
                st.session_state["v2_page"] = page_names[0]
            chosen_page = st.pills("Models shown (rank positions in this chart)", page_names, selection_mode="single",
                                   key="v2_page",
                                   help="Each button shows one block of the ranking, about 25 models. Scores and rank "
                                        "numbers stay the same, and only the rows drawn change.") or page_names[0]
            a, b = pages[page_names.index(chosen_page)]
        else:
            a, b = 0, n
            st.caption(f"{n} model{'s' if n != 1 else ''} match the selection, so all are shown.")
    page_view = view.iloc[a:b]
    top_n = len(page_view)
    legend_line([(CRITERION_COLOURS[c], an.CRITERION_LABELS[c] + ", weighted points") for c in criteria])
    event = st.plotly_chart(chart_view2(page_view, top_n, criteria, subset), width="content", key="v2_chart",
                            config=PLOT_CONFIG, on_select="rerun", selection_mode="points")
    clicked = None
    try:
        for point in event.selection.points:
            custom = point.get("customdata") or []
            if custom:
                clicked = custom[0]
                break
    except Exception:  # no selection yet
        clicked = None
    chosen_row = ranked.loc[ranked["model"] == clicked] if clicked else ranked.iloc[0:0]
    if len(chosen_row):
        render_detail(chosen_row.iloc[0], criteria, weights, arena)
    else:
        st.caption("Showing the model ranked first. Click any part of another bar to see the original numbers and "
                   "sources behind that model. The toolbar on the chart zooms, pans and resets.")
        render_detail(ranked.iloc[0], criteria, weights, arena)

    share = an.first_place_share(ranked, ranked[[f"pct_{c}" for c in an.CRITERIA]].set_axis(an.CRITERIA, axis=1),
                                 criteria=criteria)
    ranked = ranked.assign(wins=share.values)
    winners = ranked.loc[ranked["wins"] > 0].sort_values("wins", ascending=False)
    mixes = len(an.slider_grid(len(criteria)))
    st.markdown(f"**Wins under any weighting** (share of all {mixes:,} weight mixes in which the model ranks first): "
                + ", ".join(f"{r.label} {r.wins:.0f}%" for r in winners.head(6).itertuples()) + ".",
                help=wins_help(len(criteria), mixes))

    with st.expander("**How to read this chart**"):
        st.markdown(V2_HOW)
    with st.expander("**How the score is calculated** (CRITIC weights and custom weights)"):
        picture = Path(__file__).resolve().parents[1] / "assets" / "critic_vs_custom_workflow.png"
        if picture.exists():
            st.image(str(picture), caption="Both ways of setting the weights lead to the same score formula. "
                                           "Example: GLM-5.3-Flash with the default settings.")
        else:
            st.caption("The workflow picture is missing from the assets folder.")
    with st.expander("**Design decision for this view** (task, form, rejected alternative)"):
        st.markdown(V2_DECISION)
        mini_view1(ranked, pct, points)
    with st.expander("**What this chart cannot show**"):
        st.markdown(V2_LIMITS)
    ranked = ranked.assign(developer=ranked["organization"].where(ranked["organization"].notna(), "Not stated"))
    cols = ["rank", "overall_rank", "label", "developer", "route", "release_date", "score", "eci", "arena_rating", "output_price_usd_per_million",
            "wins"]
    table = ranked.loc[page_view.index][cols]
    names = {"rank": "Rank", "overall_rank": "Overall rank", "label": "Model (LMArena setting)", "developer": "Developer", "route": "Route", "release_date": "Release date",
             "score": "Weighted score", "eci": "Capability (points)", "arena_rating": "LMArena rating",
             "output_price_usd_per_million": "Price (USD / M output tokens)", "wins": "Wins under any weighting (%)"}
    with st.expander("**Values behind the chart** (the models drawn above, with their original numbers)"):
        shown = table.rename(columns=names).copy()
        shown["Release date"] = table["release_date"].astype(str).str[:10]
        shown = shown.round(1)
        shown["Price (USD / M output tokens)"] = table["output_price_usd_per_million"].map(
            lambda v: money(v) if pd.notna(v) else "")
        st.dataframe(shown, hide_index=True, key="v2_values")
    records(ranked, ["model", "release_date", "organization", "route", "eci", "eci_ci_low", "eci_ci_high",
                     "arena_rating", "arena_rating_lower", "arena_rating_upper", "arena_votes",
                     "output_price_usd_per_million", "litellm_match", "lmarena_match", "match_status"],
            "v2", "view2_three_source_models.csv",
            f"Only models found in all three sources under the rule \"{rule_label}\".")
    footer(["epoch", "litellm", "lmarena"], "7 Oct 2026 (latest Epoch release date), prices 17 Oct 2026, "
                                            "LMArena 15 Oct 2026")
