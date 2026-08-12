# One Call, One Turn

MCP describes a capability well and spends one badly. Our layer cost about three
times plain Codex for the same patch, and most of the gap was the protocol rather
than the work.

## Status

Draft. Not publication-ready, and deliberately not marked as such, so the voice
gate does not treat it as a candidate. It passes that gate today; the evidence is
what holds it.

## What the voice pass changed

Rewritten against Part I and Part III of the voice guide. The finding is in the
lead, the headings carry the argument on their own, the two surfaces are shown as
code rather than described, and the closing advice became four rules in the
voice's imperative form.

Two things were added rather than cut. The credits column is now marked
indicative in the text, because it was measured on a host later found thrashing
its page cache, and that moves cost and timing while leaving token and call
counts alone. And the decomposition is attributed to a unit, since which term
dominates depends on what counts as a turn.

## The cells are committed, and they contradict the table

Recovered from CT403 on 2026-08-12 and committed under `benchmarks/`, in three
directories because the run is three configurations rather than one campaign.
`benchmarks/recompute_table.py` rebuilds the table and exits non-zero while a
figure fails.

The credits reproduce to the digit and identify the run beyond doubt: baseline
mean 5.11, roundtable off 11.29, as shipped 15.16. All nine cells report
`hidden_ok` true with compile and smoke zero, so the identical-correctness claim
holds.

The call and token figures do not reproduce, and the decomposition does not hold
under any unit:

| unit | round trips | per-call weight |
|---|---:|---:|
| `agent_message` | 1.42× | **3.22×** |
| tool calls | **2.56×** | 1.78× |
| messages plus tool calls | 2.25× | 2.03× |
| **the article** | **3.30×** | **1.27×** |

The article says round trips dominate and weight is the smaller term. On the
committed cells the honest statement is that both terms are large and neither
dominates. That is the sentence the piece turns on, so it cannot be printed as it
stands.

One more thing the cells show: `11.3 to 15.2` is not replicate spread. It is the
distance between two configurations that differ by one tool, pooled into a row
called `ours, over MCP`. Splitting them surfaces the run's strongest result,
which is that removing `roundtable_review` moved cost by 26%.

## The one thing standing in the way

**The cost table does not reproduce against the committed measurement of the same
task**, and the disagreement is about the thesis rather than the arithmetic.

The article's numbers come from the 2026-08-11 22:00 run, whose cells are not on
this machine. The committed `ct403-results` campaign covers the same task with
three replicates and splits the same total gap the other way:

| basis | round trips | per-call weight |
|---|---:|---:|
| the article, calls | **3.3×** | 1.27× |
| committed cells, messages plus tool calls | 1.98× | **2.94×** |

The article argues that round trips dominate. On the committed cells that
reverses under every unit tested. Both runs agree the total gap is 4× to 6×, so
this is not a measurement dispute; it is a question of what a turn is, and the
answer decides the article's conclusion.

A tool result forces a fresh model request, which argues for the article's unit.
That case is currently assumed rather than made, and it needs making in the text.

`evidence/figures.md` records this, the thrashing caveat, the seven uncited
figures, and five steps to close the gap.

## Note on the third number

`articles/three-zeros-and-a-wrong-answer` records a third decomposition of the
same quantity, 1.42× against 2.93×, on the `agent_message` basis across all
tasks. Three numbers for one quantity means the quantity is not yet defined, and
settling it fixes both articles at once.
