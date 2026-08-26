# Figure provenance and reporting record

Paths below are relative to the shared series evidence base at
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`.

## Measurements used

| article section | measurement | artifact or record |
|---|---|---|
| confidence gate | floored and unfloored scores, including the zeroed runs | `results/noconf/`; `harness/harness/score.py` |
| confidence gate | 1B against 3B Granite, floored and unfloored | `results/noconf/`; comparison in `ARTICLE_NOTES.md` |
| two zeroes | parse-success and parse-failure examples that both printed zero | `MEASUREMENT_LOG.md`, scorer and guard audits |
| tool-call envelope | parse collapse with normal completion lengths | `MEASUREMENT_LOG.md`, defects 7 and 8 |
| context exhausted | token totals and the missing truncation guard | `ARTICLE_NOTES.md`, context-length audit; affected files under `results/diagnostics/` |
| identity guard | model-name guard rejecting an otherwise serving model | `MEASUREMENT_LOG.md`, host-placement defect record |
| speculative decoding | absence of draft counters on the throughput run | `results/vast/Qwen3.6-35B-A3B.UD-Q4_K_XL.live.pred.jsonl`; matching 27B file |
| size ladder | E2B, 26B-A4B, 12B and 31B scores | `results/qat-vs-ud/gemma-4-E2B-it.qat.score.json`; `results/ct140/gemma-4-26B-A4B.qat-unsloth-UDQ4.5080.score.json`; `results/vast/gemma-4-12B-it.qat-UD-Q4_K_XL.live.score.json`; `results/ct140/gemma-4-31B-it.qat-UD-Q4_K_XL.xtx.score.json` |
| size ladder | E2B to 31B endpoint, +0.0465, range +0.0220 to +0.0712 | `harness/harness/bootstrap_ci.py`; mapped in the head-to-head `evidence/figures.md` |
| score floor | 15 gold facts in 40 unreadable rows, +0.0038 repair bound | `results/qat-vs-ud/gemma-4-E2B-it.qat.pred.jsonl`; `MEASUREMENT_LOG.md`, floor audit |
| score floor | two 12B runs parsing 0.90 and 0.92 with no context exhaustion | the two 12B prediction files under `results/`; `MEASUREMENT_LOG.md`, floor audit |

The third kind of zero comes from a different benchmark and a different evidence
base. Its artifacts are not under the series tree above:

| figure | artifact | kind |
|---|---|---|
| `cached_input_tokens: 0` in the committed cells | `articles/three-zeros-and-a-wrong-answer/benchmarks/ct403-results/`, 81 cells across eight run labels | benchmark artifact, committed and verified byte-identical |
| the gateway dropped the nested cached-token field; three sites read only the flat counters | `aimee`, `src/openai_shape.c` and `src/agent_runtime.c` | static source audit |
| the fix | `aimee` PR 2569, merged 2026-08-11 | merged change, named in the text |

That article is retired and unpublished. Its benchmarks and figure map are
retained where they are, because this article cites them and the repository rule
requires the artifact to stay reachable.

Two figures from that article are deliberately **not** carried here. Its cache-rate
series and its cost table trace to a `token_audit` database and a results tree
that its own reporting record says are not present on this machine, so neither can
be re-derived. This article therefore states the serialisation defect and its fix,
which the source audit and the merged change support on their own, and makes no
claim about how much the corrected accounting moved the cost.

Every adjacent-model interval printed in the article is reproduced in
`articles/local-llm-fact-extraction-head-to-head/evidence/figures.md` under
"Intervals".

## Speculation-on control, 2026-08-10

| figure | artifact |
|---|---|
| 27B, 79.0% of 1,020,888 drafted tokens accepted | `results/qwen36-mtp-xtx/Qwen3.6-27b.Q4_K_M.xtx.mtp-on.pred.jsonl`, summed over `draft_n` and `draft_n_accepted` |
| 35B-A3B, 76.6% of 1,034,913 accepted | `results/qwen36-mtp-xtx/Qwen3.6-35b.Q4_K_M.xtx.mtp-on.pred.jsonl`, same fields |
| no draft counts on either speculation-off run | the matching `.mtp-off.pred.jsonl` files; `draft_n` is absent or zero on all 1,001 rows |
| 0.7180 and 0.7177; 0.7495 and 0.7427 | the four matching `.score.json` files, strict F1 |

These same-card pairs postdate the original reporting and serve as a positive
control: they show what a drafted run records, which is what the banked
`results/vast/` runs do not. A first 35B-A3B speculation-off attempt was stopped
at 115 rows and is retained beside them as
`Qwen3.6-35b.Q4_K_M.xtx.mtp-off.aborted-115rows.pred.jsonl`, with its stop reason
in `results/qwen36-mtp-xtx/ABORTED-2026-08-10.md`. It carries no result; the
completed 1,001-row rerun supplies the speculation-off side.

## Reporting inventory and disposition

- **Confidence-floor probes:** kept, with floored and unfloored results
  distinguished. The inverted size comparison is the reason the floor was
  replaced rather than retuned.
- **Model guard and host observations:** kept as single-sourced observations from
  `MEASUREMENT_LOG.md`; no raw API response was preserved.
- **Speculative-decoding attribution:** withdrawn as a mechanism claim and
  narrowed to the run. The 2026-08-10 same-card pairs are reported as the control
  that establishes the missing signature, not as a restatement of the original
  claim.
- **Paired bootstrap comparisons:** kept. The adjacent nulls and the endpoint
  difference remain distinct, which is the point of that section.
- **Causal explanation for E4B's partial reasoning:** withdrawn. The article says
  the cause is unexplained here and points at the open investigation rather than
  closing the thread.
- **Score floors:** kept as bounds, not corrections. The +0.0038 figure is the
  most a perfect repair could add, and the 12B pair is reported as a lower bound
  because the equivalent repair bound was never computed for it.
- **Unwritten cache field:** kept, and it is the one finding here from outside the
  extraction campaign. It is included because it is the clearest case of the
  pattern: the zero was not small, noisy or variable, it was exact in every cell.

## Findings moved out of this article

The two compilations merged here restated findings measured in more depth
elsewhere in the series. Each is now reported once, in the article holding its
evidence. The live article links the published destinations and records the rest
as unpublished:

| finding | now reported in |
|---|---|
| startup time inside throughput; orphaned clients; rented-fleet accounting; timeout diagnoses | `the-parallelism-limit-was-never-vram`, publication-ready and unpublished |
| sequence position; borrowed 0.0105 threshold; cross-card identity | `repeatable-is-not-identical`, publication-ready and unpublished |
| shared slots against speculation, and self-reproduction under concurrency | [Local LLMs: Speculative Decoding](https://rakuensoftware.com/blog/speculative-decoding-was-free), published |
| suppressed reasoning pass; withdrawn +0.084 constant | `one-sentence-turned-the-reasoning-off`, publication-ready and unpublished |
| factless strata; scorer null categories displayed as 0.0 | `the-corpus-is-the-experiment`, publication-ready and unpublished |
| bit-width ladder and the QAT deltas | [Quantization Barely Mattered Until Two Bits](https://rakuensoftware.com/blog/which-quant-beats-how-many-bits), published |
| 31B and 12B QAT tie, recall against invention | [Local LLMs: Fact Extraction Head to Head](https://rakuensoftware.com/blog/local-llm-fact-extraction-head-to-head), published, which reports the same recall-against-restraint trade |
| sparse throughput and resident size | `the-parallelism-limit-was-never-vram`, publication-ready and unpublished |

No external source, interview or vendor claim carries a material conclusion.
