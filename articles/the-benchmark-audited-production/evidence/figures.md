# Figure provenance and reporting record

Paths below are relative to the shared series evidence base at
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`.

## Production and scorer audits

| finding | evidence | weight |
|---|---|---|
| three names for one entity | `MEASUREMENT_LOG.md`, production identity audit | static source audit plus production observation; source snapshot not committed |
| migration lost the merged memory | `MEASUREMENT_LOG.md`, migration test | first-party runtime test against the production engine |
| negation discarded | `harness/harness/score.py`; prompt examples in `harness/harness/prompt.py`; production audit in `ARTICLE_NOTES.md` | scorer/source comparison |
| retraction table, 132-note slice | affected prediction files under `results/v5-v7-1k/`; counts in `ARTICLE_NOTES.md` | first-party measurement |
| one polarity error in 1,738 ordinary notes | the same prediction files; recomputation recorded in `ARTICLE_NOTES.md` | first-party measurement, two models on one corpus |
| ontology fragmentation counts | v5 corpus under `corpus/data/corpora/v5/`; ontology audit in `MEASUREMENT_LOG.md` | corpus and static source audit |
| fragmentation rate 21.0% to 13.0%, split 5.68 ontology and 2.34 prompt | `results/ontology-ab-20260812/` in the head-to-head article: both prediction files, `fragmentation.json`, and `PROVENANCE.md` | first-party measurement, 1,001 notes per arm, one model on one card |

## Reporting inventory and disposition

- **Production identity test:** kept. The substitute-engine test that initially
  passed was insufficient and is described as such.
- **Migration observation:** kept. It is a runtime result, not inferred from the
  migration source alone.
- **Negation audit and 132-note slice:** kept. Model extraction and production
  usability are reported as separate stages.
- **Ontology review:** kept. The benchmark's own specification error remains in
  the article rather than being assigned only to production.
- **Interrupted fragmentation rerun:** dropped. The 223-note figures of 23.5%
  and 10.0% left no artifact, so nothing can say whether they disagree with the
  complete run because of sample size, model, or a different definition of
  novel. They are not reproduced and cannot be.
- **Post-fix fragmentation result:** now claimed, and smaller than the figure it
  replaces. The complete run gives 21.0% to 13.0%, a fall of 8.02 points against
  the 13.5 the provisional pair implied. The direction survived the rerun and
  the magnitude did not.
- **The split into ontology and prompt terms:** claimed, and it is the reason
  the rerun was worth a card. Rescoring the v7 predictions against the larger
  seed set moves 5.68 of the 8.02 points with no model involved, so most of the
  gain was definitional rather than behavioural. A single before-and-after number
  cannot show that, which is what the superseded figure was.

Both arms ran against one server process with the same weights, cache size and
concurrency, so the interpolated relation list is the only difference between
them. The rate is one proportion from one run and carries no interval; the
direction is not in doubt and the second decimal is not defended.

The production source snapshot and migration output are not committed to this
repository. Those observations are therefore single-sourced to the reporting
ledger, and the article does not present them as independently reproduced.
