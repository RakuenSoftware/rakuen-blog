---
title: "Three Zeros and a Wrong Answer"
date: 2026-08-11
author: Rakuen Software
tags: [agent-tooling, benchmarks, instrumentation, post-mortem, aimee]
excerpt: "We built a layer on Codex to make it cheaper. It cost three to four times more, and the reason was round trips, not the cache I spent the day investigating. Three wrong answers came first, each built on a zero nobody had measured."
---

*Rakuen builds aimee, the system measured here and the one that comes off worst.
Every figure below traces through the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/three-zeros-and-a-wrong-answer/evidence/figures.md).*

We built a layer on top of Codex to make it cheaper and smarter. On the same
task, same model and same box, it cost three to four times more. Baseline
finished for about five credits. Ours spent fifteen to twenty.

The cause was not the cache, which is where I spent the day. I was wrong about it
three times first, each time confidently, and each time on a zero nobody had
measured.

## A measured zero and an unwritten field look identical

A number that reads 0 means one of two things. The value was measured and it was
zero, or nobody wrote it down. A database stores both the same way.

| what I read | what I concluded | what was true |
|---|---|---|
| `files_indexed: 0` in benchmark cells | the project was never indexed, so every aimee result is invalid | the harness always returns zero there. A comment three lines above the value says so. The real readiness gate is a semantic round-trip, and it passed in 27 of 27 cells |
| `cached_input_tokens: 0` in 8 of 8 cells | the gateway defeats prompt caching, so every token bills uncached, near a 6× input-cost penalty | a real defect, wrong by an order of magnitude. Caching worked. We never told the client about it. Correcting the accounting moved the cost about 13% |
| a 14.9% cache hit rate in our own ledger | a regression below baseline, and the recent economizer work is the likely cause | the window straddled a deploy. Before the recording path shipped, 0.0% across 1,545,665 prompt tokens. After it, 46.6% overall and 80% to 96% on warm turns, against 80.5% in production |

The corrected figure carries its own caveat. Most remaining misses after the
deploy are session-opening calls, which cannot hit a cache by construction. There
was no regression, and the economizer was never involved.

The tell was in the second row and I walked past it. The rate was not low, or
noisy, or variable. It was exactly zero, in every cell, across three result sets.

A cache that genuinely fails still hits sometimes. A field that is never
serialised is always precisely nothing.

## The boundary that looks like passthrough is where the field fell out

Under the second reading sat a real defect. Our gateway speaks OpenAI's shape to
the client and upstream, so nobody experienced that boundary as a translation.

It was not passthrough. It was a rebuild, assembling the usage block field by
field from five scalars. Cached tokens are not among them. They sit one level
down, in a sibling object that arrived with the feature years later.

The rebuild dropped it in silence. No error, no failing test, because a test
asserts what is present and nothing asserts what was never mentioned. The
Anthropic-facing path, where the shapes genuinely differ, carried it across.
Someone mapped those fields by hand, saw the cached count, and handled it.

The boundary that announces itself gets handled. The boundary that looks like a
no-op is where things fall on the floor.

That defect landed where it did the most damage. The benchmark computes cost from
client-reported usage, and the gateway is the only run where our code sits in
that path.

So it was the only run whose numbers could be wrong, the run under evaluation,
and the error biased toward expensive. It confirmed the hypothesis the benchmark
existed to test. Fixed in aimee PR 2569, merged 2026-08-11.

## It was never the cache. It was volume.

With the accounting corrected, our cache performance beats baseline's. One task,
`t01_cache`, three replicates per run, same model and host.

| run | input tokens | cache hit | round trips | credits |
|---|---:|---:|---:|---:|
| baseline, plain Codex | 84k to 98k | 66% to 88% | 4 to 5 | 4.3 to 6.6 |
| ponytail add-on | 107k to 143k | 63% to 85% | 4 to 5 | 5.3 to 7.4 |
| aimee plugin | 464k to 648k | 89% to 91% | 13 to 22 | 13.8 to 19.2 |
| aimee gateway, no plugin | 136k to 231k | 25% to 70% | 5 to 11 | 7.9 to 21.5 |

Five to seven times the input tokens at a better hit rate. On one cell our cached
tokens alone cost more than baseline's entire run, so free caching could not have
closed the gap.

**About 2.3× heavier per call.** Nineteen tool schemas and an injected context
envelope ride on every round trip. A stateless protocol charges for them on all
of them.

**About 2.5× more round trips.** Each trip re-sends the accumulated
conversation, so doubling trips more than doubles tokens.

## The persona bought the round trips, not the tools

The last row gave it away. The gateway run exposes the same tools as the plugin
run, without the plugin's persona. It sits at 5 to 11 round trips against the
plugin's 13 to 22.

So it was not the tools. It was the process we wrote around them. Act as a
manager rather than do the work, delegate multi-file changes, review the returned
diff, run a roundtable review before declaring done, then re-validate.

Every one of those is a round trip. On a single-file cache change it is overhead,
a process sized for work an order of magnitude larger than the task in front of
it.

Two counts sharpen it. Across the corpus `roundtable_review` was called 52 times.
`delegate`, which our persona instructs the agent to always use for multi-file
changes, was called zero times, because in that mode it cannot be.

We paid on every call to ship an instruction that could never be followed. That
last zero is a measured one. I checked, because this piece is about the other
kind.

## Codex's loop is the optimisation, not the laziness

It is hard to beat the specialised teams building these harnesses, and that is
what we tried to do. Codex's loop is tuned by people who look at nothing else,
against far more usage than we will see. Batch aggressively, keep the prefix
stable, take as few turns as the task allows.

Every layer was individually defensible. A manager persona for structure, a
roundtable review so nothing ships unreviewed, delegation for parallelism, memory
injection for context. Each was bought with round trips, the currency that
compounds against you.

A second finding says the same from the other side. Our agent mostly declines to
use our own code-navigation tools, and we spent three rounds rewriting the prompt
to persuade it. It was right to decline.

One shell command reads four files, greps a pattern and checks git status in a
single trip. Our tools batch within a capability but not across them, so
following our own guidance would have tripled the trips. Wording was never going
to beat that arithmetic.

When an agent ignores your tool, check the exchange rate before you rewrite the
prompt.

## What we are keeping, and what changes

The serialisation defect was real and is fixed. The tools that do get used are
the ones nothing else provides, a division of labour rather than a failure. The
instrumentation is now honest enough to have caught us out three times in a day,
which is what it is for.

Three changes follow, and none is a better agent than Codex. Scale the process to
the size of the task. Stop shipping instructions the surface cannot honour. Stop
paying for a manager on a one-file change.

Before treating any zero as a finding, check when the recording path for that
metric last shipped, and split the window at that boundary.
