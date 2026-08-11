# The 12B Synthesis Run Scored Higher and Missed the CPU Question

Two 10,000-case GPU configurations measure a quality-and-latency tradeoff. They
do not select the production CPU model the original campaign set out to choose.

## Status

Publication-ready as of 2026-08-09. Not yet published. The article is deliberately
narrower than the planned multi-model selection because only two complete model
runs are committed here.

## Evidence

| path | contents |
|---|---|
| `benchmarks/fixtures/ab-v1/synthesis.jsonl` | 10,000 frozen silver-label cases |
| `benchmarks/ab-v1/gemma4_e2b/` | raw rows, summary, validation and hardware record |
| `benchmarks/ab-v1/gemma4_12b/` | raw rows, summary, validation and hardware record |
| `benchmarks/ab-v1/paired_content_bootstrap.py` | paired content-score interval |
| `evidence/figures.md` | figure map and reporting disposition |

Both summaries carry suite manifest SHA-256
`16d2c16add86052ff24be410699ab9452ee1a36252de6dba31ab5391de7ab81c`.
The E2B file has 10,000 rows and cases. The 12B file has 10,013 rows for 10,000
cases; analysis keeps the last row for each `case_id`, preserving failed attempts
and their successful retries.

The E2B response for case `9490bd93bed2a6ceabb59f3f` matched a credential-syntax
scanner after scoring. Its committed row replaces only the response text, records
the original SHA-256 and preserves the pre-redaction metrics.

## Reporting record

The planned wider Tier-A model matrix is not committed in this article folder and
contributes no result. This version answers the supported two-run question and
states that neither run measures CPU affordability. There are no interviews,
external benchmark claims or material criticisms requiring a reply.
