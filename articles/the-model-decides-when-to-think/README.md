# The Model Decides When to Think

E4B returns an answer without reasoning first on 13% to 16% of notes. E2B never
does. The rows are not distinguished by length, truncation or malformed output,
which is where the previous investigation stopped.

## Status

Investigation, not a draft. There is no article file yet, and that is deliberate.

`evidence/investigation-2026-08-11.md` is the full record. The finding is real
and reproducible, but the result that would have led the piece did not survive
its only replication, so prose would be premature.

## Why there is no prose yet

The striking first-run result was that skipping reasoning cost 0.40 F1 on
`governance` notes, four times larger than any other effect in the split. In the
independent QAT run the sign reverses, on 62 and 20 notes. A result that flips on
its only replication is not a finding, and writing around it would have produced
a confident article built on 62 notes.

What survives replication is narrower and still worth publishing: silence is
category-dependent within a run, the same notes tend to go silent across runs at
2.7 times chance, and the accuracy effect is positive on `first_person` and
`novel_pred` and negative on `third_person` in both runs.

## The gap that decides whether this is publishable

Every comparison here is observational. The model chooses when to reason, so
"silent notes score better" is equally consistent with reasoning being unhelpful
and with the model correctly recognising notes it already knows. Nothing in the
corpus separates those two.

One run separates them: the same notes with reasoning forced on, paired against
these observations. Until that exists the piece can report a pattern and cannot
claim a mechanism, and the honest version of it is shorter and less interesting
than the one the first run suggested.

The intervals now exist, added 2026-08-12, and they strengthen the case. Three
categories hold in both runs with 95% intervals clear of zero: `first_person`
around +0.36, `novel_pred` between +0.24 and +0.36, `third_person` between −0.08
and −0.14.

They also sharpened the governance problem, which is now resolved. Its two
intervals do not overlap each other, and the cause is that the two runs went
silent on different notes: of 257 shared governance notes, each run skipped 20
and only 5 are the same. Not corpus difficulty, and not one influential note.

So the governance effect is real in the run that shows it and is not a property
of the category. It is a property of which notes that run chose to skip, and the
choice moves with the quantisation. The claim both runs support is that the skip
decision can be badly calibrated, evidenced once, which is narrower than either
run alone suggests.

## Reproducing

`analysis/` holds the four scripts, in the order the investigation ran:

| script | what it establishes |
|---|---|
| `rate_and_exclusions.py` | the rate per run, and that length, truncation, parse failure and position do not explain it |
| `note_overlap_and_category.py` | cross-run note overlap against chance, and the category breakdown |
| `accuracy_split.py` | F1 on silent against reasoned notes, using the harness's own per-note scorer |
| `replication_check.py` | the same split in both runs, with sign agreement per category |

They read committed artifacts under
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/` and run no
inference. `accuracy_split.py` and `replication_check.py` import the harness
scorer, so they need the pinned ontology under that article's `evidence/src/`.
