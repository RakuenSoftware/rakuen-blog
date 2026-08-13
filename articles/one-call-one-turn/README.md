# One Call, One Turn

MCP describes a capability well and spends one badly. Our layer cost about three
times plain Codex for the same patch, and most of the gap was the protocol, not
the work.

## Status

Published 2026-08-12 at https://rakuensoftware.com/blog/one-call-one-turn. The
voice gate passes it and the cells behind its table are committed under
`benchmarks/`.

Two edits landed after it went live. The batching claim was corrected: MCP does
not forbid several tool calls in one message, and what we observed is that no
model we tested emitted them. A same-day correction notice was then removed,
because it was written and applied on the publication date and so announced a
draft edit as a change to something readers had already seen.

## The claim this rests on

A stateless protocol re-sends the whole accumulated conversation on every turn.
Adding tokens to a call you are already making costs those tokens. Adding a turn
costs the entire conversation again. That is arithmetic about how the protocol
bills, not a result that a benchmark has to establish, and it is why an
unchainable surface is expensive independently of how any one run came out.

The measurement illustrates the mechanism. It does not carry it.

## Evidence

`benchmarks/` holds the 2026-08-11 22:00 run, recovered from CT403 on
2026-08-12. Three directories, one per configuration:

| directory | configuration |
|---|---|
| `results-base-now` | plain Codex |
| `results-rt-off` | ours, `roundtable_review` removed from the tool surface |
| `results-rt-on` | ours, as shipped |

Nine cells, all `gpt-5.6-sol`, all `cost_comparable`.
`benchmarks/recompute_table.py` rebuilds the table from them.

The credits reproduce to the digit and identify the run beyond doubt: baseline
5.11, roundtable off 11.29, as shipped 15.16. All nine cells report `hidden_ok`
true with compile and smoke zero, so the identical-correctness claim holds.

The call and token counts recompute differently from the figures in the text, and
`evidence/figures.md` records every difference, the unit dependence of the
decomposition, and the five figures that remain uncited. That file is the
reporting record and it is deliberately harder on the article than the article is
on itself.

## Known limits, stated in the text

The credits were measured on a host later found thrashing its page cache, which
moves cost and timing and leaves token and call counts alone. The article marks
that column indicative and leans on tokens and calls.

## What the voice pass changed

Rewritten against Part I and Part III of the voice guide. The finding is in the
lead, the headings carry the argument on their own, the two surfaces are shown as
code rather than described, and the closing advice became four rules in the
voice's imperative form.

`arm` became `run`, the em dashes went, the `X rather than Y` reformulation went
from four uses to one, and the strong claim about terminals was scoped so one
counterexample would settle it.
