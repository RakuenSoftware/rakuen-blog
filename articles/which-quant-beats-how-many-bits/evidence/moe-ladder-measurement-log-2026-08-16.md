# Measurement log: the two-task quant ladder

Companion to `moe-ladder-plan-2026-08-16.md`, which is the registered plan. This
file records what went wrong while executing it, what each defect would have
corrupted had it survived, and which banked results are affected.

The campaign runs on one RTX 5080 in LXC 140 on 192.168.1.253, one arm at a
time. Runner sources are under `campaign/` in this repository.

**Every defect below shares one shape: it produced output indistinguishable from
success.** None of them raised an error. That is why they are logged
individually rather than summarised — the pattern is the finding.

## Discarded runs

| run | why discarded |
|---|---|
| First campaign, 2026-08-16 09:12Z, LFM2.5-2.6B Q4 | served with four slots and an unbounded prompt cache; superseded |
| Second campaign, 09:59Z, LFM2.5-2.6B Q4 | unbounded prompt cache; froze at 247/1001, see defect 3 |
| All synthesis before 2026-08-16 21:00Z (Q4, BF16) | served with reasoning enabled; see defect 10. Retained at `results-synthesis-DISCARDED-reasoning-on-20260816` |
| All synthesis 2026-08-16 21:00Z to 2026-08-17 08:20Z (6 arms) | `--reasoning-format none` broke grammar compilation; see defect 11. Retained at `results-synthesis*-DISCARDED-grammar-20260817` |

No score was published from either. The third campaign, from 10:49Z, is the one
whose results stand.

## Defects

### 1. Dense-spill detection never ran

**Symptom.** Arms logged `offload=unrecorded` and completed normally.

**Cause.** The check grepped the server log for `offloaded N/M layers`. This
llama.cpp build (version 1, `f9e832c`) emits no such line at any verbosity, so
the grep matched nothing — and the spill check was itself conditional on that
string being present, so it silently never executed.

**What it would have corrupted.** The operator's rule is that a dense model
which does not fit the card invalidates the arm, because every token traverses
every layer and a partially resident dense model is not the same experiment as
its fully resident siblings. `gemma4-12b.base.q8` at ~12.6 GiB plus an MTP draft
plus KV against 15880 MiB usable is the arm most likely to spill. It would have
produced a score, and that score would have been a measurement of card capacity
wearing a bit-width label.

**Fix.** Residency is measured, not parsed: weights resident on the card must
occupy at least their own file size in VRAM, read from the `/props` endpoint's
`model_path`. An unresolvable `model_path` now fails the arm rather than being
assumed fine. A physical invariant cannot silently pass by failing to match.

### 2. Four slots instead of one

**Symptom.** None. Arms ran and scored.

**Cause.** `--concurrency 1` was passed to the client; `-np` was left at its
default on the server, which starts four slots with a unified KV cache.

**What it would have corrupted.** Shared-slot state is a difference between arms
that has nothing to do with quantization, and this harness already carries two
investigations into parallel-slot nondeterminism
(`investigate_np32_nondeterminism.sh`, `check_parallel_determinism.py`). The
synthesis load profile pins one slot deliberately; extraction did not.

**Fix.** `-np 1` explicit. Affected arms discarded.

### 3. Unbounded prompt cache: a 9.3 GB balloon and a frozen queue

**Symptom.** The arm slowed from ~17 rows/min to ~5, then stopped. GPU
utilisation flat at 0% across a ten-second sample. No error in any log; the
campaign log's last line was `EXTRACT start`.

**Cause.** `--cache-ram` was not set. The prompt cache grew until the server held
**9.3 GB RSS for a 1.6 GiB model**, logging hundreds of `making room for prompt
cache entry` evictions, then deadlocked in `futex_do_wait` during shutdown while
the client waited out its hour-long socket timeout. `run_arm.sh` never returned,
so the campaign never reached arm 2.

**What it would have corrupted.** Beyond the freeze, this value is
results-affecting in this series: the 10,000-note ladder was quarantined and
re-taken because two model families had run at different `--cache-ram` settings,
and 1024 is the value that re-take standardised on. An arm at the unbounded
default was never comparable to anything else here, even if it had completed.

**Fix.** `--cache-ram 1024` explicit, matching the synthesis load profile. RSS
now settles at ~1.85 GB and holds. A watchdog with two independent liveness
signals — the server answering `/health`, and the prediction file still growing
— kills a stalled arm within minutes and lets the queue continue. The failure
presented as slowness, which is why one signal was not enough.

### 4. Bundle verification compared path formatting, not content

**Symptom.** `PUSHWARN: bundle checksums differ` on a byte-perfect transfer.

**Cause.** Local and remote each hashed a *file listing*. The local list yielded
`arms.tsv`; the remote list, after its `sed` passed through
`ssh` → `pct exec` → `bash -lc` quoting, kept the `./` prefix. Identical files,
different digest.

**What it would have corrupted.** Nothing directly — but a guard that cries wolf
gets ignored, which is worse than no guard.

**Fix.** A manifest of relative paths ships with the bundle and is checked with
`sha256sum -c` on the far side, which compares content and names the offending
file. 175 files verified per push. The manifest must exclude itself or it fails
its own check while still being written.

### 5. Throughput conflated prefill with generation

**Symptom.** A mean of **8,678 tok/s** for a model generating at 372.

**Cause.** llama.cpp logs `prompt eval time` for prefill and `eval time` for
generation. A grep for `eval time` matches both, and prefill runs about 45x
faster.

**What it would have corrupted.** Speed is a reported result of this article.
This would have inflated it by more than an order of magnitude, in the
flattering direction.

**Fix.** `throughput.py` separates them and reports both. Verified against the
completed Q4 arm: generation median 372.28 over 1,003 samples, matching a hand
computation. Prefill is reported separately at ~17,000 tok/s rather than
discarded.

### 6. The synthesis half was never wired in

**Symptom.** Three hours of campaign, reported as progress on a two-task matrix.

**Cause.** `run_campaign.sh` invoked `run_arm.sh` and nothing else. The synthesis
wrapper was written, shipped, and verified byte-for-byte on the container — and
never called. `grep -n synthesis run_campaign.sh` returned nothing.

**What it would have corrupted.** The article is specified as two tasks per arm.
Thirty-three extraction-only arms would have been half the experiment, with every
visible signal green.

**Fix.** `run_synthesis_arm.sh`, called per arm, idempotent independently of the
extraction half so completed extractions do not have to be re-run to backfill it.
`run_campaign.sh` now reports the two halves separately and says plainly when
their counts differ.

### 7. The KV sweep would have been five identical runs

**Symptom.** Would have been none. Five arms would have agreed perfectly.

**Cause.** The synthesis controller's `candidate_command` never emits
`-ctk`/`-ctv`. Every arm would have served at the f16 default whatever the
manifest said.

**What it would have corrupted.** The entire KV-precision sweep: five
configurations, five labels, one actual configuration, and a set of results whose
agreement would have looked like a finding.

**Fix.** `candidate_command` is wrapped to pass both cache types. Cache type
joins `LOAD_PROFILE`, so it is provable from the artifacts and the controller's
own equality check catches drift. Because that check requires one profile per
results root, each cache configuration writes to its own root.

**Related.** `-ctkd`/`-ctvd`, the *draft* model's cache, default to f16
independently of the target's. A "q4_0 KV" arm on any speculating model would
have been serving a q4_0 target cache against an f16 draft cache — not the
configuration its label claims. LFM2.5 ships no draft so it did not bite, but
every Gemma and Qwen arm speculates.

### 8. A schema change broke synthesis silently-enough

**Symptom.** Two arms recorded `synthesis FAILED rc=1 after 0s`.

**Cause.** Adding `ctk`/`ctv` took `arms.tsv` from 8 columns to 10;
`run_synthesis_ladder.py` asserts the field count.

**What it would have corrupted.** Nothing, and this one is included because it
worked as intended: the assertion fired, the loop recorded a failure, and the
campaign continued. The failure was in the harness rather than the model, so the
markers were cleared with `reset_results.sh --synth-failed` and the arms retried.
It is logged because a reader comparing arm counts will otherwise find two
unexplained failures in the record.

### 10. Synthesis measured reasoning behaviour, not synthesis

**Symptom.** LFM2.5-2.6B recorded 51-59% `truncated_rate`, a `raw_parse_rate`
of 0.41-0.49 and a `content_f1` of 0.14-0.17. Read naively: this model is bad at
synthesis.

**What the artifacts actually said.** Inspecting a "truncated" row:

    finish_reason: length
    usage: {"completion_tokens": 1536, "prompt_tokens": 553}
    response: ''
    parse_error: Expecting value: line 1 column 1 (char 0)

The model spent its entire 1,536-token budget and returned an **empty string**.
Not a cut-off answer -- no answer at all.

**Cause.** The runner requests `{"enable_thinking": false}` as a chat-template
kwarg. Every model in the published nine-configuration matrix honours it, and
every one truncates on **zero** of 1,000 cases with a parse rate of 1.000.
LFM2.5 does not honour it. It reasons regardless; llama.cpp, serving with
`--jinja`, routes reasoning into a channel separate from `message.content`; the
budget is exhausted before reasoning ends; `content` is never populated. The
server said so at load time and it was not read:

    chat template supports preserving reasoning, consider enabling it via
    --reasoning-preserve

**What it would have corrupted.** An entire task's worth of results, in a way
that looks like a finding. "LFM2.5-2.6B scores 0.14 on synthesis against the
published matrix's 0.29-0.36" is a publishable-looking sentence and it would
have been false: the number measures a model that was never told to stop
thinking, on a harness that discards thinking. It would also have contaminated
every cross-task claim, which is the point of the campaign.

Extraction was unaffected, and the asymmetry is the clue that should have been
noticed sooner: `run_llamacpp.py` uses the completion endpoint, where no
reasoning separation happens, and parsed 1001/1001 on every arm.

**Fix.** Reasoning is now forced off at the server with `--reasoning off`, which
applies the same intent as the template kwarg from a layer the model cannot
ignore, plus `--reasoning-format none` as a backstop so that any thoughts a
template still emits land in `message.content` and are scored rather than
discarded -- the behaviour Muse Glimmer already had in the published matrix.
Both are recorded in `LOAD_PROFILE`, so the divergence from the published
profile is visible in every artifact.

**Consequence.** The two completed synthesis arms are discarded and will be
re-run. No synthesis result stands as of this entry.

### 11. The fix for defect 10 broke structured output entirely

**Symptom.** Six synthesis arms completed with `truncated_rate` 0.000 — the
truncation problem looked solved — and `empty_rate` **1.000**, `raw_parse_rate`
0.000, `content_f1` **0.0000**. Read naively: the models produce nothing at all.

**What the artifacts actually said.** A raw row carried `ok: false`,
`attempts: 3`, `finish_reason: null`, `usage: null`, `response: null`. The
requests never succeeded; there was no model output to be empty. The server log:

    E common_sampler_init: error initializing grammar sampler for grammar:
    E srv send_error: task id = 1, error: Failed to initialize samplers
    E srv process_sing: failed to launch slot with task, id_task = 1

The grammar string is empty — nothing follows `grammar:`.

**Cause.** Defect 10's fix added two flags. `--reasoning off` addresses the
actual problem. `--reasoning-format none` was added as a backstop and is
incompatible with this harness: every request is constrained by
`response_format: {type: json_schema, strict: true}`, and with that flag set the
schema-to-grammar compilation yields an empty grammar and sampler init throws.
Every request fails, three retries each.

**Isolated rather than guessed.** `probe_reasoning_flags.sh` serves the smallest
model in the campaign on a spare port and issues one schema-constrained request
per configuration:

| configuration | result |
|---|---|
| baseline | `OK content='{ "colour": "blue" }'` |
| `--reasoning off` | `OK content='{ "colour": "blue" }'` |
| `--reasoning-format none` | `SERVER_ERROR 400 Failed to initialize samplers` |
| both | `SERVER_ERROR 400 Failed to initialize samplers` |

**What it would have corrupted.** The same task as defect 10, in the opposite
direction and more obviously — a content_f1 of exactly 0.0 across every arm is
implausible enough to invite scrutiny. The more dangerous property is that
`truncated_rate` fell to 0.000, so the metric being watched to confirm defect
10's fix showed exactly the improvement expected while the run was entirely
broken.

**Fix.** `--reasoning-format none` removed; `--reasoning off` retained and
verified to return content under strict `json_schema`. Six arms discarded.

### 9. Smaller faults, fixed without consequence

- `bootstrap_ci.py --pred` takes `LABEL=PATH`; a bare path lands entirely in the
  label and dies with `FileNotFoundError: ''`, which reads like a missing file
  rather than a malformed argument.
- `VRAM_MIB` was captured *after* the residency check that consumes it, so the
  new check would have compared against an empty string.
- Arm cleanup ended in `pkill -f` on the llama-server binary, which matches any
  server on the box regardless of owner. Now kills by pid, escalating to SIGKILL
  after ten seconds — the deadlock case can hold VRAM indefinitely.
- A summary line read a non-existent top-level `f1` key and printed `f1=None` on
  a fully successful arm. `arm.json` carried the complete score throughout.

## Results standing as of 2026-08-16

All from the third campaign, all on one RTX 5080, `-np 1`, `--cache-ram 1024`,
KV f16, no speculation (LFM2.5 publishes no draft), 1,001 notes of corpus v5
`gold_small.jsonl`, scored against the pinned ontology.

| arm | strict F1 | 95% CI | generation tok/s | parse |
|---|---|---|---|---|
| LFM2.5-2.6B Q4_K_M | 0.5952 | [0.5648, 0.6242] | 372.28 | 1001/1001 |
| LFM2.5-2.6B Q6_K | 0.5714 | [0.5411, 0.6015] | 302.50 | 1001/1001 |
| LFM2.5-2.6B Q8_0 | 0.5625 | [0.5323, 0.5922] | 252.15 | 1001/1001 |
| LFM2.5-2.6B BF16 | 0.5825 | [0.5529, 0.6117] | 150.28 | 1001/1001 |

Paired, seed `20260809`, 20,000 replicates, **one comparison per process** — the
scorer draws individual and paired intervals from a single random stream, so a
third `--pred` moves a paired endpoint even at the same seed.

| comparison | delta | 95% CI | verdict |
|---|---|---|---|
| Q6 − Q4 | −0.0238 | [−0.0513, +0.0041] | indistinguishable |
| **Q8 − Q4** | **−0.0327** | **[−0.0592, −0.0063]** | **significant** |
| Q8 − Q6 | −0.0089 | [−0.0331, +0.0152] | indistinguishable |
| BF16 − Q4 | −0.0127 | [−0.0393, +0.0137] | indistinguishable |
| BF16 − Q8 | +0.0200 | [−0.0029, +0.0432] | indistinguishable |

**One of five comparisons separates.** The defensible reading is that accuracy
is flat across bit width on this model within what 1,001 notes can resolve,
while throughput falls by a factor of 2.5.

Two cautions against making more of the Q8 result than it carries. With five
comparisons drawn from four overlapping runs, one range clearing zero is close
to what chance alone produces; no multiple-comparison correction is applied here,
and none is applied elsewhere in this series either. And if added bits genuinely
degraded this model, BF16 would be its worst arm — instead it is second best and
statistically tied with Q4.

### A mechanism proposed and then falsified, within one arm

Before BF16 ran, this log recorded a prediction: false positives rose
monotonically with width (404, 440, 477) while true positives stayed flat
(544, 528, 531), suggesting the extra bits bought more extractions and the
extras were wrong.

BF16 falsified it. The counts across the full ladder are:

| arm | tp | fp | fn |
|---|---:|---:|---:|
| Q4_K_M | 544 | 404 | 336 |
| Q6_K | 528 | 440 | 352 |
| Q8_0 | 531 | 477 | 349 |
| BF16 | 547 | 451 | 333 |

Neither series is monotonic once the top rung is included, so the
over-extraction story is dead. It is kept in this log rather than deleted
because it was stated as a prediction for the remaining ladders, and the record
of a prediction that failed is worth more than its quiet removal.

Nothing here was retracted, because nothing here was published. A hypothesis
that a later arm killed is the method working. This log records what was
believed and when so the reasoning can be audited, not because any of it
reached a reader.

**This bears on a withdrawn claim, but weakly.** The published article states:
*"An earlier claim that LFM2.5 worsened with more bits is withdrawn because its
range crosses zero."* That row was Q4 − Q8 = +0.0104, range [−0.0153, +0.0363].
This campaign measures the same direction three times larger, at Q8 − Q4 =
−0.0327, with a range that clears zero — but the BF16 rung then comes back up
and ties with Q4, which is not what "worsens with more bits" predicts. The
withdrawn claim should stay withdrawn.

Throughput is the result that is not ambiguous here: 372.28, 302.50, 252.15 and
150.28 tok/s across Q4, Q6, Q8 and BF16, monotonic, on identical hardware, from
about a thousand generation samples per arm with under 2% spread.

One model, and the smallest in the set. The article's existing Gemma ladders peak
at Q6, which is a third shape again.

## Results standing as of 2026-08-18

Twenty-two extraction arms and eighteen synthesis arms complete. All on one RTX
5080, `-np 1`, `--cache-ram 1024`, KV f16, MTP on where a draft exists, 1,001
notes of corpus v5 against the pinned ontology. Paired intervals at seed
`20260809`, 20,000 replicates, one comparison per process.

Four comparisons separate. Three were not anticipated by the published article.

### QAT collapses at two bits, on both models

| pair | delta | 95% CI | verdict |
|---|---:|---|---|
| E2B: QAT Q2 minus non-QAT Q2 | **-0.3511** | [-0.3830, -0.3187] | significant |
| E4B: QAT Q2 minus non-QAT Q2 | **-0.2982** | [-0.3317, -0.2638] | significant |

These are the largest effects in the campaign by an order of magnitude — the
whole LFM2.5-2.6B ladder spans 0.033 — and they replicate across two models in
the same direction.

The same pairs at four bits are level: E4B QAT Q4 0.6217 against non-QAT Q4
0.6183. So the finding is not "QAT helps less at low width", it is that the QAT
artefact is **actively worse** below four bits, by an amount that makes the model
unusable: E2B QAT Q2 scores 0.1889 against 0.5399 for the plain Q2 build.

It costs speed as well. E2B QAT Q2 generates at 126.3 tok/s against 459.4 for
non-QAT Q2; E4B 178.0 against 330.3. Slower *and* far worse, so no trade is
being made.

The two models fail in opposite ways, which is set out below under "The QAT Q2
collapse takes two different shapes".

A plausible reading is that these artefacts are built to be served at the width
their training targeted, and that quantising one past that point leaves the
range the training compensated for. This campaign does not test that mechanism;
the tables above are the measurement, not the explanation.

### The LFM family splits by architecture, not by publisher

The dense LFM2.5-2.6B declines across its ladder — 0.5952, 0.5714, 0.5625 at Q4,
Q6, Q8 — with only Q8 minus Q4 separating, at -0.0327.

The mixture-of-experts LFM2.5-8B-A1B does the opposite, monotonically:

| pair | delta | 95% CI | verdict |
|---|---:|---|---|
| 8B-A1B: Q8 minus Q4 | **+0.0378** | [+0.0080, +0.0675] | significant |

0.5091, 0.5341, 0.5470 at Q4, Q6, Q8. Same publisher, same quant family, same
card, opposite direction. Whatever drives the 2.6B result, it is not a property
of LFM2.5 as a family.

### gemma-4 E4B peaks at six bits, reproducing the published finding

| pair | delta | 95% CI | verdict |
|---|---:|---|---|
| E4B: Q6 minus Q8 | **+0.0235** | [+0.0068, +0.0403] | significant |

0.6183, 0.6393, 0.6158 at Q4, Q6, Q8. The published article reports E4B
Q6-over-Q8 at +0.0245 [+0.0091, +0.0405], measured on different hardware, a
different serving configuration and a different campaign. This measures +0.0235
[+0.0068, +0.0403]. An independent reproduction of an existing result, which is
worth more than a new one.

### The QAT Q2 collapse takes two different shapes

The two models that publish a QAT Q2 build both collapse, and they collapse in
opposite directions:

| arm | median completion tokens | strict F1 |
|---|---:|---:|
| E2B non-QAT Q2 | 520 | 0.5399 |
| **E2B QAT Q2** | **65** | **0.1889** |
| E4B non-QAT Q2 | 297 | 0.5858 |
| **E4B QAT Q2** | **611** | **0.2876** |

E2B stops producing output — 65 tokens a note, an eighth of its non-QAT twin.
E4B produces twice as much as its twin. One goes quiet, the other will not stop,
and both lose roughly a third of an F1 point.

That argues the failure is instability rather than a single degradation
mechanism. A model degraded uniformly would be expected to fail the same way
twice.

### Output length does not track bit width

Recorded because the intuitive story — fewer bits, worse discipline, longer
rambling output — is not what the arms show:

| model | Q2 | Q4 | Q6 | Q8 |
|---|---:|---:|---:|---:|
| E2B median tokens | 520 | 464 | 506 | 503 |
| E4B median tokens | 297 | 369 | 324 | 351 |
| LFM2.5-2.6B | — | 1037 | 1028 | 1000 |
| LFM2.5-8B-A1B | — | 675 | 725 | 709 |

E2B's Q2 is longer than its Q4; E4B's Q2 is *shorter*. Across both LFM ladders
length is flat within a few percent while accuracy moves in opposite directions
between the dense and MoE models. Whatever bit width does to these models, it is
not mediated by how much they write.

### The slow-arm gate has a blind spot

The gate measures **tokens per second** against the model's own Q4 arm.
`gemma4-12b.base.q2` probed at 183.9 tok/s against a 179.7 baseline — a ratio of
0.98, comfortably inside the 10x threshold — then ran at roughly half the rows
per minute of the Q4 arm, because it spent those tokens on longer generations
rather than on more notes.

Nothing was lost: the arm is slow, not stalled, and 5.7 hours against 2.7 is
tolerable. It is recorded because a model that generates at full speed and never
stops is invisible to a throughput gate, and the remaining arms run with experts
offloaded to system RAM, where the same behaviour would cost far more.

### At 26B, QAT is the difference between fitting the card and not

| gemma-4 26B-A4B Q4 | file | VRAM | host RSS | expert offload | generation | wall clock |
|---|---:|---:|---:|---|---:|---:|
| non-QAT | 16,222 MiB | 14,166 | 5,791 | first 8 layers on CPU | 109.9 tok/s | 3 h 46 m |
| **QAT** | **13,588 MiB** | 14,746 | **1,233** | **none** | **359.6 tok/s** | **1 h 17 m** |

Accuracy is a wash:

| pair | delta | 95% CI | verdict |
|---|---:|---|---|
| 26B-A4B: QAT Q4 − non-QAT Q4 | −0.0048 | [−0.0235, +0.0139] | indistinguishable |

The non-QAT artefact is 16,222 MiB against roughly 15,600 MiB usable — about
600 MiB too large — so its experts must partly compute on the CPU. The QAT
artefact is 2.6 GiB smaller and fits whole. Same accuracy, **3.3x the
throughput**, purely because one crosses a capacity threshold and the other does
not.

This independently reproduces the published article's central QAT claim, that
"QAT's clearest benefit was fitting a 26B model on a 16-gibibyte card", and puts
a number on the consequence the original could not: on this card it is not a
marginal fit advantage, it is 3.3x.

Note the probe overstated it. The warmed 400-token probe read 427.7 tok/s where
the full arm settled at 359.6 over 1,003 samples. Probe figures throughout this
campaign are a gate input, not a reported result; the medians are the result.

### Two-bit quantisation destroys output discipline on the larger dense model

| gemma-4 12B | median tokens per note | rows per minute | generation |
|---|---:|---:|---:|
| Q4 | 958 | 7.07 | 213.1 tok/s |
| Q6 | 976 | 6.29 | 183.8 tok/s |
| Q8 | 933 | 5.85 | 157.6 tok/s |
| **Q2** | **7,609** | **2.76** | **233.2 tok/s** |

Q2 generates *fastest* of the four and finishes *slowest*, taking 6 hours where
Q4 took 2.4. It emits roughly **eight times as many tokens per note** as any
other rung on its own ladder.

This settles a question left open earlier in this log. The effect is strongly
model-dependent and does not follow bit width in any simple way:

| model | Q2 median | Q4 median | ratio |
|---|---:|---:|---:|
| E2B | 520 | 464 | 1.12x |
| E4B | 297 | 369 | **0.80x** — shorter |
| 12B | 7,609 | 958 | **7.94x** |

E4B writes *less* at two bits; 12B writes eight times more. An earlier entry in
this log generalised from a single live log line that "Q2 rambles" and was
corrected to "output length does not track bit width". Both corrections stand:
length does not track width, and the 12B Q2 case is an extreme that belongs to
that model rather than to the rung.

### The two ways an arm gets slow are unrelated

The campaign now has clean examples of both, and they need separating because
they look identical from the outside — an arm that takes far longer than its
siblings:

- **Verbosity.** `gemma4-12b.base.q2` ran at the highest generation rate on its
  ladder and took the longest, because it spent those tokens on 7,609-token
  answers rather than on more notes.
- **Capacity.** `gemma4-26b-a4b.base.q4` ran at 109.9 tok/s against its QAT
  twin's 359.6 because 8 layers' experts computed on the CPU. Its output length
  was normal, 851 tokens against the twin's 825.

The slow-arm gate measures tokens per second, so it sees the second and is blind
to the first. `gemma4-12b.base.q2` probed at a 0.98 ratio against its own Q4
baseline and then took two and a half times as long.

Neither cost a result — both arms completed — but a gate that cannot see the
verbosity case would not stop a genuinely runaway arm, and the low rungs are
where that behaviour appears.

### Every offloaded arm ran with mmap enabled, against llama.cpp's own advice

All six expert-offload arms carry this at load:

    W llama_model_loader: tensor overrides to CPU are used with mmap enabled -
                          consider using --no-mmap for better performance

It was not acted on. gemma-4 26B-A4B at Q4, Q6 and Q8, and Qwen3.6-35B-A3B at
Q4, Q6 and Q8 — every arm that offloads experts — was served this way.

**Accuracy is unaffected.** Memory mapping changes how weights reach the compute
path, not what the compute produces, so every F1, every paired interval and
every ladder comparison in this log stands as measured.

**Throughput is affected and the figures are therefore a lower bound.** The
offload penalties recorded here — 109.9 tok/s at 26B Q4 against 359.6 for the
resident QAT build, down to 34.8 at Qwen Q8 — are the cost of offload *as
configured*, not the cost of offload. Real achievable throughput on this
hardware is better than these numbers by an unmeasured margin.

The direction of the capacity finding does not depend on it: a resident model
beat an offloaded one by 3.3x under a configuration that handicapped the
offloaded side, so correcting the handicap can only narrow that gap, never
reverse it. The magnitude is what is uncertain, and it is quoted as an upper
bound on the cost.

No A/B was run. Measuring it would cost an extra arm on a matrix that already
took five days, and it cannot change any accuracy claim — the only thing it
would refine is a number already labelled as bounded.

This is the third time in this campaign that a warning printed at model load
went unread. The first cost two synthesis runs to a reasoning channel nobody
looked at; the second was the same message about preserving reasoning; this one
cost precision in the campaign's headline figure. The pattern is not that the
warnings were obscure — it is that nothing in the harness reads them.

### The offloaded arms ran with unused VRAM, on purpose

The expert-offload tuner rejects any configuration using more than 14,200 MiB,
which left roughly 1.7 to 2.4 GiB of a 16 GiB card unused on the arms that most
needed it:

| arm | VRAM used | headroom | expert offload |
|---|---:|---:|---|
| 26B-A4B Q4 | 14,166 | 1,714 | first 8 layers |
| 26B-A4B Q6 | 14,102 | 1,778 | first 15 layers |
| 26B-A4B Q8 | 13,516 | 2,364 | first 19 layers |

That ceiling is too cautious and the campaign's own data says so. Tuning
26B-A4B Q4 explicitly rejected `n=7` at 14,622 MiB and `n=6` at 15,074 MiB, both
of which loaded cleanly. Two arms have since run for hours above the ceiling
without incident: 26B QAT Q4 at 14,746 MiB for 1 h 17 m, and gemma-4 12B Q8 at
14,546 MiB for 2 h 51 m.

Raising it to about 14,800 MiB would move one or two more layers onto the card
per offloaded arm, worth perhaps 10 to 15% on those arms.

**It was left alone deliberately.** All three 26B rungs and Qwen's Q4 were tuned
at 14,200. Changing the ceiling with Qwen Q6 and Q8 outstanding would give one
ladder two different serving budgets, which is the single inconsistency this
campaign cannot afford: the ceiling is an operational choice, but varying it
inside a ladder would make it behave like a variable.

The cost is bounded, known, and cheaper than a ladder that is not internally
comparable. It is recorded rather than fixed because the evidence that the
margin was too large arrived after the arms it constrained had already run.

### Synthesis prefers more bits; extraction does not

Across every model with both halves scored, synthesis content F1 rises with
width while extraction does not follow it:

| model | Q2 | Q4 | Q6 | Q8 |
|---|---:|---:|---:|---:|
| E2B synthesis | 0.2861 | 0.3284 | 0.3325 | 0.3350 |
| E4B synthesis | 0.3009 | 0.3222 | 0.3226 | 0.3246 |
| 8B-A1B synthesis | — | 0.2803 | 0.2815 | 0.2843 |
| LFM2.5-2.6B synthesis | — | 0.2960 | 0.3047 | 0.3047 |

Four models, monotonic or flat in every case, never inverted. Extraction over
the same arms inverts twice.

These synthesis figures carry **no paired intervals yet**. The synthesis harness
ships `paired_content_bootstrap.py` and it is not wired into this campaign, so
what is shown is a consistent direction across four models rather than a set of
separated comparisons. Closing that gap is the next task.

The practical shape: **on this evidence the task decides the answer.** A "use
Q4" recommendation drawn from extraction would cost synthesis quality on every
model measured, and a "use Q8" recommendation drawn from synthesis would cost
extraction accuracy on two of four.

## Synthesis

**No synthesis result stands.** Eight arms have now completed mechanically and
all eight are discarded: two under defect 10 and six under defect 11. Two arms completed mechanically -- LFM2.5-2.6B
Q4 in 3,693 s and BF16 in 8,714 s, both 1,000 cases, both through the
controller's case-population, model-identity, artifact-hash and load-profile
validators -- and both are discarded under defect 10, because they measured a
model reasoning into a discarded channel rather than performing the task.

That the controller's validators all passed is worth recording: they check that
the run was *configured and executed* as declared, which it was. Nothing in that
suite can tell you the declared configuration was the wrong one.
