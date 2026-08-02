---
title: "Token compression tools measure the wrong thing"
date: 2026-07-24
author: Rakuen Software
tags: [agents, llm, cost, aimee]
excerpt: "A token counter cannot tell you whether a compression tool lowered your bill. The useful measure is cost per successful task, with cache writes, cache reads, retries and task quality included."
---

Token compression can lower an agent's bill. A counter showing tokens removed
cannot prove that it did. The counter may include text the client would have
truncated while missing retrievals and corrective turns caused by the rewrite.
In the best independent test I found, RTK 0.43.0 made low-effort Claude Code
tasks **7.6% more expensive at the median** and saved nothing at high effort. I
found no equivalent paired GPT-5.6 result for Headroom. The useful number is
cost per successful task.

This is reported analysis. Prices, benchmark results and software behaviour
come from named sources or pinned code. The conclusions are mine.

Disclosure: Rakuen Software builds `aimee`, which competes for some of the same
users by managing agent memory, context and model routing. Our counters are not
evidence either.

*Substantially revised on 2 August 2026. This version restores the original
first-party observations with their limits, adds contrary evidence, and
accounts for native client truncation and extra turns.*

## Cache position decides whether compression saves

Providers price uncached input, cache writes and cache reads differently. For
GPT-5.6, OpenAI's 9 July 2026 launch post says
["cache writes are billed at 1.25x"](https://openai.com/index/gpt-5-6/) the
input rate while cache reads receive a 90% discount. Writing a token therefore
costs 1.25 price units. Reading it costs 0.10.

Suppose a tool changes an already-cached suffix of `x` tokens and removes a
share `r`. Rewriting the replacement costs `1.25(1-r)x`; reading the old
suffix costs `0.10x`. The illustrative break-even point is:

`1.25(1-r)x <= 0.10x`

The tool must remove at least **92% of the invalidated suffix**. Removing 92% of
one block is not enough if the edit also invalidates later material.

Compression can avoid that penalty. OpenAI says cache hits require
["exact prefix matches"](https://openai.com/index/unrolling-the-codex-agent-loop/),
and GPT-5.6 supports explicit breakpoints. A tool can compress new content
before its first write or preserve the stable prefix.

Yan Song measured that distinction in the 17 July 2026 preprint
[*Cache-Aware Prompt Compression*](https://arxiv.org/abs/2607.15516). On the
50-task tau-bench retail test, query-stable compression cost **7.9% less** than
an uncompressed Sonnet 4.6 baseline with the same reward, 36 successful tasks
in each arm. Query-aware compression changed the cached prefix and cost **40.1%
more**. Those are one paper's results on one model and cache policy. They do not
validate RTK, Headroom or GPT-5.6. They establish the stronger point:
compression can work when it respects the cache.

## The original tests produced a hypothesis, not a number

The original article began with two days spent reconciling an Anthropic
reseller bill against its rate card, followed by checks of the same cache
mechanism on GPT-5.6 and the OpenAI API. In every case I measured, the extra
cost associated with lost cached input exceeded the saving attributed to
removed text.

The invoices, request traces and case table were not archived when the article
moved into this repository. I cannot reproduce an effect size or generalise the
result across resellers. The observation produced the hypothesis. Published
prices and paired completed-task tests must carry the claim.

## RTK's counter did not predict its bill

RTK rewrites supported shell-command output before the agent reads it. That can
make a conversation smaller. Its development README at
[commit `e0ffd40`, dated 1 August 2026](https://github.com/rtk-ai/rtk/blob/e0ffd40ef7c450489aca4a50c0ab1358e4375691/README.md#how-savings-work)
now says its reduction in Bash output "is not the same as cutting your bill by
90%." Its absolute token estimate is `bytes / 4`.

The counter cannot see the full provider request, native client truncation or
the number of turns the task would have taken without RTK. JetBrains showed the
gap in a 20 July 2026 replay. Claude Code's built-in `Read` and `Grep` paths
bypassed RTK, while its native limit would have truncated a 1.2 MB `cat`
result to a few thousand tokens. RTK counted that command against the full raw
file. Across the run,
[`rtk gain` reported 96.2 million tokens saved](https://blog.jetbrains.com/ai/2026/07/rtk-claude-code-token-savings/)
while the measured bill increased.

The effect depends on the client, version, command and tool path. A built-in
read, Bash `cat`, compound command and supported direct command can pass
through different transformations. RTK may compete with controls the client
already applied.

The same release produced a local correctness failure. My pytest configuration
already supplied `-q`; RTK added another `-q`; effective `-qq` removed the
summary its filter expected. The
[pinned 0.43.0 source](https://github.com/rtk-ai/rtk/blob/5a7880d404db8364d602f2ecdc41dd790f64013f/src/cmds/python/pytest_cmd.rs#L28-L43)
supports the mechanism: it checks command-line arguments but cannot see
`addopts` in pytest configuration. I did not archive the terminal output and
fixture, so this is a disclosed local reproduction, not a frequency estimate.
The failure was RTK, not Headroom.

My RTK installation also reported about **6.1 million estimated tokens saved**
on work whose actual input, as the original article recorded it, was a fraction
of that. I did not preserve the matching RTK and provider exports, so the figure
describes the counter I saw, not a bill saving.

Denis Shiryaev supplied the paired result. His JetBrains benchmark used RTK
0.43.0, Claude Code 2.1.201, Claude Sonnet 5 and SkillsBench. Across **80 clean
low-effort pairs**, RTK raised median cost per task by **7.6%** (`p=0.004`),
turns by **13.8%** and cache reads by **14.3%**. At high effort, cost changed by
**+0.1%** (`p=0.99`). Task quality was statistically tied in both arms.

RTK's filters worked and quality did not fall. The test covered Claude Code,
not GPT-5.6, and found a low-effort penalty plus a high-effort tie. Install RTK
if compact Bash output is the result you want. Its counter does not establish a
cost saving.

## Extra turns can erase a local saving

A fixed block of `c` tokens kept for `n` calls adds `nc` input traffic,
which is linear. A growing conversation is different. With a base prompt of
`b` tokens and `d` new live tokens per turn, cumulative input is:

`T(n) = nb + d n(n+1)/2`

The second term grows with the square of turn count. The next turn replays the
live prefix, adds output and can enlarge every later request. Cache discounts,
compaction and truncation change the realised bill, so this is a workload
model, not a universal pricing law.

One user's traces show the shape, not the bill. On 24 July 2026, Reddit user
[`ikhDark`](https://www.reddit.com/r/codex/comments/1v4vawj/important_findings_on_cache_and_baked_in_codex/)
reported 2,007 calls across ten GPT-5.6 Codex rollouts. The average call carried
125,394 input tokens and produced 290 output tokens. I did not receive the raw
traces, and subscription metering was not shown. The figures are
single-sourced. They still illustrate why another turn can cost more than
leaving one block in context.

## Headroom reaches the right layer but inherits the turn problem

Headroom has the stronger architecture. Its proxy sees the assembled model
request, can compress new output before its first cache write, stores the
original for retrieval and
[replays frozen prefixes byte-for-byte](https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/cache/prefix_tracker.py#L267-L368).
I audited version 0.33.0 at commit `6d5516d`. This was a static source review,
not a live request.

Headroom's README at that commit leads with
["15-20% fewer tokens (for coding agents)"](https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/README.md#proof).
Those vendor tests are not paired GPT-5.6 costs per completed task. Two
accounting fallbacks also did not match GPT-5.6 pricing on 1 August: the
[Responses handler](https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/proxy/handlers/openai.py#L1246-L1257)
said OpenAI had no cache-write premium, while a
[manual fallback](https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/providers/openai.py#L530-L587)
priced cache reads at 50% of input instead of 10%. Other paths may use exact
provider usage or LiteLLM pricing. The audit does not prove every dashboard
number wrong.

Recovery has a cost. When the model calls `headroom_retrieve`, the pinned
[CCR handler retrieves the full original, appends it as a tool result and
makes another API call](https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/ccr/response_handler.py#L420-L529).
The default permits three retrieval rounds. Reversibility prevents permanent
loss; it does not make recovery free.

Compression can also change the output shape and detail the agent expected.
The model may retrieve, re-read, change its reasoning path or miss detail. I
found no paired GPT-5.6 coding benchmark that reports those behavioural turns,
so this is a mechanism to test, not a measured failure rate. Headroom could
save money. Its local token reduction cannot establish that it did.

## Compression needs an adaptive control, not a global switch

The decision depends on what the client already removed, where material sits
relative to the cached prefix, how the provider prices and reports caching,
what the model can recover and what the task needs. A policy tuned for one
combination can fail after any part changes.

An add-on therefore needs bounded feedback. "Self-learning" here means recording
completed-task cost and quality, keeping occasional uncompressed controls,
segmenting results by client, provider, model and task, and backing off when
the result deteriorates. Learning from a tokens-removed counter is learning the
wrong target.

A viable implementation should:

- compare paired successful tasks, including cache writes, reads, retrievals
  and corrective turns;
- measure after native client handling and give one layer ownership of output
  shape;
- preserve stable prefixes and compress new material before its first write;
- keep raw logs on disk, then leave only a result and retrieval receipt in live
  context;
- detect client, provider and model drift, then re-test or stop rewriting; and
- expose cumulative input, cache activity and model calls to the user.

[The working `aimee` source is public](https://github.com/RakuenSoftware/aimee).
We use this design brief for our own product. That is not evidence that it
works.

Keep a compression tool only when paired runs show a lower cost per successful
task at equal quality. If it cannot observe the client pipeline, provider
economics and later turns, it cannot know that it saved money.

*Right of reply: Rakuen Software has contacted the RTK and Headroom projects
about the findings in this article. If either responds, we will update the
article with the response where it bears on those findings.*
