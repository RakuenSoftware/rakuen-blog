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
`mtp-Qwen3.6-35B-A3B-Q4_0.gguf`. Ornith-1.5-35B-A3B publishes no draft.

**No 9B model in this study can speculate on this build**, which was checked
rather than assumed after the base probed at 133 tok/s against 213 for the
larger gemma-4 12B. Two MTP shapes exist and only one of them works here:

- A *separate draft model*, passed with `-hfd`. This is what the gemma and
  qwen36 runs use, and it is why the 12B is faster than a model half its size.
- MTP layers *baked into the model*. `unsloth/Qwen3.5-9B-MTP-GGUF` ships these
  and this llama.cpp build discards them at load: `model has unused tensor
  blk.32.nextn.eh_proj.weight -- ignoring`, repeated for every nextn tensor. It
  serves at 133.11 tok/s against 133.6 for the ordinary build, so the MTP file
  is a larger download for no speedup.

protoLabsAI publishes a separate head for both Ornith 9B models
(`mtp-head/mtp-Ornith-1.0-9B-head-Q8_0.gguf`), but it fails to load as a draft:
`common_speculative_init_result: failed to load draft model`.

So both halves of the 9B pair run without speculation, which leaves the pair
matched. 133 tok/s is what a 9B dense at four bits does on this card unassisted,
and the comparison is unaffected.

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

## Registered expectation

**We expect a finetune not to shift measurably from its base in either
direction on this work.** Not merely that it fails to win: that it lands close
enough to its base that most of these comparisons do not separate at all.
Post-training moves behaviour, and these tasks ask for facts a base model
already has and output a base model can already format.

That is written here before any run produced a figure, so that whichever way
the intervals fall the reading was not chosen afterwards to fit them.

Stated this way the prediction is falsifiable and symmetric. **A large shift in
either direction contradicts it**, and a large loss is as much a surprise as a
large win.

Recording a prior cuts both ways and the discipline has to be symmetric:

- A null confirms the expectation, which is exactly when it is easiest to stop
  looking. A null still has to be a measured null with an interval, not an
  absence of evidence. If a comparison is indistinguishable, the article says
  1,001 notes could not tell them apart, not that the finetune is no better.
- A win contradicts the expectation, which is exactly when it is tempting to
  hunt for a defect until it goes away. A separating result gets the same
  scrutiny a null gets and no more: check output health, check the pair is
  matched, then report it.

If a large shift does appear, the first question is whether the finetune changed
what the model knows or what it emits. This harness separates those already,
because `score.json` records `output_health` alongside the score:
`json_parse_rate`, `schema_rate` and the completion-token distribution. A
finetune that stops producing parseable output scores badly on extraction
without having lost any knowledge, and that reads as a large shift unless the
health fields are checked beside it.

That check has earned its place twice in this series. It is what identified two
NVFP4 conversions as broken rather than merely worse, one failing JSON parsing
on 29% of notes and another emitting 33 tokens a note against 369 for its
sibling. It is also what characterised the two-bit QAT collapse as instability
rather than degradation: one model went quiet, the other would not stop.

The failure mode this guards against is real and has already happened once in
this series. In the quantization work a QAT pair was called a tie, and a second
task later separated it; the correction came from measuring the other half, not
from re-reading the first.

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
