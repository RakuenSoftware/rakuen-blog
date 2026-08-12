# Figure provenance and reporting record

## Correction, 2026-08-12: MCP does not forbid batching

The published piece said the protocol has no `&&` and that a tool call cannot
compose. That is wrong. A client can emit several tool calls in one assistant
message and the schema permits it.

The observation that stands is narrower and is the author's, from reading the
transcripts: no model tested emitted more than one tool call in a message, for
any tool, in any cell.

**This is not checkable from the committed artifacts.** `summary.json` records
`item_types` and `tool_calls` as totals, with no ordering and no grouping by
assistant message, so a cell showing six `mcp_tool_call` items against five
`agent_message` items is consistent with both batched and unbatched calls. The
raw event streams would settle it and are not committed; only their `sha256` is,
in each cell's `raw_stream_sha256`.

Committing those streams, or a per-message tool-call count derived from them, is
what would move this from an observation to a figure. Until then it is reported
as observed and marked as single-sourced to the transcripts.

The measured cost does not change. The recommendation does not change. What
changes is the cause, and therefore the next experiment: ask the model directly
for parallel tool calls and see whether the count moves. Not yet run.

The argument here is about protocol shape and the evidence for it is one
benchmark table. The cells behind that table are now committed, and they do not
support the table's central split.

## The cells, located and committed

The 2026-08-11 22:00 run was recovered from CT403 on 2026-08-12 and committed
under `benchmarks/`. It is not one campaign directory. It is three, one per
configuration, and they were identified by matching the credit signature in the
reporting record rather than by name:

| directory | configuration | cells |
|---|---|---|
| `results-base-now` | plain Codex | 3 |
| `results-rt-off` | ours, `roundtable_review` removed from the tool surface | 3 |
| `results-rt-on` | ours, as shipped | 3 |

All nine cells report `model: gpt-5.6-sol`, `cost_comparable: true`,
`hidden_ok: true`, `compile_exit: 0` and `smoke_exit: 0`.

`benchmarks/recompute_table.py` rebuilds everything below and exits non-zero
while a figure in the article fails to reproduce.

## What reproduces

| figure | cells |
|---|---|
| baseline 5.11 credits | 5.236, 5.625, 4.480, mean **5.11** |
| ours 11.3 to 15.2 credits | roundtable off mean **11.29**, as shipped mean **15.16** |
| identical hidden-test results in every cell | `hidden_ok` true in all nine, with compile and smoke both zero |
| baseline 91k input tokens | 89,421 mean, inside print rounding |

The credit figures identify the run beyond doubt. They match the reporting
record to the digit.

## What does not

| the article states | the cells give |
|---|---|
| baseline 8.7 calls | **10.7** counting every tool call, **8.0** excluding `file_change`. Neither is 8.7 |
| ours 389k input | **365k** pooled across both configurations, 408k as shipped alone, 323k with roundtable off |
| round trips 3.30× | **1.42× to 2.56×**, depending on the unit |
| per-call weight 1.27× | **1.78× to 3.22×**, depending on the unit |

### The decomposition does not hold under any unit

Ours as shipped against plain Codex, total input 4.56 times:

| unit | round trips | per-call weight |
|---|---:|---:|
| `agent_message` | 1.42× | **3.22×** |
| tool calls | **2.56×** | 1.78× |
| messages plus tool calls | 2.25× | 2.03× |
| **the article** | **3.30×** | **1.27×** |

The article's case is that round trips dominate and per-call weight is the
smaller term. No unit in the committed cells produces that split. Counting tool
calls, the unit most favourable to the argument, trips lead at 2.56 against 1.78,
which is a lead rather than dominance. Counting assistant messages it reverses
outright.

The article's 3.30 against 1.27 is more lopsided than any unit gives, and the
sentence it supports is the one the piece turns on.

### The `ours` row pools two configurations

`11.3 to 15.2` is not the spread of three replicates. It is the distance between
two means: roundtable off at 11.29 and as shipped at 15.16. Presented as one row
called `ours, over MCP`, it reads as replicate variation within one condition.

Those two configurations differ by one tool. Pooling them into a single row and
quoting the gap as a range hides the strongest result in the run, which is that
removing one tool from the surface moved cost by 26% with non-overlapping ranges.

## The credits were measured on a thrashing host

On 2026-08-12 CT403 was found at load 89 with 93 tasks in uninterruptible sleep,
`aimee-server` holding about 20 GB of anonymous memory and the kernel re-reading
executables at roughly 860 MB/s. The reporting record says timings and credits
from that box are suspect, and names this run.

Token and call counts are protocol facts and do not move with page-cache thrash.
Credits and wall time do. The credit column is the one that reproduces exactly
and the one that should not be trusted, which is an awkward pairing and worth
stating plainly.

## Still not cited

| figure | status |
|---|---|
| about 178k of 389k input tokens are conversation re-sends | not derivable from a cell summary, and 389k does not reproduce |
| zero command-line invocations across thirteen cells | `tool_calls` shows `command_execution` counts, 8 to 16 per cell, but not which command ran. Needs the transcripts |
| nineteen tools | not cited |
| four capabilities that exist only as tools | not cited |
| four attempts to move the behaviour by wording | not cited |

The handshake quotation is verbatim from the MCP initialize message and needs no
artifact beyond the server.

## Reporting inventory and disposition

- **The comparison of surfaces:** kept. It is an argument about what the protocol
  can express and it stands on the absence of an `&&`, not on the table.
- **The credit figures and correctness:** kept and reproduce exactly.
- **The call and token figures:** do not reproduce and are not yet safe to print.
- **The decomposition:** not supported by the committed cells under any unit.
- **The roundtable comparison:** currently hidden inside a pooled row, and it is
  the run's strongest measured result.
- **Adjacent interest:** disclosed in the article, next to the claim, and the
  layer that comes off worst is ours.

## What has to happen before this can be published

1. Replace the call and token figures with the committed ones, or say which cells
   the current figures came from.
2. Settle the unit and rewrite the decomposition around it. On the committed
   cells the honest statement is that both terms are large and neither dominates.
3. Split the `ours` row into the two configurations it pools, which also surfaces
   the roundtable result.
4. Decide what to do about credits: they reproduce and the host was thrashing.
5. Cite the re-send figure, the tool count, the tool-only capabilities and the
   wording attempts, or drop them.
6. Establish the zero command-line invocations from the transcripts.
