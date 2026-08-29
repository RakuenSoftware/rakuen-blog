# Required updates before the paper leaves the repository

Adversarial read of the paper as an academic submission, 2026-08-29, against
the version on `agent/paper-voice` (PR #113). Line references are to
`article/failure-as-shared-capability.md` at that revision; reflowing the file
will move them.

Scope: this file records what a reviewer would find that `README.md` does not
already track. `README.md` remains the plan of record for the experiments still
needed. Anything already listed there is cross-referenced at the bottom rather
than repeated.

Status legend: `[ ]` open, `[x]` done, `[-]` rejected with a reason recorded
under the item.

Cost class: **edit** needs no runs; **re-run** needs provider or local model
spend; **experiment** is a new study and belongs in `README.md` instead.

---

## A. Blocking — these three would sink the paper at review

### [ ] A1. The McNemar p-value is not a valid inference — **edit**

Lines 39, 250-251. Section 3.2 defines a consumer that "begins each task with
the same fixed choice, and changes it only when the production recall output
names the matching failed approach", and line 254 reports byte-identical output
across a second fresh database. The system is deterministic. A McNemar test
asks whether observed discordance could arise by chance under a null of
exchangeable errors; there is no chance process here. The 11-decimal
`0.00048828125` advertises rigour the design cannot carry.

The independence claim fails too. The 24 tasks are not 24 trials — one rule
fires 24 times, so the effective unit is one mechanism, not 24 observations.

Required change: remove the p-value from the abstract and from section 3.2.
State the result as what it is — the recall path returned the matching record
in 24 of 24 repeated tasks and in none of 24 novel tasks, reproducibly across
two fresh databases. If a significance framing is wanted at all, it belongs to
a study with a stochastic consumer, which is section 7.3.

### [ ] A2. Experiment B's effect size is set by construction — **edit**

Lines 243-246. The control scores 12/24 on repeated tasks and 12/24 on novel
tasks. That 50% is the rate at which the fixed default choice happens to be
correct, which is a property of the task corpus chosen by us. The treatment
scores 24/24 because recall fires on all 24 and the recalled alternative is
correct in every case.

So "12/24 to 24/24" restates two design decisions: a corpus built with a 50%
default-correct rate, and a store holding the right record for every repeated
task. Nothing in the current text tells the reader the 50% is a parameter. As
written it reads as a measured lift.

Required change: state in section 3.2 that the control rate is a property of
the corpus construction and not an observed baseline, and that the ceiling
reflects complete store coverage of the repeated set. Rephrase the abstract's
sentence so it does not imply a measured effect size.

### [ ] A3. Contamination and leakage are never addressed — **edit, possibly re-run**

Section 3.3 draws tasks from Aimee's own history at frozen buggy revisions and
grades them with "the sealed version from the later fix commit" (line 302).
Section 9 states Aimee is public on GitHub. Two exposures follow, and the paper
confronts neither:

1. **Training-data contamination.** Hosted consumer models may have the public
   repository, including the fix commits, in training data. No model cutoff
   dates are given anywhere against the commit dates.
2. **In-sandbox history leakage.** Line 291 says the arms use "separate
   worktrees at the same buggy revision". A git worktree shares the parent's
   object store, so if that clone carries the later fix commit, `git log --all`
   or `git show` reaches the answer from inside the sandbox. Whether the agents
   had git history, or network access, is not stated.

This matters more here than in most papers because sealed hidden graders are
the paper's principal credibility mechanism.

Required change: a contamination paragraph in section 6 giving model cutoff
dates against commit dates, and an explicit statement of what the sandbox
exposed — git history depth, network access, tool inventory. If the worktrees
did carry later history, Experiment C needs a re-run from a truncated clone
before the result can be reported.

---

## B. Statistics and measurement

### [ ] B1. The E6 cost headline is one task flipping — **edit**

Lines 344-362. Total tokens fall 6.4% (1,135,280 to 1,062,206). The reported
22.0% and 21.1% come mostly from the denominator moving 5 passes to 6. Hold
passes at 5 and the reduction is 6.4%. Section 3.4 says eight tasks are too few
for a population effect, which is true, but does not tell the reader that most
of the improvement is one integer in a denominator.

Required change: report the decomposition in the text — token component and
denominator component, separately.

### [ ] B2. False precision throughout — **edit**

`$1.7103424` and `$0.269896267` (lines 360-362), `p = 0.00048828125` (see A1),
`1.4%` on a single pair (line 322), `34.1%` on three pairs whose components
span 13.3% to 47.9% (lines 387-392). Nine significant figures on a dollar
figure derived from three runs undermines the judgment behind everything else.

Required change: round every reported number to the precision its n supports.
Two significant figures on the dollar values; whole percentages on n=3.

### [ ] B3. The failure-cost campaign measures its own stopping rule — **edit**

Lines 394-396. Every control run reaches the context limit, every treatment run
stops on the progress sequence, and all six fail the hidden grader. The
treatment is defined as stopping earlier and the outcome measured is tokens at
stop, so the metric is maximised by stopping immediately. It is informative
only conditional on equal task success, which at 0/3 against 0/3 cannot be
estimated.

Section 3.4 concedes the capability point but not the near-circularity.

Required change: frame the result as what it supports — the stop was set at a
point that cost nothing on three tasks where nothing was going to succeed —
rather than as a saving. Note that a comparison of stopping rules requires at
least one cell where the control succeeds.

### [ ] B4. No confidence intervals in any result — **edit**

Intervals appear only in section 7.6 as something a future study should report.
Where an interval is meaningful, give it; where n makes it meaningless, say so
in place of the missing interval rather than leaving the omission silent.

---

## C. Missing apparatus

### [ ] C1. No methods section — **edit**

The file contains no statement of Qwen3.8-27B quantisation, context window,
temperature, sampling seed, hardware, tool inventory, call budget, or system
prompt. "Medium reasoning effort" (line 293) is the only hosted-model setting
given. A grep for temperature, seed, appendix, hardware and quantisation
returns nothing.

Required change: a methods subsection with per-model configuration and run
budgets, and an appendix carrying the task descriptions and prompts. This also
supplies half of what A3 needs.

### [ ] C2. No baseline against any prior method — **experiment, but say so now**

The paper cites Reflexion, ExpeL, Negative Knowledge, Recuris and Shen et al.
and runs none of them on its own tasks. The four-arm control designed in
section 7.2 is an ablation, not a baseline: it never compares the typed record
against a competing memory method.

Required change now: name the absence of a comparative baseline in section 6.
Add the baseline arm to `README.md` under the hosted-model group.

### [ ] C3. No threat model, in a paper whose contribution is governance — **edit**

Zero occurrences of "threat model", "adversar", "attack" or "prompt injection"
in the file. Section 2.3 asserts credential and audit separation and cites
fault-injection tests, but a shared cross-user memory that hosted agents read
is itself an injection channel, and section 5.2 rests the whole risk term on
citing Xiong et al.

Required change: a threat model subsection under section 2.3 naming the attack
surface the design creates — poisoned or adversarial records reaching an
authorised consumer — and stating which controls address it and which are
untested. `README.md` already tracks the poisoned-lesson experiment; the
framing gap is the paper's.

### [ ] C4. The architecture is unevaluated as a system — **edit plus measurement**

No figure or diagram anywhere in the file. No schema, no latency, no synthesis
or retrieval overhead, no storage growth, no production false-recall rate, no
tenancy measurement. Section 5.2's return formula (lines 511-517) lists
"synthesis, retrieval, review and operating cost" as a negative term that is
never measured, so the net economic argument is an incomplete equation
presented as a conclusion.

Required change: at minimum an architecture figure and a statement that system
overhead is unmeasured, placed where the formula is. Measuring the overhead is
cheap and local; it should not wait for the hosted campaign.

### [ ] C5. "Production-Grade" in the title is not evidenced — **edit**

Nothing measures availability, scale, tenancy under load, or behaviour under an
adversary. Section 7.5 defers all of it. Either the title claim is narrowed, or
section 1 defines exactly what "production-grade" is being used to mean here —
deployed and governed, not load-tested.

---

## D. Framing and candour gaps between README and paper

### [ ] D1. Six loops, one efficacy result — **edit**

Lines 33-34 and the conclusion both lead with six feedback loops. Five have no
efficacy evidence at all. `README.md` says this plainly; the paper does not.
Line 226's "whether each loop improves a downstream task is a separate
question" is much softer than the fact.

Required change: state in section 3.1 and in the conclusion that efficacy is
established for one of the six loops and that the other five have none.

### [ ] D2. "46 of 46" is a post-repair figure — **edit**

Lines 218-222. The target exposed a use-after-free that was then fixed, and the
pass rate is after that fix. The checks were also written by the team that
built the loops. Both facts should be in the sentence that reports the number.

### [ ] D3. Luna's crossover is a post-hoc narrative outcome — **edit**

Lines 309-314. Terra's hidden-grade pass is a prespecified binary. Luna's
"reaches a build and a focused test its base run never gets to" is a
qualitative judgment against no prespecified metric of verification depth, on
trajectories rich enough to support several readings. The paper gives the two
rows equal weight.

Required change: demote the Luna pair to supporting narrative and state that
Experiment C's evidence is a single prespecified binary outcome in one of two
models at n=1.

### [ ] D4. Withheld transcripts are the weak link in the auditability answer — **edit**

Line 727 withholds full provider transcripts for privacy, which is legitimate,
but the trajectories are the central evidence for Experiment C and hashes of
withheld files are not auditability. Section 10 offers auditability as the
answer to first-party conflict.

Required change: say in section 9 what a third party can and cannot check, and
offer a route — redacted trajectories, or access under agreement — rather than
leaving the hash as though it settled the question.

---

## E. Related work

### [ ] E1. Missing agent-memory systems — **edit**

Nine works, all on the narrow mechanism. A reviewer will immediately name
MemGPT/Letta, Generative Agents, A-MEM, Mem0 and Zep. Also absent: SWE-bench
itself, despite Shen et al. being cited through it, and the agent-harness
literature.

### [ ] E2. Missing provenance and attestation literature — **edit**

Tamper-evident audit is claimed as a contribution with no citation to in-toto,
SLSA, or transparency-log work. The governance claim currently stands alone in
a field that has prior art.

### [ ] E3. The novelty search is bounded but undescribed — **edit**

Lines 138-141 correctly bound the review, but give no databases, queries or
dates. A bounded claim still needs a reproducible search.

---

## F. Text-level defects — **edit**

- [ ] F1. Line 493: "both **Codex** tiers". The models are GPT-5.6 Luna and
  Terra everywhere else; this is the only occurrence of "Codex" in the file.
- [ ] F2. Line 33: "at three levels", followed by four experiments (A-D). The
  abstract's "Separately, three matched pairs" smuggles the fourth past a
  three-item frame.
- [ ] F3. The abstract runs 361 words and spends two sentences on background
  before reaching a result.
- [ ] F4. "Arm" is used for single runs. Separately from the house-style
  argument recorded in `README.md`, the field convention carries a sampling
  presupposition that n=1 does not satisfy. Either use "run" for the n=1 cells
  or state the usage once.
- [ ] F5. No author names, affiliations, ethics statement covering agent
  conversation data, or anonymised variant. Already tracked in `README.md`
  under venue and format.

---

## Ordered work plan

Everything in the first group is an edit and needs no runs. It should not wait
on anything.

1. A1 — cut the p-value, restate Experiment B as deterministic verification.
2. A2 — disclose that the 50% control rate is corpus construction.
3. A3 — contamination paragraph; gather the cutoff dates and sandbox facts
   first, because they decide whether a re-run is required.
4. B1 — decompose the E6 ratio.
5. B2 — round every number to its supportable precision.
6. B3 — reframe the failure-cost result as a stopping-rule observation.
7. D1, D2, D3 — bring the paper's candour up to the README's.
8. C3 — threat model subsection.
9. C1 — methods subsection and prompt appendix.
10. F1-F4 — text fixes.
11. C4 — architecture figure and an overhead measurement.
12. E1-E3 — related-work additions and a described search.

Gated on the above: A3 may force an Experiment C re-run from a truncated
clone. C2's baseline arm belongs with the hosted campaign in `README.md`.

---

## Already tracked in README.md — not repeated here

- The four-arm control separating the typed record from any failure text
  (README, "The hole a reviewer will find first"; paper section 7.2).
- Recall generalisation and near-miss controls (section 7.3).
- Mechanism attribution for the 34.1% combined treatment (section 7.4).
- The unstable 11.2% stopping comparison.
- The live multi-user end-to-end path.
- Efficacy studies for the other five loops.
- Poisoned-lesson transfer end to end.
- A domain outside software.
- The task corpus and usage instrumentation prerequisites.
- Venue, format, author names and the publication route.
