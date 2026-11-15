# V3 dataset data dictionary

**File:** `data/raw/epoch_article_gpqa_table.csv` (versioned source transcription) → `data/processed/gpqa_reported_vs_epoch.csv` (app input)

**Primary source:** https://epoch.ai/data-insights/self-reported-gpqa (Jaeho Lee and Yafah Edelman, 19 September 2025), including cited model-developer disclosures. **Last observation:** curated frontier model selection through 2025 (not a time series; exact model-specific dates not all included in this summary). **Downloaded / transcribed:** 14 November 2026. **Licence:** Not verified for this webpage's derived comparison table; attribution is provided, but reuse permissions must be checked with Epoch before publishing a repackaged dataset. This is not the same as the separate ECI dataset's claimed CC Attribution licence.

**Primary key:** `model` (unique display names in this curated eight-row table).

| Column | Meaning | Unit |
|---|---|---|
| model | Model display name | text |
| developer_reported_pct | Published developer or third-party-endorsed score | % correct on GPQA Diamond |
| epoch_independent_pct | Epoch-run standardized GPQA estimate | % correct on GPQA Diamond |
| epoch_standard_error_pp | Standard error of independent estimate | percentage points |
| epoch_90ci_halfwidth_pp | Epoch approximate 90% interval half width | percentage points |
| developer_report_type | developer_report or third_party_endorsed | category |
| source_page | Epoch article containing comparison | URL |
| developer_source | Source for published claim / endorsement | URL |
| reference_model | Epoch benchmark model identifier | text |
| notes | Benchmark configuration or exception | text |

**Transform:** Manual transcription of the eight rows from the Epoch article's published table. Run `python notebooks/build_v3_data.py` to validate source sample and regenerate processed data. It computes `difference_pp = developer_reported_pct - epoch_independent_pct` and `within_epoch_90ci = abs(difference_pp) <= epoch_90ci_halfwidth_pp`. App loads the processed output and recomputes these derived fields for validation. No aggregation, imputation, model scoring or automatic remote data refresh is performed.

**Limitations:** Selected 2025 GPQA comparison, not a 2026 sample, no banking-task relevance, and Epoch evaluation settings may differ from developer settings. Mistral is endorsed third-party, not developer self-reported, and its display name/reference model version differ in source.
