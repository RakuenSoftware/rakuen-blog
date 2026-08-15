# The fragmentation measurement, finished

The article prints the novel-predicate rate falling from 23.5% to 10.0% and calls
it provisional, because the run behind it stopped at 223 notes and left no
artifact. This is that measurement run to completion at 1,001 notes with both
arms on one card.

**It does not confirm the provisional figure.** The direction holds and the size
does not: 21.04% to 13.02%, a fall of 8.02 points against the 13.5 that was
printed. Both endpoints were more extreme than the complete run gives.

## Collection

- Started 2026-08-12 21:05:47 UTC, completed 23:00:05 UTC
- Hardware: AMD RX 7900 XTX, llama.cpp device `Vulkan1`, host `admin@192.168.1.254`
- Server binary: `/mnt/media/tierbench/bin/llama-b10210/llama-server`
- Model: `unsloth/gemma-4-E4B-it-GGUF:UD-Q4_K_XL`, no speculation on either arm
- Corpus: v5 `gold_small.jsonl`, 1,001 notes, both arms over all of it
- Client: concurrency 1, one process, `--cache-ram 1024`, thinking on, port 8820
- Scorer and ontology: the pinned source under `evidence/src/`, aimee `c2b44220217c`
- Launched by `harness/harness/ontology_ab.sh`

Both arms hit the same server process with the same weights, cache size and
concurrency. The only difference between them is the canonical relation list
interpolated into the prompt: 17 names against 24. The template text is
byte-identical, which is why `prompt_versions.v7()` derives the list rather than
keeping a second copy of the prompt.

| arm | prompt | relations | wall |
|---|---|---:|---:|
| v7 | `prompt_versions.v7()` | 17 | 55m |
| v8 | the live prompt | 24 | 59m |

## Result

A predicate is novel when it survives alias folding and is still not a seed
relation, which is what `rel_type_canonicalize()` decides in production.

| arm | facts | novel | rate | distinct | seen once |
|---|---:|---:|---:|---:|---:|
| v7 prompt, 17 relations | 1,022 | 215 | **21.04%** | 58 | 32 |
| v7 predictions, rescored against 24 | 1,022 | 157 | 15.36% | 53 | 32 |
| v8 prompt, 24 relations | 1,029 | 134 | **13.02%** | 53 | 31 |

The fall is 8.02 points and it splits:

- **ontology, 5.68 points.** The same predictions against the larger seed set.
  No model involved. This is the share that was the ontology failing to cover
  its own domain, and it would have been obtained by editing `rel_types.c` and
  rescoring, with no card and no rerun.
- **prompt, 2.34 points.** The model reaching for a listed name instead of
  inventing a synonym, which is the part that needed the rerun.

Roughly seven tenths of the improvement was definitional. The single number in
the article credits the prompt with work the ontology did.

## What moved, by name

The two seeded relations that were being invented most stopped being invented:
`runs_on` 24 to 0 and `mentors` 9 to 0. That is the mechanism working exactly as
the seeding argument said it would.

What remains is mostly the deliberate non-folds. `owns` 30 to 21 and
`contributes_to` 16 to 10 are both documented as too generic or too distinct to
fold, so they are expected to persist and they do.

One entry is worth flagging: `drives` appears 9 times under v7 and 8 under v8.
It is not in the ontology and it is not in the corpus vocabulary. It is one of
the three examples the prompt itself gives for inventing a predicate, so the
escape hatch is steering output rather than merely permitting it. See defect 44
in `MEASUREMENT_LOG.md`, which found the same sentence naming two canonical
relations as things to invent.

## Artifact integrity

Both arms: 1,001 rows, 1,001 unique ids matching the gold set exactly, zero
errors, every row parsed, none truncated, thinking on throughout, no draft
counters on any row. Each arm's rows all carry one `prompt_version`, and
`fragmentation.py` refuses to report if an arm mixes versions.

## What this does not settle

**One model, one corpus, one card.** The rate is a property of what a model
emits, so a different model gives a different rate. E4B was chosen because it is
the model the original fragmentation work used, not because the result
generalises.

**No interval.** This is a proportion over one run, not a paired comparison, and
nothing here bootstraps it. Two arms differing by 8 points on about 1,000 facts
is not in doubt as a direction; the second decimal is not defended.

**The 223-note figure is not reproduced and cannot be.** No artifact of that run
exists, so there is no way to tell whether it disagrees because of the sample
size, a different model, or a different definition of novel. What can be said is
that the complete measurement is the one with artifacts behind it.
