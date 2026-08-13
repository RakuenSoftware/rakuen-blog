# Figure provenance and reporting record

Every figure comes from committed prediction files under the head-to-head
article's evidence tree. No figure here required a run that is not banked.

## The silence rates

| figure | artifact | weight |
|---|---|---|
| E4B Q6 13.3% on three 10,000-note runs | `results/10k-sharded/`, `results/10k-nomtp/`, and the quarantined `10k-sharded/quarantine/E4B-10k-cacheram8192-20260804T0041Z/` E4B `UD-Q6_K_XL` files | first-party, three independent runs |
| E4B Q6 15.0% to 16.8% at 1,001 notes | `results/quant-ledger/v5small`, `results/quant-ledger/v3small`, `results/v8-baseline/E4B.UD-Q6_K_XL.mtp`, and this article's own live half | four campaigns, three corpora |
| E4B QAT 16.0% | `results/qat-mid-3k/gemma-4-E4B-it.qat.mid.pred.jsonl`, 3,002 notes | first-party |
| E4B Q4 and Q8 at 0.1%, E2B at 0.0% | the same `10k-sharded` and `10k-nomtp` directories | first-party |

Silence is `reasoning_chars` of zero on a row that recorded `thinking: true`, so
it is the model returning no reasoning content when the channel was open, not the
channel being closed.

The rate was measured across all 280 committed prediction files rather than the
eight the earlier investigation used. That is what moved the claim: the
investigation reported the behaviour as a property of E4B, and E4B at Q4 and Q8
sit in the same sweep at 0.1%.

## The forced-reasoning pair

`results/forced-reasoning-20260813/`: both prediction files,
`forced_reasoning.json`, the run log, and `harness/harness/forced_reasoning.py`
which rebuilds every number below.

- 2026-08-13, 07:41 to 09:33 UTC, RX 7900 XTX, `Vulkan1`, llama.cpp `b10210`
- `unsloth/gemma-4-E4B-it-GGUF:UD-Q6_K_XL`, no speculation on either half
- v5 `gold_small.jsonl`, 1,001 notes, both halves over all of it
- concurrency 1, one process, `--cache-ram 1024`, thinking on, port 8830
- Both halves against one server process. The only difference is the conditional
  clause, rendered by `prompt_versions.forcereason()`

| figure | value |
|---|---|
| silent under the live prompt | 134 of 1,001, 13.4% |
| silent under the forced prompt | 71 of 1,001, 7.1% |
| silent-note F1 under live | 0.8507 |
| reasoned-note F1 under live | 0.4212 |
| FORCED group, 67 notes | 0.8507 to 0.6418, **−0.2090** |
| 95% range on that change | **−0.3284 to −0.0896**, 20,000 replicates, seed `20260809` |
| wording control, 863 notes reasoned under both | −0.0028 |
| selection control, 67 notes silent under both | −0.0448 |
| net of both controls | −0.1614 |

Both halves: 1,001 rows, 1,001 unique ids matching gold, zero errors, every row
parsed, none truncated, no draft counters. Each half records one
`prompt_version`, and the analysis refuses to report on a file that mixes them.

## Where the loss sits, and the confound the controls do not catch

`analysis/who_obeyed.py` rebuilds this from the same two files.

| figure | value |
|---|---|
| notes unchanged | 47 of 67 |
| notes improved | 3 of 67 |
| notes that got worse | **17 of 67** |
| mean change among those 17 | **−1.0000**, every one from a perfect score to zero |
| of the 17, gold object is the implicit `user` and the forced answer left it | **10** |
| of the 17, relation changed only / object only / both | 3 / 9 / 5 |

The mean of −0.2090 is 17 total failures and 50 notes that did not move, not a
small loss spread evenly.

**Ten of those seventeen are a scoring convention rather than an error.** The
gold object for "Aldridge Chemicals signed as a customer" is `user`, the implicit
other party, which the sentence does not name. Answering directly the model wrote
`user`; reasoning, it wrote `customer`. That is the more literal reading of the
note and the scorer gives it zero.

So under 0.12 of the 0.2090 is the model getting a fact wrong. The article states
this rather than reporting the mean alone, and the earlier draft of the article
did not, which is the reason this section exists.

The seven remaining failures are ordinary, the clearest being `works_for` for
"Ming Lei contributes to linux" where the direct answer gave `contributes_to`.

## The two confounds the controls do catch

**The wording.** The forced prompt is a different prompt, so the change could be
the sentence rather than the reasoning. The 863 notes that reasoned under both
saw the same new sentence and moved −0.0028, which is the sentence's own worth on
this corpus.

**The selection.** The FORCED group is chosen for having scored 0.85, and any
high-scoring selection falls on remeasurement. The 67 notes that stayed silent
under both prompts are chosen identically and never treated, and they moved
−0.0448.

**What the selection control does not do.** The two groups start at 0.8507 and
0.6567, so they are not matched. Subtracting one from the other bounds the
regression artifact; it does not remove it. A matched design would pair each
forced note with a silent note of the same live score, and that is not run.

## The escalation, and the claim it removed

`results/escalation-20260813/`: the prediction file, the 134-note gold subset,
the run log, and `harness/harness/escalation.py` which rebuilds the counts.

- 2026-08-13, 17:21 to 17:26 UTC, same card, model, cache size and concurrency as
  the pair above; only the prompt differs
- `prompt_versions.forcereason2()`, which replaces the conditional reasoning
  clause with one naming a minimum, forbidding the obvious-answer exemption and
  covering the empty case
- 134 notes: exactly those the live prompt answered without reasoning, extracted
  by `harness/harness/silent_subset.py`, which fails if any id is missing from
  the gold rather than quietly measuring a smaller set

| group | notes | reasoning under forcereason2 |
|---|---:|---:|
| moved by the first wording | 67 | 67 |
| ignored the first wording | 67 | **67** |
| all notes silent under live | 134 | **134**, 100% |

134 of 134 parsed, zero errors.

**This removed a claim from the article.** The draft said that whatever decides
the skip "sits below the level a sentence reaches", on the evidence that half the
notes ignored one instruction. A firmer instruction reached every one of them, so
the first sentence was weak rather than the model unreachable.

The two levers are therefore separate, which is the corrected statement: the
build decides the default and no wording changes the quantization, while the
prompt decides whether that default holds and needs to ask harder than "reason on
every note".

## Not claimed

- **That the skip is out of reach of the prompt.** An earlier draft said so, from
  one wording that half the notes ignored. A firmer wording moved all of them.
  What is out of reach of the prompt is the quantization, which is a different
  claim about a different lever.
- **That the model was right to skip.** An earlier draft of this article said so,
  on the mean alone. Ten of the seventeen damaged notes are the model leaving a
  labelling convention rather than getting a fact wrong, so this corpus cannot
  settle whether the skip was correct. It can only say that forcing reasoning
  stopped the model matching the house style.
- **A mechanism for why Q6 and QAT skip and Q4 and Q8 do not.** Nothing here
  explains it. The article reports the association and stops.
- **Anything general about skipping.** One model, one corpus, one card, 67
  treated notes, 17 of which carry the whole effect.
- **That the 67 unmoved notes are unreachable.** They did not move under this
  wording. A stronger instruction is untested.
- **Any connection to Q6 winning the E4B width comparison** in
  `which-quant-beats-how-many-bits`. Q6 is both the width that scored best and
  the width that skips, and whether those are the same effect is unmeasured. It
  is not asserted in the article and should not be inferred from it.

## Supersedes

This replaces the framing in the earlier investigation record,
`evidence/investigation-2026-08-11.md`, which is kept unchanged. That record
attributes the behaviour to E4B and treats the accuracy split as unresolvable
without a forced run. The first half is wrong, and the second half is why this
article waited for one.
