# Roundtable review: synthesis model selection

The unpublished article at
`article/synthesis-model-selection.md` received four review passes on August 15,
2026, through aimee `pre-merge-safety-1696-g49b2d315e5`. Each pass reviewed the
current file rather than an earlier commit.

## Findings and disposition

1. The first pass rejected language that treated a confidence range crossing
   zero as proof of equivalence. It also found missing paired comparisons in the
   Numbers tab and an unstated denominator for Muse's 2.94-times token total.
   The article now says “not statistically separated”, states that this does not
   establish equivalence, exposes every prose comparison in Numbers, and names
   E2B's 141,295-token denominator.
2. The second pass found an incorrect “both Qwen rows” caption despite three
   displayed Qwen configurations. It also found technical abbreviations in the
   table before their prose expansions. The caption now says all three Qwen
   configurations use `Q4_K_M`; QAT, UD-QAT, MTP, DFlash, JSON and GiB are
   expanded before the first figure, and `p95` is written as 95th percentile.
3. The third pass required the Qwen and Muse mechanism comparisons to appear in
   a reader-facing Numbers view. The added Outcome/Numbers figure now carries
   the completion-token totals, decode rates, medians, parse and schema rates,
   required-field recall and document-summary scores used by the prose.
4. The fourth pass returned: “Roundtable approved the artifact with no
   findings.”

## Independent checks supplied beside review

- `python3 tools/voice_gate.py synthesis-model-selection`: pass.
- `python3 -m unittest tools.test_voice_gate -v`: two tests passed.
- `git diff --check`: pass.
- Python compilation for every `benchmarks/ab-v2/*.py` file: pass.
- Raw audit: nine configurations, 1,000 latest successful rows each; recomputed
  content F1, median latency and completion-token totals match
  `canonical/analysis-20260815.json`.
- Analysis replay: 10,000 paired resamples with seed 20260815 reproduced SHA-256
  `c825f90f1a4a8d5e6ef4d9e9de2a9cba43c17527025d9fd7a2c71201b615c095`.
- Figure audit: three figures, three Numbers tables, unique radio identifiers
  and a matching label for every control.

The review approves the completed `Q4_K_M` matrix article. Qwen3.8 UD-Q4 remains
a separate pending run and cannot silently replace this result.
