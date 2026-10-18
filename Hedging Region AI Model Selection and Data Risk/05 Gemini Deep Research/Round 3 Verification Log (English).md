# Gemini Round 3 verification log

Date: 18 October 2026. Brief used: `Deep_Research_Brief_Round_3_Leads_and_Visuals.md` (same folder). Gemini output: `Gemini Round 3 Output (uploaded by Ian).docx` (same folder).

Rule we applied: Gemini's "opened" label counts for nothing. We opened every page ourselves with our own tools (WebFetch and search) and wrote down what we saw. Where a site was blocked to our tool we did not use another route, and the item stays "unverified".

## Result in one line

Gemini listed 14 pages, which the table below groups into 10 sources. Of the 10, 5 passed (the Stanford FMTI page and its licence, HKMA, APRA, MAS, the Epoch data page), 1 is a secondary source only (AIAAIC), 1 is unverified (PCPD PDF), 3 were rejected (OECD AI Incidents Monitor, Inhumain, OpenRouter OP.GG). No new data file was opened. Nothing was found for Q7, for open-weight licence texts or for price history.

## Page by page

| Source | What we saw | Result | Used for |
|---|---|---|---|
| Stanford Foundation Model Transparency Index, December 2025, and its GitHub repository | The page lists 13 developers, including Alibaba, DeepSeek, Mistral, Anthropic, OpenAI, Google, Meta and xAI. The repository shows a CC-BY-4.0 licence and the README says all data and visuals are CC-BY. Gemini wrongly said no licence was found. Our tool is blocked from the repository folder, so file names and columns are unchecked | Verified for the page and licence, files unchecked | Q5 context. Ian to download the Dec2025 folder in a browser |
| OECD AI Incidents Monitor | Copyright line "© 2026 OECD. All rights reserved", no download | Rejected for reuse | None |
| AIAAIC Repository, OECD catalogue entry | The entry gives the licence as "Creative Commons Attribution Share Alike 4.0 International". aiaaic.org itself is blocked to our tool | Secondary source only | Q6 fallback. Confirm the licence on aiaaic.org |
| Inhumain AI incident tracker | Not an original dataset, it draws on AIAAIC and the AI Incident Database. The full database is only on request and no licence is shown | Rejected | None |
| OpenRouter OP.GG page | Token use of one app only, no region and no licence | Rejected | None |
| HKMA, "ART" Framework press release, 15 October 2026 | Announces updated supervisory guidance, a training data sharing platform and a coming discussion paper on agentic AI. Copyright "© 2026 Hong Kong Monetary Authority. All rights reserved." | Verified, cite only | Q5 regulator note |
| APRA, CPG 230, June 2024 | Guidance and not the binding standard, which is CPS 230. Incident notice within 72 hours. Licensed CC BY 3.0 Australia | Verified | Q5 regulator note |
| MAS, FEAT principles | Published 12 November 2018 and updated 7 February 2019, Gemini gave only the update date. Binding status not stated | Verified | Q5 regulator note |
| PCPD, AI Model Personal Data Protection Framework | Our tool returned no text from the PDF | Unverified | Ian to open it in a browser |
| Epoch AI data page | States that data is "free to use, distribute, and reproduce provided the source and authors are credited" under a Creative Commons Attribution licence | Verified | Settles the Epoch licence question for ECI, benchmarks and models data |

## Errors in Gemini's report

1. It said the Stanford index has no licence. The repository shows CC-BY-4.0.
2. It used the OECD AI Incidents Monitor dashboard as the public example of an availability heatmap. That dashboard shows incidents and policy initiatives, not provider availability.
3. It advised linear cost axes for the capability-against-price chart. Our prices span several orders of magnitude, so we keep a log axis with labelled ticks and a note.
4. It cited our own brief as evidence that pages were "opened".
5. It gave no usable result for Q7 (availability of Mistral, Meta, Google and resellers in Hong Kong and Singapore), for the licence texts of Kimi K3, DeepSeek V4, GLM, Qwen and MiniMax, or for price history.

## Chart ideas: what we took and what we did not

| Gemini idea | Decision |
|---|---|
| Q1 scatterplot of capability against cost, with a data-control gate | Already in our design (V4, with the gate in V1) |
| Q2 slope chart of the open or non-US gap over time | We use a change-over-time line or step (V2). Slope would show only two dates |
| Q3 paired bar of self-reported against independent scores | We use a diverging bar (V3). Its warning is useful: compare scores only when the test setting is the same (for example the same number of shots) |
| Q5 stacked column of transparency sub-scores | Our V5 is a stacked column of data-handling terms from Search A. FMTI sub-scores could add context only after Ian opens the files |
| Q7 XY heatmap | Gemini itself would drop it if only four charts fit. We agree and keep V6 optional and not counted |

Gemini's chart ideas were used only as prompts for our own design.

## What is still open after Round 3

Ian to download the FMTI Dec2025 folder and the AI Incident Database export in a browser, open the PCPD PDF, and confirm the AIAAIC licence on aiaaic.org. The open-weight licence pages were checked afterwards by Claude on 18 October (see Licence Check for Open-Weight Models). The GLM-5 LICENSE file is still unread. No usage source exists for Q4.

## Source links

Addresses of the pages in the table above. Where the original address was not saved, the row says so, and addresses found later by search are marked to be confirmed.

| Source | Address |
|---|---|
| Stanford FMTI December 2025 page | https://crfm.stanford.edu/fmti/December-2025 |
| Stanford FMTI repository | https://github.com/stanford-crfm/fmti |
| Stanford FMTI paper | https://crfm.stanford.edu/fmti/December-2025/paper.pdf |
| AI Incident Database snapshots page | https://incidentdatabase.ai/research/snapshots/ |
| MAS terms of use (address supplied by a team member, our tool could not load it) | https://www.mas.gov.sg/terms-of-use |
| Epoch benchmarking data page (CC BY 4.0, read 2026-10-18) | https://epoch.ai/benchmarks/about |
| OECD AI Incidents Monitor | https://oecd.ai/en/incidents (main page, the address Gemini cited is not recorded) |
| AIAAIC Repository | https://www.aiaaic.org/aiaaic-repository (the OECD catalogue entry address is not recorded) |
| Inhumain AI incident tracker | address not recorded |
| OpenRouter OP.GG page | address not recorded |
| HKMA ART press release, 15 October 2026 | https://www.hkma.gov.hk/eng/news-and-media/press-releases/2026/10/20261015-3/ (confirmed by a team member on 18 October 2026) |
| APRA CPG 230 | https://www.apra.gov.au/practice-guides/cpg-230 (confirmed by a team member on 18 October 2026) |
| MAS FEAT principles | https://www.mas.gov.sg/~/media/MAS/News%20and%20Publications/Monographs%20and%20Information%20Papers/FEAT%20Principles%20Final.pdf (confirmed by a team member on 18 October 2026, the page read may be a web page that links to this PDF) |
| PCPD AI page | https://www.pcpd.org.hk/english/artificial_intelligence/index.html |
| PCPD Model Framework PDF (June 2024) | https://www.pcpd.org.hk/english/resources_centre/publications/files/ai_protection_framework.pdf |
| PCPD agentic AI guidance (August 2026) | https://www.pcpd.org.hk/english/resources_centre/publications/files/pcpd_use_of_agentic_ai.pdf |
| Epoch AI data page | https://epoch.ai/data |
