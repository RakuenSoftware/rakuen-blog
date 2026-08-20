# Your Agent's Memory Has No Authority Model

An architecture piece. `aimee` holds conversations, typed facts and source code
in one graph ranked by one query, across four scopes and two clocks, and every
guard on its write path exists because an edge is a path.

Around that: a source audit of seven publicly available agent memory systems,
each read at a pinned commit on 2026-08-20.

## Status

Draft, 2026-08-20. Not publication-ready. Two blockers, below.

## Evidence

No measurement, first-party or otherwise, and no performance or accuracy claim
about any system. The evidence is a static source audit of eight repositories.

[`evidence/source-audit-2026-08-20.md`](evidence/source-audit-2026-08-20.md)
records every commit, the test behind each judged column, the per-system
findings and the limits of a static read.
[`evidence/figures.md`](evidence/figures.md) maps each claim to its source line,
and separates out the three claims that are not code citations.

No artifacts were produced, so `evidence/raw/` does not exist. The competitor
checkouts were read-only clones in a scratch directory; each is reproducible
from the commit recorded in the audit.

## Blockers

**1. The fusion citations are ahead of the pinned commit.** The article
describes typed facts participating in the graph walk that ranks recall. At
`50c5d88d` they do not: `src/db2/entity_edges.c` carries `edge_class <>
'semantic'` on 25 read sites, so the walk sees co-occurrence and code-projection
edges only, and typed facts reach a turn through `db2_fact_recall_in_query` as
an injected text block.

That exclusion is being removed in a separate `aimee` session, on the author's
instruction to write the article against the fixed behaviour. **Before this
article ships, every `aimee` citation must be repointed at the merge commit
carrying that change, and the fusion claims re-verified against it.** Publishing
against `50c5d88d` would put the article in direct conflict with the source it
cites, which is the failure the repository's provenance rule exists to prevent.

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

**Interest.** Rakuen Software builds `aimee`, one of the eight systems audited,
and benefits if readers prefer its design. Disclosed in the standfirst, next to
the opening finding.

**Refused metric.** No head-to-head accuracy or savings figure against any other
system appears. The claim is architectural and is specified so a single
counterexample settles it.

**First-party claims.** Production status and duration are the author's own,
supplied 2026-08-20, not independently verifiable, and marked as such in
`evidence/figures.md`. The article states in the same paragraph that the public
repository is younger than the claimed run, so a reader checking git history is
not left with an apparent conflict.

**Corrections policy.** Any finding shown to be wrong will be corrected in
place, dated, with the superseded claim left legible beside it.
