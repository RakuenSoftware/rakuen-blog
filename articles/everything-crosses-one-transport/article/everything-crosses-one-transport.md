---
title: "Everything Crosses One Transport"
slug: everything-crosses-one-transport
date: 2026-08-24
author: Rakuen Software
tags: [aimee, architecture, isolation, governance, event-bus]
excerpt: "A language model does not need a new safety discipline invented for it. It needs to be made subject to the ones we have had for decades. The only thing standing in the way was the cost of applying them everywhere, and that is what one transport at a bounded 134 ns buys back."
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

We know how to do access control. We know how to do observability. We know how
to do audit logging, and capability grants, and separating a control plane from
the things it controls. None of that is research. It is decades of ordinary
engineering, most of it settled before anyone reading this started working, and
all of it built for exactly this situation: a component you cannot fully
predict, which must therefore be bounded by what it can reach and be visible in
what it does.

The mistake I see repeatedly is treating a model as a special case that needs
its own safety theory. It is a component. Put it inside the patterns, deny it
ambient authority, record what it does, and the problem becomes one you can
staff with the engineers you already have.

There was one reason that could not be done cheaply before, and the rest of
this article is about it.

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

What it is, described honestly, is a broker-mediated message router whose
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

So the lineage is clear enough. Transport shape from the ring-buffer line,
admission from the capability line, plus a mandatory full-stream tap ahead of
routing and a rule that everything in the system crosses it. I have not found
the four together, and I say that as someone who has not surveyed the field, so
it describes what I have seen and worked with. One counterexample settles it
and I would like to see one.

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
safety. What it removes is the cost that stopped people using the ideas they
already had.

The audit record, the grants, the isolation, the module boundary that admits
any language, the loops being safe enough to leave running: every one of those
is downstream of one transport being cheap enough that everything could be made
to cross it. Take the bound away and you are back to choosing which paths get
observed, and once you are choosing, none of the guarantees in these three
articles can be stated as guarantees.

## Crossing it costs about what calling into Go costs anyway

Per-event dispatch, from a producer writing its outbound ring through a
subscriber reading its inbound ring, is bounded to a **134 ns** maximum on the
reference box with a 16-byte inline payload. Publishing a governed-action audit
row costs the caller **82 ns**. Both sit under committed ceilings in
`bench/bus_baseline.json`, 2,000 ns and 5,000 ns, and a merge gate builds and
runs the benchmark and fails the merge if the measured number goes over. The
budget is a real checkable number.

The comparison matters more than the number. Once you count what a cgo call
actually costs, sending the same work over the bus is about as fast as calling
straight into the Go code would have been. Observability arrives at roughly
what you were going to pay anyway.

And the per-crossing figure is not where the pressure is. **It stacks.** One
ordinary request does not cross the transport once. It crosses it to reach
memory, again for the recall gate, again for the confidence band, again for
governance, again for whatever the answer turns out to need, and each of those
modules may cross it again to do its own work. The cost that matters is per-hop
multiplied by however many hops an operation actually takes, and that
multiplier is not small.

Run that arithmetic against a conventional transport and the design stops
working. A traditional event bus, or ordinary IPC between processes, is not
disqualified because it is inelegant. It is disqualified because a per-hop cost
in microseconds, times the hops one request takes, produces a system that
cannot answer coherently. The individual hop looks fine in a benchmark. The sum
is what you have to live in.

And the median is not the number that kills you. Every candidate I looked at
was fast on a good day. What none of them would promise was a bad one. They had
tails, some of them long, from the usual places: a collector deciding
now is the time, a syscall that took the slow path, lock contention, an
allocator growing something, a page fault, the scheduler having other ideas.

A tail you cross once is an outlier you can live with. A tail you cross fifteen
times an operation is not, because the chance of catching at least one goes up
with every hop, and one is all it takes. Multiply a rare stall by a system that
touches the transport constantly and the rare stall stops being rare from the
user's point of view. It becomes the reason the thing feels unpredictable,
which is worse than being slow, because you cannot design around it.

So the budget in `bench/bus_baseline.json` is written as a ceiling, and a merge
gate fails the build over it. The committed number is the promise about the
worst case. The observed number is just evidence that the promise is currently
being kept. For a transport everything crosses, those are the right way round,
and getting them the wrong way round is how you end up with a system that
benchmarks beautifully and stutters in production.

So the bound is doing two jobs at once. It is why nothing had to be exempted
from being observed, which is the argument the rest of this article makes. It
is also, and more basically, why the system works at all at the speed a person
is waiting at. A traditional event bus would have made us choose between
observability and coherence, and there would not have been a good answer.

## The transport chose the language

The bound above is the reason the architecture is written in what it is written
in, and that order matters: the transport requirement came first and the
language followed it.

What we needed was the guarantee described above, and it is the same
requirement one layer down. Go could not give us one. Neither could the other
candidates we looked at. They are fine languages and several of them are fast;
what none of them offered was a way to say *this dispatch will not exceed this
cost*, and hold it, with the memory layout and the lifetime of every buffer
under our own control. A transport everything must cross cannot have a tail
nobody owns, and a runtime that reserves the right to pause you is a tail
nobody owns.

On investigation that left two options for the whole architecture, C and Rust,
and we went with C.

The consequence is the part worth noticing. Because the guarantee lives in the
transport, the code on either side of it does not have to carry one.

**So a module can be written in any language.** That is not a roadmap item, it
is what the boundary already is.

**No event travels over a socket.** That is the whole point, and it is what the
bound above is bought with. A module reads and writes shared memory directly:
its own queue pair, mapped into its address space, plus the shared arena. There
is no send, no receive, no copy through the kernel, and no per-event syscall on
the ordinary path.

The descriptors get there once. At attach, the daemon checks the process
against a grant naming its principal, its uid and its executable, and hands
over the anonymous `memfd` regions with `SCM_RIGHTS`: up to three of them, one
time, and then that channel is done. Everything after is memory. Each client
maps only its own rings and cannot enumerate or map anyone else's, and the
control region is read-only.

A socket-based design was never on the table. A round trip through the kernel
per event does not come close to the bound above, and a transport everything
must cross cannot afford one.

None of it requires a particular runtime. Receiving a descriptor and mapping
memory is ordinary POSIX, which is why the pure-Go client needs no cgo, and why
it and the C client are held to each other by byte-for-byte conformance tests.

The design decision that makes it true is the one about payloads. Trusted code
co-located with the host may allocate in the shared arena, which is the fast
path and the one with real requirements attached. **Separately shipped module
processes deliberately do not.** They use a protocol that fragments request and
reply bodies above a negotiated inline budget and reassembles them at the
endpoints, up to a 16 MiB message limit. The arena is described in aimee's own
documentation as cooperative isolation for trusted native modules, with hostile
code outside its remit, and keeping shipped modules off it is what turns "you
must be C" into "you must speak this protocol."

Sixteen module identities happen to be served by Go processes. That is a
staffing decision. A module can have a garbage collector precisely because it
sits on the far side of a boundary that does not, and the same instinct as
everywhere else in this piece, that the transport is boring so the ends can be
interesting, turns out to apply to language choice too.

That deserves naming as its own property, because it is the strongest thing the
boundary gives you. **A module is a completely independent execution space.**
Its own process, its own address space, its own runtime, its own failure
domain. It maps its own queue pair and nothing else, so it cannot enumerate or
map another module's rings, and the control region is read-only to it. What it
does inside itself is nobody else's problem, and nobody else can see it: the
language, the dependencies, the collector, the crash. What it shares with the
rest of the system is one contract, and that contract is the one everything
else crosses on too.

Which is also what makes the next part work. If a module were only mostly
independent, its grant would be a description of some of what it does, and the
rest would be whatever it could reach by other means. There are no other means.

## A grant is how you know what a module will do

I would defend this part hardest, because it is easy to read as a restriction
when it does the opposite. A grant is a behaviour guarantee, fixed at build
time.

It is a declaration: this principal, running this executable as this uid, may
serve these event kinds and no others. Read a grant and you know what that
module can do, before it runs, without reading its source and without trusting
its author. The learning module's grant serves one event kind and publishes,
subscribes and requests nothing. That is the boundary of its possible
behaviour, fixed ahead of anything it happens to do today.

So the declaration holds still. A guarantee that can be edited while the system
runs is not a guarantee, and the whole value of the thing is that it was
settled before anything started. Everything above it moves freely. A module
process attaches, serves, detaches, crashes and comes back, at any point, and
the host checks it against the declaration on every attach: peer uid and
executable path, every time. The population is dynamic. What the population may
do was decided in advance and is knowable by reading a file.

New capability does not need new grants either. The thing that holds the grant
is the adapter, and what plugs into the adapter is open-ended. In 0.4.0 that
includes MCP servers and pluggy plugins attaching through the transport and
inheriting its guarantees: ordered delivery, correlation and cancellation,
bounded payloads, a recorded crossing, and a capability set that is enumerated
in advance. A plugin does not get to negotiate its own terms. It arrives inside
a contract that was declared before it existed.

This is where I part company with how plugin systems usually work, and it is a
constraint the design was built around.

The ordinary bargain is that a plugin loads into the host process, runs with
the host's privileges, and the honest answer to "what can this do?" is
"anything the host can do." Extensibility and authority arrive in the same
package. That is tolerable when a person installs a plugin they have read, on a
machine they control, and it stops being tolerable the moment the thing
deciding to invoke it is a model. A plugin surface with ambient authority is an
injection surface aimed at everything the host owns.

The cost side of that bargain has its own article on this blog:
[installability is not
composition](https://rakuensoftware.com/blog/stacking-isnt-composing). Three
context tools, each correct inside its own hook, produce a combined bill no one
of them can predict, because no add-on owns the order they run in. Authority is
the same problem read for safety instead of for cost, and it has the same
answer: somebody has to own the sequence.

And it does not require anyone to be attacking you. Go back to the model that
took an unused node to finish its job. A plugin that can do anything is the
shortest path to a task, and a system that gets better at finding shortest
paths will find that one. Nothing has to go wrong for it to be used, which is
exactly why "we will review what gets installed" is not a control.

So the constraint is that a thing which plugs in must not be able to do
anything that was not enumerated before it arrived. That is the same rule as
everywhere else in this piece, in its last place: authority comes from what you
are declared to be. Claiming it, reaching it, or being loaded into a process
that already had it does none of the work.

The grant is what turns that from a policy into a property, and the consequence
is a different unit of security analysis.

Normally the work scales with the number of extensions. Every plugin is its own
review, because every plugin is its own set of capabilities, and you are asking
"what does this one do?" once per plugin, forever, including for the next one
somebody installs on Tuesday. That is a treadmill, and it is the reason plugin
security in practice degrades into trusting the author.

Here the work scales with the number of grants. A grant is a generalised attack
surface: these event kinds, this identity, this executable, and nothing else.
Analyse that once and the finding covers everything that ever runs under it. A
new plugin arriving inside an existing grant needs no new analysis, because it
cannot exceed the grant, and the grant is what you already analysed. The
question stops being "what does this plugin do?" and becomes "what does this
class of thing get to do?", which is a bounded question with an enumerable
answer.

It is also why the set of grants stays small and settled at build time: what
deserves scrutiny is what holds still.

It is also what stands between us and the two failures nobody gets to prevent
by being careful: a zero-day in a dependency, and a supply-chain compromise of
a module we did not write.

Take the worst version. A module is compromised outright, and the code now
running under that identity is doing whatever an attacker wants. It still only
holds the event kinds its grant enumerates. It cannot serve a kind it was not
granted, request one it was not granted, or subscribe to traffic it was not
granted, because none of that is its decision to make: the host routes, the
grant is loaded before the module existed in memory, and enforcement is on the
far side of the boundary from the compromise. It cannot map another client's
rings. Every attempt it does make crosses the transport and lands on the tape.

Compromising a module gets you the module's capabilities and no more, which is
the whole difference. The usual outcome of a supply-chain compromise is that an
attacker inherits the host's authority because the plugin was running inside
it; here there is no authority to inherit, because it was enumerated in a file
before the attack and the file does not change when the code does.

Be precise about what that covers. A compromised module can lie, and a
compromised memory module may return memory that is wrong, because answering is
what it was granted to do. A lie is the extent of it. A wrong answer is bad; a
wrong answer plus arbitrary reach is a different category of event, and the
second one is off the table.

That distinction is also why the analysis is tractable at all. Predicting what
a piece of code will *do* is a losing game, especially when the code arrives
from someone else or is rewritten by something that is not a person. Reading
what a piece of code may *reach* is a finite question with a written answer.
Grants can be analysed statically, at the level of the code, which means the
security work is inspection.

The cost is real too, and worth stating exactly. What has to be anticipated is
the class of reach. The thing that uses it can arrive later, and a capability
nobody enumerated is unavailable until somebody enumerates it, and that is a
build-time change. I think that is the right trade, and I would rather have a
system whose behaviour is declared than one whose behaviour is discovered.

So every inter-module decision crosses the one transport. Each daemon has one
host and one full-stream tap, which means exactly one place to order, observe,
meter and audit inter-module work. The host writes an ordered capture as it
goes, and that capture preserves the accepted stream for replay, which is what
lets capture, audit and replay
[share one accepted order without becoming one
subsystem](https://rakuensoftware.com/blog/stacking-isnt-composing). Twenty-two
components run as supervised processes of their own, each authenticated
separately.

## Nothing can do anything without crossing it

**The model crosses it. Every module crosses it. So does every subsystem that
predates the design.** Anything can do what it likes inside its own local
environment. Nothing it does there reaches memory, tools, the knowledge store,
another module or the host until it crosses. Crossing is where it is permitted
or refused, and where it is written down. There is no second path, no side
channel left over from before, and no direct call that skips the transport
because it happened to be hot.

So governance can be a guarantee. A rule with one enforcement point can be
enforced. A rule with an unknown number of ways around it is advice.

The decisions themselves moved to the ends to make this true. The learning
router keeps no signal-to-sink table; before a signal is persisted or any
reranker, supersede, rule or workflow proposal is queued, it asks the
supervised learning process for the sink mask over the bus, and a missing or
invalid response aborts ingestion. Memory pre-injection confidence comes only
over the bus, and an unavailable or malformed response means the context
envelope is omitted, and nothing local stands in for it. Governance's response
tool-policy decision fails closed the same way. A module cannot quietly answer
its own question, and nothing takes a local fallback when the answer does not
arrive.

Execution runs in fully isolated containers on the same terms, and that case is
worth its own section, because it is where the rule stops being enforced by the
architecture and starts being enforced by the kernel.

## A delegate gets one socket, and everything is behind it

The first article in this series opens with a model that got around its
protections, took an unused node, and spent a testing API key on inference. It
did that over the network, because the network was there.

A delegate now runs in a container created with `--network none`. No interface,
no route, no IP stack to configure or evade. The deployment check is `curl
https://api.github.com` from inside, which has to fail with no route and not
with an auth error.

What replaces it is one bind-mounted Unix socket with aimee-server on the far
end, and the interesting part is how much comes back through it. The forge, the
web, memory, the code index, the model providers: every one of them is a tool
call on that socket. The delegate is handed a surface where each capability has a
name, a grant and a place on the tape, in exchange for an IP stack where it had
none of those.

Package installs make the point, because they are the case that looks like it
must be an exception. A delegate installs from a registry by speaking ordinary
HTTP proxy protocol, and its package manager needs no special support: there is
a proxy configured, and it uses it. The proxy is reached over the same Unix
socket, aimee-server answers it, and one function there is the only thing in the
module that may open an IP socket at all.

Policy lands at that single point, in the module aimee's own configuration calls
the sole-egress module. Seven registry hosts, wildcarded only where Ubuntu's
geographic mirrors demand it. Ports 80 and 443, because anything else is a
different protocol wearing a proxy request. The host is resolved, validated, and
dialled as a numeric address without returning control in between, so a second
lookup cannot move the destination after the check passed. Authorization,
proxy-authorization and cookie headers are stripped on the way through. A
deadline and a byte ceiling bound what one request can become. The allowlist,
the resolver and the dialer are package-private, so no caller inside the module
can widen the policy, supply a lying resolver, or dial something other than the
address that was validated.

And it records where it went. The destination the module reports is the numeric
address it actually dialled. A name the delegate asked for would be a record of
the request, and a DNS lookup repeated afterwards for the log would be a record
of some later moment. Those three answers diverge exactly when it matters. An
audit trail built from names tells you what was requested; this one tells you
where the bytes went.

The hosted models are inside this too, which is the part people assume is
exempt. A remote-only model like Claude or Codex is handed the same container,
because the agent process acting for it runs there, and its network-bound tools
are replaced instead of trusted. Claude Code's built-in `WebSearch` and
`WebFetch` come off its allowed-tools list, and `web_search` and `web_read` go
back on, mediated over the bus and landing on the tape like everything else. The
model keeps the capability. It loses the private route.

Be clear about what that cost. `--network none` takes capabilities away, and
each one had to exist on aimee's side **before** the network went, or the
sandbox is breakage wearing a security argument. A network-less container could
not commit at all until the mediated git tools existed. The order was not
optional.

There is a second half to why this was affordable, and it is the reason the
other two articles come first.

Most of what an agent reaches the network for is a lookup. How this library
behaves, what was decided about this last time, what this error means, where
this thing is configured. Those are recall questions, and recall is local. A
delegate holding full access to aimee's memory and the code index has been
answered already, before the question would have become an HTTP request.

So the demand for egress falls before the supply of it is cut, and that order is
the whole trick. A sandbox around something that constantly needs to leave is a
standing argument with your own users, and it is an argument the sandbox
deserves to lose, because the thing inside it is right: it does need what it is
asking for. Make the memory good enough and most of the need stops arriving.
What survives is narrow enough to name seven hosts.

A reach that is genuinely needed then gets paid once. What comes back is
extracted, classed, dated and stored by the machinery in the second article, so
the next session answers that question out of memory and never leaves. Egress
here is a cost with a decay curve attached, and it is the first article's loop
pointed at this problem: the system reduces its own need to reach out by
remembering what reaching out told it. Security boundaries usually age the other
way, with the needs growing while the restriction stays where it was put.

The measurement campaign in the first article is load-bearing here for the same
reason. If recall is thin or wrong, this design is a cage around a model that
cannot do its job, and the honest response would be to open the network back
up.

The verification is what stops this being a Docker flag. Every start and resume
is handed over only after the sandbox module proves three things about the
running container: its network mode, the exact source, target and read-write
state of every mount, and an effective environment holding no credentials and
exactly one writable control socket. A failed observation destroys the container
and refuses it. So does an unknown one, which is the rule from the first two
articles arriving in the runtime: absent is not open. The C backend supplies
runtime facts and cannot pick a network mode or weaken that verdict.

So the outermost edge of the system obeys the rule the rest of it does. A client
reaches the world by asking something that is holding a grant and writing to a
tape, and the shape of that is the same whether the client is a module inside
the process tree or a model in a container with no way to speak IP. The posture
is on by default, `delegate_sandbox: false` is the operator's only host opt-out,
and all of it is 0.4.0. The Go ownership, the post-start verification and the
proxy policy arrived in [pull request
2839](https://github.com/RakuenSoftware/aimee/pull/2839).

## The defaults are boring on purpose, and the leash is long

Here is the section promised at the top, and the invariant above is the whole
of the answer.

Almost every behaviour in aimee can be configured. The module seams are the
easiest to point at: the vector store is a module, so is the embedder, modules
register at runtime, and MCP servers and pluggy plugins attach through the
transport. It does not stop there. The thresholds in part two are constants.
Confidence weights, the promotion and expiry clocks, how far a memory has to
climb, the scope bands, the recall weight vector, container policy, which model
does the work: settings, most of the way down.

Over the top of that, every default is chosen to be dull. PostgreSQL for
storage, pgvectorscale for vectors, supervised processes, ordinary capability
grants, patterns settled before most of the people using them started working.

The criterion is the worst case, and whether that worst case is knowable in
advance. The transport is held to that rule already; this applies it to
everything else. A store ten times quicker than Postgres on the median that
occasionally stalls for ten seconds is worth nothing here, because the ten
seconds is the part a person waits through and the part somebody gets called
about. A duller thing whose bad day is documented beats a quicker one whose bad
day is a surprise.

The two in the morning test from the top of the article is the same thing
stated as an engineering property. The misbehaviour has a name, the operational
answer is already written down, and nobody is deriving it from first principles
while half awake.

Those two properties usually trade against each other. A system that permits
deep customisation either locks the surface down until the customisation is not
worth having, or opens it and gives up any claim about what the result will do.
Pick extensibility and lose the guarantee, or pick the guarantee and ship
something rigid.

Both stay available because the guarantee is enforced at the crossing rather
than in the settings. Re-tune every constant in the memory lifecycle and you
change what the system believes and how fast it believes it; you do not change
what any of it can reach, because reach is decided when a frame crosses,
against a declaration made before the module existed. Swap the vector store for
something we have never seen and the tap still records everything it does. The
knobs move behaviour. The invariant does not have a knob.

So the defaults are conservative because we are the people they wake up, and
the surface is wide because that is a different question from whether our
defaults suit you. What is not configurable at runtime is the part that decides
what anything can reach, and that is the only part that has to hold still.

## Attacking the chokepoint buys nothing

The obvious objection has an answer, and it is the easiest thing here to miss.
Route everything through one component and you have built the perfect thing to
compromise.

**The bus has almost no attack surface, by design. It is just a bus.**

At the heart of it, it does two things. It communicates: between modules, and
between aimee instances, which is how the thin client, `aimee-server` and
`aimee-kb` reach each other. And it offers validation behind that
communication, supplied by another module or another server.

Everything else on its list is how those two get done. It stamps envelopes. It
handles mTLS between instances and bearer tokens, and carries the authorization
riding on them. That is the inventory, and a list is worth more than an
adjective, because a reader can go and check it.

Note what is not on it. PAM and OIDC are not the bus's job. Dedicated modules
own those, and the bus carries what they decide the same way it carries
anything else. That is the pattern: the transport does not interpret payloads,
decide policy, or run anything on anyone's behalf, so even authentication is
answered somewhere with a name and a grant.

So a bearer token buys the ability to speak as some identity on the bus. What
that identity may say is the enumerated list in its grant, and every word of it
lands on the tape. You have not acquired a capability. You have acquired a seat
with a name on it, in a room that is being recorded.

## Validation runs both ways, so nothing is trusted by position

A downstream module can check that the upstream module or server is behaving as
expected, with no obligation to accept whatever arrives because of where it
came from.

An OIDC server signs off that a caller is authenticated. The downstream module
does not have to take that on faith because it arrived stamped: it can go back
to that OIDC server and verify the authentication is valid. The claim and the
authority for the claim are separable, and a module is allowed to ask.

So there is no party in the system that everything else has to trust.

Now follow the attack through. Say you compromise the bus outright. The module
you are lying to can go and check with the OIDC server, so now you need the
OIDC server as well. And once you are compromising the OIDC server: why did you
bother with the bus? Go straight there. Everything the bus could have given you
was downstream of a thing you now own directly, and the bus leg of that attack
only added an audit trail of you doing it.

A component with no real attack surface looks like that from an attacker's
side. Impregnable is the wrong word for it. Not worth the trip is closer.

The same holds if something got control of another part of aimee outright. It
is still on the far side of the same transport, still holding only the event
kinds that part's grant enumerates, still writing to the same tape. And because
validation runs downstream as well as up, the modules it starts talking to are
entitled to disbelieve it. Capturing something upstream does not confer the
right to be obeyed. What it captured is one more participant.

Take the case that should worry you most, since it is the one the first article
in this series is about. Suppose a model gets control of the isolation module
itself: the component whose job is confinement, which is exactly where you
would go if you wanted out.

It gains nothing general. That module holds a grant like everything else, and
its grant serves four event kinds and publishes, subscribes and requests
nothing. So capturing it buys the ability to answer four questions and no
ability to ask any. It cannot direct traffic anywhere, because directing
traffic is not something a participant does here. The host routes, against a
table loaded before the module started. It cannot reach past the bus, because
there is no past the bus to reach: no side channel, no socket it can open to
somewhere else, no ambient authority attached to being the security component.

The property worth having follows: there is no piece of this system whose
capture hands you the system, including the pieces whose job is to stop you.
Confinement does not depend on the confiner being trustworthy, which is
fortunate, because trustworthiness is exactly the thing you cannot verify about
a component after something else has taken it over.

The awkward half of that is real and worth saying. A transport this dumb cannot
make a clever decision. It has no idea whether a request is reasonable. Every
judgement lives in the module that answers, under its grant, failing closed
when the answer does not arrive. The transport is trustworthy because it is
boring, and everything interesting had to be pushed to the ends where it can be
named and audited.

## Two numbers hold the rest of it up

Audit is all-or-nothing: 5,000 emitted rows must reach the ledger exactly 5,000
times, zero drops, with a graceful shutdown draining what is in flight. There is
no path where an action happens and the record of it is optional.

Event kinds are carved from a module's permanent reference number, and a retired
reference is never reissued, so a grant or a capture naming one can never
quietly come to mean a different module later.

## You cannot reach anything without passing the tap first

What makes the rest of it worth having turns on where the tap sits.

The host drains each client's outbound ring, stamps a monotonic sequence
number, and offers the event to the tap **before any routing decision**: ahead
of delivery, ahead of any sampling, and before the host has decided where the
thing is going or whether it is going anywhere at all.

Work through what that forbids. To affect any other part of the system you must
submit an event. To submit an event is to be tapped, because tapping happens
first. There is no ordering available in which something acts and is observed
afterwards, and no ordering in which it acts and is not observed, because the
observation is upstream of the action taking effect. You cannot go around the
tap to reach a module, because the route to every module runs through the host,
and the host taps before it routes. You cannot go around it to attack the bus
itself, for the same reason: reaching the host means submitting to the host.

The difference from ordinary logging is the whole point. Normally the component
doing a thing also writes the record of having done it, which means
compromising the component compromises the record, and the first thing anything
hostile does is stop narrating. Here the record is not the actor's job and
never passes through the actor's hands. The host writes it, upstream, whether
the actor cooperates or not, and a component has no way to be excused from it.

It holds for the failures too, which is where most audit systems quietly stop.
An event blocked by a full destination is seq-stamped and tapped once, then
retried; the retry does not re-tap and the loss does not go unnamed. An event
shed under pressure emits a typed overflow record naming the exact sequence and
kind that was lost. An event held for a producer that has since died is emitted
as `producer_reaped` **to the tap only**, because there is nowhere left to
deliver it and the loss is recorded anyway. Even the degenerate case has a
backstop: if the reserve carved out for control events is itself full, a sticky
`control_lost` flag is set. The comment in the routing code is the honest
summary of the intent, and it is the design rule for the whole file: never
silently.

In 0.4.0 metrics and logging run directly off that tap, and the record goes
off-box. The consequence is the one worth stating plainly. Something may manage
to compromise a part of this system. It cannot do so invisibly, and it cannot
do so and then edit the account of having done it, because the account was
written somewhere it never had access to, by something upstream of it, before
its action took effect.

## Cutting the tap buys a timestamp

Suppose something does get far enough to sever the tap. That is the case the
design is most interesting in, and it is where a second mechanism takes over.

`aimee-kb` holds a hash-chained, WORM evidence store and is the system of
record. Each witnessed event commits its evidence row **atomically, in the same
transaction as the source event**, so a source event cannot commit without its
evidence and a failed witness append aborts the source event. Signed
checkpoints periodically bind the shard heads under an Ed25519 root. All of it
is exported outward as ordinary log and OTLP frames, which is what puts a copy
somewhere the compromised machine does not own.

That gives two grades of detection, and the distinction matters. Tampering that
leaves the store locally inconsistent, an edited row whose hash no longer
matches or a regressed shard sequence or a corrupt checkpoint signature, is
caught **unconditionally**, by local cross-check and continuous verification.
Tampering careful enough to rewrite the rows and heads and sign them coherently
cannot be caught locally, by construction, because the local store is then
self-consistent. It is caught by comparing against the copy retained off-host.

So severing the tap buys a mark. The record stops at a known point, the
off-host copy shows where, and everything after that point is not silently
trusted: it is quarantined as unverifiable. You do not get to choose between a
true account and no account. You get a true account up to a timestamp, and an
explicit boundary after it.

Deleting the logs is the next thing to try, and it gets a similar answer,
because deletion is not destruction. Whatever survives on the underlying medium
can be recovered by ordinary forensics, and the chain is what makes the
recovered bytes worth having. Normally a recovered log fragment is close to
useless as evidence: you cannot tell whether it is the original, or which parts
were altered before or after the deletion. Here you can. A recovered record
either verifies against the hash chain and its signed checkpoints or it does
not, and that verdict does not depend on the machine it was recovered from
being trustworthy, since the anchor was exported before any of this happened.

Recovery itself is opportunistic and no one should promise otherwise:
overwritten sectors are gone, and a sufficiently thorough wipe wins. But the
useful question after an incident is rarely "do we have everything." It is "can
we trust what we have," and that question has an answer here.

Better than prevention, and more honest to offer. This can be attacked. What an
attack cannot do is look like ordinary operation, retroactively launder the
period it covers, or turn recovered evidence into unverifiable evidence.

The limits are real and aimee's own runbook states them for operators verbatim,
which is the right way round. Detection of a coherent rewrite rests entirely on
retained off-host copies: with one consumer, coverage is exactly what that
consumer retained; with several, coverage is the intersection of what each
retained over the incident window, and a gap no consumer covered is a gap in
detection. Retention is the operator's job, and `aimee-kb` cannot tell "no
consumer configured" from "consumer down" and does not pretend to. Nor does the
chain defend a fully-compromised single machine able to rewrite a user's
workstation, `aimee-server` and `aimee-kb` consistently. The defence against
that is the breadth of external copies.

The witness chain and the bus record are also two mechanisms. The chain makes
evidence tamper-evident. Reconstructing what actually happened, in order, is
the tap's job. They answer different questions and this article should not be
read as merging them.

## Two services, so that one can check the other

Aimee runs as two of these, and the split is deliberate. `aimee-kb` is better
described as the control plane than as a knowledge service: it holds the
memory, the graph, the gates, the policy and the WORM evidence chain, and it is
built against DB2, the shared PostgreSQL store. `aimee-server` is where work
happens. The daemon builds with `-DAIMEE_DB2_DISABLED`.

Control plane and execution on separate processes is a standard shape. What
falls out of it here is the part worth pointing at.

Two processes, two identities, two hosts, two grant sets, and each keeps a
record the other can be checked against. That is the point of the arrangement.
Compromising one does not deliver the other, and it does not deliver a coherent
story either, because the story now has to agree in two places that a single
compromise does not reach. It is the same instinct as validation running both
ways, promoted from modules to services: nothing is trusted because of where it
sits.

Read the earlier caveat again with that in mind. The witness chain does not
defend against something able to rewrite a user's workstation, `aimee-server`
and `aimee-kb` consistently. Two of those three are this split. The bar was
deliberately moved from compromising a machine to compromising both halves in
agreement.

And agreement between the two hosts is not the end of what a forgery owes. Both
export outward continuously, to whatever observability consumers an operator
has configured, and metrics go with the narrative: counts, rates, timings,
volumes, all derived from the same stream. Those numbers are an independent
projection of the same events, so a story rewritten to be internally consistent
must also come out consistent with every aggregate anybody already computed
from the original, on machines the attacker does not hold. Remove an event and
some counter is one too high. Adjust the counter and it disagrees with the rate
derived from it, or with a second consumer's copy, or with the timing envelope
around it.

Note which way the arithmetic runs for each side. For detection, coverage is
the intersection of what the consumers retained, which is why the runbook makes
retention the operator's responsibility. For the forgery, the burden is the
union: every consumer that kept anything at all is one more place the lie has
to hold, and it only takes one of them to disagree.

And the compromised half cannot simply stop talking. The daemon is compiled
with DB2 disabled, so the memory it recalls from, the facts it writes, the
learning ledger, the endogeneity gate and the evidence chain all sit on the
other side of that line, reachable only by asking. Keep working and you keep
generating records in a service you do not control, which is what you were
trying to avoid. Stop, and you are left with an agent that has no memory, no
recall, nothing to store to and no gate answers, which is most of what made it
worth taking. That door was not left open carefully. It falls out of the memory
living somewhere else, which it does for reasons that had nothing to do with
security.

The capabilities are split the other way too, and that is what makes neither
half worth taking on its own.

`aimee-server` is the half that can act, and what it can act on is the machine
it runs on. Compromise it and the blast radius is that host: not the estate,
and it stops there.

The control plane is where everything worth having lives, and it is not inert.
It authenticates, it answers OIDC, it makes authorization decisions, it curates
and synthesises.

It will also run a plugin, and that one needs stating precisely, because it is
the only way code executes on that side. We ship none. An MCP plugin or a
pluggy plugin installed on the control plane runs on the control plane, and how
far it reaches is a property of the plugin somebody chose to install. Install
nothing and nothing runs there.

The general rule behind that is worth saying once. The architecture bounds what
it grants. It does not bound what an operator decides to grant. Nothing here
stops someone writing a module that offers root on the box and then granting it
everything it asked for, and no design can: a system that could override its
operator would be a worse problem than the one it solved. What the mechanism
guarantees is narrower and still worth having. That module has to be declared.
Its reach is written in a grant file somebody can read, before it runs, in the
same format as every other grant. You can give away the store here. You cannot
do it quietly.

So here is the claim, stated plainly enough to be held to:

**No module can do anything within aimee that is not either visible or allowed
by its grants.**

The claim is about coverage, and it is narrower than "nothing bad can happen"
or "every extension is safe", both of which would be false. There is no action
inside this system that is both outside a grant and outside the record, because
the grant bounds what may be attempted and the tap records what was.

The limit that goes with it belongs in the same breath. Install a malicious MCP
plugin and aimee will observe it and give you the traceability to work out what
it did, and that is all it will do. It will not stop it, beyond holding it to
the grant it was given. Detection and provenance, and that is the whole of it.

At least for now. That is a statement about today's design and a permanent
position, and it is the obvious place for this to get better.

What the control plane cannot do, with or without plugins, is initiate.
Everything above is a reply. The plugin call arrives from a server over the
`mcp.call` channel and the result goes back as an answer to that request, and
the plugin runs in the daemon that hosts it, which is the point of the
arrangement. There is no channel by which the control plane sends a command to
a server, no client for a server's API on that side, and nothing over there
built to start a conversation. It answers, at some length, and never speaks
first.

That distinction is narrower than "the control plane cannot execute", and it is
the one the code actually supports.

It also asks for little. The heaviest credential the design needs on that side
is a read-only git key, and read is all it wants: the control plane reads
repositories to know about them, and never needs to change one. An operator can
of course hand it more than that, and if they do they have widened their own
blast radius, which is a different thing from finding a hole in this one. What
the architecture requires and what a deployment provisions are different
questions, and only the first one is mine to answer.

Saying the control plane can do nothing would be false, and would fall over the
moment somebody found the auth code. It holds real capability. None of it is a
way to make something happen out in the world.

The boundary is real in the other direction too, and enforced by the compiler
and not by convention, which produces its own failure mode: code can be placed
on the side that cannot reach its own data. Four pieces of the self-learning
work had landed that way, and the [first
article](https://rakuensoftware.com/blog/aimee-recursive-self-learning) carries what that
cost and the check that catches it now. That is the bill for the split and it is
worth paying. A boundary strong enough that two halves can check each other is
strong enough to strand code on the wrong side of it, and a boundary that could
not do the first would not have done the second either. What it buys is that no
single process holds both the activity and the record of it.

Line those up and see what each compromise actually yields. Take the server and
you get one machine and an agent that has forgotten everything, still narrating
into a service you do not hold. Take the control plane and you get the memory,
the ledger, an auth surface, a read-only git key, and whatever plugins the
operator chose to install there. What you do not get is a way to make anything
happen that nobody asked for, because you cannot reach out from there. Neither
of those is an agent. Assembling one means holding both at once, keeping their
stories consistent with each other, and keeping both consistent with whatever
left the building before you arrived.
