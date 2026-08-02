---
title: "Stacking isn't composing"
date: 2026-07-24
author: Rakuen Software
tags: [agents, llm, architecture, aimee]
excerpt: "Modules do not compose because they share a process, a plugin API or an event bus. They compose when the system settles ownership, order, failure and evidence at every shared boundary."
---

Modules do not compose because they can be installed together. They compose
when the system defines what each module may change, in what order, and what
happens when one cannot proceed. A plugin API can settle the shape of a call.
It cannot settle who owns the state behind it.

*Correction, 2 August 2026: The previous version did not preserve the traces
behind its joint add-on account, so the exact cost and recall outcome is not a
measurement. The architectural finding remains: separately integrated add-ons
have no shared contract guaranteeing cross-tool order or visibility, and their
combined behaviour can therefore be unpredictable.*

This is reported analysis based on the public `aimee` source at commit
[`7223411`](https://github.com/RakuenSoftware/aimee/tree/72234117fb4155103a59a484459fa902363e2715).
The source establishes what the parts promise. The conclusions about system
design are mine.

Disclosure: Rakuen Software builds `aimee`. Its architecture is evidence for
the ordering and ownership claims here, not for a cost or quality outcome.

## Add-ons have no guaranteed shared order

Pure functions compose because one produces a value and the next consumes it.
Agent tools usually work on state: a request under construction, a cached
prefix, a memory store, a budget or a policy decision. Two modules can expose
clean interfaces and still make incompatible edits to the same state.

An add-on may be deterministic inside its own hook. That does not give it a
contract with another add-on attached through a client, proxy or memory layer.
Unless the host defines a shared pipeline, their combined order emerges from
those separate integration points. Neither add-on can guarantee which view of
the shared state the other will receive. A client update or configuration
change can change the result without changing either add-on.

The strongest case for stacking is replaceability. Independent tools let an
operator choose one component, upgrade it alone and remove it without replacing
the system. Keep that property. Add a joint contract wherever two tools touch
the same resource.

Consider a tool that shortens command output, a stage that decides which prompt
prefix must stay stable, and memory that injects recalled context. Their names
do not determine their shared order. The pipeline must say which view memory
sees, where reduction happens, and which stage owns the final request. Without
that contract, each part can behave correctly while the combination changes a
cache boundary, removes context another part needs, or recalls the same fact
again.

That is the finding. A joint trace is needed to quantify the resulting bill,
recall loss or frequency. It is not needed to establish that independently
integrated add-ons lack a guaranteed shared order of operation.

## A bus carries contracts; it does not create them

The current [`aimee` event-bus
contract](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/modules/bus.md)
is narrower than the old article claimed. It gives each source FIFO delivery,
stamps a global accepted order, declares bounded backpressure by event kind and
provides one full-stream tap. A successful publish means the producer ring
accepted an event. It does not mean a consumer acted on it or stored it.

Those are useful guarantees. They do not define the meaning of an event, choose
the order of business stages or give two modules a shared objective. The bus
document explicitly excludes workflow scheduling, WORM storage, network
transport between services and module business schemas.

A transport can carry two incompatible decisions perfectly. Composition lives
one level above it, in the ownership and stage contracts that decide which
decision is allowed to exist.

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

## `aimee` uses the bus as the enabling seam

At the reviewed commit, `aimee` has useful pieces of this replacement. The bus
provides a bounded typed seam for C and Go modules, enables full-stream capture
and carries governed actions to the audit sinks. The [gateway
contract](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/modules/gateway.md)
owns the ordered request pipeline. Audit owns its records. Those boundaries are
what make the bus compositional: one shared route, with separate owners for the
meaning, execution and evidence around each event.

They do not prove that adding another module is easy, that no path bypasses the
bus, or that the whole system lowers cost without harming results. Source
architecture cannot prove those outcomes. Full-system tests have to.

Before installing two agent add-ons, write down the shared resources, the owner
of each final value, the stage order, the failure rule and the outcome measure.
If the tools cannot fit that contract, the stack is still an experiment. Run it
as one, keep the handoff traces, and do not call it composed yet.
