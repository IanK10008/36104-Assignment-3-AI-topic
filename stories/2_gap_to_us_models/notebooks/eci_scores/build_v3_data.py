"""Rebuild the Story 2 V3 app data from a versioned source transcription."""
from pathlib import Path
import pandas as pd
BASE = Path(__file__).resolve().parents[1] / 'data'
raw = pd.read_csv(BASE / 'raw' / 'epoch_article_gpqa_table.csv')
assert len(raw) == 8 and raw.model.is_unique
for c in ['developer_reported_pct', 'epoch_independent_pct']:
    assert raw[c].between(0,100).all()
processed = raw.copy()
processed['difference_pp'] = (processed.developer_reported_pct - processed.epoch_independent_pct).round(2)
processed['within_epoch_90ci'] = processed.difference_pp.abs() <= processed.epoch_90ci_halfwidth_pp
output = BASE / 'processed' / 'gpqa_reported_vs_epoch.csv'
output.parent.mkdir(exist_ok=True)
processed.to_csv(output, index=False)
print('Wrote', output, len(processed), 'rows')
