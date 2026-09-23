# Final editorial review, 2026-09-20

## Inventory made before editing

Input: article and reporting record at blog commit
`d00365f215e515eb6bcebdd608fedd981bbe807b`. Read VOICE.md Parts I and III
and ARTICLE.md Part I in `/home/virant/dev/voice-guide` before editing.
The historical reporting record remains unchanged; this document records the
new dispositions. No original raw artifacts are present in this article folder.
Referenced artifacts in other articles and repositories must remain intact.

This is an architecture essay about the August 2026 implementation. A source
read in this pass does not constitute a runtime reproduction or a security test.
No independent benchmark, interview, billing measurement or vendor comparison
is introduced. The API-key incident is an author-reported observation, not a
billing analysis.

| ID | Existing reporting or claim | Evidence class | Editing disposition |
|---|---|---|---|
| 01 | Company knowledge platform; cloud and self-hosted; identity and scope | Author positioning and shared product document review | Retain brief orientation and interest disclosure; remove promotional scale implication. |
| 02 | Two-in-the-morning goal, low-attention setup, conservative defaults | Author design intent | Retain goal; distinguish aspiration from measured incident reduction; consolidate repeated defaults argument. |
| 03 | Other transports' long tails and named possible causes | Author investigation without candidate list or raw timings | Retain account and explicit missing-method limit; cannot support superiority or a tail-latency guarantee. |
| 04 | 134 ns, 16-byte inline dispatch | Committed first-party benchmark baseline | Retain as recorded median, excluding module work; inspect measurement definition. No new benchmark claimed. |
| 05 | 117 ns; eight pinned runs of 5,000 emits; i7-14700K | First-party runtime measurement summarised in prior reporting record | Retain as reported median of per-run medians; distinguish enqueue from durable write and disclose missing local run logs. |
| 06 | 1,000 ns dispatch and audit ceilings | Baseline and merge-gate source audit | Retain as regression budgets, never maximum latency; locate revision supporting tightened values. |
| 07 | Go 1.24.4 cgo: 38–102 ns and 147–164 ns | First-party comparison reported in ledger; official benchmark source | Retain with direction and workload caveats; source code establishes fixture, not observed timing. No parity claim. |
| 08 | Repeated hops make latency matter | Author analysis | Retain briefly; state no hop-count or request-tail distribution was measured. |
| 09 | C over Rust; memory layout/lifetime and managed-runtime separation | Author design-decision account | Retain; invent no reason for choosing C over Rust or hard timing guarantee. |
| 10 | C and pure-Go clients, no cgo, conformance suite | Static source/document audit | Retain two-client scope; future language clients conditional. |
| 11 | Private queue pairs, one-time Unix attach, identity check, memfd/SCM_RIGHTS, read-only control | Static source/document audit | Retain and diagram; distinguish attach channel from normal data path. |
| 12 | Cooperative arena, trusted native code, fragmentation, 16 MiB limit | Static source/document audit | Retain limits together; correct opening's unqualified large-payload arena claim. |
| 13 | Process/runtime/failure separation | Static architecture plus inference | Retain isolation mechanism; qualify claim that a crash or pause cannot affect callers. |
| 14 | LMAX, virtio, io_uring, DPDK; Aeron and seL4 lineage | Author comparative source reading | Keep useful primary-source lineage; no comparative performance result. Preserve omitted name list in historical record. |
| 15 | Combination is novel within author's experience | Author judgement, no field survey | Preserve in record; omit from article because novelty is unnecessary to architectural argument. |
| 16 | Startup grants bind identity and serve/publish/request/subscribe; learning serves one kind | Static grant/runtime audit | Retain; scope to host-enforced bus reach. |
| 17 | Permanent module references and event-kind numbering | Static document audit | Retain non-reuse rule briefly. |
| 18 | Plugins inherit adapter authority; grant and extension review | Author analysis; adapter routing partly pending in historical record | Use conditional extension example; do not imply all MCP/pluggy routing shipped. |
| 19 | Compromise cannot widen grant; permitted replies can lie | Security analysis from static code | Retain with uncompromised-host and OS-authority conditions; no exploit test claimed. |
| 20 | Memory confidence, learning sink mask and governance fail closed | Static source/document audit | Retain concrete learning and memory cases; distinguish semantic policy from transport admission. |
| 21 | Coverage is supervised inter-module traffic; core-local/external exclusions | Static architecture audit | Move scope to opening; one bus per daemon, not one global cross-machine bus. |
| 22 | Model used unused node and testing API key over network | Author-reported self-learning incident, shared with part one | Retain with attribution and companion source; no new incident reproduction. |
| 23 | network-none container and curl deployment check | Sandbox documents/check specification | Retain as documented check, not a run performed in this pass. |
| 24 | One control socket, mediated tools, source mount, no credentials | Static source/document audit | Diagram network mediation; retain mount/process boundary and avoid literal 'only channel' guarantee. |
| 25 | HTTP proxy, one IP dial owner, seven registry entries, ports 80/443 | Static proxy source audit | Retain; verify client-facing Unix-socket detail before asserting package-manager compatibility. |
| 26 | DNS validation, numeric dial target, header removal, deadline/byte limit, private policy fields | Static proxy source audit | Retain mechanism; package-private visibility is not a security boundary against code in same package. |
| 27 | Hosted tools substituted; git mediation prerequisite | Tool configuration audit and author implementation account | Retain configuration scope; no all-provider containment test or universal compatibility claim. |
| 28 | Memory reduces egress over time | Author reasoning without longitudinal measurement | Retain as hypothesis and state failure condition; no measured decline. |
| 29 | Inspect actual network/mounts/env on start/resume; fail or unknown refuses; PR 2839 merged | Static source/document audit and recorded merge check | Retain as documented enforcement; separate source verification from runtime assurance. |
| 30 | delegate_sandbox false opt-out; configuration cannot widen reach | Configuration audit plus analysis | Retain opt-out beside containment; correct contradiction that no setting can give network access. |
| 31 | Transport, authentication modules, mTLS/bearer identity and downstream verification | Static source audit plus author architecture account | Retain scoped identity/policy separation; downstream verification conditional. |
| 32 | Sandbox grant serves four kinds, requests/publishes/subscribes none | Static grant audit | Retain as bus reach example; no full containment inference. |
| 33 | Tap before routing, sequence, blocked retry once, overflow, producer_reaped, control_lost | Static routing source audit | Retain and diagram; offering to tap is distinct from durable capture. |
| 34 | 5,000 audit intents, exactly once, zero drops, shutdown drain | Committed durability-test result | Retain fixture and shutdown scope; no all-event or abrupt-crash durability claim. |
| 35 | Metrics/logging consume full tap and can export it | Conflicting historical source audit and later prose | Resolve against pinned source; preserve prior result that capture is best-effort, pruned and abandoned on failure. Do not upgrade planned consumers to shipped paths. |
| 36 | WORM witness, atomic source/evidence transaction, Ed25519 checkpoints | Static runbook/code audit | Retain, define WORM and scope to witnessed events. |
| 37 | C close path and five SQL paths; fault injection, recovery, restart | First-party runtime validation report referenced by earlier rewrite inventory | Retain as reported validation with source location/limits; do not silently erase absent raw logs. |
| 38 | Local tampering versus coherent rewrite; off-host retained copies | Runbook audit and security analysis | Retain conditions; replace guaranteed severance timestamp with last retained observation. |
| 39 | Independent metrics increase forgery burden; retained overlap | Author analysis, no live forgery test | Retain only conditional comparison; no guaranteed reconstruction or exact incident boundary. |
| 40 | Separate server/KB processes, identities, buses, grants; one KB/many servers | Deployment document/source audit | Retain and diagram; distinct processes need not mean independent machines or failure domains. |
| 41 | No KB-to-server command client found; inbound plugins, read-only git requirement | Static negative audit plus author account | Retain 'audit found no' and search limit; no absolute inability to initiate harm. |
| 42 | Severing KB loses recall/storage/gates and leaves checkpoint/current context | Architecture consequence | Narrow: retained context remains; governed paths fail closed; no measured claim that attacker loses a usable agent. |
| 43 | Mutual checking, compromise requires both sides, server limited to one user | Security analysis without cross-verification procedure | Correct: separation permits reconciliation; one side can cause harm and reachable credentials affect scope. No automatic cross-audit or two-compromise requirement. |
| 44 | Four learning components stranded across service boundary | Shared first-party deployed test and build-graph review, part one | Retain engineering cost and link to original record; not independent replication. |
| 45 | No penetration test, formal proof, independent audit, forensic recovery, or measured on-call benefit | Reporting limits | State material security and performance limits in article; preserve remaining limits here. |

## Diagram plan

Use accessible, self-contained inline SVG, matching the site's existing
`sg-figure` convention. The site's Markdown renderer has no Mermaid integration.
Each diagram will include a caption and textual description. Diagrams describe
architecture and documented checks; they are not runtime traces or test results.
Cover the per-daemon bus, delegate egress, and the split between execution,
ordered capture and witnessed evidence. Record final source mapping below.

## Findings resolved in the edit

1. **The bus is intra-daemon.** `docs/EVENT_BUS.md` at `6bcc87e` explicitly
   assigns one host to each daemon and places server/KB communication on the
   authenticated `/v1` network surfaces. Figure 4 therefore has two buses and
   a network link, not one shared-memory bus spanning machines. Core-local
   calls remain outside the coverage in the lead.
2. **The baseline is stronger than the old ledger's attribution.** Commit
   `5b110b500bf936fa17ef966169ea24fb84de5716` contains both 1,000 ns ceilings
   and the 117 ns result, including the eight per-run medians. It supersedes
   the older 82 ns and 2,000/5,000 ns baseline at `6bcc87e`. All older numbers
   remain in `figures.md`. The dispatch reference has no CPU model attached in
   that baseline. The article no longer implies that its hardware is known to
   match the audit/cgo host. No benchmark was rerun.
3. **The cgo comparison had the wrong direction.** Go 1.24.4's
   `benchCgoCall` calls C from Go. The original sentence about what a C host
   pays to call Go is unsupported by that fixture. All previously reported
   timings remain in the article, identified as a comparison without attached
   run logs. They cannot establish workload parity or the cost of replacement.
4. **Capture is lossy and retained selectively.** The pinned bus document
   specifies 16-session retention, failure and prune records, and observational
   replay. The earlier historical note saying this was only future work is also
   stale by this pin: gap reporting and declared durability classes are present.
   The revised account follows the pinned document. The 5,000-row graceful
   shutdown invariant remains distinct from full-frame capture and crash safety.
5. **The witness transaction had been conflated.** The pinned witness runbook
   still describes a source event and its witness committing together. The
   more specific 25 August validation report documents the change: source
   mutation plus immutable outbox intent commit first; the separate worker's
   drain, chain append, witness and delivery acknowledgement commit later in
   their own transaction. The article and Figure 3 use that newer account.
   The live test exercises the memory-insertion path and worker recovery;
   the five SQL close sites are also checked structurally. The article does
   not claim five independently exercised SQL mutation scenarios.
6. **Proxy header stripping has a protocol limit.** At this pin the active
   handler is `server-go/modules/sandbox/proxy.go`, not the old delegates path
   recorded in `figures.md`. `parseProxyRequest` rewrites headers only for
   non-CONNECT requests; CONNECT enters the byte relay. Header stripping does
   not inspect encrypted HTTPS headers. Private fields constrain outside
   callers, not hostile code inside the package. Seven refers to allowlist
   entries, one of which is a wildcard, not seven possible hosts.
7. **Package-manager compatibility is not demonstrated.** The source establishes
   a server-side HTTP proxy handler over a Unix channel. It cannot establish
   the draft's claim that every ordinary package manager needs no adapter.
   The article preserves the proxy mechanism and identifies this limit.
8. **Service separation does not require two compromises for harm.** The
   previous conclusion exceeded its own examples of dishonest policy and memory.
   Either side can cause harm. Separate records allow comparison only if they
   remain available and sufficiently independent. No automatic mutual-audit
   routine or unusable-agent result is established by the reporting.
9. **A retained record does not date the compromise exactly.** The last retained
   event is an observation boundary. Capture/export failure can produce a gap;
   a gap alone cannot identify an attack, its time or later activity.
10. **The default-setting argument contradicted the opt-out.** The prose now
    distinguishes recall tuning from `delegate_sandbox: false`, which can
    change containment. It removes repeated reassurance about configuration.

## Source preservation and new artifacts

[Source audit collection](raw/source-audit-20260920T143044Z/collection.json)
records commands, exact commits, collection time, environment, outcomes and
SHA-256 hashes. These files are raw source snapshots, not raw benchmark output.
The Go fixture has a separate [collection record](raw/cgo-source-20260920/collection.json).
No original article artifact or historical ledger entry was removed or replaced.

The read-only source review used `git show <commit>:<path>` in the local aimee
repository. The two relevant pins are:

- `6bcc87ea73f4e39947a5bc101d4033403b0e2324`: architecture, capture,
  sandbox, proxy and worker validation.
- `5b110b500bf936fa17ef966169ea24fb84de5716`: tightened performance
  budgets and controlled audit-enqueue reference.

The remaining grant, process-topology and negative source-audit results retain
attribution to the original reporting. This pass did not simulate module
compromise, run containers, contact sources or replay the PostgreSQL tests.
The raw snapshot of the validation document preserves its existing test report;
it is not a newly collected run log.

Official Aeron media-driver and seL4 capability documentation were read for
architectural lineage. Go's pinned source was fetched to inspect call direction.
No third-party product is materially criticised, and no right-of-reply outreach
was made or claimed. General transport observations remain explicitly an
unpublished first-party investigation, without identifying or ranking a rival.

## Final diagram provenance

| Diagram | Source and scope | Interpretation limit |
|---|---|---|
| `bus-path.svg` | Pinned `docs/EVENT_BUS.md`, Ordering and delivery, Capture and replay, Trust boundary | One direction of the queue pair is shown. Tap invocation precedes routing; the capture sink can lose data. No latency or durability result is drawn. |
| `delegate-egress.svg` | Pinned `docs/DELEGATE_SANDBOX.md`; `server-go/modules/sandbox/proxy.go` and `proxy_policy.go` | Package path expanded, other tool handlers omitted. Worktree mount remains a data surface. Enabled posture only; no claim of an escape test. |
| `witness-chain.svg` | Pinned `docs/validation/memory-changeset-worm-seal-2026-08-25.md`; witness runbook for configured export | Two transactions with possible worker lag. Export/retention conditional. Does not depict bus capture as a memory witness. |
| `service-split.svg` | Pinned `docs/EVENT_BUS.md`; original deployment and negative KB source audit recorded in `figures.md` | One example server/KB pair. No automatic cross-verifier or mandatory physical separation implied. Dashed exports require actual configuration and retention. |

All diagrams have SVG titles and descriptions, captions with pinned source
links, and focusable horizontal scroll regions for small screens. Standalone
SVGs are generated from `build_diagrams.py`; the same SVG is embedded in the
article so the live site's existing Markdown/HTML path can render it without
Mermaid support or an asset-copy change.

## Verification and publication status

The mechanical voice gate passes. Four diagrams render through the site's
installed `marked` parser and SmoothGUI/site styles in Chromium 151.0.7922.34.
Desktop width is 1,000 px and mobile width is 390 px. Diagrams scroll within
342 px regions on mobile; the document itself does not overflow. All SVG text
bounds remain within the canvas. Light and dark theme screenshots were reviewed.
The first render check is preserved; its cramped capture-box labels were
shortened for the second render. This is editorial rendering validation,
not an aimee runtime test.

The prose/caption count, with inline code, SVG labels and link destinations
excluded consistently, is 5,336 before and approximately 3,050 after. The
architecture sequence remains cost, process boundary, grants, delegation,
observation, witness and the service split. Cuts target repetition, novelty
promotion and unsupported security conclusions; the inventory records what
happened to their evidence.

The article remains a draft. This pass does not promote it to September product
validation or certify a publication gate. Raw cgo timing logs, broader latency
measurements, all-provider containment and independent security validation are
still absent from the reporting and are not implied by these edits. The current
claims identify their first-party sources and scope. `REVIEW` and `PUBLISHED`
are unchanged; no publication or right-of-reply messages were sent.
