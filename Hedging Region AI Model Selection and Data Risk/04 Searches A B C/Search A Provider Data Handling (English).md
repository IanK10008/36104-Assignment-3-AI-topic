# Provider Data-Handling Table (Search A)

Oct 16, 2026 · @Ian

## 1. What this table is

This table answers Search A from the Round 2 brief. It records how seven AI providers handle customer data, using only each provider's own policy, terms or documentation pages. It replaces the Voibe tracker, which is a commercial blog page with no reuse terms. The app will use it to code the "data control" weight in Q1 and to support Q5.

The providers are OpenAI, Anthropic, Google, DeepSeek, Alibaba Cloud, Z.ai (Zhipu) and Moonshot AI (Kimi). I read every page on 16 October 2026. Where a page was silent on a point, the table says "not stated" and does not fill the gap from memory. The rows describe the business or API tier unless the row says otherwise, because consumer apps often have different terms. Zhipu and Moonshot each run an international site and a China site with different terms, so each has separate rows.

## 2. Coding scheme

Each row is coded on the fields below. A second person should be able to reach the same code by reading the same page.

| Field | Allowed values | Rule for coding |
|---|---|---|
| training_default | no_by_default, yes_by_default, depends_on_tier, contract_only, not_stated | Code from the provider's own statement about using customer inputs and outputs to train or improve models. If the page is silent, code not_stated. Do not infer it from reputation. yes_by_default means training is allowed by default with no contract route stated. contract_only means training is allowed by default and only a written agreement can restrict it. |
| retention_class | fixed_days, account_lifetime, not_retained, not_stated | fixed_days needs a number of days on the page. account_lifetime means kept while the account is active. not_retained means the page says inputs are not saved. |
| zero_retention_option | yes_on_request, no, not_stated | yes_on_request means the page says a zero data retention arrangement exists, even if approval is needed. |
| storage_location | a stated country or region, or not_stated | Record the place exactly as the page words it. If the page says only where the service is available, code not_stated. |
| region_choice | yes, no, not_stated | yes means the customer can pick a storage or processing region. |
| authority_sharing | clause_present, not_stated, not_checked | clause_present means the page says data may be shared with public authorities. This records that a clause exists. It does not measure how often it is used. not_checked means we did not look for this point on the page. |
| policy_date | a date, or not_shown | Use the effective or last-updated date printed on the page. |
| source_url and date_viewed | link and date | Every row cites the page it was read from and the day it was read. |
| entity_and_governing_law | the company name and the law named, or not_stated, or not_checked | Record the company that signs the terms, the country whose law governs them and where disputes are heard. This shows which legal system the customer contracts under. |

## 3. The table

All pages were read on 16 October 2026. Quoted words are copied from the page, and the China-site pages were read in Chinese, so their quotes are my translations. "Not checked" means we did not look for that point on the page.

| Provider and tier | Training on customer data | Retention | Storage and region choice | Authority sharing | Entity and governing law | Policy date | Sources |
|---|---|---|---|---|---|---|---|
| OpenAI, API | no_by_default. "data sent to the OpenAI API is not used to train or improve OpenAI models" unless you opt in | fixed_days. Abuse-monitoring logs kept up to 30 days, longer if the law requires. Zero retention yes_on_request, with prior approval | Regional storage at rest can be chosen in the US, Europe, Australia, Canada, Japan, India, Singapore, South Korea, the UK and the UAE. The page says regional storage does not imply regional processing. Hong Kong and mainland China are not listed | not_checked | not_checked | not_shown | [Data controls](https://developers.openai.com/api/docs/guides/your-data), [Business data page](https://openai.com/sr-RS/business-data/) |
| Anthropic, commercial API | no_by_default. "Anthropic may not train models on Customer Content from Services" | fixed_days. Inputs and outputs deleted within 30 days by default, up to 2 years if flagged. Zero retention yes_on_request | Location not_stated on the pages read. A data residency option exists but its regions are on a page we did not read | not_checked | not_checked | Terms effective 17 June 2025, retention article dated 1 July 2026 | [Commercial Terms](https://www.anthropic.com/legal/commercial-terms), [Retention article](https://privacy.claude.com/en/articles/7996866-how-long-do-you-store-my-organization-s-data), [API retention docs](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention) |
| Google, Gemini API paid | no_by_default. Google "doesn't use your prompts" or responses to improve its products | Logged for "a limited period of time", days not_stated. Grounding data kept 30 days | "may be stored transiently or cached in any country in which Google or its agents maintain facilities". Access only within an available region | not_checked | not_checked | Last updated 28 April 2026 | [Gemini API terms](https://ai.google.dev/gemini-api/terms_preview) |
| Google, Gemini API unpaid | yes_by_default. Content used to "provide, improve, and develop" Google products, and human reviewers may read it | not_stated | Same as paid | not_checked | not_checked | Last updated 28 April 2026 | [Gemini API terms](https://ai.google.dev/gemini-api/terms_preview) |
| DeepSeek, app and web | not_stated. The policy says data is used to "improve the Services" and no training opt-out was found | account_lifetime. "for as long as you have an account" | "secure servers located in the People's Republic of China". Region choice not_stated | clause_present. Law enforcement and public authorities | not_checked | 15 May 2024 | [Privacy Policy](https://chat.deepseek.com/downloads/DeepSeek%20Privacy%20Policy.html) |
| DeepSeek, Open Platform (API) | not_stated. The terms let the customer use outputs for "training other models" and say nothing about DeepSeek's own use | not_stated | not_stated. The terms refer to the Privacy Policy, and the policy does not name the API | not_checked | Hangzhou DeepSeek Artificial Intelligence Co., Ltd. Mainland PRC law, and disputes go to the court where the company is registered | Effective 29 April 2026 | [Open Platform Terms](https://cdn.deepseek.com/policies/en-US/deepseek-open-platform-terms-of-service.html) |
| Alibaba Cloud, Model Studio | no_by_default. Alibaba Cloud "will never use your data for model training" | not_stated | Storage location not_stated. The service is offered in Beijing, Virginia, Singapore, Tokyo, Frankfurt and Hong Kong, and the customer picks the region | not_checked | not_checked | Last updated 11 October 2026 | [What is Model Studio](https://www.alibabacloud.com/help/model-studio/getting-started/what-is-model-studio), [Privacy notice](https://www.alibabacloud.com/help/en/model-studio/privacy-notice) |
| Z.ai (Zhipu), international API | no_by_default. Terms of Use say "we will not use your User Content for developing or improving Services unless you explicitly agree" for API customers | not_retained for input content ("is not saved on our servers"). Other data stored temporarily, no fixed period | "generally provide the Services from Singapore". Region choice not_stated | clause_present. The company will tell the customer about binding disclosure requests | JINGSHENG HENGXING TECHNOLOGY PTE.LTD. Singapore law, with arbitration in Singapore | Privacy Policy and DPA 29 September 2025, Terms of Use 14 April 2026 | [Privacy Policy and DPA](https://docs.z.ai/legal-agreement/privacy-policy), [Terms of Use](https://docs.z.ai/legal-agreement/terms-of-use) |
| Z.ai (Zhipu), international consumer chat | yes_by_default. "For individual users, we reserve the right to process any User Content to improve our existing Services" | account_lifetime. "as long as you have an account" | Generally Singapore. Data may be transferred outside the user's country | clause_present. Disclosure where required by law | Same as above | Same as above | [Privacy Policy](https://docs.z.ai/legal-agreement/privacy-policy), [Terms of Use](https://docs.z.ai/legal-agreement/terms-of-use) |
| Zhipu Open Platform, China site (bigmodel.cn) | contract_only. The user agreement says Zhipu may use data from your use of the platform to optimise its services unless you agreed otherwise. The privacy policy allows training on anonymised data without separate consent | not_stated. Kept only for "the shortest period necessary" | Stored in mainland China. "At present, we do not transfer or store your personal information across borders" | clause_present. Where law or mandatory government enforcement requires it | Beijing Zhipu Huazhang Technology Co., Ltd. Mainland PRC law, with disputes in a Beijing court | Privacy policy effective 20 May 2025, user agreement effective 4 September 2026 | [Privacy Policy](https://docs.bigmodel.cn/cn/terms/privacy-policy), [User Agreement](https://docs.bigmodel.cn/cn/terms/user-agreement) |
| Moonshot AI (Kimi), OpenPlatform, international site | contract_only. "Unless otherwise expressly agreed in writing, Customer Content may be used" to improve the services | account_lifetime. "retained while your account is active" | "secure servers located in Singapore". Region choice not_stated | clause_present. May share with government authorities | Moonshot AI PTE. LTD. Singapore law, with arbitration in Singapore | Terms 30 July 2026, privacy policy 30 April 2025 | [Terms of Service](https://platform.kimi.ai/docs/agreement/modeluse), [Privacy Policy](https://platform.kimi.ai/docs/agreement/userprivacy) |
| Moonshot AI (Kimi), OpenPlatform, China site (platform.kimi.com) | yes_by_default. Conversation information "helps us optimise models", and no training opt-out is given | not_stated. Kept only as long as necessary for the service | Stored within mainland China. No personal information goes overseas without separate consent and legal compliance | clause_present. Responding to government department instructions needs no consent | Beijing Moonshot AI Technology Co., Ltd. Governing law not stated on the page | Version dated 24 August 2026, effective 31 August 2026 | [Privacy Policy (Chinese)](https://platform.kimi.com/docs/agreement/userprivacy) |

## 4. Caveats and gaps

This table records what each provider says. It does not measure what the provider does. These points need a human check before the team cites any row:

- **Page reader.** I read the pages through a tool that returns extracts, so the quotes come from those extracts. Reopen each page and confirm the wording before you cite it in the assignment.
- **Anthropic wording differs between pages.** The retention article says inputs and outputs are deleted within 30 days by default. The API documentation says conversation content is not retained by default, with 30-day retention for Covered Models. I coded the table from the retention article because it gives the number. Confirm which applies to your use.
- **Google page name.** The Gemini terms page is called "terms_preview" in its address. Confirm that it is the live version.
- **DeepSeek.** The privacy policy dates from May 2024 and never names the API. The API terms refer to that policy. The API rows therefore have many not_stated values. The API terms use mainland PRC law.
- **Alibaba Cloud.** The pages read state the no-training promise, and they do not state where data is stored or for how long. Those details may sit in the International Website Privacy Policy and the Product Terms, which the Related agreements page lists and I have not read.
- **Singapore storage does not settle jurisdiction.** On their international sites Z.ai and Moonshot say their servers are in Singapore and the terms use Singapore law. The pages do not say who can access the data, and each company also runs a China site under mainland law, so do not read Singapore storage as data staying out of China.
- **Authority sharing is only a clause check.** A clause that allows sharing exists in many policies, and the table does not say how often it is used.
- **Tiers differ.** Consumer apps and API services often have different terms. Keep each row's tier in the app.
- **Terms change.** Show the policy date next to each value in the app, and recheck the pages before you submit.

This table does not cover where each provider is available, which is Search C, or the data-protection rules of each jurisdiction, which is Search B.

## 5. Notebook schema

Save the table as a CSV named provider_data_handling.csv in the data folder, with one row per provider and tier. The data-control step of the app joins it to the model tables on the provider column. Keep the policy date and the date viewed, so the app can show how fresh each value is.

| Column | Type | Example |
|---|---|---|
| provider | text | OpenAI |
| tier | text | api, consumer, unpaid, paid |
| training_default | text, one of the allowed values | no_by_default |
| retention_class | text, one of the allowed values | fixed_days |
| retention_days | integer or empty | 30 |
| zero_retention_option | text | yes_on_request |
| storage_location | text | Singapore |
| region_choice | text | yes |
| authority_sharing | text | clause_present |
| policy_date | date or empty | 2026-04-28 |
| date_viewed | date | 2026-10-16 |
| source_url | text | https://ai.google.dev/gemini-api/terms_preview |
| quote | text | the exact words that support training_default |
| site | text | international or china |
| contracting_entity | text | Moonshot AI PTE. LTD. |
| governing_law | text | Singapore |

Load it with pandas.read_csv and check three things before use. Every row has a source_url and a date_viewed. No value falls outside the allowed list in Section 2. The provider names match the names in the model table, so the join drops no rows.
