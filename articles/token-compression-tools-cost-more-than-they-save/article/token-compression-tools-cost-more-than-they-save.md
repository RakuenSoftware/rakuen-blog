---
title: "Token compression tools measure the wrong thing"
date: 2026-07-24
author: Rakuen Software
tags: [agents, llm, cost, aimee]
excerpt: "RTK and Headroom count tokens removed. Your provider bills cache writes, cache reads and replayed context. The real drain isn't the tool output. It's resending it four hundred times, and the fix is architectural, not a plugin."
---

I spent two days working out why an Anthropic reseller was billing me more than its own rate card said it should. The answer became a rule I now run every "compress your context" tool against: **tokens removed and money saved are different numbers. A tool that only measures the first isn't measuring your bill.**

I ran the same dig against GPT-5.6 and the OpenAI API, on two tools that work opposite ends: `RTK` rewrites command output, `Headroom` proxies the model request. Then I read someone else's trace of where a real coding session's tokens actually go, and it moved the problem to a different layer than I expected. Fair warning: this is a wall of text, and it gets geeky.

## The number that actually gets billed

Providers don't charge for tokens in the abstract. They charge for cache writes, cache reads, uncached input, output, and reasoning. Each one is a different price.

On GPT-5.6 the spread is wide. A cache read costs 10% of ordinary input. A cache write costs 125% of it. So a token that moves from "cached read" to "cache write" costs **12.5 times more**, not less.

That changes the maths on any tool that edits your prompt. Caching keys on an exact prefix match: same tokens, same order, byte for byte. Change one token in a cached prefix and everything after it stops matching. The whole suffix gets written again at 125%.

Work the break-even and it's brutal. For an edit to an already-cached prefix to pay for itself on the *next* request, it has to strip more than **92% of the entire invalidated suffix**. Not 92% of the block it touched. 92% of everything downstream of the first changed token. Almost no real edit clears that bar.

I hit Anthropic first, and that's where the rule came from. Anthropic runs its own cache, and it's widely misunderstood. It's unforgiving in one specific way: if a message isn't byte-identical to what was there last request, it isn't a cache hit. You pay full, uncached input for it. There's no partial credit for "nearly the same."

That's exactly what a "compress your context" tool does to you, two ways. One: if it ever goes back and pulls the full original it compressed (some call it rehydrating), you've already spent more that session than the compression could ever save. Two: the moment it changes how a provider expects the prefix to look, you fall off the cached tokens onto the full-price ones. Every case I measured, losing the cache cost more than the tokens the tool removed. The saving is a rounding error next to the penalty.

It's worse in practice, because every Anthropic reseller caches a bit differently. That's how I got over-billed in the first place. Cutting tokens in a way that survives all of them, without tripping any one provider's cache, turned out to be hard and provider-specific, not the one-line win the plugins sell. GPT-5.6 just sharpens the same edge. The numbers above are the OpenAI version of a penalty I first watched on Anthropic.

## RTK measures text, not money

`RTK` rewrites command output before it lands in history. Trims a chatty test run, collapses a big file listing. Its `rtk gain` counter reports how many tokens it saved.

It can't report that number, because it can't see it. RTK sees command output, nothing else. Not the API request, not the cache breakpoints, not the cache state, not the write or read token counts. `rtk gain` compares raw output to filtered output at about `characters / 4`. It's counting characters it deleted, not credits the provider never charged.

That gap matters, because coding agents already truncate big output before it reaches the model. RTK will happily claim it stripped hundreds of thousands of tokens from a file the agent would only have shown a few thousand of anyway. My own install reported about 6.1 million tokens saved on work where the real input was a fraction of that.

The independent benchmarks land where you'd expect. The one public GPT-5.6 comparison I could find ([Tura's benchmark lab](https://moltpress.org/tura_benchmark_lab/token-savings-completed-task-cost)) put RTK at +7.18% cost, except its own two-run arm varied by 30.78%, so that figure proves nothing on its own. The JetBrains benchmark is firmer: it debunked the headline 60% to 90% savings claim outright, and found RTK ran 14.3% more cache reads on 13.8% more turns. The tech news site TechTimes reported it on 21 July, under the headline [RTK raises Claude Code costs at low effort, JetBrains benchmark debunks 60-90% claim](https://www.techtimes.com/articles/321223/20260721/rtk-raises-claude-code-costs-low-effort-jetbrains-benchmark-debunks-6090-claim.htm).

One thing about that JetBrains result, because people keep drawing the wrong lesson from it. "RTK randomly nukes your cache" is wrong. RTK formats *new* output before it enters history. It doesn't rewrite a prefix that's already cached. Once the compressed result is in history, later requests reuse it fine. The extra cache reads are mostly the extra turns re-reading context, plus thin command coverage and provider-side truncation doing the real work anyway. More turns, not a busted cache.

There's a sharper failure than cost, though. I reproduced a correctness bug in RTK 0.43.0. My pytest config already passed `-q`. RTK added its own `-q`. The effective `-qq` swallowed the summary RTK then went looking for, and it failed. That's not a bigger bill on its face. But a rewrite that changes the result buys you a re-run and another turn, which *is* a bigger bill, by the back door.

## Headroom is more capable and harder to trust

`Headroom` proxies the real model request, so in principle it has what RTK lacks. It can compress large, brand-new tool output before that output enters the cache. With GPT-5.6 charging 125% on writes, shrinking something before it's written is exactly where the money is.

The catch is what it still can't see. Headroom sees explicit breakpoints if the client sends them. It can't see OpenAI's internal cache: which implicit breakpoint matched, or what OpenAI actually kept.

Two things in the current code make me distrust its dashboard as a GPT-5.6 ledger:

- It doesn't seem to support GPT-5.6's new explicit-breakpoint fields. It injects a `prompt_cache_key` and guesses which messages are still live. A stable cache key helps routing. It doesn't make two different prefixes match.
- Its cost model is stale. The code assumes cached reads cost 50% and writes carry no premium, and infers writes as uncached input because it says OpenAI exposes no write counter. On GPT-5.6 that's all wrong: reads are 10%, writes are 125%, and writes come back in `cache_write_tokens`.

Then there's rehydration. Headroom compresses something, the model later asks for the full original, and now you've paid for the compressed version, the retrieval tool call, another model turn, and the original in full. Unless the compressed version was reused enough times first to bank a saving, that one retrieval erases it.

In its favour, the current code restores frozen messages byte-for-byte, so I won't claim Headroom definitely busts the cache. That's unmeasured, not proven. But a dashboard doing counterfactual accounting on last year's prices isn't evidence it saved you anything.

## The bill isn't the tool output. It's replaying it.

Here's where I changed my mind about the whole category. Both tools fight over how big a single tool result is. That's not where a coding session's tokens go.

The clearest evidence I've seen isn't mine. It's a trace-level writeup on r/codex, [Important findings on cache and baked-in Codex behaviour](https://www.reddit.com/r/codex/comments/1v4vawj/important_findings_on_cache_and_baked_in_codex/), and the numbers below are the author's, not mine. They pulled traces from ten `gpt-5.6-sol` Codex rollouts. Ten sessions came to **252.2 million tokens: 251.7 million input, 581 thousand output.** Input was 99.77% of everything. Across 2,007 model calls, the average call took in **125,394 input tokens and produced 290.** Some of those sessions made three edits total.

That's the shape of it. The model isn't spending your tokens thinking or writing. It's re-sending its accumulated context (system prompt, tool schemas, repository instructions, file contents, shell output, patches, test logs, prior messages) hundreds of times. The average task made about 200 model calls, and peak input averaged 233,012 tokens, past 90% of the window, before compaction kicked in. The worst single task burned **61 million tokens over 434 calls in 98 minutes**, re-inspecting and re-checking against a history that only grew.

The waste starts before you do. In those traces the first request alone averaged about **30,550 input tokens**, before the model read one source file or ran one test. Most of that is the runtime's own furniture: system and safety instructions, tool schemas, skill descriptions, plugin and repo rules, environment metadata. The tool put it there, not you. Then it compounds. That worst task ran 132 file reads, 98 shell commands, 93 searches, and 78 patches, and every one stayed in the history the next call resent. Across the ten sessions the model was fed **8.21 million characters of tool output**. The author reckons an 8,000-character cap per result would have cut 2.93 million of them, 35.7%, before you count the saving from not replaying that text on every later call.

Now hold that next to the caching argument. The worst task had a **98.89% cache rate** and still logged 60.9 million input tokens. Across all ten, the weighted rate was 97.8%: 246 million cached against 5.5 million uncached. A high cache rate is exactly what makes people wave this off: "it's cached, it's basically free." On GPT-5.6 a cached read is 10% of input, not 0%. 10% of 246 million isn't free, and it's the same context going round again, not new work.

The writeup is careful on one point, and so am I. The traces don't show how a given plan meters cached tokens against a subscription, so neither of us is calling it a billing bug. But metering is the small question. The runtime makes enormous context traffic, keeps used-up material live far too long, and gives you no way to see or stop it. That holds whatever the discount on the replayed half.

Two more things fell out of the same analysis. Subagents make the accounting worse, not better. One 18-minute child agent ate 16.4 million tokens by itself. The parent spawned four, and only one child's trace was available, so the real total is higher than any number here. If your UI shows only the root task, you never see any of it. And the runtime ships with the savings switched off. The author read the source and found a `turn_cost_guard` that picks the earlier, cheaper summarisation, with every call site passing it `false`. A token-saving switch, hard-coded off, that no prompt you write can flip.

What turns this from waste into a grievance is that you can't switch any of it off. You can't shrink the base prompt, stop a skill being re-read twenty times, drop the schemas the task will never call, retire history the runtime is still hauling around, force a compaction, or cap it at fifty calls instead of four hundred. Compaction only fires at the cliff, past 90% of the window, not at the natural break between investigating and implementing where the old context stops earning its place. The author keeps a local fork and patched some of this back by hand. Almost nobody can do that, and nobody should have to fork their coding tool to stop it draining them.

## What actually lowers the bill

Line the failures up and they point one way. Compressing a tool result after the fact is the wrong layer. The bill is set by things a plugin can't touch:

- **Retire used-up context.** Once a file read or a passing test log has done its job, the model doesn't need its full text on the next 300 calls. Keep the raw log on disk. Leave a compact receipt in the prompt: status, the paths that mattered, what changed.
- **Don't reinject what hasn't changed.** An unchanged `AGENTS.md`, an unchanged skill file, the same source file read twice: represent it by a stored fact or a content hash, not a fresh copy pasted back into context on every call.
- **Load only the schemas the task needs.** A config change shouldn't open with every email, calendar, browser, and connector definition loaded. Defer the ones this task will never call.
- **Budget the output, not just the input.** A command that succeeded doesn't need the same 10,000-token allowance as one that failed with a stack trace. Ordinary success belongs closer to 1,500 to 2,500 tokens.
- **Compact at boundaries, not at the cliff.** Summarise when you cross from investigating to implementing, while you still know what mattered, instead of waiting for the context to hit 90% and dumping whatever's oldest.
- **Send the small model the small job.** A 125K-token context that produces 290 output tokens has no business on the top model. Most sub-tasks (a scoped edit, a lookup, a summary) belong on a cheaper one.
- **Cap the runtime, and show the bill.** Model calls, cumulative input, child agents, tool-output bytes, context percentage, repair cycles: budgets you can see and enforce, with root and child usage on the same screen, not a `turn_cost_guard` someone else nailed shut.

None of that is compression. It's holding less context, for less time, and refusing to replay it.

## This is what we build aimee to do

I didn't reverse-engineer that list from the blog post. It's the design brief for `aimee`, our local server that sits between a coding tool and the model. The controls Codex withholds are the ones aimee hands back, so getting them doesn't mean forking a runtime almost nobody can maintain.

Memory is the "stored fact, not a fresh re-read" point made real. Facts about the repo and past decisions are written once and recalled when they matter, so a session doesn't rebuild the same understanding, and re-pay that 30,550-token entry fee, every time it starts. A map of your code lets the agent navigate by structure instead of dumping files into the prompt to find one function. Cheap delegate models take the bounded jobs off the expensive one, so a 290-token edit doesn't ride on the top tier. The economizer is the accounting and the budgets the traces above show Codex withholding: where the tokens went, root and child on one screen, with caps you set on calls, input, child agents, tool-output bytes, and context. Not limits set for you, and switches nailed shut. And guardrails it can't write past, for the same reason. The runtime should answer to you, not the other way round.

I'm not going to hand you a savings percentage for aimee. That's the exact `rtk gain` move this whole post is against. The only honest number is cost per successful task, measured in paired runs: tool on, tool off, same model, same effort, same repos reset to the same state, same success check, several times over. That's the bar aimee has to clear too, and the one we hold it to.

## Bottom line

Delete the compression plugins. On the evidence, `RTK` shows no saving and sometimes a higher bill, plus a correctness bug I hit myself. `Headroom` could help on GPT-5.6 in theory, but its current build won't tell you whether it did. Both fight over the size of one tool result while the real bill is the same context replayed across hundreds of calls.

The lever that reliably lowers your bill isn't compressing the context you send. It's sending less of it, keeping what you do send byte-stable so the cache keeps working, retiring it once it's used, and putting the cheap jobs on cheap models. That's an architecture problem, not a plugin. It's why we build `aimee` around it, and why I'd still tell you to measure it before you believe it.
