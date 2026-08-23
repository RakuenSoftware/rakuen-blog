# Figure provenance and reporting record

Every measurement in the article comes from the 2026-08-16 campaign: 37 runs,
seven models, one RTX 5080, each run scored on 1,001-note fact extraction and on
a 1,000-case synthesis fixture.

The earlier draft of this article measured a different, smaller set (bit-width
ladders on four small dense models, plus SmolLM3 and 10,000-note ladders). None
of that is cited in the article now. Its provenance map is reachable through git
history at this path, and its raw artifacts are retained under the shared series
evidence base described at the end of this file.

## Vendored evidence

| file | contents |
|---|---|
| `campaign-results/arms-2026-08-22.json` | all 37 runs: extraction scores, synthesis summary, throughput distribution, VRAM and offload state, completion-token stats |
| `campaign-results/extraction-pairs-2026-08-22.json` | 45 paired bootstrap comparisons, seed `20260809`, 20,000 replicates, one comparison per process |
| `campaign-results/extraction-pairs-2026-08-22.raw.txt` | the scorer's own output for each of those comparisons, unparsed |
| `campaign-results/synthesis-pairs-2026-08-22.json` | 44 paired comparisons on mean content F1, seed `20260809`, 5,000 replicates |
| `moe-ladder-plan-2026-08-16.md` | the plan, registered before any run started |
| `moe-ladder-measurement-log-2026-08-16.md` | eleven defects, two discarded campaigns, and what each fault would have corrupted |

Replicate counts differ by task on purpose. Each matches the published series it
belongs to, so an interval here is comparable to earlier work on the same task
and only roughly comparable across the two.

## Where each claim comes from

| claim in the article | source |
|---|---|
| 45 extraction comparisons, 15 separate; 44 synthesis, 10 separate | the two pair files; counted by `separates` |
| every sub-four-bit rung against its own Q4, six rows | `extraction-pairs`, baseline `<model>.base.q4` |
| dense mean 0.153, mixture mean 0.031, worst dense 9.5x worst mixture | computed from those six rows |
| Qwen3.6-35B-A3B at one bit scores 0.6817 | `arms`, `qwen36-35b-a3b.base.q1.extraction.strict.f1` |
| 12B emits 7,609 tokens per note against 958 | `arms`, `completion_tokens.median`, computed by the scorer over the 1,001 scored notes |
| QAT Q2 minus QAT Q4: −0.4330 and −0.3341 | `extraction-pairs`, baseline `<model>.qat.q4` |
| QAT Q2 minus non-QAT Q2: −0.3511 and −0.2982 | `extraction-pairs`, baseline `<model>.base.q2` |
| 12B QAT Q4 separates on synthesis, +0.0088 | `synthesis-pairs`, `gemma4-12b.qat.q4` against `.base.q4` |
| E2B 65 tokens against 520, E4B 611 against 297 | `arms`, `completion_tokens.median` for the four QAT and non-QAT Q2 runs |
| 26B-A4B Q4 is 16,222 MiB, 600 MiB too large | `arms`, `offload` field for `gemma4-26b-a4b.base.q4` |
| 3.3x throughput between 26B QAT Q4 and non-QAT Q4 | `arms`, `throughput.generation_tok_per_s.median`, 359.59 against 109.92 |
| Qwen 319.6 against 39.4 tok/s, 29 layers offloaded | `arms`, same field plus `offload_mode` |
| LFM2.5-8B-A1B 510.5, 433.2, 364.9, 66.9 | `arms`, same field across its four widths |
| five separations at four bits and above | `extraction-pairs`, filtered to rungs Q4 and up |
| 26B and Qwen Q8 minus Q4 nulls | `extraction-pairs` |
| synthesis moves 0.004 where extraction moves 0.036 | 12B Q2 rows in each pair file |

`campaign/check_article_intervals.py` enforces the table above for intervals: it
fails if the article prints a 95% range that no pair file reports, in either
direction. Figures are generated from the same evidence by
`campaign/build_figures.py` and installed by `campaign/install_figures.py`, so a
chart cannot state a number the bootstrap did not produce.

## Single-sourced and out-of-campaign

- **The earlier E4B six-bit result**, +0.0245 [+0.0091, +0.0405], is the one
  interval in the article not produced by this campaign. It comes from the
  earlier draft's ladder on different hardware and is cited as independent
  reproduction of the current +0.0235 [+0.0068, +0.0403]. It is exempted by name
  in `check_article_intervals.py`.
- **One bit was measured once**, on Qwen3.6-35B-A3B, the only model in the set
  publishing a one-bit build.
- **The architecture comparison rests on six points**, three dense and three
  mixture, and gemma-4 12B dominates the dense mean.
- **Offloaded throughput figures are lower bounds.** All six expert-offload runs
  used memory mapping against llama.cpp's load-time warning. This costs speed
  only, so the direction of the capacity finding is safe and its magnitudes are
  upper bounds on the cost.
- **Completion-token medians come from the scorer**, over the 1,001 scored
  notes. The server log counts requests instead, which includes warm-ups and
  retries and gives a different median; the two must not be mixed.
- **Two runs predated the throughput instrumentation.** `lfm25-2.6b` at Q4 and Q6
  carried only a single warmed probe in `arm.json`; both distributions were
  recovered from their retained server logs by `campaign/throughput.py`, 1,003
  samples each.

## Shared series artifacts

Raw artifacts for the whole series live under
`articles/local-llm-fact-extraction-head-to-head/evidence/raw/`:

| directory | contents |
|---|---|
| `results/` | every prediction file, score file and run log produced by the benchmark |
| `corpus/` | corpus v5, the gold sets at 1,001, 3,002 and 10,000 notes |
| `harness/` | the runner, scorer, bootstrap and orchestration scripts |
| `ARTICLE_NOTES.md` | the running findings ledger |
| `MEASUREMENT_LOG.md` | the defect log, including every withdrawn claim |

Campaign raw artifacts remain on the benchmark host at
`/opt/campaign/results/<label>/` and `/opt/campaign/results-synthesis/<label>/`.
What the article depends on is vendored above; the host copies are the fuller
record, including server logs.

## Reporting record

This article reports first-party measurement only. There are no external sources,
interviews or vendor claims in it, so there is no right-of-reply obligation
outstanding.
