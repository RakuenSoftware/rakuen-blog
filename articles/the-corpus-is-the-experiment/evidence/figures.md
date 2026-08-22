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
| fragmentation rate 21.0% to 13.0%, split 5.68 ontology and 2.34 prompt | `results/ontology-ab-20260812/`: both prediction files, `fragmentation.json`, and `PROVENANCE.md` |
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
- **Interrupted fragmentation rerun:** dropped. The 223-note figures of 23.5%
  and 10.0% left no artifact, so nothing can say whether they disagree with the
  complete run because of sample size, model, or a different definition of
  novel. They are named in the article only as the superseded pair.
- **Post-fix fragmentation result:** cited, not claimed here. The complete
  2026-08-12 run gives 21.0% to 13.0%, and this article reports only that
  headline and its direction. The split into definitional and behavioural terms,
  the artifacts and the reporting record belong to
  `the-benchmark-audited-production`, which owns the measurement.
- **Sequence-position controls:** cited, not reproduced. The predecessor and
  prompt-cache refutations and the seeded shuffle are owned by
  `repeatable-is-not-identical`. This article keeps only the tier-containment
  result, which is a corpus-assembly finding.
- **Template mislabelling audit:** kept with counts from the source corpus.
- **Corpus regeneration attempt:** kept as a document review. The generator inputs
  were missing, so no regeneration result is claimed.
- **Second independent corpus:** remains open and limits every model comparison.

No external source or interview carries a material conclusion.
