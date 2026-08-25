---
title: "Everything Crosses One Transport"
slug: everything-crosses-one-transport
date: 2026-08-24
author: Rakuen Software
tags: [aimee, architecture, isolation, governance, event-bus]
excerpt: "Aimee routes supervised inter-module work through one typed transport per daemon. The host applies grants, orders accepted events and exposes one audit point. The coverage boundary matters as much as the mechanism."
---

*Rakuen builds aimee, the system reported on here. Third in a three-article
series, after the
[self-learning loops](https://rakuensoftware.com/blog/aimee-recursive-self-learning)
and
[memory](https://rakuensoftware.com/blog/the-remembering-is-the-learning).
Figures and source pins live in the [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/everything-crosses-one-transport/evidence/figures.md).
Source was rechecked against `testing` at `6bcc87e` on 25 August 2026.*

“Everything crosses one transport” needs a boundary. Inside each aimee daemon,
supervised inter-module requests, replies and events use one host. Calls among
seven components still linked into the core remain ordinary in-process calls.

Traffic between daemons and external clients uses authenticated network
surfaces. The transport observes what crosses it. A call that never enters the
transport sits outside this record.

Within that boundary, one shape repeats:

```text
producer -> private outbound ring -> host -> private inbound ring -> consumer
                                  |
                                  +-> ordered capture and audit tap
```

The host assigns order, checks the sender's grant and routes the frame. Each
client gets its own queue pair. A slow consumer meets bounded backpressure
instead of creating an unbounded host queue.

The design puts three old controls in one place: capability checks,
observability and an audit handoff. Its value comes from coverage. A rule
enforced at every supervised crossing has fewer bypasses to audit than a rule
copied into each caller.

## The measured figures are medians, and the ceilings are the guardrail

The committed baseline records a **134 ns median** for dispatch from host
enqueue to client dequeue. The test used batched samples, a 16-byte inline
payload and the reference development machine. It excludes whatever work the
receiving process performs.

Publishing one governed-action audit row cost the caller a measured **82 ns
median** on the same reference machine. That figure excludes the durable ledger
write, which happens away from the caller's thread.

The enforced numbers are larger: **2,000 ns** for dispatch and **5,000 ns** for
audit enqueue. A merge gate builds and runs the benchmark and fails when a
measurement exceeds its ceiling.

Those ceilings are regression guards with generous headroom. They are not
latency guarantees for every event, and the baseline makes no comparison with
an in-process call or another transport.

The architecture needs a cheap crossing because one request may make several
of them. The committed data shows that the current hot path sits well inside
its budget. A tail distribution and a per-request hop distribution have not
been published, so the article makes no claim about either.

## Frames move through private rings

The data path uses shared-memory rings. A client first connects through a Unix
`SOCK_SEQPACKET` socket. After admission, the host passes anonymous `memfd`
descriptors with `SCM_RIGHTS`. Ordinary frames then move through the mapped
queue pair without a per-event socket operation.

Small payloads fit inside a ring slot. Trusted code beside the host may use the
shared arena for larger payloads. Separately shipped processes stay off that
arena. Their protocol fragments and reassembles messages above the inline
budget, with a current limit of 16 MiB.

The shared arena provides cooperative isolation for trusted native code.
Hostile code needs a sandbox. A transport boundary and an execution boundary
solve different problems.

The repository carries C and pure-Go clients with byte-for-byte conformance
tests. The contract therefore avoids tying supervised processes to the host's
implementation language. It does not prove that every language or runtime has
a working client.

## Grants describe reach before a process starts

Admission begins with a grant file. It names a stable principal, the required
user id, an executable path and the event kinds the process may publish,
subscribe to, request or serve. The host reads those policies at startup and
checks identity again when a process attaches.

A grant answers a finite question: which bus operations can this identity
attempt. It does not answer whether the process will return a truthful result.
A compromised memory process may still return bad memory when answering memory
requests is part of its grant.

The grant also says nothing about activity kept inside the process. A program
can compute, allocate and fail locally without emitting a frame. Operating
system isolation, filesystem permissions and container policy carry that part
of the boundary.

The controls divide cleanly:

- The grant bounds reach through the supervised transport.
- The tap records accepted traffic according to its durability class.
- The execution environment bounds local access outside the transport.

Treating any one of those as the whole security model would overstate it.

## The tap sits before delivery

The host gives each accepted event a monotonic sequence number before routing.
The tap sees accepted events in that order. Request and reply frames retain a
correlation id, and replies return only to the requester.

Pressure stays visible. Event kinds declare whether they block or may shed.
Sheds create typed overflow records. Reaping a producer with blocked work
records the discarded sequence, kind and source slot.

Capture files preserve the accepted stream for inspection and observational
replay. Replay does not execute tools or drive a process again. Capture may be
disabled, pruned or abandoned after an I/O failure. Each transition to a broken
capture state writes a durable gap record with the last flushed sequence.

The durable audit ledger is a separate mechanism. The capture reconstructs
order. The ledger makes selected security records tamper-evident. Combining
those two in prose would promise more coverage than either provides.

One committed durability test emits **5,000** governed-action rows through the
real producer and consumer. It requires **5,000** ledger rows, each exactly
once, with zero drops, and it checks that graceful shutdown drains work in
flight. This result covers that audit migration. It does not establish
exactly-once delivery for every event kind on the transport.

## A chokepoint concentrates risk

One host per daemon is easier to inspect and also more valuable to attack. The
design reduces that host's job to envelope handling, ordering, routing,
backpressure and admission. Policy decisions stay in named processes with their
own grants.

That separation narrows the host. It does not make compromise harmless. A
host-level attacker could disrupt routing or falsify traffic presented to a
process. Downstream verification can catch some false claims by checking with
the authority that issued them, but its coverage depends on each protocol
actually doing that check.

The defensible claim is smaller: inter-module authority is declared outside the
participant, and the host enforces the declared event kinds. The current source
also records transport gaps and routes ledger-classified traffic to the durable
audit path. No penetration test or independent security audit is offered here.

## Delegates have a separate execution boundary

The transport alone cannot confine an agent process. Aimee delegates therefore
run in containers with networking disabled, no Docker socket and no ambient
provider, vault, git or host SSH credentials. The workspace is mounted at its
declared root, and resource limits bound CPU, memory, process count, time and
output.

External package requests use a mediated proxy or a prebuilt cache. The proxy
owns destination and protocol policy on the server side. The delegate never
receives host networking to make that request.

The runtime verifies the network mode, exact mount set and effective
credentialless environment after start or resume. An observation that fails or
cannot be made destroys the container. The trusted primary session remains a
separate host-execution path; it is not a fallback for a failed delegate.

The source documentation states the limit directly: this sandbox bounds damage
after a bad model or dependency decision, and arbitrary host mounts remain
unsafe. A writable worktree also comes from the agent's role and workflow.
Container membership does not grant it.

## Learned records get an independent audit intent

Memory mutations use a further path. Every changeset close now submits an
immutable audit intent inside the mutation transaction. A separately
credentialed worker turns committed intents into a hash chain.

The follow-up existed because five close paths once produced no audit record.
The structural check resolves those five sites, fails if any lacks its seal and
fails if its analysis resolves zero sites. In the live test, one closed memory
changeset produced one matching audit row. Removing the five seal calls reduced
the count to zero.

The recovery test then injected a crash after chain insertion and before
delivery acknowledgement. The transaction rolled back. Restart sealed the two
pending intents once, and a second restart added nothing. The final chain held
three rows and three witnesses with zero broken links.

This protects the integrity of the tested record. A coherent rewrite by an
attacker who controls the whole host still needs an off-host witness or anchor
for detection. Retention outside that host is an operator responsibility.

## Two daemons keep activity and shared state apart

A deployment has a shared control service behind per-user execution services.
The control side holds shared memory, learning gates and audit state. The
per-user side runs the work for one user.

The split changes the blast radius and creates a second account to compare. It
also creates deployment failures. Code can be built into the service that
cannot reach the provider it needs. The first article records one such defect
and the build-graph check added after it.

Separation therefore costs testing across the real topology. Unit tests that
inject every dependency can pass while one daemon omits the registration
needed in production.

## Configuration changes behaviour inside the boundary

Many ranking thresholds, learning policies and runtime choices are
configurable. Grants are different. The host loads them at startup, and the
source exposes no live reload path.

This keeps configuration from silently widening transport authority. An
operator can still install code with a broad grant, and the architecture cannot
protect an operator from deliberately giving authority away. It can make that
choice explicit and inspectable before the process attaches.

The title can now be stated precisely. Supervised inter-module work crosses one
typed transport per daemon. The host orders it, applies a declared capability
set and exposes one place to observe it. Core-local calls, external network
traffic and activity inside a process sit outside that claim and need their own
controls.
