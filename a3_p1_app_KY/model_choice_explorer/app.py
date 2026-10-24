from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src import analysis as an
from src import data
from src.views import SOURCES, render_view1, render_view2

QUESTION = ("In regions where leading closed US models are restricted, which accessible AI model gives an "
            "organisation the most measured capability for its cost and self-hosting feasibility?")

st.set_page_config(page_title="Model Choice Explorer", layout="wide")


@st.cache_data(show_spinner=False)
def load_models():
    return data.load()


models = load_models()


@st.cache_data(show_spinner=False)
def load_arena():
    """The LMArena overall leaderboard file, used to list every setting of a model in the detail panel."""
    return pd.read_csv(Path(__file__).resolve().parent / "data" / "source" / "lmarena_overall.csv")


arena_all = load_arena()

st.title("Model Choice Explorer: capability for the cost, where closed US models are restricted")
st.markdown(f"**Question:** {QUESTION}")

with st.container(border=True):
    st.markdown(
        "**Persona:** group enterprise architect at an Asia-Pacific bank or insurer with operations in Hong Kong and "
        "other markets.\n\n"
        "**Scenario:** the risk committee has asked for an approved list of AI models for staff and internal tools. "
        "The leading closed US models are not offered in Hong Kong. The committee wants an interim list within one to "
        "two weeks. The architect must choose between API services from outside the US and self-hosted open weights, "
        "and the committee will ask what capability is given up, what each route costs, and which models the bank "
        "may run itself.\n\n"
        "**Task:** produce an interim approved list. For each candidate model, say which route it uses (API or "
        "self-hosted), what its licence allows, how much capability it gives, and what it costs.\n\n"
        "**Decision this page serves:** which accessible models go on the approved list, by route, with capability "
        "set against price.\n\n"
        "**Constraints (assumed):**\n\n"
        "- **Time:** one to two weeks, so the list is interim and each version is kept with its date and sources.\n"
        "- **Reasons:** the committee needs the reasons for each choice, not a single score.\n"
        "- **Source of values:** capability and licence class come from files.\n"
        "- **Data control:** a proxy only, because availability by place is not measured.\n"
        "- **Not covered:** regulator rules, the bank's own tasks, hosting cost and security review.")

all_three_recent = models.loc[(models["release_year"] >= 2025)
                              & models["match_status"].isin([data.ALL_SAME, data.ALL_TAG])]
developers = sorted(an.developer_name(models).unique())


def _saved(key: str, options: list, default):
    """Value kept in the browser session, or the default if it is missing or no longer one of the options
    (for example, left over from an older version of the page)."""
    value = st.session_state.get(key, default)
    if value not in options:
        value = default
        st.session_state[key] = default
    return value


def window_text(name: str) -> str:
    """Window name, with the first date written out for the rolling windows (they follow the data refresh)."""
    spec = an.WINDOWS[name]
    if isinstance(spec, tuple):
        start = an.window_start(models, spec)
        return f"{name}, from {start.day} {start:%b %Y}"
    return name


def controls_block(prefix: str, settings=None) -> tuple:
    """Counts, reading guide and the controls of one view. View 1 and View 2 each have their own copy
    (keys start with ``prefix``), so each can be set differently. Returns the selected data for that view."""
    if not prefix:  # shown once, in View 1, and not repeated in View 2
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Models with an Epoch capability score", f"{len(models)}",
                  help="Released 24 Feb 2023 to 7 Oct 2026, Epoch file retrieved 17 Oct 2026")
        m2.metric("... with a LiteLLM list price", f"{models['output_price_usd_per_million'].notna().sum()}")
        m3.metric("... with an LMArena rating", f"{models['arena_rating'].notna().sum()}")
        m4.metric("In all three sources, released 2025-2026", f"{len(all_three_recent)}",
                  help="Same name, or same name plus a tag such as (High)")
        st.info(
            "**How to read this page.** Three public sources measure different things: **capability** (Epoch Capabilities "
            "Index, benchmark-based), **human preference** (LMArena votes) and **list price** (LiteLLM, US dollars per "
            "million output tokens). View 1 sets capability against price and shows the price frontier. View 2 combines "
            "the three into one weighted ranking and shows the reasons behind each model's rank. Each view has its own "
            "controls, so the two can be set differently. Where intervals overlap, read models as roughly equal, not "
            "better or worse.")
    if prefix:
        settings = settings if settings is not None else st.container()
    else:
        settings = st.container()
        with settings:
            st.markdown("#### Controls for this view")
    k = lambda name: prefix + name
    year = an.WINDOWS[_saved(k("window"), list(an.WINDOWS), list(an.WINDOWS)[0])]
    route = an.ROUTE_CHOICES[_saved(k("route"), list(an.ROUTE_CHOICES), list(an.ROUTE_CHOICES)[0])]
    _saved(k("match_rule"), list(an.MATCH_RULES), list(an.MATCH_RULES)[0])
    st.session_state.setdefault(k("developers"), developers)
    devs = [d for d in st.session_state[k("developers")] if d in developers]
    st.session_state[k("developers")] = devs
    base = an.filter_models(models, year, route, devs)
    rule_counts = {n: len(an.three_source(base, v)) for n, v in an.MATCH_RULES.items()}
    window_counts = {n: len(an.filter_models(models, y, route, devs)) for n, y in an.WINDOWS.items()}
    route_counts = {n: len(an.filter_models(models, year, r, devs)) for n, r in an.ROUTE_CHOICES.items()}

    with settings:
        c1, c2, c3 = st.columns([1, 1.2, 1.6])
        window_label = c1.selectbox("Release window", list(an.WINDOWS), key=k("window"),
                                    format_func=lambda x: window_text(x) + f" ({window_counts[x]} models)")
        route_label = c2.selectbox("Route", list(an.ROUTE_CHOICES), key=k("route"),
                                   format_func=lambda x: f"{x} ({route_counts[x]} models)")
        rule_label = c3.selectbox("Which name matches count as \"in all three sources\"", list(an.MATCH_RULES),
                                  key=k("match_rule"), format_func=lambda x: f"{rule_counts[x]} models: {x}",
                                  help="Same name: identical in all three files. Plus a tag: LMArena adds a setting such "
                                       "as \"(High)\" to the same model. Unclear versions and \"-max\" entries are "
                                       "always left out. The number in each option is how many models it gives for the "
                                       "current window, route and developers.")
        chosen = st.multiselect("Developers", developers, key=k("developers"),
                                help="Remove developers to compare a subset. An empty selection shows a message.")

        window = an.filter_models(models, an.WINDOWS[window_label], an.ROUTE_CHOICES[route_label], chosen)
        points = an.price_points(window)
        three = an.three_source(window, an.MATCH_RULES[rule_label])
        pct = an.percentiles(three) if not three.empty else three
        st.caption(f"Selected: {len(window)} Epoch models · {len(points)} with a usable price · "
                   f"{len(three)} in all three sources")

    # The weights are drawn inside the view; the ranking here reads them from the saved state.
    if not three.empty:
        criteria = list(an.CRITERIA)
        if prefix:  # View 2 can leave a criterion out of its ranking
            picked = st.session_state.get(k("criteria"), list(an.CRITERIA))
            criteria = [c for c in an.CRITERIA if c in picked] or list(an.CRITERIA)
        if st.session_state.get(k("weight_method"), "CRITIC (data-driven)").startswith("CRITIC"):
            w = an.critic_weights(pct, criteria)
        else:
            w = an.normalise({c: st.session_state.get(k(f"w_{c}"), 5) if c in criteria else 0 for c in an.CRITERIA})
        ranked = an.score(three, pct, w)
        tags = [an.effort_tag(m, l) for m, l in zip(ranked["model"], ranked["lmarena_match"])]
        ranked["label"] = [f"{m} ({t})" if t else m for m, t in zip(ranked["model"], tags)]
        best = ranked.iloc[0]
        if not prefix:  # View 2 shows the ranking itself, so the one-line answer is only needed in View 1
          st.success(
              f"**Answer under the current settings:** {best['model']} ranks first among {len(ranked)} models in all "
              f"three sources ({best['route'].lower()}): {best['eci']:.1f} capability points, LMArena "
              f"{best['arena_rating']:.0f}, ${best['output_price_usd_per_million']:,.2f} per million output tokens. "
              "Its rank depends on how much price matters: see \"Wins under any weighting\" in View 2.")
    else:
        ranked = three
    return window_label, rule_label, points, three, pct, ranked


# Keep every widget setting when a view is closed and opened again (Streamlit drops state of unrendered widgets).
st.session_state.setdefault("show_view1", True)
st.session_state.setdefault("show_view2", True)
for _key in list(st.session_state):
    if not _key.endswith(("_download", "_table", "_chart", "_values")):
        st.session_state[_key] = st.session_state[_key]

with st.container(key="cost_capability", border=True):
    head1, tog1 = st.columns([5, 1], vertical_alignment="center")
    head1.subheader("1. Which models give the most capability for the price?", anchor="view-1")
    open1 = tog1.toggle("Show view", key="show_view1")

    @st.fragment  # a click inside View 1 re-runs only View 1
    def view_one():
        w_label, r_label, points, three, pct, ranked = controls_block("")
        render_view1(models, points, ranked, pct if not three.empty else three, w_label)

    if open1:
        view_one()

with st.container(key="ranked_options", border=True):
    head2, tog2 = st.columns([5, 1], vertical_alignment="center")
    head2.subheader("2. Which models rank highest once capability, preference and price are weighed together?",
                    anchor="view-2")
    open2 = tog2.toggle("Show view", key="show_view2")

    @st.fragment  # a click inside View 2 re-runs only View 2, so the chart updates faster
    def view_two():
        summary_slot = st.container()
        advanced = st.expander("Advanced settings: release window, route, name matching, developers, weights")
        w_label2, r_label2, points2, three2, pct2, ranked2 = controls_block("v2_", advanced)
        render_view2(ranked2, pct2, r_label2, arena_all, list(an.CRITERIA), advanced, summary_slot, points=points2)

    if open2:
        view_two()

st.subheader("Data, methods and limitations", anchor="data-methods")
with st.expander("**Sources**"):
    st.markdown("\n".join(f"- **{t}**, {p}. [{u}]({u}). {n}." for t, p, u, n in SOURCES.values()))
with st.expander("**Methods**"):
    st.markdown(
        "- **Matching by name** (`src/data.py`): names are lower-cased, \"+\" becomes \"plus\" and punctuation is "
        "removed. A model is found in a source by the same name, or after removing a bracketed tag, a date or an "
        "effort tag such as \"(High)\". When several Epoch versions share one stripped name, the version is unclear "
        "and the model is left out. LMArena entries found only via \"-max\" need a manual check and are left out.\n"
        "- **Price:** median, minimum and maximum of the output price over all LiteLLM chat rows of the model above "
        "$0.\n"
        "- **Percentile rank:** (rank - 1) / (n - 1) × 100 among the models shown, cheaper ranks higher.\n"
        "- **Weights:** CRITIC (Diakoulaki, Mavrotas and Papayannakis, 1995), or custom (the sliders start at 5/5/5 = equal). **Wins under any "
        "weighting:** SMAA first-rank acceptability (Lahdelma and Salminen, 2001) over the 1,033 different weightings that the three 0 to 10 sliders can produce (settings with the same shares count once).\n"
        "- **Price frontier:** models that are stronger than every cheaper model.")
with st.expander("**Source choice and where the sources can mislead**"):
    st.markdown(
        "- **Epoch Capabilities Index:** a non-profit's joint fit of 62 benchmarks (Ho et al., 2025), used in the "
        "Stanford AI Index and the International AI Safety Report. It keeps each model's best setting, leans to maths "
        "and reasoning, covers smaller and non-US models less well, and its 90% intervals overlap for neighbours.\n"
        "- **LMArena:** millions of public pairwise votes (Chiang et al., ICML 2024), quoted by labs at launch. Voters "
        "are self-selected, longer, well-formatted answers win more often, labs can test private variants "
        "(Singh et al., 2025, \"The Leaderboard Illusion\"). It agrees with capability at about 0.85, so it is used "
        "mainly as a cross-check.\n"
        "- **LiteLLM:** a widely used open-source gateway (about 61k GitHub stars) whose price file is updated by "
        "community pull requests and carries no date. List price per token is not cost per task.\n"
        "- Full notes with references: `Research_Weighting_and_Source_Credibility.md` in the project folder.")
with st.expander("**What the data cannot show**"):
    st.markdown(
        "- Where each provider is offered: the restriction in Hong Kong is the premise of the story, not measured.\n"
        "- Licence terms beyond \"open weights\", provider data handling, security review and hosting cost.\n"
        "- Usefulness for the bank's own documents, languages and workflows.\n"
        "- Prices change often, this page is a snapshot of 17 Oct 2026 and is not a quote.")
st.caption("Last data refresh: Epoch and LiteLLM files retrieved 17 Oct 2026. LMArena snapshot published "
           "15 Oct 2026. Latest model release date in the data: 7 Oct 2026.")
