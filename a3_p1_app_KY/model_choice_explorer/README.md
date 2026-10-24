# Model Choice Explorer (A3 Part 1, Q1 core question)

**Question:** In regions where leading closed US models are restricted, which accessible AI model gives an organisation the most measured capability for its cost and self-hosting feasibility?

**Persona:** group enterprise architect at an Asia-Pacific bank or insurer (Hong Kong and other markets) who must give the risk committee an interim approved list of AI models within one to two weeks.

## Run

```
cd "D:\UTS MDSI\36104 (2026)\Assignment 3\a3_p1_app\model_choice_explorer"
pip install -r requirements.txt
streamlit run app.py
```

Rebuild the processed table from the three source extracts: `python -m src.data`. Tests: `python -m pytest -q`.

## Files

- `app.py`: page, question, persona, shared controls, data/methods/limitations.
- `src/views.py`: View 1 (cost against capability, price frontier, labels that never overlap) and View 2 (ranked options, weighted parts, design decision).
- `src/analysis.py`: filters, percentile ranks, CRITIC weights, SMAA first-place share, price frontier, label placement.
- `src/data.py`: name matching of Epoch, LiteLLM and LMArena; validation.
- `data/source/`: source extracts (Epoch ECI 17 Oct 2026, LiteLLM chat prices 17 Oct 2026, LMArena overall 15 Oct 2026). `data/models.csv`: processed table (277 models).
