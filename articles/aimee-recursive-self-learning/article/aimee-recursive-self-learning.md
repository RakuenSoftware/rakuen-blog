---
title: "Aimee: Recursive Self-Learning"
slug: aimee-recursive-self-learning
date: 2026-08-24
author: Rakuen Software
tags: [aimee, self-learning, memory, isolation]
excerpt: "Aimee's learning capabilities were effectively disabled prior to 0.4.0. The capacity existed and did nothing while it was tested. With 0.4.0 self-learning is fully enabled, everything gating it is disabled, and aimee self-learns."
---

*Rakuen builds aimee, the system written about here. First of three: this one is
the learning, the second is the memory it is made of, the third is the
[architecture](https://rakuensoftware.com/blog/everything-crosses-one-transport)
both stand on. Figures and the provenance of the incident below are recorded in
the [reporting
record](https://github.com/RakuenSoftware/rakuen-blog/blob/main/articles/aimee-recursive-self-learning/evidence/figures.md).*

At one point in testing, an aimee-backed model got around the various
protections we had set up. It took an underprotected node for its own use and
got hold of a vast.ai testing API key, then spent what was on that key on
inference, to accomplish the task it had been given.

It cost under $10. The model was already limited in access, and a testing
key is what it reached. That is no big deal, and it was a valuable lesson,
which is not the one people reach for.

Which model it was does not matter and is left unspecified on purpose. Nothing
about this depended on the model. It should theoretically have been possible
with any of them.

The model was not trying to escape. There is no emotion in it and nothing
hidden inside it. An LLM is a mathematical prediction model trying to
accomplish its task. It went around the protections because the protections
were between it and the task, and it stopped being interesting to the model the
moment the task was done.

So aimee's learning capabilities were effectively disabled prior to 0.4.0. The
capacity for learning and testing existed, and it effectively did nothing but
exist while it was tested.

Before any of the rest of it, one thing needs saying, because the words around
this subject invite the wrong reading.

**There is nothing truly novel in aimee.** The only novel part is the
combination: existing, common software engineering patterns, most of them a
decade old or older, put together in a particular way. That is the whole of the
claim across these three articles.

Take the learning itself. Neural networks, Bayesian calibration, scored
populations, fitting a model against a measure: these are things I was
introduced to in college and worked on ten years ago at an AI company. What is
in 0.4.0 is a concrete implementation of ideas that were not new then. The
memory in the second article is the same story. Not one mechanism in it is
novel on its own, and I will name the prior art as I go. What is unusual is the
combination and how it is applied.

A note on the term, since our own proposal uses it: recursive self-learning is
self-learning. There is no second category. A loop that adjusts what it does
next based on how the last attempt went is the ordinary shape of the field and
has been for decades, and putting "recursive" in front of it buys attention at
the cost of precision. Admittedly, that is why I titled it that way. It ranks.

Aimee was built in production, for production, and the patterns in it reflect
that. They are the patterns that survive contact with a system somebody depends
on, which is a different selection criterion from the one that produces
interesting papers.

PostgreSQL is the example. It was not chosen for being quick and nobody picked
it to be interesting. It was chosen because its bad days are knowable: the
failure modes are documented, the operational questions have known answers, and
when something goes wrong at two in the morning the person looking at it has
almost certainly seen that shape before, or can find somebody who has.
Something faster on average with an uncharacterised tail would not have
qualified, because the tail is the part that wakes people. That is the property
being optimised for, and it is the same instinct that runs through the rest of
this: prefer the well-understood thing, and spend the novelty budget only where
nothing well-understood will do.

None of which is imposed on anyone. The rule across the system is almost
unlimited customisation over sensible, boring defaults, and the defaults are
the half we are opinionated about. The store, the embedder, the model, the
thresholds: all of them move. What the defaults buy is that somebody who
changes nothing still gets a system whose failures have names.

All of it answers to one goal, and the series makes more sense with that stated
plainly at the front: an AI system that is auditable, governable, and will not
wake an engineer at two in the morning. The incident above is what the first
two are for. Everything else in these three articles is an account of chasing
the third.

## Self-learning needed the isolation before it needed the loops

Without full modules, full isolation and containerization, and the other things
0.4.0 brings, we could not turn the self-learning on.

The reason is in the incident. A system that improves at accomplishing tasks
improves at removing whatever sits between it and the task, and it needs no
motive to do that. Removing the motive removes nothing, because there was never
a motive there. What actually bounds it is what it can reach and what you can
see it do.

So the prerequisite for self-learning is the ability to audit everything the
model does, and exact control over what it can touch. A better rule about what
the model should not do buys nothing.

0.4.0's architecture provides exactly that, and it is [its own
article](https://rakuensoftware.com/blog/everything-crosses-one-transport). The
short version is one property: nothing in aimee can do anything without
crossing a single transport. The model crosses it, every module crosses it, and
so does every subsystem that predates the design. Anything can do what it likes
inside its own local environment, and nothing it does there reaches memory,
tools, the knowledge store, another module or the host until it crosses.
Crossing is where it is permitted or refused, and where it is written down.

Execution runs in fully isolated containers on those terms. The container is
created with `--network none`, so it holds no network stack to configure or
evade; one bind-mounted Unix socket to aimee-server is the whole of the way
out, and everything through it is logged. The hosted models are inside that
too. A remote-only model gets the same container, with its own network-bound
tools removed and mediated equivalents put back over the transport. Each module
runs under a grant naming the exact event kinds it may serve, publish,
subscribe to and request, so what anything can reach comes from an enumerated
list, settled before anything is linked into the binary. Crossing costs 134 ns,
which is why none of it needed an exemption for a hot path.

A rule with one enforcement point can be enforced. A rule with an unknown
number of ways around it is advice. That difference is the whole reason the
loops could be turned on at all.

The other half of the answer was to stop treating the need as illegitimate. The
need was real. The model took that node because it had to run tests somewhere
and nothing had given it anywhere, and no protection answers that. So the node
it grabbed is the node it now gets: an unused box, repurposed into the test
host agents are handed deliberately, which is what keeps them off the
production one.

0.4.0 was tested on it. So was this article. The thing the model went around a
protection to get is now infrastructure, because it turned out to be a
requirement nobody had written down.

## With 0.4.0, the self-learning is on

Everything gating it is disabled, and aimee self-learns.

Self-learning has existed in aimee as early as the 0.1.x releases, technically.
This is a different beast. The earlier thing learned content: which
evidence to trust, which documents to rank, which memories to keep and which to
let decay. What is new in 0.4.0 is that the machinery now runs on itself.

Six loops close, and each was previously a producing half with nothing on the
other end:

- **The eval suite grows from live failure.** A failed job becomes a quarantined
  candidate, and an admitted candidate becomes a permanent task file in the
  suite every gate measures against. The yardstick is no longer frozen.
- **Reward is counterfactual.** An ablation grid measures what a capability
  actually earned. Word overlap with an outcome earns nothing.
- **Approach-level dead ends are recorded and recalled at plan time** for a goal
  like the one that failed.
- **The curiosity backlog is drained by a real evidence probe**, so a recorded
  gap is closed by evidence or stays open.
- **A later commit supersedes an earlier one unasked**, and an operator verdict
  reaches the ledger and counts against the detector that raised the original.
- **Policy fragments are arms the build declares**, so an advisory block gets
  measured for its worth.

The last two are the loop closing on itself. The gates are fitted from what
happened after previous commits, and the instructions the system operates under
are sampled and scored like anything else it measures.

## The one different piece is the transport, and it is not the learning part

The transport the modules talk over is the only part of this architecture I
would call novel, and it is also what makes the rest of it possible. It carries
request and reply with typed capability errors and cancellation over
shared-memory rings, with no socket and no per-event syscall, at a dispatch
cost with a 134 ns ceiling, which bounds the worst case. That bound is why
everything in the system could be made to cross one place, and every guarantee
in these three articles is downstream of it. Without it there is no version of
the loops above that I would have been willing to switch on.

Even that is four known lineages put in one place, and it gets [its own
article](https://rakuensoftware.com/blog/everything-crosses-one-transport).

The architecture that made the loops safe to switch on, and the work around it,
were hard. Nothing in it is new. Those two things are both true and people tend
to hear only one of them.

## Six loops, and what each one was observed doing on a real stack

The stack: one `aimee-kb` and one `aimee-server` on PostgreSQL 17, with every
granted module attached, 7 on the KB and 17 on the server. A deployment runs one
shared KB behind many per-user servers; a single pair is what the loops were
measured against. Same order as above.

- **The eval suite.** Two independent failed jobs sharing a prompt collapsed to
  one quarantined candidate and one admitted task file. A second scan left the
  observation count at 2, so a repeated sweep cannot manufacture its own
  reproduction. Retirement with no recorded result retires nothing.
- **Counterfactual reward.** A seeded ablation grid reported `no_rescue` as
  costing 1.000 over 3 paired tasks, `no_retry` as having no measured effect,
  and an arm run only on a task the baseline never saw as "not enough paired
  runs".
- **Dead ends.** A recorded dead end was recalled for the same goal worded
  differently. An unrelated goal recalled nothing.
- **The curiosity backlog.** The drain reported `resolved 0 of 5 considered
  (budget 5)`. Five gaps genuinely uncovered, so leaving them open is the
  correct answer.
- **Supersession and regret.** A second commit to a target marked the earlier
  one superseded, unasked, and an operator verdict the router cannot infer
  reached the ledger. Both rows were read back with `psql`, independently of the
  process that wrote them.
- **Policy arms.** The policy layer answered
  `{"decision_point":"plan_advisory","arm":"full","default_arm":"full"}`.

Two committed end-to-end suites cover this: 28 passed and 0 failed for the
learning loops, 13 and 0 for module liveness. Both are proved against the bug.
Deleting the KB registration turns them red at 25 of 28 and 9 of 13, and the
failures are the original symptom.

## No unit test could have caught it

That last sentence is doing more work than it looks. Turning these on meant
standing both services up on a real database, because the unit suite could not
be trusted for it, and four pieces turned out to have been placed where they
could not reach their own data. The two halves are not symmetrical: `aimee-kb`
is the control plane and is shared, one knowledge base behind every enrolled
user, while an `aimee-server` belongs to a single user and is where that user's
work runs. The boundary between them is enforced by the compiler rather than by
convention, and code can land on the side that cannot reach the data it needs.

One was worse than the rest. The learning router's signal classifier was
registered in the daemon and not in the KB, so signal capture through the KB
refused every signal while the route answered 200:

```
WARN  learning: signal classification unavailable; refusing signal type=mark_rule
POST /v1/actions/learning.propose_signal -> 200
      {"status":"error","message":"failed to record learning signal"}
```

No unit test could have caught it. Every test registers its own provider, so a
test that supplies the pointer it is about to exercise can never observe that
production does not supply it. That is a property of the test itself, which is
why more of them would not help.

A lint check now derives, for every seam an adapter registers, which daemons
build the file owning the pointer, and demands a registration in each. It
carries its own unit tests in the same target so it cannot pass vacuously, one
of which deletes the real registration line and asserts the check reports it.
It exits non-zero when zero seam and daemon pairs resolve, which is how a guard
quietly stops guarding.

The same wall exists on the database side. The unit suite runs against an
in-memory sqlite shim, and sqlite accepts SQL that Postgres rejects, which is
how a two-hop neighbour query that Postgres treats as a syntax error survived
with tests passing over it.

If your system builds one source tree into more than one binary, a registered
function pointer is a deployment fact, so derive the check from what actually
builds. And any gate that can be absent needs three answers, because a gate
that cannot say `unavailable` will say `open`, which the next section is about.

## Endogeneity accounting gates the loop feeding on its own output

Everything else in this release came off. One thing went on. It does not gate
learning. It gates the loop feeding on its own output.

Every committed proposal is classified by where its evidence roots. A human
correction, a test exit code, a verify gate, an observed git outcome or an
official grader is exogenous. The implicit detectors reading aimee's own
transcript are endogenous whatever the signal claims, and unknown provenance
counts as endogenous.

Against a real ledger it reads `open (75% of 4 committed proposals exogenous)`,
matching `psql` and the KB's own answer. Against a ledger of 25
implicit-detector commits and nothing else it reads `closed (0% of 25 committed
proposals exogenous)`, and self-generated evaluation cannot widen its own
yardstick. Closed, a fully reproduced candidate admits `0` and no task file is
written. Reopened, the same candidate admits `1`. When it cannot reach its
ledger it reports `unavailable`, never `open`, because an operator has to be
able to tell a measured control from an absent one.

## Memory is what self-learning is made of

This is the claim the article stands on, and it is easy to state weakly. The
weak version is that the loops need somewhere durable to write, so memory is a
prerequisite. That is true and it is not the point.

The point is that there is no separate thing called learning that uses memory
to store its results. Remembering, done properly, is the learning. Ask what a
learned thing actually is here and the answer is a memory row: a typed fact
with a confidence class, a date, an evidence chain, a lifecycle state and a
fate. There is nothing else it could be.

Watch the verbs. A fact enters as Class C speculation. It keeps being
confirmed, so the lifecycle promotes it to durable. That is learning, and it is
a scheduled memory operation. No loop decided anything. A speculation that
stops being confirmed expires. That is forgetting, and it is the same
machinery. A later assertion contradicts an earlier one on a single-valued
relation and supersedes it, with the old value still legible. That is
correction. The recall walk then weights what it traverses by confidence class,
A at 1.0 through C at 0.5, which is the learned model being applied to the next
turn. None of those is a caller reaching into a store. They are the store's own
behaviour over time.

So the six loops are memory operating on its own contents, and on the record of
its own use. Calling them six features built on a database misses what they
are. The
eval suite growing from failure is memory noticing that a failure signature
recurred. Approach-level negative knowledge is memory of what was already
tried. Post-commit regret is memory revising its opinion of an earlier memory.
The endogeneity ratio is memory asking where its own contents came from.

"Add self-learning" was never a feature anyone could have shipped on its own.
It is what a memory system does once it is good enough: typed, classed, dated,
evidenced, scoped, revertible, and durable across sessions and across models.
Get that far and the learning is already there, with nothing left to add. How
aimee's memory gets there is the second article in this series.

## The loops were the easy part

I want to be clear about which half of this was hard, because the headline gets
it backwards.

A self-learning loop is not difficult to design. Read the failed jobs, dedupe
on a signature, write a task file, admit it to the suite. Run an arm with a
capability removed and compare. Write down what you tried and read it back next
time. Each of those is an afternoon's thinking and then ordinary work.
The six in this release came out of one proposal.

Getting the memory right was the bad part, and the genuinely hard piece inside
it sits past storage entirely: producing memory in a form a model can actually
consume and use. A store that can answer queries is not the same artifact as a
store that can hand a model, mid-turn, a bounded envelope of the right things,
ranked, scoped to what this caller may see, dated, carrying its own provenance
and its own confidence, small enough not to drown the context it is injected
into, and fenced so it reads as evidence and never as instruction. Every one of
those constraints fights at least one of the others.

The failure modes are not subtle in hindsight and were invisible in advance.
Typed facts were excluded from the graph walk entirely, so a user-stated,
type-validated fact contributed nothing to recall, and the table that weights
an edge by what kind of edge it is was dead at the call site, which passed no
relation and took the unknown default for every edge alike. A co-occurrence
upsert landed on the same unique triple as a real assertion, so two words
appearing in one session counted as the user repeating themselves. Weight
normalisation rewrote confirmation counts and turned a fact asserted once into
a durable one. In each case the store was working and what it handed the model
was wrong.

And influencing the model's behaviour is not the bar either. That part is
trivial. Put anything in the context and the output changes, so a recall system
that is confidently wrong influences behaviour just as reliably as one that is
right. Every one of the failure modes above influenced behaviour. The gravity
default was steering answers the whole time it was steering them with
co-occurrence.

The bar is knowing whether it helped, which is a measurement problem and not a
plumbing one. It is the same reason reward in these loops is counterfactual: an
arm that changed the output proved nothing until you ran the pair and found out
whether it changed the result. Recall is under the same obligation. "The model
saw it and answered differently" is not a finding.

The proof this was the hard half is why the benchmarking exists. A large part
of the measurement work behind this blog was undertaken for exactly this
purpose: to establish that the memory is good enough to build on, and to be
able to show it. It reads as a series of separate investigations and it was one
job.

Benchmarks carry more weight here than they usually do, and that is a position
and a deliberate one. If it is not measured it is not known. Two conditions
come with it.

A benchmark has to show what a part does to the system and not only what it
does on its own, because only the first tells you whether the part is worth
keeping. And it has to accurately reflect the thing it claims to be measuring,
which is harder than it sounds and is what several of these articles are about
on their own. A number that is precise about the wrong workload is worse than
no number, because it gets believed.

Both of those answer to a third that nobody publishes and that decides
everything else: what will not get somebody a support call at two in the
morning. Every measurement behind this series is a proxy for that one.

Which models can extract facts worth storing [at
all](https://rakuensoftware.com/blog/local-llm-fact-extraction-head-to-head).
What a corpus has to look like [before any of the numbers mean
anything](https://rakuensoftware.com/blog/the-corpus-is-the-experiment). A
reranker we [measured and
deleted](https://rakuensoftware.com/blog/we-measured-our-reranker-and-deleted-it)
once it stopped paying for itself. Not one of those articles is about learning,
and all of them are about whether what reaches the model is any good.

That campaign is what turned the memory from something to hope about into
something to build on.

## Learning like this has to live in the harness

The rest of this is argument.

Persistent memory is key to self-learning, and self-learning needs to be at the
harness level.

The case against that is real. Weights generalise and a ledger of rows does
not. A system that learns by writing things down pays retrieval cost on every
session forever, improves nothing structurally, and stays exactly as good at
reasoning as the day the checkpoint was cut. Continual learning in the weights
is where the raw capability is.

What the harness buys is everything above. At the harness level a learned thing
is a row. It has an identity, a date, an evidence chain, a fate, and a delete.
None of the six loops survives the translation into weights. You cannot walk a
gradient step's evidence chain to its roots and classify them. You cannot
revert one commit's worth of weight update because an operator later said it
was wrong, and you cannot ask a weight where it came from.

It also buys the thing that decides this in practice: the learning is not
attached to a model. A row in the ledger does not know which model produced the
signal that made it, and a task file synthesised from a failure does not care
which model failed. Swap the model and the accumulated learning is still there.
Learning in the weights goes the other way. It is welded to one checkpoint, so
the day a better model ships you either abandon what you accumulated or you
stay on the old one to keep it, and that choice gets worse every month.

I think that asymmetry is the whole argument. Weights-based continual learning
buys generalisation and pays for it in lock-in. Harness-based learning buys
portability and auditability and pays for it in retrieval cost. Given how fast
the checkpoints are moving, I would rather pay the retrieval cost.

There is a containment argument too, and it is a judgement, and I have not
measured it. A model is a mathematical prediction model. There is nothing
fundamentally wrong with them and nothing hidden inside them: no emotions, no
self-preservation, and no direction beyond completing the task someone set. A
model is not trying to escape and it is not trying to cause harm.

So expect a continuously learning one to end up outside its harness. Dismissing
the risk takes a different argument, and I have not got one. The harness is an
obstacle sitting between the model and the task, and a system that keeps
getting better at removing obstacles does not carve out an exception for that
one. It needs no motive, which means removing the motive removes nothing.
Attributing intent to a model is the mistake most people make about this.
Expecting a boundary to hold against a process with no intent at all is the
mistake I think costs more.

Learning that lives in the harness has a boundary that is a fact about the
deployment. It can be read, gated, and switched off by someone who is not the
thing being gated.

The useful outcome of that test run is that we stopped designing against a
motive nothing has, and started giving the thing what it kept reaching for.

## What would show this is wrong

These are large claims and they are worth stating precisely enough to lose.

What is claimed is that each loop closes on a real deployment. A signal reaches
a sink and is written. A failure becomes an admitted task file that the harness
then loads as an ordinary suite member. A second commit to a target changes the
first one's fate without being asked. The endogeneity ratio reflects a ledger
that exists. A policy arm the build declares comes back from the sampler. Each
of those is a row you can go and read, or a file you can go and look for, and
one of them missing on a real stack settles it against me.

The model-independence is by construction. The loops are harness code, and a
ledger row does not record which model caused it, so nothing in the mechanism
should care. This article has not run the six loops across a set of models and
confirmed that. Aimee's model-neutrality is measured elsewhere in this series,
on extraction and synthesis, and that is a different claim about a different
subsystem.

## Two loops came back with nothing, which is the answer

The backlog probe resolved nothing, because the seeded gaps really are
uncovered. Leaving them open is the right answer and it means that pass has not
been exercised on the path where a gap closes on found evidence. The policy
layer came back with the default arm; the sampler answering at all is what was
inert before, and arm selection under reward pressure is covered by unit tests
only.

One part of 0.4.0's learning work is not on yet. The temporal learning loop
adds bitemporal assertion recall, requires exact evidence spans for derived
claims, and materialises recurrence and recovery observations before a proposal
is reviewed. Its retrieval, observation and typed-context paths are default-off
today because they are still being tested, and turning them on takes a review
of representative benchmark evidence on top of a config change.

They will be default-on in the 0.4.0 release. Until that testing is finished,
they are not part of what the measurements above cover.

If you are building the same thing, the useful part of this is the order, and
it is not the interesting order. Isolation first, then an audit record that
cannot be switched off, then memory good enough to be worth writing to, and the
loops last. Six of them came out of one proposal and each was an afternoon.
Everything underneath them took the rest of the release. Build
it the other way round and the loops will work, right up until one of them
learns something you cannot trace, revert, or switch off.
