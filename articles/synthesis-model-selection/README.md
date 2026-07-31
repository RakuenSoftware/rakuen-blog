# Synthesis / extraction model selection

**Status: not written.** This folder holds evidence for a future article. Nothing
here has been turned into prose yet.

## What the question is

Which model performs Tier-A synthesis and extraction — turning a note into
structured, schema-valid triples — at a quality and latency the CPU tier can
afford. That is a different decision from which model *embeds*, on a different
gold set, and it is deliberately kept out of the retrieval article
([we-measured-our-reranker-and-deleted-it](../we-measured-our-reranker-and-deleted-it/)).

## What is here

| folder | what it is |
| --- | --- |
| `benchmarks/ab-v1/gemma4_e2b/` | Gemma-4 E2B on the ab-v1 synthesis view, 10,000 cases |
| `benchmarks/ab-v1/gemma4_12b/` | Gemma-4 12B on the same view |
| `benchmarks/fixtures/ab-v1/synthesis.jsonl` | the synthesis view of the frozen suite |

These share the ab-v1 case population and manifest SHA-256
`16d2c16add86052ff24be410699ab9452ee1a36252de6dba31ab5391de7ab81c` with the
retrieval article's evidence. Same 10,000 cases, different task view. The corpus
itself lives with the retrieval article rather than being duplicated here.

Raw logs are append-only. Select the last row per `case_id` before computing
metrics — E2B has 10,000 unique cases and 12B has 10,013 rows for 10,000 cases,
with failed attempts superseded by retries.

One redaction to know about: E2B's generated response for case
`9490bd93bed2a6ceabb59f3f` matched a credential-syntax scanner after scoring. The
committed row replaces only that response text, records `response_redacted: true`
and the original SHA-256, and preserves its pre-redaction metrics.

## What is missing

The larger Tier-A campaign is not here yet. It lives on the benchmark host at
`/opt/tierA/bench/tier-a` (LXC 140 on `.253`) and covers roughly 16 models scored
on GPU and 13 timed on CPU — granite, SmolLM2, LFM2, gemma-3/3n/4 and Qwen3/3.5,
down to 230M — with ablation, diagnostics and prompt-fix arms, its own 70-note
gold set, and its own labelling rules. It was still running a `ceiling` arm
against gemma-4-12B when this folder was created, so it has not been ingested.
Pull it once that run completes.
