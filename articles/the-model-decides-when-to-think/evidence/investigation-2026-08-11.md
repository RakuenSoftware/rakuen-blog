# E4B's reasoning refusal: what it is, and what did not survive replication

Investigation run 2026-08-11 against committed artifacts. No new inference was
run. Every number below is reproducible with the scripts in `../analysis/`.

`ARTICLE_NOTES.md` records the open question this starts from:

> Why E4B declines to reason on a stable ~16% of rows is unexplained. The rows
> are not distinguished by context length, truncation, or the tool-call envelope.
> That is a real open question, not a caveat.

## The rate, and who has it

`reasoning_chars` of zero on a row means the model returned an answer without
reasoning first.

| run | rows | reasoned | silent | rate |
|---|---:|---:|---:|---:|
| E2B 10k Q4 | 10,000 | 10,000 | 0 | 100.0% |
| E2B 10k Q6 | 10,000 | 10,000 | 0 | 100.0% |
| E2B 10k Q8 | 10,000 | 10,000 | 0 | 100.0% |
| E4B 10k Q4 | 10,000 | 9,989 | 11 | 99.9% |
| **E4B 10k Q6** | 10,000 | 8,673 | **1,327** | 86.7% |
| E4B 10k Q8 | 10,000 | 9,994 | 6 | 99.9% |
| **E4B qat mid3k** | 3,002 | 2,523 | **479** | 84.0% |
| E2B qat mid3k | 3,002 | 3,002 | 0 | 100.0% |

Two things the framing in `ARTICLE_NOTES.md` does not say. E2B never does this,
across six runs and 33,002 notes. And it is not a property of E4B either: E4B at
Q4 and Q8 is at 99.9%. Only two runs show it, and they are different quants on
different corpora.

A third data point arrived on 2026-08-12 from an unrelated run. The 31B QAT half
of the mid3k pair reasoned on 3,002 of 3,002 notes, on the same corpus where E4B
QAT reasoned on 2,523 of 3,002. Same notes, same harness, same card, same
concurrency, 100% against 84%.

That is the cleanest contrast available: the corpus cannot be what makes a model
skip reasoning, because a different model on exactly those notes skipped none of
them.

## What it is not

Checked on the E4B 10k Q6 run, silent rows against reasoned rows:

| candidate | silent | reasoned | verdict |
|---|---|---|---|
| malformed output | `parse_ok` true on all 1,327 | true on all 8,673 | not it |
| schema violation | `schema_ok` true on all | true on all | not it |
| truncation | `truncated` false on all | false on all | not it |
| note length | 575.7 mean prompt tokens | 575.6 | not it |
| drift over the run | 129 to 155 silent per position decile | uniform | not it |

Silent rows are valid, complete, well-formed answers. They are shorter, at 41.4
against 376.2 mean completion tokens, which is what skipping reasoning costs.

## What it is, partly

**The same notes tend to go silent across runs.** On the 3,002 notes both runs
share, 387 are silent in 10k Q6 and 479 in qat mid3k. If the two were
independent, 62 would be silent in both. The observed overlap is 168, or 2.7
times chance. So something in the note drives it, and something else does not,
because the overlap is far from complete.

**Silence is category-dependent, in the 10k Q6 run.**

| category | silent | total | rate |
|---|---:|---:|---:|
| third_person | 795 | 1,580 | 50.3% |
| novel_pred | 141 | 321 | 43.9% |
| infra | 239 | 772 | 31.0% |
| governance | 62 | 856 | 7.2% |
| first_person | 50 | 795 | 6.3% |
| multi_fact | 40 | 1,738 | 2.3% |
| implicit | 0 | 723 | 0.0% |
| ambiguous | 0 | 506 | 0.0% |
| negation | 0 | 1,318 | 0.0% |
| transient | 0 | 1,391 | 0.0% |

Four categories at exactly zero across 3,938 notes is not a rate, it is a rule.
The prior investigation looked at length, truncation and the envelope, and
category was not among them.

**But the category pattern itself does not hold across runs.** In qat mid3k,
`transient` has 178 silent rows and `ambiguous` has 26, against zero for both in
10k Q6. So category predicts silence within a run and not between runs. Whatever
selects these notes is conditioned on the quantisation as well as the note.

## Does declining to reason cost anything

Scored with the harness's own `per_note_counts`, so these are the published
scorer's numbers.

E4B 10k Q6, aggregate:

| group | notes | tp | fp | fn | F1 |
|---|---:|---:|---:|---:|---:|
| reasoned | 8,673 | 4,813 | 3,673 | 2,415 | 0.6126 |
| silent | 1,327 | 1,265 | 299 | 298 | 0.8091 |

The aggregate favours silence by 0.197, and the aggregate is not usable. Silence
concentrates in `infra`, which scores near 1.0 for everyone, so this is a
composition effect rather than a finding.

Per category, and against the same split in the independent qat mid3k run:

| category | 10k Q6 delta | n silent | mid3k delta | n silent | sign agrees |
|---|---:|---:|---:|---:|---|
| first_person | +0.3564 | 50 | +0.3617 | 41 | yes |
| novel_pred | +0.2400 | 141 | +0.3636 | 26 | yes |
| third_person | −0.0767 | 795 | −0.1442 | 155 | yes |
| **governance** | **−0.4025** | 62 | **+0.1087** | 20 | **no** |

Delta is F1 on silent notes minus F1 on reasoned notes, within the category.

## Intervals, added 2026-08-12

Every delta above was a point estimate. Bootstrap intervals, 20,000 replicates,
seed 20260812, resampling each group independently within its category because
the two groups are different notes rather than a pairing.

| category | 10k Q6 delta | 95% interval | mid3k delta | 95% interval |
|---|---:|---|---:|---|
| first_person | +0.3564 | +0.2682 to +0.4302 | +0.3617 | +0.2893 to +0.4380 |
| novel_pred | +0.2400 | +0.1712 to +0.3079 | +0.3636 | +0.2727 to +0.4595 |
| third_person | −0.0767 | −0.1178 to −0.0356 | −0.1442 | −0.2241 to −0.0660 |
| governance | −0.4025 | −0.5243 to −0.2751 | +0.1087 | −0.0705 to +0.2553 |
| infra | +0.0207 | +0.0099 to +0.0330 | too few silent notes | |
| multi_fact | +0.2838 | +0.1795 to +0.3577 | too few silent notes | |

Three categories now hold in both runs with intervals clear of zero, and the
overlap between runs is close: `first_person`, `novel_pred`, `third_person`. That
is stronger than the earlier sign-agreement check showed.

`governance` is worse than unreplicated. Its two intervals do not overlap each
other at all, with the 10k upper bound at −0.2751 and the mid3k lower bound at
−0.0705. The second run does not merely fail to confirm the first; the two runs
are incompatible.

### Why governance disagrees, resolved 2026-08-12

Three explanations were checked with `analysis/governance_contradiction.py`.

**It is not corpus difficulty.** Governance scores 0.7816 pooled in the 10k
corpus and 0.7491 in the mid3k subset.

**It is not one influential note.** Leaving out the single most influential note
in the 10k silent group moves the delta from −0.4025 to −0.4123. The effect is
robust within that run.

**The two runs went silent on different notes.** The runs share 257 governance
notes. The 10k run is silent on 20 of them and the mid3k run on 20, and only 5
are shared, a Jaccard of 0.143. Chance alone predicts 1.6 shared, so the overlap
is above chance and still leaves two mostly disjoint sets.

That is the explanation. The 10k run skipped a set of governance notes it then
failed, and the QAT run skipped a different set it handled. Within the 10k run
the failure is stark: 37 of 62 silent governance notes produced no true positive
at all, against 114 of 794 reasoned ones, and silent notes averaged 0.58 false
positives against 0.26.

So the effect is real in the run that shows it, and it is not a property of the
category. It is a property of which notes that run chose to skip, and the choice
moves with the quantisation. The finding is therefore that the skip decision can
be badly calibrated, evidenced once, rather than that governance notes need
reasoning.

That is a narrower claim than either run alone suggests, and it is the one both
runs support.

### A degenerate zero in this analysis

`ambiguous`, `transient` and `negation` first came back with a delta of exactly
+0.0000 and a zero-width interval, which read as the strongest result in the
table.

They carry no gold triples by construction. The scorer reports `f1: None` for
them and says why in the artifact. The helper here returned 0.0 instead, which
turned "not applicable" into "no difference".

They are now excluded and labelled. Recorded because it is the same fault this
series keeps finding: a zero produced by a code path that had nothing to measure,
sitting in a table beside zeros that mean something.

## What did not survive

The governance result was the striking one in the first run: skipping reasoning
looked like it cost 0.40 F1 there, four times any other effect. It does not
replicate. The sign flips in the second run, on 62 and 20 notes.

It is recorded here because it was found and would otherwise have led the
article. A result that reverses on its only replication is not a finding.

## What stands

1. E4B declines to reason on 13% to 16% of rows in two runs. E2B never does, in
   six runs, and 31B QAT never does on the same 3,002 notes where E4B QAT skips
   479 of them.
2. It is not length, truncation, malformed output, schema failure or position.
3. The same notes tend to go silent across runs, at 2.7 times chance.
4. Within a run, silence is strongly category-dependent, including four
   categories at exactly zero across 3,938 notes.
5. Between runs, the category pattern changes, so quantisation conditions it too.
6. Skipping reasoning is associated with better accuracy on `first_person` and
   `novel_pred` and worse on `third_person`, in both runs, with bootstrap
   intervals clear of zero in all six cases.

## What this cannot say

The model chooses when to reason, so every comparison here is observational. A
positive delta is equally consistent with reasoning being unhelpful and with the
model correctly identifying the notes it already knows. Nothing here separates
those, and no run in the corpus forces reasoning on or off per note.

The experiment that would separate them is a paired run over the same notes with
reasoning forced on, against these observations. That is one run, and it is not
in the corpus.

Sample sizes for the per-category deltas are small once split, at 20 to 141 for
every category except `third_person`. None of the deltas above carries an
interval yet.
