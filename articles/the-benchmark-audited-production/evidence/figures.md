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
| fragmentation rate 23.5% to 10.0% | `ARTICLE_NOTES.md` | provisional interrupted run; no complete raw artifact |

## Reporting inventory and disposition

- **Production identity test:** kept. The substitute-engine test that initially
  passed was insufficient and is described as such.
- **Migration observation:** kept. It is a runtime result, not inferred from the
  migration source alone.
- **Negation audit and 132-note slice:** kept. Model extraction and production
  usability are reported as separate stages.
- **Ontology review:** kept. The benchmark's own specification error remains in
  the article rather than being assigned only to production.
- **Interrupted fragmentation rerun:** kept as provisional, with its incomplete
  status next to the number.
- **Post-fix fragmentation result:** not claimed because it was not re-measured.

The production source snapshot and migration output are not committed to this
repository. Those observations are therefore single-sourced to the reporting
ledger, and the article does not present them as independently reproduced.
