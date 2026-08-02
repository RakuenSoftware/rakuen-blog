---
title: "Stacking isn't composing"
date: 2026-07-24
author: Rakuen Software
tags: [agents, llm, architecture, aimee]
excerpt: "RTK rewrites shell output. Memory stores that view. Headroom compresses it again. One confused extra turn can cost more than the context they removed."
---

[RTK](https://github.com/rtk-ai/rtk/blob/e0ffd40ef7c450489aca4a50c0ab1358e4375691/README.md#how-savings-work)
rewrites supported shell output before the agent reads it. Bolt on a semantic
memory add-on and it stores the view it receives, which now contains
RTK's rewrite. When memory recalls that view later,
[Headroom](https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/ccr/response_handler.py#L420-L529)
compresses the assembled request again.

Headroom can recover the original block Headroom received. It cannot restore
detail RTK removed before that request existed, and memory cannot recall detail
it never indexed. RTK reduced the shell output. Memory found a match. Headroom
reduced the request. All three worked.

The combined agent can still need another model call to retrieve what Headroom
removed, work from detail RTK already discarded, or recall the same incomplete
fact again. Three local savings have become a larger bill.

Context cost is linear: send twice as many uncached input tokens in one call
and you pay for twice as many input tokens. Turn cost compounds. Each new call
resends the accumulated conversation and adds another turn to it. If that
history grows by a similar amount per turn, the total context processed follows
`1 + 2 + ... + n`. It grows quadratically with the number of turns.

This is why unusable context is not merely a quality problem. If the agent
cannot make sense of a shortened, recalled and recompressed view, the recovery
turn pays for that view again, the rest of the live history and the new request.
Giving the agent the original context once can be cheaper than giving it less
context and making it ask twice.

That is stacking. Each add-on is deterministic inside its own hook. Their
combined behaviour depends on which view each hook receives, which client path
ran and which transformation landed first. No add-on owns that sequence. No
add-on can predict the bill it produces. Installability is not composition.

## Three correct tools see three different sessions

RTK's contract ends when it emits shorter shell output. It cannot say whether a
later memory hook stores the raw command result or the rewritten one, because
the raw result has already gone. That is not a defect in RTK. Filtering the
output is its job.

The semantic memory add-on indexes the session its host exposes. When it recalls
a fact, it puts text back into a later request. It does not know that RTK removed
detail upstream, or that Headroom may replace the recalled block downstream.
Similarity can be high while the available fact is incomplete.

Headroom's contract begins at the assembled model request. Its proxy compresses
new material, preserves stable cache prefixes and keeps the pre-compression
block for retrieval. That recovery is real. It reaches back to Headroom's
input, not past it to the shell output RTK already changed. When retrieval
fires, Headroom appends the recovered block as a tool result and makes another
continuation call.

The strongest case for stacking is replaceability. Independent tools let an
operator choose one component, upgrade it alone and remove it without replacing
the system. Keep that property. It does not supply the missing cross-tool
contract. RTK owns its output rewrite. Memory owns its index and recall.
Headroom owns its request compression and recovery. No component owns the
history all three are changing.

That is the finding. A joint trace is needed to quantify the resulting bill,
recall loss or frequency. It is not needed to establish that independently
integrated add-ons lack a guaranteed shared order of operation.

*Correction, 2 August 2026: The previous version did not preserve the traces
behind its joint add-on account, so its exact cost and recall outcome is not a
measurement. That limit does not change the architectural finding.*

This is reported analysis based on pinned public source for RTK, Headroom and
`aimee`. The source establishes how the parts work. The conclusion about their
composition is mine.

Disclosure: Rakuen Software builds `aimee`. Its architecture is evidence for
the ordering and ownership claims here, not for a cost or quality outcome.

## The bus provides the guarantees composition needs

The current [`aimee` event-bus
contract](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/modules/bus.md)
gives each source FIFO delivery and stamps a global accepted order before
routing. Operations that use the bus therefore enter the system in an order
chosen by the host, and consumers observe that order. It also gives the stages
bounded backpressure, typed absence and one full-stream tap. These are the
cross-stage guarantees that let their contracts compose.

The bus does not own workflow scheduling. A scheduler still decides which
operations a workflow should issue and when to issue them. The bus controls the
accepted order of those operations once issued. Every stage therefore acts
against the same sequence instead of the order in which independent hooks
happen to run.

Composition is the stage contracts plus the bus. The contracts define what an
operation means, which stage owns it and what the next stage may assume. The bus
enforces the shared order and delivery rules across those contracts. Remove
either half and the stages stop composing.

## The bus makes replay possible

The bus is the enabling seam for both capture and audit. Its full-stream tap
feeds ordered capture, and its observability bridge carries governed actions to
consumers that drain them into audit sinks. Without the bus, those paths would
need separate wiring and could disagree about order.

Capture and WORM audit remain separate subsystems inside `aimee`, with the bus
underneath both. The [`aimee` bus working
guide](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/EVENT_BUS.md)
describes capture records containing the accepted frame and its materialised
payload in bus order. That ordered stream is the input a replay system needs.
The current reader exposes observational replay. Execution replay can consume
the same record as module replay contracts are added.

The bus carries audit events. The [audit
module](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/modules/audit.md)
owns safe record formation, storage and verification. Its WORM store has
append-only triggers, a hash chain and keyed checkpoints when enabled. Capture
supplies the ordered accepted stream. Audit supplies a tamper-evident record of
the governed events it receives from that stream.

This is the architectural consequence of one bus: capture, audit and replay can
share the same accepted order without becoming one subsystem. Full execution
replay is another consumer of that record, not another back channel that must
reconstruct the run.

## Composition assigns an owner to every shared decision

A composable agent system needs a contract at each place where modules can
change one another's result:

- **Assign one writer.** One stage owns the final form of each shared resource.
  Other modules propose changes or consume named views.

- **Fix the stage order.** A context reduction before the first cache write is
  a different operation from the same reduction after it. The pipeline records
  which one happened.

- **Declare failure.** Each boundary says whether pressure blocks, sheds,
  retries or aborts. A local success cannot conceal a failed consumer.

- **Measure the completed outcome.** Token count, cache activity and retrieval
  score diagnose parts. Cost and quality per successful task judge the system.

- **Separate action from evidence.** Transport moves the decision. Capture
  records an observation. Audit protects a bounded claim about it. An external
  result can test that claim.

For the context example, the contract could give one gateway stage ownership of
the provider request. The output reducer would submit a typed candidate change.
The cache policy would accept or reject it against the prefix already written.
Memory would receive an explicit original or reduced view rather than whichever
string happened to be left. The specific design can change. The ownership
cannot stay implicit.

## `aimee` keeps one recoverable history

`aimee` converts each provider request to canonical IR before the economizer
touches it. In the safe tier, command condensation keeps failures and
diagnostics, writes the full tool output to a bounded spill and leaves a
recovery pointer. Folding and condensation happen before cache alignment.
Provider translation happens last. One stage owns each transformation, and the
next stage receives the result named by that contract.

Memory runs inside the [ordered gateway
pipeline](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/modules/gateway.md).
The event bus gives operations across those stages one accepted order, enables
full-stream capture and carries governed actions to audit. Memory does not have
to infer which add-on rewrote the session. Cache alignment does not discover a
context edit after it happened. Recovery reaches the tool output preserved by
the same system, not the last lossy view one add-on happened to receive.

That architecture does not prove a lower cost or better answer. It proves the
difference the article turns on: the stack gives three tools three partial
histories; `aimee` gives contracted stages one ordered, recoverable history.

Before installing two agent add-ons, write down the shared resources, the owner
of each final value, the stage order, the failure rule and the outcome measure.
If the tools cannot fit that contract, the stack is still an experiment. Run it
as one, keep the handoff traces, and do not call it composed yet.
