---
title: "One Call, One Turn"
date: 2026-08-12
author: Rakuen Software
tags: [mcp, agent-tooling, protocols, benchmarks, aimee]
excerpt: "We exposed a code-intelligence layer over MCP and it cost about three times plain Codex for the same patch. Most of the gap was the protocol, not the work. A shell command composes and a tool call does not."
---

*Rakuen builds aimee, the layer measured here and the one that comes off worst.
Figure sources and what has not been reproduced are in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/one-call-one-turn/evidence/figures.md).*

The Model Context Protocol (MCP) is a fine way to describe a capability and a bad
way to spend one. We measured our own agent paying about three times what plain
Codex paid for the same patch, and most of the difference was the protocol, not
the work.

We built a code-intelligence layer and exposed it over MCP, because that is what
you do now. Symbol lookup, blast radius, hybrid search, span reads: nineteen
tools as of 2026-08-12, each described and typed. Then we benchmarked it against
the same agent with no layer at all, same task, same machine, same hour.

Ours cost 2.2 to 3.0 times more and produced a patch that passed the same hidden
tests in every cell. Not dearer because it did more work. Dearer because of how
the work was shaped.

## Nothing we tested ever batched a tool call

Late in a task the agent knows three function names and wants the callers of
each. Here is one intention on two surfaces.

As tool calls, three round trips:

```
find_callers("get_profile")
find_callers("invalidate_profile")
find_callers("cached_profile")
```

As a command, one round trip:

```sh
aimee index callers get_profile && \
aimee index callers invalidate_profile && \
aimee index callers cached_profile
```

Nothing about the second is cleverer. The lookups are identical and the result
payload is identical.

The protocol is not what separates them. A client can emit several tool calls in
one assistant message, and the schema permits it. In our transcripts no model did
it once, for any tool, in any cell. The shell form arrives batched because
writing one command line is how a shell is used, and the tool form arrives one
call per turn because that is what the models produced.

So the gap is real and observed, and its cause is the model rather than the
specification. That distinction matters for what you can do about it, and it is
the correction below.

In a stateless protocol the unit of cost is not the call. It is the turn, and
every turn drags the whole conversation behind it.

## The unit of cost is the turn

One task, three replicates per run, every run on one image inside the same hour on
2026-08-11. Hidden-test results were identical in every cell.

| run | tool and shell calls | input tokens | credits |
|---|---:|---:|---:|
| plain Codex | 8.7 | 91k | 5.11 |
| ours, over MCP | 29.0 | 389k | 11.3 to 15.2 |

The 4.3 times gap in input tokens splits in two. Round trips account for 3.3
times, at 29.0 calls against 8.7. Per-call weight accounts for 1.27 times, at
13.4k tokens against 10.5k, which is nineteen tool schemas riding every request.
About 178k of the 389k input tokens in one cell are the conversation sent again,
a figure derived from the call and token counts and not measured on its own.

That split rests on counting a tool call as a turn. A tool result forces a fresh
model request, so it bills as one, which is why calls are the denominator here.
Count assistant messages instead and the same total splits the other way, which
is what a second campaign on this task does.

The total is not in dispute and the division is. Under the billing unit, round
trips dominate, and every one of ours came from a tool call the model chose to
make alone. Per-call weight is then the smaller term, and it is the one thing
here the protocol does charge for on its own.

The credits column is the soft one. It was measured on a host that we later found
thrashing its page cache, which moves timings and cost and does not move token or
call counts. The token and call figures carry the argument; treat the credits as
indicative.

## We told it to do this

Across thirteen benchmark cells our agent invoked our own command-line tool zero
times. The binary was on `PATH` throughout.

Not defiance. Instruction-following. The MCP initialize handshake, the one
message every client reads before any work, told it:

> find_symbol, preview_blast_radius, search_docs and search_memory are listed:
> use them as your first move on repository questions rather than after a shell
> search.

We wrote that. It is good advice about which capability and poor advice about
which surface, and it arrives with more force than anything else we can say,
because it is guaranteed and it is first.

The surface also argues for itself. A tool schema is structural: it sits in the
request every turn, typed and described and there to be called. A sentence
recommending a shell command is advisory prose competing against it.

We tried four times to move the behaviour with wording. It moved on the fourth,
and only because we stopped asking the model to do the expensive thing.

## MCP describes a capability well

This is not a case against the protocol. Before it, every integration was
bespoke. As a way to describe a capability it works, and the schemas earn their
place with a model that would otherwise guess at the arguments.

It is also the only option for clients with no shell. That is a real
constituency and MCP serves it well.

The mistake is treating a description format as an execution surface for agents
that have something better. Where an agent has a shell and the capability already
has a command form, MCP is a more expensive way to run it, and it stays more
expensive until the protocol can put two calls in one turn.

## Make every capability a command first

**Never count calls when the turn is what bills.** A cheap tool that costs a
round trip is not cheap, because in a stateless protocol it costs the whole
conversation again.

**Never mistake batching for composition.** We added plural arguments for spans,
queries and symbols, and they help for repeats of one operation. Real work mixes
a search, two reads and a `git status`, and in our transcripts only a shell ever
got those into one call.

**Never put guidance anywhere but the handshake.** It is guaranteed and it is
first. We hung ours on an optional tool call instead, the agent never made that
call, and the advice was correct, verified and never delivered.

**Make every capability a command first.** Ours has four that exist only as
tools. Those four are the ones the agent reaches for first in every transcript,
and the ones it never once batched.

Our layer's largest cost was not the intelligence in it. It was the doorway we
put in front of it.

## Correction, 2026-08-12

This piece first said the protocol has no `&&` and that a tool call cannot
compose. That is wrong. A client can emit several tool calls in one assistant
message and the schema permits it, so nothing in MCP forbids batching.

What we observed is that no model we tested ever did, for any tool, in any cell.
The measured cost is unchanged and the recommendation is unchanged. The cause is
not.

It matters because the two readings point somewhere different. A protocol limit
is a thing you route around. A model behaviour is a thing you might prompt for,
and the next useful experiment is to ask directly for parallel tool calls and see
whether the count moves. We have not run it.

The original wording is left above in the headings and the argument so the change
is legible rather than tidied away.
