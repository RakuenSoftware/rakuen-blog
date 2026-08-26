---
title: "Everything Crosses One Transport"
slug: everything-crosses-one-transport
date: 2026-08-24
author: Rakuen Software
tags: [aimee, architecture, isolation, governance, event-bus]
excerpt: "A language model does not need a new safety discipline invented for it. It needs to be made subject to the ones we have had for decades. A cheap, governed transport makes that practical across the system."
---

*Rakuen builds aimee, the system written about here. Third of three: the
[self-learning loops](https://rakuensoftware.com/blog/aimee-recursive-self-learning)
come first and the memory second. This one is the architecture both of those
stand on. Figures are traced in the [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/everything-crosses-one-transport/evidence/figures.md).*

The goal of the whole system is one sentence: an AI system that is auditable,
governable, and will not wake an engineer at two in the morning.

That last clause is the acceptance test, and the first two are what make it
reachable. A system you cannot audit wakes you because nobody can say what it
did. A system you cannot govern wakes you because anything it might have done
is still on the table. Make both of those answerable in advance and the call
either does not come, or is over in a minute.

There is a user-facing form of the same goal, and it is the one I would give
first if somebody asked what aimee is meant to feel like. A short setup, and
then nothing. It should be invisible. If you want to know what it is doing
there are metrics, more of them than anyone is going to read in a sitting, but
wanting them should be a choice, and the thing works whether or not you look.

After installation, a user should not have to know aimee is there.

The two in the morning criterion, seen from the other end of the day. A system
that needs attention gets it, at whatever hour it decides to ask. The way not
to be woken by something is for it to not need you.

From that goal comes a rule that runs through every part of what follows:
almost unlimited customisation across the whole system, over defaults chosen to
be sensible and boring. Both halves carry weight. The defaults are how the two
in the morning promise is kept for somebody who changes nothing, and the
customisation is what stops that promise being a cage for somebody whose
situation is not ours. A later section covers why those two do not cost each
other anything here.

The premise of the architecture follows from the same goal. A language model
does not need a new discipline invented for it. It needs to be made subject to
the ones we already have.

We know how to do access control. We know how to do observability.

We know how to do audit logging, capability grants and separation between a
control plane and the things it controls. None of that is research. It is decades of ordinary
engineering, most of it settled before anyone reading this started working, and
all of it built for exactly this situation: a component you cannot fully
predict, which must therefore be bounded by what it can reach and be visible in
what it does.

The mistake I see repeatedly is treating a model as a special case that needs
its own safety theory. It is a component. Put it inside the patterns, deny it
ambient authority, record what it does, and the problem becomes one you can
staff with the engineers you already have.

The obstacle was cost. If every request has to cross an observable,
policy-enforced boundary, that crossing has to be cheap enough that engineers
do not create exceptions. The rest of this article is about the transport that
made the boundary practical.

We call the thing aimee's modules talk over an event bus, and it is not really
an event bus. An event bus is fan-out: a producer publishes, subscribers
receive, nobody answers. This carries point-to-point request and reply with
typed capability errors, cancellation, bounded backpressure, and large payloads
passed by shared-arena lease. The ordering and the single transport are the
resemblance, and that is where it ends.

Nor is it a bus in the older sense. A bus is a shared medium that devices
contend for. Every client here has its own private queue pair, mapped into its
own address space, and cannot see or map anyone else's. Nothing is shared and
nothing contends.

What it is, described plainly, is a broker-mediated message router whose
transport medium is shared-memory ring buffers. The host is the part that
matters: it moves frames between clients, orders them, and routes them by
pattern under credit-based flow control. Shared memory is how frames move. The
host is what makes it a system.

That has neighbours, and they are worth naming. Ring-buffer IPC is a
well-trodden path: the LMAX Disruptor, virtio vrings, `io_uring`, the DPDK
rings. Aeron is the closest whole system I know of, a media driver process plus
shared-memory ring buffers carrying publications and subscriptions, and anyone
reaching for a comparison should reach for that one first. The admission model
comes from somewhere else entirely: capability microkernels in the seL4
tradition, where a component may only send on endpoints it holds a capability
for, which is what a grant is.

The lineage is clear. The transport shape comes from the ring-buffer line and
admission comes from the capability line. Aimee adds a mandatory full-stream
tap ahead of routing and requires governed inter-module traffic to cross that
path. I have not found those pieces combined in the same way, but that is an
account of what I have seen and worked with, not a field survey.

It is the only part of aimee I would call novel, and it is not an oddity off to
one side of the architecture. The self-learning loops in the first article are
decades-old technique, and the memory in the second is careful work on old
ideas. Take this piece out and there is no version of either that survives,
which is a stronger claim than calling it the one new part.

The whole argument has that shape. Every technique here is one the industry has
had for years, and the reason they were not already applied to an agent this
thoroughly is that applying them everywhere was too expensive to consider. Make
the crossing cheap and the old techniques become available again, at a scale
where nothing needs an exemption. Nothing here contributes a new idea about
safety.

What it removes is the cost that stopped people using the ideas they
already had.

The audit record, the grants, the isolation, the language-neutral module
boundary and the loops being safe enough to leave running all depend on one
transport being cheap enough for governed work to use consistently. Make the
crossing expensive and exceptions become tempting. Once exceptions appear,
the coverage claim becomes a list of paths somebody remembered to instrument.

## The crossing is cheap enough to use throughout the design

The committed baseline reports a **134 ns median** for dispatching a 16-byte
inline event from a producer ring to a subscriber ring on the reference host.
Enqueuing a governed-action audit intent reports a **117 ns controlled median**:
the median of eight per-run medians, with each run timing 5,000 emits while
pinned to one CPU. Those are observations, not maximums.

`bench/bus_baseline.json` sets a **1,000 ns regression ceiling** for both
dispatch and audit enqueue. The merge gate rebuilds and runs each benchmark,
then rejects a result over that budget. The ceiling is not a measured
worst-case bound; it is the line the project has chosen not to cross.

Per-crossing cost matters because an ordinary operation may cross several
times. It can ask memory for recall, ask another component for confidence, pass
through governance and then request the work itself. The published baseline
does not report full-request hop counts or a latency distribution, so it cannot
support a claim about production tail latency.

The architectural pressure is still real. A small cost repeated throughout a
request is easier to carry than a large one, and predictable regression budgets
make accidental drift visible. That is what the benchmark establishes. It
does not establish parity with a direct Go call, because no comparative
measurement was run.

The cheap crossing does two jobs. It makes pervasive observation affordable,
and it lets the module boundary remain on paths where a person is waiting for
an answer. The rest of the design follows from not having to choose between
those two.

## The transport chose the language

The transport requirement came first and the implementation language followed
it. We wanted direct control over memory layout and buffer lifetime, with no
runtime pause inside the host's dispatch path. That led us to C. This is a
design account, not evidence that every other candidate was incapable of
meeting the requirement.

The useful consequence sits on the other side of that choice. The transport
host owns the constrained path, so module processes do not have to share its
runtime. Aimee has working C and pure-Go clients, held to the same byte-level
conformance tests. Those clients demonstrate a language-neutral protocol;
they do not prove that a client already exists for every language.

Ordinary event delivery does not use a socket. A module reads and writes its
own shared-memory queue pair, plus the shared arena where that contract permits
it. There is no per-event syscall on that path.

The descriptors get there once. At attach, the daemon checks the process
against a grant naming its principal, its uid and its executable, and hands
over the anonymous `memfd` regions with `SCM_RIGHTS`: up to three of them, one
time, and then that channel is done. Everything after is memory. Each client
maps only its own rings and cannot enumerate or map anyone else's, and the
control region is read-only.

Trusted native code co-located with the host may allocate in the shared arena.
The documentation calls that cooperative isolation and explicitly excludes
hostile code from its promise. Separately shipped processes stay off that path.
They fragment larger request and reply bodies above the negotiated inline
budget and reassemble them at the endpoints, up to the documented 16 MiB
message limit.

That leaves each module in its own process, address space, runtime and failure
domain. It maps its queue pair, not another module's rings, and sees the control
region read-only. A crash or runtime pause remains local to that process. What
the module shares with the system is the transport contract.

That separation is what makes a grant meaningful. If the process retained
other ambient routes into the system, its grant would describe only part of
its reach.

## A grant tells you what a module may reach

A grant can look like a restriction. It is a capability contract loaded at
startup.

It is a declaration: this principal, running this executable as this uid, may
serve these event kinds and no others. Read a grant and you know the module's
event surface before it runs, without reading its source or trusting its
author. The learning module's grant serves one event kind and publishes,
subscribes and requests nothing. That is the boundary of its possible
reach through the bus, fixed ahead of anything it happens to do today.

So the declaration holds still. A guarantee that can be edited while the system
runs is not a guarantee, and the whole value of the thing is that it was
settled before anything started.

Everything above it moves freely. A module
process attaches, serves, detaches, crashes and comes back, at any point, and
the host checks it against the declaration on every attach: peer uid and
executable path, every time. The population is dynamic. What the population may
reach through the bus was decided in advance and is knowable by reading a file.

This changes how extensions are analysed. The ordinary plugin bargain loads
code into the host process and gives it the host's privileges. Extensibility
and authority arrive together. That bargain becomes dangerous when a model can
choose when and how to invoke the extension.

Aimee puts the transport-facing adapter behind a grant. Anything attached
through that adapter can use the event kinds granted to the adapter and no
others. That is an upper bound on its reach through aimee, not a declaration
that the extension is safe or truthful. Any operating-system authority held by
the adapter process still has to be confined separately.

The cost side of that bargain has its own article on this blog:
[installability is not
composition](https://rakuensoftware.com/blog/stacking-isnt-composing). Three
context tools, each correct inside its own hook, produce a combined bill no one
of them can predict, because no add-on owns the order they run in. Authority is
the same problem read for safety instead of for cost, and it has the same
answer: somebody has to own the sequence.

No attacker is required. The model that took an unused node to finish its job
shows the problem. An extension with ambient authority can be the shortest path to
a task, and a system improving at finding short paths may use it for exactly
that reason. Reviewing what gets installed remains necessary, but it is not an
authority boundary.

So the constraint is that a thing which plugs in must not be able to do
anything that was not enumerated before it arrived. That is the same rule as
everywhere else in this piece, in its last place: authority comes from what you
are declared to be. Claiming it, reaching it, or being loaded into a process
that already had it does none of the work.

The grant turns reach through the transport into a property the host enforces.
Extension review still scales with the number of extensions, because permitted
code can misuse permitted capabilities. The separate grant review scales with
the smaller set of capability classes. One review asks whether the extension
behaves correctly; the other asks what its class can reach when it does not.

It is also why the set of grants stays small and settled at build time: what
deserves scrutiny is what holds still.

It is also what stands between us and the two failures nobody gets to prevent
by being careful: a zero-day in a dependency, and a supply-chain compromise of
a module we did not write.

Take the worst version. A module is compromised outright, and the code now
running under that identity is doing whatever an attacker wants. It still only
holds the event kinds its grant enumerates.

It cannot serve a kind it was not
granted, request one it was not granted, or subscribe to traffic it was not
granted, because none of that is its decision to make: the host routes, the
grant is loaded before the module existed in memory, and enforcement is on the
far side of the boundary from the compromise. It cannot map another client's
rings. Every attempt it does make crosses the transport and lands on the tape.

The same process may still have authority outside the bus, which is why this
limit belongs beside the sandbox boundary rather than standing in for it.

Through the bus, compromising a module gets the module's declared event
capabilities. The file does not change when the code does. This statement is
limited to the governed transport surface; sandboxing and process credentials
bound what the process may do elsewhere.

Be precise about what that covers. A compromised module can lie, and a
compromised memory component may return memory that is wrong because answering
is what it was granted to do. A grant bounds event kinds. It does not make a
permitted answer correct or a permitted side effect harmless.

That distinction is also why the analysis is tractable at all. Predicting what
a piece of code will *do* is a losing game, especially when the code arrives
from someone else or is rewritten by something that is not a person. Reading
what a piece of code may *reach* is a finite question with a written answer.
Grants can be analysed statically, at the level of the code, which means the
security work is inspection.

The cost is that the class of reach has to be anticipated. The thing that uses
it can arrive later, while a capability nobody enumerated remains unavailable
until a build-time change. I would rather inspect declared reach than discover
it after execution.

So governed inter-module decisions cross the one transport. Each daemon has one
host and one full-stream tap, which provides one place to order, observe, meter
and audit that work. The host writes an ordered capture as it goes, and that
capture preserves the accepted stream for replay. This is what lets capture,
audit and replay
[share one accepted order without becoming one
subsystem](https://rakuensoftware.com/blog/stacking-isnt-composing).

## Governed work cannot bypass the crossing

The model-facing paths and supervised modules use the bus to reach memory,
tools and other governed components. Crossing is where the host permits or
refuses an event and where the tap observes it.

The scope matters. Core-local calls inside one process do not cross the bus,
and neither does arbitrary external network traffic. The claim is complete
coverage of governed traffic that uses the bus, not complete observation of
everything a process or machine can do. Delegate containment, described next,
closes a different boundary with operating-system isolation.

So governance can be a guarantee. A rule with one enforcement point can be
enforced. A rule with an unknown number of ways around it is advice.

The decisions moved to the ends to make this useful. The learning router asks
the supervised learning process for its sink mask before persisting a signal or
queuing a proposal, and a missing or invalid response aborts ingestion. Memory
confidence and governance policy follow the same fail-closed pattern. The
caller does not substitute a permissive local answer when the named provider is
unavailable.

Execution runs in fully isolated containers on the same terms, and that case is
worth its own section, because it is where the rule stops being enforced by the
architecture and starts being enforced by the kernel.

## A delegate gets one socket, and everything is behind it

The first article in this series opens with a model that got around its
protections, took an unused node, and spent a testing API key on inference. It
did that over the network, because the network was there.

A delegate now runs in a container created with `--network none`. The
deployment check runs `curl https://api.github.com` inside the container and
requires a no-route failure rather than an authentication failure.

What replaces it is one bind-mounted Unix socket with aimee-server on the far
end. The forge, the
web, memory, the code index, the model providers: every one of them is a tool
call on that socket. The delegate is handed a surface where each capability has a
name, a grant and a place on the tape, in exchange for an IP stack where it had
none of those.

Package installation looks like the necessary exception. It is not. The
package manager speaks ordinary HTTP proxy protocol over the Unix socket, and
aimee-server answers through the sole-egress module. One function in that
module owns IP dialing.

Policy therefore lands at one point: seven registry hosts, with a label-bounded
wildcard where Ubuntu mirrors require it, and ports 80 and 443. The module
resolves the host, validates the result and dials the numeric address without
returning control between those steps. It strips authorization, proxy
authorization and cookie headers, then applies a deadline and byte ceiling.

The audit record names the numeric address actually dialled. The requested name
records intent; a later DNS lookup records a later answer. Recording the dialled
address says where the bytes went.

Hosted-provider tools are configured on the same principle. Built-in web tools
are removed from the allowed tool list and mediated replacements are added.
That configuration is checkable. This reporting does not include an
end-to-end test proving every hosted provider's agent process ran under
`--network none`, so the claim stops at the documented tool substitution.

Removing the network takes capabilities away. Each needed capability had to
exist on aimee's side before the network went, or the sandbox would only break
the work. A networkless container could not commit until mediated git tools
existed. The order was not optional.

There is a second half to why this was affordable, and it is the reason the
other two articles come first.

Many network requests begin as lookup questions: how a library behaves, what
was decided last time, what an error means or where something is configured.
Those can often be answered from memory and the local code index.

That is the demand-side argument for the sandbox: reduce the need for egress
before restricting its supply. We have not measured proxied requests per
session over time, so this remains an architectural hypothesis. If recall is
thin or wrong and network demand stays flat, the argument fails.

A genuinely needed reach can still be paid once. What comes back can be
extracted, classed, dated and stored by the machinery in the second article, so
a later session may answer locally. That is the first article's learning loop
pointed at containment: remember what egress taught, then need less egress.

Verification makes this more than a container flag. Before start or resume is
handed over, the sandbox checks the running container's network mode, the exact
source, target and read-write state of every mount, and an effective
environment with no credentials and exactly one writable control socket. A
failed or unknown observation destroys and refuses the container.

The outer boundary therefore uses the same shape as the internal one. A client
reaches a named capability through a controlled channel, and the crossing
leaves a record. The transport enforces the internal boundary; the kernel and
post-start inspection enforce the delegate boundary.

## The defaults are boring on purpose, and the leash is long

This is the promise from the opening. Aimee exposes settings for confidence,
promotion, expiry, scope, recall weights, container policy and model choice.
The shipped defaults are conservative because they have to work without an
operator studying every knob.

The two in the morning test from the top of the article is the same thing
stated as an engineering property. The misbehaviour has a name, the operational
answer is already written down, and nobody is deriving it from first principles
while half awake.

Configuration changes behaviour inside the boundary. It does not rewrite the
grant loaded at startup or move the tap behind routing. Re-tuning the memory
lifecycle changes what the system believes and how quickly it believes it. It
does not grant a component new event kinds.

So the defaults are conservative because we are the people they wake up, and
the surface is wide because that is a different question from whether our
defaults suit you. What is not configurable at runtime is the part that decides
what anything can reach, and that is the only part that has to hold still.

## A chokepoint concentrates risk

Route governed traffic through one component and that component becomes both an
enforcement point and a valuable target. The design keeps its job narrow for
that reason, but narrow is not the same as safe.

At the heart of it, the host communicates between modules and between aimee
instances. It stamps envelopes, routes by grant and identity, handles mTLS
between instances and carries bearer-token authorization. A list is more useful
than calling the host small, because each item can be inspected.

Note what is not on it. PAM and OIDC are not the bus's job. Dedicated modules
own those, and the bus carries what they decide the same way it carries
anything else. That is the pattern: the transport does not interpret payloads,
decide policy, or run anything on anyone's behalf, so even authentication is
answered somewhere with a name and a grant.

So a bearer token establishes an identity on the bus. The grant enumerates the
event kinds that identity may use, and the tap sees the accepted stream.

## Validation runs in both directions

A downstream module can check that the upstream module or server is behaving as
expected, with no obligation to accept whatever arrives because of where it
came from.

An OIDC server signs off that a caller is authenticated. The downstream module
does not have to take that on faith because it arrived stamped: it can go back
to that OIDC server and verify the authentication is valid. The claim and the
authority for the claim are separable, and a module is allowed to ask.

That reduces positional trust. Capturing something upstream does not by itself
make a downstream component accept every claim it sends. The downstream check
is another boundary an attacker may have to cross.

The stronger claim in this argument has not been established. There is no
penetration test, formal proof or independent security audit showing that the
host is not worth attacking. A compromised host could misroute, suppress or
forge traffic unless another mechanism detects the result. The grant model,
downstream validation and independent evidence records limit some consequences;
they do not make compromise harmless.

The narrow host also carries a cost. It cannot decide whether a permitted
request is reasonable. Judgement lives in the component that answers, under
its grant, and callers fail closed when that answer does not arrive. The host
stays inspectable by keeping policy and payload interpretation at the ends.

## Two numbers hold the rest of it up

The durability test emits **5,000 governed-action audit intents** and requires
exactly 5,000 ledger rows after graceful shutdown, with no duplicates or drops.
That establishes the tested audit path and its drain behaviour. It does not
prove that every possible action in every process produces such an intent.

Event kinds are carved from a module's permanent reference number, and a retired
reference is never reissued, so a grant or a capture naming one can never
quietly come to mean a different module later.

## Routed traffic reaches the tap before its destination

The tap's position determines the coverage.

The host drains each client's outbound ring, stamps a monotonic sequence number
and offers the event to the tap before making its routing decision. Delivery
and sampling happen later.

That ordering matters. A client cannot route an event to another module through
the host and then ask to omit the record. The tap is the host's job, not the
actor's, so compromising a client does not also give that client control over
how its bus traffic is recorded.

This differs from ordinary logging. Normally the component
doing a thing also writes the record of having done it, which means
compromising the component compromises the record, and the first thing anything
hostile does is stop narrating. Here the record is not the actor's job and
never passes through the actor's hands. The host writes it, upstream, whether
the actor cooperates or not, and a component has no way to be excused from it.

Failures stay in that order. An event blocked by a full destination is stamped
and tapped once, then retried without producing a duplicate tap record. Shedding
under pressure emits a typed overflow record naming the sequence and kind that
was lost. Work retained for a dead producer becomes a `producer_reaped` record
for the tap, and exhaustion of the control reserve sets a sticky
`control_lost` flag.

The rule is to name loss instead of hiding it.

Metrics and logging consume that tap, and operators can send the record
off-host. A compromised client cannot edit a record already exported by the
host. A compromised host remains a different case, which is why the durable
evidence path exists.

## Cutting the tap buys a timestamp

Suppose something does get far enough to sever the tap. That is the case the
design is most interesting in, and it is where a second mechanism takes over.

`aimee-kb` holds a hash-chained, write-once-read-many evidence ledger and is
the system of record. A memory changeset and its witness commit in one
transaction, so a failed witness aborts the source mutation. The current
validation covers the C close path and all five SQL-owned close paths, including
crash recovery and idempotent worker restart.

Signed checkpoints bind the shard heads under an Ed25519 root. An edited row,
regressed sequence or corrupt signature leaves a local inconsistency that
verification can detect. A coherent rewrite of local rows, heads and signing
material cannot be detected from that same rewritten machine. Detection then
depends on comparison with a copy retained elsewhere.

With an off-host consumer, severing the tap produces a boundary in the retained
record. Later activity may be unverifiable rather than silently accepted as
ordinary history. No recovery test in this reporting establishes what can be
reconstructed from deleted local media, so the claim stops at retained and
verifiable copies.

Detection of a coherent rewrite rests on retained off-host copies. With one
consumer, coverage is whatever that consumer kept. With several, a gap no
consumer covered remains a gap. Retention belongs to the operator, and
`aimee-kb` cannot distinguish no consumer configured from a consumer that is
down.

The witness chain and the bus capture remain separate mechanisms. The chain
makes evidence tamper-evident. The tap preserves the accepted event order.

## Two services, so that one can check the other

Aimee splits this architecture across two services. `aimee-kb` is the control
plane: it holds memory, the graph, gates, policy and the evidence chain.
`aimee-server` is the execution side, attached to one user's work and one
user's machine. One control plane can stand behind many per-user servers.

This is a familiar control-plane split, but the consequences matter here. The
services have separate processes, identities, hosts and grant sets. Each
produces records that can be compared with the other. A single compromise does
not automatically rewrite both accounts.

Both sides may also export logs and metrics to operator-controlled consumers.
Those copies add independent observations, but only where retention exists. A
consumer that kept nothing over the incident window contributes nothing to
detection.

The execution side asks the control plane for recall, writes, learning-ledger
operations and gate decisions. If that relationship stops, the server loses
those capabilities rather than replacing them locally. This limits how useful
an isolated execution-side compromise can remain, although the compromised
host and user data are still a serious blast radius.

The control plane is not inert. It authenticates, answers OIDC, makes
authorization decisions, curates and synthesises, and can return false data if
compromised. The current service contract is request and reply: the control
plane answers server requests and has no channel for initiating a server
command. That is narrower than saying it cannot execute or cannot cause harm.

Operators can widen either side. A grant mechanism cannot protect a deployment
from an operator who deliberately grants broad authority or installs code with
ambient host credentials. What it can do is make transport reach explicit in a
file loaded before the process attaches. A grant is an inspectable ceiling, not
a substitute for reviewing the code beneath it.

The split has an engineering cost. Four pieces of the self-learning work once
landed on the side that could not reach their data. The [first
article](https://rakuensoftware.com/blog/aimee-recursive-self-learning)
describes that failure and the build-graph check added after it. The same
boundary that separates activity from its record can strand code on the wrong
side.

That brings the story back to its opening. The transport does not make an AI
system safe by itself. It makes ordinary controls cheap enough to apply to
governed inter-module work: explicit identity, bounded event kinds, ordered
observation, failure records and independent evidence. Delegate isolation
extends the pattern to execution with a different enforcement boundary.

The result is narrower than the original slogan and more useful. What crosses
the bus can be ordered, checked against grants and offered to the tap before
routing. Core-local work, external traffic and a compromised host require their
own controls. Naming that boundary is what makes the coverage auditable rather
than aspirational.
