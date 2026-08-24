# Reporting record and figure provenance

Every figure in
[`the-remembering-is-the-learning.md`](../article/the-remembering-is-the-learning.md),
and where it came from.

Part two of three. Part one is `articles/aimee-recursive-self-learning/`, part three
`articles/everything-crosses-one-transport/`. Figures shared with those pieces
are marked shared, and recorded in their records too, so one number is not
logged three times as if independently sourced.

## Provenance of this article

Most of the aimee mechanism described here was first reported in
`articles/your-memory-has-no-authority-model/`, a comparative piece pinned to
`testing` at `1d36f8c1`. That article's source audit and its fourteen-project
comparison are **not** carried here and are not superseded by this article; see
`## Disposition of the earlier article` below.

Sections carried over and re-verified against `testing` on 2026-08-24: classes
and extraction authority, correction policy and the two clocks, the write gate
and vocabulary growth, identity resolution and reversible merges, one recall and
one score, scope bands and tiers, distillation thresholds, and demotion by
attributed outcome.

Material new to this article and not in the earlier one: the scheduled lifecycle
as promotion and expiry, the five module seams and their per-seam failure
behaviour, required-core readiness, typed-fact admission to the recall walk with
its defects, the evidence and lifecycle layer, and the untrusted-evidence
boundary on recall.

## Sources

| key | document | read |
|---|---|---|
| `AUDIT` | `articles/your-memory-has-no-authority-model/evidence/source-audit-2026-08-20.md` | pinned `1d36f8c1` |
| `MEM` | `docs/modules/memory.md` on `testing` | 2026-08-24 |
| `AUTH` | PR #2828, memory write authority from authentication | merged 2026-08-21 |
| `TYPED` | PR #2824, typed facts in the recall walk and the scheduled lifecycle | merged 2026-08-20 |
| `LIFE` | PR #2831, evidence and lifecycle layer (P1-P9) | merged 2026-08-22 |
| `BUS` | `docs/EVENT_BUS.md` on `testing` | 2026-08-24 |
| `TIERS` | `src/headers/aimee.h`, `src/modules/memory/memory_core_tiers.c` on `testing` | 2026-08-24 |
| `FUSION` | `src/modules/memory/memory_graph_fusion.{c,h}` on `testing` | 2026-08-24 |

## Figures

| figure | source | note |
|---|---|---|
| three classes; extraction passes model authority as a constant; provenance stamped from the authenticated writer | `AUDIT`, `AUTH` | carried from the earlier article, re-verified |
| the extractor commits only when both endpoints occur in the source note | `AUDIT` | its stated limit is also carried: it does not catch a false relation between two present names |
| repetition buys durability, not authority | `AUDIT` | reinforcement can make a model inference durable and it stays Class B |
| weight normalisation rewrote confirmation counts, Class A 1 to 20 and Class C 2 to 100 | `TYPED` | **shared** with part one; observed live |
| the co-occurrence upsert landed on the same unique triple as a real assertion | `TYPED` | **shared** with part one; `idx_ee_unique_triple` is on the bare triple |
| correction policies: supersede, retire from matching, refuse quiet rewrites | `AUDIT` | |
| class-rank ordering on single-valued relations; an outranked write is dropped, not inserted alongside | `AUTH` | |
| retraction treats request authority as a ceiling; model-composed context text is forced to model authority | `AUDIT`, `AUTH` | a request body may lower authority, never raise it |
| the four places a write could claim user authority | `AUTH` | retraction body, typed-fact ingress, functional-relation supersede, `memory.delete` |
| valid time and transaction time | `AUDIT` | |
| seventeen shipped relationships; the live set is an extensible table with cardinality and endpoint rules | `AUDIT` | |
| a sighting registers only after its fact commits; three committed sightings promote a relation; catch-alls never qualify | `AUDIT` | |
| identity resolved before storage; names point at identities; merges recorded and reversible | `AUDIT` | |
| top twelve candidates, up to forty-eight canonical entity seeds, one fourteen-part score | `AUDIT` | |
| ranking weights fitted from feature rows and recorded outcomes; a new model lands as a proposal behind a benchmark gate | `AUDIT` | |
| typed facts were excluded from the graph walk, and the gravity table was dead at the fusion call site, which passed no relation and took the 0.45 unknown default for every edge | `TYPED`, `FUSION` | **shared** with part one. Two distinct defects; an earlier draft merged them into "co-occurrence at 0.45 drove recall". `MEMORY_GRAPH_GRAVITY_DEFAULT` is 0.45 and `co_discussed`'s own gravity is also 0.45, which is what made the conflation easy to miss |
| A 1.0, B 0.75, C 0.5, multiplying a semantic baseline of 0.80 | `FUSION` | **shared** with part one. `memory_graph_confidence_factor`; `MEMORY_GRAPH_GRAVITY_SEMANTIC` is 0.80. The class is a multiplier on gravity, not an alternative to it |
| three visibility bands, scope applied inside the query, stable sort within a band | `AUDIT` | |
| five functional tiers: Experience, Observation, World, Mental Models, Patterns; a directive can require recorded operator approval | `TIERS` | Corrected from an earlier draft reading "from scratch at L0 ... to L5", which implied six tiers. `TIER_L0_NAME` and `TIER_L1_NAME` are both `"Experience"` and `memory_functional_tier_name()` collapses L0 and L1 |
| Experience occupies two storage levels, L0 and L1 | `TIERS` | distinct priorities from `memory_tier_priority()` (0 and 1) and their own promotion and expiry constants; five tiers, six levels |
| scope is orthogonal to tier and is never encoded as an extra tier | `TIERS` | stated in the header comment |
| three thresholds with differing units; the vocabulary counter does not record distinct sources | `AUDIT` | the article carries that asymmetry as a stated limit |
| demotion reads a time-decayed window of attributed outcomes; the scorer's exclusion contract | `AUDIT` | paraphrased in the article, no longer quoted verbatim. The source wording is: "The scorer reads only attributed outcome evidence, not source tags, declared confidence, author id, or retrieval frequency." Check the paraphrase against it if the contract changes |
| under a floor of recorded outcomes the scorer declines to judge | `AUDIT` | |
| contradictions retain both claims, linked, with sources | `AUDIT` | |
| injected context is untrusted evidence, not authorization or executable instruction | `MEM` | |
| memory is required core; `runtime_toggle.supported` false; readiness needs storage and a compatible embedding dimension | `MEM` | |
| five seams: write gate `5890`, extract and retraction pre-scan `5889`, PII recall gate `5892`, confidence band `5893`, embedding `5891` | `MEM`, `BUS` | **shared** with part three. The memory grant serves **six** kinds; `5894` is command declaration rather than a decision, which is why the article says five decisions |
| four of the five are pure decisions whose provider is authoritative and never falls back locally | `MEM` | "a silent fallback lets a broken module look healthy". Corrected from an earlier draft applying this to all five |
| embedding is arranged differently: the module serves HTTP embedders behind its own breaker, program-based embedders stay in the host path by explicit contract | `MEM` | the module declines those commands rather than failing them |
| per-seam failure behaviour | `MEM` | write gate defers, extraction errors, PII fails closed, retraction scan does not retract |
| differential fixtures generated from the original implementation | `MEM` | |
| append-only evidence ledger, changesets with compensating revert, lifecycle states, purge receipts, derived staleness, scoped recall explanations | `LIFE` | P1, P2, P3, P4, P9 |
| 10,000 evidence-ledger events in 5.397 s at 812 bytes/event | `LIFE` | PostgreSQL 17 with pgvector, fresh Debian 13 LXC. Append-only row insertion; the vector extension is not in this path |

## Disposition of the earlier article

`articles/your-memory-has-no-authority-model/` contains first-party reporting
that this article does not carry and does not replace: a static source audit of
sixteen repositories read at pinned commits on 20 and 21 August 2026, three raw
collection artifacts, an editorial inventory, and a per-claim source map.

Under `articles/AGENTS.md` that reporting is append-only and cannot be dropped
because a later article reused part of the same subject. It keeps its folder,
its evidence and its raw artifacts.

**Decision still needed:** whether the fourteen-project comparison is published
as its own article or retired with a recorded disposition. Its right-of-reply
blocker travels with it either way, which is why splitting it lets this article
publish without waiting on other projects' replies.

## No comparative claim is made here

This article compares aimee to nothing. Every claim is about aimee's own
implementation, read from source. The earlier article's comparative findings,
including that mnem, Menhir and Graphify also join code and memory in one graph,
are neither repeated nor contradicted here.

## The default-store passage

Author's account of a deliberate engineering choice: PostgreSQL with
pgvectorscale as the default, a swappable vector-store module for anyone who
wants something else, and no claim that the default is fastest.

The passage now states this as an instance of a system-wide rule rather than a
storage decision, and asserts that the thresholds, class weights, lifecycle
clocks, tiers and scope bands in this article are all configurable constants.
**That list is the author's characterisation and is not enumerated against
source here.** The individual values are reported elsewhere in this record; that
each is operator-changeable is not separately verified.

**No benchmark against any named vector database appears or is implied**, and
none was run. The article concedes that a purpose-built vector store will beat
the default, possibly substantially. That concession is the point of the
passage and should not be edited into a hedge.

The passage asks for worst-case figures rather than dismissing vector-store
benchmarking. Its stated position is that a best-case number is the wrong end
of the distribution for this decision, and that stall behaviour, its triggers,
duration and frequency would be decision-relevant. It says outright that such
figures could change the choice. No published figure is cited or contested, and
no such measurement is offered here.

The passage does not claim speed is irrelevant. It states which number decides:
the worst case over the median, on the grounds that an uncharacterised tail is
what reaches a person and what wakes somebody. **No tail measurement of either
the default or any alternative is reported here**, and none was taken. The
comparison to the transport's committed ceiling is drawn to show it is one
criterion applied in two places, not to import that measurement into this one.

The passage closes by stating the criterion as the authors' own rather than as
a general result, and support for a replacement vector store follows from that
rather than being offered as a concession. Recorded because it is the author's
stated position on end-user choice: a user who wants a purpose-built vector
database is making a legitimate engineering decision and the project backs it.

The article says **pgvectorscale** because that is what 0.4.0 moves to. The
reports ran on **pgvector 0.8.0** because that is what existed when they ran.
Both are correct and neither is at issue: no figure in this article is a
vector-search measurement.

The claim that memory has been "battle-tested in production across entire teams"
is the author's and carries no figures here.

Shared with part three, which generalises this into a standing position on
defaults and the configuration surface as a whole:
`articles/everything-crosses-one-transport/evidence/figures.md`, "The
defaults-and-configurability passage". The reasoning is one claim reported in
two places, not two independent sources for it.

## The provenance-of-design claim

The article states that the constraints described came out of running aimee in
production rather than from reasoning in advance: the thresholds, class
ordering, reversible merge and outcome-only demotion.

That is the author's account of how the design arrived, given directly. No
incident record or decision log is cited for each constraint. Two of the cases
are corroborated in the article by defects that are documented in the aimee
repository (the gravity default at the fusion call site and the
confirmation-count rewrite, both `TYPED`), but the general claim about design
provenance rests on the author's word.

The accompanying judgement — that a system with fast, bad memory is worse than
one with no memory — is argument, signed in the first person, and carries no
figures.

## Limits stated in the article

- The extractor's endpoint check does not catch a false relation drawn between
  two names genuinely present in the note.
- The vocabulary-promotion counter does not require distinct sources, so one
  participant can reach the threshold alone.

Both are carried from the earlier article's own reporting rather than
discovered here, and neither is fixed in this release.
