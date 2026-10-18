# Deep Research Brief, Round 3: source leads and visual ideas

Paste everything below the line into Gemini Deep Research. Written 18 October 2026.

How we will use the answer: we treat every item as a lead and nothing else. Claude opens each URL, checks the quoted text against the page, checks the licence and the field names, and drops anything that cannot be opened. Only items that pass are cited in the project.

---

## Context

We are a university group building a Streamlit data story. Our single question is:

> In regions where leading closed US models are restricted, which accessible AI model gives an organisation the most measured capability for its cost and data-control needs?

Our one persona is a group enterprise architect at an Asia-Pacific bank or insurer. Within one to two weeks the architect must give the risk committee an interim approved list of AI models. The architect needs to decide which accessible models pass a data gate for the level of data staff will send, whether waiting for US access is worth it, and whether the choice can be defended to a regulator.

Our chapters are:

- Q1 best accessible option (capability, cost, data control)
- Q2 capability gap over time
- Q3 independent versus self-reported benchmarks
- Q4 real-world usage (optional, weakest)
- Q5 developer disclosure about data handling
- Q6 reported AI incidents (optional)
- Q7 which providers are available in which place (optional)
- Q8 capability by model licence class (optional)

We already hold, so do not suggest these: Epoch AI capability index and benchmark files, LiteLLM price file, LMArena leaderboard data, Wikimedia page views, the AI Incident Database snapshot page, and three hand-made tables (provider data handling, data-protection rules for four places, provider availability by place).

Do not suggest Kaggle datasets, GitHub scrapes or blog copies unless you can point to the original publisher and a licence statement on the original page.

## Strict output rules

1. Report only pages you actually opened and read. Mark each item "opened" or "not opened". Items marked "not opened" will be discarded.
2. Never guess a URL. Give the exact address of the page you read.
3. Copy the licence or terms-of-use sentence exactly as written on the page, in quotation marks. If the page has no licence text, write "no licence text found".
4. Copy the column names or field names exactly as written. If the page does not list them, write "fields not listed".
5. Give the publication or last-updated date shown on the page. If none is shown, write "no date shown".
6. Do not summarise findings, do not give statistics and do not give conclusions. We only want where to look.
7. At most three candidates per gap. Fewer is fine. If you find nothing credible, say so.
8. No advice about bypassing access restrictions, VPNs or evading controls. This is policy and market analysis.

## Part A: source leads

For each gap below, list candidates in this format:

- Gap:
- Publisher and page title:
- Exact URL:
- Opened or not opened:
- Date shown:
- Licence or terms sentence, copied exactly:
- Field names, copied exactly:
- Which of Q1 to Q8 it could support and why in one sentence:

Gaps:

1. **Real-world usage by model (Q4).** Public, reusable data on how much each model or developer is used, ideally by region or country and including Chinese and open-weight models. Examples of the kind of thing we mean are token share, API traffic share or survey data. State clearly whether the data covers one developer only.
2. **A per-developer transparency or data-practice score (Q5).** Any published index or audit that scores or rates AI developers on disclosure, data handling or privacy, with the scores available for download.
3. **Reported AI incidents (Q6).** Any publisher other than the AI Incident Database that publishes incident records about named AI systems or developers in a reusable form, with a country or region field if one exists.
4. **Availability of Mistral, Meta and Google open-weight models and of cloud resellers in Hong Kong and Singapore (Q7).** Official provider or cloud documentation pages that list where each model is offered. Official pages only.
5. **Financial-sector rules that affect the choice (Q5).** Official regulator pages from Hong Kong (HKMA, PCPD), Singapore (MAS, PDPC), Australia (APRA) and Taiwan (FSC) about AI use, outsourcing, cloud or cross-border data in banks and insurers. Official regulator pages only, no law-firm summaries.
6. **Licence texts of leading open-weight models (Q8).** The official licence page or model card for Kimi K3, DeepSeek V4, GLM-5, Qwen and MiniMax models, with the sentence that says whether commercial use is allowed.
7. **Price history (Q1 cost).** Any public, reusable record of how API list prices for named models have changed over time.

## Part B: visual ideas

Our persona decides by looking at charts, so we want to test our design against how others show similar choices.

For each of Q1, Q2, Q3, Q5 and Q7, give up to three chart ideas. Use chart names from the Financial Times Visual Vocabulary (for example ordered bar, slope, scatterplot, XY heatmap, paired bar, stacked column, lollipop, diverging bar). For each idea give:

- The decision the architect would make from it.
- The fields we would need.
- One real, existing public example of a similar chart, with its exact URL and "opened" or "not opened". Examples can come from model leaderboards, Epoch AI, OpenRouter, Artificial Analysis, LMArena or anywhere comparable. Do not describe an example you did not open.
- One way the chart could mislead a risk committee, and how to avoid it.

Also tell us which one or two charts you would drop if we only had time for four, and why.

## Final check

End with a table of every URL you list, with columns: URL, opened or not opened, date shown, licence sentence found (yes or no). Do not add anything else after the table.
