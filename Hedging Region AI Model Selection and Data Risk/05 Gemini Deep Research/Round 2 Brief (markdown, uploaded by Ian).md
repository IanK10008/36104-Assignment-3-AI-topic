# Deep Research Brief Round 2: Corrections and Rework

Oct 15, 2026 · @Ian

## 1. What we need from this round

This is a follow-up to the first brief, "Deep Research Brief: AI Model Choice Where Closed US Models Are Restricted". Your Round 1 report gave us useful leads, but our team opened every page you cited and found errors that stop us using it as written. The headline question, the personas and the source rules from the first brief still apply. Please do three things:

1. Correct each Round 1 dataset using the verdicts in Section 2 and the instructions in Section 3.
2. Search again for the gaps that Round 1 missed or got wrong, as listed in Section 4.
3. Return the result in the same format as before, under the stricter rules in Section 5 and with the self-check in Section 6.

The errors fall into four kinds. Some descriptions of files did not match the page (columns, contents, row counts). Some download links were guessed and not opened. Some licences were assumed or paraphrased instead of quoted. Some citations pointed to the wrong or an unrelated page. We would rather have three datasets that are fully verified than ten that we must check again.

## 2. Verdicts on the Round 1 datasets

Our team opened each of these pages on 15 October 2026. The right-hand column states what we saw, so please compare it with your own notes and correct yourself where we differ. If you believe we are wrong, show the page text that proves it.

| Dataset from Round 1 | Verdict | What we found on the page |
| --- | --- | --- |
| LiteLLM price file (model\_prices\_and\_context\_window.json) | Keep | The file exists on GitHub at BerriAI/litellm. It is about 47,000 lines and 1.64 MB, not the 2.65 MB you stated. We saw current prices only and found no price history. We did not confirm the MIT licence from the repository's licence file. |
| LMArena leaderboard dataset (lmarena-ai/leaderboard-dataset) | Keep, fix the details | It exists and the page shows the tag cc-by-4.0. It has 23 subsets and two splits, full and latest, and the latest snapshot is dated 2026-10-14. The columns are rating, rating\_lower, rating\_upper, variance, vote\_count and rank. There is no elo\_rating, win\_rate or votes column, and the page did not show your parquet URL. |
| Stack Overflow Developer Survey | Keep, fix the source | The survey site states "Survey data licensed under ODbL 1.0, contents under DbCL 1.0". Raw data sits in GitHub folders by year (StackExchange/Survey, packages/archive/YEAR) from 2011 to 2026. Your 2024 link was not found, and the sources you cited for this entry were unrelated pages. We did not see the country values. |
| Stanford FMTI indicators file (fmti-indicators.csv) | Fix | The file exists with 101 lines. The columns are Domain, Subdomain, Indicator, Definition, Notes, Reference\_1, Reference\_2, Link\_1 and Link\_2. It holds indicator definitions, not scores per developer, so your Developer\_Score field and developer-column matrix do not exist in it. The page shows no licence. |
| JailbreakBench JBB-Behaviors | Drop for Q6 | The dataset is real and tagged MIT. It holds 100 harmful and 100 benign behaviours (Goal, Target, Behavior, Category, Source) and a judge\_comparison subset of 300 rows. It has no attack success rate per model. The page says those results sit on a separate leaderboard. |
| LiveBench (livebench/coding) | Drop | The page shows 128 question rows and 15 columns, with no model scores and no licence tag. The card calls the data instruction\_following while the rows say coding. Scores sit on livebench.ai, which we have not checked. |
| Open LLM Leaderboard contents | Context only | The dataset has 4.58k rows and 36 columns, including "Average", "MMLU-PRO", Architecture and Flagged. It has no GSM8K or plain MMLU column. The organisation page shows it last updated on 20 March 2025, and the dataset has no licence tag. Only a per-model Hub License column exists. |
| Artificial Analysis AA-Briefcase-Lite | Drop | The page is real and tagged Apache-2.0, but it is a sample scenario for an agentic knowledge-work evaluation (a fictional egg producer, 4 tasks, 63 rubric checks in checks.jsonl). It holds no latency, throughput, price or quality-index data. |

## 3. Rework instructions for each dataset

Redo the full set of tables for every dataset below (summary, source record, fields and notebook note) using only facts from pages you open. Where the page does not show something, write "not shown on the page" and do not fill the gap from memory.

| Dataset | What to redo |
| --- | --- |
| LiteLLM price file | Quote the licence text from the repository's licence file and link it. State the file size and line count as shown on the page. Say whether the file holds only current prices or also dated history. Look for an open source of price history, such as dated snapshots, and say whether its terms allow reuse. Name the providers in the file that are regional hosts, and show the entries as evidence instead of asserting it. |
| LMArena leaderboard dataset | List the subsets and say which one holds the main text leaderboard. Give the real column names. Give a load call that you opened and checked, using the Hugging Face datasets library with the config and split names, or a parquet path you saw on the Files tab. Quote the licence tag. Show how model names are written, with a few examples, so we can match them to Epoch's model names. |
| Stack Overflow Developer Survey | Give the GitHub folder for the newest year and the file names and sizes in it. Quote the licence text. Give the exact column names for AI tool use and country. List the exact country strings for Hong Kong, mainland China, Taiwan and Singapore, or say they are absent. Say whether the newest survey asks more AI-tool questions than the 2024 one. |
| Stanford FMTI | Find where the per-developer scores for the December 2025 index are published. This may be a folder in the repository, an appendix of the paper or a page on the site. Give the file or page URL you opened, the columns, and which of the 13 developers it covers. Quote the licence, or say "not stated". Say how developer names are written, so we can match them to Epoch's Organization field. |
| JailbreakBench | Do not propose JBB-Behaviors for Q6. Find where per-model attack success rates are published as downloadable data, if anywhere, and give the licence. If they are not downloadable, say so. Then search for other open safety or robustness evaluations that report a score per model. |
| LiveBench | Do not propose the Hugging Face coding page. Check whether livebench.ai publishes model scores as a downloadable file, and quote its licence and terms. If scores exist only on a web page with no stated reuse terms, reject it and say why. |
| Open LLM Leaderboard | Keep it as context only. Correct the columns and the last update date, remove the CC BY claim, and state that it covers open-weight models only and stops at its last update. |
| Artificial Analysis | Reject AA-Briefcase-Lite for this purpose. Check whether Artificial Analysis publishes price, latency or throughput data under terms that allow reuse, and quote those terms. If it needs a key or forbids reuse, say so and reject it. |

## 4. New searches

Round 1 found nothing for the data-protection and availability gaps and little for data handling. Please search these areas in this order. Each one should end with either a verified dataset or a clear statement that you opened the likely sources and found nothing usable.

| Search | What we need | Where to look |
| --- | --- | --- |
| A. Data-handling practices by provider | Structured fields such as data retention, training on user data, hosting region and opt-out terms, covering Chinese and other non-US providers as well as US ones | Academic or civil-society audits of provider privacy terms, open datasets of AI provider policies, and the sub-scores of transparency indices |
| B. Data-protection rules by jurisdiction | Cross-border transfer and localisation rules for Hong Kong, mainland China, Singapore and Taiwan as structured fields, not PDFs | Regulator publications, official legal portals and open legal datasets. Quote the licence or reuse terms of each |
| C. Provider availability by country | Which countries each major AI provider supports, with the date of each record, so we can code availability and show when it changed | The providers' own supported-countries pages, dated archive snapshots and academic work on AI access restrictions. Record the date you viewed each page |
| D. Price history | Dated price per token by model, to replace the cost axis if the LiteLLM file holds current prices only | Open price trackers or dated snapshots whose terms permit reuse |
| E. Security scores per model | A downloadable score per model for jailbreak or safety robustness, covering open and closed models | Open evaluations that publish per-model results as files |
| F. Independent benchmark scores | Per-model scores from an independent evaluator, with developer, date and country, to support Q3 | Held-out or contamination-controlled evaluations that publish data with stated terms |

## 5. Tightened rules for sources

All the Round 1 rules still apply, including no circumvention advice, coverage of Hong Kong, mainland China, Singapore and Taiwan, and no invented figures. These rules are added or sharpened:

1. **Primary sources only.** Drop blogs, news summaries, aggregator sites, forum threads, tutorials and any page that repeats another source's data. You may use a second-hand page to find the primary one, but never cite it as the source of a number or a licence.
2. **Drop irrelevant sources.** Cite a page only if it directly concerns AI models, providers, benchmarks, data protection or AI usage. Your Round 1 list of cited works included a Python guide, a framework comparison and a sprint-estimation article, and none of them belongs in this research.
3. **Drop low-quality data.** If a dataset is unmaintained, undated, a sample or demo, has no documented method, or holds opinions and not measurements, do not shortlist it. List it under rejected with the reason.
4. **Open every URL you give.** Do not guess file paths. If you did not open a file or page, write "not opened" and do not present it as a link to load.
5. **Quote the licence text exactly, or write "not stated".** Phrases such as "public open access" and "open data" are not licences. A licence from a third-party summary does not count. It must come from the publisher's own page or licence file.
6. **Describe only what you saw.** Take columns, row counts, file sizes and dates from the page. Where the page does not show a detail, write "not shown on the page".
7. **Make each citation support its own claim.** Do not cite a page about something else, and remove any leftover markers such as \[cite: 12\] in favour of readable links.
8. **Label code honestly.** Mark any snippet you did not run as untested, and use the exact column names you saw.

## 6. Requested output

Return the report in this order. Keep the table formats from the first brief and do not pad.

1. A short correction log. For each of the eight Round 1 datasets, say what you changed, what you dropped and why, in one or two sentences.
2. A ranked shortlist of up to eight verified datasets. Fewer is better if the rest cannot be verified. Each one gets the summary table, the source record table, the fields table, the notebook extraction note and a pros, cons and limitations note.
3. For searches A to F in Section 4, one line each saying what you found or that you found nothing usable, followed by the datasets, if any.
4. Three lists: use first, context only, and rejected with the reason. Put low-quality and second-hand sources in the rejected list.
5. The verification log described below, then the pages you opened as readable links, and a list of anything you could not open, marked unverified.

**Pros, cons and limitations.** For every dataset or source, add a short note in three parts. Pros are what makes it useful for our headline question. Cons are what makes it weak or risky to use. Limitations are coverage gaps, bias, how the data was collected, reuse terms, how fresh it is, and anything else that could stop us using it. Give at least two points in each part, and base each point on something you saw on the page and not on the source's general reputation.

**Verify it yourself before you send it.** After your first draft, do a second pass. Reopen every dataset page and file listing, compare each statement in your report with the page, and correct or delete anything that does not match. Then add a verification log with one row per dataset and these columns: the dataset, the pages you reopened (URL and date), the statements you confirmed, the statements you corrected or removed, and what is still unverified. We will spot-check your log against the pages, so do not mark a statement as confirmed unless you saw it on the page.

Before you send the report, check each dataset against this list and fix any failure:

- Every URL was opened and every file path appears on a page you saw.
- The licence is quoted from the publisher's own page, or marked "not stated".
- Columns, row counts and sizes match the page.
- Each citation supports the claim next to it.
- No blog, aggregator or tutorial is cited as the source of a number.
- Code is marked tested or untested.
- The dataset covers at least some of our regions, or the report says it does not.
- Every dataset has a pros, cons and limitations note based on what you saw.
- You reopened every page in a second pass and completed the verification log.
