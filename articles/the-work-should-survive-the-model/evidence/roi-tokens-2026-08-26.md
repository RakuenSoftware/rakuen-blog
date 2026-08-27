# Token ROI analysis, 2026-08-26

This analysis asks the narrowest useful ROI question available in the tracked
first-party evidence: how many provider-recorded tokens were consumed for work
that passed its task test, and how many frontier-model tokens did delegation
displace.

It does not convert tokens to dollars. Input, cached input and output have
different prices, model rates change and customer contracts differ.

## Quality-adjusted provider tokens

The primary source is the completed E6 paired coding experiment at Aimee commit
`aa8c40e9d75449774c9b0b630bb8f1037efb8097`. It used `gpt-5.6-sol` at medium
reasoning on eight tasks in each arm. Hidden tests scored task success. The run
completed 32 cells across four arms with no exclusions or retries. This analysis
uses only the `standard` and `on` arms.

The checked-in provider result contains task success and uncached input tokens.
The preserved `codex.jsonl` streams contain the provider's final input, cached
input and output counts. The analysis script hashes every stream and verifies
that `input_tokens - cached_input_tokens` equals the uncached count in the
checked-in result before accepting it.

| measure | standard | Aimee on | change |
|---|---:|---:|---:|
| successful tasks | 5/8 | 6/8 | +1 |
| input tokens | 1,115,730 | 1,046,028 | -6.2% |
| cached input tokens, included above | 873,216 | 802,304 | -8.1% |
| uncached input tokens, included above | 242,514 | 243,724 | +0.5% |
| median uncached input per attempt | 33,626 | 34,009 | +1.14% |
| output tokens | 19,550 | 16,178 | -17.2% |
| input plus output tokens | 1,135,280 | 1,062,206 | -6.4% |
| input plus output tokens per successful task | 227,056 | 177,034 | -22.0% |

The quality-adjusted calculation is:

```text
standard: 1,135,280 / 5 = 227,056 tokens per successful task
Aimee on: 1,062,206 / 6 = 177,034 tokens per successful task
change:   (177,034.33 - 227,056) / 227,056 = -22.03%
```

The paired outcomes contained one recovery and no regression: task `c05` failed
in `standard` and passed in `on`; the other seven pass or fail outcomes were
unchanged. With only one run in each condition and eight tasks, the result is
directional. It does not establish a stable population effect. The article
therefore publishes the counts and sample size rather than a generalized
expected saving.

The original E6 validation qualified on wall time, not tokens. It reported the
median uncached input above, which rose 1.14 percent. This ROI analysis uses
summed consumption because a bill covers every task, then divides that sum by
the number of passing tasks. Both views are retained.

The raw input-plus-output sum is useful as token volume, but it is not a dollar
proxy. Cached input usually has a different rate from uncached input, and output
usually has another. Reasoning output is already included in output tokens and
is not added twice.

## Frontier-model displacement through delegation

The supporting source is the tracked 50-instance SWE-bench Lite cost-savings
campaign at Aimee commit `4b46f973a5a6c2b21c95ce4db9b4465fdfc92b47`.
The default condition used the primary `gpt-5.6-sol` agent. The delegated
condition used the same frontier model as manager and a worker pool of
MiniMax-M3, mimo-v2.5-pro and kimi-k2.7-code.

| measure | default | delegated | change |
|---|---:|---:|---:|
| frontier-model tokens | 464,252 | 192,406 | -271,846, or -58.6% |
| tasks with lower frontier use | | 45/50 | |
| tasks with higher frontier use | | 5/50 | |
| median per-task frontier-token reduction | | 60.8% | |

This result deliberately receives a narrower label than total savings. The
ledger windows count the frontier manager's prompt and completion tokens. They
exclude worker-model tokens. The campaign also did not grade task correctness.
It therefore measures frontier-model displacement, not all-model tokens and not
cost per correct task.

The 50-task result is used instead of the tracked ten-task subset or the
separate 12-task multifile run because it is the largest recorded corpus under
this protocol. Publishing the 87.0 percent multifile reduction beside the
58.6 percent result would add a more favorable ungraded number without fixing
the worker-token or correctness limits.

## Reproduction and retained evidence

Run from this article directory:

```bash
python3 evidence/analyze_roi_tokens.py \
  --aimee-repo /home/virant/dev/aimee \
  --provider-stream-root /home/virant/.local/share/aimee/e6-paired-aa8-20260730-v2/cell-artifacts
```

The append-only derived record is
`evidence/raw/roi-token-analysis-2026-08-26.json`. It records the command,
environment, checked-in source hashes, all 16 provider-stream hashes, usage
fields, exact calculations, expected and actual row counts, and interpretation
limits. No new provider call was made.

The local provider streams are retained outside the blog repository because
they contain full agent transcripts. The checked-in raw record retains their
hashes and the usage fields used here. The task success and uncached-input
values remain independently reproducible from the checked-in Aimee result.
