# Interval recomputation, 2026-08-11

Every paired interval in the series was published from `bootstrap_ci.py` and
none had been re-derived since. This is the record of doing that, now that the
scorer pin under `evidence/src/` is restored and the tree scores standalone.

Command form, one comparison per process, as
`quant-clarification-2026-08-09.md` requires:

```sh
python3 harness/harness/bootstrap_ci.py \
  --gold corpus/data/corpora/v5/gold_small.jsonl \
  --pred A=<pred> --pred B=<pred> --boot 20000 --seed 20260809
```

## Reproduced

| article | comparison | published | recomputed | verdict |
|---|---|---|---|---|
| which-quant | E2B Q6 − Q4 | +0.0065, −0.0142 to +0.0273 | identical | unchanged |
| which-quant | E4B Q6 − Q4 | +0.0150, −0.0035 to +0.0339 | identical | unchanged |
| which-quant | E4B Q6 − Q8 | +0.0245, +0.0091 to +0.0405 | identical | significant |
| which-quant | SmolLM3 Q8 − Q4 | +0.0351, +0.0156 to +0.0543 | identical | significant |
| which-quant | LFM2.5-2.6B Q4 − Q8 | +0.0104, −0.0153 to +0.0363 | identical | unchanged |
| how-small | 31B − E2B | +0.0465, +0.0220 to +0.0712 | +0.0465, **+0.0217 to +0.0715** | significant |
| how-small | Qwen 35B − 31B | +0.0386, +0.0194 to +0.0577 | +0.0386, **+0.0197 to +0.0577** | significant |

Every delta reproduces to four decimals.

The two `how-small` intervals move by 0.0003 at one endpoint each. That is the
random-stream artifact `quant-clarification-2026-08-09.md` documents: the scorer
draws the individual-run and paired intervals from one stream, so an invocation
carrying more than two `--pred` arguments lands on different endpoints at the
same seed. The five `which-quant` rows were already corrected to
one-pair-per-process values, and these two were not.

No verdict changes and neither interval crosses zero. Correcting them is a
consistency question rather than a correction, and it is left to the author.

## Not reproducible from committed artifacts

| article | comparison | why |
|---|---|---|
| one-sentence-turned-the-reasoning-off | thinking restored against v4, +0.0103, −0.0201 to +0.0404 | `results/v5-large/E4B.v5-955.pred.jsonl` is not committed |
| my-benchmark-lied-to-me | the same interval, cited for the withdrawn +0.084 constant | the same missing file |

`results/v5-large/` holds `E4B.v4-same955.pred.jsonl` and both score files, and a
second copy of the v4 predictions under `audit/`. The v5 side exists only as
`E4B.v5-955.score.json`.

A paired bootstrap resamples notes and needs both prediction sets, so the
aggregate score survives and the interval cannot be re-derived. The published
delta of +0.0103 is consistent with the two committed score files. The interval
around it is single-sourced to the run that produced it.

This does not retract the figure. It records that one interval in the series
rests on an artifact that was not kept, which is the distinction the reporting
rules ask for.

## Scope

Deltas and intervals only. The score-level figures were checked separately by
matching every four-decimal figure in each article against all six score scopes
across 185 committed score files, which is what found the quarantined 10k ladder
corrected on 2026-08-11.
