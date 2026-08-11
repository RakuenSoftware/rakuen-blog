# Figure provenance and reporting record

Paths below are relative to the shared series evidence base at
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`.

## Corpus measurements

| figure | artifact |
|---|---|
| 10,000-note category counts and 3,215 factless notes | `corpus/data/corpora/v5/gold_large.jsonl` |
| factless-category F1 correction | `harness/harness/score.py`; `MEASUREMENT_LOG.md`, defect 24 |
| native 1,001 against subset of 3,002 | `results/qat-vs-ud/`; `results/qat-mid-3k/`; comparison in `MEASUREMENT_LOG.md` |
| 529/1,001 byte identity and −0.0079 score change | same files and reporting record |
| predecessor split, 44.8% against 48.3% | analysis recorded in `MEASUREMENT_LOG.md`; no derived table artifact retained |
| cache-off identity, 499/1,001 | `results/cache-isolation/E2B.qat.cacheoff.small.pred.jsonl`; matching `mid` file |
| shuffled identity, 524/1,001 | `results/cache-isolation/E2B.qat.cacheoff.shuffled.pred.jsonl` |
| ontology coverage and relation-family counts | v5 corpus plus `harness/harness/score.py`; audit in `ARTICLE_NOTES.md` |
| hostname template counts, 23 and 28 | source corpus and generation audit in `MEASUREMENT_LOG.md` |

## Reporting inventory and disposition

- **Factless-stratum audit:** kept. The earlier claim that F1 was blind was
  corrected in the article.
- **Tier-containment test:** kept. It establishes that a subset extraction is not
  equivalent to a native run.
- **Predecessor mechanism:** refuted.
- **Prompt-cache mechanism:** refuted by the cache-off pair.
- **Sequence-position mechanism:** confirmed by the seeded shuffle.
- **Ontology coverage audit:** kept. It criticises the benchmark rather than the
  models.
- **Template mislabelling audit:** kept with counts from the source corpus.
- **Corpus regeneration attempt:** kept as a document review. The generator inputs
  were missing, so no regeneration result is claimed.
- **Second independent corpus:** remains open and limits every model comparison.

No external source or interview carries a material conclusion.
