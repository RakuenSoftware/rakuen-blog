---
title: "Agent memory needs an authority model"
date: 2026-08-20
author: Rakuen Software
tags: [memory, agents, knowledge-graph, ontology, aimee]
excerpt: "I compared thirteen inspectable agent-memory implementations at pinned commits, plus one packaged engine whose source I could not audit. mnem and Menhir overturn the broad code-plus-memory uniqueness claim. Menhir also proves that authority-aware memory exists. The remaining question is whether authority, source, time and code structure meet on the default write and recall paths."
---

*Drafted 2026-08-20; comparison expanded 2026-08-21. Rakuen builds aimee, one
of the thirteen inspectable systems compared here, and benefits if readers
prefer its design. The named projects have not yet had a chance to respond. The
audit is recorded in
[evidence/source-audit-2026-08-20.md](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/your-memory-has-no-authority-model/evidence/source-audit-2026-08-20.md),
with a per-claim source map in
[evidence/figures.md](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/your-memory-has-no-authority-model/evidence/figures.md).*

*Implementation note, 21 August 2026. The `aimee` sections describe `testing`
at `1d36f8c1`. I read the pinned source and its validation record but did not
rerun the tests.*

Long context can remove the retrieval problem from agent memory. Put the whole
conversation in the window and no old turn has to be found.

What a window cannot do is decide which of two contradictory facts is true,
refuse to let a model's guess overwrite a person's statement, or tell you what
it believed last week. Those are properties of a write path, and a context
window does not have one.

On 20 and 21 August 2026, I traced the write paths of thirteen publicly
inspectable memory implementations at pinned commits and read A-MEM separately
as a research reference. I also read Supermemory's public repository and
self-hosting documentation, but its memory engine is distributed as a packaged
server binary rather than as source in that repository. I do not count it as a
negative result.

The expanded set changed the article. Hindsight and MemOS have substantially
more provenance, lifecycle and correction machinery than the original table
showed. mnem puts code, documents and conversations into one versioned graph.
Menhir goes further: it joins a structural code graph to semantic memory,
retains source receipts and superseded history, separates user-grounded claims
from agent inference at admission, and reserves promoted ground truth for an
operator.

The useful claim is therefore not that agent memory has no authority model.
Some does. The question is whether the authority distinction is stored,
enforced on every correction path, and used by the recall path that runs by
default.

`aimee` is a general-purpose memory service for an organisation. It puts facts,
conversations, documents and code in one graph ranked by one query.

Its core goal is to let any part of an organisation reach any other. Legal can
follow a policy into engineering; finance can follow a cost decision into
operations. A question can then follow the documents and discussions that
produced a decision to the code running now. The answer can show how the
organisation got there and cite the exact behaviour it implements.

mnem and Menhir both provide code-to-memory paths. Menhir is the direct
counterexample: its structural and semantic entities share one Neo4j graph, and
its blast-radius query can return affected code, tests and related memories.
What remains distinctive in this audit is a narrower conjunction of source
documents, a native code graph, endpoint-kind validation and per-fact assertion
authority. At the current `testing` pin, `aimee` enforces that authority on its
typed-fact correction paths.

The graph also distils what separate people and sessions corroborate. That
reach is why its design puts rules on the write path: a bad edge changes what
later queries can find and can influence later distillation.

It is an opinionated system. Take this for what it is worth.

## One recall, one score

Lexical matching and dense vectors produce the first candidates. The top twelve
supply up to forty-eight canonical entities as seeds. Expansion collects the
memories attached to each seed, then follows its direct neighbours using the
relation and authority class of each edge.

The graph adds memories that both lexical and vector search missed. A question
can share no words with its answer if an entity connects the two.

One fourteen-part score ranks the result, including lexical and dense match,
graph and code proximity, confidence, evidence, time and query intent. A typed
fact, a conversation from March and a function edited last week compete on the
same scale.

Reserved slots keep summaries and facts from being crowded out. The winners
pull in neighbouring turns, then scope removes anything the caller cannot see.

The weights are fitted from feature rows and recorded retrieval outcomes. A new
ranking model lands as a proposal until a benchmark gate promotes it. Shadow
evaluation can record per-query rank and score changes between fused and
unfused ranking over real traffic, without retaining the payloads. It is an
evaluation harness, not a production path.

## Code was the beginning. General memory lets it reach the real world

Before it was `aimee`, it was `aimem`: a code graph with a small fact memory,
built about a year ago to solve a production need. It was not an R&D project.
Engineers used it on live work, and what failed for them determined what we
built next.

Every expansion of memory since has come from that production loop. The users
have been demanding and the code has had to survive their workloads.
Tree-sitter extractors put symbols, calls, imports and git co-change into the
graph, and memory grew on top of it. Code still lives in the same edge table as
conversational memory: files, symbols, routes and projects use prefixed keys in
the same namespace.

That origin no longer bounds the product. `aimee` is general-purpose memory for
an organisation, not a code-memory tool. That breadth is what makes its code
graph different: a function can point at the contract, policy decision or
operational consequence behind it. A team with no code question can still use
the same facts, documents, conversations and reminders under its own scope.

That lets a prose question reach code. A question about a pool wedging under
load can find the conversations that mention it, cross into the symbols and
return the retry function. Starting from the function can recover the thread
where its policy was decided. A per-node gate keeps queries with no code-shaped
token out of the call graph.

Cross-repository links need more care. Names collide, vendored copies duplicate
them, and an untrusted repository can plant an export. Each link carries a
confidence tier and the evidence behind it.

Top-tier links need a trusted import resolution or an exported symbol used at
three call sites across three files. A lone call site stays tentative and out of
default output. Several possible definers or a collision goes to review.
Untrusted repositories cannot vouch themselves into the top tier.

Code also has its own clock. Every projected edge belongs to a generation, and
each project exposes one generation at a time. Publishing a new projection
swaps pending for visible and marks the old one superseded.

A traversal sees one state of the tree. Old and new symbols never mix.

## A contract, the decision behind it, and the code running now

Documents enter the same graph. Office formats go through a converter. PDF
extraction keeps page coordinates, reading order, table cells, optical character
recognition and the confidence of each layer. A citation names the document
hash, page and bounding box.

The full text remains the primary evidence. Each fragment records its source
path, whole-file hash, heading path and line span, with links to its neighbours
in reading order. A retrieved clause can recover the section that qualified it.

A conversation can enter through the same path. The code shows what was
decided; the thread may be the only record of why.

Together those sources give a decision a history. The document states the
obligation, the thread records why a policy was chosen, and prior versions show
what changed. The current code projection shows the implementation the graph
treats as live, down to the cited line.

Whatever goes in is mined for the entities it mentions, each resolved against
the canonical entities already known by searching up the scope lattice from
project to workspace to global. A narrow mention lands on the broad entity that
exists. Uncertain matches go to a judge. Code units resolve onto the same
entities, so document to entity to code becomes a graph traversal.

A clause in a signed agreement and the function that enforces it are two hops
apart. One answer can name the required retention period, the job that deletes
the rows, and a citation on each side.

The person asking does not need the symbol name or repository. A compliance
officer can ask in the language of the contract and receive both sources.

## Scope ranks inside the query

Memory shares one graph. Query-time scope separates projects and workspaces.

A recall carries the caller's active project and workspace. Active-project
memory gets the first visibility band, the workspace gets the second, and
shared or global memory gets the third. Anything else scores zero.

The database query receives that ranking as parameters. A later filter would
leak through timing and through which candidates reached the scorer. Scope must
take effect inside retrieval.

A stable sort preserves relevance inside each visibility band. The result is the
best match the caller may see, with no signal that a stronger hidden match
exists.

Underneath that runs a second axis: how settled a memory is, from scratch at L0
through durable fact at L2 to policy at L4 and synthesised pattern at L5. A
memory climbs through evidence. Policy can require a recorded operator approval
because it changes future work.

Tier records how settled a memory is. Scope records where it may appear.

## A team's memory, distilled out of work nobody filed

The design goal is refinement under use. Something one engineer established can
climb out of its original scope after independent work corroborates it. Nobody
has to file or curate it.

Three is the default threshold in three places, but the units differ. A durable
fact seen in three distinct sessions can become a pattern. An entity
corroborated by three distinct sources can move out of local scope. A novel
relation joins the vocabulary after three committed sightings.

That last counter does not record distinct sources. One participant can repeat
a relation to the threshold. The fact still enters as speculation, but the
vocabulary promotion is weaker evidence than the other two paths.

Months later, somebody who never spoke to the first engineer can receive an
answer carrying what that work established.

The loop closes on the other side. Demotion runs on verdicts attributed across
everyone's recalls. A shared memory that keeps failing in practice sinks.

## Prospective memory waits for its trigger

A prospective memory is a reminder with a trigger, an action, an anchor and a
recurrence. It sits armed, and context assembly checks the current turn against
the set before answering. An entity or file can anchor it, so the reminder does
not need a date.

The store raises the reminder when somebody touches its subject. The person does
not first have to remember that a note exists.

## Fusion raises the cost of a bad write

A wrong fact in an isolated fact store harms queries that retrieve it. In a
fused graph, an edge changes what the walk reaches and what enters the ranking,
including queries that mention neither endpoint. On a shared deployment, later
sessions can also carry it into pattern synthesis. A bad write can spread.

## Fact extraction does not grant model authority

Every fact is born into one of three classes. The asserted authority and the
write-gate verdict choose the class, not how sure anyone sounds.

Say something yourself through a relation the system understands and the fact is
Class A. It carries full confidence and is exempt from expiry. A background
extraction can reach Class B. Novel relations and other unconfirmed claims begin
in Class C.

The extraction path has no route from model authority to Class A. The extractor
passes model authority as a constant, so a fact-extraction prompt cannot claim
the user's class. Stored-note provenance is also stamped from the authenticated
writer and defaults to agent-authored rather than user-stated.

The extractor ignores the model's self-reported confidence. It commits only
when both endpoints occur in the source note. That catches invented endpoints,
but not a false relation between two names that are present.

A new relation remains speculation even when a person asserted it. The
unsettled part is the vocabulary, and personal authority cannot settle that.

Reinforcement can make a model inference durable, but it stays Class B.
Unconfirmed speculation runs out its clock and is stamped as no longer
believed. Repetition buys durability. It does not buy authority.

## Correcting a fact leaves the old one where it is

Each relation carries its correction policy. Most supersede: stamp the old value
and write the new one beside it. Some retire a stale value from matching while
keeping its row. Others refuse quiet rewrites.

A person can still supersede a protected value. `facts.retract` treats the
request's authority as a ceiling: user authority is granted only when the
transport attested a person, and the knowledge service repeats the check against
its authenticated actor. Model-composed context-block text is forced to model
authority even when its surrounding turn belongs to a user.

The ordinary commit path applies the same ordering. If a model extracts a
different object for a single-valued relation, the write first compares the old
and new classes. A Class B `works_for` write cannot supersede a current Class A
value or sit beside it. A user write can replace a model value, and equal-ranked
writes retain the relation's ordinary correction policy.

The retained rows carry two clocks. Valid time records when the fact held in the
world. Transaction time records when the system believed it. "What was true
last year" and "what did you believe last week" become different queries.

## The write gate rejects the wrong kinds, and the vocabulary can grow

Facts are triples, and each kind of relationship declares what may sit on
either end of it. Employment joins a person to an organisation, an address
joins a device to an address. The write gate looks up the relation and checks
both ends. If the model says the printer works for the kernel, the commit stops
before writing a row.

Seventeen relationships ship with the system so a fresh install can validate
before it has learned anything. The live set sits in a table the running system
can extend, with cardinality and endpoint rules attached to each relation.

A relation the system has never seen enters as speculation. A provisional entry
gives the fact somewhere to attach, and the sighting is counted.

A sighting registers only after its fact commits. Failed writes do not raise the
candidate's standing, and a rejected relation keeps that verdict.

Three committed sightings let the maintenance pass promote the relation.
Catch-alls such as `misc` never qualify because they cannot later reconcile to a
specific relationship.

A person may also teach a domain from its documentation before evidence has
accumulated. That is the human path into the vocabulary.

## Two spellings of a name are one thing, and a bad guess is reversible

The graph walk starts from the entities a candidate mentions. Split one person
across three nodes and the walk loses paths.

The ends of a fact are resolved to an identity before the fact is stored. Names
point at that identity, never at other names. Values such as an address or age
bypass the identity register.

Every completed merge is recorded and reversible. A name with several plausible
owners goes to a queue with bounded retries. It blocks neither write nor recall.

## Demotion reads outcomes, not popularity

Each recall records the memories placed in front of the model. Memories that
shaped the answer receive an outcome: accepted, corrected, contradicted, rolled
back or beside the point.

Demotion reads a time-decayed window of those outcomes. Its contract excludes
everything else:

```text
The scorer reads only attributed outcome evidence — not source tags, declared
confidence, author id, or retrieval frequency.
```

A frequently retrieved memory that keeps failing sinks. Independent sources
asserting the same thing still count as corroboration. Retrieval frequency is a
property of ranking; source count is evidence about the claim.

Under a floor of recorded outcomes the scorer declines to judge at all and says
so.

Contradictions are not resolved by picking a winner. Both claims stay, linked,
with their sources intact. Policy chooses the current value. Unresolved
conflicts join a backlog with stale facts and topics that have thin coverage.

## Ten of thirteen do not connect memory and code in one graph

Every cell was read from the project's own source at the commit named, on 20 or
21 August 2026. "Authority" means an enforced distinction between a person's
assertion and a model inference, not confidence, content type or message role.
"Typed gate" means that a relation with the wrong endpoint kinds is refused a
row. The final column says what disappears from current recall and what
survives. The audit file carries the complete tests and source lines.

| system | commit | memory and code in one graph | retrieved fact reaches source | typed endpoint gate | assertion authority | valid time | correction or removal path |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `aimee` | `testing` `1d36f8c1` | yes, native code graph | hash, span, heading, neighbours | yes | A / B / C; authority derived from authenticated actor | yes, plus code generations | retained supersession; lower-authority correction refused |
| Graphiti (Zep) | `c4069327` | graph, no native code model | raw episode kept | no | none | yes | expired edge retained |
| cognee | `fd5045f6` | graph plus vector, no native code model | chunk to document to path | optional enrichment only | none | edge `updated_at` only | tagged edge retained |
| mem0 OSS | `3599aa75` | no; graph removed | messages kept, memory lacks link | no | none | no | v3 extraction is ADD-only |
| Letta Code | `d1dc6880` | no | block history in git | no | none | no | model rewrites block; git retains history |
| LangMem | `29cbe41e` | no | no document model | no | none | no | model tool hard-deletes |
| Memobase | `358c16bb` | no | blobs kept, slots lack link | slot schema, not relation kinds | none | no | model rewrites slot |
| Hindsight | `3de41af8` | hybrid memory graph, no native code model | fact to document and original text | no | world / experience are content types, not authority | yes, occurred start / end | invalidation archives; MCP document delete permanently removes linked facts |
| MemOS | `be68e2fb` | graph plus vector, no native code structure | source snippet or locator; versions retained | no | provenance and confidence, no assertion rank | event metadata, no general valid interval | MCP delete reaches hard `DETACH DELETE` |
| mnem | `2a8a3698` | yes, code, documents and conversations | chunk to document with source offsets | schema tree exists; endpoint validation not implemented | author / agent provenance, no assertion rank | no | MCP tombstone hides current fact; history is reversible |
| Menhir | `4e4f39ed` | yes, structural code and semantic memory | episode, evidence span and code anchors | yes for work-artifact links; not extracted memory edges | user-grounded vs agent inference; candidate / persistent / promoted | yes | delete requires operator tier; superseded history retained |
| Neo4j Agent Memory | `5b4e00af` | graph memory, no native code model | entities link to messages; direct fact tool does not set source | no | explicit / inferred share confidence field | yes, `valid_from` / `valid_until` | preference supersession retained; no delete in shipped MCP tools |
| Memori | `538b61f2` | facts and triples, no native code model | fact-mention link to conversation | no | source / signal taxonomy, no enforced rank | no | host API hard-deletes entity memory; agent tool is read-only |

Within the original seven-system set, Graphiti was the closest architecture. It
is bitemporal and keeps contradicted edges as expired rows
([`edges.py`](https://github.com/getzep/graphiti/blob/c406932767ee490ad2311fd694a6b2ac3b164599/graphiti_core/edges.py#L262-L283)). Custom edge types exist,
but they control what definitions the extraction prompt sees.

The write path does not check the returned relation against those definitions.
Its edge has no confidence, provenance or authority field.

cognee's conflict resolver keeps superseded edges. Its docstring also states why
correction policy cannot be generic:

```text
Nothing is applied automatically: the caller names the relationships that are
single-valued. Most cognee relationships (``knows``, ``mentions``, ...) are
legitimately many-valued and must never be collapsed, and there is no
cardinality metadata to tell them apart.
```

The quote comes from
[`temporal_conflict_resolver.py`](https://github.com/topoteretes/cognee/blob/fd5045f6b60522c1953fc1ae258e041ba53602d8/cognee/modules/graph/utils/temporal_conflict_resolver.py#L13-L16).
Cardinality metadata lets a relation carry that policy in the store. cognee
ships ontology support but defaults to no ontology file, with contradiction
detection off
([`config.py`](https://github.com/topoteretes/cognee/blob/fd5045f6b60522c1953fc1ae258e041ba53602d8/cognee/modules/cognify/config.py#L13-L17)).

mem0 removed graph memory from its open-source release: "Graph memory is removed
from OSS. It's a built-in, always-on Mem0 Platform feature"
([`oss-v2-to-v3.mdx`](https://github.com/mem0ai/mem0/blob/3599aa75ed64ee41c3b1d8133a8b39403fb8f703/docs/migration/oss-v2-to-v3.mdx#L41)). The same
release made extraction ADD-only, removing the old model-selected deletion path.
Contradictory memories now accumulate without reconciliation.

Letta stores memory as a block the agent can rewrite
([`toolset.ts`](https://github.com/letta-ai/letta-code/blob/d1dc6880971dc55a5e5dfcf845d4cba740b14585/src/tools/toolset.ts#L61-L68)). MemFS tracks every block in git,
so the old content survives in a commit. The block still has no field
separating user text from model text.

LangMem is the plainest case in the set. `create_manage_memory_tool` permits
`delete` by default and the branch is one line,
`store.delete(namespace, key=str(id))`
([`tools.py`](https://github.com/langchain-ai/langmem/blob/29cbe41e58528f92e9efa773c12e15c47be3808c/src/langmem/knowledge/tools.py#L327-L328)), with no history
row or check on what is removed.

Memobase has the closest thing here to an ontology, in topic and subtopic
profile slots. An LLM chooses to append, update or abort. Update rewrites the
slot text.

Source retention is more common than the usual criticism allows. Graphiti keeps
the raw episode, mem0 writes every message to a table and Letta has git history.
In the original seven-system set, the missing part was usually a path from the
retrieved fragment back to that source. cognee came closest: a chunk names its
document, and the document names a filesystem path.

The added systems make that last paragraph less bleak. Hindsight is presented
as a persistent MCP agent-memory product, not a research prototype, and its
recall combines semantic, keyword, graph and temporal strategies
([product guide](https://github.com/vectorize-io/hindsight/blob/3de41af867582c810309d6ea4c1b1de9d0ed9b7e/hindsight-docs/blog/2026-03-04-mcp-agent-memory.md#the-approach)).
It stores the original document and gives each memory unit a `document_id`.
Invalidating a fact moves it out of recall, consolidation and the graph, but
into a reversible archive rather than oblivion
([migration](https://github.com/vectorize-io/hindsight/blob/3de41af867582c810309d6ea4c1b1de9d0ed9b7e/hindsight-api-slim/hindsight_api/alembic/versions/c9a1b2d3e4f5_add_invalidated_memory_units.py#L1-L26)).
Its world facts, experiences, observations and mental models are meaningful
memory types. They do not say whether a person asserted a fact or a model
inferred it. The gentler fact-level path is not the whole deletion story:
Hindsight also exposes an MCP `delete_document` tool that permanently removes
the document and every memory linked to it
([`mcp_tools.py`](https://github.com/vectorize-io/hindsight/blob/3de41af867582c810309d6ea4c1b1de9d0ed9b7e/hindsight-api-slim/hindsight_api/mcp_tools.py#L3742-L3803)).

MemOS deserves similar precision. Its public model stores source roles,
message IDs, document paths and archived versions
([`item.py`](https://github.com/MemTensor/MemOS/blob/be68e2fb5370866bd5e2b188bb3d22bd13b49e09/src/memos/memories/textual/item.py#L16-L92)).
That is provenance and recoverable history. It is not an authority ranking,
and the shipped MCP delete path reaches a hard graph delete.
The architecture introduction's `MemLifecycle` and `MemGovernance` claims are
broader than the like-for-like modules I could locate in the public core, so I
credit the implemented metadata and history rather than treating every
architecture label as a runtime guarantee.

mnem falsifies the original code-plus-memory claim. Its ingest path accepts
source code, documents and conversation exports, links chunks back to document
nodes, and commits snapshots of the node, edge and schema trees. Those snapshots
can branch, diff, merge and roll back. A tombstone
removes a fact from current retrieval while the prior commit remains available
([README](https://github.com/Uranid/mnem/blob/2a8a36985dbcf107378a76daeeef7154691220e7/README.md#L23-L31)).
It does not yet validate candidate edge endpoints against its schema tree, and
its author, agent and task fields are commit provenance rather than a rank on
each assertion.

Menhir is the stronger counterexample. Its structural and semantic entities
share one Neo4j graph
([README](https://github.com/Archolith/menhir/blob/4e4f39ed388a1c689740a7d48daade9fbc79c000/README.md#L24-L58)).
A claim that declares itself user-sourced must be grounded in retained turn
evidence or it is downgraded to `agent_inference`. Candidate memories stay out
of recall until review, and only an operator can promote persistent memory to
verified ground truth or invoke deletion. This is an authority model. Its
remaining caveat is deployment state: scalar-state and event-history recall
authority are shipped but default-off, so those derived views do not yet govern
the ordinary recall path by default.

Neo4j Agent Memory and Memori broaden the production set without changing that
conclusion. Neo4j Agent Memory carries `valid_from`, `valid_until` and source IDs,
but its MCP fact tool accepts arbitrary subject, predicate and object strings
with one confidence field. Memori links facts to the conversations that mention
them, but its source and signal taxonomy classifies memory content rather than
ranking who may overrule whom.

Supermemory does not receive a row. Its documentation says inferred memories
carry `isInference: true`, rank below stated facts and can enter a review queue
([memory review](https://github.com/supermemoryai/supermemory/blob/34876664810a43a55954a0a83571662a3bd333b8/apps/docs/recall/memory-review.mdx#L8-L36)).
That would overlap this article's authority test. The self-hosting path,
however, downloads `supermemory-server` as a release binary; the repository
contains the documentation, clients and MCP layer, not the engine that
implements those fields
([self-hosting quickstart](https://github.com/supermemoryai/supermemory/blob/34876664810a43a55954a0a83571662a3bd333b8/apps/docs/self-hosting/quickstart.mdx#L28-L58)).
I cannot turn an unauditable implementation into either a yes or a no.
The docs also describe AST-aware code chunking, but do not establish from
inspectable engine source that code structure and temporal memory occupy one
traversable graph.

A-MEM (`ceffb860`) sits outside the table because it is a research implementation.
The open-source field also includes retired servers and features moved to
hosted tiers. The table describes only the pinned source a reader can inspect,
not the hosted products behind mem0, Zep or Letta.

## The narrower claim this audit supports

Of the thirteen inspectable implementations in the table, `aimee` is the only
one I found that combines all four of these in one store: a native call and
import graph, a path from a retrieved document fragment to its source, an
endpoint-kind gate for semantic relations, and a stored user-versus-model
authority class. Menhir has the native code graph, provenance and assertion
authority, and an endpoint-kind gate for work-artifact links, but not for the
general extracted semantic-memory graph. mnem has the fused,
versioned graph, but not per-assertion authority.

That is a claim about this search set, not the field. Supermemory is outside the
set because the engine source was not available in the repository I inspected.
A single inspectable implementation holding the same conjunction would settle
it.

The current `testing` source enforces the claim: retraction authority is capped
by transport and actor authentication, and functional corrections compare
class rank before changing the current value. The repository's validation
exercised the plain loopback and PostgreSQL paths; its live mTLS actor branch
remains a stated test limit.

## What this design costs

A vocabulary that is wrong rejects facts that are true. Seventeen relations is
a small seed. On a fresh corpus, novel facts land as speculation and need three
committed sightings to promote their relation. A true fact stated once in an
untaught domain expires.

Retaining fact rows has a price too. The edge table grows with every correction,
and a store running for a year carries every value each fact has held.
Superseded rows still occupy disk.

Recall abstention exists and is default-off with its threshold uncalibrated,
because calibrating it needs labelled ask-outcome data nobody has collected. I
would rather say that than ship a threshold I guessed.

## Who this is not for

Choose first between a library and a system. mem0 and LangMem run inside your
process. If that is the shape you want, use one of them. `aimee` is an AGPL-3.0
server.

Setup is clone, `docker compose up`, then a seven-step wizard that provisions
the store and selects the embedder. Graphiti asks for a Neo4j, FalkorDB or
Neptune cluster first. Both are a different commitment from `pip install`.

As of 20 August 2026, there is no hosted `aimee` tier. Mem0, Zep and Letta will
operate their systems for you. If you do not want to run a database, use one of
those.

If the memory holds preferences that are cheap to get wrong, this machinery is
not worth its cost. The next turn can correct a mild annoyance.

The argument starts to bind when a remembered fact drives an action, and it
binds harder when memory and code are the same question. A device address, a
policy decision, an on-call owner, the reason a function is written the way it
is.

## Go and check your own

Four checks to run against whatever memory system you have. mnem and Menhir now
pass the last one, which is why the original article had to change.

Open the schema for a stored fact and look for a field recording who asserted
it, distinct from the model that wrote it down. If there is no such column, the
distinction does not exist at runtime, whatever the prompt says.

Follow the delete path from the model's tool surface and see what survives it.
A history table is worth having. A tombstone the recall path walks past is
worth more, because the fact is still in the graph.

Try to write the two queries "what did you believe last week" and "what was
true last year" against different columns. If they are the same query,
corrections are overwrites and you cannot audit one.

Then ask it something in plain prose whose answer is a function, and see
whether the function comes back. If your memory and your code index are
separate services, you already know the answer, and no amount of context window
fixes it.
