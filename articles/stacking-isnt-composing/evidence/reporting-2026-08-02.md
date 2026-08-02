# Reporting record: stacking rewrite

Date: 2026-08-02

Status: rewrite complete; publication correction included.

This file records the form, source audit, limits and publication decisions for
the rewritten article. It is not evidence that any add-on combination fails or
that `aimee` improves cost or quality.

## Form and interest

The article is reported analysis. The descriptions of current `aimee`
contracts come from a pinned public source revision. The distinction between
stacking and composition, and the replacement design brief, are Rakuen
Software's analysis.

Rakuen Software builds `aimee` and benefits if readers prefer integrated agent
architecture. The article discloses that interest next to the opening finding.
It also corrects the earlier use of `aimee` architecture as evidence that the
product produces a better outcome.

## Source revisions

### Original published article

- `rakuensoftware-web` commit
  [`92b41b47997b24879a279338f0ac1791ef203495`](https://github.com/RakuenSoftware/rakuensoftware-web/blob/92b41b47997b24879a279338f0ac1791ef203495/src/content/blog/stacking-isnt-composing.md),
  published 2026-07-24.

This is the contemporaneous record of the first-party observations and product
claims being corrected. The live article supplied no linked evidence folder.

### Reviewed `aimee` source

- `aimee` `origin/main` commit
  [`72234117fb4155103a59a484459fa902363e2715`](https://github.com/RakuenSoftware/aimee/tree/72234117fb4155103a59a484459fa902363e2715),
  reviewed 2026-08-02;
- [event-bus module
  contract](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/modules/bus.md);
- [event-bus working
  guide](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/EVENT_BUS.md);
- [economizer
  contract](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/features/economizer.md);
- [audit module
  contract](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/modules/audit.md);
- [gateway module
  contract](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/modules/gateway.md); and
- [memory module
  contract](https://github.com/RakuenSoftware/aimee/blob/72234117fb4155103a59a484459fa902363e2715/docs/modules/memory.md).

### Reviewed RTK and Headroom source

- RTK development README, commit
  [`e0ffd40ef7c450489aca4a50c0ab1358e4375691`](https://github.com/rtk-ai/rtk/blob/e0ffd40ef7c450489aca4a50c0ab1358e4375691/README.md#how-savings-work);
- RTK 0.43.0 source, commit
  [`5a7880d404db8364d602f2ecdc41dd790f64013f`](https://github.com/rtk-ai/rtk/tree/5a7880d404db8364d602f2ecdc41dd790f64013f);
- Headroom 0.33.0 source, commit
  [`6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9`](https://github.com/headroomlabs-ai/headroom/tree/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9);
- Headroom [prefix replay](https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/cache/prefix_tracker.py#L267-L368);
  and
- Headroom [retrieval continuation](https://github.com/headroomlabs-ai/headroom/blob/6d5516dcb878b6ffd139a1c7b3d480a1c8c1beb9/headroom/ccr/response_handler.py#L420-L529).

The full static audits are recorded in the sibling article's
[`reporting-2026-08-02.md`](../../token-compression-tools-cost-more-than-they-save/evidence/reporting-2026-08-02.md).
This article uses only the integration points established there.

The audit read committed objects with `git show origin/main:<path>`. The local
`aimee` working tree had unrelated changes and was not used as publication
evidence.

This was a static source and contract audit, not a live bus test, replay test,
billing comparison or full-system quality evaluation.

## Findings carried by the source audit

The event-bus contract supports these claims:

- per-source FIFO and host-stamped global accepted order;
- bounded backpressure declared by event kind;
- publish acceptance is not consumption or durability;
- one core full-stream tap and observational capture; and
- public C and pure-Go implementations with conformance checks.

The same contract assigns business schemas, workflow scheduling, WORM storage
and deterministic module execution replay to owners outside the bus core.

Those exclusions assign ownership. They do not remove the bus's control of
operation order. A scheduler decides which workflow operations to issue; the
bus host stamps their global accepted order before routing, and consumers
observe that order. FIFO delivery, bounded backpressure, typed absence and the
full-stream tap supply guarantees across stages that the scheduler does not.

The working guide says replay presents the accepted stream to an inspector. It
does not execute tools or drive modules. It also says the bus currently carries
observability and audit traffic, and that the extension path is not a claim
that every subsystem has moved.

That is current implementation status, not an architectural limitation. The
capture materialises the accepted frames and payloads in bus order. Combined
with audit, it provides the record from which deterministic execution replay
can be implemented as module replay contracts are added.

The bus working guide supports the architectural link: the full-stream tap
enables ordered capture, the observability bridge carries governed actions, and
consumers drain accepted events into durable audit sinks. The audit contract
owns the separate WORM guarantees: append-only triggers, a SHA-256 row chain
and keyed checkpoints. It also records the limits: legacy logging remains
authoritative, WORM dual-write is default-off and best-effort, and off-host
witnessing plus guaranteed filesystem immutability are not present.

The gateway contract assigns ownership of the canonical ordered request
pipeline. The stage contracts define operation meaning and ownership; the bus
provides the ordering and delivery guarantees that let those contracts compose.
It does not establish a measured cost or quality result.

The RTK source establishes its Bash-output rewrite boundary. The Headroom source
establishes its assembled-request, prefix-preservation and retrieval boundaries.
A semantic-memory add-on stores and recalls the view its host supplies. The
article's combined sequence is analysis from those boundaries: Headroom can
recover what reached Headroom, but it cannot restore detail an upstream RTK
rewrite already removed.

## Prior first-party work and corrections

The complete item-by-item disposition is in
[`first-party-reporting-2026-08-02.md`](first-party-reporting-2026-08-02.md).
The rewrite preserves the existence and limits of the original joint-tool
account. It distinguishes the unarchived cost and recall outcome from the
architectural finding that separately integrated add-ons have no guaranteed
shared order unless a host supplies one.

The rewrite keeps capture and WORM storage as distinct `aimee` subsystems while
describing the bus as the enabling seam for both. It treats full execution
replay as a capability built from that shared ordered record, not as a claim
invalidated by the current observational replay interface.

The absence of an archived joint-tool trace is recorded as a measurement limit,
not as a retraction of the composition finding.

No raw first-party runtime artifacts were found. No new runtime test was run for
this rewrite. The publication therefore makes no effect-size, frequency,
performance or full-system outcome claim.

## Right of reply

The rewrite does not publish a product-specific performance finding about
Headroom or RTK. It publishes the general architecture finding that separately
integrated add-ons have no guaranteed cross-tool order unless their host
provides one. No right-of-reply request is required for that general analysis.

If a later version restores a product-specific result, the project must receive
the exact proposed finding and a fair chance to answer before publication. The
request and response belong in this evidence directory.

## Publication gate

- The article carries no measured figure.
- Every current-source claim links to the pinned public revision.
- Every prior first-party observation and source claim has a recorded
  disposition.
- The correction is marked and dated in the article.
- The commercial interest is disclosed beside the finding.
- No material external criticism remains.

The article is ready to replace the live version after editorial review.
