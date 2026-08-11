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

## What did not survive

The governance result was the striking one in the first run: skipping reasoning
looked like it cost 0.40 F1 there, four times any other effect. It does not
replicate. The sign flips in the second run, on 62 and 20 notes.

It is recorded here because it was found and would otherwise have led the
article. A result that reverses on its only replication is not a finding.

## What stands

1. E4B declines to reason on 13% to 16% of rows in two runs. E2B never does, in
   six runs.
2. It is not length, truncation, malformed output, schema failure or position.
3. The same notes tend to go silent across runs, at 2.7 times chance.
4. Within a run, silence is strongly category-dependent, including four
   categories at exactly zero across 3,938 notes.
5. Between runs, the category pattern changes, so quantisation conditions it too.
6. Skipping reasoning is associated with better accuracy on `first_person` and
   `novel_pred` and worse on `third_person`, in both runs.

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
