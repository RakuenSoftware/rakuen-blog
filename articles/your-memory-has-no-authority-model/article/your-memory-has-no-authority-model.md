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

Long context retired the question agent memory used to be judged on. Whether
the right turn comes back from a corpus is a question a large enough window
answers by not asking it. Paste the conversation in. The retrieval problem
stops existing.

What a window cannot do is decide which of two contradictory facts is true,
refuse to let a model's guess overwrite a person's statement, or tell you what
it believed last week. Those are properties of a write path, and a context
window does not have one.

I investigated the source of seven publicly available memory systems on 20
August 2026, each at a pinned commit. In six of them, a fact a person stated
and a fact a language model inferred are the same kind of row, with no field
distinguishing them, and the model's own output decides which rows survive. In
three, a model tool call destroys the prior content outright.

`aimee` answers it with one graph. Facts, conversations, episodes and code are
not separate stores that get stapled together at the end. They are one
substrate that a single query ranks.

And that substrate distils under collective use. What several people reach
independently rises out of the scope it was learned in, what fails the people
it reached sinks, and a team's store compounds on work nobody filed. Everything
strict about the write path exists because of those two facts together.

Something to be up front about: `aimee` is opinionated. `aimee` is highly
opinionated. Take this for what it's worth.

## One recall, one score

Lexical matching and dense vectors produce a set of candidate memories, and
then it stops being ordinary. The top twelve candidates are asked which
canonical entities they mention, and those become up to forty-eight seeds for a
walk across the graph. The walk runs two hops by default, weighted by how
useful each edge has proven, and it collects memories attached to every node it
reaches.

Memories the walk finds that the vectors and the keywords both missed are added
to the candidate set. The code calls this the bridge case, and it is the whole
point. A question can be worded nothing like the memory that answers it, so
long as something the question does match is connected to it.

Everything then ranks together under one score with fourteen parts: lexical
overlap, dense similarity, entity match, graph proximity, code proximity,
PageRank, confidence, evidence strength, salience, surprise, temporal fit,
lifecycle state, coverage and query intent. A typed fact, a conversation from
March and a function you edited last week compete in the same ranking, on the
same scale.

Floors then guarantee that summaries and facts keep their seats even when raw
score would crowd them out, conversational neighbours of the winners are pulled
in, and scope sorts hard on what the caller is allowed to see. The fusion is
not a blend of two result lists. It is one candidate set that several kinds of
evidence built together.

Fourteen weighted signals invites an obvious question, which is who picked the
weights. Nobody did. A background worker turns accumulated feature rows and
recorded retrieval outcomes into a fitted model (`kb_ranker_fit.h`, run from
`kb_service_workers.c`), keyed to the same retrieval events the demotion scorer
reads. The ranking learns from which candidates turned out to be useful.

And a fitted model does not get to install itself. It lands as a proposal and a
benchmark gate has to promote it. The same rule the facts live under, applied
to the thing that ranks them.

Changes to this machinery are measured before they ship. A shadow mode records
per-query rank and score deltas between fused and unfused ranking, compactly
enough to run over real traffic without keeping the payloads. That is an
evaluation harness and not a production path, which is the honest description
of it.

## Code was not added to this memory. The memory was added to the code

The order things were built in explains the design better than the design
explains itself. This did not start as a memory system that later grew a code
index. It started as code intelligence, tree-sitter extractors pulling symbols,
calls, imports and git co-change into a graph, and the memory layer was built on
top to make that better. The classes, the ontology and the distillation all
exist because a system reading code needed somewhere to keep what it worked out.

So code lives in the same edge table under prefixed keys: a file, a symbol, an
import, an export, a route, a project. One namespace, one traversal. The
relation weights are where it shows, with `defines` pulling hardest at 1.00 and
`calls` at 0.55, sitting in the same list as `co_edited` at 0.60 and
`co_discussed` at 0.45.

A static analyser produces the first group. Only history produces the second,
and to this walk they are the same kind of edge.

Which is why a question asked in prose reaches code. Ask why a pool wedges under
load, hit the conversations that mention it, cross into the symbols, and come
back with the retry function. It runs the other way too: start from a symbol and
get the thread where somebody decided the policy it implements. A code index has
never heard the conversation, a conversation store cannot reach the call graph,
and the interesting answer is almost always one hop across that boundary.

One guard keeps it from becoming mush. A query that does not look like a code
question is refused entry to code subgraphs, checked per node as the walk
proceeds. Ask about your spouse and no call graph appears.

The graph does not stop at the checkout boundary either. Symbols are keyed by
project, so a client calling `LiStartConnection` and the library defining it are
two unrelated nodes, and the reference deployment carries forty repositories
with that seam between every pair.

Resolving it by name is the obvious move and the wrong one, because names
collide, vendored copies duplicate them, and a planted export in a repository
you did not write is an attack rather than an accident. So no booleans. Every
cross-repo edge carries a confidence tier and the evidence that earned it.

The top tier wants corroboration rooted in a repository you marked trusted:
an import resolving to the definer, or the symbol in its exports while the
caller uses it three times across three distinct files. That second threshold is
the corroboration rule from further down this piece, pointed at code. A single
call site, several plausible definers, or a vendored copy colliding with its
original all go to a review queue rather than being guessed.

Trust caps what a repository can vouch for. An untrusted definer can never lend
top-tier export corroboration, because its export list is not something it can
attest to about itself.

One more thing the code graph does with time. Every projected edge belongs to a
generation, a project has exactly one visible at a time, and the walk traverses
only edges whose generation is visible on a project that is current. Generations
move from pending to visible to superseded, so publishing a new projection is a
swap and never an edit in place.

The consequence is the part worth having. A traversal cannot mix symbols from
two different states of the tree, which is what an incrementally updated code
index does to you on a bad day. You get one consistent view of the repository as
it was at a moment, or the current one, and never a blend.

## A contract and the code that implements it are two hops apart

Push a document at it. A signed contract, a payroll policy, a compliance
standard, a spreadsheet somebody has been maintaining since 2019.

Ingestion routes by format and falls through to taking the bytes as they are.
Office formats take a converter, and PDFs take an extraction layer that keeps
page coordinates, reading order, tables as cells and OCR, each layer degrading
on its own terms without claiming what it lost. A citation is then a document
hash, a page and a bounding box.

One thing about how it is stored, because the usual answer is wrong. Chunking a
document and keeping the chunks is not a representation of that document. The
whole text is the primary evidence, and a chunk is secondary evidence that
earns its place by pointing back at what it came from.

So a fragment carries the source path, the content hash of the whole file, its
heading path and its line span, and it is doubly linked to its neighbours in
reading order. A clause retrieved without the section it qualifies is not a
shorter answer. It is a wrong one.

A conversation is a document too. Export the thread where a design was argued
out and it ingests like anything else, which is worth doing because of what
those threads hold: not what was decided, which the code already shows, but
why, which it never does. That reasoning is the least durable thing an
organisation produces, stated once by somebody who has since moved teams.

Whatever goes in is mined for the entities it mentions, each resolved against
the canonical entities already known by searching up the scope lattice from
project to workspace to global. A narrow mention lands on the broad entity that
exists instead of forking a duplicate beside it, and the uncertain band between
a near match and a new entity goes to a judge.

Those are the same entities the code units resolve onto. A curator pass writes
the links, and the file that does it states the consequence in its own header:
doc to entity to code unit becomes a graph traversal, with an endpoint for
exactly that question.

So a clause in a signed agreement and the function that enforces it are two hops
apart. Which retention period the contract obliges you to, and which scheduled
job deletes the rows, is one question with one answer citing a page on one side
and a line number on the other.

Which changes who can ask. A compliance officer, a lawyer, or an engineer three
days into the job does not need a symbol name, or the repository holding it, or
the idea that a repository is the thing to look in. Today that question becomes
a message to an engineer who reads for twenty minutes and replies in prose
nobody can check, which is two people doing a worse version of a job the store
can do with both citations attached.

## One graph, four scopes, and visibility is a rank

Your memory and your company's memory are the same graph. What separates them
is not which store they sit in but how visible they are to the query asking.

Scope comes in four kinds: user, project, workspace, global. A recall carries
the caller's active project and workspace, and every candidate is ranked
against them. A memory scoped to the active project outranks one scoped to the
workspace, which outranks something shared or global, and anything outside the
caller's context scores zero and is gone.

That ranking is bound into the query as parameters, not applied to the results
afterwards. The distinction matters more than it sounds: filtering after
ranking leaks through timing and through which candidates were considered, so
the authorisation boundary has to be inside the retrieval, not downstream of
it.

Relevance is preserved inside each band. The sort is stable, so the reranker's
ordering survives within a visibility bucket and only the bands themselves are
hard. You get the most relevant thing you are allowed to see, and never a hint
of the more relevant thing you are not.

Underneath that runs a second axis: how settled a memory is, from scratch at L0
through durable fact at L2 to policy at L4 and synthesised pattern at L5. A
memory climbs by evidence, and stable facts promote on confidence while
patterns condense from the same fact appearing across separate sessions. One
step wants a person. Promotion into the tier that carries operating policy can
require a recorded operator approval, because a rule the system will apply to
future work is not something a confidence score should be allowed to enact
alone.

The two axes are independent, which is what makes this cohere. A tier says how
much the system trusts a memory. A scope says who it belongs to. Personal
context and organisational knowledge sit in one substrate, ranked by one query.

Because that boundary lives inside the ranking, widening who is allowed to ask a
question is not the same decision as widening what any of them can see.

## A team's memory, distilled out of work nobody filed

The design goal is that a team's memory gets better the more the team uses it.
Not larger. Better, in the sense that what it holds becomes more refined and
more of it is worth reading, because a store built this way has one thing no
individual has: several people arriving at the same conclusion separately.

One store serves a person, a team or a company, and it distils. Something one
engineer's work established climbs out of the scope it was learned in once
enough independent work agrees with it. Nobody files it and nobody curates it.

The same threshold governs that in three places. A durable fact that has turned
up in three separate sessions is synthesised into a pattern, on a query
counting distinct sessions. An entity corroborated by three distinct sources is
promoted out of local scope, on a query that considers only the not-yet-global
ones. A novel relation seen three times joins the vocabulary.

None of this is visible while it happens, and that is the point. An engineer
does their work. Months later somebody who has never spoken to them asks a
question, and the answer carries what that work established, because enough
other work independently agreed with it in between.

The loop closes on the other side. Demotion runs on verdicts attributed across
everyone's recalls, so a shared memory that keeps proving wrong in practice
sinks on the evidence of the people it failed.

Which makes collective use the selection pressure in both directions, and
neither direction needs a curator.

There is nothing novel in the principle underneath that, and it is stronger for
being old. Independent convergence is what replication means in science, what a
second team reaching your architecture tells you about the architecture, and
what makes a finding worth more than the confidence of whoever reported it. Two
people agreeing after talking is a conversation. Two people agreeing without
having talked is evidence.

The system counts distinct sources because that is the difference, and it is
the whole reason the count means anything.

## Some memory is armed rather than stored

Everything so far answers a question when one is asked. One part of the store
does the opposite.

A prospective memory is a reminder with a trigger, an action, an anchor and a
recurrence. It sits armed, and context assembly checks the current turn against
the armed set before the turn is answered. An anchor can be an entity or a
file, so a reminder can be attached to the thing it concerns instead of to a
date.

The difference from recall is who initiates. Nobody has to remember that there
was something to remember, which is the failure mode a note-to-self has and
cannot fix. The store raises it when you touch the subject.

Everything else in this piece is about not losing what you know. This is the
one part that is about not missing the moment when knowing it mattered.

## Which is why the write path has to be strict

In a system where facts sit in their own store and get consulted when a query
looks factual, a wrong fact gives a wrong answer to the questions that reach
it. The damage is bounded by the query.

In one graph it is not. An edge is a path, and paths change what the walk
reaches, which changes what enters the candidate set, which changes the ranking
for questions that never mentioned either endpoint. A relationship a model
invented at three in the morning does not sit quietly in a corner waiting to be
asked about. It bends recall.

And on a shared deployment it does not bend only yours. Something corroborated
three times is promoted into everyone's context, so a store that distils is a
store where a bad write earns compound interest.

## A model's guess never outranks what you told it

Every fact is born into one of three classes, and the class is decided by who
asserted it, not by how sure anyone sounds.

Say something yourself, using a relation the system already understands, and
the fact is Class A. It carries full confidence, it wins every conflict about
the same subject and relation, and it never expires. Let the background
extractor infer something from a note you wrote, and the best it can earn is
Class B. Everything else is Class C, which is to say speculation.

The rule that assigns the class is eleven lines long and has no way to reach
Class A from a model. The extractor's calls pass their authority as a constant,
so there is no argument a prompt could win.

The model is asked how confident it is, and the answer is used once, as a
floor: below six-tenths the triple is dropped. Above the floor the number buys
nothing. A model that returns perfect confidence on a hallucinated triple lands
exactly where a hedging one does.

The awkward branch is the first one. A relation nobody has established yet is
speculation even when you asserted it personally, because what is unproven
there is the vocabulary and your authority cannot cure that. It costs you
something real, and it is still the right trade.

Reinforcement moves a fact along that scale and never off the end of it. A
model inference confirmed enough times stops expiring and stays Class B, and
speculation that is never confirmed runs out its clock and is stamped as no
longer believed. Repetition buys durability. It does not buy authority.

## Correcting a fact leaves the old one where it is

What a correction means is a property of the fact being corrected. Most
relations supersede: the old value is stamped and the new one written beside
it. A few are marked so a stale value stops matching while the row stays for
the record, which is what an old nickname needs. A few more refuse to be
quietly rewritten at all.

That last kind does not mean you are locked out. It means no model may rewrite
the value behind your back. You can still supersede it yourself, and the new
value arrives with your authority on it.

The guard runs in both directions. An inferred correction cannot retract
something you stated, on any relation at all. In a fused graph that guard is
doing more than protecting one answer, because retracting an edge removes a
path and quietly changes what the walk can reach.

Because the old rows survive, two clocks have somewhere to write. Valid time is
the interval a fact held in the world, transaction time is when the system
stopped believing it, so "what was true last year" and "what did you believe
last week" are different queries against different columns. A store that
overwrites can answer neither.

All of which is a promise until something records it. Mutations land in a
hash-chained, append-only audit store, the same record shape the server keeps,
with write-once enforced underneath.

A chain is checkable in a way a policy is not. Every system in the comparison
can tell you what it currently holds. This one can tell you whether anything was
quietly changed on the way to holding it.

## The model cannot invent its way around the rules, and the rules grow anyway

None of this holds if a model can route around it by making up a relation. So
the vocabulary is checked before anything is written.

Facts are triples, and each kind of relationship declares what may sit on
either end of it. Employment joins a person to an organisation, an address
joins a device to an address.

When a triple arrives the relationship is looked up and both ends are checked
against what it permits. A model that proposes the printer works for the kernel
gets a rejection, and the commit path stops before writing anything, under a
comment that says never to write an unvalidated edge.

Seventeen relationships ship with the system so a fresh install can validate
before it has learned anything, and the live set lives in a table the running
system extends. Each one carries its own rules, which is why nothing downstream
has to be told, case by case, that a person has one employer and many
acquaintances.

The obvious objection is that seventeen relationships is a rounding error
against the world, and a vocabulary that is wrong rejects things that are true.
Which is why the vocabulary grows on its own.

A relationship the system has never seen is not thrown away. It is admitted as
speculation, with a provisional entry created so the fact has something to hang
on, and the sighting is counted.

The counting is careful in two ways worth noticing. A sighting registers only
after the fact it came from actually committed, so a failed write cannot
inflate a candidate's standing. And a relationship already rejected keeps that
verdict, so it cannot creep back onto the shortlist by being proposed again.

Recur across enough separate sources and the maintenance pass promotes it, on
the threshold the distillation runs on, with nobody asked. One family of words
is barred from ever making it: a model falling back on a catch-all is refused
however often it does so, because a durable relationship called `misc` can never
be reconciled to a real one later.

The one path that does want a human is teaching a whole domain up front from its
documentation, which changes the shape of the vocabulary before any evidence has
accumulated to justify it.

## Two spellings of a name are one thing, and a bad guess is reversible

Identity is not a nicety here. The graph walk starts from the entities a
candidate memory mentions, so a name that splits into three nodes is three
places the walk cannot get to.

The ends of a fact are resolved to an identity before the fact is stored. Names
point at that identity and never at each other, which makes a circular chain of
nicknames impossible by construction.

Values are left alone. An address or an age is not somebody, and running it
through an identity register would invent a person where there is none.

Two things about this matter more than the matching itself. Every close-call
merge is written down and can be undone, which is the difference between a
system that is confident and one that can be wrong safely. And a name with
several plausible owners is not guessed at. It goes on a queue with a status
and a bounded number of retries, blocking neither the write nor the recall.

## What survives is decided by how it turned out

Recall is not free of consequences. Each one records which memories it put in
front of the model, and each memory that shaped an answer gets a verdict
written against it: accepted, corrected, contradicted, rolled back, or beside
the point.

Whether a memory keeps its standing is then decided from a time-decayed window
of those verdicts and nothing else. The contract spells out what is
deliberately excluded:

```text
The scorer reads only attributed outcome evidence — not source tags, declared
confidence, author id, or retrieval frequency.
```

`demotion.h`. That exclusion list is the whole idea. A memory pulled up
constantly and wrong every time sinks, and a memory wearing a respectable
provenance tag earns nothing for it.

Note which frequency is being refused, because the system counts the other one
carefully. How many independent sources asserted a thing is corroboration, and
it promotes. How often a row got surfaced is popularity, and it counts for
nothing.

Being retrieved is something that happens to a memory. Being arrived at
separately is something several people did.

Under a floor of recorded outcomes the scorer declines to judge at all and says
so. It is the same instinct as abstaining on a weak answer, pointed at
housekeeping.

Contradictions are not resolved by picking a winner. Both claims stay, linked,
with their sources intact, and the current value is a matter of policy. An
unresolved one also raises a question on a backlog of things the system knows
it does not know, alongside gaps like a fact gone stale and a topic with thin
coverage.

## Six of seven systems keep their stores in separate piles

Every cell was read from the project's own source at the commit named, on 20
August 2026. The per-system findings, the test behind each column and the line
numbers behind each verdict are in the audit file rather than here.

| system | commit | one fused graph | fragment points at its source | typed write gate | authority classes | valid time | model may remove a fact |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `aimee` | `50c5d88d` | yes, with code | hash, span, heading, neighbours | yes, kind-validated | A / B / C, enforced | yes, plus code generations | no, superseded |
| Graphiti (Zep) | `c4069327` | graph only | raw episode kept, no document above it | no | none | yes | expired, retained |
| cognee | `fd5045f6` | graph plus vector | chunk names a document, document names a path | optional, enrichment only | none | edge `updated_at` | tagged, retained |
| mem0 OSS | `3599aa75` | no, graph removed | messages kept, memories do not reference them | no | none | no | not in v3, ADD-only |
| Letta Code | `d1dc6880` | no | git history of the block | no | none | no | yes, block rewrite |
| LangMem | `29cbe41e` | no | no document model | no | none | no | yes, hard delete |
| Memobase | `358c16bb` | no | blobs kept, slots do not reference them | slot schema | none | no | yes, slot rewrite |

Graphiti is the closest architecture and the fairest comparison. It is genuinely
bitemporal and a contradicted edge is expired with the row kept
([`edges.py`](https://github.com/getzep/graphiti/blob/c406932767ee490ad2311fd694a6b2ac3b164599/graphiti_core/edges.py#L262-L283)). Custom edge types exist,
but what they constrain is which definitions the extraction prompt is shown, so
nothing checks the relation the model returns against them. There is no
confidence, provenance or authority field on an edge at all.

cognee arrived at the same problem and named it. Its temporal conflict resolver
tags superseded edges and keeps them, and its docstring says why that cannot
happen automatically:

```text
Nothing is applied automatically: the caller names the relationships that are
single-valued. Most cognee relationships (``knows``, ``mentions``,...) are
legitimately many-valued and must never be collapsed, and there is no
cardinality metadata to tell them apart.
```

[`temporal_conflict_resolver.py`](https://github.com/topoteretes/cognee/blob/fd5045f6b60522c1953fc1ae258e041ba53602d8/cognee/modules/graph/utils/temporal_conflict_resolver.py#L13-L16).
That missing cardinality metadata is what a relation's own correction policy
carries in the store. cognee ships real ontology support and defaults to no
ontology file, with contradiction detection off
([`config.py`](https://github.com/topoteretes/cognee/blob/fd5045f6b60522c1953fc1ae258e041ba53602d8/cognee/modules/cognify/config.py#L13-L17)).

mem0's open-source graph memory no longer exists: "Graph memory is removed from
OSS. It's a built-in, always-on Mem0 Platform feature"
([`oss-v2-to-v3.mdx`](https://github.com/mem0ai/mem0/blob/3599aa75ed64ee41c3b1d8133a8b39403fb8f703/docs/migration/oss-v2-to-v3.mdx#L41)). The same
release made extraction ADD-only, which is a real improvement on an LLM choosing
DELETE per fact. What replaces it is accumulation: self-contained sentences,
related ones linked by id, and nothing reconciling two that contradict.

Letta's V1 server is retired to an `archive` branch that "receives no fixes or
security updates, and should not be used in production", and memory is now a
block the agent rewrites in place
([`toolset.ts`](https://github.com/letta-ai/letta-code/blob/d1dc6880971dc55a5e5dfcf845d4cba740b14585/src/tools/toolset.ts#L61-L68)). Credit where it is due, and
it is a design nobody else here has: MemFS tracks every block in git, so a
destructive rewrite leaves a commit. That is an audit trail. The store still has
no idea which line came from the user.

LangMem is the plainest case in the set. `create_manage_memory_tool` permits
`delete` by default and the branch is one line,
`store.delete(namespace, key=str(id))`
([`tools.py`](https://github.com/langchain-ai/langmem/blob/29cbe41e58528f92e9efa773c12e15c47be3808c/src/langmem/knowledge/tools.py#L327-L328)), with no history
row and no check on what is being removed. A tool call the model chooses to
emit removes a fact a person stated, and afterwards the store cannot tell you it
happened.

Memobase has the closest thing here to an ontology, in topic and subtopic
profile slots. Reconciliation is an LLM choosing to append, update or abort,
where updating means rewriting the slot's text over what was there.

On the source column the field does better than the criticism usually aimed at
it, and worse than that sounds. Retention is common: Graphiti keeps the raw
episode, mem0 writes every message to a table, Letta has every block version in
git. What is uncommon is a path from the thing you retrieved back to the whole
it came from, and cognee gets closest by having a chunk name its document while
the document names a filesystem location instead of holding the text.

The cheap part is keeping the bytes and nearly everyone does it. The part that
takes deciding is making the fragment carry enough to reconstitute its context,
and then making retrieval able to walk it.

A-MEM (`ceffb860`) organises memories as Zettelkasten-style linked notes with no
temporal, authority or ontology layer. It is a research implementation and I am
not holding it to a production bar.

`aimee` is not a research project. It is the system Rakuen runs, the memory
described above is the memory doing that work, and it has been carrying it in
production for about a year. The public repository is younger than that,
because its first commit is a snapshot import.

That is worth stating because of something this audit turned up without looking
for it. Across the seven, the open-source artifact and the working system are
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

Of the seven systems in the table above, plus A-MEM, all read at a pinned
commit on 20 August 2026, `aimee` is the only one in which all four of the
following hold: conversational memory, typed facts and source code are ranked
by one query against one graph; a model-extracted fact cannot reach the
authority class a user-stated fact gets, by any path including repetition; a
model authority cannot retract a user-stated fact on any relation; and a triple
whose subject or object kind violates the relation's ontology is refused a row.

I looked for a counterexample among the systems I could read and did not find
one. That is a claim about what I searched. Hosted systems whose source I
cannot read are outside it, and so is any system I did not think to clone. One
system holding all four would settle it, and I would rather be shown one than
keep the claim.

## What this design costs

Fusion is not free, and the bill arrives on the write path. Every guard in the
middle of this piece exists because an edge is a path, and a system that lets
anything become an edge has let anything change every ranking.

A vocabulary that is wrong rejects facts that are true. Seventeen relations is
a small seed, so on a fresh corpus most of what arrives is novel, lands as
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
seven-step wizard that provisions the store and picks the embedder. That is
less work than standing up Graphiti, which asks you to bring your own Neo4j,
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
