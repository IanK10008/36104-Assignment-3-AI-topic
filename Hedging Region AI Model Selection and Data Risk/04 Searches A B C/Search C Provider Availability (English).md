# Provider Availability by Country (Search C)

Oct 16, 2026 · @Ian

## What this answers

This table records, provider by provider, whether the official page says Hong Kong, mainland China, Singapore and Taiwan are supported. It is the evidence behind the word "unavailable or restricted" in Q1. Every row links to the page it came from and shows the date the page was viewed. A Traditional Chinese version is in the second tab.

## Coding scheme

- **supported**: the place appears in the provider's official supported list for that product.
- **not_listed**: the provider publishes a list and the place is absent. This means "not on the list", not proof of a technical block.
- **excluded_stated**: a page says in words that the place is excluded or that service is not offered there.
- **no_list_found**: no official country list was found. Availability is unknown, not assumed.
- **Scope**: API or developer platform only. Consumer chat apps often follow different rules and are noted separately.
- **Dates**: page last-updated date where the page shows one, otherwise "none shown", plus the date I viewed it (2026-10-16).

## Availability table

OpenAI, Anthropic and Google publish country lists. Hong Kong and mainland China are absent from all three, while Singapore and Taiwan are on all three. The five China-linked providers publish no country list, so their cells stay "no_list_found" rather than a guess.

| Provider and product | Hong Kong | Mainland China | Singapore | Taiwan | Other notes | Page date (viewed 2026-10-16) | Sources |
|---|---|---|---|---|---|---|---|
| OpenAI API | not_listed | not_listed | supported | supported | Macau also absent. The old platform.openai.com address redirects (HTTP 302) to the new page. | none shown | [OpenAI supported countries](https://developers.openai.com/api/docs/supported-countries) |
| Anthropic API and Claude | not_listed | not_listed | supported | supported | Macau also absent. Ukraine is listed with named regions excluded. | none shown (footer copyright 2026) | [Anthropic supported countries](https://www.anthropic.com/supported-countries) |
| Google Gemini API | not_listed | not_listed | supported | supported | The page points unlisted regions to a Google enterprise cloud route. Not checked further, see caveats. | last updated 2026-04-28 UTC | [Gemini API available regions](https://ai.google.dev/gemini-api/docs/available-regions) |
| DeepSeek Open Platform API | no_list_found | no_list_found | no_list_found | no_list_found | Section 1.4 gives no warranty that the service is available in certain jurisdictions. Sanctions clause names no places. | effective 2026-04-29 | [DeepSeek Open Platform Terms](https://cdn.deepseek.com/policies/en-UK/deepseek-open-platform-terms-of-service.html), [DeepSeek API docs home](https://api-docs.deepseek.com/) |
| Alibaba Cloud Model Studio | no_list_found | no_list_found | no_list_found | no_list_found | Offers a China (Hong Kong) deployment region and a Singapore region. FAQ says all models can be called from mainland China. Each region has its own endpoint and API key. | none shown | [Model Studio regions](https://www.alibabacloud.com/help/en/model-studio/regions.md) |
| Z.ai API (international) | no_list_found | no_list_found | no_list_found | no_list_found | Terms exclude Iran, North Korea, Cuba, Crimea, Donetsk and Zaporizhzhia. Hong Kong and mainland China are not named. | terms dated 2026-04-14 | [Z.ai Terms of Use](https://docs.z.ai/legal-agreement/terms-of-use.md), [Z.ai docs overview](https://docs.z.ai/guides/overview/overview) |
| Kimi open platform (international) | no_list_found | no_list_found | no_list_found | no_list_found | Section 13 bars use in countries under comprehensive sanctions. No place is named. | last updated 2026-07-30 | [Kimi platform terms](https://platform.kimi.ai/docs/agreement/modeluse) |

## Caveats

- **Not on the list is not the same as blocked.** The pages say where service is offered. They do not say how a provider enforces it, for example by IP address or payment country. Test access on your own account before any claim.
- **Page text came from a page reader.** Each fetch returned a model-written extract of the page, not the raw page. Anthropic's country list and the OpenAI list were read this way, so check them by eye before quoting.
- **Two providers show no date.** OpenAI and Anthropic pages show no last-updated line, so the only date is my viewing date.
- **The Google page mentions an enterprise route for unlisted regions.** I did not open it, so I make no claim about whether it works in Hong Kong.
- **China-site products are not covered.** Zhipu bigmodel.cn and Kimi platform.kimi.com are separate China services. I did not check who can sign up.
- **Cloud resellers are not covered.** Whether the same models are reachable through a cloud provider's Hong Kong or Singapore region is a separate search.
- **Terms change.** Several of these pages changed during 2026, so re-check each one before submission.

## CSV schema (provider_availability.csv)

```csv
provider,product,site,place,status,page_date,date_viewed,source_url,quote,note
OpenAI,API,international,Hong Kong,not_listed,,2026-10-16,https://developers.openai.com/api/docs/supported-countries,,place absent from list
OpenAI,API,international,Singapore,supported,,2026-10-16,https://developers.openai.com/api/docs/supported-countries,Singapore,
Google,Gemini API,international,Taiwan,supported,2026-04-28,2026-10-16,https://ai.google.dev/gemini-api/docs/available-regions,Taiwan,
```

One row per provider, product and place. Allowed status values: supported, not_listed, excluded_stated, no_list_found. Leave page_date empty when the page shows none.

## References (all opened on 2026-10-16)

1. OpenAI, Supported countries and territories: https://developers.openai.com/api/docs/supported-countries (redirected from https://platform.openai.com/docs/supported-countries)

2. Anthropic, Supported countries and regions: https://www.anthropic.com/supported-countries

3. Google, Gemini API available regions (last updated 2026-04-28 UTC): https://ai.google.dev/gemini-api/docs/available-regions

4. DeepSeek, Open Platform Terms of Service (effective 2026-04-29): https://cdn.deepseek.com/policies/en-UK/deepseek-open-platform-terms-of-service.html

5. DeepSeek, API docs home (no country wording found): https://api-docs.deepseek.com/

6. Alibaba Cloud, Model Studio regions: https://www.alibabacloud.com/help/en/model-studio/regions.md

7. Z.ai, Terms of Use (export control section dated 2026-04-14): https://docs.z.ai/legal-agreement/terms-of-use.md

8. Z.ai, docs overview (no country wording found): https://docs.z.ai/guides/overview/overview

9. Kimi open platform, Terms (last updated 2026-07-30): https://platform.kimi.ai/docs/agreement/modeluse
