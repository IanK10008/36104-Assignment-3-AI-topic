# Hedging Region AI Model Selection and Data Risk

36104 Assignment 3 group project. Saved 16 October 2026, updated 18 October 2026 (Gemini Round 3, notebooks 01 to 10, data quality review, Q6 brought back).

Core question (one-sentence version): in regions where leading closed US models are restricted, which accessible AI model gives an organisation the most measured capability for its cost and data-control needs? The original two-part wording is kept in the proposal as an alternative for the group to decide.

Topic: where leading closed US models are unavailable or restricted (Hong Kong, mainland China, Asia-Pacific), which accessible option gives the most measured capability for its cost and data-control needs, and how much does the answer depend on how an organisation weighs those?

Note: "hedging area" was read as Hong Kong and Asia-Pacific. Please confirm.

主題（繁體中文）：在領先的美國閉源模型無法使用或受限的地區（香港、中國大陸、亞太），哪一個可取得的選項在其成本與資料控管需求下，能提供最高的實測能力？答案又有多依賴組織如何權衡這些因素？
註：「hedging area」暫時理解為香港與亞太地區，請確認。

See MEMORY.md for the running record of what we discussed and decided.

## Folder map

| Folder | Contents |
|---|---|
| 01 Final Proposal | Final proposal (English and 繁體中文, .docx and .md): question, personas, value linkage, rationale, views, data quality and difficulty by question, risks. The question-tree diagram is in media-en and media-zh. Synced to the notebooks on 18 October 2026 |
| 01b Alternative Proposal (No Search ABC) | Fallback proposal on the same template if Searches A, B and C are all given up (English and 繁體中文, .docx and .md). Same persona and three stories, core question reworded around self-hosting feasibility, Q7 removed, Q4 dropped, Q5 reworked on FMTI. Choose between 01 and 01b |
| 02 Dataset Usage | Dataset inventory and ranking, 20 candidates re-scored on 18 October 2026 (English and 繁體中文, .docx and .md, landscape). The crosswalk figure is in media-en and media-zh |
| Data | Ten notebooks (01 to 10), one folder each with raw and processed files, plus Data/README.md, Data/raw/README.md and q_charts (first-pass charts for Q1 to Q3, Q5, Q7 and Q8). Start with Data/README.md |
| 03 Deep Research Documentation | Log of every Gemini round and our own searches, what was kept or replaced (English and 繁體中文, .pdf and .md) |
| 04 Searches A B C | Our own web searches: A provider data handling, B data-protection rules by jurisdiction (now with HKMA, APRA and MAS regulator pages, 18 October), C provider availability by country (.pdf, plus .md for the English versions) |
| 05 Gemini Deep Research | Round 1, 2 and 3 briefs, Ian's three Gemini outputs, the Round 3 verification log (English and 繁體中文), three screenshots |

## Markdown files

Each document in folders 01 to 03 has a Markdown copy beside it. In folder 04 only the English Search A, B and C have one, because they are structured coding tables that feed the pipeline CSVs, and Markdown is easy to diff and to read in code. The Chinese Search B and C stay as PDF reading copies. Ask if you want Markdown for those too.

## Live copies (Claude Docs)

| Item | Doc id |
|---|---|
| Final Proposal | 8561508c-bb79-44cd-be52-b607ac20d318 |
| Dataset Inventory and Ranking | 6f452402-46ac-4a6a-8c4e-8e4a3068ac3e |
| Deep Research Documentation | 038954c0-cf81-46ae-bcf9-0a15c6d43a4c |
| Search A | 3b7002b1-1b18-487e-a827-3891201e23c9 |
| Search B | 6ca3e9a3-46dd-43a1-8c0d-bd406d868e47 |
| Search C | 31eae3cc-c885-48b3-9d45-f21d24532783 |
| Round 1 brief | 960cbe86-f030-441c-9704-73b7a8136744 |
| Round 2 brief | b46999cc-531d-49e6-8666-65cdcd04bb34 |

Links: https://claude.ai/code/artifact/<doc id>

## Open decisions

1. Confirm the "hedging area" reading (Hong Kong and Asia-Pacific). The core question names no place, so it holds either way.
1a. Weighting (sliders, defaults, role presets) is optional and deferred. Discuss later.
1b. Choose the question wording. The proposal gives a one-sentence version (recommended, because the brief wants one question in one sentence) and the original two-part version as an alternative. Only one goes in the app README.
2. Check the topic fits the teaching team's question territories.
3. Part 1 recording due date: 23 Oct (brief) or 26 Oct (Canvas header).
4. Which optional chapters to keep. Current order: Q7 availability by place, Q8 capability by licence class. Q6 reported incidents was brought back on 18 October 2026 as a small chapter (confirm). Q4 real-world usage has no data source since Wikimedia page views were struck, so it is dropped unless a source is found.
5. Whether to run another Gemini round. Round 3 (18 October) is in folder 05 and was checked page by page: a few usable sources, no new data file.
6. Closed on 18 October 2026: the FMTI files, the AIID export, both PCPD PDFs (addresses checked by a team member), the LiteLLM file and licence, and the open-weight licence pages. Still open: the MAS general terms text, the Epoch Creative Commons version on the ECI chart page, the first real run of notebook 09, the model crosswalk, the Source column in notebook 07 and the hedging-area confirmation. See MEMORY.md section 9.

## Dataset ranking (re-scored 18 October 2026)

Compulsory: Epoch ECI scores (18), Search A, Search C and LiteLLM prices (17), Epoch benchmark files (16). Optional: LMArena, Epoch per-benchmark CSVs and Stanford FMTI (14), Search B and AI Incident Database (13, included for Q6), regulator pages and Epoch models CSV (12). Dropped: Wikimedia page views (team decision), Stack Overflow, Epoch ChatGPT usage and polling, AIAAIC, data centers, Ember, OWID and IEA. The full 20-row table is in 02 Dataset Usage.

## Question status (18 October 2026)

Q2 and Q8 feasible now. Q7 and Q5 medium. Q6 data ready, small chapter. Q3 needs the Source column and a hand map. Q1 is hardest and needs the model crosswalk. Q4 has no data source. Details in section "Data quality and difficulty by question" of 01 Final Proposal.
