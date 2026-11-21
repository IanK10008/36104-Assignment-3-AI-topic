"""Page furniture copied word for word from the A3P1 app (app.py), so stories 1b and 2 read the same.

header(): title, question and persona box.  story(): the user-story line.  limitations(): the
"Data, methods and limitations" block.  limitations_1a() and limitations_3() are the blocks of Stories 1a and 3.
The rest is copied word for word.
"""
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import pandas as pd
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
       "overall and check whether independent benchmarks agree with developer claims, so "
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
div[data-testid="stElementContainer"]:has(div[data-testid="stPlotlyChart"]) {
    margin-left: auto !important; margin-right: auto !important; }
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
    """The user story as a bordered block with the three parts on their own lines, so that it reads as the aim of the page."""
    note = NOT_YET if "#9aa1a9" in STORIES[number] else ""
    text = STORIES[number]
    who, rest = text.split(", I want ", 1)
    want, so = rest.split(", so that ", 1)
    st.markdown(
        "<div style='border-left:5px solid #0072B2;background:#f3f7fb;border-radius:4px;padding:0.8rem 1.1rem;"
        "margin:0.4rem 0 1rem 0;font-size:1.08rem;line-height:1.55;color:#1f2328'>"
        f"<div style='font-size:0.85rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:#0072B2;"
        f"margin-bottom:0.3rem'>User story {number}{part}</div>"
        f"<div><b>{who.replace('As a ', 'As a ', 1)},</b></div>"
        f"<div><b>I want</b> {want},</div>"
        f"<div><b>so that</b> {so}<i>{note}</i></div></div>", unsafe_allow_html=True)


EPOCH_FILE = Path(__file__).resolve().parent.parent / "stories" / "1b_licence_route" / "data" / "model_capability.csv"


@st.cache_data
def dataset_fact() -> str:
    """One fact about the whole Epoch file, counted from the data each time the file is read."""
    table = pd.read_csv(EPOCH_FILE)
    dates = pd.to_datetime(table["release_date"], errors="coerce")
    access = table["access_class_epoch"].value_counts()
    return (f"Epoch scores {table['model'].nunique()} models released between {dates.min():%B %Y} and "
            f"{dates.max():%B %Y}. Of these, {access.get('open_weights', 0)} are open weights and "
            f"{access.get('api_only', 0)} are API only. The pages also read the LiteLLM price file and the LMArena "
            f"leaderboard (Story 1a), the licence readings (Story 1b), the Epoch Benchmarking Hub (Story 2), and the "
            f"AI Incident Database and the Foundation Model Transparency Index (Story 3).")


def header() -> None:
    help_icons_left()
    st.title("Model Choice Explorer: capability for the cost, where closed US models are restricted")
    st.markdown(f"**Question:** {QUESTION}")
    st.markdown(f"**What the data shows:** {dataset_fact()}")

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
            "**Constraints:**\n\n"
            "- **Time:** one to two weeks, so the list is interim and each version is kept with its date and sources.\n"
            "- **Reasons:** the committee needs the reasons for each choice, not a single score.\n"
            "- **Source of values:** capability and licence class come from files.\n"
            "- **Data control:** a proxy only, because availability by place is not measured.\n"
            "- **Not covered:** regulator rules, the bank's own tasks, hosting cost and security review.")



# References in the style of the APA 7th edition (APA guide, January 2025). Dates in a reference are written as
# (Year, Month Day). A data set that changes carries the day it was retrieved.
_MONTH_DAY = re.compile(r"(\d{1,2}) ([A-Z][a-z]{2}) (\d{4})")


def _apa_day(text) -> str:
    """'20 Nov 2026' -> 'November 20, 2026'. Empty when the text holds no day."""
    match = _MONTH_DAY.search(str(text))
    if not match:
        return ""
    try:
        day = datetime.strptime(" ".join(match.groups()), "%d %b %Y")
    except ValueError:
        return ""
    return f"{day:%B} {day.day}, {day.year}"


def _apa_year_day(text, year: str) -> str:
    """'19 Nov 2026' -> '2026, November 19'. The year alone when the text holds no day."""
    day = _apa_day(text)
    return f"{day.rsplit(',', 1)[1].strip()}, {day.rsplit(',', 1)[0]}" if day else year


def _retrieved_from(text) -> str:
    day = _apa_day(text)
    return f"Retrieved {day}, from " if day else ""


def ref_epoch(retrieved, letter: str = "") -> str:
    return (f"Epoch AI. (2026{letter}). *Epoch Capabilities Index (ECI)* [Data set]. "
            f"{_retrieved_from(retrieved)}https://epoch.ai/benchmarks/eci")


def ref_hub(retrieved, letter: str = "") -> str:
    return (f"Epoch AI. (2026{letter}). *Epoch AI Benchmarking Hub: Benchmark data* [Data set]. "
            f"{_retrieved_from(retrieved)}https://epoch.ai/data/benchmark_data.zip")


def ref_litellm(retrieved) -> str:
    return (f"BerriAI. (2026). *LiteLLM: Model prices and context window* [Data set]. GitHub. "
            f"{_retrieved_from(retrieved)}https://github.com/BerriAI/litellm")


def ref_lmarena(published) -> str:
    return (f"LMArena. ({_apa_year_day(published, '2026')}). *Leaderboard dataset: Text, overall category* [Data set]. "
            "Hugging Face. https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset")


def ref_aiid(snapshot) -> str:
    return (f"Responsible AI Collaborative. ({_apa_year_day(snapshot, '2026')}). *AI Incident Database: Weekly snapshot* "
            "[Data set]. https://incidentdatabase.ai/research/snapshots/")


LICENCE_PAGES_READ = "18 Oct 2026"   # day the group read the five licence pages (licence_basis in model_capability.csv)
REF = {
    "fmti": "Stanford Center for Research on Foundation Models. (2025). *Foundation Model Transparency Index, December "
            "2025* [Data set]. https://crfm.stanford.edu/fmti/December-2025",
    "mit": "MIT AI Risk Repository. (n.d.). *The AI Risk Repository: Risk domains and subdomains*. https://airisk.mit.edu/",
    "gpqa": "Lee, J., & Edelman, Y. (2025, September 19). *AI developers accurately report GPQA Diamond scores for recent "
            "models*. Epoch AI. https://epoch.ai/data-insights/self-reported-gpqa",
    "ho": "Ho, A., Denain, J.-S., Atanasov, D., Albanie, S., & Shah, R. (2025). *A Rosetta Stone for AI benchmarks* "
          "[Preprint]. arXiv. https://arxiv.org/abs/2512.00193",
    "chiang": "Chiang, W.-L., Zheng, L., Sheng, Y., Angelopoulos, A. N., Li, T., Li, D., Zhu, B., Zhang, H., Jordan, "
              "M. I., Gonzalez, J. E., & Stoica, I. (2024). Chatbot Arena: An open platform for evaluating LLMs by "
              "human preference. In *Proceedings of the 41st International Conference on Machine Learning* (Vol. 235, "
              "pp. 8359\u20138388). PMLR. https://proceedings.mlr.press/v235/chiang24b.html",
    "singh": "Singh, S., Nan, Y., Wang, A., D'souza, D., Kapoor, S., \u00dcst\u00fcn, A., Koyejo, S., Deng, Y., Longpre, S., "
             "Smith, N. A., Ermis, B., Fadaee, M., & Hooker, S. (2025). *The leaderboard illusion* [Preprint]. arXiv. "
             "https://doi.org/10.48550/arXiv.2504.20879",
    "diakoulaki": "Diakoulaki, D., Mavrotas, G., & Papayannakis, L. (1995). Determining objective weights in multiple "
                  "criteria problems: The CRITIC method. *Computers & Operations Research, 22*(7), 763\u2013770. "
                  "https://doi.org/10.1016/0305-0548(94)00059-H",
    "lahdelma": "Lahdelma, R., & Salminen, P. (2001). SMAA-2: Stochastic multicriteria acceptability analysis for group "
                "decision making. *Operations Research, 49*(3), 444\u2013454. "
                "https://doi.org/10.1287/opre.49.3.444.11220",
    "cottier": "Cottier, B., You, J., Martemianova, N., & Owen, D. (2024, November 4). *How far behind are open "
               "models?* Epoch AI. https://epoch.ai/blog/open-models-report",
    "moonshot_hf": "Moonshot AI. (n.d.-a). *Kimi-K3* [Model card]. Hugging Face. " + _retrieved_from(LICENCE_PAGES_READ)
                   + "https://huggingface.co/moonshotai/Kimi-K3",
    "moonshot_gh": "Moonshot AI. (n.d.-b). *Kimi-K3* [Computer software]. GitHub. " + _retrieved_from(LICENCE_PAGES_READ)
                   + "https://github.com/MoonshotAI/Kimi-K3",
    "deepseek": "DeepSeek-AI. (n.d.). *DeepSeek-V4-Pro* [Model card]. Hugging Face. " + _retrieved_from(LICENCE_PAGES_READ)
                + "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro",
    "zai": "Z.ai. (n.d.). *GLM-5* [Model card]. Hugging Face. " + _retrieved_from(LICENCE_PAGES_READ)
           + "https://huggingface.co/zai-org/GLM-5",
    "minimax": "MiniMax. (n.d.). *MiniMax-M3* [Model card]. Hugging Face. " + _retrieved_from(LICENCE_PAGES_READ)
               + "https://huggingface.co/MiniMaxAI/MiniMax-M3",
    "qwen": "Qwen. (n.d.). *Qwen* [Organization profile]. Hugging Face. " + _retrieved_from(LICENCE_PAGES_READ)
            + "https://huggingface.co/Qwen",
    "wan": "Wan, A., Klyman, K., Kapoor, S., Maslej, N., Longpre, S., Xiong, B., Liang, P., & Bommasani, R. (2025). "
           "*The 2025 Foundation Model Transparency Index* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2512.10169",
}


def _references_block(entries: list[str]) -> None:
    """The reference list of a story, in alphabetical order, open by default."""
    ordered = sorted(entries, key=lambda text: text.replace("*", "").lower())
    with st.expander("**References**", expanded=True):
        st.markdown("\n\n".join(ordered))


def _sources_block(lines: list[str]) -> None:
    """The sources of a story, open by default so that they are visible without a click."""
    with st.expander("**Sources**", expanded=True):
        st.markdown("\n".join(lines))


def limitations_1b() -> None:
    """The "Data, methods and limitations" block of Story 1b: only the sources, methods and limits of its three views."""
    from src import snapshot as snap
    ep = snap.story_facts("1b_licence_route")
    st.subheader("Data, methods and limitations", anchor="data-methods")
    _sources_block([
        f"- **Capability, release date, developer, country and accessibility label:** Epoch AI (2026). "
        f"File retrieved {ep['epoch_retrieved']}, models "
        f"released 24 Feb 2023 to {ep['epoch_last']}, CC BY (version not stated). File in the app: `model_capability.csv`. "
        "Used in Views 1 and 2. View 3 lists the models of this file that Epoch labels restricted use, non-commercial or "
        "unknown, and six models of earlier Epoch files that this file no longer holds.",
        "- **Licence terms of 51 models:** the licence files and pages of the models that Epoch labels restricted use, "
        "non-commercial or unknown (released 2024 to 2026), read on 18 Nov 2026 by Claude. File in the app: "
        "`licence_terms.json`. The link of each model is in its full note. Used in View 3.",
        "- **Licence pages of five models:** Kimi K3 (Moonshot AI, n.d.-a, n.d.-b), DeepSeek V4 Pro 0813 (DeepSeek-AI, "
        "n.d.), Qwen 3.8 27B (Qwen, n.d.), MiniMax-M3 (MiniMax, n.d.) and GLM-5 (Z.ai, n.d.), read on 18 Oct 2026. "
        "Used in the table \"Licences read by the group\" of View 1."])
    _references_block([ref_epoch(ep["epoch_retrieved"]), REF["ho"], REF["cottier"], REF["moonshot_hf"],
                       REF["moonshot_gh"], REF["deepseek"], REF["zai"], REF["minimax"], REF["qwen"]])
    with st.expander("**Methods**"):
        st.markdown(
            "- **Licence class (Views 1 and 2):** Epoch's accessibility label, read as what it allows a bank to do. "
            "Restricted use is a licence that limits users or purposes. Non-commercial is a licence that does not allow "
            "commercial use, and a missing licence also counts as non-commercial (Cottier et al., 2024).\n"
            "- **View 1:** one dot per model. The best model of each class is labelled with its 90% interval.\n"
            "- **View 2:** the open-weight models of each release year, as a share of the year's total by licence class. "
            f"2026 is a part year, to {ep['epoch_last'].rsplit(' ', 1)[0]}.\n"
            "- **View 3:** one row per model and one column per licence term. Each cell holds the text of the term and a "
            "colour for its state. The evidence level says whether the licence was read in full, in part or assumed.\n"
            "- **Check at every refresh:** for each new open-weight model and each model that Epoch labels restricted "
            "use, non-commercial or unknown, the licence file is opened and read before the label is used.")
    with st.expander("**Source choice and where the sources can mislead**"):
        st.markdown(
            "- **Epoch Capabilities Index (ECI):** a non-profit's joint fit of benchmark results (method: Ho et al., 2025; the Hub file of 20 Nov 2026 marks 58 benchmarks as part of it). It keeps "
            "each model's best setting, leans to maths and reasoning, covers smaller and non-US models less well, and its "
            "90% intervals overlap for neighbours.\n"
            "- **Epoch's licence label:** it can differ from the licence text. Epoch labels Kimi K3 non-commercial, while "
            "its licence allows commercial use above a revenue condition. Views 1 and 2 keep Epoch's label and View 3 "
            "shows the group's reading.\n"
            "- **Licence readings:** 42 models were read in full, 5 in part, 3 assumed and 1 is not a licence case. They are "
            "AI work and not legal advice.")
    with st.expander("**What the data cannot show**"):
        st.markdown(
            "- **Legal reading:** the classes are Epoch's labels and the readings are not legal advice. Legal or "
            "procurement must confirm before any approval.\n"
            "- **Models not read:** models that Epoch labels unrestricted were not read in View 3, and in Views 1 and 2 "
            "only five licences were read.\n"
            "- **Quality and use:** a year with more unrestricted models does not mean better models, and the page does "
            "not measure performance on the bank's own documents.\n"
            "- **Operations:** hardware, running cost, provider data handling and security review are not measured.\n"
            "- **Availability:** where each model may be used is not measured. The restriction in Hong Kong is the premise "
            "of the story.")
    st.caption(f"Last data refresh: Epoch Capabilities Index file retrieved {ep['epoch_retrieved']} (latest model release "
               f"{ep['epoch_last']}). Licence terms read 18 Nov 2026. Licence pages of five models read 18 Oct 2026.")


def limitations_2() -> None:
    """The "Data, methods and limitations" block of Story 2: only the sources, methods and limits of its three views."""
    from src import snapshot as snap
    ep, hub = snap.story_facts("2_gap_to_us_models"), snap.hub_facts()
    st.subheader("Data, methods and limitations", anchor="data-methods")
    _sources_block([
        f"- **Capability, release date, developer, country and accessibility label:** Epoch AI (2026b). "
        f"File retrieved {ep['epoch_retrieved']}, models "
        f"released 24 Feb 2023 to {ep['epoch_last']}, CC BY (version not stated). File in the app: `model_capability.csv`. "
        "Used in Views 1 to 3.",
        "- **Benchmark scores and who produced them:** Epoch AI (2026a). File benchmark_data.zip, CC BY 4.0, "
        f"downloaded {hub['downloaded']}. {hub['scores']} scores of {hub['models']} models that match a model of the "
        f"Epoch capability file, on {hub['benchmarks']} benchmarks. File in the app: "
        "`hub_scores_by_model.csv`. Used in View 2.",
        "- **Reported and independent GPQA Diamond scores:** Lee and Edelman (2025). Scores of "
        "eight models transcribed by the group on 14 Nov 2026. File in the app: `gpqa_reported_vs_epoch.csv`. Used in "
        "View 3."])
    _references_block([ref_hub(hub["downloaded"], "a"), ref_epoch(ep["epoch_retrieved"], "b"), REF["gpqa"], REF["ho"]])
    with st.expander("**Methods**"):
        st.markdown(
            "- **Restricted and accessible (View 1):** restricted means a US developer and no downloadable weights. "
            "Accessible means open weights from any country, or a service from a developer outside the US. This is a "
            "rule and not a measurement.\n"
            "- **Step lines (View 1):** each line is the best score released up to that date. Months behind is the time "
            "since the restricted models first reached the best accessible score.\n"
            "- **One score (View 2):** one model, one benchmark and one kind of source. Versions of a model are merged "
            "and the highest score is kept. The share is the scores of one kind over all scores in the bar. The kind of "
            "source (Epoch AI, third party or developer-reported) follows a label that the group set for each of the 81 "
            "named sources (58 of them appear in the scores).\n"
            "- **Difference (View 3):** the developer-reported score minus Epoch's independent score, in percentage "
            "points. The grey band is 1.645 times Epoch's reported standard error. Access groups follow the rule of "
            "View 1.\n"
            "- **Check at every refresh:** when the data is downloaded again, the group reads the licence of each new "
            "open-weight model and of each model that Epoch labels restricted use, non-commercial or unknown (see docs.md).")
    with st.expander("**Source choice and where the sources can mislead**"):
        st.markdown(
            "- **Epoch Capabilities Index (ECI):** a non-profit's joint fit of benchmark results (method: Ho et al., 2025; the Hub file of 20 Nov 2026 marks 58 benchmarks as part of it). It keeps "
            "each model's best setting, leans to maths and reasoning, covers smaller and non-US models less well, and its "
            "90% intervals overlap for neighbours.\n"
            "- **Benchmarking Hub labels:** the labels and the name matching of View 2 were made by one reader.\n"
            "- **Epoch's comparison (View 3):** eight models chosen by Epoch, of which seven are plotted (Mistral Large is "
            "left out), one benchmark, published on 19 Sep 2025.")
    with st.expander("**What the data cannot show**"):
        st.markdown(
            "- **The future:** when US access returns, or whether the gap keeps shrinking.\n"
            "- **Excluded models:** 16 older models with no open weights and no stated country belong to neither side.\n"
            "- **Small groups:** four restricted and three accessible models in View 3 are too few to test a difference.\n"
            "- **Other benchmarks:** agreement on GPQA Diamond does not carry over to other benchmarks.\n"
            "- **Different definitions:** Epoch's own open-weight lag figures use other groups, so they cannot be compared "
            "with the gap here without saying so.\n"
            "- **Availability:** where each model may be used is not measured. The restriction in Hong Kong is the premise "
            "of the story.")
    st.caption(f"Last data refresh: Epoch Capabilities Index file retrieved {ep['epoch_retrieved']} (latest model release "
               f"{ep['epoch_last']}). Epoch Benchmarking Hub ZIP downloaded {hub['downloaded']}. GPQA scores transcribed "
               "14 Nov 2026 from an article of 19 Sep 2025.")


def limitations_3() -> None:
    """The "Data, methods and limitations" block of Story 3: only the sources, methods and limits that Views 1 and 2 use."""
    from src import snapshot as snap
    from src import views_story3 as v3
    from src.views_story3 import SOURCES_3
    ep = snap.story_facts("3_reported_incidents")
    st.subheader("Data, methods and limitations", anchor="data-methods")
    files = {"fmti": "fmti_dec2025_scores_tidy.csv and fmti_companies.csv, View 1",
             "aiid": "aiid_model_incidents_by_developer.csv, View 2", "mit": "the same file, View 2",
             "epoch": "model_capability.csv, View 2"}
    with st.expander("**Sources**", expanded=True):
        st.markdown("\n".join(f"- **{label}:** {cite} Data note: {SOURCES_3[k][3]}. "
                              f"File in the app: {files[k]}." for k, label, cite in [
            ("fmti", "Transparency scores", "Stanford Center for Research on Foundation Models (2025)."),
            ("aiid", "Incidents", "Responsible AI Collaborative (2026)."),
            ("mit", "Risk domains", "MIT AI Risk Repository (n.d.)."),
            ("epoch", "Model releases", "Epoch AI (2026).")]))
    _references_block([REF["fmti"], REF["wan"], ref_aiid(SOURCES_3["aiid"][3]), REF["mit"],
                       ref_epoch(ep["epoch_retrieved"])])
    with st.expander("**Methods**"):
        st.markdown(
            "- **FMTI scores (View 1):** 100 yes-or-no indicators for 13 companies, each for one flagship model, the one the company "
            "selected as of May 2025.\n"
            "  - *Domains:* the scores file has no domain column, so each indicator takes its domain and subdomain from its "
            "position in the indicator file of the same edition.\n"
            "  - *Check:* all 100 indicators matched, with Upstream 34, Model 30 and Downstream 36 in 19 subdomains.\n"
            "- **Heatmap cell:** the indicators a company discloses, over the indicators in the subdomain.\n"
            "  - *Rows:* grouped by headquarters region (the headquarters country is from Table 1 of Wan et al. (2025), the regions are the group's grouping) and sorted A to Z inside each "
            "group, so the order is not a ranking.\n"
            f"- **Model incidents (View 2):** the AI Incident Database export of 16 Nov 2026 holds {v3.AIID_SINCE_2020:,} incidents since "
            "2020.\n"
            f"  - *Developers:* {v3.AIID_NAMED} name one of the eleven, {v3.AIID_NAMED_DEV_FIELD} in the developer field and "
            f"{v3.AIID_NAMED_IMPLICATED} only in the implicated systems.\n"
            f"  - *Counted:* {v3.AIID_MODEL} are model incidents.\n"
            f"  - *Not counted:* {v3.AIID_NOT_COUNTED}, of which 61 are platform products, 5 are operations cases and 16 name a developer only "
            "as the place where a scam appeared.\n"
            f"- **Dots and counts:** one dot per incident and named developer, which gives {v3.AIID_DOTS} dots for {v3.AIID_MODEL} incidents.\n"
            "  - *Monthly strip:* it counts each incident once.\n"
            "- **Incident type:** the MIT risk domain grouped into four types.\n"
            f"  - *MIT:* set the domain for {v3.AIID_MIT_SET} incidents (circles).\n"
            f"  - *Project group:* for the other {v3.AIID_GROUP_SET} incidents only, which MIT has not classified yet (diamonds), the group "
            "assigned the closest MIT risk domain manually, with AI assistance in the reading of the incident title, the "
            "description and the developer, deployer and implicated-system fields.\n"
            f"  - *Counts by type:* {v3.AIID_TYPES[0]} wrong output or failure, {v3.AIID_TYPES[1]} data and security, "
            f"{v3.AIID_TYPES[2]} misuse by others and {v3.AIID_TYPES[3]} harm to users or society.\n"
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
            f"  - *Consequence:* {v3.AIID_2026_GROUP_SET} of the {v3.AIID_2026_INCIDENTS} incidents of 2026 had no domain, so the project group assigned their type "
            "manually and the page marks them as diamonds.\n"
            f"- **Epoch:** the capability list holds {v3.EPOCH_N} models, {v3.EPOCH_ELEVEN_N} of them from the eleven developers.")
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
    st.caption(f"Last data refresh: FMTI edition of December 2025. AI Incident Database export of 16 Nov 2026, latest "
               f"incident {v3.AIID_LATEST}. Epoch file retrieved {ep['epoch_retrieved']}, latest model release {ep['epoch_last']}.")


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
    with st.expander("**Sources**", expanded=True):
        cites = {"epoch": "Epoch AI (2026).", "litellm": "BerriAI (2026).", "lmarena": "LMArena (2026)."}
        lines = [f"- **{label}:** {cites[k]} Data note: {notes[k].lower()[0] + notes[k][1:]}. "
                 f"File in the app: `{file}`. Used in {used}." for k, (label, file, used) in keys.items()]
        lines.append(f"- **Licence marks:** the licence pages of {_names(marked)}, linked under the View 2 chart. The key "
                     "terms in the hover are the group's reading of those pages. Used in View 2 only.")
        st.markdown("\n".join(lines))
    _references_block([ref_epoch(snap.get("epoch_retrieved")), ref_litellm(snap.get("litellm_retrieved")),
                       ref_lmarena(snap.get("lmarena_published")), REF["ho"], REF["chiang"], REF["singh"],
                       REF["diakoulaki"], REF["lahdelma"]])
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
            "- **Weights (View 2):** CRITIC (Diakoulaki et al., 1995), or custom (the sliders start at "
            "5/5/5 = equal).\n"
            "- **Weighted score (View 2):** the sum of weight × percentile over the criteria in use, from 0 to 100.\n"
            "- **First-place share (View 2):** SMAA first-rank acceptability (Lahdelma & Salminen, 2001) over the 1,033 "
            "different weightings that the three 0 to 10 sliders can produce (settings with the same shares count once).\n"
            "- **Rounding:** charts and hovers show the LMArena rating as a whole number and the ECI to one decimal. Tables "
            "and CSV downloads keep the original values, except the computed weighted score and first-place share, which "
            "are shown to one decimal.")
    with st.expander("**Source choice and where the sources can mislead**"):
        st.markdown(
            "- **Epoch Capabilities Index (ECI):** a non-profit's joint fit of benchmark results (method: Ho et al., 2025; the Hub file of 20 Nov 2026 marks 58 benchmarks as part of it), used in the "
            "Stanford AI Index and the International AI Safety Report. It keeps each model's best setting, leans to maths "
            "and reasoning, covers smaller and non-US models less well, and its 90% intervals overlap for neighbours.\n"
            "- **LMArena:** millions of public pairwise votes (Chiang et al., 2024), quoted by labs at launch. Voters "
            "are self-selected, longer, well-formatted answers win more often, and labs can test private variants "
            "(Singh et al., 2025). It agrees with capability at about " + snap.corr_text() + " at the default settings, so it is a "
            "cross-check more than an independent measure.\n"
            "- **LiteLLM:** a widely used open-source gateway whose price file is updated by "
            "community pull requests and carries no date. List price per token is not cost per task.\n"
            "- **Licence labels:** Epoch's label can differ from the licence text, so the marks in View 2 show both.")
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
