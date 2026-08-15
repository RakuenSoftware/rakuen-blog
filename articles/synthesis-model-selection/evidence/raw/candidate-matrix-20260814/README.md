# Candidate matrix provenance

These directories preserve the 2026-08-14 GPU benchmark campaign. Paths in
this note are relative to this directory. Raw files are append-only.

## Canonical run

The canonical command on `admin@192.168.1.254` was:

```text
python3 benchmarks/ab-v2/run_candidate_matrix.py \
  --bundle benchmarks/fixtures/ab-v1 \
  --results-root results-canonical-1k-udqat \
  --max-cases 1000
```

The controller selected `Vulkan1`, an AMD Radeon RX 7900 XTX, and refused any
occupied port, wrong loaded filename, wrong speculation state, mismatched
candidate record or incomplete result population. Each candidate used one
worker, one slot, 8,192 context tokens and strict JSON-schema responses.

Every Gemma target was the QAT repository's `UD-Q4_K_XL` artifact, described in
the article as UD-QAT. Gemma 4 and both Qwen families used multi-token
prediction. Muse Glimmer used no draft model, keeping DFlash off, and passed
`reasoning_strength=low`; its reasoning remained inside the timed request.

The raw rows, summaries, hardware records and logs for all nine completed
configurations are under `canonical/`. `RUN_STATE.json` records completion.
`analysis-20260815.json` validates the matched population and configuration,
then calculates 10,000 paired case-bootstrap replicates with seed 20260815 and
NumPy 2.5.0. Its SHA-256 is
`c825f90f1a4a8d5e6ef4d9e9de2a9cba43c17527025d9fd7a2c71201b615c095`.

The canonical Muse directory contains the resumed 1,000-case result. The 289
rows saved before interruption remain separately under `interrupted/`; they
were not deleted or substituted.

## Preflight disposition

- `preflight/results-smoke/` stopped before any case when the target was changed
  from Q4_0 to UD-Q4_K_XL.
- `preflight/results-smoke-udqat/` used llama.cpp's generic `grammar` field.
  Seven models completed diagnostic rows, but Muse failed at the transport
  layer. Those scores are invalid for comparison because production aimee uses
  strict `response_format` JSON schema.
- `preflight/results-smoke-jsonschema-muse/` proved that Muse exhausted the
  output limit in mandatory reasoning when no reasoning-strength setting was
  supplied. Its two zero scores are invalid as model-quality results.
- `preflight/results-smoke-jsonschema-muse-low/` and
  `preflight/results-smoke-jsonschema-gemma-udqat/` are two-case transport
  checks for the corrected request.
- `preflight/results-smoke-jsonschema-udqat-final/` is the complete ten-case
  matrix check. It validates the harness only and contributes no published
  accuracy or speed number.

The fixture and copied result trees passed the credential, email, private-key,
IP-address and home-username scan in `build_254_fixtures.py` before commit.
