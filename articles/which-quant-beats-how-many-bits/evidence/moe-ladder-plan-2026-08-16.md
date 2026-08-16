# The two-task quant ladder: campaign specification

Written 2026-08-16, before any arm ran. This is the registered plan. Deviations
from it are recorded in the campaign log, not edited out of here.

## What this measures and why it is new

The published article carries five bit-width comparisons, all of them on small
*dense* models: gemma-4 E2B, gemma-4 E4B, SmolLM3-3B and LFM2.5-2.6B. Two of the
five cleared their paired range and they point in opposite directions on width.
Above 12B there is no ladder at all, because a 16 GiB card cannot hold a dense
Q8 build of anything larger.

Two things are missing, and this campaign supplies both.

**A ladder that reaches past 12B.** Mixture-of-expert models make this possible
on the same card: the weights spill into host RAM while only the active experts
need to move. gemma-4 26B-A4B (4B active), Qwen3.6 35B-A3B (3B active) and
LFM2.5-8B-A1B (1B active) carry that part.

**A second task.** Every bit-width claim in the series rests on one task, fact
extraction. Whether the answer transfers is untested. Each rung here is scored
on the extraction corpus *and* on the frozen synthesis fixture, so a rung that
wins on one task and loses on the other becomes visible rather than assumed.

The question the campaign answers is therefore narrower and sharper than "how
many bits": **is the bit-width answer stable across model scale, across
architecture (dense against MoE), and across task?**

## The matrix

Seven models, three rungs each, plus a QAT arm at Q4 wherever a QAT build
exists. BF16 is deliberately deferred; see below.

Standing preferences, applied wherever the published artifacts allow it:
**UD builds preferred, MTP on, QAT on.** Each is qualified below by what is
actually published, which in one case changes the shape of the experiment.

The rule is simply: **every rung a model actually publishes gets run.** Where a
width does not exist for a model, that cell is empty and the ladder is reported
as reaching only as far as its published builds allow. Nothing is substituted in
from another publisher or another quantization method to fill a gap.

| model | active | Q1 | Q2 | Q4 | Q6 | Q8 | MTP | QAT arms |
|---|---|---|---|---|---|---|---|---|
| gemma-4 E2B | dense | — | UD-Q2_K_XL | UD-Q4_K_XL | UD-Q6_K_XL | UD-Q8_K_XL | on | Q2, Q4 |
| gemma-4 E4B | dense | — | UD-Q2_K_XL | UD-Q4_K_XL | UD-Q6_K_XL | UD-Q8_K_XL | on | Q2, Q4 |
| gemma-4 12b | dense | — | UD-Q2_K_XL | UD-Q4_K_XL | UD-Q6_K_XL | UD-Q8_K_XL | on | Q4 |
| gemma-4 26B-A4B | 4B | — | UD-Q2_K_XL | UD-Q4_K_XL | UD-Q6_K_XL | UD-Q8_K_XL | on | Q4 |
| LFM2.5-2.6B | dense | — | — | Q4_K_M | Q6_K | Q8_0 | unsupported | none |
| LFM2.5-8B-A1B | 1B | — | — | Q4_K_M | Q6_K | Q8_0 | unsupported | none |
| Qwen3.6-35B-A3B | 3B | UD-IQ1_M | UD-Q2_K_XL | UD-Q4_K_XL | UD-Q6_K_XL | UD-Q8_K_XL | on | none |

27 ladder rungs plus 6 QAT arms = **33 arms**. Each arm is scored on both
tasks, so 66 runs.

Availability was checked against the HuggingFace file listings on 2026-08-16.
LiquidAI publishes nothing below Q4 for either LFM2.5 model, and the QAT builds
for 12B and 26B-A4B stop at Q4 while E2B and E4B also publish a QAT Q2 — which
gives those two models a genuine two-rung QAT ladder rather than a single point.

Qwen3.6-35B-A3B is the only model in the set publishing any Q1 build at all.

### The bottom of the ladder changes method, and that is a confound

`UD-Q2_K_XL` is a K-quant and stays inside the same `UD-*_K_XL` family as Q4, Q6
and Q8, so the two-to-eight-bit span of each ladder holds one method constant.
That is why Q2 uses it rather than the `UD-IQ2_M` and `UD-IQ2_XXS` builds that
also exist for several of these models.

The Qwen Q1 point cannot have that property. `UD-IQ1_M` is an **imatrix** quant —
importance-weighted using calibration data — so it differs from the rungs above it
in method as well as width. It is reported as a one-bit probe on one model, not
as a comparable rung, and any gap between it and Q2 is not attributable to width
alone.

### Expect the low rungs to fail differently, and record how

The scorer counts malformed JSON as failure, so every score is a floor. At Q2 and
Q1 the binding constraint is likely to stop being extraction quality and start
being whether the model emits parseable JSON at all. The article already carries
a parse-floor thread — two 12B runs parsed 90% and 92%, and a bounded repair
analysis sits beside them.

Parse rate is therefore recorded as a first-class result for every arm, not a
diagnostic. A Q2 arm that scores near zero because it cannot produce valid JSON
is a different finding from one that parses cleanly and extracts badly, and the
two must not be reported as the same number.

Publishers, verified against the HuggingFace file listing on 2026-08-16:
all four Gemma models and Qwen3.6-35B-A3B come from `unsloth`, both LFM2.5
models from `LiquidAI`.

### QAT is an arm, not a rung, because only Q4 is published

The four `unsloth/gemma-4-*-it-qat-GGUF` repositories each publish exactly one
target build: `UD-Q4_K_XL`, plus a `UD-Q2_K_XL` for E2B and E4B. There is no QAT
Q6, no QAT Q8 and no QAT BF16 for any model.

So QAT cannot be a property of the ladder — a bit-width ladder on QAT weights
does not exist to be run. The ladder rungs are therefore non-QAT, and QAT enters
as an additional arm at the Q4 rung for each of the four Gemma models.

This is a better experiment than folding QAT into the rungs would have been. It
asks whether QAT-Q4 buys what extra bits buy: if QAT at four bits lands level
with non-QAT Q6 or Q8, that is a far stronger and more useful statement than the
article's current E2B-only +0.0389, and it is measured on the same card, the
same corpus and the same fixture as the rungs it is being compared against.

### MTP is on wherever a draft sidecar exists

Both the QAT and non-QAT Gemma repositories ship `MTP/mtp-*-Q8_0.gguf`, so all
Gemma arms run with speculation on, the draft held constant across every rung of
a model. Qwen3.6-35B-A3B takes its draft from `ggml-org`, which is the only
publisher shipping an MTP sidecar for it; the target weights remain unsloth UD.

Carried forward from the series' own findings: the Qwen draft head is Q4_0 and
cannot be overridden on this llama.cpp lineage — `-hfd REPO:file` is accepted and
then ignored, measured byte-identical. The draft is Q4_0 whatever is requested.
Because it is identical across that model's rungs, the ladder remains
one-variable; it only means Gemma-to-Qwen *acceptance* is not a clean comparison.

LFM2.5 publishes no draft sidecar for either model, so those two ladders run
without speculation. That is recorded as unsupported, not as a choice.

### Two decisions the file listing forced

**Qwen3.6-35B-A3B moves publisher.** The prior series used
`ggml-org/Qwen3.6-35B-A3B-GGUF`, which publishes only Q4_K_M, Q8_0 and BF16 —
**there is no Q6 in that repository**, so it cannot carry a ladder.
`unsloth/Qwen3.6-35B-A3B-GGUF` publishes the complete UD-Q4/Q6/Q8_K_XL family.
The ladder uses unsloth. Consequence, stated rather than buried: this model's
rungs do not join to the Q4_K_M rows in the synthesis-model-selection or
speculative-decoding articles, because those are different weights.

**LFM2.5 cannot use the same quant family as the rest.** LiquidAI does not
publish unsloth's dynamic UD builds, so the LFM ladders are stock K-quants while
Gemma and Qwen are dynamic. This is a real asymmetry and it is not fixable by
choosing differently. It is also directly relevant to the article's existing
finding that a dynamic four-bit packing beat a flat one by +0.0229: if the LFM
ladders behave differently from the Gemma ladders, packing scheme is one of the
candidate explanations and must be named as such.

Within any one model, all three rungs share one publisher and one naming family.
That is the property a ladder actually requires, and it is the property the
article's own `quant-clarification-2026-08-09.md` records having previously got
wrong by pairing a Q4 from one campaign against Q6 and Q8 from another.

### What "one variable" means here

Speculation is on for five of the seven models and unavailable for two. That is
a difference *between models*, not within a ladder, and the ladder is the unit of
comparison: within any one model, every rung shares publisher, quant family,
draft model, serving flags and hardware, and differs only in target bit width.

Cross-model comparisons in this campaign are therefore weaker than within-model
ones and are reported as such. The LFM ladders in particular carry two
differences from the Gemma ladders at once — stock K-quants rather than dynamic
UD, and no speculation — so they can support a statement about the *shape* of an
LFM ladder but not a like-for-like ranking against Gemma.

## Hardware and the changes made to it

One RTX 5080, 16303 MiB, in LXC 140 `tierA-5080` on the Proxmox host
192.168.1.253. Every arm runs on that card, one at a time.

Two container limits were raised on 2026-08-16 to make offloaded arms possible:

| limit | was | now | verified |
|---|---|---|---|
| RAM | 32 GiB | 96 GiB | live cgroup `memory.max` = 103079215104; container reports 96 GiB total |
| rootfs | 300 GiB | 800 GiB | `df -h /` reports 787 GiB, 702 GiB free |

**The container has no usable swap.** Its config declares 4 GiB but the Proxmox
host has none, so the declaration is inert. There is no soft landing if an arm
overshoots RAM: it will be killed. Arms must therefore be guarded by a projected
footprint check before launch, not by watching them fail.

The host has 125 GiB total with roughly 49 GiB in use by 27 other containers,
several of them serving real traffic (`dns`, `nginx-proxy`, `rakuen-web`). An
LXC memory figure is a cap and not a reservation, so nothing is taken from those
containers until an arm actually touches the pages. The largest arm in *this*
phase is Qwen3.6-35B-A3B at Q8, about 36 GiB, which leaves comfortable headroom.
The BF16 phase is where that stops being true, which is one of the reasons it is
deferred.

## Why BF16 is deferred rather than dropped

BF16 is wanted for six of the seven models. It is held back because its
footprint is where the plan stops being safe on measurement rather than on
estimate: Qwen3.6-35B-A3B at BF16 is roughly 68 GiB and gemma-4 26B-A4B roughly
50 GiB, against a host with 76 GiB free and no swap. gemma-4 12b is excluded from
BF16 entirely — about 24 GiB against a 16 GiB card is a fully offloaded dense
model, which is the worst case for this task shape and buys nothing.

The Q4/Q6/Q8 phase produces the measurement that decides the BF16 phase: real
tokens-per-second at real offload ratios on this exact card. That number is not
currently known and cannot be estimated honestly from the GPU-resident history.

## The slow-arm rule

Offload does not cost what the active-parameter count suggests it should. The
harness's own `sweep_moe.sh` records why:

> a long prefill routes across most experts, so the active-parameter saving
> largely evaporates exactly where our cost is

Extraction is prefill-dominated — roughly 400 tokens in, 48 out — so an A3B model
spilled to host RAM does **not** get the generation-side discount that makes MoE
offload attractive elsewhere.

Accordingly, no arm is allowed to block the queue:

1. After the server reports healthy, run a warmed throughput probe. Warmed, and
   over a generation long enough to average — the first `moe-tune` probe was
   discarded precisely because it measured page-fault-in on a cold 100-token
   generation and produced non-monotonic nonsense.
2. Project the arm's wall-clock from that measurement.
3. If the projection exceeds **10x the same model's Q4 arm**, do not run it.
   Record `SKIPPED_TOO_SLOW` with the measured throughput, the projection and
   the offload ratio, then continue to the next arm.
4. A skipped arm is reported as skipped. It is never reported as a completed
   measurement, and the ladder it belongs to is reported as incomplete.

The skipped set is a deliverable, not a failure: "which rungs are unreachable on
16 GiB and what would they cost" is itself one of the article's findings.

## Execution order

Ascending cost, so the cheap ladders complete and are analysable early and any
harness defect surfaces on a fast arm rather than a slow one:

1. LFM2.5-2.6B — Q4, Q6, Q8
2. gemma-4 E2B — Q4, QAT-Q4, Q2, QAT-Q2, Q6, Q8
3. gemma-4 E4B — Q4, QAT-Q4, Q2, QAT-Q2, Q6, Q8
4. LFM2.5-8B-A1B — Q4, Q6, Q8
5. gemma-4 12b — Q4, QAT-Q4, Q2, Q6, Q8
6. gemma-4 26B-A4B — Q4, QAT-Q4, Q2, Q6, Q8
7. Qwen3.6-35B-A3B — Q4, Q2, Q1, Q6, Q8

Within a model, non-QAT Q4 runs first because the slow-arm rule needs it as the
baseline, and its QAT counterpart runs second so the two four-bit builds are
adjacent in time on the same card. The low rungs follow, being the cheapest and
the most likely to expose a parse-rate collapse early. Q6 and Q8 run last because
they are the arms at risk of spilling to host RAM.

gemma-4 12b at Q8 is about 12.6 GiB against 16303 MiB of VRAM. It is expected to
fit only with a short context and nothing else resident, and is the most likely
card-resident arm to spill. Whether it does is recorded, not assumed.

## Tasks, harnesses and what is held constant

**Extraction.** Corpus v5 `gold_small.jsonl`, 1,001 notes, the same set every
1k arm in the series used. Driven by `harness/sweep_quant_arm.sh` →
`run_llamacpp.py`, scored by `score.py`, intervals by `bootstrap_ci.py` at seed
`20260809` with 20,000 replicates, **one comparison per process** — the scorer
draws individual and paired intervals from one random stream, so a third
`--pred` moves a paired endpoint even at the same seed.

Scoring requires the pinned ontology under
`articles/local-llm-fact-extraction-head-to-head/evidence/src/`. Without it the
run scores against a different ontology and the numbers are not comparable to
the series.

**Synthesis.** The frozen 1,000-case fixture from
`articles/synthesis-model-selection/benchmarks/fixtures/ab-v1/synthesis.jsonl`,
taken in SHA-256 case-ID order, driven by
`benchmarks/ab-v2/run_candidate_matrix.py` and validated by
`analyze_candidate_matrix.py`, which checks case population, load profile, model
identity and raw artifact hashes before bootstrapping.

That controller launches `llama-server` as a local subprocess and its
`CANDIDATES` tuple is hardcoded, so it runs *inside* CT 140 with the ladder arms
added. The extraction driver keeps its existing shape and drives the container
from outside. Both are serialised: only one arm ever holds the card.

Held constant across every arm: card, llama.cpp build, context length, prompt,
request order, concurrency 1, scorer, fixture, seed. Varying: the weights.

Recorded per arm, because `-ngl 99` and an absence of offload warnings were both
satisfied by the wrong card once already: serving device identity, resident
memory, offload ratio, model file SHA-256, and the warmed throughput probe.

## What this campaign will not establish

- It cannot separate publisher from bit width for the LFM ladders, because
  LiquidAI and unsloth quantize differently and no LFM UD build exists.
- It shares one corpus lineage with every other extraction result in the series.
  A second independently built corpus remains the gate for stronger claims and
  this campaign does not supply one.
- Every speculating arm holds its draft constant across rungs, so the campaign
  measures quantization *under* speculation rather than its interaction with it.
  It licenses no statement about that interaction beyond the three pairs already
  published.
- The QAT arms compare QAT-Q4 against non-QAT rungs of the same model. They
  cannot separate QAT from the UD packing both builds share, and they say nothing
  about QAT above four bits, because no such build is published.
