---
title: "Everything Crosses One Transport"
slug: everything-crosses-one-transport
date: 2026-08-24
author: Rakuen Software
tags: [aimee, architecture, isolation, governance, event-bus]
excerpt: "A cheap, language-neutral transport gives ordinary engineering controls one place to hold: declared reach, ordered observation, durable evidence and a boundary around every governed action."
---

*Rakuen builds aimee, the system written about here. Third of three: the
[self-learning loops](https://rakuensoftware.com/blog/aimee-recursive-self-learning)
come first and the memory second. This one is the architecture both of those
stand on. Figures are traced in the [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/everything-crosses-one-transport/evidence/figures.md).*

The goal is an AI system that is auditable, governable, and will not wake an
engineer at two in the morning.

The last clause is the acceptance test. Audit tells the person on call what
happened. Governance bounds what could have happened. With both answers already
written down, the call ends quickly or never starts.

The user should see even less: a short setup, then silence. Metrics exist for
the person who wants them. The system works for the person who does not.

That goal produces a wide configuration surface over conservative defaults.
The defaults serve people who change nothing. The settings leave room for an
operation unlike ours. The boundary around both has to survive every setting.

A language model is a component we cannot fully predict. Software engineering
already has a discipline for that: limit its authority, mediate its access and
record what it does. Access control, capability grants and separated control
planes are old work.

Cost kept that work off the hot path. An observable, policy-enforced crossing
that takes too long will acquire exceptions. Each exception turns a guarantee
into a list of places somebody remembered to instrument.

That failure usually arrives by degrees. One component calls another directly
because the common path is too slow. A second keeps its own log because the
first observer lacks a field it needs. A third performs a local permission
check because the policy service is inconvenient from its runtime.

Every choice
can be reasonable in isolation, while the system-wide claim disappears between
them.

One transport changes where those decisions live. A component declares its
reach once, the host orders the accepted traffic once, and observers consume
that order without asking each actor to cooperate. The common route has to be
cheap enough that the direct call never becomes the sensible engineering
choice.

Aimee calls its crossing an event bus. Broker-mediated message router is more
exact. It carries point-to-point request and reply, typed capability errors,
cancellation and bounded backpressure over shared-memory rings. Large payloads
move by shared-arena lease.

Every client owns a private queue pair mapped into its address space. The host
moves frames between those pairs, gives them one order and routes them under
credit-based flow control. Clients cannot map one another's rings.

The parts have known lineages. LMAX, virtio, `io_uring` and DPDK all belong to
the ring-buffer family. Aeron's media driver is the closest whole-system
comparison I know. Grants come from the capability-microkernel line represented
by seL4.

Aimee combines those lines with a mandatory full-stream tap ahead of routing
and one required path for governed inter-module traffic. I have not found the
same combination elsewhere. That statement covers what I have seen and worked
with; it is not a field survey.

The combination is the part I would call novel. The safety ideas are ordinary.
The self-learning loops and memory lifecycle in the first two articles use old
techniques too. A cheap crossing makes those techniques affordable everywhere
they need to hold.

The audit record, grants, isolation, language-neutral module boundary and safe
learning loops all depend on that price.

## The price of crossing stopped being an excuse

The committed baseline reports a **134 ns median** for dispatching a 16-byte
inline event from a producer ring to a subscriber ring on the reference host.
Enqueuing a governed-action audit intent reports a **117 ns controlled median**:
the median of eight per-run medians, with each run timing 5,000 emits while
pinned to one CPU. Those are observations, not maximums.

`bench/bus_baseline.json` sets a **1,000 ns regression ceiling** for both
dispatch and audit enqueue. The merge gate rebuilds and runs each benchmark,
then rejects a result over that budget. The ceiling is not a measured
worst-case bound; it is the line the project has chosen not to cross.

The comparison matters more than the number. A C host reaching into a Go
module already pays for a cgo crossing. On the same i7-14700K used for the audit
reference, Go 1.24.4's own `BenchmarkCgoCall` put simple crossings between
roughly 38 and 102 ns. An eight-pointer call took between 147 and 164 ns.

The bus's 134 ns dispatch belongs to that cost class.

That gives the architecture a useful trade. We spend about what one
language-specific boundary would have cost and receive a boundary with no
language on the far side. The C host can route to Go today and to another
protocol client later. Neither endpoint needs a binding to the implementation
language at the other end.

Per-crossing cost stacks. An ordinary operation may ask memory for recall,
another component for confidence, governance for permission, and then a module
for the work itself. Each module can cross again. One tolerable delay becomes a
problem when a request takes the chance repeatedly.

The transports I examined were quick on a good run. Their bad runs arrived
through the usual routes: a collector, a slow syscall, lock contention,
allocation, a page fault or the scheduler. A long tail crossed once is an
outlier. Cross it throughout a request and the system feels unpredictable.

The 1,000 ns figure is a regression budget. It gives the project a line to
defend while leaving room for machine and scheduler variance. The observed
medians show where the implementation runs today.

The cheap crossing does two jobs. It makes pervasive observation affordable,
and it lets the module boundary remain on paths where a person is waiting for
an answer. The rest of the design follows from not having to choose between
those two.

## The transport chose the language

The transport requirement came first and the implementation language followed
it. We wanted direct control over memory layout and buffer lifetime inside the
host's dispatch path. I narrowed the choice to C and Rust, then chose C.

The choice also kept the host free of a managed runtime. Garbage collection is
useful in the processes where most of aimee's work happens. In the component
that orders every governed crossing, a runtime pause would become everybody's
pause. Allocation and lifetime belong in the design there, not behind a
collector whose schedule the host cannot control.

The constraint ends at the transport. Module processes can use their own
runtimes because the host owns the path with the budget. Aimee has working C
and pure-Go clients held to the same byte-level conformance tests.

The Go client contains no cgo. It maps memory and speaks the protocol.

Neither endpoint needs to know the implementation language at the other end.
A client in another language would implement the same bytes and queue rules.
No existing endpoint would need a binding to it.

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

Each module keeps its own process, address space, runtime and failure domain. It
maps its queue pair and sees the control region read-only. A crash or runtime
pause stays in that process. The transport contract is all it shares with the
system.

That makes language choice local again. A module can choose a runtime for its
libraries, its deployment and the people maintaining it. A collector pause or
process crash affects that module instead of moving into the router. New client
implementations have one protocol and one conformance suite to satisfy; the
existing modules remain untouched.

That separation is what makes a grant meaningful. If the process retained
other ambient routes into the system, its grant would describe only part of
its reach.

## Grants turn reach into a written contract

A grant names a principal, executable and uid, then lists the event kinds it may
serve, publish, request and subscribe to. The learning module serves one kind
and has empty lists for the other three. Its reach through the bus is readable
before the process starts.

The host loads grants at startup and checks the peer uid and executable on every
attach. Processes may arrive, crash and return. Their declared reach holds
still.

Extensions make the value easier to see. The usual plugin loads inside a host
and inherits the host's authority. Once a model chooses when to invoke it,
extensibility and ambient authority have become the same surface.

Aimee puts the transport-facing adapter behind a grant. Code attached through
that adapter gets the adapter's event kinds. The adapter's operating-system
credentials remain a separate boundary for the sandbox to handle.

The distinction matters even with honest code. The model from the opening used
an available route because it was the shortest path to its task. A learning
system will keep finding useful routes. Installation review cannot tell the
host what a route may reach at runtime; the grant can.

Two reviews remain. Extension review asks whether a particular piece of code
behaves correctly with the capabilities it has. Grant review asks what the
whole class can reach when one member misbehaves. The second review scales with
the smaller set of grants and survives a later extension arriving under the
same contract.

Now take the hostile case. A compromised module keeps the event kinds in its
grant. The host still routes, and the module still maps only its own queues. A
zero-day or supply-chain compromise changes the code without changing the file
that bounds its bus access.

Permitted capability can still do damage. A compromised memory component can
return a lie because answering memory requests is its job. A process may also
hold host authority outside the bus. Grants bound the governed event surface;
process credentials and sandboxing cover the rest.

Predicting every action of changing code is a losing game. Declared reach is a
finite list. The cost is equally concrete: a new class of reach waits for a
build-time grant change. I would rather inspect that change than discover the
capability after execution.

Each daemon then has one host and one full-stream tap for governed inter-module
work. The host orders, meters and records the accepted stream for replay. This
lets capture, audit and replay
[share one accepted order without becoming one
subsystem](https://rakuensoftware.com/blog/stacking-isnt-composing).

Event kinds derive from a module's permanent reference number. A retired
reference is never reused, so an old grant or capture cannot acquire a new
meaning later.

The resulting promise is deliberately narrow: governed work is visible through
the tap or permitted by a grant, and usually both. It does not promise that a
permitted action is wise or that code with separate host credentials is safe.
It gives an operator a complete place to inspect the authority aimee itself
provides.

## Governed inter-module work crosses here

The model-facing paths and supervised modules use the bus to reach memory,
tools and other governed components. Crossing is where the host permits or
refuses an event and where the tap observes it.

A recall request shows the whole shape. The caller may ask a confidence service
which evidence is admissible, send the resulting query to memory and receive a
bounded envelope. Each step uses a named event kind. An unavailable confidence
answer aborts the path instead of becoming a permissive local default, and the
tap sees the accepted sequence even when the final destination refuses it.

Adding another decision therefore adds another declared participant rather
than another invisible integration. The transport carries the question and its
answer while the provider remains the authority. Policy can evolve at the edge
without teaching the host how to interpret memory, identity or model output.

The coverage is governed traffic carried by the bus. Core-local calls and
arbitrary external network traffic sit outside it. Delegate containment closes
the network boundary with the kernel and a mediated socket.

So governance can be a guarantee. A rule with one enforcement point can be
enforced. A rule with an unknown number of ways around it is advice.

Decision code moved to the ends. The learning router asks
the supervised learning process for its sink mask before persisting a signal or
queuing a proposal, and a missing or invalid response aborts ingestion. Memory
confidence and governance policy follow the same fail-closed pattern. The
caller has no permissive local answer to substitute when the named provider is
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

Package installation is the hard case. The package manager speaks ordinary
HTTP proxy protocol over the Unix socket, and aimee-server answers through the
sole-egress module. One function in that module owns IP dialing.

The package manager needs no private integration. It sees a proxy and behaves
as package managers already do. The unusual part stays behind the socket, where
the proxy request becomes a named capability and the sole-egress module decides
whether it may leave the host.

Policy therefore lands at one point: seven registry hosts, with a label-bounded
wildcard where Ubuntu mirrors require it, and ports 80 and 443. The module
resolves the host, validates the result and dials the numeric address without
returning control between those steps. It strips authorization, proxy
authorization and cookie headers, then applies a deadline and byte ceiling.

The allowlist, resolver and dialer are package-private. A caller inside the
module cannot supply a friendly resolver for the check and a different address
for the connection. The validation result and the dial target remain one
decision.

The audit record names the numeric address actually dialled. The requested name
records intent; a later DNS lookup records a later answer. Recording the dialled
address says where the bytes went.

Hosted-provider tools use the same shape. Their built-in web tools leave the
allowed list and mediated replacements take their place. The checked artifact
here is that tool configuration; the reporting record has no end-to-end run
covering every hosted provider under `--network none`.

The model keeps the capability to search or read the web. It loses the private
route. A request acquires a name, passes through policy and joins the same
record as local tool use.

The distinction matters because containment that merely removes useful work
will eventually be disabled. Mediation preserves the work while narrowing the
route that performs it.

Removing the network takes capabilities away. Each needed capability had to
exist on aimee's side before the network went, or the sandbox would only break
the work. A networkless container could not commit until mediated git tools
existed. The order was not optional.

There is a second half to why this was affordable, and it is the reason the
other two articles come first.

Many network requests begin as lookup questions: how a library behaves, what
was decided last time, what an error means or where something is configured.
Memory and the local code index can answer those before they become HTTP.

Egress demand has to fall before egress supply can be cut. A sandbox around an
agent that constantly needs the network is a standing argument with the work,
and the work deserves to win. Good recall makes the remaining reaches narrow
enough to name. We have not yet measured whether proxied requests decline over
successive sessions, so that decay remains a design claim.

A genuinely needed reach can still be paid once. What comes back can be
extracted, classed, dated and stored by the machinery in the second article, so
a later session may answer locally. Remember what egress taught, then need less
egress. The first article's learning loop now points at containment.

Verification makes this more than a container flag. Before start or resume is
handed over, the sandbox checks the running container's network mode, the exact
source, target and read-write state of every mount, and an effective
environment with no credentials and exactly one writable control socket. A
failed or unknown observation destroys and refuses the container.

The check reads the running container, not the launch request. Configuration
describes what an operator hoped to create. Inspection answers what the process
actually received after runtime defaults, mounts and environment assembly took
effect. Resume receives the same scrutiny as first start because a stopped
container is still a container whose effective state may have drifted.

The outer boundary therefore uses the same shape as the internal one. A client
reaches a named capability through a controlled channel, and the crossing
leaves a record. The transport enforces the internal boundary; the kernel and
post-start inspection enforce the delegate boundary.

This posture ships enabled. `delegate_sandbox: false` is the operator's one
host-level opt-out. The Go ownership, post-start verification and proxy policy
arrived in [pull request
2839](https://github.com/RakuenSoftware/aimee/pull/2839). The point of naming the
switch is operational: a deployment that changes the boundary can be found in
configuration instead of inferred from a model's behaviour.

## The defaults are boring on purpose, and the leash is long

Aimee exposes settings for confidence, promotion, expiry, scope, recall
weights, container policy and model choice. The shipped defaults are
conservative because they have to work without an operator studying every
knob.

That surface is deliberately wide. Memory suitable for one team can be noisy
for another. Promotion clocks, evidence requirements and recall weights should
move with the work.

Model choice and container policy carry equally local tradeoffs. Freezing those
choices into the architecture would turn an operating opinion into a permanent
constraint.

The two in the morning test from the top of the article is the same thing
stated as an engineering property. The misbehaviour has a name, the operational
answer is already written down, and nobody is deriving it from first principles
while half awake.

Configuration changes behaviour inside the boundary. Re-tuning the memory
lifecycle changes what the system believes and how quickly it believes it.
Grants and tap ordering hold while those settings move.

The separation is the reason customisation does not erase the guarantee. A
setting can make recall permissive or cautious. It cannot add an event kind to a
process, move observation after delivery or give a delegate an IP route. Those
changes belong to grants and deployment, where they are explicit and
reviewable.

We choose conservative defaults because we are the people they wake up. The
surface stays wide because somebody else's operation may justify another
choice. Runtime configuration stops at the declaration of what each component
may reach.

## The chokepoint stays narrow, and validation runs both ways

Route governed traffic through one component and it becomes a valuable target.
The host stays narrow for that reason. It stamps envelopes, routes by grant and
identity, handles mTLS between instances and carries bearer-token
authorization. Each item in that list can be inspected.

Authentication policy lives elsewhere. Dedicated modules own PAM and OIDC, and
the transport carries their decisions. It does not interpret payloads or make
policy. A bearer token establishes an identity on the bus; the grant says which
event kinds that identity may use.

Downstream modules may check an upstream claim with the authority that issued
it. An OIDC decision can be verified with the OIDC service before another
module acts on it. Position in the route does not make a claim true.

Consider the isolation module, the component an attacker would want to turn
against the boundary. Its bus grant serves four request kinds and gives it no
publish, subscribe or request surface. Capturing that process permits forged
answers to those four questions. It does not permit the process to invent a
fifth event kind or direct the host to a new destination.

The operating-system side still matters. A process with a socket, credentials
or a writable host mount can act outside its bus grant, which is why the grant
claim is limited to governed traffic. Process isolation removes those ambient
routes. Inside the transport, capture yields one participant's declared reach,
not the router's table.

A host compromise remains serious. The host can misroute, suppress or forge
traffic until another mechanism catches the disagreement. Grants, downstream
checks and independent records raise the cost and limit some consequences.
They do not turn the chokepoint into a harmless target.

Keeping policy at the ends creates its own rule: the host cannot decide whether
a permitted request is sensible. The module holding that decision answers
under its grant, and the caller fails closed when no answer arrives. The host
remains small because it stays out of the interesting decisions.

## Routed traffic reaches the tap before its destination

The tap's position determines the coverage.

The host drains each client's outbound ring, stamps a monotonic sequence number
and offers the event to the tap before making its routing decision. Delivery
and sampling happen later.

The durability test sends **5,000 governed-action audit intents** through that
path and requires 5,000 ledger rows after shutdown, with no duplicate or drop.
It tests the audit path and its drain behaviour.

The order keeps recording out of the client's hands. A client cannot route an
event through the host and then ask to omit it. Compromising the client leaves
the host's tap in place.

Every effect on another governed module begins with an accepted event. The tap
sits between acceptance and routing, so an actor has no sequence in which it
first changes another module and later decides whether to narrate the change.
Observation is part of the route, not a courtesy performed after it.

The timing of observation changes the kind of account the system can keep. If
logging happens after delivery, a crash between action and log creates an
ordinary-looking gap. Here the accepted event has a sequence before the route
can succeed or fail. The later record can say delivered, blocked, shed or left
behind by a dead producer while referring to the same accepted order.

Ordinary logging gives the actor responsibility for narrating its own work. A
compromised actor stops. Here the record never passes through the actor's
hands. The host writes it upstream whether the client cooperates or stays
silent.

Failures stay in that order. An event blocked by a full destination is stamped
and tapped once, then retried without producing a duplicate tap record. Shedding
under pressure emits a typed overflow record naming the sequence and kind that
was lost. Work retained for a dead producer becomes a `producer_reaped` record
for the tap, and exhaustion of the control reserve sets a sticky
`control_lost` flag.

Loss gets a name.

Metrics and logging consume that tap, and operators can send the record
off-host. A compromised client cannot edit a record already exported by the
host. A compromised host remains a different case, which is why the durable
evidence path exists.

Metrics provide another projection of the stream. Counts, rates, timing and
volume give an incident another set of facts to reconcile alongside the event
record. Removing an event from a later story may leave a counter
or timing envelope that still reflects it. Their value depends on where the
operator exports them and how long that consumer retains them.

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

The useful result is a timestamp, not an assertion of invulnerability. The
retained copy says where continuous observation ended. Operations after that
point enter an incident as unverified activity instead of inheriting the trust
of the earlier chain. A responder can quarantine the interval without claiming
to reconstruct events that were never retained.

Detection of a coherent rewrite rests on retained off-host copies. With one
consumer, coverage is whatever that consumer kept. With several, a gap no
consumer covered remains a gap. Retention belongs to the operator, and
`aimee-kb` cannot distinguish no consumer configured from a consumer that is
down.

Detection coverage follows the retained overlap. The attacker's burden runs in
the other direction: every consumer holding any original event or derived
metric creates another fact a coherent rewrite must match. One disagreement is
enough to expose the rewrite. More consumers increase that burden only when
they are independently placed and actually retain data.

The witness chain and the bus capture remain separate mechanisms. The chain
makes evidence tamper-evident. The tap preserves the accepted event order.

## Two services, so that one can check the other

Aimee splits the architecture across two services. `aimee-kb` is the control
plane. It holds memory, the graph, gates, policy and the evidence chain.

One control plane can stand behind many users. Each user has an `aimee-server`
attached to their work and their machine.

The asymmetry matters. The server can act and holds little of the system's
learned state. The control plane holds the learned state and has no channel for
starting a command on a server. It answers requests.

Each side has its own process, identity, host and grant set. Each also writes a
record the other can be checked against. Compromising one side leaves another
account to reconcile, plus any copies already exported to operator-controlled
consumers. Retention decides how useful those outside copies are.

The separation raises the cost of inventing a coherent history. A rewritten
server record must agree with the control plane's memory changes, gate answers
and evidence. Both stories must also agree with records and aggregates that
left either host before the compromise.

The design cannot promise that every operator retains every projection. It can
ensure that the two halves do not begin with one shared, editable account.

The server keeps asking the control plane for recall, memory writes,
learning-ledger operations and gate decisions. Cut that relationship and the
server falls back to the provider checkpoint and whatever context the current
run still holds. The task history, learned facts, failed approaches, policy
evidence and later corrections remain on the other side of the boundary.

Keeping the connection does not solve the attacker's problem either. Continued
work continues to ask a service the attacker does not control, and those
requests keep adding to its record. Silence avoids that record by giving up the
memory and decisions that made the running system useful.

That does not make a compromised server harmless. It still owns one user's
host and work. It does make the compromise a poor substitute for the agent that
was there before: the part that acts has lost the accumulated learning that
made later runs better than a stock model trained on older data.

The control plane has the opposite problem. It authenticates, makes
authorization decisions, curates and synthesises. A compromise there can lie
about memory and policy.

Plugins installed there also run there, with whatever host authority the
operator gave them. The transport grant records their reach through aimee; it
cannot rescue an operator who deliberately grants the host.

That is real capability. Bad memory can mislead every server that recalls it,
and a bad authorization decision can approve work that should have stopped.
The split limits how that capability becomes action: the compromised service
still needs a server to ask a question before it can answer dishonestly.

An installed plugin deserves the same precision. A plugin runs where the
operator installed it and inherits whatever host authority that environment
provides. Its grant makes transport reach visible and finite. The architecture
cannot bound authority an operator deliberately supplies outside that
transport.

What the control plane lacks is initiation. The service contract is request and
reply. A server asks over the transport and the control plane answers.

There is no control-plane client for a server command and no channel for
starting a conversation in the other direction. The heaviest credential the
design needs there is a read-only repository key.

Neither half is the whole agent. One can act and forgets. The other remembers
and cannot start the action. Taking the system requires both sides, their two
records, and the outside copies to agree.

This asymmetry arrived for operational reasons as much as security. One shared
control plane can hold durable knowledge for many users while each server stays
close to one user's work and machine. The resulting blast radii differ.

A server compromise reaches that host and user. A control-plane compromise
reaches shared learned state and policy, but lacks a channel for initiating
work on those hosts.

The split charges an engineering price. Four pieces of the self-learning work
once landed on the side that could not reach their data. The [first
article](https://rakuensoftware.com/blog/aimee-recursive-self-learning)
describes that failure and the build-graph check added after it. A boundary
strong enough to separate activity from its record is strong enough to strand
code on the wrong side.

The transport makes the older controls in this article affordable on every
governed crossing: identity, declared reach, ordered observation and an
independent record. The kernel supplies the outer boundary for delegated
execution. Core-local work, external traffic and a compromised host still need
their own controls.

One transport gives the ordinary safety controls somewhere to hold.
