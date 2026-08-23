# Ornith against the base it came from: registered plan, 2026-08-23

Written before any run started, to the same rule as
`which-quant-beats-how-many-bits/evidence/moe-ladder-plan-2026-08-16.md`: the
design and its known weaknesses are on record before the numbers exist.

## The question

Ornith is a finetune family. Every Ornith model is derived from a Qwen base, so
each one can be measured against the exact model it came from, on the same card
and the same corpora. That answers a narrower question than a leaderboard does:
**does this finetune do the job better than the thing it was made from.**

Lineage is confirmed from `config.json` rather than from the card text, which
never names an upstream. `ornith-ai/Ornith-1.0-9B` reports
`Qwen3_5ForConditionalGeneration` and `model_type: qwen3_5`; the 35B reports
`Qwen3_5MoeForConditionalGeneration` and `qwen3_5_moe`.

## Pairs

| finetune | file | base | file |
|---|---|---|---|
| Ornith-1.0-9B | unsloth UD-Q4_K_XL, 5.57 GiB | Qwen3.5-9B | unsloth UD-Q4_K_XL, 5.56 GiB |
| Ornith-1.5-9B | ornith-ai Q4_K_M, 5.24 GiB | Qwen3.5-9B | unsloth UD-Q4_K_XL, 5.56 GiB |
| Ornith-1.5-35B-A3B | ornith-ai Q4_K_M, 20.22 GiB | Qwen3.6-35B-A3B | unsloth UD-Q4_K_XL, 20.82 GiB |

There is no Qwen3.6-9B, so both 9B finetunes pair against Qwen3.5-9B.

UD-Q4_K_XL is this series' standard and stays the standard for the base half.
Where Ornith publishes nothing above Q4_K_M, the finetune runs at Q4_K_M rather
than the base being downgraded to match. The recipe difference is recorded here
and travels with any result from those two rungs.

## What is already measured

`qwen36-35b-a3b.base.q4` from the quantization campaign is the base half of the
35B pair: UD-Q4_K_XL, `-ncmoe 19`, f16 cache, strict F1 **0.7194** on the same
1,001-note corpus. It is reused rather than re-run.

## Speculation is measured as shipped

The series rule is multi-token prediction on wherever the publisher provides a
draft, and off wherever they do not. That is applied here without exception.

The existing Qwen3.6 baseline was served **with** the ggml-org MTP draft
`mtp-Qwen3.6-35B-A3B-Q4_0.gguf`. Ornith-1.5-35B-A3B publishes no draft, and
neither does any 9B model in this study, so those run without one.

Speculation does not change what a model outputs, so every accuracy comparison
here is unaffected by it. Throughput is affected, and the article says so: the
35B throughput gap includes the fact that the base ships a draft and the
finetune does not. That is a real difference between the two things a reader can
download, not an artefact to correct away. Shipping no draft is a choice the
publisher made.

## Runs

Four new runs, same harness, same card, `-ctk f16 -ctv f16`, `-np 1`, `-c 8192`,
`-ncmoe` tuned to the smallest workable value on anything that spills. Each
scored on both the 1,001-note extraction corpus and the 1,000-case synthesis
fixture, as the quantization campaign was.

| label | target | speculation |
|---|---|---|
| `qwen35-9b.base.q4` | unsloth/Qwen3.5-9B-GGUF:UD-Q4_K_XL | none |
| `ornith10-9b.base.q4` | unsloth/Ornith-1.0-9B-GGUF:UD-Q4_K_XL | none |
| `ornith15-9b.base.q4` | ornith-ai/Ornith-1.5-9B-GGUF, Q4_K_M file | none |
| `ornith15-35b-a3b.base.q4` | ornith-ai/Ornith-1.5-35B-A3B-GGUF, Q4_K_M file | none |

## What this can and cannot support

- It can say whether a given Ornith build extracts facts or writes syntheses
  better than the Qwen it was made from, on these two tasks, at four bits.
- It cannot rank Ornith against models outside its own lineage, and it cannot
  separate the finetune from the quantization recipe on the two rungs where
  Ornith ships only Q4_K_M.
- A null is a real result here. "The finetune did not beat its base on this
  work" is the outcome most worth stating plainly if it is what the intervals
  say.

## Intervals

Paired bootstrap against the base half of each pair, seed `20260809`, 20,000
replicates on extraction and 5,000 on synthesis, one comparison per process, as
in the quantization campaign.
