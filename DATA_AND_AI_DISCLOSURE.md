# Data and AI disclosure statement

**Group members:** Yin KAO, Anh Quyen Hoang, Rida Mehboob and Yash Vikas Patil.

## Contributions

- **Yin:** Story 1a, Story 3, Story 1b Views 1 and 3, Story 2 View 2, the current Story 2 View 3 and a basic version of View 1 (made first, because Rida had also worked on View 1), and the shared app that joins all stories. Yin also restyled Story 1b View 2 to the common layout, refreshed all data on 20 Nov 2026 and wrote the root documents.
- **Anh:** the first version of Story 1b View 2 (licence mix by release year). Anh also checked the first 66 of the 91 incident types and a sample of 30 of the first 400 incident labels for Story 3.
- **Rida:** the initial Story 2 submission, including the first GPQA chart (`v3_benchmark.py`), and her own work on View 1. The split of View 1 between Yin and Rida is not certain.

Claude assisted with code, checks and documents as listed under "Use of AI tools".

## Data sources

The app uses only public data. The details of each file are in `DATA_DICTIONARY.md`.

| Source | Organisation | Used in | Licence as recorded in the repository |
|---|---|---|---|
| Epoch Capabilities Index (`eci_scores.csv`) | Epoch AI | Stories 1a, 1b, 2 and 3 | Creative Commons Attribution, version not stated (`docs.md`). CC BY 4.0 in the app's Sources list |
| Epoch AI Benchmarking Hub (`benchmark_data.zip`) | Epoch AI | Story 2 View 2 | CC BY 4.0. Data that Epoch took from external projects keeps its original licence |
| Epoch AI article on self-reported GPQA Diamond scores | Epoch AI | Story 2 View 3 | Not verified for the article's table |
| LiteLLM price file (`model_prices_and_context_window.json`) | BerriAI LiteLLM | Story 1a | MIT, except the `enterprise/` directory |
| LMArena text leaderboard | LMArena (now Arena) | Story 1a | CC BY 4.0 |
| AI Incident Database weekly export | Responsible AI Collaborative | Story 3 View 2 | CC BY-SA 4.0 for the incident collections, checked on the AIID terms of use on 21 Nov 2026. The report text and user submissions are not under that licence and are not used |
| MIT AI Risk Repository risk domains | MIT | Story 3 View 2 | Not read. The labels are used as carried in the AI Incident Database export |
| Foundation Model Transparency Index, December 2025 | Stanford Center for Research on Foundation Models | Story 3 View 1 | CC BY 4.0. The repository holds the Attribution 4.0 International text in `LICENSE.md` and its README says that the data is licensed CC BY |
| Licence pages of open-weight models | Model developers (Hugging Face and GitHub) | Stories 1a and 1b | Read for the group's licence notes. Each page keeps its own terms |

The group's own work is credited to the group and not to any source. It covers the licence class `licence_class_ours`, `licence_terms.json`, the 425 incident labels (343 of them model incidents), the 91 assigned incident types, the incident type grouping and the FMTI company table.

## Personal data

The app uses no personal data. The files describe AI models, companies, licences, benchmark scores and public incident reports. Incident titles and developer names come from the public AI Incident Database.

## Use of AI tools

| Tool | What it was used for |
|---|---|
| Claude | Building and testing the Story 1a changes after A3P1, the Story 1b View 3 matrix, Story 2 Views 2 and 3 and Story 3 Views 1 and 2. Running checks on Story 1b View 2. Reading licence pages with its fetch tool. Reading the licences of the 51 models in `licence_terms.json` on 18 Nov 2026. Reading the incident labels and the 91 incident types of Story 3 (AI assistance, as recorded in `docs.md` of Story 3). Setting the 81 source labels of Story 2 View 2. Refreshing all data sources on 20 Nov 2026, rebuilding the Story 2 Benchmarking Hub tables, extending the incident labels and assigned types to the new incidents of the export of 16 Nov 2026 and updating the page text and documents to the new data. Drafting documentation, including the three root documents on the data dictionary, the provenance matrix and this statement |
| ChatGPT | A first version of the Story 2 GPQA comparison (`v3_benchmark.py`), its CSV and data dictionary. The page no longer calls this module |

Each use is listed with its verification in `AI_PROVENANCE_MATRIX.csv`.

## Review of AI outputs

**Records:** Each AI use and its check are recorded in `AI_PROVENANCE_MATRIX.csv`. The matrix names the member who reviewed each row.

**Date:** 21 Nov 2026.

## Licence readings are not legal advice

The licence classes are Epoch AI's labels and the group's own reading. Some readings were made with AI and reviewed by a member. They are not legal advice. An organisation that deploys any of these models should check the full licence text with its own counsel.
