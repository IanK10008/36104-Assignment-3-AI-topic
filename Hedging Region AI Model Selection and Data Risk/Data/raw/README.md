# Data/raw: files saved by hand

This folder holds source files that a person put here, as opposed to files a notebook downloaded by itself. Notebook downloads go to the `raw/` folder inside each dataset folder.
這個資料夾放「人工下載或複製」的原始檔。由 notebook 自動下載的檔案放在各資料集資料夾自己的 `raw/` 裡。

| Sub-folder | Content | Used by | Origin |
|---|---|---|---|
| `epoch/` | `eci_scores.csv`, `benchmark_data.zip` | notebooks 01 and 07 as a fallback if the download fails | `eci_scores.csv`: hand download of 2026-10-18 (277 models, 34,152 bytes), replaced the Part 2 copy of 2026-10-14 (274 models). `benchmark_data.zip`: Part 2 download of 2026-10-14 (2,382,498 bytes) |
| `epoch/` (also) | `all_ai_models.csv` (not saved yet, optional) | notebook 09 | Save https://epoch.ai/data/all_ai_models.csv here if the notebook's download is blocked |
| `manual/` | `fmti-main.zip` and other files | notebook 08 reads `fmti-main.zip` as a fallback | Hand download of the Stanford FMTI repository ZIP |
| `lmarena/` | (empty) | notebook 06 as a fallback | If the Hugging Face download fails, save the `text` / `latest` Parquet file from https://huggingface.co/datasets/lmarena-ai/leaderboard-dataset here |
| `litellm/` | (empty) | notebook 04 as a fallback | If the download fails, save https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json here as `model_prices_and_context_window.json` |

The notebooks use the **newer** of a hand-saved file here and their own earlier download, so a fresh hand download always wins.

## Files you downloaded by hand that are still in the `Data` folder

These are for the later batch (not Q1), so notebooks do not read them yet. They are now in `raw/manual/` (moved by hand on 2026-10-18):

- `AIID_Excel_Export-20261012.xlsx` (AI Incident Database export, CC BY-SA 4.0 on the snapshot collections)
- `fmti-main.zip` and `FMTI 2025 paper.pdf` (Stanford Foundation Model Transparency Index)
- `ai_protection_framework_pcpd_hl.pdf` (PCPD AI framework, copyright terms not yet read)
- `backup-20261012101643.tar.bz2` (AIID database backup, large, only if needed)
- `APAC Enterprise AI Model Research.docx`, `Deep_Research_Brief_Round_3_Leads_and_Visuals.md` (research notes, not data)
