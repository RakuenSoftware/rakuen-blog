---
title: "Token compression tools measure the wrong thing"
date: 2026-07-24
author: Rakuen Software
tags: [agents, llm, cost, aimee]
excerpt: "A token counter cannot tell you whether a compression tool lowered your bill. The useful measure is cost per successful task, with cache writes, cache reads, retries and task quality included."
---

Token compression can lower an agent's bill. A counter showing tokens removed
cannot prove that it did. In the best independent test I found, `RTK` 0.43.0
made low-effort Claude Code tasks **7.6% more expensive at the median** and
saved nothing at high effort. I found no equivalent paired, independent result
for `Headroom` on GPT-5.6. The useful number is cost per successful task, not
the size of a tool's output.

This is reported analysis. The prices, benchmark results and software behaviour
below come from named sources or pinned code. The conclusions are mine.

Disclosure: Rakuen Software builds `aimee`, which competes for some of the same
users by managing agent memory, context and model routing. We benefit if you
accept the architectural alternative argued here. That interest does not turn
our own counters into evidence, so `aimee` gets the same measurement rule at
the end.

*Substantially revised on 2 August 2026. The revision adds the strongest result
I found in favour of cache-aware compression, separates RTK's low- and
high-effort results, and pins fast-moving software claims to commits.*

## A removed token can cost 12.5 times more

Providers do not bill one undifferentiated token count. They price uncached
input, cache writes, cache reads and output differently.

For GPT-5.6, OpenAI's 9 July 2026 launch post says, "[cache writes are billed at
1.25x](https://openai.com/index/gpt-5-6/)" the ordinary input rate, while a
cache read receives a 90% discount. In API-price units, writing one token costs
1.25. Reading the same token from cache costs 0.10.

That creates a narrow but important break-even rule. Let an already-cached
suffix contain `x` tokens. Reading it again costs `0.10x`. If a tool changes the
prefix before that suffix and forces the compressed replacement to be written,
the next request costs `1.25(1-r)x`, where `r` is the share removed. The edit
breaks even when:

`1.25(1-r)x <= 0.10x`

So `r` must be at least **92% of the invalidated suffix**. Removing 92% of one
tool block is not enough when the edit also invalidates material after it.

This does not mean every compression pass destroys the whole cache. OpenAI says
"[cache hits are only possible for exact prefix
matches](https://openai.com/index/unrolling-the-codex-agent-loop/)," and
GPT-5.6 now supports explicit breakpoints. A tool can compress new content
before its first write, or change only material after a known breakpoint. Both
can save money. The expensive case is mutating a prefix that was already cheap
to read.

## Compression works when it respects the cache

The strongest case against a blanket rejection of compression arrived before
the original version of this article and should have been in it.

Yan Song's 17 July 2026 preprint, [*Cache-Aware Prompt
Compression*](https://arxiv.org/abs/2607.15516), tested a query-stable
compressor with explicit cache control on Anthropic's Sonnet 4.6. On the public
50-task tau-bench retail test, the method cost **7.9% less than an uncompressed
baseline** with the same task reward, **36 successful tasks out of 50** in both
arms. Query-aware compression, which changed the cached prefix for each query,
cost **40.1% more** than the baseline.

Those are the author's results from one preprint, one model family and one
five-minute cache policy. The paper says its provider-specific numbers "[will
need re-measurement](https://arxiv.org/html/2607.15516v1)" elsewhere. It does
not validate RTK, Headroom or GPT-5.6.

It does settle the mechanism. Compression is not the problem. Changing the
wrong part of the prompt is.

## RTK now says its counter is not your bill

RTK's case is straightforward. It rewrites supported shell-command output
before the agent reads it. A long `git status` becomes a compact status. Passing
tests collapse to a count while failures keep their useful lines. Less text
enters the conversation.

The project has also narrowed its public claim. In its development README at
[commit `e0ffd40`, dated 1 August
2026](https://github.com/rtk-ai/rtk/blob/e0ffd40ef7c450489aca4a50c0ab1358e4375691/README.md#how-savings-work),
RTK says it cuts up to 90% of Bash output and adds: "That is what RTK measures,
and it is not the same as cutting your bill by 90%." Its absolute counts use a
`bytes / 4` estimate rather than a model tokenizer.

That is an accurate description of the counter. RTK can see the command output
before and after its filter. It cannot see the full provider request or know
the counterfactual number of agent turns. A smaller result may prevent later
replay. It may also omit something the agent then retrieves in another turn.
The counter records the first effect and cannot price the second.

Denis Shiryaev tested that counterfactual for JetBrains on 20 July 2026. The
[paired benchmark](https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/)
used RTK 0.43.0, Claude Code 2.1.201, Claude Sonnet 5 and SkillsBench. Across
**80 clean low-effort pairs**, RTK increased median cost per task by **7.6%**
(`p=0.004`), turns by **13.8%** (`p=0.03`) and cache reads by **14.3%**
(`p=0.008`). At high effort the cost difference was **+0.1%** (`p=0.99`). Task
quality was statistically tied in both arms.

The strong case for RTK survives that result. Its filters worked, the
compression was real, and quality did not fall. The test was on Claude Code,
not GPT-5.6. It found a low-effort cost penalty and a high-effort tie, not a
universal law that RTK always costs more.

It found no saving either. Shiryaev's useful line is that a tool's
self-reported saving is "[a claim about its counterfactual, not about your
bill](https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/)."

Install RTK if compact Bash output is the outcome you want. Do not install it
because `rtk gain` says it cut your bill. On the only substantial independent
paired test I found, it did not.

## Headroom reaches the right layer but still needs the right test

Headroom has the stronger architecture. It proxies the model request, so it can
compress large, new tool output before that output enters the provider cache.
It stores the original for retrieval and freezes previously forwarded prefixes.
The current code can [replay a compressed prefix
byte-for-byte](https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/cache/prefix_tracker.py#L267-L368).
I will not claim that Headroom simply destroys the cache. Its code is trying to
prevent exactly that.

The project's [README at commit `6d5516d`, dated 1 August
2026](https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/README.md#proof),
leads with "15-20% fewer tokens (for coding agents)" and reports larger
reductions on selected tool workloads. It also publishes small accuracy checks.
Those are vendor-run before-and-after token measurements, not paired GPT-5.6
costs per completed coding task.

The GPT-5.6 accounting paths are not settled either. At that same commit,
Headroom's OpenAI Responses handler [infers cache writes from uncached
input](https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/proxy/handlers/openai.py#L1246-L1257)
because it says OpenAI exposes no separate write counter, then says OpenAI has
no write premium. GPT-5.6 exposes `cache_write_tokens` and charges the 1.25x
premium. A separate [manual cost
fallback](https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/providers/openai.py#L530-L587)
prices cached reads at 50% of input rather than 10%.

Those paths do not prove every Headroom dashboard number is wrong. Headroom
uses LiteLLM pricing when it can, and other response paths may supply exact
provider usage. They do show that its source contains fallbacks that cannot
price GPT-5.6 correctly as of 1 August.

Retrieval belongs in the same test. If the model asks Headroom for the full
original, the task adds a tool call, another model turn and the retrieved text.
That may still be cheaper after enough reuse. A token-reduction counter cannot
tell you whether it was.

Headroom could save money on GPT-5.6. I have not found the paired task result
that establishes it.

## One user's Codex traces put the larger cost in replay

Tool output is only the material added on one turn. An agent sends its live
history again on the next turn, then again on the one after that. This is where
a small local saving can disappear inside a large bill.

The most concrete trace I found is single-sourced. On 24 July 2026, Reddit user
`ikhDark` published [an analysis of ten `gpt-5.6-sol` Codex
rollouts](https://www.reddit.com/r/codex/comments/1v4vawj/important_findings_on_cache_and_baked_in_codex/).
The author reported **252.2 million total tokens**, of which **251.7 million
were input**, across **2,007 model calls**. The average call received **125,394
input tokens** and produced **290 output tokens**. The weighted cache rate was
**97.8%**. The source's conclusion was that Codex was "not primarily consuming
usage by producing answers or performing deep reasoning."

I did not receive the raw traces and did not reproduce that analysis. These are
one user's figures, not an independent measurement. The traces also do not show
how a Codex subscription meters cached input, so they do not establish a
billing or quota bug.

They do show the workload shape reported by the source. In those ten sessions,
the dominant traffic was accumulated context sent through the model call by
call, even with a high cache rate. A cached API token costs less. It does not
cost zero.

OpenAI's own 2026 guidance points at the same architectural levers. Its
GPT-5.6 guide tells API developers to expose only relevant tools, keep prompts
lean and [track both cached and cache-write
tokens](https://developers.openai.com/api/docs/guides/latest-model). Its 9 July
launch post says Programmatic Tool Calling can filter intermediate data and
reduce model round trips. That does not verify the Reddit figures. It does make
context lifecycle a provider-recognised engineering problem, not a theory that
depends on one trace.

## The replacement is context lifecycle, not a better counter

The useful controls sit where the runtime can see the whole request and the
task outcome:

- **Measure completed work.** Run the same task with and without the change,
  reset the repository, keep the model and effort fixed, and score success
  before comparing the full bill.
- **Preserve the cheap prefix.** Put stable instructions and schemas first. Put
  changing material after an explicit breakpoint, then record writes and reads
  separately.
- **Retire used output.** Keep raw files and logs on disk. Once they have served
  their purpose, leave a receipt in context with the result and the locations
  that still matter.
- **Defer unused tools.** A task should not pay to carry schemas it will not
  call.
- **Route bounded work down.** A lookup or scoped edit should use the cheapest
  model that clears its quality test, without hauling the parent task's whole
  working set behind it.
- **Expose a budget.** Show cumulative input, cache writes, cache reads, model
  calls and child-agent use, then let the user cap them.

[The working `aimee` source is
public](https://github.com/RakuenSoftware/aimee). We build it to retain facts
outside the live prompt, navigate code by structure, route bounded work to
cheaper models, and account for the whole run. Those features are a design
response to the mechanism above. They are not evidence that the response works.

I will not give you an `aimee` savings percentage without paired runs. That
would be the same counterfactual mistake.

## The number to demand is cost per successful task

RTK 0.43.0 did not save money in the JetBrains benchmark. Headroom operates at
a layer where it could, but its public token reductions and current GPT-5.6
accounting do not establish that result. Cache-aware compression itself has a
promising measured case on Sonnet 4.6, with limits the author states.

Disable any compression tool you cannot test against the full task. Keep one
only when paired runs show a lower cost per successful task, including cache
writes, cache reads, retries, retrievals and quality.
