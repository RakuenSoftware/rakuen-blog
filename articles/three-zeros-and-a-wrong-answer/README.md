# Three Zeros and a Wrong Answer

A layer built on Codex to make it cheaper made the same task cost three to four
times more, and three confident conclusions along the way were each built on a
zero that was never a measurement.

## Status

Draft. Not publication-ready, and deliberately not marked as such, so the voice
gate does not treat it as a candidate. Two things stand between this and the
publication gate, and they are different in kind.

**Evidence.** Every first-party figure is currently sourced to another
repository. `evidence/figures.md` lists each one, where it lives today, and the
seven things that have to happen before the article can be published against it.
Two rows are worse than missing: the gateway run in the cost table has no located
cells, and `summary.json` does not appear to carry the input-token, cache-hit or
credit fields the table is built from.

**Voice.** The draft is in the author's register, not the repository's standard,
and `tools/voice_gate.py` would fail it on several rules if it were marked ready.
The known failures are listed below so the rewrite is a decision rather than a
discovery.

## Voice gate failures, if this were marked ready

| rule | where |
|---|---|
| no em dash in prose | throughout |
| no prose question | the opening question, and the heading `So where did the money actually go?` |
| no intensifiers | `very easy to make`, `simply never told`, `simply better at economics` |
| use run, not arm | the cost table and the natural-experiment section use `arm` throughout |
| 1,300-word gate | the draft is over it |
| at most four sentences per paragraph | several paragraphs exceed it |

The bold-text rule is also worth a pass: the gate only permits bold that contains
a figure or opens with a rule verb, and the three reading headers are neither.

## A note on the subject matter

The article's thesis is that a zero can be an absence of recording rather than a
measurement. It contains two zeros of its own, `delegate` called zero times and
`files_indexed: 0`, and one of them is load-bearing. Holding those to the
standard the article sets is a publication condition, not a nicety.

The comparison is also with a third-party product's default behaviour, and the
article draws a comparative cost conclusion about it. Right of reply has not been
sought.
