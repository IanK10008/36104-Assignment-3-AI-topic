# Check of the files Ian downloaded, 18 October 2026 / Ian 下載檔案的檢查

Folder: Assignment 3 / Hedging Region AI Model Selection and Data Risk / Data. Claude opened the files after Ian downloaded them by hand. The 115 MB MongoDB backup (backup-20261012101643.tar.bz2) was not opened because the Excel export is enough.

## Stanford FMTI December 2025 (fmti-main.zip) / 可用
- Licence confirmed in the files: LICENSE.md is Creative Commons Attribution 4.0 International, and the README says "All data and visuals are licensed under CC-BY and may be re-used for any purpose with attribution". Cite the Foundation Model Transparency Index and keep the attribution.
- Dec2025/Dec2025_scores.csv: 100 indicators by 13 developers (AI21 Labs, Alibaba, Amazon, Anthropic, DeepSeek, Google, IBM, Meta, Midjourney, Mistral, OpenAI, Writer, xAI). Each cell is 0 or 1. Dec2025_indicators.csv has Domain, Subdomain, Indicator, Definition, Notes and Example disclosure. reports/ has one CSV per developer with Indicator, Definition, Notes, Disclosure, Justification, References and Score.
- Totals out of 100: IBM 95, Writer 72, AI21 Labs 66, Anthropic 46, Google 41, Amazon 39, OpenAI 35, DeepSeek 32, Meta 31, Alibaba 26, Mistral 18, Midjourney 14, xAI 14. Moonshot, Zhipu and MiniMax are not in the index.
- Fit for Q5: the index measures how openly a developer discloses how a model was built and used, not how it treats a customer's data. The closest indicators sit in the Downstream "Usage data" subdomain (for example "Data retention and deletion policy", where only OpenAI scores 1 among six developers we looked at) and in Upstream "Usage data used in training". Use it as context beside our own Search A table, not as a data-handling score.
- 這個指數衡量開發者對模型建置與使用的揭露程度，不是客戶資料的處理方式。最接近的指標在 Downstream「Usage data」（例如資料保留與刪除政策）。只當作 Search A 旁邊的背景，不當成資料處理分數。

## AI Incident Database Excel export, 12 October 2026 / 可用，但對地區問題幫助有限
- Sheets: Incidents (1,734 incidents, 59 columns), Reports (7,920), Entities (7,465), Data Dictionary and Coverage Map. The header row is row 3, so read with header=2.
- Fields we can use at full fill rate: Incident ID, date, year, title, description, deployer, developer, harmed, report_count. Developer and deployer are alleged, so keep "alleged" wording.
- Country: the Country Code column is filled for only 143 incidents (12% in the dictionary, from the CSETv1 taxonomy), and Location Region for about the same. Hong Kong appears 0 times and China 4 times. The US has 91.
- Developers we care about: OpenAI 190 incidents, Google 102, Meta 58, Microsoft 42, Anthropic 39, Alibaba 4, DeepSeek 3, Baidu 3, Tencent 1, Moonshot, Zhipu and MiniMax 0. 790 incidents list more than one developer.
- Consequence: Q6 cannot show incidents by region for Hong Kong or mainland China, and it hardly covers the Chinese developers. It can show incidents by developer for US developers. Keep Q6 optional and either reframe it as incidents by developer or drop it. Do not use the reports text field and do not draw conclusions about region.
- Licence reminder: CC BY-SA 4.0 for the database collections, not the reports text field.

## PCPD AI framework PDF (ai_protection_framework_pcpd_hl.pdf) / 可讀
- The PDF has readable text this time. It is the Artificial Intelligence: Model Personal Data Protection Framework from the Office of the Privacy Commissioner for Personal Data, Hong Kong, dated June 2024 (PDF created 3 June 2024). Part I covers AI strategy and governance, including "Governance Considerations for Procuring AI Solutions", and it targets organisations procuring or using AI.
- Use for Q5 as the Hong Kong reference. It is guidance, not law. Copyright terms read on 18 October 2026 from the last page of the PDF: "licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) licence", free to share and adapt with attribution to the Office of the Privacy Commissioner for Personal Data, Hong Kong. 60 pages.
- 這次 PDF 有可讀文字，是 PCPD（香港個人資料私隱專員公署）2024 年 6 月的 AI 個人資料保障模範框架，針對採購或使用 AI 的機構，屬於指引而非法律。版權條款已讀（2026 年 10 月 18 日，PDF 最後一頁）：CC BY 4.0，須標示 PCPD 為來源。共 60 頁。

## PCPD agentic AI guidance (pcpd_use_of_agentic_ai.pdf) / 可讀，是另一份文件
- Uploaded by Ian and read by Claude on 18 October 2026. It is a different document from the June 2024 framework above: "Artificial Intelligence: Model Personal Data Protection Framework — Protecting Personal Data Privacy in the Use of Agentic AI", 8 pages, dated August 2026 (PDF created 13 August 2026). It says it is supplementary guidance to the Model Framework, which "remains generally applicable to the use of agentic AI".
- Licence on the last page: Creative Commons Attribution 4.0 International (CC BY 4.0), attribute to the Office of the Privacy Commissioner for Personal Data, Hong Kong. Supporting organisations named: the Digital Policy Office of the HKSAR Government and the Hong Kong Applied Science and Technology Research Institute.
- Content that matters for us: AI agents are not legal persons, so the organisation stays the data user and answerable under the PDPO and its six Data Protection Principles. It lists risks (extensive access, system vulnerabilities, vulnerable plugins or skills, function creep, multi-agent risks) and recommends retention limits, avoiding third-party or outdated versions of agentic AI, contract terms with external vendors on retention (DPP 2) and security (DPP 4), staff training, and a Security Checklist in Annex A. This bears on the earlier question about tools such as OpenClaw: a wrapper or agent built on another model is still the organisation's responsibility under this guidance.
- Use for Q5 as a second Hong Kong reference. Guidance, not law.
- 這是與上面不同的另一份文件：PCPD 2026 年 8 月發布的「代理式 AI（agentic AI）」補充指引，共 8 頁，授權 CC BY 4.0，須標示 PCPD。重點：AI 代理人不是法律主體，機構仍是資料使用者，須依 PDPO 六項保障資料原則負責，並建議限制保留期間、避免第三方或過時版本、與外部供應商簽約規範保留與安全、訓練員工，附錄 A 有安全檢查表。屬指引而非法律。

## APAC_Enterprise_AI_Model_Research.docx
Already in the folder as Gemini Round 3 output and verified in the Round 3 Verification Log. Not rechecked here.

## Source links / 來源連結
Where each file came from, and the page that states its licence. Addresses were added on 18 October 2026. Where we hold only a file name, the address is marked as matched by file name or by search and should be confirmed.
各檔案的來源與載明授權的頁面。網址於 2026 年 10 月 18 日補上。只有檔名時，網址是依檔名或搜尋比對，需要再確認。

| File | Source page | Licence or terms page |
|---|---|---|
| fmti-main.zip (Stanford FMTI Dec2025) | Results page https://crfm.stanford.edu/fmti/December-2025 and repository https://github.com/stanford-crfm/fmti (the zip is named like the GitHub archive of the main branch, confirm) | LICENSE.md inside the zip, CC BY 4.0. Licence text https://creativecommons.org/licenses/by/4.0/ |
| FMTI 2025 paper.pdf | https://crfm.stanford.edu/fmti/December-2025/paper.pdf (linked from the FMTI results page) | Not read |
| AIID_Excel_Export-20261012.xlsx (AI Incident Database) | Snapshots page https://incidentdatabase.ai/research/snapshots/ , file https://pub-72b2b2fc36ec423189843747af98f80e.r2.dev/AIID_Excel_Export-20261012.xlsx (weekly, on Mondays) | Terms of use https://incidentdatabase.ai/terms-of-use (CC BY-SA 4.0 for the snapshot collections, not for submissions, report text or media) |
| backup-20261012101643.tar.bz2 (AIID database backup) | Same snapshots page , file https://pub-72b2b2fc36ec423189843747af98f80e.r2.dev/backup-20261012101643.tar.bz2 (weekly backups, 2021-03-29 to 2026-10-12) | Same terms. The snapshots page itself states no licence and links to the terms. Not opened |
| ai_protection_framework_pcpd_hl.pdf (PCPD Model Framework, June 2024) | PDF address https://www.pcpd.org.hk/english/resources_centre/publications/files/ai_protection_framework.pdf (supplied by a team member on 2026-10-18). PCPD AI page https://www.pcpd.org.hk/english/artificial_intelligence/index.html | CC BY 4.0, stated on the last page of the PDF |
| pcpd_use_of_agentic_ai.pdf (PCPD agentic AI guidance, August 2026) | https://www.pcpd.org.hk/english/resources_centre/publications/files/pcpd_use_of_agentic_ai.pdf (supplied by a team member on 2026-10-18) | CC BY 4.0, stated on the last page of the PDF |
