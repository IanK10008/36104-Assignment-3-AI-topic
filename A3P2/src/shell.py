"""Page furniture copied word for word from the A3P1 app (app.py), so stories 1b and 2 read the same.

header(): title, question and persona box.  story(): the user-story line.  limitations(): the
"Data, methods and limitations" block.  Nothing here is new text.
"""
from __future__ import annotations

import streamlit as st

from src.views import SOURCES

QUESTION = ("In regions where leading closed US models are restricted, which accessible AI model gives an "
            "organisation the most measured capability for its cost and self-hosting feasibility?")

GREY = "<span style='color:#9aa1a9'>{}</span>"
STORIES = {
    1: "As a group enterprise architect, I want to pick a route (API or self-hosted) and shortlist the accessible "
       "models whose licence fits it, ranked with capability set against price, so that I can build an interim "
       "approved list the risk committee will accept.",
    2: "As a group enterprise architect, I want to measure how far the best accessible model trails the best model "
       "overall " + GREY.format("and check whether independent benchmarks agree with developer claims") + ", so "
       "that I can judge whether waiting for US access is worth it.",
    3: "As a group enterprise architect, I want to see " + GREY.format("how openly each developer builds its models "
       "and") + " how often it appears in reported incidents, so that I can tell the committee what is known and "
       "unknown about the developers we would rely on.",
}
NOT_YET = " Grey text: not covered by this page, see \"What this chart cannot show\"."


def standalone_page_config() -> None:
    """Wide layout when a page.py is run on its own. Inside app.py the layout is already set, so this does nothing."""
    try:
        st.set_page_config(page_title="Model Choice Explorer", layout="wide")
    except st.errors.StreamlitAPIException:
        pass


def story(number: int, part: str) -> None:
    note = NOT_YET if "#9aa1a9" in STORIES[number] else ""
    st.markdown(f"<div style='font-size:0.95rem;color:#5b6470;margin:0.2rem 0 0.6rem 0'><b>User story {number}"
                f"{part}:</b> {STORIES[number]}<i>{note}</i></div>", unsafe_allow_html=True)


def header() -> None:
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



def limitations() -> None:
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
            "- **Price frontier:** models that are stronger than every cheaper model.\n"
            "- **Licence class (View 3):** Epoch AI's accessibility label, read as what it allows a bank to do. Five "
            "licences were also read by the group on 18 Oct 2026 and are shown beside Epoch's label.\n"
            "- **Restricted and accessible (View 4):** restricted = a US developer and no downloadable weights. "
            "Accessible = open weights from any country, or a service from a developer outside the US. Each line is the "
            "best score released up to that date. Months behind = time since the restricted models first reached the "
            "best accessible score.\n"
            "- **Incident counts (View 5):** one count per incident and named company, from the AI Incident Database "
            "export of 12 Oct 2026 (notebook 10).")
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
            "- Prices change often, this page is a snapshot of 17 Oct 2026 and is not a quote.\n"
            "- When US access returns, or whether the capability gap keeps shrinking.\n"
            "- How safe a developer's models are: incident reports follow usage and English-language media.\n"
            "- Legal advice: licence classes are Epoch's labels and the group's own reading.")
    st.caption("Last data refresh: Epoch and LiteLLM files retrieved 17 Oct 2026. LMArena snapshot published "
               "15 Oct 2026. Licence pages read 18 Oct 2026. AI Incident Database export of 12 Oct 2026. Latest model "
               "release date in the data: 7 Oct 2026, latest incident: 3 Oct 2026.")
