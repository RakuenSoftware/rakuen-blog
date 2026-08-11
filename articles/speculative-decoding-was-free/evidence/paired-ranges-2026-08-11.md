# Paired accuracy ranges, 2026-08-11

All eleven comparisons use 20,000 paired bootstrap replicates. The script
resamples the same note IDs on both sides and reports MTP-on minus MTP-off. The
five 1,001-note pairs and three E2B pairs use seed 42. The E4B ranges were
banked earlier with their run record.

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

## Earlier 10,000-note Gemma pairs

These six pairs use corpus v5 `gold_large.jsonl`. The E2B ranges were recomputed
from the stored per-note artifacts on 2026-08-11. The scorer and ontology were
checked out at aimee commit `0a7c8cc3a3`, which reproduces the banked scores
exactly. Using a later ontology does not. The complete E2B output is stored at
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/results/10k-nomtp/e2b-mtp-paired-ci-20260811.txt`.

| pair | MTP-off F1 | MTP-on F1 | on minus off, 95% range | result |
|---|---:|---:|---:|---|
| Gemma 4 E2B Q4 | 0.6207 | 0.6246 | +0.0039 [−0.0015, +0.0092] | crosses zero |
| Gemma 4 E2B Q6 | 0.6331 | 0.6344 | +0.0013 [−0.0034, +0.0060] | crosses zero |
| Gemma 4 E2B Q8 | 0.6351 | 0.6329 | −0.0021 [−0.0073, +0.0031] | crosses zero |
| Gemma 4 E4B Q4 | 0.6306 | 0.6301 | −0.0005 [−0.0036, +0.0028] | crosses zero |
| Gemma 4 E4B Q6 | 0.6435 | 0.6452 | +0.0017 [−0.0013, +0.0048] | crosses zero |
| Gemma 4 E4B Q8 | 0.6327 | 0.6337 | +0.0010 [−0.0021, +0.0041] | crosses zero |

The E4B ranges were already recorded in `ARTICLE_NOTES.md`. Reversing their
published no-MTP-minus-MTP direction gives the on-minus-off ranges above.
Paired deltas use unrounded counts; displayed arm scores are rounded separately.
