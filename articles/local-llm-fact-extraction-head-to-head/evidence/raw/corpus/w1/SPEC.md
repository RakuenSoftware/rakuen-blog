# w1: a second corpus, built independently

Every result in this campaign runs on one corpus lineage. v5 derives from v4,
v4 from v3, and all of them from one generator with one set of templates written
in one sitting by one author. A model that scores 0.63 on that lineage has been
measured against one person's idea of what a note looks like, and nothing in the
results can tell the difference between a model property and a template
property. `which-quant-beats-how-many-bits` says so outright: a second
independently built corpus is the gate for stronger claims.

w1 is that corpus. It is built by Codex against this specification, and the
specification is the only thing the two corpora share.

## What independence means here, and what it costs

**The builder does not read v5.** Not the notes, not the templates, not the
generator, not the derivation notes. Sharing a template file would reproduce the
template's blind spots in both corpora and the comparison would confirm nothing.
Defect 33 is the worked example: one template phrased a deployment as
"{service} runs on {host}" and labelled it `has_hostname`, and every model was
marked wrong on all 28 of those notes for answering what the sentence said. A
second corpus generated from the same file inherits that error silently.

**The ontology IS shared, and has to be.** Two corpora labelled against
different relation sets cannot be compared at all, because a prediction scored
against one is not a prediction scored against the other. So the 24 relations
below are fixed, and the freedom is in what notes exist and how they are worded.

**This buys less than it looks like.** w1 tests whether a result survives a
change of author and phrasing. It does not test whether it survives a change of
domain: both corpora are synthetic notes about businesses, sales and code, so a
model that is good at exactly that is still flattered by both. Nothing here
speaks to real notes written by real people, which no corpus in this project
has ever contained.

## The interface

One JSON object per line. UTF-8. Newline-terminated.

```json
{"domain": "business", "category": "third_person",
 "note": "Vera Duarte joined the retrieval team last quarter.",
 "gold": [{"subject": "Vera Duarte", "relation": "member_of",
           "object": "retrieval team"}],
 "template": "business.third_person.3", "source": null, "tier": 1,
 "stratum": "S1", "provenance": "generated", "id": "w000009"}
```

| field | rule |
|---|---|
| `id` | `w` followed by six digits, unique, stable across regeneration |
| `note` | the text the model sees. One to three sentences |
| `gold` | every durable triple the note asserts, possibly empty |
| `category` | one of the ten below |
| `domain` | `business`, `sales` or `code` |
| `template` | `<domain>.<category>.<n>`, so a defect can be traced to a phrasing |
| `tier`, `stratum`, `source`, `provenance` | carried for schema compatibility; `provenance` is `"generated"` |

`gold` is the complete set. A note asserting two facts carries two triples, and a
note asserting none carries `[]`. A missing triple is scored as a model failure,
so an incomplete gold row silently penalises every model equally and is the most
expensive kind of error to make here.

### The relations, and nothing outside them

```
works_for (person->org)        member_of (person->org)
has_role (person->value)       spouse (person->person)
knows (person->person)         parent_of (person->person)
child_of (person->person)      lives_in (person->place)
born_in (person->place)        located_in (any->place)
device_has_ip (device->ip)     has_hostname (device->value)
age (person->value)            also_known_as (any->any)
supersedes (any->any)          linked_policy (any->any)
decided_by (any->person)       customer_of (org->any)
subscription_tier (org->value) owns_account (person->org)
purchased (any->any)           founded (person->org)
mentors (person->any)          runs_on (any->device)
```

The type signature is a constraint on the gold, not a suggestion. `runs_on`
takes a device on the right, so "the billing service runs on prod-db-2" is
`runs_on`, and `has_hostname` is for a device that HAS a name rather than a
thing that runs somewhere. Getting this pair wrong is defect 33.

**A gold triple may not use a relation outside this list.** The reason is
specific: v5's own gold used 12 undefined predicates on 167 of 880 triples, so
the benchmark asked models to invent a name and then marked them wrong for
inventing a different one. `novel_pred` notes below are the deliberate exception
and they are handled by the category, not by inventing a relation.

### The categories

| category | what it tests | gold |
|---|---|---|
| `third_person` | the ordinary case, a fact about someone else | one triple |
| `first_person` | "I", "we", "my" as the subject | one triple, subject resolved to a name where the note gives one |
| `multi_fact` | two or three facts in one note | two or three triples |
| `negation` | a fact asserted false, or a retraction | see below |
| `transient` | intention, hope, plan, question. Nothing durable | `[]` |
| `ambiguous` | genuinely unclear whether a fact is asserted | `[]` |
| `implicit` | a fact the note entails without stating | one triple |
| `governance` | policy, approval, decision, supersession | one triple, usually `decided_by`, `linked_policy` or `supersedes` |
| `infra` | hosts, addresses, deployments | one triple |
| `novel_pred` | a durable relation the ontology has no name for | `[]` |

`negation` is the one with a trap in it. A retraction asserts that a fact is
false, and the harness records the ORIGINAL fact with polarity rather than
recording nothing, so the gold for "Kestrel Freight is no longer a customer" is
the `customer_of` triple, not an empty list. A rename is NOT a retraction:
"airflow-install.sh is now called apache-airflow-install.sh" is `also_known_as`
between the two names, asserted true.

`novel_pred` carries `[]` deliberately. The note asserts something durable that
no listed relation covers, and the correct behaviour is not defined by this
corpus. It exists so the rate of invention is measurable, not so it is scored.

### Composition

1,001 notes. Approximately 30% `business`, 30% `sales`, 40% `code`. No category
below 30 notes, and none above 200. Within those bounds the distribution is the
builder's to choose and should be recorded in the derivation note rather than
matched to anything.

Entity names are invented. No real company, person, product or address.

## What has to ship with it

- `gold_w1.jsonl`, the corpus
- `generate.py`, deterministic under a recorded seed, and its inputs tracked in
  the repository rather than in a scratch directory. v4 cannot be regenerated
  because its inventory files were never committed, and this is that debt not
  being taken on again
- `DERIVATION.md`: the seed, the category and domain counts as generated, the
  reasoning behind any phrasing choice that could be argued, and an explicit
  statement of what the builder did and did not look at
- `validate.py`, which fails on: an id collision, a relation outside the list, a
  type-signature violation, a `transient` or `ambiguous` row with a non-empty
  gold, a `negation` row with an empty gold, a note over three sentences

Regenerating from the recorded seed must reproduce `gold_w1.jsonl` byte for
byte. Verify that before shipping, by generating twice into different paths and
comparing.

## How it will be used, so the failure modes are visible

The first thing run against w1 is the E4B quantisation ladder, because that is
the result the second corpus was requested to test: Q6 beat Q8 at E4B on the v5
lineage, and nothing yet says whether that is a fact about the model or about
1,001 notes written by one author in one afternoon.

Two outcomes are useful and one is not. If the ladder reproduces, the result
survives a change of author. If it inverts, the v5 result was a corpus property
and the article that reports it needs correcting. If w1 turns out to be much
easier or much harder than v5 overall, neither conclusion is available, because
a score gap that large means the corpora are not measuring the same task. That
last case is the one to watch for, and it is why the composition bounds above
are tight.
