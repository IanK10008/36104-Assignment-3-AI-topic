# Licence check for open-weight models and LiteLLM, 18 October 2026

Checked by Claude on 18 Oct 2026 from the Hugging Face and GitHub pages named below. Our fetch tool summarises each page, so every quote should be re-read once on the page before it goes into a graded document. Gemini's links were not used because several were malformed or pointed to a non-official account (Kimi link with a space, DeepSeek link under https://github.com/glmnes).
Claude 於 2026 年 10 月 18 日依下列 Hugging Face 與 GitHub 頁面檢查。抓取工具會先摘要頁面，所以每段引文放進正式文件前，請再到原頁面讀一次。Gemini 的連結沒有採用，因為多個連結格式錯誤或指向非官方帳號。

| Model | Page opened | Licence shown | Commercial use rule found | Status |
|---|---|---|---|---|
| Kimi K3 | https://huggingface.co/moonshotai/Kimi-K3 and its LICENSE file | "Kimi K3 License", copyright 2026 Moonshot AI | If the licensee or an affiliate runs a Model as a Service business and aggregate revenue exceeds US$20 million in any 12 months, a separate agreement is needed before commercial use. Branding "Kimi K3" required for products above 100 million monthly users or US$20 million monthly revenue. Internal use (no access for third parties to the software, its outputs or capabilities) and use through Moonshot's official products or certified partners are exempt from Sections 2 and 3 | Verified, corrected after cross-check |
| DeepSeek V4 (V4-Pro) | https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro and its LICENSE file | MIT License, copyright 2023 DeepSeek. Page text: "This repository and the model weights are licensed under the MIT License" | No restriction beyond MIT. Gemini's "custom model agreement with patent clause" is not supported by this page | Verified, Gemini wrong |
| GLM-5 | https://huggingface.co/zai-org/GLM-5 | "License: mit" | MIT. Our tool could not load the LICENSE file page. Ian checked the repository himself and reports no further licence document, only the standard MIT licence (Ian's observation, not opened by Claude) | Page field verified, standard MIT per Ian |
| Qwen3.8-2.4T-A95B (Max) only | https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B and its LICENSE file | "Qwen3.8-Max License" (licence field qwen3.8-max). Other versions differ: Qwen3.8-27B is Apache License 2.0, Qwen3.8-Flash-Next is Qwen Community License 1.0 (separate licence needed for Model as a Service or AI Work Assistant businesses, no revenue figure in that clause) | Clause 1: model name must be shown for products above 100 million monthly users or US$20 million monthly revenue. Clause 2: a Model as a Service or AI Work Assistant business with over US$50 million revenue in 12 months needs a separate licence. The internal-use exemption sits at the end of clause 2 and exempts only the separate-licence requirement, not the clause 1 display rule. Gemini's "Apache-2.0 for weights" is not what this page shows | Verified from the page |
| MiniMax M3 | https://huggingface.co/MiniMaxAI/MiniMax-M3 and its LICENSE file | "MINIMAX COMMUNITY LICENSE" | Display "Built with MiniMax M3". Above US$20 million yearly revenue a separate prior written authorisation is needed (email api@minimax.io, subject "M3 licensing - authorization request"). At or below it a one-time notice is still required (subject "M3 licensing — notice"), so commercial use is never contact-free. Appendix lists prohibited uses including any military purpose | Verified from the page |
| LiteLLM | https://github.com/BerriAI/litellm/blob/main/LICENSE | "Portions of this software are licensed as follows" | MIT for all content except the enterprise/ directory, which has its own licence. Our use is the price JSON, not enterprise code | Verified, with the enterprise exception |

## What this means for Q8
- Four of five models allow commercial use with conditions that do not stop an internal bank deployment. Kimi K3 exempts internal use from its Sections 2 and 3. Qwen3.8-Max exempts internal use from the separate-licence clause only. MiniMax M3 counts commercial use as primarily for commercial advantage, so a bank must read Section 3 and the military-purpose ban with its own legal team.
- DeepSeek V4 and GLM-5 are MIT on the pages checked. Per Ian, GLM-5 has no licence document beyond standard MIT, which Claude did not open itself.
- The price JSON in LiteLLM sits at the repository root, so it falls under MIT. A second tool (Perplexity, brought by Ian) was cross-checked against the pages on 18 Oct 2026 and agreed except where corrected above.
- Q8 classes should therefore be: MIT, custom licence with revenue or user thresholds, and API only.
- This is not legal advice. Check the full licence text with the bank's counsel before any deployment claim.

## 對 Q8 的意義
- 五個模型中有四個允許商用，但附帶條件。Kimi K3 與 Qwen3.8 豁免內部使用。MiniMax M3 對商用的定義較廣，並禁止軍事用途，需要法務自行判讀。
- DeepSeek V4 與 GLM-5 在已檢查的頁面上是 MIT。
- 因此 Q8 的分類建議為：MIT、附營收或用戶門檻的自訂授權、僅限 API。
- 這不是法律意見，實際部署前請法務檢查完整條文。

## Mismatch with Epoch's labels / 與 Epoch 標籤的落差
- Epoch's ECI file labels Kimi K3 as open weights non-commercial, but the Kimi K3 License we read allows commercial use with a Model as a Service revenue condition and exempts internal use. Q8 should classify by the licence text and show Epoch's label beside it. Epoch's label may rest on an older licence, so check before saying Epoch is wrong.
- Epoch 把 Kimi K3 標為「開放權重、非商用」，但我們讀到的 Kimi K3 License 允許商用，只對 MaaS 營收設條件，內部使用豁免。Q8 應依授權文字分類，並把 Epoch 的標籤並列。Epoch 的標籤可能依據舊版授權，所以說 Epoch 錯之前要先確認。

## What MIT means / MIT 的意思
Reference pages opened on 18 Oct 2026: https://choosealicense.com/licenses/mit/ and https://huggingface.co/datasets/choosealicense/licenses/blob/main/markdown/mit.md. MIT permits commercial use, distribution, modification and private use. The only condition is to keep the copyright and licence notice, and the software comes without warranty. These pages describe MIT in general and are not the GLM-5 or DeepSeek files themselves.
MIT 允許商用、散布、修改與私人使用，唯一條件是保留版權與授權聲明，且軟體不附保證。這兩個頁面說明的是 MIT 的一般內容，不是 GLM-5 或 DeepSeek 本身的授權檔。

## Second check, 18 October 2026 / 第二次檢查
- Kimi K3 was read again on GitHub (https://github.com/MoonshotAI/Kimi-K3/blob/main/LICENSE) and matched the Hugging Face text: five numbered provisions, MaaS revenue condition over US$20 million in any 12 months, attribution above 100 million monthly users or US$20 million monthly revenue, internal-use exemption in Section 4. Two secondary write-ups (Simon Willison, Context Studios) describe the same conditions and neither calls it non-commercial.
- Epoch's own definitions (https://epoch.ai/blog/open-models-report, Table A1): "restricted use" means a licence that limits things like user counts or permitted purposes, "non-commercial" means a licence that does not allow commercial use, and a missing or unclear licence also falls under non-commercial. By these definitions Kimi K3 fits "restricted use", not "non-commercial". The ECI label for Kimi K3 is likely out of step with the licence text, or it rests on an older licence. Q8 should use our class from the licence text and show Epoch's label beside it.
- Kimi 授權已在 GitHub 上再讀一次，與 Hugging Face 的內容一致。兩篇第二手文章也描述了相同條件，且都沒有稱它為非商用。
- Epoch 自己的定義：「受限使用」是授權對用戶數或用途設限，「非商用」是授權不允許商用，沒有授權或授權不明也歸入非商用。依這個定義，Kimi K3 應屬於「受限使用」，不是「非商用」。所以 ECI 檔裡的標籤很可能與授權原文不符，或是依據舊版授權。Q8 要用我們依授權原文的分類，並把 Epoch 的標籤放在旁邊。

## Dataset licences rechecked, 18 October 2026 / 資料集授權重新檢查
| Dataset | Page opened | Licence found | Note |
|---|---|---|---|
| LMArena leaderboard dataset | https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset | Licence field "cc-by-4.0". Columns for text subsets: model_name, organization, license, rating, rating_lower, rating_upper, variance, vote_count, rank, category, leaderboard_publish_date | Verified |
| Wikimedia pageviews | https://dumps.wikimedia.org/other/pageviews/readme.html and the Analytics API access policy | "All Analytics datasets are available under the Creative Commons CC0 dedication." The API page says its data is under CC0 1.0 and requires a User-Agent header | Verified |
| Epoch AI data | https://epoch.ai/data | Free to use, distribute and reproduce "provided the source and authors are credited" under a Creative Commons Attribution licence | The page read does not state a version number. We wrote CC BY 4.0 earlier, so confirm the version on each dataset page |
| AI Incident Database | https://incidentdatabase.ai/terms-of-use | Collections incidents, quickadd, duplicates, taxa, classifications, entities and entity_relationships are CC BY-SA 4.0. Not licensed: submissions, the reports "text" field and displayed media. Terms also say "You are not allowed to sell or commercially exploit any aspect of the Site without express permission of RAIC" | Verified. Use only the snapshot collections, share-alike applies to our output of those fields. The snapshots page itself has no licence text, only a terms link |
| Stanford FMTI | https://crfm.stanford.edu/fmti/December-2025 | The results page has no licence sentence. The repository (https://github.com/stanford-crfm/fmti) was earlier read as CC-BY-4.0 | Repository files unopened, our tool is blocked |
| APRA CPG 230 | https://apra.gov.au/copyright | Site-wide: "All material presented on this website is provided under a Creative Commons Attribution 4.0 International licence". Our Search B recorded CC BY 3.0 Australia for the CPG 230 page | The two differ, so keep the page-level licence and cite © Australian Prudential Regulation Authority 2024 as APRA asks |
| LiteLLM | https://github.com/BerriAI/litellm/blob/main/LICENSE | MIT, enterprise/ excluded | Verified, price JSON is at the repository root |

Not rechecked: HKMA and MAS page terms, AIAAIC (blocked, secondary source only).

## Regulator site terms, 18 October 2026 / 監管機關網站條款
- HKMA (https://hkma.gov.hk/eng/other-information/terms-and-conditions-of-use/): the HKMA owns the copyright. Paragraph 12 allows non-commercial use: display, download, reproduce and print in the original format, reproduced accurately without modification, with clear attribution to the HKMA and the website. Uses beyond that, and linking, need the HKMA's prior written consent (Paragraph 13). Names and logos may not be used to imply endorsement. For us: cite and link, describe the rule in our own words, do not alter or re-present its text as ours. This is a university project, so the non-commercial permission fits, but it is not a Creative Commons licence.
- MAS (https://mas.gov.sg/terms-of-use): the page did not load for our tool, so its terms are unverified. Ian to read it in a browser.
- HKMA 條款：版權屬 HKMA，第 12 段允許非商業用途（原格式顯示、下載、複製、列印，不得修改，須清楚標明來源），其他用途與連結需事先書面同意。我們的做法是引用並附連結，用自己的話描述規則，不改動或冒充原文。這不是 Creative Commons 授權。
- MAS 條款：頁面無法載入，未查證，請 Ian 用瀏覽器閱讀。
