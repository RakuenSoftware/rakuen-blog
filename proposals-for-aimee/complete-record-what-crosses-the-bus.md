# Proposal: A complete record of what crossed the bus

- **State:** 🔴 **PROPOSED — not started.**
- **Author:** JBailes
- **Date:** 2026-08-24
- **Charter roles:** Review (the record that makes review possible), Persist
  (a durable, non-prunable record), Gate-Promote (a guard that fails loudly
  when the record is absent).
- **Owns:** the durability contract for bus traffic, and the distinction
  between the diagnostic capture stream and the durable audit record.
- **Depends on:** `src/modules/audit/obs_bus.c` (the observability bridge and
  capture tap), `src/core/event_bus/bus_route.c` (shed and reap control
  events), the WORM audit ledger, `bench/bus_baseline.json` (the budget this
  work must not break).

## Problem

The bus is the one place every module request, reply and notification is
ordered and observable, and that property is load-bearing: it is what lets an
operator answer "what did this system do?" from one place instead of from
whatever each subsystem chose to print.

**The record of that traffic is not durable, and the gap is not visible from
inside the system.**

There are two records, and they are not the same thing:

| | carries | durable |
| --- | --- | --- |
| **WORM audit ledger** | two event kinds: `OBS_BUS_KIND_ACTION` (3000) and `OBS_BUS_KIND_GUARDRAIL` (3001) | yes |
| **Capture stream** | every routed event, in sequence order | **no** |

`docs/EVENT_BUS.md` states the division correctly: "The durable WORM audit
ledger remains the security record. Capture is the ordered diagnostic and
replay layer above it." The code agrees, in `obs_bus.c`:

> Best-effort: if there is no writable home the tap is NOT registered (capture
> off ...), and audit still works — the ledger is the durable record, capture
> is the replay layer on top.

That division is a reasonable design. The problem is what has accumulated on
top of it: **the things a reviewer most needs are in the layer that is allowed
to disappear**, and nothing tells them it disappeared.

### Capture can be absent, truncated, or pruned

Three ways the capture stream is not there when someone goes looking:

1. **Off from the start.** `capture_open()` sets `cap_fd = -1` and returns
   without registering the tap when there is no writable home directory, or
   when the file cannot be opened. It logs a `WARN` and the daemon runs
   normally.
2. **Abandoned mid-stream.** `capture_flush()` closes the fd and sets
   `cap_fd = -1` on a short or failed write, or when the in-memory sink breaks
   on allocation. From that point the process keeps running and writes nothing
   further. Again, a `WARN`.
3. **Pruned.** `capture_prune()` keeps the newest `AB_CAP_KEEP` sessions
   (currently **16**) and unlinks the rest, on every capture open.

None of those is wrong on its own. Together they mean a capture file is not
evidence of anything a month later, and its absence is indistinguishable from
a period in which nothing happened.

### The evidence of loss is itself only in the losable layer

This is the sharpest form of the problem. The bus is careful about loss:

- `shed()` emits a `BUS_KIND_OVERFLOW` control event naming the exact `seq` and
  `event_kind` a full destination lost;
- `bus_route_forget_slot()` emits `BUS_KIND_PRODUCER_REAPED` for a block-held
  event discarded when a slot departs, with the comment "name its seq to the
  tap as producer_reaped so the loss is recorded, not silent."

Both go **to the tap**. The tap goes to capture. Capture is the layer that can
be off, abandoned or pruned. So the record that something was lost is kept in
the one place that is itself allowed to be lost, and a reviewer who finds no
overflow records cannot distinguish "nothing was shed" from "the shed records
went with the capture file."

### Module request/reply reaches no durable record at all

Every module call goes through `aimee_module_call` in
`src/core/event_bus/module_client.c`. That file contains **zero** audit
emissions.

So a module decision reaches the durable ledger only if the caller separately
emits one, and most do not. The following are consequential decisions that
cross the bus and are durable nowhere:

- the memory typed-fact **write gate** (`5890`), deciding whether a candidate
  triple may commit as a semantic edge;
- memory **extraction and the retraction pre-scan** (`5889`);
- the memory **PII recall gate** (`5892`) — a withhold decision about sensitive
  data leaves no durable trace of having been made;
- the memory **confidence band** (`5893`);
- the **learning signal sink mask** (`6145`), which decides which sinks a
  learning signal reaches before anything is persisted;
- **skills trigger matching** (`7682`);
- **workflow advance admission**, and **governance's response tool-policy
  decision** — both documented as fail-closed, neither durably recorded as
  having fired.

Governed actions, guardrail decisions, memory mutations, vault access, sandbox
degradation, MCP activity and tool completions do reach the ledger, through
their own bridges. Everything else does not.

### Components that never emit at all

Eight components are `execution: core` in `src/modules/process-contracts.json`
— compiled into the daemon rather than run as module processes. Their
inter-component calls are ordinary function calls and cross no transport, so
nothing observes them by construction. Of the eight, these have **no audit
emission anywhere in their tree**:

| component | audit emitters |
| --- | --- |
| `gateway` | 0 |
| `execution-policy` | 0 |
| `ir` | 0 |
| `translation` | 0 |
| `protocols` | 0 |
| `module-runtime` | 0 |

`vault` and `audit` are the exceptions: vault has `src/server/vault_audit_bridge.c`,
and audit is the bridge.

`execution-policy` is the one to look at first. A policy component that makes
decisions and emits no audit row is the shape of gap this proposal exists to
close.

## Non-goals

- **Not moving the core components onto the bus.** That is a much larger piece
  of work with its own performance and layering consequences, and this proposal
  does not depend on it. What is proposed here is that the components which
  *do* cross the bus produce a durable record, and that the ones which do not
  are named rather than assumed.
- **Not making capture durable.** Capture is correctly a best-effort diagnostic.
  The fix is to stop asking it to carry evidence, not to promise it will never
  be pruned.
- **No new always-on cost on the hot path** beyond the committed budget. The
  bus's value depends on 134 ns dispatch and 82 ns audit publish
  (`bench/bus_baseline.json`); an unconditional durable write per event would
  destroy that and is not what is proposed.

## Decision

Four slices, ordered so the visibility work lands before the coverage work.

| Slice | What it does |
| --- | --- |
| **C0** | Absence becomes observable: a capture gap is a first-class, queryable fact rather than a `WARN` |
| **C1** | Loss records escape the losable layer: overflow and reap reach the durable ledger |
| **C2** | A declared coverage contract: every bus event kind declares its durability class, checked by lint |
| **C3** | Close the gaps C2 names, starting with the decision seams |

### C0 — A capture gap is a fact, not a log line

Today the three failure paths log `WARN` and continue. Make each of them
record a durable **capture-gap marker** in the audit ledger: session id, the
last sequence number captured, the reason (`no_home`, `open_failed`,
`write_failed`, `sink_broken`), and the wall time.

Add the symmetric marker on prune: when `capture_prune()` unlinks a session
file, record that the session existed and is gone.

The point is that a reviewer looking at the ledger can see *"capture stopped
here"* and *"session N was pruned"*. Absence stops looking like silence.

Health output gains a `capture_ok` field with the reason when false, so an
operator does not discover a month later that the replay layer has been off
since a disk filled.

### C1 — Overflow and reap reach the durable ledger

`shed()` and `bus_route_forget_slot()` continue to name the loss to the tap,
and additionally emit a durable audit row. These are rare by construction — a
shed means a destination was full, a reap means a slot departed with work in
flight — so the cost is bounded and does not touch the ordinary path.

A dropped event may be routine. A dropped event nobody can later prove was
dropped is not.

### C2 — Every event kind declares its durability class

Add a `durability` field to each event kind's declaration, with three values:

- **`ledger`** — a durable audit row is written for every occurrence;
- **`capture`** — diagnostic only, deliberately not durable;
- **`sampled`** — durable at a declared rate, for high-volume kinds where
  per-event durability is genuinely unaffordable.

Then a lint check, in the same shape as `check_provider_registration.py`:
for every event kind a module's `module_api.h` declares, require a `durability`
value and require that a `ledger` kind actually has an emitter on its handling
path. A kind with no declaration fails the build.

The check must carry its own unit tests in the same target so it cannot pass
vacuously, and must exit non-zero rather than reporting `ok` when zero kinds
resolve — the failure mode `check_provider_registration.py` already guards
against.

This is the slice that makes the coverage claim checkable instead of
believed. It also produces the list C3 works from, and keeps that list from
going stale.

### C3 — Close the named gaps

Working from C2's output, and in this order:

1. **The decision seams**, because a fail-closed decision that leaves no trace
   cannot be audited or disputed: PII recall gate, typed-fact write gate,
   learning sink mask, governance tool-policy, workflow advance admission.
2. **`execution-policy`**, which makes decisions and emits nothing.
3. **The remaining `ledger`-classified kinds** C2 finds without an emitter.

Kinds that are genuinely diagnostic are marked `capture` and left alone. The
deliverable is not "everything is durable"; it is that every kind's durability
is a declared, checked decision rather than an accident of which bridge
happened to get written.

## Threat and failure model

| Failure | Control |
| --- | --- |
| A period with no record is read as a period with no activity | C0's capture-gap markers and prune markers make absence explicit |
| Loss records lost with the capture that held them | C1 puts overflow and reap in the ledger |
| A new event kind ships with no durability decision | C2 fails the build on an undeclared kind |
| The lint check silently stops covering anything | C2 exits non-zero on zero resolved kinds, and carries its own tests |
| Durability cost creeps onto the hot path | `bench/bus_baseline.json` ceilings and the existing merge gate; `sampled` exists for the high-volume cases |
| A fully compromised host forges or suppresses the record | Out of scope and stated: `docs/EVENT_BUS.md` already says an off-host witness or anchor is required for that case. This proposal does not change it |

## Acceptance

- A capture gap in each of the four reasons produces a durable marker, proved
  by inducing each condition (read-only home, open failure, write failure,
  sink break) and reading the ledger back.
- A pruned session leaves a durable marker naming the session.
- A shed and a reap each produce a durable row, proved by filling a
  destination and by killing a slot with work in flight.
- `make lint` gains the durability check, green, with its own tests, and
  reports a real count.
- Every kind in the C3 list either emits durably or is declared `capture` with
  a recorded reason.
- `make -C src lint`'s bus perf gate stays green: dispatch overhead within the
  2,000 ns ceiling and audit enqueue within 5,000 ns.
- The e2e suites run on a real two-service stack with PostgreSQL, in the shape
  of `tests/e2e/module-liveness-pg-e2e.sh`, and are proved against the bug:
  disabling capture must turn a "the record is complete" assertion red.

## What this does not fix

The eight `execution: core` components still call each other in-process, and
nothing observes those calls. C2 and C3 improve the record of what crosses the
bus; they do not make the core components cross it. That boundary should be
stated wherever the completeness of the record is described, including in
`docs/EVENT_BUS.md`, so the claim matches the mechanism.
