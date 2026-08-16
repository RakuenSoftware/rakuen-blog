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

Neither series is monotonic once the top rung is included. The over-extraction
story is withdrawn. It is kept in this log rather than deleted because it was
stated as a prediction for the remaining ladders, and the record of a
prediction that failed is worth more than its quiet removal.

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

## Synthesis

One arm complete: LFM2.5-2.6B Q4, 3,693 s, 1,000 cases, through the controller's
case-population, model-identity, artifact-hash and load-profile validators. The
remaining arms are queued.
