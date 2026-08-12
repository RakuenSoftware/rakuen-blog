# 31B QAT pair, same card, 3,002 notes

The registered same-card rerun of the gemma-4-31B QAT against non-QAT comparison.
The earlier 1,001-note pair crossed hardware, CT140 against a rented host, and the
rented-versus-local calibration bound of about ±0.019 is wider than the delta it
was measuring, so that pair could not resolve at any sample size. Both halves here
ran on one card.

## Collection

- Started 2026-08-11 19:51:25 UTC, completed 2026-08-12 11:33:42 UTC
- Hardware: AMD RX 7900 XTX, llama.cpp device `Vulkan1`, host `admin@192.168.1.254`
- Server binary: `/mnt/media/tierbench/bin/llama-b10210/llama-server`
- Corpus: v5 `gold_mid.jsonl`, 3,002 notes, no rows flagged excluded
- Client: prompt v8, concurrency 1, one process, `--cache-ram 1024`, port 8810
- Scorer: the pinned ontology under `evidence/src/`, aimee `c2b44220217c`
- Launched by `harness/launch_mid3k_xtx_20260811.sh`, a wrapper that changes
  nothing about `harness/harness/mid3k_pairs.sh`

| half | model | draft |
|---|---|---|
| QAT | `unsloth/gemma-4-31B-it-qat-GGUF:UD-Q4_K_XL` | `MTP/mtp-gemma-4-31B-it-Q8_0.gguf` |
| non-QAT | `unsloth/gemma-4-31B-it-GGUF:UD-Q4_K_XL` | the same file from the non-QAT repository |

## Result

| half | rows | strict F1 | precision | recall | tp | fp | fn | wall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| QAT | 3,002 | 0.6867 | 0.5939 | 0.8138 | 2,150 | 1,470 | 492 | 462m |
| non-QAT | 3,002 | 0.6857 | 0.5960 | 0.8073 | 2,133 | 1,446 | 509 | 474m |

Paired bootstrap over notes, 20,000 replicates, run by the campaign script itself
and recorded in `mid3k_xtx.log`:

```
QAT - nonQAT    0.0009   [-0.0064,+0.0082]   INDISTINGUISHABLE
```

## The registered prediction, and what happened

Quoted verbatim from `harness/harness/mid3k_pairs.sh`, written before the run
started:

> Why 3k: the interval narrows with sqrt(n). The 31B pair's half-width was 0.0124
> at n=1001; at n=3002 it should fall to about 0.0072, which would put the whole
> interval above zero IF the point estimate holds. That is the run's registered
> prediction, written down before it starts so it cannot be adjusted afterwards.

**The precision half of the prediction was right.** The achieved half-width is
0.0073 against 0.0072 predicted.

**The condition failed.** The point estimate did not hold. It fell from +0.0108 at
n=1001 to +0.0009 at n=3002, so the narrower interval closed around zero instead
of clearing it.

The prediction was therefore well made and cleanly answered. Narrowing the
interval was never going to help, because the effect it was narrowing around was
not there once the hardware term was removed.

The 1,001-note figure of +0.0108, recomputed on 2026-08-12 as +0.0108 with a
range of −0.0015 to +0.0231, is in `../../interval-recomputation-2026-08-11.md`.
It was fixed there while this run's second half was still going, so the before
number was recorded blind to the after.

## Artifact integrity

Both halves: 3,002 rows, 3,002 unique ids matching the gold set exactly, no
truncated rows, no error rows, concurrency 1 throughout, speculation active on
every row. QAT accepted 79.6% of 1,707,942 drafted tokens, non-QAT 79.1% of
1,801,290. Malformed output on 1 row of 3,002 in the QAT half and 2 in the
non-QAT half, which is 0.03% and 0.07%.

## The 12B half of this campaign was never completed

`mid3k_pairs.sh` registers a 12B pair on the 5080 as well. It has no prediction or
score file anywhere on this machine. Its log records two `START` lines four
seconds apart, at 10:55:09Z and 10:55:13Z on 2026-08-10, from two overlapping
launcher invocations that would have contended for port 8300 and the card, and
then nothing: no `DONE`, no `FAIL`, no stop reason.

That is worth stating precisely. It is not a run that was attempted and failed to
finish. It is a run that was started twice and abandoned without recording an
outcome, which is why nothing here supersedes the 12B row.

The earlier `results/mid3k/` directory holds those launch logs and is left
untouched.
