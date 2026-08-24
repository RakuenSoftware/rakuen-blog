# EuroBERT-15 fact-extraction corpus

Six static test sets extend the English fact-extraction benchmark with examples
generated from pinned open-source projects in EuroBERT's 15-language scope.

| File | Rows | Contents |
| --- | ---: | --- |
| `gold_1k.jsonl` | 1,001 | existing English small tier |
| `gold_2k.jsonl` | 2,000 | 1k English plus 999 multilingual rows |
| `gold_3k.jsonl` | 3,002 | existing English middle tier |
| `gold_5k.jsonl` | 5,000 | 3k English plus 1,998 multilingual rows |
| `gold_10k.jsonl` | 10,000 | existing English large tier |
| `gold_20k.jsonl` | 20,000 | 10k English plus 10,000 multilingual rows |

The English tiers remain authoritative under the published article's evidence
tree. The builder reads those files on every run and copies them byte-for-byte,
so an English correction automatically appears in its multilingual superset.

## Languages and sources

The language set follows the
[EuroBERT model card](https://huggingface.co/EuroBERT/EuroBERT-210m): English,
French, German, Spanish, Chinese, Italian, Russian, Polish, Portuguese,
Japanese, Vietnamese, Dutch, Arabic, Turkish, and Hindi.

English comes from the existing benchmark. The 10,000 added rows are balanced
across the other 14 languages, with 714 or 715 rows per language. Their facts
come from these open-source projects:

- the French, German, Chinese, Italian, Russian, Polish, Portuguese, Japanese,
  Vietnamese, and Arabic Vue documentation projects;
- the Spanish and Turkish Python documentation projects; and
- Django, whose source tree and locale catalogues supply Dutch and Hindi rows.

Every project is pinned by full Git commit in `source-projects.json`. Every
generated row records the repository URL, commit, and exact source path or
paths used to construct it.

The notes are synthetic descriptions of real repository-tree facts. They are
not translations of the English corpus. Fact-bearing rows describe file
location or project membership; factless rows use proposed moves, explicit
negation, and deliberately ambiguous mentions. The generation schedule follows
the 10k English corpus and preserves its 32.15% factless share. English
fact-bearing categories without a direct repository-tree equivalent are
labelled `third_person` rather than carrying a misleading category name.

## Files

- `data/multilingual.jsonl` is the static 10,000-row non-English pool.
- `generated/v1/` contains the six complete test sets and `manifest.json`.
- `source-projects.json` pins the source repositories.
- `generate_multilingual.py` rebuilds the multilingual pool from checkouts of
  those pinned commits.
- `build_corpus.py` builds and validates the six tiers.
- `summarize_readability.py` reports JSON parse and schema-valid rates overall
  and for every language.

## Rebuild

With the repositories in `source-projects.json` checked out under a source
directory using their `checkout` names:

```sh
python3 benchmarks/multilingual-fact-extraction/generate_multilingual.py \
  --source-root /path/to/source-checkouts \
  --blueprint articles/local-llm-fact-extraction-head-to-head/evidence/raw/corpus/data/corpora/v5/gold_large.jsonl \
  --out benchmarks/multilingual-fact-extraction/data/multilingual.jsonl

python3 benchmarks/multilingual-fact-extraction/build_corpus.py build
python3 benchmarks/multilingual-fact-extraction/build_corpus.py validate
```

The builder rejects unsupported languages, duplicate IDs or notes, incomplete
source provenance, ungrounded gold endpoints, broken English nesting,
imbalanced language slices, wrong tier sizes, and stale generated outputs.

## Result reporting

Parse/read rates are first-class metrics. For every model run, report JSON
parse and schema-valid rates overall and per language, plus macro language
averages, transport failures, and truncated rows:

```sh
python3 benchmarks/multilingual-fact-extraction/summarize_readability.py \
  --gold benchmarks/multilingual-fact-extraction/generated/v1/gold_2k.jsonl \
  --pred path/to/model.pred.jsonl \
  --json-out path/to/model.readability.json
```

Run the contract tests with:

```sh
python3 benchmarks/multilingual-fact-extraction/test_build_corpus.py
python3 benchmarks/multilingual-fact-extraction/test_summarize_readability.py
```
