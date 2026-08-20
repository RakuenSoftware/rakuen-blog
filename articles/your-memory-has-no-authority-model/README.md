# Your Agent's Memory Has No Authority Model

An architecture piece. A source audit of seven publicly available agent memory
systems, and the mechanism in `aimee`'s typed-fact layer that makes it the
exception: a typed write gate, provenance-keyed authority classes, and
correction that stamps the old row and keeps it.

## Status

Draft, 2026-08-20. Not publication-ready.

The article passes provenance: every claim traces to a pinned public source
line, mapped in [`evidence/figures.md`](evidence/figures.md). It does not pass
the reporting gate, for one reason recorded below.

## Evidence

This article contains no measurement, first-party or otherwise, and makes no
performance or accuracy claim about any system. Its evidence is a static source
audit of eight repositories, each read at a pinned commit on 2026-08-20.

[`evidence/source-audit-2026-08-20.md`](evidence/source-audit-2026-08-20.md)
records every commit, the test behind each judged column, the per-system
findings, and the limits of a static read.

No artifacts were produced, so `evidence/raw/` does not exist. The competitor
checkouts were read-only clones in a scratch directory and were not copied into
the repository; each is reproducible from the commit recorded in the audit.

## Scope

The article describes `aimee`'s typed-fact layer: ontology, write gate,
confidence classes, correction, entity canonicalisation, outcome-attributed
demotion. Free-text prose memory has different write semantics and is out of
scope, stated as such in the article text and in the audit.

## Reporting record

**Form.** Reported analysis with an opinion section. The source findings are
reporting. The claim that the write path is the binding constraint, and the
recommendation in the closing section, are Rakuen Software's analysis and are
written in the first person.

**Interest.** Rakuen Software builds `aimee`, one of the eight systems audited,
and benefits if readers prefer its design. Disclosed in the article's standfirst,
next to the opening finding.

**Refused metric.** No head-to-head accuracy or savings figure against any other
system appears. The article makes an architectural claim and stays inside it.

**Right of reply: outstanding.** No project named in the comparison was given
the specific claim ahead of publication. This is the blocker on publication
readiness. Options are to solicit reply from each named project before
publishing, or to publish with the gap stated in the article text as well as
here. The audit file records the mitigating facts and does not treat them as
satisfying the obligation.

**Corrections policy.** Any finding shown to be wrong will be corrected in
place, dated, with the superseded claim left legible beside it.
