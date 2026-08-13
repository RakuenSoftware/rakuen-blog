# We Forced It to Think and the Score Fell

gemma-4-E4B at Q6 answers about 13% of notes with no reasoning pass. Forcing it
to reason on those notes cost 0.21 F1, and most of that turned out to be a
labelling convention in our corpus rather than the model getting anything wrong.

## Status

Publication-ready. Not yet published.

## What changed from the investigation

This started as `the-model-decides-when-to-think`, and both halves of that title
were wrong.

**The model does not decide.** The investigation read eight runs and reported the
behaviour as a property of E4B. Across all 280 committed prediction files it is a
property of the build: E4B at Q6 does it on 13.3% of notes across three separate
10,000-note runs, the QAT build on 16.0%, and the same weights at Q4 and Q8 on
0.1%. E2B never does it at any width.

**The benchmark cannot say whether it is a defect.** The investigation could not
tell whether silent notes scored well because reasoning was unnecessary or
because the model was skipping notes it already knew, and its README named the
run that would separate them. That run now exists and moved those notes from
0.8507 to 0.6418, but 17 notes carry the whole change and 10 of those are the
model leaving a gold convention rather than making an error. The first draft of
the article reported the mean and claimed the model was right. Reading the notes
underneath it took the claim away.

`evidence/investigation-2026-08-11.md` is kept unchanged as the record of what was
believed before the forced run, including the governance result that did not
survive replication and is not in the article.

## Evidence

`evidence/figures.md` maps every figure to an artifact. Everything lives under the
head-to-head article's evidence tree:

| directory | contents |
|---|---|
| `results/forced-reasoning-20260813/` | both halves of the forced-reasoning pair, the analysis, the run log |
| `results/10k-sharded/`, `results/10k-nomtp/` | the three 10,000-note runs behind the 13.3% |
| `results/qat-mid-3k/` | the QAT rate |
| `harness/harness/forced_reasoning.py` | rebuilds the paired figures |
| `analysis/who_obeyed.py` | which half obeyed, and where the loss actually sits |
| `harness/harness/prompt_versions.py` | `forcereason()` and `forcereason2()`, which change the conditional clause and nothing else |
| `results/escalation-20260813/` | the firmer wording, on the 134 notes the live prompt skipped |

## Reproducing

`analysis/` holds seven scripts. All read committed artifacts and run no
inference, so every one of them reruns without a card:

| script | what it establishes |
|---|---|
| `rate_and_exclusions.py` | the rate per run, and that length, truncation, parse failure and position do not explain it |
| `note_overlap_and_category.py` | cross-run note overlap against chance, and the category breakdown |
| `accuracy_split.py` | F1 on silent against reasoned notes, using the harness scorer |
| `replication_check.py` | the same split in both runs, with sign agreement per category |
| `category_intervals.py` | intervals on the per-category split |
| `governance_contradiction.py` | why the governance result did not survive replication |
| `who_obeyed.py` | which half obeyed the first instruction, and where the loss actually sits |

The first six are the original investigation and are kept as the record of what
was believed before the forced run. `governance_contradiction.py` in particular
explains a result that is deliberately absent from the article.

Two things need a card, and only to regenerate predictions that are already
banked: `harness/harness/forced_reasoning_ab.sh` for the pair, and the
`forcereason2` arm behind `harness/harness/escalation.py`. Both analyses run from
the committed artifacts without one.

## What is not claimed

No mechanism for why Q6 and QAT skip while Q4 and Q8 do not. No claim that
skipping is right on other models or corpora, because the treatment group is 67
notes on one card. No connection to Q6 winning the E4B width comparison in
`which-quant-beats-how-many-bits`, which is the same build and may be the same
effect, and is not measured.

And no claim that the skip is beyond the reach of the prompt. The draft said that
on one wording half the notes ignored; a firmer wording moved all 134, so the
sentence was weak rather than the model unreachable. What the prompt does not
reach is the quantization.
