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
| `SCORE` | `src/modules/memory/memory_core_search_b.c`, `src/headers/memory.h` at `958af1c5` | 2026-08-25 |
| `SCOPE` | `src/modules/db2/c/memory_scope_query.{c,h}` at `958af1c5` | 2026-08-25 |
| `BENCH` | `docs/validation/evidence-lifecycle-acceptance.md`, `scripts/evidence-lifecycle-benchmark.sql` at `958af1c5` | 2026-08-25 |
| `LANES` | `src/modules/memory/memory_core_search_{b,c}.c`, `src/config_client_accessors_3.c` at `958af1c5` | 2026-08-25 |
| `ONTO` | `src/modules/kb-synthesis/kb_curator_drain.c`, `src/modules/db2/c/ontology_evolution.c`, `src/kb/http/kb_http_console.c`, `src/kb/kb_memory_facts.c` at `958af1c5` | 2026-08-25 |
| `PROMOTE` | `src/modules/kb-synthesis/kb_curator_promote.{c,h}`, `src/modules/memory/memory_core_tiers.c`, `src/modules/memory/memory_health.c` at `958af1c5` | 2026-08-25 |

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
| a sighting registers only after its fact commits; the count orders a review queue; activation is an authenticated decision | `AUDIT`, `ONTO` | **Corrected in draft, 2026-08-25, and this is a mechanism change rather than a misreading.** At `AUDIT`'s pin `1d36f8c1` the article's original description was accurate: `kb_curator_drain.c:843-870` ran a §7.2 auto-promote sweep at `KB_ONTO_PROMOTE_DEFAULT_THRESHOLD 3`, default-on via `kb_typed_facts_auto_promote_enabled = 1` (`config_kb_curator.c:75`), and skipped `other`/`unknown`/`misc`/`unspecified` in code. Commit `4e8c8fabc3` (2026-08-21, PR #2831) removed that block: "P7 deliberately removes the former count-based ontology promotion: activating a provisional relation is an authenticated governance decision, regardless of how often extraction observed it." The threshold macro survives but is dead, with one occurrence in `src/`. `db2_ontology_approve()` has one non-test caller, `console_typed_facts_relation()` behind `POST /v1/console/typed_facts/relation`, and it is unchanged at `origin/testing` on 2026-08-25. **The actor is a credential, not necessarily a human**, and the article says so: `db2_fact_actor_from_request(1, &actor)` accepts either an authenticated tenancy principal, to which the `require_operator` argument assigns operator rank at the call site, or a verifier-authenticated `console-admin` service scope. `docs/gen/api-v1.md` records the route as requiring a console-admin credential. An automation holding one can work the queue, so vocabulary growth can still be autonomous; what the mechanism requires is an activation attributable to a named actor, recorded via `db2_fact_graph_record_external_in_txn("ontology.approve", ...)` with actor and transport identity. Sighting counting itself is unchanged (`rel_types_store.c:325`), and facts on a provisional relation still commit as Class C. **PR #2831 is `LIFE` in this table**: the article cited that PR for the lifecycle section and did not carry its ontology change, so this passage was stale on the day it was written |
| catch-all predicates excluded by extractor instruction, not by a code guard | `ONTO` | **New in draft, 2026-08-25.** The `other`/`unknown`/`misc`/`unspecified` skip lived inside the removed auto-promote block. What remains is the extraction prompt at `kb_memory_facts.c:79`, instructing the model to emit a specific snake_case predicate and "NEVER a generic catch-all". The article carries this as one of its two named limits, and notes that an automation approving on a count alone restores the old sweep's behaviour without the guard it had |
| identity resolved before storage; names point at identities; merges recorded and reversible | `AUDIT` | |
| top twelve candidates, up to forty-eight canonical entity seeds, one score of thirteen summed parts | `AUDIT`, `SCORE` | **Corrected in draft, 2026-08-25, from "one fourteen-part score"**, carried from the earlier article, whose record cited a line range that no longer holds. The counting rule is the terms actually summed into `parts->total` in `memory_compute_score_parts()`: lexical, coverage, entity, temporal, evidence, semantic, state, intent, salience, surprise, pagerank, the weighted graph term, and outcome. `memory_score_parts_t` names more fields than that. `code_proximity` is a copy of `graph_score` when the expansion arrived via a code node, not a separate term, and `confidence` is populated after ranking for display, with a source comment saying it is "a calibration artifact, not a retrieval-relevance signal". The earlier article's own claim is not amended here; see its record |
| ranking weights fitted from feature rows and recorded outcomes; a new model lands as a proposal behind a benchmark gate | `AUDIT` | |
| lane floors for summaries and facts, gated by configuration | `LANES` | **Corrected in draft, 2026-08-25, then narrowed the same day.** An earlier version read "reserved slots keep summaries and facts from being crowded out", stated as unconditional recall behaviour. `memory_apply_lane_floor()` is called at `memory_core_search_c.c:929-932` inside `if (config_memory_recall_lanes_enabled())`, so the gating is certain. **The shipped default is not verified here and the draft claims none.** A first pass read `double value = 0` in that accessor as the default; it is the fallback when the key is absent from the served snapshot. `config_client_read_number()` reads a snapshot fetched over the transport from the config module, whose implementation is external to this repository (`src/modules/config/module.yaml` names `github.com/RakuenSoftware/aimee-module-config`), so no default for this key is readable from the aimee tree at this pin. `memory_recall_lanes_enabled` is one of the flags `docs/validation/flag-rollout-readiness.md` lists as still needing an A/B |
| typed facts were excluded from the graph walk, and the gravity table was dead at the fusion call site, which passed no relation and took the 0.45 unknown default for every edge | `TYPED`, `FUSION` | **shared** with part one. Two distinct defects; an earlier draft merged them into "co-occurrence at 0.45 drove recall". `MEMORY_GRAPH_GRAVITY_DEFAULT` is 0.45 and `co_discussed`'s own gravity is also 0.45, which is what made the conflation easy to miss |
| A 1.0, B 0.75, C 0.5, multiplying a semantic baseline of 0.80 | `FUSION` | **shared** with part one. `memory_graph_confidence_factor`; `MEMORY_GRAPH_GRAVITY_SEMANTIC` is 0.80. The class is a multiplier on gravity, not an alternative to it |
| three visibility bands, scope applied inside the query, stable sort within a band | `AUDIT`, `SCOPE` | **Corrected in draft, 2026-08-25.** An earlier version credited the exclusion to the ranking expression. `DB2_MEMORY_SCOPE_RANK_SQL` is the `CASE` used for ordering; `DB2_MEMORY_SCOPE_FILTER_SQL` is the separate `WHERE` predicate that drops out-of-band rows. Both bind through `db2_memory_scope_bind_current()` and are applied together in `memory_briefing.c`, `memory_relations.c` and `pgvec_transport.c` |
| five functional tiers: Experience, Observation, World, Mental Models, Patterns; a directive can require recorded operator approval | `TIERS` | Corrected from an earlier draft reading "from scratch at L0 ... to L5", which implied six tiers. `TIER_L0_NAME` and `TIER_L1_NAME` are both `"Experience"` and `memory_functional_tier_name()` collapses L0 and L1 |
| Experience occupies two storage levels, L0 and L1 | `TIERS` | distinct priorities from `memory_tier_priority()` (0 and 1) and their own promotion and expiry constants; five tiers, six levels |
| scope is orthogonal to tier and is never encoded as an extra tier | `TIERS` | stated in the header comment |
| three thresholds with differing units; two survive as counts, one became a governance decision | `AUDIT`, `PROMOTE`, `ONTO` | **Corrected in draft, 2026-08-25.** Pattern synthesis is called unconditionally from `memory_run_maintenance()` (`memory_health.c:380`), and the threshold is hardcoded in SQL: `db2_memory_promotion_l5_pattern_candidates()` selects `HAVING COUNT(DISTINCT p.session_id) >= 3` over L2 `fact`/`pattern` rows at `confidence >= 0.8` with no existing `synthesizes` link (`memory_promotion.c:407-430`). "Unconditional" is inside the maintenance run: the scheduled entry at `agent_runtime.c:1732` and `memory_maintenance_maybe_run()` are both gated on `config_memory_maintenance_enabled()`, whose default is likewise not readable here. The article says the pass runs inside the maintenance cycle and claims nothing about whether that cycle is on. Entity scope promotion at `CURATOR_PROMOTE_DEFAULT_MIN_SOURCES 3` (`kb_curator_promote.c:20`) is intact but gated on `kb_curator_promote_entity_enabled`. That it is **off by default rests on the header comment at `kb_curator_promote.h:11`**, not on a defaults table: config defaults are served by an external module (see the lane-floors row), so the article attributes the claim to the header rather than asserting it flat. Relation promotion at three sightings no longer exists; see the row above. The earlier stated limit, that the vocabulary counter does not record distinct sources, is retired rather than dropped: with activation now requiring an authenticated decision, a single participant repeating a relation to a count no longer promotes anything |
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
| the ledger at 812 bytes an event, one run, idle test container | `LIFE`, `BENCH` | **Corrected in draft, 2026-08-25.** An earlier version read "the ledger writes 10,000 events in 5.397 s at 812 bytes an event", which dropped every qualifier the source document carries and billed the batch's elapsed time to the ledger. The source states **one run on LXC 9078** and that "figures are measurements, not performance guarantees, and include local PostgreSQL transaction/trigger overhead in an otherwise idle test container". `evidence-lifecycle-benchmark.sql` times one bulk `INSERT` of 10,000 rows into `memories` and diffs `pg_total_relation_size('memory_evidence_events')`: the ledger rows are written by trigger, and the measurement is storage growth. The elapsed figure is not carried in the article. PostgreSQL 17 with pgvector, fresh Debian 13 LXC; the vector extension is not in this path |

## Draft revision, 2026-08-25

Checked against `testing` at `958af1c5`, prompted by an external review of the
draft. Six figures changed. Nothing here was published; these are corrections
to an unpublished draft, and the article's status is recorded in its README.
Each row above carries its own note, and the pattern across them is worth
stating once.

Five of the six are drift. The draft was written from source read on
2026-08-24 and from PRs merged in the days before it, and in that window the
tree moved under three of its claims. The score gained a term and lost two
that were never terms. Lane floors and entity-scope promotion are both intact
mechanisms the draft described as if they ran unasked, when each sits behind
its own switch.

The sixth is not drift and is worth separating. Count-based ontology promotion
was removed by PR #2831, which this record already cited as `LIFE` for the
evidence-lifecycle section. The change was in a source the draft had read. That
is a checking failure rather than a stale reading, caught before publication by
someone outside the project rather than by the drafting process, and the fix is
the one the review proposed: check each claim against a named symbol at a
pinned commit, rather than against a PR's summary.

The benchmark row is a seventh and different again: nothing moved, and the
qualifiers were dropped in the writing.

**A limit of this check, stated plainly.** Config defaults are not readable
from this repository. `src/modules/config/module.yaml` names
`github.com/RakuenSoftware/aimee-module-config` as the implementation, and the
`config_*` accessors here read a snapshot served over the transport rather than
a defaults table in-tree. Every claim above about whether a flag is *gated* is
read from a call site and is firm. Claims about what a flag *defaults to* are
not, and the draft avoids them except where a source comment states one and is
cited as the source. Before publication, any claim about a shipped default has
to be checked against the config module, not against an accessor's local
initialiser, which is a fallback and not a default.

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

## Self-learning measurements moved from part one, 2026-08-26

The article now carries the deployed **46 checks, 46 passed** result and the
paired outcome study previously reported in part one. The checks come from
`docs/validation/learning-loop-evidence-2026-08-25.md`. The paired study comes
from [Aimee PR #2859](https://github.com/RakuenSoftware/aimee/pull/2859),
including `docs/validation/self-learning-efficacy-2026-08-26.md`. Both valid raw
runs are preserved in part one's
[`evidence/raw/self-learning-efficacy-2026-08-26/`](../../aimee-recursive-self-learning/evidence/raw/self-learning-efficacy-2026-08-26/)
directory.

| figure in article | result |
|---|---:|
| deployed self-learning checks | 46/46 passed |
| repeated tasks without the learned failure record | 12/24 |
| repeated tasks with the learned failure record | 24/24 |
| novel tasks, both conditions | 12/24 |

The paired study used a fixed consumer. It isolates whether recalled failure
changes a later choice and does not measure model performance.

## Standalone opening pass, 2026-08-26

The opening now gives the concrete lifecycle operations before stating that
remembering is the learning. It no longer describes the claim as something the
first article failed to show. Three later cross-article references were replaced
with the mechanism or criterion they depended on. The first mechanism section
now introduces Classes A, B and C as a reference table before using them. No
figure, mechanism or limit changed.

## Project orientation, 2026-08-26

The opening project description records the author's 0.4.0 positioning: Aimee
is available with cloud or local hosting and provides self-learning memory from
one user to the models and users an entire company enrols. The series' identity,
scope, model-independence and audit arguments supply the mechanism behind that
product description; it introduces no new measurement.
