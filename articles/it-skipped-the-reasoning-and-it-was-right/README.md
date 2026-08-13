# It Skipped the Reasoning and It Was Right

gemma-4-E4B at Q6 answers about 13% of notes with no reasoning pass. Forcing it
to reason on those notes cost 0.21 F1. The skip was the model being right about
which notes were easy.

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

**It is not a defect.** The investigation could not tell whether silent notes
scored well because reasoning was unnecessary or because the model was skipping
notes it already knew, and its README named the run that would separate them. That
run now exists. Removing the model's discretion moved those notes from 0.8507 to
0.6418.

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
| `harness/harness/forced_reasoning.py` | rebuilds every number in the article |
| `harness/harness/prompt_versions.py` | `forcereason()`, which changes the conditional clause and nothing else |

## Reproducing

`analysis/` holds the four scripts from the original investigation, which read
committed artifacts and run no inference:

| script | what it establishes |
|---|---|
| `rate_and_exclusions.py` | the rate per run, and that length, truncation, parse failure and position do not explain it |
| `note_overlap_and_category.py` | cross-run note overlap against chance, and the category breakdown |
| `accuracy_split.py` | F1 on silent against reasoned notes, using the harness scorer |
| `replication_check.py` | the same split in both runs, with sign agreement per category |

The forced-reasoning pair is rerun with `harness/harness/forced_reasoning_ab.sh`,
which needs a card. Its analysis is rerun from the banked predictions without one.

## What is not claimed

No mechanism for why Q6 and QAT skip while Q4 and Q8 do not. No claim that
skipping is right on other models or corpora, because the treatment group is 67
notes on one card. No connection to Q6 winning the E4B width comparison in
`which-quant-beats-how-many-bits`, which is the same build and may be the same
effect, and is not measured.
