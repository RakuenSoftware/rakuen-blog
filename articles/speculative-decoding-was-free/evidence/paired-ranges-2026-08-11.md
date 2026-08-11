# Paired accuracy ranges, 2026-08-11

All four comparisons used corpus v5 `gold_small.jsonl`, seed 42 and 20,000
paired bootstrap replicates. The script resamples the same note IDs on both sides
and reports MTP-on minus MTP-off.

Command shape:

```sh
python3 harness/harness/bootstrap_ci.py \
  --gold corpus/data/corpora/v5/gold_small.jsonl \
  --boot 20000 --seed 42 \
  --pred off=PATH_TO_MTP_OFF.pred.jsonl \
  --pred on=PATH_TO_MTP_ON.pred.jsonl
```

| pair | MTP-off F1 | MTP-on F1 | on minus off, 95% range | result |
|---|---:|---:|---:|---|
| Gemma 4 12B | 0.6854 | 0.6932 | +0.0079 [−0.0050, +0.0209] | crosses zero |
| Gemma 4 26B-A4B | 0.6833 | 0.6804 | −0.0029 [−0.0215, +0.0159] | crosses zero |
| Gemma 4 31B | 0.6898 | 0.6872 | −0.0026 [−0.0110, +0.0055] | crosses zero |
| Qwen3.6-35B-A3B | 0.7495 | 0.7427 | −0.0068 [−0.0203, +0.0068] | crosses zero |

Each input is the complete 1,001-row prediction artifact listed in
`evidence/figures.md`. Qwen3.6-27B was computed earlier with the same seed and
replicate count.
