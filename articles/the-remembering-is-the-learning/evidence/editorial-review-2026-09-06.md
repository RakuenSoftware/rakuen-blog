# Editorial review, 6 September 2026

Reviewed the article at `8509c8b36ba9cd2419f85fde4db4d8f350d8e7a0`,
against Part I and Part III of `voice-guide/VOICE.md` and Part I of
`voice-guide/ARTICLE.md`, including the guide's existing uncommitted rules on
antithesis and demonstrative openers. Line references below refer to that
378-line article. The article was unchanged when this review was recorded;
the implementation note at the end describes the subsequent revision.

This is an editorial and reporting-record review. It includes no new runtime
test or implementation audit. Technical questions below identify claims to
clarify or verify; they are not newly established implementation defects.

## The main revision

The article's strongest argument is that remembered experience changes what a
later run attempts, trusts and corrects. Its strongest evidence is the account
of defects that changed those decisions while ordinary reads and writes kept
working. Give those consequences more space and remove the sentences that
repeatedly announce that the machinery constitutes learning.

The author's additional observation about failure learning gives this argument
a practical centre. Knowing that several approaches failed can narrow a later
search. A successful approach may depend on the exact conditions that made it
work. The memory machinery has to preserve enough context to tell whether a
previous failure applies now.

Keep the title. Define what learning means in this article early: stored
experience changes a later decision. Then distinguish the rules governing that
change from the state or fitted parameters that change through experience.
Authority checks and scope filtering govern learning. A retained failure,
changed lifecycle state or fitted ranking weight can affect what subsequent
work does. Calling every operation learning obscures the relationship between
them.

## The author's observation about failures

The author supplied this account during the review on 6 September 2026:

> The best possible learning is in failures for models, not successes. Failures
> are (more) generally applicable then successes, and it seems to be more
> important for a model to know what not to do for generalized use.

The author clarified:

> A model already knowing X, Y, and Z failed extracts more value then just
> knowing that A succeeded...unless A was that exact same task.

These are direct author statements about a recurring observation from use.
No comparative measurement, task sample, model version or raw artifact was
supplied with them. Preserve the observation with that evidentiary weight.

Suggested article wording, for review:

> In our use, models have gained more from remembering failed approaches. A
> successful approach can be useful when the same task returns. Knowing which
> routes failed can also narrow the search on a different task, provided the
> conditions that caused the failure still apply.

This keeps the author's asymmetry without asserting a universal ranking of all
learning signals. The condition is essential: a timeout, an unavailable tool,
an invalid premise and a rejected operation teach different lessons. A failure
record should distinguish the attempted route, observed result, relevant
conditions and any established cause. An unexplained failure still belongs in
memory, with the uncertainty attached.

For this article, the useful question is what happens to that record next:
which task retrieves it, how its scope is bounded, what corroboration changes,
and how a later correction withdraws an obsolete restriction. Explain the
relationship between failed work and outcome-based demotion. A record of an
unsuccessful attempt can be useful evidence. The attempt's failure does not by
itself mean that recalling its record was harmful.

The existing paired study in Article One isolates the effect of a learned
failure record under a fixed consumer. Repeated tasks improved from 12/24 to
24/24; new tasks stayed at 12/24 in both conditions. It did not compare failure
memory against success memory and does not establish the broader transfer
claim. Keep those results in their present home. A short local description and
link are sufficient here.

If the author wants a measured comparative claim later, compare failure-only,
success-only and no-history conditions on held-out tasks sharing an underlying
constraint with earlier tasks. Match the information budget and distinguish
repeated tasks from changed conditions. Include cases where a previously failed
route becomes valid, so the measurement also catches unjustified avoidance.
That study is a proposed follow-up, not a prerequisite for publishing the
clearly attributed observation.

## Opening and argument

**Restore orientation, then state the operational claim (lines 12–36).** The
disclosure sends readers to three other articles before telling them what Aimee
is. The body starts with five properties of a learned object. Add a compact
project definition using the established description in Article One, then say
what remembering changes in a later task. The README says this orientation was
restored, but it is absent from the reviewed text.

Reduce the series numbering to a short navigation note. Keep the company
disclosure and source provenance visible. The architecture article is absent
from both `articles/PUBLISHED` and `articles/REVIEW`; remove the live-link
assumption or supply a verified destination. This is a repository-state check,
not an HTTP check.

**Give the reader one example to carry through the machinery.** Prefer a
documented failure record if one can be selected from existing reporting. Show
the failed approach and its conditions, its admission into memory, its recall
for a later task, and what would invalidate the lesson. Do not invent a test
result or imply that every mechanism described participated in one run.

For correction authority, a small explicitly illustrative employment example
can do separate work: a person states an employer; a model extracts a conflicting
employer; a later authenticated user statement corrects the first value. This
makes class ordering and retained history readable without inventing an
observed incident. Keep it short enough that the article retains one main
example.

**State the actual cost of caution (lines 346–361).** The current closing calls
slowness protective and cheaper than rebuilding trust. It does not give the
reader the strongest opposing case: cautious memory can preserve an outdated
human assertion, delay a useful new relation, or withhold a useful inference.
Explain the relevant correction or approval route. Present the cost as an
engineering tradeoff; no measurement here prices delay against lost trust.

## Claims to clarify before polishing

| location | problem in the prose | recommended treatment |
| --- | --- | --- |
| 40–62, authority classes | "Full confidence" can be read as certainty that a person's claim is true. The prose also alternates between authority class and confidence class. | Name what the class controls. Distinguish authenticated provenance and precedence from factual correctness. Verify the precise meaning of the confidence field before paraphrasing it as probability. |
| 66–77, promotion and expiry | Durability, authority and truth are close enough in the prose to appear interchangeable. | Keep the concrete rule that a reinforced Class B fact remains Class B. Explain what expiry changes operationally; a lack of reinforcement alone does not establish a contrary fact. |
| 79–90, confirmation defects | The numerical corruption is concrete, but "stopped anything ever expiring" is an unbounded conclusion. The paragraph never explicitly closes with the fix and release status. | Bound the effect to the affected facts or lifecycle path, as the evidence permits. State the documented fix, retaining the observed counts and continued successful reads and writes. |
| 107–117, authority escalation | A model-composed query is a strong example, but actual exploitation and an available exploit are different claims. | Retain "could have" unless there is an observed exploit. Link the fix and identify the affected write paths in the evidence record. |
| 119–122, two clocks | The clock definitions are useful; the final comparison to a log adds an unsupported categorical distinction. | End after the two questions the retained timestamps can answer. |
| 141–155, vocabulary activation | "Signed" may imply a cryptographic signature. The reporting record establishes an authenticated actor and a ledger entry. | Use "approved by an authenticated actor and recorded in the ledger" unless signature evidence is supplied. Define actor separately from person. |
| 192–205, ranking | Fitted ranking weights and fixed class multipliers appear as one learned trust model. Several listed score inputs concern relevance. | Identify what is fitted, what is configured and what each affects. Keep the 0.80 baseline and class multipliers adjacent if the arithmetic serves the explanation. Move the thirteen-term inventory to a compact reference note or retain its reporting-record home. |
| 217–242 and 246–265, scope | The prose moves from visibility constraints to evidence-driven scope expansion without saying who permits wider disclosure. "Independent work" also sounds stronger than a count of distinct sessions or sources. | Explain whether scope promotion remains within an authorised audience and which authority permits it. Define what distinct sources establish. Do not equate distinct identifiers with independent corroboration without support. |
| 246–261, current feature state | "Two of the three mechanisms" behind switches is hard to reconcile with the later statement that one of the three was removed. | Describe current pattern synthesis, entity promotion and vocabulary activation separately, with each gate attached. Keep the obsolete three-sighting rule in the vocabulary passage only. |
| 269–284, outcome attribution | Placement in context, use in an answer and causal benefit are different observations. "Counterfactual discipline" implies a comparison not described here. | Explain how attribution is obtained and what its limits are. Use "attributed outcome evidence" until the counterfactual mechanism is demonstrated. Distinguish a useful memory of failure from a memory whose use caused failure. |
| 286–288, contradiction handling | "Not resolved by picking a winner" is immediately followed by a policy choosing the current value. | State both operations directly: policy selects the current value and preserves the conflicting claims with their sources. |
| 302–309 versus 227–234, evidence and directives | Recalled material is described as untrusted evidence, while approved directives receive high prompt priority. | Name the two paths and the approval that permits an instruction to enter the directive path. Avoid an apparent universal claim that all remembered material has the same role. |
| 316–344, deletion and reversal | Mistaken deletion is called unrecoverable near a description of retained rows and compensating reverts. | Distinguish supersession, logical retirement, compensating reversal and content purge. State which operation each safety claim concerns. |
| 340–344, model weights | "A gradient step has no evidence chain" and a weight update cannot be reverted are broad comparison claims. | Specify the required capability, such as withdrawing one learned claim while retaining unrelated later learning. Support any model-weight comparison at that level or leave it to Article One. |
| 373–378, closing advice | "Cheap to establish on the first day" has no cost evidence, and the final sentence restates the title. | End with a concrete requirement for future correction: preserve the source, scope and history needed to revise a fact after it has been used. |

## Structure and pacing

The body has 2,996 whitespace-separated words after reducing Markdown links to
their labels, including headings, the disclosure and table text. There are
fourteen mechanism headings. Section body counts range from 64 to 378 words.
The closing warning occupies 280 words; the central account of demotion gets
169. Word counts diagnose the weighting, not a target length.

Recommended sequence, with headings to be written after the paragraphs move:

1. **Experience changes the next attempt.** Orient the reader, define the claim,
   introduce the author's failure-learning observation with its limits, and give
   the reader a concrete record to follow.
2. **Authority controls what a new claim can replace.** Classes, extraction
   limits, vocabulary admission, identity and the employment illustration where
   needed. Preserve the authority-escalation example and its resolution.
3. **Evidence changes how long a claim remains usable.** Promotion, expiry and
   the confirmation-count defects. Explain how a failure lesson can become
   stale and what qualifies it for continued use.
4. **Recall determines whether the lesson reaches another task.** Retrieval,
   fitted ranking, class multipliers and the two graph-fusion defects. Follow
   into outcome attribution and demotion. Put error propagation beside graph
   expansion, where its mechanism is already visible.
5. **Sharing a lesson changes who can receive it.** Scope filtering, tiers and
   cross-session synthesis, with present gates and authorisation boundaries
   stated separately. Explain the directive/evidence distinction here or beside
   recall, whichever keeps its enforcement and consequence together.
6. **Correction has to reach what the old claim produced.** Retained history,
   derived staleness and the evidence ledger. Attach provider failure behaviour
   to the decision it protects. End with the cost of caution and a concrete
   design requirement, without retelling the two known limits.

This is a proposed reading order, not six containers for the existing text.
Move paragraphs first. The 64-word propagation and 72-word evidence-fence
sections are candidates to join their parent arguments. The 378-word vocabulary
section can lose repeated descriptions of named approval while retaining its
removed code guard and current limit. Preserve any deliberate authorial line
unless its meaning, placement or support warrants a change.

## Sentence-level work

The new examples have been added to `voice-guide/VOICE.md`. Existing rules
already cover antithesis, demonstrative openers and flat triads; those additions
were preserved.

| draft | suggested action or replacement |
| --- | --- |
| "Those operations are the claim" (28) | State the claim directly, once the opening has defined learning. |
| "This article follows that machinery" (30) | Delete the itinerary; use the space for the practical consequence. |
| "They are ordinary memory maintenance and also the learning process" (70–71) | Delete after showing the actual promotion or expiry decision. |
| "repetition buys durability, not authority" (73–74) | "Reinforcement can make a Class B fact durable. It remains Class B." |
| "something named signs" (154) | "The ledger records the authenticated actor who approved activation." |
| "That door and the queue differ in bulk rather than in kind" (164) | "An operator can also import a domain vocabulary from documentation." Verify and retain any distinct approval conditions. |
| "Of the three thresholds this article started with" (260) | Delete the reference to drafting history. Attach each current threshold to its mechanism. |
| "The loop closes on a timescale no session can see" (264–265) | Keep the preceding concrete example of a later engineer receiving the lesson, scoped as a design capability. |
| "Here the architecture in part three meets the lifecycle in this article" (322) | Delete. The next sentence states the dependency. |
| "identity, date, evidence chain, fate and delete" (340–341) | Name the lifecycle and deletion operations where their meanings differ. Avoid turning a list into a refrain. |
| "Both limits are known" (369) | Delete the announcement. Give each limit one home beside its mechanism. |

Avoid an indiscriminate simplification pass. "Reads and writes continued to work
throughout" earns its short landing because it supplies a specific operational
consequence. The `works_for` refusal is a useful negative statement of a real
boundary. Neither needs replacement to satisfy a pattern counter.

## Reporting to preserve and records to reconcile

Any future rewrite must record the disposition of the existing reporting under
`articles/AGENTS.md`. In particular, preserve:

- The observed confirmation changes from 1 to 20 and 2 to 100, and the separate
  co-occurrence collision.
- The authority-escalation paths and the distinction between possible and
  observed misuse.
- The two graph-fusion defects: excluded typed facts and omitted relation names.
- The vocabulary change, attributable activation and removed catch-all guard.
- The extraction limit, class ordering, correction clocks, reversible merges,
  scope filtering, tiers, outcome exclusions and lifecycle evidence.
- The conditions attached to numerical ranking and promotion rules, including
  which defaults remain unverified.

At the review stage, the article, historical ledger and raw reporting artifacts
were unchanged. The subsequent rewrite has its own disposition inventory.

The article's source note says 24 August; its reporting record contains later
checks at `958af1c5` and `6bcc87e`. The README treats a moving `testing` branch as
a sufficient release pin. Reconcile the note with the actual immutable source
revisions used, keeping historical entries intact. The README's old word count
and its statement that the opening contains a project definition also need
updating when the article is revised.

The evidence record describes four of five decisions as having no local
substitute, with a separate embedding contract. Check the breadth of the
article's "Every decision" heading against that recorded exception. Its record
also preserves an older pending comparison decision that the README says was
settled. An additive current-status note can resolve that without erasing the
history.

Validation for this review: read the article, companion study summary, article
README, reporting record, publication/review manifests and relevant guide
sections. The existing `tools/voice_gate.py` reports PASS for the unchanged
article. That check catches surface issues; it does not assess the argument,
the claim boundaries or the recurring tics described above.

## Implementation, 2026-09-06

The user requested a PR with the updates. The revised article uses an explicitly
illustrative compiler failure to connect the author's observation about
transfer, the need for relevant conditions, recall and later correction.
It distinguishes the outcome of a failed attempt from the usefulness of
remembering it, and keeps the limits of the existing study adjacent to its
description.

Eight sections replace fourteen. The rewrite retains the reported defects and
their figures, the extraction and catch-all limits, and the mechanisms recorded
in the [pre-rewrite inventory](figures.md#failure-learning-revision-inventory-2026-09-06).
It restores project orientation, removes the unavailable architecture link,
separates fitted ranking weights from class multipliers, and narrows claims
about signing, outcome attribution and reversal. Scope-promotion authorisation
remains an explicit verification item in the article and README.

The revised body contains 2,672 whitespace-separated words with Markdown links
reduced to labels, including headings, table text and disclosure. The article
passes the existing voice gate. Whitespace checks pass for the changed
documents. No runtime code changed, and no new runtime result is claimed.
