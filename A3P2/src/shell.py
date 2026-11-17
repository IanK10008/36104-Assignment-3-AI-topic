"""Page furniture copied word for word from the A3P1 app (app.py), so stories 1b and 2 read the same.

header(): title, question and persona box.  story(): the user-story line.  limitations(): the
"Data, methods and limitations" block.  limitations_1a() and limitations_3() are the blocks of Stories 1a and 3.
The rest is copied word for word.
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
    3: "As a group enterprise architect, I want to see how openly each developer builds its models and how often it "
       "appears in reported incidents, so that I can tell the committee what is known and unknown about the "
       "developers we would rely on.",
}
NOT_YET = " Grey text: not covered by this page, see \"What this chart cannot show\"."


# The help (?) icon of every widget label sits right after the label text, as it already does for the pills.
HELP_ICON_CSS = """<style>
label[data-testid="stWidgetLabel"] { justify-content: flex-start !important; }
label[data-testid="stWidgetLabel"] > div:has(> [data-testid="stTooltipIcon"]) {
    flex: 0 0 auto !important; width: auto !important; margin-left: 6px !important; justify-content: flex-start !important; }
div:has(> [data-testid="stMarkdownContainer"] + label > [data-testid="stTooltipIcon"]) {
    justify-content: flex-start !important; align-items: flex-start !important; gap: 6px !important; }
div:has(> label > [data-testid="stTooltipIcon"]) > [data-testid="stMarkdownContainer"] {
    flex: 0 0 auto !important; width: auto !important; }
</style>"""


def help_icons_left() -> None:
    st.html(HELP_ICON_CSS)


def standalone_page_config() -> None:
    """Wide layout when a page.py is run on its own. Inside app.py the layout is already set, so this does nothing."""
    try:
        st.set_page_config(page_title="Model Choice Explorer", layout="wide")
    except st.errors.StreamlitAPIException:
        pass
    help_icons_left()


def story(number: int, part: str) -> None:
    note = NOT_YET if "#9aa1a9" in STORIES[number] else ""
    st.markdown(f"<div style='font-size:0.95rem;color:#5b6470;margin:0.2rem 0 0.6rem 0'><b>User story {number}"
                f"{part}:</b> {STORIES[number]}<i>{note}</i></div>", unsafe_allow_html=True)


def header() -> None:
    help_icons_left()
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
            "- **Weights:** CRITIC (Diakoulaki, Mavrotas and Papayannakis, 1995), or custom (the sliders start at 5/5/5 = equal). **First-place share:** SMAA first-rank acceptability (Lahdelma and Salminen, 2001) over the 1,033 different weightings that the three 0 to 10 sliders can produce (settings with the same shares count once).\n"
            "- **Price frontier:** models that are stronger than every cheaper model.\n"
            "- **Licence class (Story 1b View 1):** Epoch AI's accessibility label, read as what it allows a bank to do. Five "
            "licences were also read by the group on 18 Oct 2026 and are shown beside Epoch's label.\n"
            "- **Restricted and accessible (Story 2 View 1):** restricted = a US developer and no downloadable weights. "
            "Accessible = open weights from any country, or a service from a developer outside the US. Each line is the "
            "best score released up to that date. Months behind = time since the restricted models first reached the "
            "best accessible score.\n"
            "- **Incident counts (Story 3 Views 1 and 2):** one count per incident and named company, from the AI Incident Database "
            "export of 12 Oct 2026 (notebook 10).")
    with st.expander("**Source choice and where the sources can mislead**"):
        st.markdown(
            "- **Epoch Capabilities Index (ECI):** a non-profit's joint fit of 62 benchmarks (Ho et al., 2025), used in the "
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


def limitations_3() -> None:
    """The "Data, methods and limitations" block of Story 3: only the sources, methods and limits that Views 1 and 2 use."""
    from src.views_story3 import SOURCES_3
    st.subheader("Data, methods and limitations", anchor="data-methods")
    files = {"fmti": "fmti_dec2025_scores_tidy.csv and fmti_companies.csv, View 1",
             "aiid": "aiid_model_incidents_by_developer.csv, View 2", "mit": "the same file, View 2",
             "epoch": "model_capability.csv, View 2"}
    with st.expander("**Sources**"):
        st.markdown("\n".join(f"- **{SOURCES_3[k][0]}**, {SOURCES_3[k][1]}. [{SOURCES_3[k][2]}]({SOURCES_3[k][2]}). {SOURCES_3[k][3]}. "
                              f"File in the app: {files[k]}." for k in ["fmti", "aiid", "mit", "epoch"]))
    with st.expander("**Methods**"):
        st.markdown(
            "- **FMTI scores (View 1):** 100 yes-or-no indicators for 13 companies, each for one flagship model assessed "
            "in May 2025.\n"
            "  - *Domains:* the scores file has no domain column, so each indicator takes its domain and subdomain from its "
            "position in the indicator file of the same edition.\n"
            "  - *Check:* all 100 indicators matched, with Upstream 34, Model 30 and Downstream 36 in 19 subdomains.\n"
            "- **Heatmap cell:** the indicators a company discloses, over the indicators in the subdomain.\n"
            "  - *Rows:* grouped by headquarters region as given in Table 1 of the FMTI paper and sorted A to Z inside each "
            "group, so the order is not a ranking.\n"
            "- **Model incidents (View 2):** the AI Incident Database export of 12 Oct 2026 holds 1,481 incidents since "
            "2020.\n"
            "  - *Developers:* 400 name one of the eleven, 378 in the developer field and 22 only in the implicated systems.\n"
            "  - *Counted:* 318 are model incidents.\n"
            "  - *Not counted:* 82, of which 61 are platform products, 5 are operations cases and 16 name a developer only "
            "as the place where a scam appeared.\n"
            "- **Dots and counts:** one dot per incident and named developer, which gives 377 dots for 318 incidents.\n"
            "  - *Monthly strip:* it counts each incident once.\n"
            "- **Incident type:** the MIT risk domain grouped into four types.\n"
            "  - *MIT:* set the domain for 252 incidents (circles).\n"
            "  - *Project group:* for the other 66 incidents only, which MIT has not classified yet (diamonds), the group "
            "assigned the closest MIT risk domain manually, with AI assistance in the reading of the incident title, the "
            "description and the developer, deployer and implicated-system fields.\n"
            "  - *Counts by type:* 137 wrong output or failure, 38 data and security, 78 misuse by others and 65 harm to "
            "users or society.\n"
            "- **Epoch model releases:** the release date of each model in the Epoch capability list, with its ECI score "
            "and 90% interval in the hover.\n"
            "  - *Period:* it starts in 2020, the same first year as the other incident charts of the app, with 2020 to "
            "2022 as the years before ChatGPT.")
    with st.expander("**Source choice and where the sources can mislead**"):
        st.markdown(
            "- **FMTI:** it measures what a company discloses and not what it does.\n"
            "  - *Evidence:* seven companies submitted their own reports (AI21 Labs, Amazon, Google, IBM, Meta, OpenAI and "
            "Writer). For the other six the researchers gathered public information, partly with an AI agent that they "
            "checked by hand, so a zero can mean the item was not found.\n"
            "  - *Scope:* one flagship model per company, and no later edition was found.\n"
            "- **AI Incident Database:** people submit and edit the incidents.\n"
            "  - *Consequence:* reports follow usage and English-language media, so a count is the number of reports and not "
            "a failure rate.\n"
            "- **MIT AI Risk Repository domains:** the classification lags behind new incidents.\n"
            "  - *Consequence:* 48 of the 76 incidents of 2026 had no domain, so the project group assigned their type "
            "manually and the page marks them as diamonds.\n"
            "- **Epoch:** the capability list holds 277 models, 229 of them from the eleven developers.")
    with st.expander("**What the data cannot show**"):
        st.markdown(
            "- **Openness of three developers:** FMTI does not score Z.ai, Moonshot and MiniMax.\n"
            "- **Safety of a developer's models:** an empty lane means few reports found and does not mean that no incident "
            "happened.\n"
            "- **Cause of incidents:** the triangles show release dates only, so the page does not test whether a release "
            "causes incidents.\n"
            "- **Severity and fault:** the data does not say how severe an incident was or who was at fault.\n"
            "- **Legal position:** the page gives no legal advice, no licence terms and no view on whether a developer may "
            "serve Hong Kong.")
    st.caption("Last data refresh: FMTI edition of December 2025. AI Incident Database export of 12 Oct 2026, latest "
               "incident 3 Oct 2026. Epoch file retrieved 17 Oct 2026, latest model release 7 Oct 2026.")


def _names(items: list[str]) -> str:
    """'A, B and C' for a list of model names."""
    if not items:
        return "no model"
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def limitations_1a(marked: list[str] | None = None) -> None:
    """The "Data, methods and limitations" block of Story 1a: only the sources, methods and limits that its two views use.
    Dates and figures come from the data in use (src/snapshot.py). `marked` lists the models that carry a licence mark."""
    from src import snapshot as snap
    marked = marked or []
    st.subheader("Data, methods and limitations", anchor="data-methods")
    keys = {"epoch": ("Capability", "model_capability.csv", "View 1 and View 2"),
            "litellm": ("List price", "model_price.csv", "View 1 and View 2"),
            "lmarena": ("Human preference", "lmarena_ratings.csv", "View 2 only")}
    notes = {"epoch": f"Retrieved {snap.get('epoch_retrieved')}, models released to {snap.get('epoch_last')}, CC BY 4.0",
             "litellm": f"Retrieved {snap.get('litellm_retrieved')}, current list prices, MIT licence",
             "lmarena": f"Snapshot published {snap.get('lmarena_published')}, retrieved {snap.get('lmarena_retrieved')}, CC BY 4.0"}
    with st.expander("**Sources**"):
        lines = [f"- **{label}:** {SOURCES[k][0]}, {SOURCES[k][1]}. [{SOURCES[k][2]}]({SOURCES[k][2]}). {notes[k]}. "
                 f"File in the app: `{file}`. Used in {used}." for k, (label, file, used) in keys.items()]
        lines.append(f"- **Licence marks:** the licence pages of {_names(marked)}, linked under the View 2 chart. The key "
                     "terms in the hover are the group's reading of those pages. Used in View 2 only.")
        st.markdown("\n".join(lines))
    with st.expander("**Methods**"):
        st.markdown(
            "- **Scope:** Epoch models released in the chosen window (2025 to 2026 by default), filtered by route and "
            "developer. View 1 keeps the models with a usable LiteLLM price. View 2 keeps the models found in all three "
            "sources.\n"
            "- **Name matching:** names are lower-cased, \"+\" becomes \"plus\" and punctuation is removed. A model is found "
            "in a source by the same name, or after removing a bracketed tag, a date or an effort tag such as \"(High)\". "
            "View 2 offers two rules, \"same name, or plus a tag\" and \"same name only\". When several Epoch versions share "
            "one stripped name, the version is unclear and the model is left out. LMArena entries found only via "
            "\"-max\" need a manual check and are left out.\n"
            "- **Price:** median output price in US dollars per million tokens over all LiteLLM chat rows of the model above "
            "$0. The minimum and maximum are in the downloads.\n"
            "- **Route:** Epoch AI's accessibility group. Open weights are downloadable (unrestricted, restricted use or "
            "non-commercial). Closed weights are API access, hosted access without an API or unreleased. Other or unknown "
            "is every remaining label.\n"
            "- **Price frontier (View 1):** a model joins the line only when its ECI is higher than that of every cheaper "
            "model. Models on the line are not ranked against each other.\n"
            "- **Percentile rank (View 2):** (rank - 1) / (n - 1) × 100 among the models shown, cheaper ranks higher.\n"
            "- **Weights (View 2):** CRITIC (Diakoulaki, Mavrotas and Papayannakis, 1995), or custom (the sliders start at "
            "5/5/5 = equal).\n"
            "- **Weighted score (View 2):** the sum of weight × percentile over the criteria in use, from 0 to 100.\n"
            "- **First-place share (View 2):** SMAA first-rank acceptability (Lahdelma and Salminen, 2001) over the 1,033 "
            "different weightings that the three 0 to 10 sliders can produce (settings with the same shares count once).\n"
            "- **Rounding:** charts and hovers show the LMArena rating as a whole number and the ECI to one decimal. Tables "
            "and CSV downloads keep the original values, except the computed weighted score and first-place share, which "
            "are shown to one decimal.")
    with st.expander("**Source choice and where the sources can mislead**"):
        st.markdown(
            "- **Epoch Capabilities Index (ECI):** a non-profit's joint fit of 62 benchmarks (Ho et al., 2025), used in the "
            "Stanford AI Index and the International AI Safety Report. It keeps each model's best setting, leans to maths "
            "and reasoning, covers smaller and non-US models less well, and its 90% intervals overlap for neighbours.\n"
            "- **LMArena:** millions of public pairwise votes (Chiang et al., ICML 2024), quoted by labs at launch. Voters "
            "are self-selected, longer, well-formatted answers win more often, and labs can test private variants "
            "(Singh et al., 2025, \"The Leaderboard Illusion\"). It agrees with capability at about " + snap.corr_text() + " at the default settings, so it is a "
            "cross-check more than an independent measure.\n"
            "- **LiteLLM:** a widely used open-source gateway (about 61k GitHub stars) whose price file is updated by "
            "community pull requests and carries no date. List price per token is not cost per task.\n"
            "- **Licence labels:** Epoch's label can differ from the licence text, so the marks in View 2 show both.\n"
            "- **Further notes:** `Research_Weighting_and_Source_Credibility.md` in the project folder lists the references.")
    with st.expander("**What the data cannot show**"):
        st.markdown(
            "- **Availability:** where each provider is offered is not measured. The restriction in Hong Kong is the "
            "premise of the story.\n"
            f"- **Licence terms:** only {len(marked)} models carry a licence mark, and the key terms are a reading of the linked "
            "pages. The full terms need checking by legal or procurement before any approval.\n"
            "- **Operations:** provider data handling, security review and hosting cost.\n"
            "- **Task fit:** usefulness for the bank's own documents, languages and workflows, and accuracy on banking "
            "tasks.\n"
            f"- **Price:** prices change often, so the page is a snapshot of {snap.get('litellm_retrieved')} and not a quote.\n"
            "- **Small differences:** ECI and LMArena intervals overlap for neighbouring models, so close scores and "
            "adjacent ranks are not a real difference.\n"
            "- **Decision:** the ranking supports a shortlist for the committee and is not an approval.")
    st.caption(f"Last data refresh: Epoch file retrieved {snap.get('epoch_retrieved')}, LiteLLM file retrieved "
               f"{snap.get('litellm_retrieved')}, LMArena snapshot published {snap.get('lmarena_published')}. "
               f"Latest model release date in the data: {snap.get('epoch_last')}.")
