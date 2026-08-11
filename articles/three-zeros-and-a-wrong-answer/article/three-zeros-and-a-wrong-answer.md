---
title: "Three Zeros and a Wrong Answer"
date: 2026-08-11
author: Rakuen Software
tags: [agent-tooling, benchmarks, instrumentation, post-mortem, aimee]
excerpt: "We built a layer on top of Codex to make it cheaper and smarter. It made the same task cost three to four times more. Finding out why meant retracting my own conclusions three times, each one built on a number that was never a measurement."
---

*Rakuen builds aimee, the system measured here. Cell-level artifacts and the
disposition of every figure are listed in the [figure provenance map](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/three-zeros-and-a-wrong-answer/evidence/figures.md).*

We built a layer on top of Codex to make it cheaper and smarter. It made the same
task cost three to four times more. Finding out why meant retracting my own
conclusions three times — each one built on a number that was never a
measurement.

The question was simple and had been nagging for weeks: why does aimee cost so
much more than plain Codex? Same benchmark task, same model, same box. Baseline
finished for about five credits. Ours spent fifteen to twenty.

The answer turned out to have nothing to do with what I spent most of the day
investigating. It's worth writing down the wrong turns, because all three shared
one root cause, and it's a mistake that is very easy to make when you instrument
your own system.

## A zero is not a measurement

A number that reads 0 can mean two completely different things. It can mean *this
thing was measured, and the value was zero*. Or it can mean *nobody wrote this
number down*. They look identical in a database. Three times in one day I read
the second as the first, and each time it produced a confident, specific, wrong
conclusion.

**Reading 01 — the empty index**

Benchmark cells reported `files_indexed: 0`.

*I concluded:* the project was never indexed, so every aimee result in the corpus
is invalid.

*Actually:* the harness always returns zero there — a comment three lines above
the value said so. The real readiness gate was a semantic round-trip, and it had
passed in all 27 cells.

**Reading 02 — the uncached gateway**

Codex recorded `cached_input_tokens: 0` in 8 of 8 cells.

*I concluded:* the gateway defeats prompt caching entirely, so every token bills
at the uncached rate — roughly a 6× input-cost penalty.

*Actually:* a real bug, wrong magnitude. Caching worked fine; we simply never
told the client about it. Correcting the accounting recovered about 13%, not 6×.

**Reading 03 — the cache regression**

Our own ledger showed a 14.9% cache hit rate.

*I concluded:* a regression has pushed us below baseline. The recent economizer
work is the likely culprit.

*Actually:* the average straddled a deploy. Before the recording path shipped:
0.0% across 1.5M tokens. After: 80–96% on warm turns, in line with production and
with our own historical figures. There was no regression, and the economizer was
never involved.

The tell was there in the second case and I walked past it. The rate wasn't low,
or noisy, or variable. It was exactly zero, in every cell, across three separate
result sets. A cache that genuinely fails still hits sometimes. A field that is
never serialised is always precisely nothing.

## The bug that was real

Underneath reading 02 there was a genuine defect, and it's a tidy illustration of
where this class of bug lives.

Our gateway speaks OpenAI's shape to the client and OpenAI's shape upstream.
Because both sides match, nobody experienced that boundary as a translation — it
feels like passthrough. But it wasn't passthrough; it was a rebuild, assembling
the usage block field by field from five scalars. Cached tokens don't live in
those five. They sit one level down, in a sibling object that arrived with the
feature years later. The rebuild dropped it silently: no error, no failing test,
because tests assert what is present and nothing asserts what was never
mentioned.

Meanwhile the Anthropic-facing path — where the two shapes genuinely differ —
carried the field across perfectly. Someone had to sit and map those fields by
hand, and while doing it they saw the cached count and handled it.

The boundary that announces itself gets handled. The boundary that looks like a
no-op is where things quietly fall on the floor.

The effect on us was specific: the benchmark computes cost from client-reported
usage, and the gateway is the only arm where our code sits in the reporting path.
So it was the only arm whose numbers could be wrong, it was the arm under
evaluation, and the error biased toward expensive — confirming precisely the
hypothesis the benchmark existed to test.

## So where did the money actually go?

With the accounting fixed, the picture is unambiguous, and it isn't caching. Our
cache performance is better than baseline's.

One task (`t01_cache`), three replicates per arm, same model and host:

| arm | input tokens | cache hit | round trips | credits |
|---|---:|---:|---:|---:|
| baseline (plain Codex) | 84–98k | 66–88% | 4–5 | 4.3–6.6 |
| ponytail add-on | 107–143k | 63–85% | 4–5 | 5.3–7.4 |
| aimee (plugin) | 464–648k | 89–91% | 13–22 | 13.8–19.2 |
| aimee (gateway, no plugin) | 136–231k | 25–70% | 5–11 | 7.9–21.5 |

Five to seven times the input tokens, at a better hit rate. The arithmetic is
unforgiving: on one cell, our cached tokens alone cost more than baseline's
entire run. Even free caching could not have closed the gap. It was never a cache
problem. It was volume, and volume decomposes into two multipliers that compound:

- **~2.3× heavier per call.** Nineteen tool schemas plus an injected context
  envelope ride along on every round trip. In a stateless protocol you pay that
  on all of them.
- **~2.5× more round trips.** And because each trip re-sends the whole
  accumulated conversation, doubling trips more than doubles total tokens.

## The natural experiment

The last row of that table is the one that gave it away. Our gateway arm exposes
the same tools as the plugin arm. What it doesn't install is the plugin's
persona. It sits at 5–11 round trips. The plugin arm sits at 13–22.

So it was never the tools. It was the process we wrote around them: act as a
manager rather than do the work, delegate multi-file changes, review the returned
diff, run a roundtable review before declaring done, then re-validate. Every one
of those is a round trip. On a single-file cache change, it is almost entirely
overhead — a process designed for work an order of magnitude larger than the task
in front of it.

Two details make the point sharper than any measurement. Across the whole corpus,
`roundtable_review` was called 52 times. And `delegate` — which our persona
instructs the agent to always use for multi-file changes — was called zero times,
because in that mode it can't be. We were paying, on every single call, to ship
an instruction that could never be followed.

We spent the day proving that the elaborate thing we bolted on was three to four
times more expensive than the default we bolted it onto, and that the tools, the
part we were most proud of, were never the problem.

## The lesson we didn't want

Here is the part worth generalising, and it stings.

It is extraordinarily hard to engineer something better than the specialised
teams building these agent harnesses. That is what we tried to do. Codex's loop
is not naive; it is tuned by people who look at nothing else, against far more
usage than we will ever see. Its default behaviour — batch aggressively, keep the
prefix stable, take as few turns as the task allows — is not laziness. It is the
optimisation.

Every layer we added was individually defensible. A manager persona to keep work
structured. A roundtable review so nothing ships unreviewed. Delegation for
parallelism. Memory injection for context. Each one reasonable; each one bought
with round trips, and round trips are the one currency that compounds against you
in a stateless protocol.

There's a related finding that says the same thing from the other direction. Our
agent mostly declines to use our own code-navigation tools, and we spent three
rounds rewriting the prompt to persuade it. It turns out it was right to decline.
A single shell command can read four files, grep a pattern, and check git status
in one trip. Our tools batch within a capability but not across them, so
following our own guidance would have tripled the number of trips. The model was
doing the correct arithmetic. Wording was never going to beat it.

When the agent ignores your tool, check the exchange rate before you rewrite the
prompt. It may simply be better at economics than your instructions are.

## What we're keeping

Not everything here is a retraction. The serialisation bug was real and is fixed.
The tools that do get used are the ones nothing else can provide — semantic
search, blast radius, memory — which is a rational division of labour, not a
failure. And the instrumentation is now honest enough to have told us we were
wrong three times in a day, which is the whole point of building it.

The changes that follow from this are unglamorous: make the process scale with
the size of the task, stop shipping instructions the surface can't honour, and
stop paying for a manager on a one-file change. None of that is a better agent
than Codex. It's getting out of its way.
