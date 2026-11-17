"""Story 2, View 2 (alternative): who produced the benchmark scores behind the capability index?

Reads data/hub_scores_by_model.csv and data/hub_model_coverage.csv, both written by
notebooks/benchmark_hub/benchmark_hub.ipynb. Place this module next to page.py and call
render_view4b() from the page.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

HERE = Path(__file__).resolve().parent
SCORES_PATH = HERE / "data" / "hub_scores_by_model.csv"
COVERAGE_PATH = HERE / "data" / "hub_model_coverage.csv"
CURRENCY_PATH = HERE / "data" / "hub_data_currency.csv"

YEARS = ["2023", "2024", "2025", "2026"]
KINDS = ["epoch", "third_party", "developer"]
KIND_NAME = {
    "epoch": "Run by Epoch AI",
    "third_party": "Third party or source not stated",
    "developer": "Developer-reported",
}
KIND_COLOUR = {"epoch": "#2a78d6", "third_party": "#1baf7a", "developer": "#eb6834"}
GROUP_NAME = {
    "accessible": "Accessible (open weights or non-US service)",
    "restricted": "Restricted (US developer, closed weights)",
    "combined": "Accessible and Restricted combined",
}
TOP_N = 15
FEW_MODELS = 5
SCORE_COLUMNS = ["model", "release_year", "access_group", "benchmark", "kind", "source", "score_pct"]


# --- Data ---------------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_scores(path: str = str(SCORES_PATH)) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"release_year": str})
    missing = [c for c in SCORE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    if not df["score_pct"].between(0, 100).all():
        raise ValueError("A score lies outside 0 to 100")
    if not set(df["kind"]) <= set(KINDS):
        raise ValueError("Unknown kind of source")
    if df.duplicated(["model", "benchmark", "kind"]).any():
        raise ValueError("A model has two scores for one benchmark and kind")
    return df


@st.cache_data(show_spinner=False)
def load_coverage(path: str = str(COVERAGE_PATH)) -> pd.DataFrame:
    return pd.read_csv(path, dtype={"release_year": str})


def pick(df: pd.DataFrame, year: str, group: str) -> pd.DataFrame:
    part = df[df["release_year"] == year]
    return part if group == "combined" else part[part["access_group"] == group]


def segment_counts(df: pd.DataFrame, groups: list[str]) -> pd.DataFrame:
    """One row per year, group and kind: number of scores and the share of that bar."""
    rows = []
    for group in groups:
        for year in YEARS:
            part = pick(df, year, group)
            total = len(part)
            for kind in KINDS:
                n = int((part["kind"] == kind).sum())
                rows.append({"year": year, "group": group, "kind": kind, "scores": n, "total": total,
                             "share": n / total * 100 if total else 0.0,
                             "models": int(part.loc[part["kind"] == kind, "model"].nunique())})
    return pd.DataFrame(rows)


def models_in_bar(df: pd.DataFrame, coverage: pd.DataFrame, year: str, group: str) -> tuple[int, int]:
    """Models with at least one score, and models in the capability file, for one bar."""
    groups = ["accessible", "restricted"] if group == "combined" else [group]
    scored = pick(df, year, group)["model"].nunique()
    total = int(coverage[(coverage["release_year"] == year) & coverage["access_group"].isin(groups)]
                ["models_in_capability_file"].sum())
    return scored, total


def top_items(df: pd.DataFrame, year: str, group: str, kind: str, n: int = TOP_N) -> pd.DataFrame:
    """Epoch rows are listed by benchmark. Third party and developer rows are listed by source."""
    part = pick(df, year, group)
    part = part[part["kind"] == kind]
    if part.empty:
        return pd.DataFrame()
    if kind == "epoch":
        out = part.groupby("benchmark").agg(scores=("score_pct", "size"), median=("score_pct", "median"))
        out = out.reset_index().rename(columns={"benchmark": "Benchmark", "scores": "Models scored",
                                                "median": "Median score (%)"})
        return out.sort_values(["Models scored", "Median score (%)"], ascending=False).head(n).reset_index(drop=True)
    out = part.groupby("source").agg(scores=("score_pct", "size"), models=("model", "nunique"),
                                     benchmarks=("benchmark", "nunique")).reset_index()
    out = out.rename(columns={"source": "Source", "scores": "Scores", "models": "Models",
                              "benchmarks": "Benchmarks"})
    return out.sort_values(["Scores", "Source"], ascending=[False, True]).head(n).reset_index(drop=True)


def top_models(df: pd.DataFrame, year: str, group: str, kind: str, n: int = TOP_N) -> pd.DataFrame:
    part = pick(df, year, group)
    part = part[part["kind"] == kind]
    out = part.groupby("model").size().rename("Benchmarks with a result").reset_index().rename(columns={"model": "Model"})
    return out.sort_values(["Benchmarks with a result", "Model"], ascending=[False, True]).head(n).reset_index(drop=True)


def model_scores(df: pd.DataFrame, model: str) -> pd.DataFrame:
    return df[df["model"] == model].sort_values(["kind", "score_pct"], ascending=[True, False])


def hover_text(df: pd.DataFrame, year: str, group: str, kind: str) -> str:
    part = pick(df, year, group)
    part = part[part["kind"] == kind]
    if part.empty:
        return "No scores of this kind"
    key = "benchmark" if kind == "epoch" else "source"
    top = part.groupby(key).size().sort_values(ascending=False).head(3)
    label = "Top benchmarks" if kind == "epoch" else "Top sources"
    lines = [f"{i}. {(k[:40] + '…') if len(k) > 41 else k} ({v})" for i, (k, v) in enumerate(top.items(), start=1)]
    return f"{label}:<br>" + "<br>".join(lines)


# --- Figure -------------------------------------------------------------------------------

def build_figure(df: pd.DataFrame, coverage: pd.DataFrame, groups: list[str]) -> go.Figure:
    counts = segment_counts(df, groups)
    titles = [GROUP_NAME[g] for g in groups]
    fig = make_subplots(rows=1, cols=len(groups), shared_yaxes=True, subplot_titles=titles, horizontal_spacing=0.06)
    for col, group in enumerate(groups, start=1):
        labels = []
        for year in YEARS:
            scored, total = models_in_bar(df, coverage, year, group)
            n_scores = len(pick(df, year, group))
            flag = "*" if scored < FEW_MODELS else ""
            labels.append(f"{year}{flag}<br>{scored} of {total} models<br>{n_scores} scores")
        for kind in KINDS:
            sub = counts[(counts["group"] == group) & (counts["kind"] == kind)].set_index("year").loc[YEARS]
            custom = [[y, group, kind, int(sub.loc[y, "scores"]), int(sub.loc[y, "total"]),
                       hover_text(df, y, group, kind)] for y in YEARS]
            fig.add_trace(go.Bar(
                x=labels, y=sub["share"], name=KIND_NAME[kind], legendgroup=kind,
                showlegend=(col == 1), marker=dict(color=KIND_COLOUR[kind], line=dict(color="white", width=1.5)),
                text=[f"{v:.0f}%" if v >= 6 else "" for v in sub["share"]], textposition="inside",
                insidetextanchor="middle", textfont=dict(color="white", size=12),
                customdata=custom,
                hovertemplate=("<b>%{customdata[0]} · " + KIND_NAME[kind] + "</b><br>"
                               "%{customdata[3]} of %{customdata[4]} scores (%{y:.0f}%)<br>"
                               "%{customdata[5]}<extra></extra>"),
            ), row=1, col=col)
    fig.update_layout(
        barmode="stack", height=470, margin=dict(l=10, r=10, t=60, b=10), bargap=0.25,
        legend=dict(orientation="h", yanchor="bottom", y=-0.28, x=0, title_text=""),
        hoverlabel=dict(align="left"), clickmode="event+select",
    )
    fig.update_yaxes(range=[0, 100], ticksuffix="%", title_text="Share of the scores in the bar", col=1)
    fig.update_xaxes(tickfont=dict(size=11))
    return fig


# --- Page ---------------------------------------------------------------------------------

def _height(rows: int) -> int:
    """Height in pixels that shows every row of a short table without an inner scroll bar."""
    return 38 + 35 * max(rows, 1)


def _kind_heading(kind: str) -> str:
    colour = {"epoch": "blue", "third_party": "green", "developer": "orange"}[kind]
    return f":{colour}[■] **{KIND_NAME[kind]}**"


def _segment_from_event(event) -> dict | None:
    try:
        points = event.selection.points
    except AttributeError:
        return None
    if not points:
        return None
    custom = points[0].get("customdata")
    if not custom or len(custom) < 3:
        return None
    return {"year": str(custom[0]), "group": custom[1], "kind": custom[2]}


def _score_rows(part: pd.DataFrame, kind: str) -> str:
    """One compact line per score: benchmark, a bar from 0 to 100% and the value. The source is in the hover text."""
    from html import escape

    colour = KIND_COLOUR[kind]
    blocks = []
    for row in part.itertuples():
        source = escape(str(row.source))
        for prefix in ("https://", "http://"):
            if source.startswith(prefix):
                source = source[len(prefix):]
        source = source.rstrip("/")
        name = escape(str(row.benchmark))
        blocks.append(
            f'<div title="{name} · {source}" style="display:grid;grid-template-columns:minmax(0,1fr) 56px 34px;gap:6px;'
            f'align-items:center;margin:0 0 5px;font-size:12.5px;line-height:1.2">'
            f'<span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{name}</span>'
            f'<div style="height:7px;background:rgba(128,128,128,.22);border-radius:3px">'
            f'<div style="width:{row.score_pct:.1f}%;height:7px;background:{colour};border-radius:3px"></div></div>'
            f'<span style="font-weight:600;text-align:right">{row.score_pct:.0f}%</span></div>'
        )
    return "".join(blocks)


SCORES_HEIGHT = 340


def _model_detail(df: pd.DataFrame, model: str) -> None:
    scores = model_scores(df, model)
    counts = scores["kind"].value_counts()
    group = scores["access_group"].iloc[0]
    year = scores["release_year"].iloc[0]
    n = len(scores)
    st.markdown(f"**{model}** ({group.capitalize()}, released {year}) · how its scores are counted")
    st.caption(
        f"{scores['benchmark'].nunique()} benchmarks with a result, {n} scores. "
        f"Developer-reported share: {counts.get('developer', 0) / n * 100:.0f}%. "
        "Bar = the score on a 0 to 100% scale. Hover over a line for its source. Scroll inside the box to see every score."
    )
    with st.container(height=SCORES_HEIGHT, border=False):
        columns = st.columns(3)
        for column, kind in zip(columns, KINDS):
            with column:
                st.markdown(f"{_kind_heading(kind)} ({int(counts.get(kind, 0))})")
                part = scores[scores["kind"] == kind][["benchmark", "source", "score_pct"]]
                if part.empty:
                    st.caption("No scores of this kind.")
                    continue
                st.html(_score_rows(part, kind))


def _model_panel(df: pd.DataFrame) -> None:
    """Advanced choice: any release year (or All) and any model. The values are preset by the clicked row."""
    st.caption("Choose a release year or All, then a model. Selecting a row in the models table above sets both.")
    left, right = st.columns([3, 2], gap="medium")
    with left:
        year_choice = st.radio("Release year of the model", ["All"] + YEARS, horizontal=True, key="story2_4b_year")
    pool = df if year_choice == "All" else df[df["release_year"] == year_choice]
    names = sorted(pool["model"].unique())
    if st.session_state.get("story2_4b_model") not in names:
        st.session_state["story2_4b_model"] = names[0]
    with right:
        model = st.selectbox("Model (type to search)", names, key="story2_4b_model")
    _model_detail(df, model)


TABLE_HEIGHT = 330


def _detail(df: pd.DataFrame, coverage: pd.DataFrame, segment: dict) -> None:
    year, group, kind = segment["year"], segment["group"], segment["kind"]
    part = pick(df, year, group)
    in_kind = part[part["kind"] == kind]
    scored, total = models_in_bar(df, coverage, year, group)
    share = len(in_kind) / len(part) * 100 if len(part) else 0
    label = f"{_kind_heading(kind)} · {GROUP_NAME[group]} · models released in {year}"
    panel = st.expander(label, expanded=True)
    with panel:
        _tables(df, coverage, segment, part, in_kind, scored, total, share)
    if in_kind.empty:
        return
    with st.expander("Look at model", expanded=True):
        _model_panel(df)


def _tables(df, coverage, segment, part, in_kind, scored, total, share) -> None:
    year, group, kind = segment["year"], segment["group"], segment["kind"]
    st.caption(
        f"{len(in_kind)} of {len(part)} scores ({share:.0f}%), from {in_kind['model'].nunique()} of {scored} models "
        f"with scores ({total} models of this group and year are in the capability file). "
        "Each number counts scores, not marks."
    )
    if in_kind.empty:
        st.info("No scores of this kind in this bar.")
        return
    models = top_models(df, year, group, kind)
    chosen, picked = models.loc[0, "Model"], False
    left, right = st.columns(2, gap="medium")
    with left:
        st.markdown("**Top benchmarks Epoch ran**" if kind == "epoch" else
                    ("**Top sources, third party**" if kind == "third_party" else "**Top sources, developer-reported**"))
        config = {}
        if kind == "epoch":
            config["Median score (%)"] = st.column_config.NumberColumn(
                format="%.0f%%", help="Median score of the models scored on this benchmark.")
        st.dataframe(top_items(df, year, group, kind), hide_index=True, column_config=config, height=TABLE_HEIGHT,
                     key=f"story2_4b_items_{group}_{year}_{kind}")
    with right:
        st.markdown("**Models with the most scores** (select a row)")
        event = st.dataframe(models, hide_index=True, on_select="rerun", selection_mode="single-row",
                             height=TABLE_HEIGHT, key=f"story2_4b_models_{group}_{year}_{kind}")
        rows = event.selection.rows if event is not None else []
        if rows:
            chosen, picked = models.loc[rows[0], "Model"], True
    token = (year, group, kind, chosen if picked else None)
    if st.session_state.get("story2_4b_applied") != token:
        st.session_state["story2_4b_applied"] = token
        st.session_state["story2_4b_year"] = df.loc[df["model"] == chosen, "release_year"].iloc[0]
        st.session_state["story2_4b_model"] = chosen


@st.fragment
def _body() -> None:
    try:
        df, coverage = load_scores(), load_coverage()
    except (OSError, ValueError) as exc:
        st.error(f"View 2 data could not be loaded: {exc}")
        return

    mode = st.radio("Show", ["Split: Accessible and Restricted", "Combined"], horizontal=True, key="story2_4b_mode")
    groups = ["accessible", "restricted"] if mode.startswith("Split") else ["combined"]
    fig = build_figure(df, coverage, groups)
    event = st.plotly_chart(fig, use_container_width=True, key=f"story2_4b_chart_{'split' if len(groups) == 2 else 'combined'}",
                            on_select="rerun", selection_mode="points")
    st.caption(
        "Hover over a segment for its top sources. Click a segment to open its benchmarks or sources and its models below. "
        "An asterisk after the year means fewer than 5 models with scores in the bar. "
        "Each bar is 100% of the scores for models released in that year."
    )

    segment = _segment_from_event(event)
    if segment and segment["group"] not in groups:
        segment = None
    if segment:
        st.session_state["story2_4b_pin"] = segment
    pinned = st.session_state.get("story2_4b_pin")
    if pinned and pinned["group"] in groups:
        _detail(df, coverage, pinned)

    with st.expander("**How to read this chart**"):
        st.markdown(
            "- **One score** is one model, one benchmark and one kind of source. Versions of a model "
            "(for example high or low effort) are merged and the highest score is kept.\n"
            "- **A benchmark with two kinds of source** for the same model counts twice. A benchmark with no result is not counted.\n"
            "- **Percent** is the scores of one kind divided by all scores in the bar. Models with more scores weigh more.\n"
            "- **Run by Epoch AI** means Epoch ran the benchmark itself. **Third party** means a leaderboard, website or paper "
            "by a group that is not the model developer, and also scores whose source the Hub does not state. "
            "**Developer-reported** means a score published in a technical report, model card or announcement. "
            "Such a report can also list scores for models of other developers, for example in comparison tables.\n"
            "- **Scores** are stored by the Hub as shares between 0 and 1 and shown here as percentages. Some benchmarks measure "
            "progress, win rate or pass rate rather than answers correct, so scores of different benchmarks are not comparable.\n"
            "- **Groups** follow the rule of View 1. Release year is the release year in the capability file."
        )
    try:
        info = pd.read_csv(CURRENCY_PATH).iloc[0]
        stamp = f"The benchmark ZIP was retrieved {info['zip_retrieved_utc']}."
    except (OSError, IndexError, KeyError):
        stamp = "The retrieval date of the benchmark ZIP is not recorded."
    accessible_restricted = int(coverage.loc[coverage["access_group"].isin(["accessible", "restricted"]),
                                             "models_in_capability_file"].sum())
    with st.expander("**What this chart cannot show**"):
        st.markdown(
            "- **How high the scores are:** the chart shows who produced the scores. It does not show whether the scores are high.\n"
            "- **Whether scores agree:** the chart does not compare two scores of the same model. View 3 does this for one benchmark.\n"
            f"- **Models without a score:** {df['model'].nunique()} of the {accessible_restricted} accessible and restricted models "
            "in the capability file have at least one score in the Epoch Benchmarking Hub after the names are matched. "
            "Some of the others may be matching misses and not missing scores.\n"
            "- **Whether developers stopped reporting:** a share of 0% developer-reported means that the Hub holds no such score. "
            "It does not show that developers stopped reporting scores.\n"
            "- **Review:** the name matching and the labels of the sources were done by one reader and have not been reviewed by a second person.\n"
            "- **Small bars:** a bar with fewer than 5 models with scores is marked with an asterisk, and its shares are not stable.\n"
            f"- **Data age:** {stamp[0].lower() + stamp[1:]}"
        )
    with st.expander("**Values behind the chart** (scores per bar by kind of source, with the number of models)"):
        counts = segment_counts(df, ["accessible", "restricted", "combined"])
        table = counts.assign(Group=counts["group"].str.capitalize(), Kind=counts["kind"].map(KIND_NAME)).rename(
            columns={"year": "Release year", "scores": "Scores", "total": "Scores in bar", "share": "Share (%)",
                     "models": "Models"})
        st.dataframe(table[["Release year", "Group", "Kind", "Scores", "Scores in bar", "Share (%)", "Models"]],
                     hide_index=True, key="story2_4b_values",
                     column_config={"Share (%)": st.column_config.NumberColumn(format="%.1f")})
    from src.views_context import download_records

    if pinned and pinned["group"] in groups:
        rows = pick(df, pinned["year"], pinned["group"])
        rows = rows[rows["kind"] == pinned["kind"]]
        note = (f"The rows are the scores of the clicked segment ({KIND_NAME[pinned['kind']]}, "
                f"{GROUP_NAME[pinned['group']].split(' (')[0]}, released {pinned['year']}).")
    else:
        rows = df
        note = "No segment is clicked, so the rows are all scores in the chart. One row is one model, one benchmark and one kind of source."
    records = rows.assign(kind=rows["kind"].map(KIND_NAME), access_group=rows["access_group"].str.capitalize())[SCORE_COLUMNS]
    records = records.rename(columns={"model": "Model", "release_year": "Release year", "access_group": "Group",
                                      "benchmark": "Benchmark", "kind": "Kind of source", "source": "Source",
                                      "score_pct": "Score (%)"}).sort_values(["Release year", "Model", "Benchmark"])
    download_records(records, "story2_4b_records", "view4b_scores.csv", note)
    st.caption(f"Source: Epoch AI Benchmarking Hub, CC BY 4.0, epoch.ai/benchmarks. {stamp}")
    st.caption(
        "**How this view relates to View 3:** View 3 checks whether independent and publisher scores agree for one benchmark. "
        "This view shows how many of the scores behind the capability index come from each kind of source. "
        "It does not compare the two scores of one model, so the two views answer different parts of the same question."
    )


def render_view4b() -> None:
    st.subheader(
        "2. Who produced the benchmark scores behind the capability index?",
        anchor="view-2",
    )
    st.caption("Share of benchmark scores by who produced them, by release year and access group. "
               "An alternative way to check the data behind View 1.")
    _body()
