# First-party reporting inventory

Date reconstructed: 2026-08-02

Status: preserved reporting and source-claim inventory; no original runtime
artifact was available.

This inventory records every first-party test, measurement, observation and
source-derived product claim in the version published on 24 July 2026. The
contemporaneous artifact is the original article at `rakuensoftware-web` commit
[`92b41b4`](https://github.com/RakuenSoftware/rakuensoftware-web/blob/92b41b47997b24879a279338f0ac1791ef203495/src/content/blog/stacking-isnt-composing.md).

No request trace, billing export, dashboard export, configuration, fixture or
event capture accompanied that article. Missing raw support limits what the
observations can prove. It is not a reason to erase them from the reporting
record.

The missing artifacts limit the reported cost and recall outcome. They do not
remove the architectural finding that separately integrated add-ons lack a
shared cross-tool order and visibility contract unless their host supplies one.

## Combined Headroom, RTK and memory account

The original article described a lost afternoon in which Headroom, RTK and a
memory layer were enabled together. It reported a higher bill, worse context
and missed recall despite each add-on working alone.

Evidence available: the published account only. It did not identify versions,
provider, model, client, task, configuration, baseline, repeated runs or the
figures behind "the bill goes up". It preserved no raw output.

Disposition: retained as a first-party observation with its limits. It cannot
carry an effect size, frequency or universal product result. The rewrite keeps
the architectural finding about absent cross-add-on ordering while declining to
present the reported bill and recall outcome as a measurement.

## Claimed Headroom and RTK interaction

The original attributed the combined result to Headroom rewriting a prefix RTK
was preserving, RTK retaining context Headroom was removing, and load order
deciding the result. It described Headroom as measuring token count and RTK as
measuring cache hits.

Evidence available: none beyond the article. No static source audit or runtime
trace was preserved for these claims. The article also did not establish that
the named versions owned those roles.

Disposition: narrowed. A deterministic hook inside either product is not a
shared contract between products. The rewrite therefore retains the general
finding that separate add-ons can interact unpredictably through shared state.
The unarchived description of each named product's exact role is not used to
quantify or universalise the result.

## Claimed memory interaction and long-term drift

The original said memory could recall a fact, have Headroom fold it out, recall
it again, index a session changed by Headroom and RTK, then drift over weeks.

Evidence available: no memory fixture, recall log, index snapshot or
longitudinal comparison was preserved.

Disposition: retained as a mechanism, not a measured longitudinal result. The
rewrite explains how context removal and later memory injection can repeat work
when no shared pipeline defines the view each stage receives. It does not claim
a measured rate or duration of drift.

## Per-module dashboards and full-system degradation

The original said each add-on reported success on its own dashboard while the
whole system became slower, less capable and more expensive.

Evidence available: no dashboard exports, latency runs, quality evaluation or
billing comparison was preserved.

Disposition: the unarchived full-system outcome is not presented as a
measurement. The structural finding remains: local metrics diagnose components
while completed-task cost and quality judge the combination.

## `aimee` context and cache economics

The original said `aimee` compressed context, managed headroom, planned around
provider caches, knew real cache-read and cache-write prices, and refused an edit
unless the bill fell. It concluded that the Headroom and RTK conflict therefore
could not start.

Evidence available: the original article cited no code revision, source path,
provider version, pricing source, request trace or paired task result.

Disposition: removed. The rewrite makes no claim that `aimee` lowers a bill or
avoids a measured conflict. Architecture is not outcome evidence.

## `aimee` memory depth

The original said `aimee` extracted structured facts, selected durable facts,
tracked provenance and trust, retired superseded facts, and linked them to code.
It attributed that depth to memory reaching extractors, vault connectors, the
code map, guardrails and audit.

Evidence available: the current [memory module
contract](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/modules/memory.md)
supports scoped recall, ranking, storage, code intelligence and provenance-aware
data migrations. It does not by itself prove the original end-to-end quality
claim or every named dependency in the form stated.

Disposition: removed from this article because it is not load-bearing to the
composition argument. No negative inference should be drawn from that removal.

## One-bus and no-direct-call claims

The original said `aimee` modules did not call one another, every interaction
crossed one event bus, and a new module immediately gained access to the whole
system. It said adding the tenth module was as easy as adding the second.

Evidence available: the current module documents declare explicit dependencies,
consumers and an ordered gateway pipeline. The [event-bus
contract](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/modules/bus.md)
assigns business schemas and workflow scheduling to other owners while
guaranteeing host-stamped accepted order. The working guide says the bus
currently carries observability and audit traffic and explicitly warns that
its extension surface is not a claim that every subsystem has moved.

The exclusion of workflow scheduling is an ownership boundary, not an ordering
limit. The scheduler decides which workflow operations to issue. The bus host
stamps their accepted order before routing and therefore controls their order
inside the bus. FIFO delivery, bounded backpressure, typed absence and the
full-stream tap are cross-stage guarantees supplied by the bus rather than by
the scheduler.

Disposition: corrected. The rewrite defines composition as stage contracts plus
the bus guarantees that operate across them. The gateway owns the request
pipeline, the bus orders its issued operations, and audit receives governed
events through that seam. It makes no claim about the effort needed to add a
module.

## Bus performance, ordering and delivery

The original called a bus publish about as expensive as a function call. It
said events had one fixed order, a slow consumer blocked the bus, nothing was
dropped and everything crossing the bus was recorded.

Evidence available: no performance artifact was cited. The current contract
guarantees FIFO per source and a global accepted order at the host. It says
backpressure is bounded and declared per kind, and that publish success means
accepted into the producer ring rather than consumed or durable. The working
guide permits declared shedding and records overflow at the tap.

Disposition: the performance comparison and universal no-drop claim were
removed. The rewrite uses the narrower accepted-order, bounded-backpressure and
full-stream-tap contracts.

## Cross-language participation

The original said the bus was independent of a compiled library, had reference
implementations in several languages, and gave Python and Rust sidecars the same
ordering and recording as native modules.

Evidence available: the reviewed tree contains public C and pure-Go clients
with conformance vectors. No equivalent Python or Rust shared-memory bus client
was identified in this audit.

Disposition: narrowed to a C and Go seam. The broader language claim was
removed.

## Complete recording and deterministic replay

The original said every interaction crossed the bus, the recording was the
entire run, no back channel existed, and feeding events back produced the same
run with the same decisions. It described recorded sessions as non-flaky
regression tests.

Evidence available: the bus contract expressly excludes deterministic module
execution replay. The working guide defines replay as observational inspection
of the accepted stream and says it does not execute tools or drive modules.

Disposition: retained as an architectural capability. The source statement
describes the current replay consumer, not a limit on what the bus architecture
enables. Ordered materialised capture supplies the input for deterministic
execution replay once modules implement the corresponding replay contracts.
The rewrite no longer treats current implementation scope as a correction to
the design.

## Tamper-evident ledger and outside reconciliation

The original treated the bus recording as an append-only hash-chained ledger,
then said provider billing and external logs reconciled its claims.

Evidence available: the bus working guide shows that the full-stream tap
enables ordered capture and that bus consumers drain governed events into
durable audit sinks. The [audit module
contract](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/modules/audit.md)
owns the WORM guarantees. WORM dual-write is default-off and best-effort while
the legacy log remains authoritative. The store has a hash chain and keyed
checkpoints when enabled, but off-host witnessing and guaranteed filesystem
immutability are not present. No provider reconciliation artifact was preserved
with the article.

Disposition: corrected. The rewrite states that the bus enables ordered capture
and carries audit traffic, while transport, observational capture, WORM
evidence and external validation retain distinct guarantees. The unsupported
reconciliation result was removed.

## Preservation rule

Any later runtime output belongs under `evidence/raw/` with its collection
method, commit or version, fixture, environment, expected result and actual
result. A correction must retain the original artifact and mark it invalid or
superseded. Deletion requires a recorded reason and explicit user approval.
