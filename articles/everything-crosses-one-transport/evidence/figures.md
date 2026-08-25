# Reporting record and figure provenance

Every figure in
[`everything-crosses-one-transport.md`](../article/everything-crosses-one-transport.md),
and where it came from.

Part three of three. The self-learning article is
`articles/aimee-recursive-self-learning/`; the memory article is the second. Figures
shared with those pieces are noted here and in theirs, so a number is not
recorded twice as if independently sourced.

Evidence is first-party and lives in the public
[aimee repository](https://github.com/RakuenSoftware/aimee) rather than in this
folder. All paths read from `testing` on 2026-08-24.

## Sources

| key | document | read |
|---|---|---|
| `BUS` | `docs/EVENT_BUS.md` | 2026-08-24 |
| `BASE` | `bench/bus_baseline.json` | 2026-08-24 |
| `GATE` | `scripts/check_bus_perf_gate.sh` | 2026-08-24 |
| `GRANT` | `.ci-logs/bundle/grants/server/learning.grant` | 2026-08-24 |
| `MODS` | `docs/modules/README.md` | 2026-08-24 |
| `MEM` | `docs/modules/memory.md` | 2026-08-24 |
| `ATTACH` | `src/core/event_bus/bus_attach.c` | 2026-08-24 |
| `RUNTIME` | `src/core/event_bus/bus_runtime.c` | 2026-08-24 |
| `PROD` | `docs/validation/recursive-self-improvement-producers-2026-08-24.md` | 2026-08-24 |
| `PR` | PR #2835, merged to `testing` as `877e994c2f` | 2026-08-24 |

## Figures

| figure | source | note |
|---|---|---|
| per-event dispatch measured at a 134 ns median | `BASE` | host enqueue through client dequeue, excluding module work; median over batched samples with a 16-byte inline payload on the reference dev box, from `src/tests/bus_bench.c`. **Corrected 2026-08-25:** the prior article called 134 ns a bounded maximum. The enforced ceiling is 2,000 ns |
| comparison with a cgo call | author | **Withdrawn from the article, 2026-08-25.** `bench/bus_baseline.json` commits no comparison with an in-process call and says that comparison is outside its budget |
| the cost stacks: one request crosses the transport many times, so per-hop cost is multiplied by hop count | author | the article names memory, the recall gate, the confidence band and governance as example hops. **No hop-count distribution is measured or published**, and none is claimed; the argument is about the shape rather than a figure |
| the alternatives examined had significant tail latency, from collectors, slow-path syscalls, lock contention, allocation and scheduling | author | characterisation of an investigation, not a published benchmark. **No named system's tail behaviour is measured or cited**, and the article names no candidate in this passage |
| a tail crossed once is survivable; a tail crossed many times per operation is not, because the chance of catching one rises with hop count | author | reasoning about the shape, not a measured distribution |
| the committed ceiling is the promise; the observed number is evidence the promise is kept | `BASE`, `GATE` | the baseline file commits `ceiling_ns` and enforces it at merge; `observed_ns` is recorded alongside. The article's framing of which number carries the promise follows the file's own stated philosophy |
| a conventional transport or ordinary IPC, at microseconds per hop, would not sustain a coherent system at that multiplier | author | comparative claim about transport classes, not a benchmark against any named implementation. No competing system is measured or named |
| audit row publish 82 ns to the caller | `BASE` | `audit_bus_emit`, excluding the ledger write, which moves off the caller's thread |
| ceilings of 2,000 ns and 5,000 ns, enforced as a merge gate | `BASE`, `GATE` | the gate builds and runs the benchmark and fails over the ceiling |
| audit exactly-once, 5,000 rows, zero drops, drained on shutdown | `BASE` | `test_bus_audit_durability` |
| twenty-two components run as supervised processes | `src/modules/process-contracts.json` | 22 of 30 are `execution: process`; the other 8 are `execution: core`, linked into the daemon. Corrected from an earlier draft that read "sixteen supervised process batches cover every production module": sixteen is the count of C-to-Go port batches in `docs/EVENT_BUS.md`, not the count of modules |
| request/reply, typed capability errors, cancellation, arena leases | `BUS` | the basis for saying it is not an event bus |
| producer, outbound ring, host, inbound ring, consumer, with an ordered capture tap | `BUS` | |
| the learning router keeps no local signal-to-sink table; a bad reply aborts ingestion | `BUS` | event `6145` |
| memory pre-injection confidence only over the bus; envelope omitted otherwise | `BUS`, `MEM` | event `5893` |
| the module seams the article points at, and the thresholds it attributes to part two | `MEM`, `BUS` | **shared** with part two, which carries the source detail: five seams, write gate `5890`, extract and retraction pre-scan `5889`, PII recall gate `5892`, confidence band `5893`, embedding `5891`. The memory grant serves six kinds; `5894` is a command declaration rather than a decision |
| governance response tool-policy fails closed | `BUS` | |
| a grant names executable, identity, and the exact event kinds a module may serve, publish, subscribe to and request | `GRANT` | the learning grant serves `6145` and publishes, subscribes and requests nothing |
| no event travels over a socket; a module reads and writes its mapped queue pair and the shared arena directly | `BUS`, `ATTACH` | the data path is shared memory with no per-event syscall. An earlier draft described the module boundary as "a process that connects to a Unix socket and speaks a wire protocol", which describes the one-time attach and gets the traffic path wrong |
| descriptors are handed over once at attach: grant match on principal, uid and executable, then anonymous `memfd` regions over `SCM_RIGHTS` | `BUS`, `ATTACH` | `bus_fd_send`/`recvmsg` in `src/core/event_bus/bus_attach.c`, up to three descriptors; a module with no matching grant is refused with `bus: attach denied` |
| each client maps only its own rings; the control region is read-only | `BUS` | it cannot enumerate or map another client's rings |
| a module is a completely independent execution space: own process, address space, runtime and failure domain | `BUS`, `ATTACH`, `MODS` | **framing, not a new figure.** It names one property over facts already recorded here: the per-slot queue pair, the read-only control region, the dynamic module population, and separately shipped modules staying off the arena. Added 2026-08-24 |
| a grant is a build-time behaviour guarantee, not a registration: reading it tells you what a module may do before it runs | `GRANT`, `RUNTIME` | the learning grant serves `6145` and publishes, subscribes and requests nothing. The article frames this as a guarantee rather than a restriction, which is the author's stated intent for the mechanism |
| the module population is dynamic while the declaration holds still | `RUNTIME`, `BUS` | `grant_find()` matches principal class and ref on every attach and re-checks peer uid and executable path; `bus_runtime_policy_load_dir()` is called once at bus start (`obs_bus.c:641`) and there is no reload entry point. An earlier draft of this record treated the absence of a reload path as a gap; it is the mechanism working as designed |
| MCP servers and pluggy plugins attach through the transport and inherit its guarantees | author, forward-looking | **Not shipped at time of writing.** `docs/proposals/pending/mcp-adapter-bus-routing-residual.md` is PENDING, with remaining deliverables including correlation, cancellation, deadline and bounded-payload semantics, identity and audit preservation across the bus boundary, and parity proof before switching defaults. The author states both land in 0.4.0. Recheck at the tag |
| C and pure-Go clients exist, held to byte-for-byte conformance tests, with no cgo | `BUS` | the basis for the any-language claim |
| separately shipped module processes do not allocate arena leases; they use a fragmenting protocol with a 16 MiB message limit | `BUS` | this is what makes the module boundary language-agnostic rather than C-only |
| the arena is cooperative isolation for trusted native modules, not a sandbox for hostile code | `BUS` | quoted as a limit, not as a guarantee |
| event kinds are carved from a module's principal ref as `4096 + ref*256 + stage` | `MODS` | |
| a retired principal ref is never reissued | `MODS` | `retired_principal_refs` |
| four pieces of the self-learning work placed where they could not reach their own data | `PROD`, `PR` | **shared** with part one, which carries the detail, the run log and the lint check. Moved there on 2026-08-24: this article states the split's cost and points to it. The rows this record previously carried for the incident moved with the prose |

### The two-service multiplicity

**Corrected 2026-08-24.** The article described `aimee-kb` and `aimee-server` as
a split without saying how many of each a deployment runs, which reads as one
for one. One KB stands behind every enrolled user; a server belongs to a single
user. The article now says so where the split is introduced and again in the
tally.

**Breadth is not capability, and an earlier revision of this correction
conflated them.** It called the control plane "one large blast radius", which
contradicts the article's own argument that the control plane cannot initiate,
cannot execute and cannot reach out. The two halves are asymmetric on two axes
that do not line up: the server is narrow in reach and is the half that can
act; the control plane is broad in reach and cannot act. A compromised control
plane reaches every enrolled user's memory and can hand back memory that is
wrong. That is the limit the article already states for a compromised memory
module. It is not a capability to make anything happen.

Source: the author, corroborated by `docs/DEPLOYMENT.md` on `testing` ("Server
and one KB are declared together", "The one-KB Compose files are deployment
profiles, not the fleet limit", and `KB_FLEET.md` for routing among several KB
containers, which is not integrated in this checkout) and by `docs/SECURITY.md`,
which carries per-user write grants and KB-signed user identity. Shared with
part one.

**No claim is made here about how many users one KB serves in practice**, and no
deployment is measured. The claim is the shape, not a capacity figure.

## Author's statements, not documents

| claim | note |
|---|---|
| the bus does two things: communicate between modules and instances, and offer validation supplied by another module or server | envelope stamping, mTLS and bearer tokens are how those are done, not separate functions |
| that inventory is complete at 0.4.0 | stated as checkable rather than as an adjective; verify against the shipped transport at the 0.4.0 tag |
| PAM and OIDC are owned by dedicated modules, not by the bus | the bus carries their decisions; it does not authenticate |
| validation runs in both directions | no party in the system is trusted by position alone |
| a module receiving an OIDC sign-off can verify it back with that OIDC server | worked instance of the above |
| containers are fully network-isolated with the bus as the only channel out | |

## The language-choice account

Author's account of a design decision, given directly. No contemporaneous
evaluation document is cited: the claim is that the transport needed a bound
rather than a good average, that Go and the other candidates examined offered no
way to guarantee one with memory layout and buffer lifetime under the caller's
control, and that the field narrowed to C and Rust for the whole architecture,
with C chosen.

**No reason is published for C over Rust**, because the author did not state one
and the article does not invent one. If that choice is worth explaining, it
needs a sentence from the author rather than a guess.

No benchmark against Go or Rust is offered and none is claimed. The article's
statement is about what those languages guarantee, not about what they measure,
and it is the author's characterisation of an investigation rather than a
published comparison. A reader who disputes it is disputing the author's
account.

The consequence drawn from it is checkable: sixteen module identities are served
by Go processes (`docs/EVENT_BUS.md`), on the far side of the C transport.

## The novelty claim, and how it is scoped

The transport is the only thing claimed as novel across all three articles.
Everything else is explicitly stated as prior art done a bit differently: the
self-learning technique is called decades old in part one, with genetic
algorithms and training loops named, and the memory in part two is described as
careful rather than new.

The claim is scoped to what the author has seen and worked with, which is a
narrower and more defensible base than a reading survey. No field survey was
conducted, the thing has no name, and the article says both.

**The claim is the combination, not any component**, and the article now names
the prior art rather than gesturing at it. Transport shape is placed in the
ring-buffer lineage (LMAX Disruptor, virtio vrings, `io_uring`, DPDK), with
**Aeron** named as the closest whole-system comparator. The admission model is
placed in the capability-microkernel tradition (**seL4**), where a component may
send only on endpoints it holds a capability for.

**No performance comparison against Aeron or any other named system is made or
implied**, and none was measured. The systems are named to locate the design,
not to beat them.

That placement is the article author's characterisation, arrived at by reading
aimee's code against systems known from elsewhere. ~~It should be checked by
someone who has actually built on Aeron before publication.~~ **Dropped as a
gate, 2026-08-24.** The naming locates the design and makes no performance or
capability comparison, the article says the base is what the author has seen
and worked with, and one counterexample settles the claim either way. An
outside Aeron reader would be welcome and is not a condition of publishing.

The article also corrects itself in passing: an earlier draft called the thing a
"shared-memory bus", which is wrong twice over. There is no shared medium and
nothing contends, since each client maps only its own queue pair.

So one counterexample settles it: a transport carrying point-to-point
request/reply with typed capability errors and cancellation, over shared-memory
rings with no socket and no per-event syscall in the data path, with dispatch
held under a committed ceiling by a merge gate, that everything in a system
crosses with nothing exempted for being hot.

The article also states why the claim matters, which is a separate assertion
worth marking: the audit record, the grants, the isolation, the language-agnostic
module boundary and the loops all depend on the bound. That is an argument about
the architecture rather than a measurement, and it is the piece's own reasoning.

## The unit-of-analysis argument

The article's security claim is that a grant is a generalised attack surface, so
analysis scales with the number of grants rather than the number of extensions,
and a new extension under an existing grant needs no new analysis because it
cannot exceed what was already analysed.

That is an argument from the mechanism, not a measurement. No security review of
any grant is published here, and no count of grants-versus-extensions is
offered.

The article states the limit itself: this bounds a blast radius and certifies
nothing. A plugin can do everything its grant permits, so an over-broad grant
produces an over-broad plugin. The claim is only that the over-broad grant is
readable in advance in one file.

### The tap claim

**Verified in `src/core/event_bus/bus_route.c`.** The tap is "the single
full-stream observer, before any routing decision — D6". Every event is
seq-stamped and offered to the tap ahead of delivery, once: a BLOCKed event is
"seq-stamped and tapped once" and its retries do not re-tap. Shed emits a typed
overflow record naming the lost seq and kind. `producer_reaped` is tap-only, for
a client that no longer exists. A full control reserve sets the sticky
`control_lost` flag. Arena payloads are materialised into the tap once, so
replay does not depend on a live arena.

So the article's claim that nothing can reach another part of the system without
passing the tap follows from the ordering: routing is downstream of tapping.

`bus_host_set_tap()` is a **single slot** — one function pointer and one
context. Today `obs_bus` occupies it with `bus_capture_tap`. Running metrics and
logging off the tap means multiplexing behind that one registration.

**Forward-looking, and marked as such in the article:** metrics and logging
running directly off the tap, with the record going off-box, is the 0.4.0
design and is not what ships at time of writing. Today the tap's only consumer
is a local capture file that is best-effort, abandoned on write failure, and
pruned at 16 sessions. The durability gap is the subject of a separate proposal.
Recheck at the tag.

The article states the threat-model boundary itself: this is a property against
component-level compromise, not against an attacker owning the host, and
`docs/EVENT_BUS.md` is cited in the body for the off-host witness requirement.

### The tamper-evidence claim

Source: `docs/runbooks/witness-evidence-and-egress-gate.md` on `testing`, read
2026-08-24. This is shipped work (P7), not forward-looking, and it corrects an
earlier draft of this article which said an off-host witness "is still required"
as though none existed.

Verified from the runbook: `aimee-kb` holds a hash-chained WORM evidence store
and is the system of record; each witnessed event commits its evidence row
atomically in the same transaction as the source event, so a source event cannot
commit without its evidence and a failed witness append aborts the source event;
signed checkpoints bind shard heads under an Ed25519 root; records, checkpoints
and leaf snapshots export outward as log/OTLP frames.

Two grades of detection, as stated there: locally-inconsistent tampering is
caught **unconditionally**; a coherent rewrite is detectable only against a
retained off-host copy, because the local store is then self-consistent by
construction.

**The article carries the runbook's own conditional-coverage statement**, which
that document marks for shipping to operators verbatim: coverage equals what
consumers retained, is the intersection across several consumers, a gap no
consumer covered is a gap in detection, retention is the operator's
responsibility, and `aimee-kb` cannot distinguish "no consumer configured" from
"consumer down". The runbook also disclaims defence against a fully-compromised
single machine able to rewrite workstation, server and KB consistently.

**Scope note carried into the article:** the witness chain covers witnessed
events and does not reconstruct history; the runbook assigns reconstruction to
the event-bus record/replay work. The two mechanisms answer different questions
and the article says so rather than merging them.

**The recovered-logs argument** is a consequence drawn from the chain's
properties rather than a documented procedure: a recovered record verifies
against the hash chain and its exported checkpoints, or it does not, and that
verdict does not depend on the recovered-from machine being trustworthy. No
forensic recovery has been performed or tested, and the article states that
recovery is opportunistic and that a thorough wipe defeats it.

### The two-service split as a security property

The article frames the `aimee-server` / `aimee-kb` split as deliberate mutual
verification rather than as an organisational division, and connects it to the
witness runbook's own caveat: the chain does not defend against something able
to rewrite a user's workstation, `aimee-server` and `aimee-kb` consistently, and
two of those three are this split.

Checkable structure: separate processes with separate identities, separate bus
hosts (`docs/EVENT_BUS.md`: each daemon hosts its own bus), separate grant sets
(`.ci-logs/bundle/grants/server/` and `.../kb/`), and the KB as holder of the
WORM evidence store and system of record (witness runbook).

**The design intent is the author's account.** No cross-verification procedure
is documented here, and the article does not claim a specific mechanism by which
one service audits the other beyond the records each holds. If a concrete
cross-check exists it should be named before publication; if it does not, the
claim is about what the arrangement makes possible rather than about a shipped
routine.

**The metrics-consistency argument** extends that: because both services export
records, checkpoints and metrics outward continuously, and the witness runbook
notes metrics carry numbers only, a coherent forgery must agree not just across
the two hosts but with every aggregate any retaining consumer already computed
from the original stream.

The article states the arithmetic in both directions, which is the honest form:
for detection, coverage is the **intersection** of what consumers retained (the
runbook's own conditional-coverage statement); for a forgery, the burden is the
**union**, since one disagreeing consumer is enough.

This is reasoning from the export design, not a demonstrated result. No forgery
has been attempted against a live deployment, and no consumer configuration is
specified or assumed. With no retaining consumer configured, this argument buys
nothing — which is exactly what the runbook warns operators about.

**The dependency argument** is the half that carries the claim, and it is checkable.
`aimee-server` builds with `-DAIMEE_DB2_DISABLED`, so memory, typed facts, the
learning ledger, the endogeneity gate and the evidence chain are all KB-side and
reachable only by request (`AIMEE_KB_API_URL`). This is the same boundary that
produced the four cross-tier defects reported in part one, read from the
security side: a compromised daemon that stops talking to the KB loses recall,
storage, learning and gate answers.

The article states this as a consequence of where the memory lives rather than
as a designed-in control, which is the honest framing — the split predates the
security argument it now supports.

**The capability partition** is the author's characterisation: `aimee-kb` is the
control plane, holding memory, graph, gates, policy and the evidence chain with
no execution capability; `aimee-server` executes and its reach is the host it
runs on.

The article uses "control plane" as the accurate description and explicitly
claims no novelty for the pattern, which is standard. That matters for the
series' overall novelty claim: the split is textbook, and only the transport
beneath it is claimed as new.

The article states the KB claim in its precise form rather than absolutely: the
control plane is **not inert** — it authenticates, answers OIDC, makes
authorization decisions, curates and synthesises — and what it lacks is the
ability to **initiate**. It has no channel by which it commands a server; the
relationship runs one way. Its worst credential is named: a read-only git key.

That formulation is falsifiable, and both falsifiers were checked against
`testing` on 2026-08-24:

- **A channel from the control plane to a server that carries a command.**
  **None found.** No `src/kb/` source calls `kb_client_*`; every reference is a
  comment describing how servers reach in. There is no server-API client on the
  KB side. The one execution path, `kb_handle_mcp_call` in
  `src/kb/kb_service_agent.c`, is inbound by contract: "Reached from a server
  over the mTLS `/v1/actions/mcp.call` channel [...] a plugin runs in exactly
  the daemon that hosts it", and the result returns as a reply. Two other
  outbound calls exist, `agent_http_post` to OCR and TSR sidecars
  (`kb_ocr_sidecar.c`, `kb_tsr_sidecar.c`), which are processing services rather
  than servers.
- **A control-plane code path that requires write capability.** **None found.**
  The only git operation reachable from the KB is `git_resolve_default_sha`
  (`src/code_collect.c:298`), used by `kb_ingest_workers.c` and
  `http/kb_http_code.c` to decide whether the canonical code moved. It resolves
  the default ref and runs `git rev-parse <ref>^{tree}`. No push, commit, clone
  or fetch appears in `src/kb/`.

**The audit changed the article.** An earlier draft said the control plane has
no execution capability. It will run a plugin hosted on that side, so the
article now claims only that it cannot *initiate*, which is what the code
supports.

The article also scopes the plugin case the same way it scopes the git
credential: **aimee ships no plugins**, so that execution path exists only if an
operator installs one, and how far such a plugin reaches is a property of the
plugin rather than of the architecture. Install nothing and nothing executes
there. That is a claim about what is shipped, and it is checkable by looking for
a bundled plugin; none was found in the tree.

**The general boundary of responsibility** is stated once in the article and
governs the credential, plugin and module cases together: the architecture
bounds what it grants, not what an operator decides to grant. An operator can
write a module offering root and grant it everything, and the article says
plainly that no design can prevent this, since a system able to override its
operator would be the larger problem.

What it claims instead is narrow and checkable: such a module must be declared,
and its reach is legible in a grant file in the same format as every other,
before it runs. The claim is about visibility, not prevention.

### The claim, as stated in the article

> No module can do anything within aimee that is not either visible or allowed
> by its grants.

This is the article's formal security claim and the one to hold it to. It rests
on two mechanisms already recorded above: the grant bounds what may be
attempted (`grant_find()` at attach, host-side routing by declared event kind)
and the tap records what was, ahead of any routing decision (`bus_route.c`, D6).

**Explicitly not claimed, and stated as such in the body:** that nothing bad can
happen, or that any extension is safe. A malicious operator-installed plugin is
observed and traced, not prevented, beyond being held to its grant.

The article marks this as today's position rather than a permanent one, with no
date attached to improving it.

This was a source read, not a runtime test, and it covers `src/kb/` plus the
functions it reaches. A path through a shared source not surfaced by these greps
would not have been caught.

**A write-capable credential found in some deployment does not falsify either.**
That is an operator provisioning choice, not an architectural property, and the
article says so: what the architecture requires and what a deployment provisions
are different questions. An earlier draft of this record listed the credential
itself as a falsifier, which was wrong — it tested the configuration rather than
the design.

The server-side blast-radius claim is likewise the author's, not a measured
containment result.

Worth checking before publication, since the article's conclusion rests on it:
that neither half alone constitutes a usable agent.

### The captured-isolation-module claim

The article's strongest containment claim is that capturing the isolation module
itself confers nothing general, because it holds a grant like any other
component.

Checkable: `.ci-logs/bundle/grants/server/sandbox.grant` serves four event kinds
(`10753`–`10756`) with `publish`, `subscribe` and `request` all empty. So the
captured component can answer four questions and ask none, and the routing
decision is not its to make — the host routes against a table loaded before the
module started (`bus_runtime_start`, grants from `bus_runtime_policy_load_dir`).

The general form — no component's capture hands over the system, including the
components whose job is confinement — is an argument from the grant mechanism,
not a tested result. See the note below on the security argument.

### The zero-day and supply-chain claim

The article claims a compromised module cannot exceed its grant, because the
host routes, the grant is loaded before the module runs, and enforcement sits on
the far side of the boundary from the compromise. That follows from the
mechanism as read: `grant_find()` resolves the grant at attach and the host
enforces event kinds at routing, not the module.

**No exploit or compromise has been simulated or tested.** This is an argument
from the design, not a red-team result, and nothing here has been through a
third-party security review.

The stated limit does real work and should survive editing, and the article
draws it along a specific line: a compromised module can **lie**, because
answering is what it was granted to do, but it has no **access** outside its
grant to compound the lie with. The claim is that compromise confers no
additional reach, not that it is harmless.

That line is also the article's epistemic claim: predicting what code will do is
intractable, reading what it may reach is a finite question with a written
answer, so grants are analysable statically at the code level. That is an
argument about what kind of question each one is, not a claim that any such
analysis has been performed and published here.

## Prior publication of two of these claims

Two arguments in this article were published on this blog in July 2026 as
[Stacking isn't composing](https://rakuensoftware.com/blog/stacking-isnt-composing),
and the article now cites it in both places instead of re-deriving them.

- **No add-on owns the order others run in.** That piece establishes it against
  pinned public source for three third-party context tools, and reaches it as a
  cost finding. This article reaches the same structural point as a safety
  finding. One argument, two consequences; it is not two independent sources for
  it.
- **Capture, audit and replay share one accepted order without merging into one
  subsystem.** Reported there against the pinned `aimee` bus and audit module
  docs. Carried here as a consequence of the tap.

That article carries a published correction dated 2 August 2026 recording that
its joint add-on cost and recall outcome was not preserved as a measurement. The
architectural finding survived the correction, and the architectural finding is
the only part cited here. **No cost or recall figure travels from it into this
article.**

## The plugin-authority argument is the author's position

The section on plugins is argument, not reporting. Its claim about how plugin
systems ordinarily work — load into the host process, run with host privileges,
authority arriving with extensibility — is a general characterisation of a
common pattern. No specific plugin system is named, measured or criticised, and
none is needed for the argument, which is about what aimee's design refuses
rather than about what anyone else ships.

The cost is stated in the article rather than left for a critic, and stated at
its real scope: what must be anticipated is the class of reach, not the
extension using it, and enumerating a new one is a build-time change rather
than a setting.

The connection to the incident in part one is the author's reasoning, not a
recorded event. Nothing is claimed to have happened through a plugin surface.

## The stated goal of the system

The article opens by stating the goal as auditable, governable, and not waking
an engineer at two in the morning. That is the author's statement of intent for
aimee as a whole, not a specification quoted from a document, and the piece
treats it as the criterion the rest of the design answers to.

It is not a claim that the goal has been met. Nothing here measures on-call
volume, incident duration or operator burden, and no such measurement exists in
this series. A reader is entitled to read it as the target being aimed at.

## The invisibility statement

Author's statement of design intent for the product, given directly: a short
setup, then invisible operation, with extensive metrics available to anyone who
wants them but not required for the system to work.

It is an aim, not a result. **No usability study, deployment survey, operator
interview or support-volume figure appears in this series**, and nothing here
measures whether installations are in fact low-attention. The article presents
it as the criterion being designed against, which is what the surrounding
sections then argue from.

The metrics half is checkable and is reported elsewhere in this record: metrics
and logging in 0.4.0 run off the tap, so the observability the statement
promises has a named mechanism rather than being an aspiration on its own.

## The defaults-and-configurability passage

Author's account of a standing design position, given directly. No design
document is cited for the position itself.

The claim is that almost every behaviour in aimee is configurable, and that the
defaults are nevertheless chosen on the worst case rather than the average: a
component whose bad day is documented over one that is quicker on the median
with an uncharacterised tail, because the tail is what reaches a person and
produces the two in the morning call.

**This is the same criterion the transport is held to**, recorded above as a
committed ceiling rather than an observed average, applied to the rest of the
system. It is not a claim of indifference to speed, and an earlier draft stated
it as "the criterion is not performance", which was wrong and is corrected
here. No tail measurement of PostgreSQL or of any alternative store appears in
this series; the position is the author's engineering judgement about which
number decides, not a result.

The mechanism drawn from it is the article's own invariant rather than any one
component: the guarantee is enforced when a frame crosses the transport, not in
the settings, so re-tuning constants or replacing a module changes behaviour
without changing reach. Grants and the tap are two instances of that, not the
basis of it. This is an argument from the design, not a measurement.

pgvectorscale is named as the 0.4.0 default. The reports in this series ran on
pgvector 0.8.0, which is what existed when they ran. Nothing here is a
vector-search measurement.

Checkable parts, which are reported elsewhere in this record and in part two:
the vector store and the embedder are modules, module registration is dynamic,
and MCP and pluggy attach through the transport. **"Almost every behaviour" is
not enumerated here and is not a closed list.** It is the author's
characterisation of the configuration surface, and a reader disputing it is
disputing that characterisation.

Shared with part two, which makes the same argument for the default memory
store specifically: `articles/the-remembering-is-the-learning/evidence/figures.md`,
"The default-store passage".

## The delegate sandbox and sole egress

The one section whose claims are enforced by the kernel and by a policy file
instead of by aimee's own design, and the one most worth checking against
source.

| claim in article | source |
|---|---|
| container created with `--network none`; no interface or route | `docs/proposals/done/delegate-sandbox-aimee-sole-egress.md`, `docs/DELEGATE_SANDBOX.md` |
| `curl https://api.github.com` from inside must fail with no route, not an auth error | the proposal, stated there as a deployment check |
| one bind-mounted Unix socket to aimee-server as the only channel out | the proposal |
| one mount: the source tree, read-write for an editing delegate, read-only for a reviewer | the proposal |
| no forge token, provider keys or vault inside the container | the proposal |
| forge, web, memory, code index and providers all become tool calls on that socket | the proposal |
| package installs use ordinary HTTP proxy protocol over the same socket, answered by aimee-server | `server-go/modules/delegates/proxy.go` |
| one function is the only thing in the module that may open an IP socket | `proxy.go`, `Serve` doc comment |
| seven registry hosts, one wildcard for Ubuntu's geographic mirrors | `proxyguard.go`, `DefaultPackageAllowlist` |
| ports 80 and 443 only | `proxyguard.go`, `ProxyPortAllowed` |
| wildcard matching is label-bounded, so `*.archive.ubuntu.com` never matches `notarchive.ubuntu.com` | `proxyguard.go`, `ProxyHostAllowed` |
| resolve, validate and dial the numeric address with no caller re-entry in between | `proxyguard.go` header comment; `ProxyDestination.IP` is the dialled address, not a later DNS observation |
| authorization, proxy-authorization and cookie headers stripped | `proxy.go`, `strippedProxyHeaders` |
| deadline and byte ceiling on a request | `proxy.go`, `ProxyDeadline` 10m, `ProxyByteLimit` 2 GiB |
| allowlist, resolver and dialer are package-private so no caller can widen policy | `proxy.go`, `Proxy` struct comment |
| the module is aimee's "Go-owned sole-egress module" | `docs/gen/configuration.md`, `delegate_sandbox` |
| the audited destination is the numeric address actually dialled, not the requested name or a later DNS observation | `proxy.go`, `ProxyDestination` doc comment |
| Claude Code's `WebSearch` / `WebFetch` removed from `--allowedTools`, replaced by mediated `web_search` / `web_read` | the proposal, recorded as done |
| default posture: network disabled, no Docker socket, no credentials, bounded CPU/memory/process/time/output, explicit image, leaked-container reap | `docs/DELEGATE_SANDBOX.md` on `testing` |
| `delegate_sandbox: false` is the only operator-controlled host opt-out | `docs/modules/delegates.md`, `docs/DELEGATE_SANDBOX.md` |
| post-start proof of network mode, exact mount set, credentialless environment with exactly one writable control socket | `docs/modules/delegates.md` |
| a failed **or unknown** observation destroys and refuses the container | same |
| the C backend cannot pick a network mode or weaken the Go verdict | same |

**The demand-side argument is reasoning, not measurement.** The section claims
that full memory and code-index access removes most of a delegate's reason to
reach the network, that a genuinely needed reach is paid once because what comes
back is stored, and that egress demand therefore decays as the system runs.

**Nothing in this series measures that.** No before-and-after egress rate, no
count of proxied requests per session over time, no comparison of task success
with and without recall. It is an argument from what the two mechanisms do,
offered as the reason the sandbox was affordable, and it is the author's
reasoning about his own system.

It is stated in a losable form in the article: if recall is thin or wrong, the
design is a cage around a model that cannot do its job. A deployment where
proxied requests per session stayed flat over months would be evidence against
it. That measurement would be worth taking and has not been.

**An earlier draft of this section was wrong and the error is worth recording.**
It described the sandbox as having no egress at all, treating package installs
as a footnote. There is egress, and it is a proxy: the delegate speaks ordinary
HTTP proxy protocol, aimee-server is the far end, and the socket underneath is a
Unix socket instead of TCP. The corrected framing is that aimee replaces the
network with a surface, which is a different claim from removing the network and
a better description of what the source does.

**Split status.** The container posture is merged on `testing` and documented
there. The Go ownership, post-start verification and the proxy policy above are
[PR 2839](https://github.com/RakuenSoftware/aimee/pull/2839), which was open with
CI outstanding when this was written and is treated as landed on the author's
statement that it merges the same day. **Re-check that it merged before
publication.**

**Update, 2026-08-24.** The sole-egress module is merged, on the author's
confirmation. The departure below is therefore closed: the section describes
shipped code rather than merging code. The original wording above is retained
because it records what was known when the section was written. Confirm the
merge commit when pinning to the 0.4.0 tag, which is the remaining step.

This is a deliberate departure from the article's rule on unshipped work,
recorded in the README. Everything past "detection and provenance" is omitted
because it is unroadmapped. This is written, reviewed and merging, and is
described as shipped rather than as intent.

The claim that a remote-only model runs against this same surface is the
author's. The checkable half is the `--allowedTools` substitution above. **No
test in this series demonstrates a hosted provider's agent process running under
`--network none`.**

## The security argument is analysis, not measurement

The claim that the bus is not worth attacking is an argument from its inventory
and from the grant model, not a result from a penetration test or a formal
proof. No third party has audited it. It is stated in a losable form: the
inventory above is checkable, and the argument fails if the transport turns out
to do something not on that list.

## Not covered here

Whether the loops the architecture supports do anything useful, and the memory
that self-learning is made of. Those are parts one and two.

## Rewrite inventory, 2026-08-25

The article was rewritten against `origin/testing` at `6bcc87e`. Existing
reporting above remains in place. This table records the disposition of every
first-party class used by the prior article.

| prior reporting | evidence class | disposition |
|---|---|---|
| 134 ns dispatch and 82 ns audit figures | committed benchmark baseline | **Retained and corrected to medians.** The article carries the 2,000 ns and 5,000 ns enforced ceilings separately |
| parity with a Go or cgo call | author judgement | **Removed.** No comparative measurement exists |
| repeated-hop and tail-latency argument | author analysis | **Narrowed.** The article says only that several crossings may occur and states that no hop or tail distribution is published |
| candidate transports and microsecond comparison | author investigation without artifacts | **Removed from prose. Preserved above** |
| private queue pairs, one-time Unix attach, `memfd` and `SCM_RIGHTS` | static source and document audit | **Retained** |
| shared arena and separately shipped process limits | static source and document audit | **Retained with the hostile-code limit beside it** |
| C and Go clients, conformance tests and language choice | static source audit plus author account | **Narrowed.** The article claims two working clients and a language-neutral contract, not support for every language |
| grants, attach identity and event-kind permissions | static source audit | **Retained with reach-versus-truth limits** |
| supervised-process counts | static inventory | **Removed from prose because the count rots quickly. Preserved above** |
| MCP and pluggy transport routing | pending proposal plus author statement | **Removed from prose.** No shipped claim remains |
| sink selection, confidence and policy decisions crossing the transport | static source audit | **Subordinated to the scoped coverage claim** |
| ordered tap, overflow and producer-reap records | static source audit | **Retained** |
| 5,000 audit rows, exactly once, zero drops and shutdown drain | committed durability test | **Retained and scoped to governed-action audit rows** |
| capture retention, replay and gap records | static source audit | **Retained with capture separated from the durable ledger** |
| complete-bus inventory and “everything” coverage | author statement plus source audit | **Narrowed.** The article names seven core-local components and external network traffic outside the claim |
| bus compromise, downstream validation and “not worth attacking” | security analysis | **Withdrawn.** The article treats the host as a concentrated risk and states that no penetration test or independent audit supports the analysis |
| isolation-process capture argument | grant audit plus analysis | **Removed as overbroad.** The general grant limit remains |
| delegate network isolation, credential absence, proxy mediation and post-start verification | shipped documentation, source audit and PR 2839 | **Retained and narrowed to documented behaviour** |
| hosted-provider execution under network isolation | author statement and tool-list audit | **Removed because the reporting record identifies no end-to-end test** |
| default and configurability passage, including storage choices | author statement and config audit | **Removed from prose.** Only the startup-loaded grant boundary remains |
| WORM chain, transaction seal, fault injection and off-host limit | source audit plus live fault injection | **Retained and updated** from the 25 August worker validation |
| two-service topology and provider-placement failure | deployment documents plus live test | **Retained briefly; detailed failure remains in part one** |
| forensic recovery after deletion | general analysis without a recovery test | **Removed** |
| security work beyond detection and provenance | unpublished plan | **Still omitted** |

The article now follows the source's own completeness boundary:
`docs/EVENT_BUS.md` says the durable coverage is “what crossed the bus,” and
explicitly excludes core-local calls. Storage-backend material remains in this
reporting record as prior reporting and test-environment context, but it no
longer appears in the article.

## Narrative restoration inventory, 2026-08-25

PR review found that the 1,705-word rewrite preserved claim dispositions but
lost the article's causal architecture story. The article was rebuilt from the
original sequence and now runs 5,310 words. This inventory updates prose
dispositions only; the raw observations and source record above remain
unchanged.

| narrative segment | restored treatment | claim boundary |
|---|---|---|
| two-in-the-morning acceptance test and ordinary-controls premise | **Restored** as the opening motive | author design goal, not a measurement |
| ring-buffer lineage and Aeron/seL4 neighbours | **Restored** | checked against official Aeron, LMAX and seL4 documentation; the combination claim remains personal experience, not a field survey |
| repeated-crossing cost | **Restored** | 134 ns and 82 ns are medians; 2,000 ns and 5,000 ns are regression ceilings; no Go-parity or tail-distribution claim |
| C host and language-neutral module contract | **Restored** | two working clients demonstrate the contract; support for every language is not claimed |
| grants and extension analysis | **Restored** | grants bound event kinds through aimee, not correctness or ambient operating-system authority |
| complete transport coverage | **Restored with scope** | applies to governed traffic that crosses the bus; core-local calls and external traffic remain outside |
| delegate incident, one-socket surface and package proxy | **Restored** | documented isolation and tool substitution retained; no end-to-end hosted-provider containment claim |
| configurability over fixed enforcement | **Restored without backend choices** | settings may change behaviour; startup grants and tap ordering remain the invariant |
| chokepoint and downstream validation | **Restored as analysis** | the article now states that no penetration test, proof or independent audit establishes the stronger security claim |
| tap, loss records and 5,000-row audit test | **Restored** | exactly-once result remains limited to governed-action audit intents |
| witness chain and off-host comparison | **Restored** | coherent local rewrite still requires an externally retained copy for detection; forensic disk recovery remains omitted |
| two-service split | **Restored** | capability and compromise consequences are qualified; backend and plugin implementation details remain omitted |

External lineage checks used the official
[Aeron media-driver documentation](https://aeron.io/docs/aeron/media-driver/),
[LMAX RingBuffer documentation](https://lmax-exchange.github.io/disruptor/javadoc/com.lmax.disruptor/com/lmax/disruptor/RingBuffer.html)
and [seL4 capability tutorial](https://docs.sel4.systems/Tutorials/capabilities.html).
