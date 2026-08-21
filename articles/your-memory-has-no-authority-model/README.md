# Agent Memory Needs an Authority Model

An architecture piece. `aimee` holds conversations, typed facts and source code
in one graph ranked by one query, with scope ranked inside recall and two clocks
on facts. Every guard on its write path exists because an edge is a path.

Around that: thirteen inspectable implementations read at pinned commits on 20
and 21 August 2026, plus A-MEM as a research reference. Supermemory is recorded
separately because its public repository distributes the memory engine as a
packaged server binary rather than exposing its implementation source.

## Status

Draft, 2026-08-20. Not publication-ready. Two blockers, below.

## Evidence

No runtime measurement and no performance or accuracy claim about any system.
The evidence is a static source audit of fifteen repositories: thirteen scored
implementations, A-MEM as a research reference, and Supermemory as an unscored
source-availability finding.

[`evidence/source-audit-2026-08-20.md`](evidence/source-audit-2026-08-20.md)
records every commit, the test behind each judged column, the per-system
findings and the limits of a static read.
[`evidence/figures.md`](evidence/figures.md) maps each claim to its source line,
and separates out the three claims that are not code citations.
[`evidence/editorial-inventory-2026-08-20.md`](evidence/editorial-inventory-2026-08-20.md)
records every first-party check and source audit present before the article was
cut, including where the shorter draft moved or removed it.

[`evidence/raw/comparison-expansion-2026-08-21.md`](evidence/raw/comparison-expansion-2026-08-21.md)
records the collection command, UTC date, repository heads and expected versus
actual reporting outcome for the expanded comparison. The competitor checkouts
were read-only clones in a scratch directory; each is reproducible from the
commit recorded in the audit.

## Blockers

**1. The `aimee` row describes an open pull request.** At the baseline commit
`50c5d88d`, typed facts do not participate in the graph walk. Their lifecycle
jobs are never scheduled, fact retraction and entity unmerge have no production
surface, orphan pruning can delete a typed fact, and co-occurrence maintenance
can rewrite its confirmation count.

[`aimee` PR 2824](https://github.com/RakuenSoftware/aimee/pull/2824) fixes those
gaps. Its current head, `5a5350b9`, admits current semantic edges to recall,
passes their relation and authority class into scoring, schedules promotion and
expiry, exposes the correction paths, protects typed facts from pruning and
weight normalisation, and adds a PostgreSQL end-to-end suite. That is a static
read of the PR and its tests; this reporting pass did not rerun the suite.

The PR does not yet enforce authority on every correction path. The explicit
retraction function skips Class A for model authority, but
`db2_entity_edge_upsert_semantic()` supersedes the current object of a functional
relation without comparing classes. Since the extractor calls that path with
model authority, a Class B `works_for` write can make a Class A value non-current.
The end-to-end suite tests model retraction, but not this conflicting-write case.

**Before this article ships, PR 2824 must merge, every `aimee` claim must be
re-verified against its merge commit, and every citation must be repointed. The
conflicting-write authority gap above must also be closed.**

The target branch has also moved DB2 from `src/db2/` to `src/modules/db2/c/`, so
the old paths and line numbers cannot be carried forward mechanically.

**2. Right of reply is outstanding.** No project named in the comparison was
given the specific claim ahead of publication. Options are to solicit reply from
each named project first, or to publish with the gap stated in the article text
as well as here. The audit records the mitigating facts and does not treat them
as satisfying the obligation.

## Reporting record

**Form.** Reported analysis with an opinion section. The source findings are
reporting. The argument that fusion is what makes write-path discipline
necessary, and the closing recommendation, are Rakuen Software's analysis and
are written in the first person.

**Interest.** Rakuen Software builds `aimee`, one of the thirteen inspectable systems compared,
and benefits if readers prefer its design. Disclosed in the standfirst, next to
the opening finding.

**Refused metric.** No head-to-head accuracy or savings figure against any other
system appears. The claim is architectural and is specified so a single
counterexample settles it.

**Development history.** Production status, duration and build order were
supplied by the author on 2026-08-20. On 2026-08-21, the author added the
original `aimem` name and that production use by engineers drove each expansion
of memory. The article states this history directly as "we"; the author is the
primary source for why and how the software was built.

**Product scope.** On 2026-08-21, the author specified that the code origin must
not frame `aimee` as a code-memory product. The article now states its current
position as general-purpose organisational memory and demonstrates that scope
with engineering, compliance and non-code use. Its comparative product claim is
now the narrower conjunction of source-linked documents, a native code graph,
endpoint-kind validation and per-assertion authority. The expanded audit found
that mnem and Menhir also join code and memory, so the broader uniqueness claim
has been removed.

**Product goal.** The author further specified on 2026-08-21 that the core goal
is to connect any part of an organisation to any other while retaining the
history of a decision: how it was reached, what changed, and the exact behaviour
of the current implementation. The opening and contract-to-code section now
carry that thesis.

**Corrections policy.** Any finding shown to be wrong will be corrected in
place, dated, with the superseded claim left legible beside it.
