# Quant comparison clarification, 2026-08-09

## Why this was run

The published head-to-head sorted saved F1 point estimates. Readers reasonably
read the vertical order as a claim that Q4 beat Q6 or Q8. This audit tests the
same-model quant comparisons directly and supplies the plain-language verdicts
used in the corrected figure.

No prediction, score or prior reporting artifact was changed or removed.

The reporting pass also compared every detailed Numbers-table field with its
mapped score artifact. Nineteen rows carried stale abstention and spurious-triple
values from an earlier scorer interpretation of empty output. F1, precision,
recall and parse rate already matched. The article now reads all six fields from
the saved score file for each row; the source artifacts remain unchanged.

## Method

- Corpus: `corpus/data/corpora/v5/gold_small.jsonl`, 1,001 notes.
- Predictions: the paths listed below, keyed to the same note ids.
- Statistic: paired bootstrap over notes, 20,000 replicates.
- Seed: `20260809`.
- Scorer: `harness/harness/bootstrap_ci.py`.
- Scorer inputs: the standalone evidence pin from rakuen-blog commit `59a468b`,
  which vendors aimee source at `c2b44220217c50a90ff61bd4dad81a7346f2790e`.
- Environment: Python 3.13 on the article workspace host, 2026-08-09 UTC.

Command form:

```sh
python3 harness/harness/bootstrap_ci.py \
  --gold corpus/data/corpora/v5/gold_small.jsonl \
  --pred Q4=results/<arm>.Q4.pred.jsonl \
  --pred Q8=results/<arm>.Q8.pred.jsonl \
  --boot 20000 --seed 20260809
```

Each comparison below was run in a separate process with exactly two `--pred`
arguments, in the order named in the comparison. This matters because the script
uses one random-number stream for the individual-run intervals and then the
paired interval. Adding a third run advances that stream and moves a paired
endpoint slightly even with the same seed. One pair per invocation makes every
row independently reproducible. Concrete prediction paths are mapped in
`../figures.md`.

## Results used in the article

| comparison | delta | paired 95% interval | verdict |
|---|---:|---:|---|
| gemma-4-E2B, Q6 minus Q4 | +0.0065 | −0.0142 to +0.0273 | tie |
| gemma-4-E2B, Q8 minus Q4 | +0.0112 | −0.0083 to +0.0307 | tie |
| gemma-4-E2B, Q8 minus Q6 | +0.0047 | −0.0151 to +0.0247 | tie |
| gemma-4-E4B, Q6 minus Q4 | +0.0150 | −0.0035 to +0.0339 | tie |
| gemma-4-E4B, Q4 minus Q8 | +0.0096 | −0.0051 to +0.0245 | tie |
| gemma-4-E4B, Q6 minus Q8 | +0.0245 | +0.0091 to +0.0405 | Q6 wins |
| LFM2.5-2.6B, Q6 minus Q4 | −0.0059 | −0.0332 to +0.0222 | tie |
| LFM2.5-2.6B, Q8 minus Q4 | −0.0104 | −0.0363 to +0.0153 | tie |
| LFM2.5-2.6B, Q8 minus Q6 | −0.0045 | −0.0302 to +0.0206 | tie |
| LFM2.5-VL-1.6B, Q6 minus Q8 | +0.0019 | −0.0075 to +0.0113 | tie |
| LFM2.5-1.2B, Q6 minus Q8 | +0.0100 | −0.0082 to +0.0280 | tie |
| LFM2.5-230M, Q6 minus Q8 | +0.0054 | −0.0012 to +0.0127 | tie |
| SmolLM3-3B, Q8 minus Q4 | +0.0351 | +0.0156 to +0.0543 | Q8 wins |

The comparison-only Smol Q4 run has strict F1 0.3581 in
`results/newcomers-1k/SmolLM3-3B.Q4_K_M.score.json`. It is not part of the
32-row leaderboard. Reported deltas are calculated from unrounded scores.

## Reproduction pass

Re-run on 2026-08-09 UTC from the same host and pinned evidence source described
above. All thirteen deltas, interval verdicts and score components reproduced
with one comparison per process. Compared with the initial multi-run invocation,
five intervals' endpoints moved by at most 0.0006 because of the random-stream
ordering described under Method. No interval changed sides of zero and no
reader-facing verdict changed.

Gemma Q4, Q6 and Q8 use the matched `results/v8-baseline/` prediction files for
this comparison. The prior leaderboard used Q4 from `results/v5-rerun-gguf/`
beside Q6 and Q8 from `results/v8-baseline/`; those are different run campaigns
and do not carry the quant verdict.

## Component check on the apparent LFM2.5 reversal

| quant | true positives | false positives | false negatives | F1 |
|---|---:|---:|---:|---:|
| Q4_K_M | 533 | 408 | 347 | 0.5854 |
| Q8_0 | 535 | 446 | 345 | 0.5750 |

Q8 found two more true facts and emitted 38 more false ones. The F1 point
estimate fell through precision, not recall. Its paired range crosses zero.

## Disposition

- Replace the default ranked score graph with a same-model quant verdict graph.
- Keep the complete observed scores under the Numbers tab.
- Call unresolved comparisons `tie` in the article, not `indistinguishable`.
- Preserve exact deltas and intervals in the article and figure map.
- Replace the two Gemma Q4 leaderboard rows with their matched v8-baseline runs.
- Refresh the detailed abstention and spurious-triple fields, the restraint
  comparison and the scatter from the mapped score artifacts.
