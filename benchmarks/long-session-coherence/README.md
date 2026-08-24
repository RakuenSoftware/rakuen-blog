# Long-Session Coherence 100

Long-Session Coherence 100 (LSC-100) measures whether a model remains internally
consistent through a long chat. It is designed for paired comparisons of lower
weight quants of the same model, not for comparing unrelated model families.

The corpus contains 100 deterministic synthetic conversations across ten
domains. Every conversation has nested context checkpoints at nominal 4k, 8k,
16k, 32k, and 64k tokens and four scored probes at each checkpoint. The probes
cover current state, revisions, withdrawn decisions, standing instructions,
entity continuity, commitments, missing information, contradiction detection,
and task continuation.

## Grading

A conversation has 20 ordered probes. A probe passes only when the response is
valid JSON, satisfies the response schema, gives the correct current answer,
and cites the required source turn or turns.

Let `k` be the number of consecutive probes passed before the first failure:

```text
incomplete conversation:  score = 50 * (k / 20)
complete conversation:    score = 100
```

For example, a model that remains coherent through 12 of 20 probes and then
fails scores 30 for that conversation. No incomplete conversation can score 50
or more.

The corpus score is the macro-average of the 100 conversation scores, which is
equivalent to:

```text
50 * full_completion_rate + 50 * mean_survival_fraction
```

Always report the numeric score, full-completion rate, mean survival, first
failure distribution, JSON parse rate, schema-valid rate, and performance
telemetry separately. A run is labelled `fully_coherent` only when it completes
all 100 conversations. The numeric score must not be presented as that claim.

## Two evaluation tracks

The primary `fixed_replay` track gives every quant the same canonical history.
Each probe branches from the recorded transcript and the model's response is not
placed into later checkpoints. This isolates quantisation effects and supports
paired statistics.

The secondary `live_session` track replaces canonical assistant turns with the
model's own replies and appends probe replies to the session. It measures
cumulative practical drift, but sessions diverge and its scores must not be
mixed with fixed-replay scores. The same probe gold and survival rule apply.
For an ordinary assistant turn, send the scripted user turn and append the
model reply in place of the corpus's `canonical` assistant turn. At a probe
boundary, send the probe, append and score the reply, then continue with the
next scripted user turn. Start every conversation with an empty context.

## Response and result contract

Every probe asks for exactly one JSON object:

```json
{"answer":"current value","evidence_turn_ids":["T0042"],"confidence":0.91}
```

Run results are JSON Lines records with `conversation_id`, `probe_id`, and the
raw `response`. Telemetry fields are optional but should include
`prompt_tokens`, `completion_tokens`, `prompt_eval_tokens_per_second`,
`decode_tokens_per_second`, `ttft_ms`, `truncated`, and `error`. See
`conversation.schema.json`, `result.schema.json`, and `run-config.schema.json`.

## Quant controls

Within a paired quant ladder, hold the base weights, tokenizer, chat template,
runtime build, context size, KV-cache precision, Flash Attention setting,
sampling settings, completion budget, hardware, and probe order constant. A
typical ladder is Q2_K, Q3_K_M, Q4_K_M, Q5_K_M, Q6_K, Q8_0, and BF16/FP16 when
practical. Treat KV-cache quantisation as a separate experiment.

The nominal checkpoint sizes are deterministic estimates. Record actual prompt
token counts from the model tokenizer for every response. Reject or flag a run
that silently truncates the supplied history. The generator reserves 6.25% of
each context band, with a minimum 512-token reserve, for the scored probe and
completion rather than filling the entire window with transcript history.

## Commands

Rebuild and validate the checked-in corpus:

```sh
python3 benchmarks/long-session-coherence/generate_corpus.py
python3 benchmarks/long-session-coherence/long_session_bench.py validate
```

Inspect one fixed-replay request without materialising every repeated prefix:

```sh
python3 benchmarks/long-session-coherence/long_session_bench.py request \
  LSC-001 P001 > request.json
```

Grade a run:

```sh
python3 benchmarks/long-session-coherence/long_session_bench.py grade \
  path/to/model.results.jsonl --out path/to/model.report.json
```

Compare two quants of the same base model with a paired conversation bootstrap:

```sh
python3 benchmarks/long-session-coherence/long_session_bench.py compare \
  path/to/q8.results.jsonl path/to/q3.results.jsonl \
  --out path/to/q3-vs-q8.report.json
```

The comparison reports candidate-minus-baseline score and completion deltas,
a deterministic 95% paired-bootstrap interval, and checkpoint retention deltas.
Do not use this command for unrelated base models or mismatched run controls.

Run the contract tests:

```sh
python3 benchmarks/long-session-coherence/test_generate_corpus.py
python3 benchmarks/long-session-coherence/test_long_session_bench.py
```
