# Project memory: Hedging Region AI Model Selection and Data Risk

36104 Assignment 3 group Streamlit data narrative. Written 16 October 2026 as a running record of what Ian and Claude have discussed and decided. Read README.md first for the folder map. This file records the reasoning and the decisions.

**Limits of this record.** It is rebuilt from the session notes that Claude kept, plus the files in this folder. The earliest part of the conversation, up to the point where the revised topic was chosen, is only known through those notes, so the order of early events may be slightly off. Ian should correct anything that does not match his memory.

## 1. Where the project stands today

- The group is building a Streamlit data narrative for Assignment 3.
- The topic was revised from four earlier proposals (P1 to P4, 14 October 2026) to one decision topic: AI model choice and data risk where leading closed US models are unavailable or restricted.
- "Hedging area" is read as Hong Kong and the wider Asia-Pacific, with Hong Kong as the worked example. **Ian has not yet confirmed this reading.**
- The final proposal, the dataset inventory, the deep research log and three hand-built search tables are written and saved in this folder.
- Ten notebooks in the Data folder (01 to 10) build the processed tables, and the proposal and dataset documents were synced to them on 18 October 2026 (see 8g).
- Next date: Part 1 recording, Friday 23 October 2026, 11:59pm (the brief) or 26 October (the Canvas header). Confirm with the teaching team.

## 2. The decisions, in the order they were made

1. **Four earlier proposals were compared.** They all described the AI field. P1 Compute concentration vs access (feasibility 16), P2 Attention vs capability (14), P3 AI energy geography (15), P4 China compute efficiency (15).
2. **The topic changed from describing the field to helping a named person choose.** The choice is arguable because the answer moves with the weights the person sets. P3 was dropped because energy data does not bear on model choice. P1, P2 and P4 each contribute a piece of data or a comparison.
3. **The core question (Q1).** In regions where leading closed US models are restricted, which accessible AI model gives an organisation the most measured capability for its cost and data-control needs? It is one sentence with a plain subject, verb and object, and it names no place, because the assignment wants one arguable question stated in one sentence. The original two-part wording (which option, and how much the answer depends on the weights) is kept in the proposal as an alternative with the same meaning, for the group to decide. Only one wording goes in the README. In the SVO version the weights are not in the question. They are the sliders, and they are why the answer is arguable.
4. **One question and seven evidence chapters.** Q2 to Q6 are written as statements, not questions, so the README and the app show only one question. Q2 capability gap over time, Q3 independent versus self-reported benchmarks, Q4 real-world usage (optional), Q5 developer disclosure, Q6 reported incidents (optional). Core chapters are Q1, Q2, Q3 and Q5. Q4 and Q6 are the first to drop if time runs short.
5. **Personas are chosen by identity and role.** Primary persona: group enterprise architect at an Asia-Pacific bank or insurer (persona 3). Extra slider presets: technology advisory partner (persona 6) and group head of IT infrastructure (persona 2). The earlier slider presets (numbers per role) were removed from the proposal. Weighting is now optional and to be decided later by the group. If built, the neutral default is equal weights.
6. **Weighting is optional and deferred.** The proposal no longer states weight numbers or role presets. If the group builds sliders, they default to equal weights. Any score is a weighted sum of three 0 to 100 scores (capability as a percentage of the best model's Epoch score, cost on a log scale from LiteLLM prices, data control from the Search A coding rules), to be discussed later.
7. **Datasets were ranked with a fixed formula.** Score = 3 x Fit + Held + Licence + Effort, each scored 0 to 3, maximum 18. Tier 15 and above is compulsory, 12 to 14 optional, below 12 dropped. The full table is in 02 Dataset Usage.
8. **Gemini Deep Research was tried for two rounds, then dropped.** See section 4.
9. **Three searches were built by hand from provider and regulator pages.** Search A provider data handling, Search B data-protection rules by jurisdiction, Search C provider availability by country. Every row cites the page it was read from and the date it was read.
10. **Everything was written up in two languages.** The finalized proposal and dataset documents exist in English and Traditional Chinese (Taiwan).
11. **Everything was saved into one folder** under Assignment 3, named after the proposal, with Markdown copies added at Ian's request (see section 7).

## 3. The data backbone

Updated 18 October 2026. Each row has a notebook in the Data folder.

| Need | Source (notebook) | Status |
|---|---|---|
| Capability scores per model | Epoch ECI (01) | In hand. 277 models to 7 October 2026, 76 China-based of which 63 open weights. Claude Opus 5.5 166.82, Kimi K3 157.42, gap 9.4, median confidence interval 7.1 |
| Prices | LiteLLM price file (04) | In hand. 4,206 rows, MIT licence checked, current prices only |
| Availability by country | Search C (03) | Done by hand. 28 rows, 7 providers, 16 rows "no list found" |
| Data handling by provider | Search A (02) | Done by hand. 12 rows, 7 providers, about half the fields not stated or not checked |
| Data-protection rules | Search B (05) | Done by hand. Plus regulator pages and both PCPD PDFs (CC BY 4.0) |
| Human preference ratings | LMArena (06) | In hand. Cross-check for Q1 and Q2 |
| Independent benchmark scores | Epoch Benchmarking Hub files (07) | In hand. 5,301 score rows, 61 benchmarks. The source column and the hand-made independent or self-reported map are still to do |
| Developer transparency (Q5 context) | Stanford FMTI Dec 2025 (08) | In hand. 13 developers by 100 indicators. IBM 95, DeepSeek 32, Alibaba 26 |
| Compute and cost context (Q2) | Epoch AI models CSV (09) | Notebook written, tested only on made-up data. First real run still to do |
| Incident records (Q6) | AI Incident Database export of 12 October 2026 (10) | In hand. 1,734 incidents, only 8 name DeepSeek, Alibaba, Z.ai or Moonshot |
| Usage share (Q4) | None | No source. Wikimedia page views struck by the team on 18 October 2026 |

## 4. What happened with Gemini

- Round 1: a brief (R1) was pasted into Gemini Deep Research. It returned eight candidate datasets.
- Round 2: a corrections brief (R3 in the log) asked Gemini to fix its errors and run six new searches (A to F).
- The Round 2 report repeated the same mistakes. It kept datasets we had told it to drop, left irrelevant citations in its reference list, left more stray citation markers than before, and contained no search section at all.
- A prompt limited to Searches A, B and C was drafted in the Gemini input box on 15 October (screenshot R6). No answer to it was kept.
- Round 3 (18 October 2026): a new brief asked only for source leads and chart ideas (`Deep_Research_Brief_Round_3_Leads_and_Visuals.md`). Ian ran it and uploaded the output. We opened every page ourselves. See section 8f.
- **Decision (16 October 2026):** stop using Gemini. The quality was too low to rely on. The three searches were done by hand instead. If more web research is needed (Q4, Q5, Q6), a Perplexity or Grok style search is the likelier tool, but every source page still has to be opened and checked by a person.
- What was kept from Gemini: pointers to LiteLLM prices, LMArena ratings and the Stanford transparency index. Nothing was used as-is.

Verdicts on the eight Round 1 datasets, from pages opened on 15 October 2026:

- **Keep:** LiteLLM price file (compulsory, score 15, licence to confirm). LMArena leaderboard dataset (optional, score 13, used for Q4).
- **Keep as a lead only:** Stanford FMTI metrics file (it holds metric definitions, not developer scores).
- **Drop or background only:** Stack Overflow Developer Survey (score 9), JailbreakBench behaviours (no per-model attack rates), LiveBench coding page (questions only, no model scores), Open LLM Leaderboard contents (last updated March 2025, no licence label), AA-Briefcase-Lite (example scenarios, no price or latency data).

## 5. What the three searches found

**Search A, provider data handling (seven providers, read 16 October 2026).**

- OpenAI, Anthropic and Google's paid Gemini API say they do not train on API customer data by default. Google's unpaid tier does allow training and human review.
- Alibaba Cloud Model Studio says it will never use customer data for training. The pages read did not say where data is stored.
- Z.ai (Zhipu) international API says it will not use user content to improve services unless the customer agrees. Its servers are in Singapore and the terms use Singapore law.
- Moonshot (Kimi) international uses Singapore servers and law, but customer content may be used to improve services unless a written agreement says otherwise.
- The mainland China sites (bigmodel.cn, platform.kimi.com) store data in mainland China, with clauses allowing disclosure to authorities.
- DeepSeek's privacy policy dates from May 2024 and never names the API. Many DeepSeek API values are therefore not stated.
- Singapore storage does not settle jurisdiction. Each company also runs a China site under mainland law.

**Search B, data-protection rules (Hong Kong, mainland China, Singapore, Taiwan).**

- Mainland China has the strictest rule (PIPL Articles 38 to 41, with volume thresholds from the March 2024 Provisions).
- Hong Kong has no statutory transfer limit in force. Section 33 of the Ordinance is on the books but not in operation. The regulator issued voluntary model clauses.
- Singapore requires comparable protection abroad (PDPA section 26).
- Taiwan's transfer rule is moving to a new regulator. The 2025 amendment was promulgated but its effective date is not set.
- Several regulator pages (PCPD, Taiwan, Singapore PDPC) could not be opened, so some rows rest on law-firm summaries and are marked that way.

**Search C, provider availability.** A "not on the list" result is not the same as "blocked", because the pages say where service is offered, not how it is enforced. OpenAI and Anthropic pages show no date. China-site products and cloud resellers are not covered. See the PDF or Markdown copy for the full table.

## 6. App plan (from the final proposal)

- Pipeline and app files with views V0 to V9 (V9 for Q4 is dropped), at least four charts across ranking, correlation, change over time and deviation.
- The headline view lets the reader move the three weights and see which accessible model wins for the chosen persona.
- Limits are stated openly. The tables record what providers say in their documents, not what they do. Terms change, so pages need rechecking before submission.

## 7. Files and folder history

- Folder: `D:\UTS MDSI\36104 (2026)\Assignment 3\Hedging Region AI Model Selection and Data Risk`.
- 01 Final Proposal and 02 Dataset Usage are the formal documents, each in English and Traditional Chinese, as Word and Markdown.
- 03 Deep Research Documentation is the log of every Gemini round and our own searches, as PDF and Markdown.
- 04 Searches A B C holds the three searches as PDF. The English versions also have Markdown copies. The Chinese Search B and C stay PDF-only as reading copies. This was Claude's recommendation because the English tables feed the pipeline CSVs, and Ian can overrule it.
- Data holds notebooks 01 to 10, one folder each with raw and processed files, Data/README.md, Data/raw/README.md (manual download routes) and q_charts (first-pass charts for Q1 to Q3, Q5, Q7, Q8 drawn on 18 October 2026, plus the Q6 chart in 10_aiid_incidents).
- 05 Gemini Deep Research holds the three briefs (Round 3 as Markdown), Ian's three Gemini reports, the Round 3 verification logs (English and 繁體中文) and the screenshots.
- The Markdown for 03 and 04 was converted from the PDF exports and spot-checked. The Markdown for 01 and 02 was converted from the Word files, so wide table columns are cosmetic only.
- The live, editable copies are Claude Docs. IDs are in README.md.

## 8. Open decisions for Ian

1. Confirm that "hedging area" means Hong Kong and the wider Asia-Pacific.
2. Check with the teaching team that a decision tool fits the Assignment 3 question territories. The earlier four proposals fitted more obviously.
3. Part 1 recording due date: 23 October (brief) or 26 October (Canvas header).
4. Which optional chapters to keep (Q7, Q8). Q6 was brought back on 18 October 2026 as a small chapter (confirm with the group). Q4 has no data source and is dropped unless one is found.
5. Decide whether the Chinese Search B and C also need Markdown copies.
6. Decide whether Gemini is dropped for good or run again. Ian re-ran it on 18 October, so the log does not say "retired".

## 8b. Check against the assignment brief (16 October 2026)

- The brief asks for one arguable question stated in one sentence, one named persona with the decision it serves, and three user stories in as-a, I-want, so-that form. The README and the app's opening screen must show the question.
- The proposal was changed to match. There is one core question in subject-verb-object form, Q2 to Q6 are chapters, and the slider presets are no longer called personas.
- Persona 3 as the primary persona is still our proposal, and Ian and the group have not yet confirmed it.
- The datasets do not depend on the persona. Epoch, LiteLLM and Searches A to C serve every persona. The persona only sets the default slider weights and the build order of chapters.
- The question territories in the brief do not list a decision tool, but the brief allows "propose your own". Check with the teaching team.

## 8c. Situation 1 as finalised on 16 to 18 October 2026

- Situation: leading closed US models are not offered in Hong Kong and the risk committee wants an interim approved list within one to two weeks (an assumption to validate).
- Task: for each candidate model, say whether it is approved, by which route (regionally hosted, non-US hosted or self-hosted open weights) and for which data level (public, internal, customer personal data).
- V1 gets a data-level selector that works as a gate. Options that fail the gate are removed with the reason and source shown, then the rest are ranked.
- The list is interim. It is reviewed when provider terms change, US access changes or a stronger accessible model appears, and each version is kept with its date, data level and sources. An optional download button could save the list as CSV.
- Acceptance criteria for all three stories are now in the proposal. A layout picture of V1 (placeholder values) is saved as V1 Ranked Options mockup.png in folder 01.
- Telecom and other regulated sectors face the same choice but get no persona of their own. The data-level selector covers them.
- Known gap: financial-sector regulator rules are not covered by Search B.

## 8d. One persona only (18 October 2026)

- The proposal now serves one persona, the group enterprise architect. The other seven roles and the value-linkage matrix were removed from the proposal. They remain in the Round 1 brief for reference. The architect's own ratings are kept: Q1 Essential, Q2 High, Q3 High, Q4 Medium, Q5 High, Q6 Medium.
- The three user stories are all written for the architect. Story 1 now starts from the data level and the data gate.
- A list of interface checks from the Users and Interfaces lecture (Nielsen heuristics, Shneiderman, one-second latency) was added after the acceptance criteria.
- Done on 18 October 2026: Q1 to Q6 and V0 to V6 were reworked, see section 8e.

## 8e. Questions and views reworked (18 October 2026)

Ian approved the new structure. Q1 stays the one question. Q2 to Q8 are evidence chapters. Old numbers Q1 to Q6 were kept so the earlier documents still read correctly, and Q7 and Q8 were added.

Ranking by feasibility and data quality (core):

1. Q2 capability gap over time (V2). Epoch scores and metadata, quality high, no join needed.
2. Q3 independent versus self-reported (V3). Epoch benchmark files, quality high, but the flag is hand-coded.
3. Q5 developer disclosure (V5). Search A (13 rows) and Search B (4 places), quality medium, no ready-made score, so shown as counts and sourced facts.
4. Q1 core question (V1 and V4). Needs the model crosswalk first, so it is last on feasibility but built first.

Optional, in priority order: Q7 availability by place (V6, Search C), Q8 capability by licence class (V7, the Epoch capability file we already hold), Q6 reported incidents (V8, AI Incident Database), Q4 usage (V9, only a weak proxy, dropped first).

Views: V0 opening, V1 gated ranking, V2 gap over time, V3 independent versus self-reported, V4 capability against price, V5 developer data handling (part-to-whole with a detail table). Core gives five charts in five families. The family of V6 and V7 is still to be checked against the Visual Vocabulary.

The question tree figure in the proposal was redrawn on 18 October 2026 (persona, Q1, three stories, chapters with view numbers, data boxes, dashed optional boxes). It is a widget in the document, and the PNG copies are in media-en and media-zh.

Stories keep their order but the verbs now differ: story 1 sets and shortlists, story 2 measures and checks, story 3 reviews and traces. Story 1 also uses V4 and story 3 uses V5.

Sources checked on 18 October 2026 (page text only, no data file opened yet):

- AI Incident Database: weekly snapshots, latest 2026-10-12. Database collections are CC BY-SA 4.0. The reports text field is excluded. Developers and deployers are "alleged". Sources are mostly English media. No country field found.
- Epoch Data on AI Models (datahub copy): CC-BY 4.0. The package schema lists Model accessibility and Country (of organization). Only the first 47 old rows could be read, so it is not needed. Q8 uses the Epoch capability file we already hold.
- OpenRouter: only a daily top-50 API that needs a key, no licence stated. Not used.
- Anthropic Economic Index: data CC-BY, Claude only. Not usable for model choice.
- Microsoft Global AI Adoption 2025: DeepSeek share map by country, no reuse terms and no downloadable table. Background only.
- Epoch LLM inference price trends: March 2025, data to February 2025, no licence seen. Not used.
- Kaggle: many LLM benchmark, price and incident datasets, but the pages show no owner, licence, date or source. Used only as pointers to the original sources, never cited as a source.

Checked on real data (eci_scores.csv, 274 models) on 18 October 2026: it has Model accessibility and Accessibility group and Country columns. 22 models have unknown accessibility and 17 have no organisation or country. Best score by class: API access 167.33 (Claude Opus 5.5), open weights non-commercial 157.45 (Kimi K3), open weights unrestricted 155.31 (DeepSeek V4 Pro 0813), open weights restricted use 146.95 (MiniMax-M3), hosted access with no API 149.16 (Grok 4.3 Beta). The best open model is labelled non-commercial, which is why Q8 asks about the licence class. The labels are Epoch's, so check each licence text before stating it. Result of the 18 October licence check: Epoch labels Kimi K3 non-commercial, but the Kimi K3 License allows commercial use with a Model as a Service revenue condition and exempts internal use, so that label does not match the licence text we read. Epoch's own definition (Table A1) says restricted use means limits on user counts or purposes and non-commercial means commercial use is not allowed, so Kimi K3 fits restricted use. DeepSeek V4 (MIT) matches unrestricted. MiniMax M3 (community licence with notice, attribution and a military ban) is plausibly restricted use. Q8 should use our own class from the licence text and show Epoch's label beside it. Q8 overlaps Q2 if framed as open against closed, because the best open model is also the best Chinese model.

Chart families checked against the FT Visual Vocabulary poster: paired bar and paired column are Magnitude, stacked column is Part-to-whole, XY heatmap is Correlation, slope and lollipop are Ranking. There is no plain matrix heat map, so V6 is drawn as an XY heatmap and not counted.

Still to check: the AI Incident Database file has not been opened. Ian can download the weekly Excel export from the snapshots page and put it in the folder, or I can read it if it is staged. Also read the AWS Bedrock regional availability page if a cloud-region question is wanted later.

Gemini: Ian is considering running deep research again but worries that Gemini 3 Flash hallucinates. The agreed method if it is run: lead generation only (URL, exact quote, date), every URL opened and checked by hand, scope limited to Q4 usage sources, a Q5 transparency score, and Search C gaps (Mistral, Meta, Google open weights, Hong Kong and Singapore cloud resellers). Section 4 is not rewritten as "retired" until Ian decides.

## 8f. Gemini Round 3 checked, ranking and situations updated (18 October 2026)

Gemini listed 14 pages and marked all of them opened. We opened each one. Passed: Stanford FMTI December 2025 page and licence (CC-BY-4.0, Gemini was wrong that it has none, repository files unopened because our tool is blocked), HKMA ART press release 15 October 2026 (cite only), APRA CPG 230 (CC BY 3.0 Australia, guidance not the binding CPS 230), MAS FEAT (published 12 November 2018, updated 7 February 2019), Epoch data page (CC attribution, settles the Epoch licence). Secondary only: AIAAIC (CC BY-SA 4.0 per the OECD entry, aiaaic.org blocked). Unverified: PCPD PDF (no text came back). Rejected: OECD AI Incidents Monitor (all rights reserved), Inhumain (not original), OpenRouter OP.GG (one app, no licence). Nothing found for Q7, open-weight licence texts or price history. Gemini errors: FMTI licence, OECD dashboard used as a heatmap example, linear cost axis advice, our own brief cited as proof of opening. Full log in folder 05.

FMTI scores how openly a model was built, not how a customer's data is handled, so it is Q5 context and does not replace Search A.

Dataset ranking redone (02 Dataset Usage, 20 rows, tier Reserve added for unopened files): compulsory ECI 18, Search A 17, Search C 17, Epoch benchmark files 16, LiteLLM 15. Optional 13 to 12: Search B, LMArena, regulator pages, Epoch models CSV, Epoch per-benchmark CSVs, Wikimedia. Reserve 11: FMTI, AI Incident Database. AIAAIC 8.

Assumed situation for each question (proposal and 02, except Q4 and Q6 which are not tied to one): Q1 interim approved list in one to two weeks for the data level staff will send. Q2 whether waiting for US access is worth it. Q3 the committee quotes developer claims and needs independent confirmation. Q5 a regulator or auditor asks how the choice was made. Q7 some staff already use a hosted model and the provider must be offered where the bank operates. Q8 whether a self-hosted open-weight model may be used commercially, since data stays inside the bank. These are assumptions, not tested with a real architect.

Dataset to question map: Q1 ECI, Search A, Search C, LiteLLM (Search B and LMArena support). Q2 ECI and benchmark model_metadata. Q3 processed_data_for_eci plus the hand-made source flag. Q5 Search A, Search B, regulator pages (FMTI context). Q6 AI Incident Database (AIAAIC fallback). Q7 Search C. Q8 ECI accessibility columns plus licence texts. Q4 Wikimedia page views only, a weak proxy.

## 8g. Notebooks 08 to 10, data quality, Q6 back, documents synced (18 October 2026)

- Notebooks 08 (FMTI), 09 (Epoch AI models) and 10 (AIID incidents) were built and the data folder README was updated. They are English only with no licence content. Notebooks 01 to 07 were left as they were.
- Data quality review of every processed table. Difficulty from easiest to hardest: Q2 and Q8 feasible now, Q7 and Q5 medium (Q7 has 16 of 28 rows "no list found", Q5 about half the fields not stated), Q6 medium (data ready, but only 8 incidents name the China-scope developers), Q3 medium to hard (needs the source column and a hand map), Q1 hardest (needs the crosswalk), Q4 not feasible (no source).
- Q6 was brought back as a small included chapter. The chart window starts in 2022. Incidents per year (all and generative-related): 2022 109/16, 2023 179/79, 2024 308/177, 2025 457/359, 2026 257/195 (to 3 October, partial). Since 2022 OpenAI 176, Google 76, Meta 52, Anthropic 39. The generative flag is a keyword rule and a lower bound.
- Wikimedia page views were struck by the team, so Q4 has no data source. AIID was restored for Q6.
- The dataset ranking was re-scored: 20 candidates, 5 compulsory (ECI 18, Search A 17, Search C 17, LiteLLM 17, benchmark files 16), 7 optional (LMArena, per-benchmark CSVs, FMTI 14, Search B, AIID 13, regulator pages, Epoch models CSV 12) and 8 dropped (Wikimedia, Stack Overflow, ChatGPT usage, polling, AIAAIC, data centers, Ember, OWID and IEA).
- 01 Final Proposal and 02 Dataset Usage (EN and 繁體中文, md and docx) were synced to all of the above, with a new section on data quality and difficulty by question, a new processed-file table with a notebook column, redrawn question-tree and crosswalk figures, and wider tables (02 is now landscape). Folders 03, 04 and 05 are historical records and were not changed.
- The Q2 gap: the best China-based model has trailed the best overall by 5 to 10 points at every half-year since end-2023 (8.4, 4.7, 9.5, 6.1, 9.9, 8.3, 9.4), about the size of the 7.1-point confidence interval, so the proposal says it has not narrowed and does not claim it is shrinking or growing.
- First-pass charts for Q1, Q2, Q3 (coverage only, the deviation chart needs the source map), Q5, Q7 and Q8 are in Data/q_charts.
- PCPD: both PDF addresses were supplied by a team member and checked, and both PDFs are CC BY 4.0.

## 8h. Alternative proposal and dataset issues added (18 October 2026)

- Dataset issues and limitations found in testing (12 items) were added to 01 Final Proposal and 02 Dataset Usage, with a note on what happens if Searches A, B and C are dropped.
- 01b Alternative Proposal (No Search ABC) was written on the Final Proposal template. Persona and three-story structure unchanged. Core question: "...most measured capability for its cost and self-hosting feasibility?" Data control becomes open weights plus a licence that allows commercial self-hosting (a proxy). Q7 removed (only Search C could answer it), Q4 dropped, Q5 reworked as FMTI transparency joined to Epoch and AIID (only 9 developers appear in both, no visible link), Q8 raised to a core chapter, Q6 stays small. Q1 gets lighter because about 155 ECI models already match a LiteLLM chat price. Weakness: the app cannot say where a provider is offered.
- Chart for the alternative: Data/q_charts/alt_transparency_capability_incidents.png.
- Claude's recommendation: keep Searches A and C (done, small), Search B can go. The group must choose between 01 and 01b.

## 9. Still to do

Updated 18 October 2026.

- Run notebooks 01 to 10 once on a team machine. Notebook 09 has only been tested on a made-up table, so its first real run is the real test. Epoch, Hugging Face, GitHub archive and the AIID host are blocked from the cloud sandbox, so save files by hand under Data/raw if a download fails.
- Build the model crosswalk (Epoch, LiteLLM, LMArena, Search A). First-pass exact-name matches of the 277 ECI models: LiteLLM 186, LMArena 77, benchmark files 122, and for the top 50 models 49, 24 and 12. The Q1 scatter (Data/q_charts) uses 155 models with a chat price.
- Add the Source column back to notebook 07 (processed_data_for_eci.csv has 2,898 rows: 1,270 blank, 872 paper or report, 756 URL) and build the benchmark source map for Q3.
- Add a name-based China fallback for the 17 ECI rows with no organisation or country.
- Read the MAS general terms (address recorded, text unread). Check the Creative Commons version on the Epoch ECI chart page (the benchmarking about page states CC BY 4.0).
- Check the Zhipu and Kimi China-site availability pages, add MiniMax to Search A, and read the Taiwan and Singapore PDPC pages.
- Licence pages of Kimi K3, DeepSeek V4, GLM-5, Qwen3.8 and MiniMax M3 were checked 18 October (05 folder, Licence Check). Other open-weight rows are marked not reviewed (150 of 277). Confirm each quote on its page.
- Recheck every provider and regulator page just before submission.
- Closed on 18 October 2026: LiteLLM file and licence, FMTI files, AIID export, PCPD PDFs, regulator page addresses (checked by a team member), data quality review, Q6 notebook and chart.

## 10. Standing preferences (how Ian wants Claude to work)

- Write in Traditional Chinese (Taiwan) for chat explanations, and provide English and Traditional Chinese versions of finalized documents.
- No semicolons in documents, in English or Chinese.
- Personas are described by identity and role.
- Never fabricate data. Use "alleged by" for distillation material. Give no VPN or circumvention advice.
- The Assignment 2 folder is read-only. Do not touch security settings.
- No personal email address in code.

## 11. 摘要（繁體中文）

這個專案已把題目從四份舊提案改成一個決策題：在領先的美國閉源模型受限的地方（香港、亞太），組織該選哪個可取得的模型，才能在成本與資料控管需求下得到最高的實測能力。「hedging area」暫時理解為香港與亞太，還需要 Ian 確認。正式文件是 01 最終提案與 02 資料集盤點，各有英文與繁體中文版。我們跑過三輪 Gemini Deep Research，前兩輪品質不夠，所以改用手工建立的 Search A、B、C。第三輪（10 月 18 日）只要求來源線索，我們逐頁自己打開查證，只留下通過的來源，並重新排名資料集。所有文件都已存進這個資料夾，並附上 Markdown 版本。10 月 18 日又完成 notebook 01 到 10、資料品質檢查、Q6 小章節的恢復，並把 01 與 02 文件、圖表與本檔同步（Q4 因 Wikimedia 被刪除而沒有資料來源）。待決定的事項列在第 8 節。

- Dataset licences rechecked 18 October 2026 (see 05 folder, Licence Check): LMArena cc-by-4.0, Wikimedia CC0, Epoch Creative Commons Attribution with no version on the page read, AIID CC BY-SA 4.0 for collections but not the reports text field, submissions or media (terms bar selling or commercially exploiting the site), FMTI repository CC-BY-4.0 unopened, APRA site CC BY 4.0 but our CPG 230 note says CC BY 3.0 AU so keep page-level.
- AIAAIC licence confirmed 18 October 2026 from Ian's screenshot of the aiaaic.org home page: "AIAAIC content is available to use, copy, adapt, and redistribute under a CC BY-SA 4.0 licence." It is not MIT. The "More" link was not read, and the repository data files are still unopened.
- Regulator terms 18 October 2026: HKMA site is not CC, copyright is HKMA's, non-commercial reuse in original unmodified form with attribution is allowed (Para 12), other use needs written consent. MAS Terms of Use of Datasets section (Ian's screenshot) grants a worldwide, perpetual, royalty-free, non-exclusive licence for commercial and non-commercial use, excluding personal data, third-party rights and patents, trademarks and design rights, with no implied endorsement. The general terms for ordinary pages such as FEAT were not seen. Details in 05 Licence Check.
- Files Ian downloaded were opened 18 October 2026 (see 05 Downloaded Files Check). FMTI Dec2025 is CC-BY-4.0 with 100 indicators by 13 developers, context only for Q5. AIID export has Country Code filled for only 143 of 1,734 incidents, 0 for Hong Kong, 4 for China, and almost no Chinese developers (DeepSeek 3, Alibaba 4, Moonshot, Zhipu, MiniMax 0), so Q6 cannot answer the region question. PCPD AI framework PDF (June 2024) is readable. Data folder: Assignment 3\Hedging Region AI Model Selection and Data Risk\Data.
- PCPD PDFs read 18 October 2026: the June 2024 Model Framework (60 pages) and the August 2026 agentic AI supplementary guidance (8 pages, uploaded by Ian) are both CC BY 4.0 with attribution to the PCPD. The open item "PCPD copyright terms unread" is closed for these two files. A team member supplied both PDF addresses on 18 October 2026: https://www.pcpd.org.hk/english/resources_centre/publications/files/ai_protection_framework.pdf (2024 framework) and https://www.pcpd.org.hk/english/resources_centre/publications/files/pcpd_use_of_agentic_ai.pdf (agentic guidance).
