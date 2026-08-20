---
title: "Your agent's memory has no authority model"
date: 2026-08-20
author: Rakuen Software
tags: [memory, agents, knowledge-graph, ontology, aimee]
excerpt: "Seven publicly available memory systems, investigated at a pinned commit. Six keep their stores in separate piles and let a model's guess overwrite what a person said. One graph that distils what a team corroborates, and a write path strict enough to deserve one, is a different design."
---

*Published 2026-08-20. Rakuen builds aimee, one of the seven systems audited
here, and benefits if readers prefer its design. Every claim below is a
quotation or a line reference against a pinned public commit, so it is checkable
without taking my word for any of it. The audit is recorded in
[evidence/source-audit-2026-08-20.md](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/your-memory-has-no-authority-model/evidence/source-audit-2026-08-20.md),
with a per-claim source map in
[evidence/figures.md](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/your-memory-has-no-authority-model/evidence/figures.md).*

Long context retired the question agent memory used to be judged on. Whether the
right turn comes back from a corpus is a question a large enough window answers
by not asking it. Paste the conversation in. The retrieval problem stops
existing.

What a window cannot do is decide which of two contradictory facts is true,
refuse to let a model's guess overwrite a person's statement, or tell you what
it believed last week. Those are properties of a write path, and a context
window does not have one.

I investigated the source of seven publicly available memory systems on 20 August
2026, each at a pinned commit. In six of them, a fact a person stated and a fact a
language model inferred are the same kind of row, with no field distinguishing
them, and the model's own output decides which rows survive. In three, a model
tool call destroys the prior content outright.

Better retrieval leaves that where it is. What the store accepts, and what it
lets go, is settled at the write, and it survives any amount of context you
throw at the read.

`aimee` answers it with one graph. Facts, conversations, episodes and code are
not separate stores that get stapled together at the end. They are one substrate
that a single query ranks.

And that substrate distils under collective use. What several people reach
independently rises out of the scope it was learned in, what fails the people it
reached sinks, and a team's store compounds on work nobody filed. Everything
strict about the write path exists because of those two facts together.

Something to be up front about: `aimee` is opinionated. `aimee` is highly
opinionated. Take this for what it's worth.

## One recall, one score

A query starts the way you would expect. Lexical matching and dense vectors
produce a set of candidate memories.

Then it stops being ordinary. The top twelve candidates are asked which
canonical entities they mention, and those become up to forty-eight seeds for a
walk across the graph
([`memory_core_search_c.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/modules/memory/memory_core_search_c.c#L846-L905)).
The walk runs two hops by default, weighted by how useful each edge has proven,
and it collects memories attached to every node it reaches.

Memories the walk finds that the vectors and the keywords both missed are added
to the candidate set. The code calls this the bridge case, and it is the whole
point. A question can be worded nothing like the memory that answers it, so long
as something the question does match is connected to it.

Everything then ranks together under one score with fourteen parts: lexical
overlap, dense similarity, entity match, graph proximity, code proximity,
PageRank, confidence, evidence strength, salience, surprise, temporal fit,
lifecycle state, coverage and query intent
([`memory_core_search_b.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/modules/memory/memory_core_search_b.c#L248-L340)).
A typed fact, a conversation from March and a function you edited last week
compete in the same ranking, on the same scale.

Floors then guarantee that summaries and facts keep their seats even when raw
score would crowd them out, conversational neighbours of the winners are pulled
in, and scope sorts hard on what the caller is allowed to see. The fusion is not
a blend of two result lists. It is one candidate set that several kinds of
evidence built together.

## Code was not added to this memory. The memory was added to the code

The order things were built in explains the design better than the design
explains itself.

This did not start as a memory system that later grew a code index. It started
as code intelligence: tree-sitter extractors pulling symbols, references, calls,
imports and git co-change out of a repository into a graph
([`CODE_INTELLIGENCE.md`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/docs/CODE_INTELLIGENCE.md)).
The memory layer was built on top of that, to make the code intelligence better.
Everything above, the classes and the ontology and the distillation, exists
because a system that reads code needed somewhere to keep what it worked out.

That is why code is not a guest in this graph. It is what the graph was for, and
the general memory is the part that arrived later.

Nothing about that walk is specific to prose. Code lives in the same edge table
under prefixed keys: a file, a symbol, an import, an export, a route, a project
([`memory_graph_fusion.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/modules/memory/memory_graph_fusion.c#L158-L165)).
One namespace, one traversal.

The relation weights are where it shows. `defines` pulls hardest at 1.00, then
`contains` at 0.85, `depends_on` at 0.75, `calls` at 0.55. Sitting in the same
list are `co_edited` at 0.60 and `co_discussed` at 0.45
([`memory_graph_fusion.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/modules/memory/memory_graph_fusion.c#L26-L50)).

A static analyser produces the first group. Only history produces the second.
Files that change together and topics discussed together are facts about a
codebase that no parser will ever derive, and to this walk they are the same
kind of edge as a function call.

So a question asked in prose reaches code. Ask why a pool wedges under load, hit
the conversations that mention it, seed the walk with the entities in them,
cross into the symbols, and come back with the retry function. It runs the other
way just as well: start from a symbol and the walk returns the thread where
somebody decided the policy that function implements.

That is the thing neither half can do alone. A code index has never heard the
conversation. A conversation store cannot reach the call graph. The interesting
answer is almost always one hop across that boundary, and the boundary is where
every other system keeps a wall.

One guard keeps this from becoming mush. A query that does not look like a code
question is refused entry to code subgraphs entirely, checked per node as the
walk proceeds
([`memory_graph_fusion.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/modules/memory/memory_graph_fusion.c#L186-L189)).
Ask about your spouse and no call graph appears.

## The graph does not stop at the repository boundary

A per-repo code graph answers questions inside one checkout. Most of what you
want to know lives across the line between two.

Take a client that calls `LiStartConnection`, a function defined in a separate
library repository. Both are indexed. Symbols are keyed by project, so the call
in one and the definition in the other are two unrelated nodes, and asking who
calls that function returns nothing useful. The reference deployment carries
forty repositories with that seam running between every pair of them.

Resolving it by name is the obvious move and the wrong one, because names
collide, vendored copies duplicate them, and a planted export in a repository
you did not write is an attack rather than an accident. So the resolver refuses
to emit a boolean. Every cross-repo edge carries a confidence tier and the
evidence that earned it
([`cross_repo_resolver.h`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/cross_repo_resolver.h)).

The top tier needs corroboration rooted in a repository you have marked
trusted, by one of two independent routes. Either an import in the caller
resolves to the definer under per-language rules, or the symbol is in the
definer's exports while the caller uses it at least three times across at least
three distinct files. That second threshold should look familiar. It is
the corroboration rule from further up this piece, pointed at code.

What happens to the rest is the part that matters. A single call site is
tentative and stays out of the default output. A symbol with several plausible
definers goes to a review queue as ambiguous and is never emitted as a
dependency. An import that resolves to more than one indexed file is routed
there too, never guessed, and a vendored copy that collides with the original
goes the same way.

Trust is a property of each repository and it caps what that repository can
vouch for. An untrusted caller's import corroboration cannot exceed the middle
tier, and an untrusted definer can never lend top-tier export corroboration at
all, because its export list is not something it can attest to about itself.

This is the same write gate, on the same graph. Refuse the unvalidated edge,
tier what remains by the evidence behind it, queue the genuinely ambiguous for a
human, and never let an unverified source promote itself. A dependency edge and
a fact about a person are held to one standard because they end up in one store,
and a question asked in one repository can be answered by code in another with
the graph saying how confident it is and why.

## A contract and the code that implements it are two hops apart

Code intelligence is where this started. It is not where it stopped, and the
generalisation is the part that pays.

Push a PDF at it. A signed contract, a payroll policy, a compliance standard.
Structured ingestion keeps what plain text extraction throws away: page
coordinates, reading order, tables as cells, OCR for the scanned ones, and the
identity and confidence of whatever extractor produced each span
([`STRUCTURED_PDF.md`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/docs/STRUCTURED_PDF.md)).
A citation is a document hash, a page and a bounding box, so an answer can point
at the paragraph it came from rather than paraphrasing it.

That document is then mined for the entities it mentions. Each mention is
embedded and resolved against the canonical entities already known, and the
search runs up the scope lattice, from the project the document arrived in, out
to the workspace, out to global
([`kb_curator_resolve_entities.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/kb/kb_curator_resolve_entities.c#L1-L12)).
A narrow mention lands on the broad entity that already exists instead of
forking a near-duplicate beside it.

The entities that document resolves onto are the same entities the code units
resolve onto. A curator pass writes the links, and the file that does it states
the consequence in its own header: doc to entity to code unit becomes a graph
traversal
([`kb_curator_link_artifacts.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/kb/kb_curator_link_artifacts.c#L5-L9)).
There is an endpoint for exactly that question
([`kb_http.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/kb/http/kb_http.c#L997-L998)).

So a clause in a signed agreement and the function that enforces it are not
three systems away from each other. They are two hops in one graph. Which
retention period the contract obliges you to, and which scheduled job actually
deletes the rows, is one question with one answer citing a page on one side and
a line number on the other.

The refusals hold on this path too. Near matches above the threshold resolve,
unrelated ones commit as new canonical entities, and mentions landing in the
uncertain band between go to a judge rather than being merged on a hunch.
Re-ingesting changed bytes creates a new version and does not move the old
coordinates under a new file. Where the retrieved evidence is too thin for the
question, answerability says so instead of producing something.

An organisation's documents are not a different kind of input here. They are
more of the same input, and the entity registry is what puts a payroll policy
and a scheduler on the same node.

## Two clocks, and neither one overwrites

A graph that ranks everything has to be honest about time, and there are two
independent clocks doing it.

Facts carry both. Valid time is the interval a fact held in the world. Transaction
time is when the system stopped believing it. Correcting a fact stamps the second
and leaves the row in place, so "what was true last year" and "what did you
believe last week" are different queries against different columns
([`schema.sql`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/schema.sql#L1400-L1409)).

The code graph runs on generations. Every projected edge belongs to one, a
project has exactly one visible at a time, and the walk traverses only edges
whose generation is visible on a project that is current
([`entity_edges.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/entity_edges.c#L21-L32)).
Generations move from pending to visible to superseded, so publishing a new
projection is a swap and never an edit in place.

The consequence is the part worth having. A traversal cannot mix symbols from
two different states of the tree, which is exactly what an incrementally updated
code index does to you on a bad day. You get one consistent view of the
repository as it was at a moment, or you get the current one, and never a
blend.

Both clocks obey the same rule for different reasons. A fact is superseded
because the world moved. A generation is superseded because the repository
moved. Neither destroys what it replaced.

## One graph, four scopes, and visibility is a rank

Your memory and your company's memory are the same graph. What separates them is
not which store they sit in but how visible they are to the query asking.

Scope comes in four kinds: user, project, workspace, global. A recall carries
the caller's active project and workspace, and every candidate is ranked against
them. A memory scoped to the active project outranks one scoped to the
workspace, which outranks something shared or global, and anything outside the
caller's context scores zero and is gone
([`memory_scope_query.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/memory_scope_query.c#L40-L59)).

That ranking is bound into the query as parameters, not applied to the results
afterwards. The distinction matters more than it sounds: filtering after
ranking leaks through timing and through which candidates were considered, so
the authorisation boundary has to be inside the retrieval, not downstream of it.

Relevance is preserved inside each band. The sort is stable, so the reranker's
ordering survives within a visibility bucket and only the bands themselves are
hard. You get the most relevant thing you are allowed to see, and never a hint
of the more relevant thing you are not.

Underneath that runs a second axis: how settled a memory is, from scratch at L0
through durable fact at L2 to policy at L4 and synthesised pattern at L5. A
memory climbs by evidence, and stable facts promote on confidence while patterns
condense from the same fact appearing across separate sessions. One step wants a
person. Promotion into the tier that carries operating policy can require a
recorded operator approval, because a rule the system will apply to future work
is not something a confidence score should be allowed to enact alone.

The two axes are independent, which is what makes this cohere. A tier says how
much the system trusts a memory. A scope says who it belongs to. Personal
context and organisational knowledge sit in one substrate, ranked by one query,
separated by an authorisation boundary that is a first-class part of the
ranking.

## A team's memory, distilled out of work nobody filed

The design goal is that a team's memory gets better the more the team uses it.
Not larger. Better, in the sense that what it holds becomes more refined and
more of it is worth reading, because a store built this way has one thing no
individual has: several people arriving at the same conclusion separately.

One store serves a person, a team or a company, and it distils. Something one
engineer's work established climbs out of the scope it was learned in once
enough independent work agrees with it. Nobody files it and nobody curates it.

The same threshold governs that in three places. A durable fact that has turned
up in three separate sessions is synthesised into a pattern, on a query counting
distinct sessions
([`memory_promotion.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/memory_promotion.c#L386-L410)).
An entity corroborated by three distinct sources is promoted out of local scope,
on a query that considers only the not-yet-global ones
([`kb_curator_promote.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/kb/kb_curator_promote.c#L85-L95)).
A novel relation seen three times joins the vocabulary.

The word doing the work in each is *distinct*: distinct sessions, distinct
source artifacts, sightings in work nobody staged together. At team scale that
is not a proxy for quality. It is what quality means.

None of this is visible while it happens, and that is the point. An engineer
does their work. Months later somebody who has never spoken to them asks a
question, and the answer carries what that work established, because enough
other work independently agreed with it in between.

The loop closes on the other side. Demotion runs on verdicts attributed across
everyone's recalls, so a shared memory that keeps proving wrong in practice
sinks on the evidence of the people it failed.

Which makes collective use the selection pressure, in both directions. What
several people reach independently rises. What fails the people it reached
sinks. Neither needs a curator.

There is nothing novel in the principle underneath that, and it is stronger for
being old. Independent convergence is what replication means in science, what a
second team reaching your architecture tells you about the architecture, and
what makes a finding worth more than the confidence of whoever reported it. Two
people agreeing after talking is a conversation. Two people agreeing without
having talked is evidence.

The system counts distinct sources because that is the difference, and it is
the whole reason the count means anything.

## Which is why the write path has to be strict

That flywheel is also the threat model, and it is the reason for everything
below.

In a system where facts sit in their own store and get consulted when a query
looks factual, a wrong fact gives a wrong answer to the questions that reach it.
The damage is bounded by the query.

In one graph it is not. An edge is a path, and paths change what the walk
reaches, which changes what enters the candidate set, which changes the ranking
for questions that never mentioned either endpoint. A relationship a model
invented at three in the morning does not sit quietly in a corner waiting to be
asked about. It bends recall.

And on a shared deployment it does not bend only yours. Something that survives
long enough to be corroborated three times is promoted into everyone's context,
which means a store that distils is a store where a bad write has compound
interest.

That is why the rest of this piece is about writes. A system that fuses
everything and shares the result has to be far more careful about what it admits
than one that keeps its mistakes in separate boxes.

## A model's guess never outranks what you told it

Every fact is born into one of three classes, and the class is decided by who
asserted it, not by how sure anyone sounds.

Say something yourself, using a relation the system already understands, and the
fact is Class A. It carries full confidence, it wins every conflict about the
same subject and relation, and it never expires. Let the background extractor
infer something from a note you wrote, and the best it can earn is Class B.
Everything else is Class C, which is to say speculation, and speculation is on a
clock.

The rule that assigns the class is eleven lines long and has no way to reach
Class A from a model
([`fact_lifecycle.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/fact_lifecycle.c#L48-L59)).
The extractor's calls pass their authority as a constant
([`kb_memory_facts.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/kb/kb_memory_facts.c#L300-L305)),
so there is no argument a prompt could win.

The model is asked how confident it is, and the answer is used once, as a floor:
below six-tenths the triple is dropped
([`kb_memory_facts.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/kb/kb_memory_facts.c#L39)).
Above the floor the number buys nothing. A model that returns perfect confidence
on a hallucinated triple lands exactly where a hedging one does.

The awkward branch is the first one. A relation nobody has established yet is
speculation even when you asserted it personally, because what is unproven there
is the vocabulary and your authority cannot cure that. It costs you something
real. It is still the right trade, because an unproven word that enters the
graph starts moving results immediately.

Reinforcement moves a fact along that scale and never off the end of it. A model
inference confirmed enough times stops expiring and stays Class B
([`fact_lifecycle.h`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/fact_lifecycle.h#L58-L61)).
Repetition buys durability. It does not buy authority.

Speculation that never gets confirmed runs out its clock, and even then the row
is only stamped as no longer believed
([`fact_lifecycle.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/fact_lifecycle.c#L83-L86)).
Expiry is a change of standing. It is never a deletion.

## Correcting a fact leaves the old one where it is

What a correction means is a property of the fact being corrected. Most
relations supersede: the old value is stamped and the new one written beside it.
A few are marked so a stale value stops matching while the row stays for the
record, which is what an old nickname needs. A few more refuse to be quietly
rewritten at all
([`fact_lifecycle.h`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/fact_lifecycle.h#L62-L85)).

That last kind does not mean you are locked out. It means no model may rewrite
the value behind your back. You can still supersede it yourself, and the new
value arrives with your authority on it.

The guard runs in both directions. An inferred correction cannot retract
something you stated, on any relation at all. In a fused graph that guard is
doing more than protecting one answer, because retracting an edge removes a path
and quietly changes what the walk can reach.

## The model cannot invent its way around the rules

None of this holds if a model can route around it by making up a relation. So
the vocabulary is checked before anything is written.

Facts are triples, and each kind of relationship declares what may sit on either
end of it. Employment joins a person to an organisation, an address joins a
device to an address.

When a triple arrives the relationship is looked up and both ends are checked
against what it permits
([`memory_fact_gate.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/modules/memory/memory_fact_gate.c#L14-L22)).
A model that proposes the printer works for the kernel gets a rejection, and the
commit path stops before writing anything, under a comment that says never to
write an unvalidated edge
([`rel_types_store.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/rel_types_store.c#L207-L208)).

Seventeen relationships ship with the system so a fresh install can validate
before it has learned anything
([`rel_types.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/rel_types.c#L18)),
and the live set lives in a table the running system extends
([`schema.sql`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/schema.sql#L1412)).
Each one carries its own rules, which is why nothing downstream has to be told,
case by case, that a person has one employer and many acquaintances.

The obvious objection is that seventeen relationships is a rounding error
against the world, and a vocabulary that is wrong rejects things that are true.

## The vocabulary grows without anyone approving it

A relationship the system has never seen is not thrown away. It is admitted as
speculation, with a provisional entry created so the fact has something to hang
on, and the sighting is counted
([`rel_types_store.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/rel_types_store.c#L255-L270)).

The counting is careful in two ways worth noticing. A sighting registers only
after the fact it came from actually committed, so a failed write cannot inflate
a candidate's standing. And a relationship already rejected keeps that verdict,
so it cannot creep back onto the shortlist by being proposed again
([`ontology_evolution.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/ontology_evolution.c#L41-L46)).

Recur across enough separate sources and the maintenance pass promotes the
relationship on its own, with nobody asked
([`kb_curator_drain.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/kb/kb_curator_drain.c#L800-L828)).
Three sightings is the default and promotion is on out of the box
([`config_kb_curator.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/modules/config/config_kb_curator.c#L74-L76)).

One family of words is barred from ever making it. A model that falls back on a
catch-all is refused promotion however often it does so, because a durable
relationship called `misc` can never be reconciled to a real one later.

A word earns permanence by turning up again in work nobody staged, and no one
signs off on it. The one path that does want a human is teaching a whole domain
up front from its documentation, which changes the shape of the vocabulary
before any evidence has accumulated to justify it.

## Two spellings of a name are one thing, and a bad guess is reversible

Identity is not a nicety here. The graph walk starts from the entities a
candidate memory mentions, so a name that splits into three nodes is three
places the walk cannot get to.

The ends of a fact are resolved to an identity before the fact is stored
([`rel_types_store.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/rel_types_store.c#L155-L183)).
Names point at that identity and never at each other, which makes a circular
chain of nicknames impossible by construction
([`schema.sql`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/schema.sql#L1443-L1456)).

Values are left alone. An address or an age is not somebody, and running it
through an identity register would invent a person where there is none.

Two things about this matter more than the matching itself. Every close-call
merge is written down and can be undone
([`entity_registry.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/entity_registry.c#L242-L408)),
which is the difference between a system that is confident and one that can be
wrong safely. And a name with several plausible owners is not guessed at. It
goes on a queue with a status and a bounded number of retries, blocking neither
the write nor the recall
([`schema.sql`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/schema.sql#L1465-L1472)).

## What survives is decided by how it turned out

Recall is not free of consequences. Each one records which memories it put in
front of the model, and each memory that shaped an answer gets a verdict written
against it: accepted, corrected, contradicted, rolled back, or beside the point.

Whether a memory keeps its standing is then decided from a time-decayed window
of those verdicts and nothing else. The contract spells out what is deliberately
excluded:

```text
The scorer reads only attributed outcome evidence — not source tags, declared
confidence, author id, or retrieval frequency.
```

[`demotion.h`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/demotion.h#L104-L112).
That exclusion list is the whole idea. A memory pulled up constantly and wrong
every time sinks, and a memory wearing a respectable provenance tag earns
nothing for it.

Note which frequency is being refused, because the system counts the other one
carefully. How many independent sources asserted a thing is corroboration, and
it promotes. How often a row got surfaced is popularity, and it counts for
nothing.

Being retrieved is something that happens to a memory. Being arrived at
separately is something several people did.

Under a floor of recorded outcomes the scorer declines to judge at all and says
so
([`demotion.c`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/demotion.c#L690-L774)).
It is the same instinct as abstaining on a weak answer, pointed at housekeeping.

Contradictions are not resolved by picking a winner. Both claims stay, linked,
with their sources intact, and the current value is a matter of policy
([`CURATOR_PIPELINE.md`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/docs/CURATOR_PIPELINE.md)).
An unresolved one also raises a question on a backlog of things the system knows
it does not know, alongside gaps like a fact gone stale and a topic with thin
coverage
([`curiosity.h`](https://github.com/RakuenSoftware/aimee/blob/50c5d88d37bae618ee08b0101f163682e864ace9/src/db2/curiosity.h#L25-L29)).

## Six of seven systems keep their stores in separate piles

Every row below was read from the project's own source at the commit named, on
20 August 2026. Where a project's design differs from what a summary line can
carry, the paragraphs after the table say so.

| system | commit | one fused graph | typed write gate | authority classes | valid time | model may remove a fact |
| --- | --- | --- | --- | --- | --- | --- |
| `aimee` | `50c5d88d` | yes, with code | yes, kind-validated | A / B / C, enforced | yes, plus code generations | no, superseded |
| Graphiti (Zep) | `c4069327` | graph only | no | none | yes | expired, retained |
| cognee | `fd5045f6` | graph plus vector | optional, enrichment only | none | edge `updated_at` | tagged, retained |
| mem0 OSS | `3599aa75` | no, graph removed | no | none | no | not in v3, ADD-only |
| Letta Code | `d1dc6880` | no | no | none | no | yes, block rewrite |
| LangMem | `29cbe41e` | no | no | none | no | yes, hard delete |
| Memobase | `358c16bb` | no | slot schema | none | no | yes, slot rewrite |

Graphiti is the closest architecture and the fairest comparison. It is
bitemporal: `valid_at`, `invalid_at` and `expired_at` all sit on `EntityEdge`,
and a contradicted edge is expired, with the row kept
([`edges.py:262-283`](https://github.com/getzep/graphiti/blob/c406932767ee490ad2311fd694a6b2ac3b164599/graphiti_core/edges.py#L262-L283)).

Custom edge types are supported and filtered per node-label pair. What that
filtering does is choose which type definitions the extraction prompt is shown
([`edge_operations.py:458-486`](https://github.com/getzep/graphiti/blob/c406932767ee490ad2311fd694a6b2ac3b164599/graphiti_core/utils/maintenance/edge_operations.py#L458-L486)).
Nothing then checks the relation the model returns against them. The validation
that does run on the way in checks that the LLM's entity names exist in the node
list and drops self-edges
([`edge_operations.py:210-241`](https://github.com/getzep/graphiti/blob/c406932767ee490ad2311fd694a6b2ac3b164599/graphiti_core/utils/maintenance/edge_operations.py#L210-L241));
the relation name is taken as given and becomes the edge's `name`.

There is no confidence, provenance or authority field on `EntityEdge` at all, so
an edge the user dictated and an edge the model inferred are indistinguishable
rows. And the graph holds what was extracted from episodes. Source code is not
a first-class citizen of it.

cognee has arrived at the same problem and named it. Its temporal conflict
resolver tags superseded edges and keeps them, which is the right behaviour, and
its module docstring explains why it cannot do that automatically:

```text
Nothing is applied automatically: the caller names the relationships that are
single-valued. Most cognee relationships (``knows``, ``mentions``, ...) are
legitimately many-valued and must never be collapsed, and there is no
cardinality metadata to tell them apart.
```

[`temporal_conflict_resolver.py:13-16`](https://github.com/topoteretes/cognee/blob/fd5045f6b60522c1953fc1ae258e041ba53602d8/cognee/modules/graph/utils/temporal_conflict_resolver.py#L13-L16).
That missing cardinality metadata is what a relation's own correction policy
carries in the store.

cognee also ships real ontology support, and the default resolver is constructed
with `ontology_file=None`
([`get_default_ontology_resolver.py:10-12`](https://github.com/topoteretes/cognee/blob/fd5045f6b60522c1953fc1ae258e041ba53602d8/cognee/modules/ontology/get_default_ontology_resolver.py#L10-L12)).
An operator-supplied OWL file is matched fuzzily to enrich extracted entities,
and a name with no match is still constructed. Contradiction detection defaults
to `False`
([`cognify/config.py:13-17`](https://github.com/topoteretes/cognee/blob/fd5045f6b60522c1953fc1ae258e041ba53602d8/cognee/modules/cognify/config.py#L13-L17)).

mem0's open-source graph memory no longer exists. The v3 release removed it:
"Graph memory is removed from OSS. It's a built-in, always-on Mem0 Platform
feature"
([`oss-v2-to-v3.mdx:41`](https://github.com/mem0ai/mem0/blob/3599aa75ed64ee41c3b1d8133a8b39403fb8f703/docs/migration/oss-v2-to-v3.mdx#L41)).

The same release made extraction ADD-only: "Single-pass ADD-only (one LLM call,
no UPDATE/DELETE)". That is a real improvement on the previous design, where an
LLM chose between ADD, UPDATE and DELETE per fact and a DELETE removed the
vector row while retaining the prior text in a SQLite history table
([`main.py:2100-2122`](https://github.com/mem0ai/mem0/blob/3599aa75ed64ee41c3b1d8133a8b39403fb8f703/mem0/memory/main.py#L2100-L2122)).

What replaces it is accumulation. Memories are self-contained sentences, related
ones are linked by id, and nothing reconciles two that contradict. The open
source you can run today is free-text memories with hash dedup and hybrid
search; the reconciliation story is on the hosted side.

Letta's V1 server has been retired and its memory is text the model edits. The
repository at `letta-ai/letta` is now a landing page, the source lives in
`letta-ai/letta-code`, and the V1 server sits on an `archive` branch that
"receives no fixes or security updates, and should not be used in production."
The memory surface is a block the agent rewrites through `memory_replace`,
`memory_insert` and `memory_rethink`
([`toolset.ts:61-68`](https://github.com/letta-ai/letta-code/blob/d1dc6880971dc55a5e5dfcf845d4cba740b14585/src/tools/toolset.ts#L61-L68)).

Credit where it is due, and it is a design nobody else here has: MemFS tracks
every block in git, so a rewrite that destroyed a fact leaves a commit. That is
an audit trail. The store itself still has no idea which line came from the
user.

LangMem lets the model delete a memory outright. `create_manage_memory_tool`
permits `create`, `update` and `delete` by default, and the delete branch is one
line: `await store.adelete(namespace, key=str(id))` on the async path
([`tools.py:293-294`](https://github.com/langchain-ai/langmem/blob/29cbe41e58528f92e9efa773c12e15c47be3808c/src/langmem/knowledge/tools.py#L293-L294)),
`store.delete(namespace, key=str(id))` on the sync one
([`tools.py:327-328`](https://github.com/langchain-ai/langmem/blob/29cbe41e58528f92e9efa773c12e15c47be3808c/src/langmem/knowledge/tools.py#L327-L328)).
No history row, no tombstone, no class check on what is being removed.

It is the plainest case in the set. A tool call the model chooses to emit
removes a fact a person stated, and afterwards the store cannot tell you it
happened.

Memobase does have a schema, and it is the closest thing here to an ontology.
Profiles are topic and subtopic slots and extraction fills them. Reconciliation
is an LLM choosing `APPEND`, `UPDATE` or `ABORT`, where `UPDATE` means rewriting
the slot's memo text
([`merge_profile.py:34-46`](https://github.com/memodb-io/memobase/blob/358c16bbc6d687937d79bc2f984a11c3be8da901/src/server/api/memobase_server/prompts/merge_profile.py#L34-L46)).
A slot holds one attribute of one profile, and the prior text does not survive
the rewrite.

I also read A-MEM (`ceffb860`), which organises memories as Zettelkasten-style
linked notes with LLM-generated links and carries no temporal, authority or
ontology layer. It is a research implementation and I am not holding it to a
production bar.

## This one is in production, and most of the field's open source is not

`aimee` is not a research project. It is the system Rakuen runs, the memory
described above is the memory doing that work, and it has been carrying it in
production for about a year. The public repository is younger than that, because
its first commit is a snapshot import.

That is worth stating because the audit turned up something I was not looking
for. Across the seven, the open-source artifact and the working system are
frequently different objects.

A-MEM is a research implementation, and its own README sends you to a separate
repository to reproduce the paper. Letta's V1 server is on an `archive` branch
that "receives no fixes or security updates, and should not be used in
production", and the current source is a different repository. mem0's graph
memory left the open source entirely and is now "a built-in, always-on Mem0
Platform feature". cognee's contradiction detection ships switched off.

None of that is dishonest and none of it is unusual. A research group publishes
to be cited and a company keeps its differentiator on the paid tier. It does
mean a reader comparing architectures is often comparing a paper, a retired
server and a hosted product, and only some of it is code they can put under
load.

The architecture above is none of those. It is public under AGPL-3.0, the
extraction prompt in the fact benchmark is lifted from the shipped extractor
unchanged, and the memory subsystem carries thirty-one of its own test files.
Every claim in this piece is written against a line number because there is a
running system behind each one.

## The claim, scoped so one counterexample would settle it

Of the seven systems in the table above, plus A-MEM, all read at a pinned commit
on 20 August 2026, `aimee` is the only one in which all four of the following
hold: conversational memory, typed facts and source code are ranked by one
query against one graph; a model-extracted fact cannot reach the authority class
a user-stated fact gets, by any path including repetition; a model authority
cannot retract a user-stated fact on any relation; and a triple whose subject or
object kind violates the relation's ontology is refused a row.

I looked for a counterexample among the systems I could read and did not find
one. That is a claim about what I searched. Hosted systems whose source I cannot
read are outside it, and so is any system I did not think to clone. One system
holding all four would settle it, and I would rather be shown one than keep the
claim.

## What this design costs

Fusion is not free, and the bill arrives on the write path. Every guard in the
middle of this piece exists because an edge is a path, and a system that lets
anything become an edge has let anything change every ranking.

A vocabulary that is wrong rejects facts that are true. Seventeen relations is a
small seed, so on a fresh corpus most of what arrives is novel, lands as
speculation, and has to earn its way to durable across three sightings. A fact
stated once, in a domain nobody has taught, expires. That is the deliberate
trade, and it is a real cost paid by the person who says something true once.

Retaining everything has a price too. Nothing is deleted, so the edge table
grows with every correction, and a store running for a year carries every value
each fact has ever held. Superseded rows are cheap to filter and they still
occupy disk.

Recall abstention exists and is default-off with its threshold uncalibrated,
because calibrating it needs labelled ask-outcome data nobody has collected. I
would rather say that than ship a threshold I guessed.

## Who this is not for

The real split here is not difficulty. It is whether you want a library or a
system.

mem0 and LangMem are libraries. You import them, pass an API key, and they run
inside your process. If that is the shape you want, take one of those, because
`aimee` is not that and never will be.

It is a server you run: clone, `docker compose up`, and click through a
seven-step wizard that provisions the store and picks the embedder. That is less
work than standing up Graphiti, which asks you to bring your own Neo4j,
FalkorDB or Neptune cluster first. It is still a different commitment from a
`pip install`.

Which points at the other disqualifier. There is no hosted tier. Mem0, Zep and
Letta will all operate this for you and `aimee` will not, so if you do not want
to run a database, the answer here is no and the answer there is yes.

And if your agent's memory holds preferences that are cheap to be wrong about,
none of the machinery above is worth its cost to you. Wrong preference, mild
annoyance, next turn corrects it.

The argument starts to bind when a remembered fact drives an action, and it
binds harder when memory and code are the same question. A device address, a
policy decision, an on-call owner, the reason a function is written the way it
is.

## Go and check your own

Four checks to run against whatever memory system you have. The last one is the
one almost nothing passes.

Open the schema for a stored fact and look for a field recording who asserted
it, distinct from the model that wrote it down. If there is no such column, the
distinction does not exist at runtime, whatever the prompt says.

Follow the delete path from the model's tool surface and see what survives it. A
history table is worth having. A tombstone the recall path walks past is worth
more, because the fact is still in the graph.

Try to write the two queries "what did you believe last week" and "what was true
last year" against different columns. If they are the same query, corrections
are overwrites and you cannot audit one.

Then ask it something in plain prose whose answer is a function, and see whether
the function comes back. If your memory and your code index are separate
services, you already know the answer, and no amount of context window fixes it.
