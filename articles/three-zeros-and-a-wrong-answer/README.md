# Three Zeros and a Wrong Answer

A layer built on Codex to make it cheaper cost three to four times more, and the
reason was round trips rather than the cache. Three confident conclusions came
first, each built on a zero that was never a measurement.

## Status

Draft. Not publication-ready, and deliberately not marked as such.

The voice pass is done and `tools/voice_gate.py` passes the article. That is not
the thing standing in the way.

**Every first-party figure is sourced to another repository.** Nothing here
satisfies the rule this repository exists to enforce, so the article cannot be
published against its current provenance no matter how it reads.
`evidence/figures.md` records each figure, where it lives today, and the seven
steps that close the gap. Two rows are worse than merely missing:

- the gateway run in the cost table has no located cells under
  `battery/codex_results/cells/`, and it is the row carrying the natural
  experiment that the argument turns on
- `summary.json` holds `num_turns` but does not appear to carry input tokens,
  cache hit rate or credits, which are three of the table's five columns

A second corpus exists at `battery/matrix_results/cells/` with the same task and
replicate naming but only three run prefixes. Which tree the table was computed
from is not established, and the two must not be mixed.

## What the voice pass changed

Rewritten against Part I and Part III of the voice guide. The finding moved into
the lead, headings became assertions, the three retracted readings became a
table, and roughly 240 words came out of the explaining rather than the evidence.
Em dashes, the decorative question, the intensifiers and `arm` are gone.

Two things were added rather than cut, both on calibration grounds. The corrected
cache figure now carries the 46.6% overall rate beside the 80% to 96% warm-turn
figure, because quoting only the warm turns overstates the recovery. And the
`delegate` zero is now marked in the text as a measured zero, since an article
arguing that a zero can be an absence of recording has to hold its own zeros to
that standard.

## Open questions for the author

- The comparison includes a `ponytail add-on` run that comes out slightly worse
  than baseline. If that is a third party's product, the piece makes an adverse
  comparative claim and right of reply has not been sought.
- `files_indexed: 0` is described as always returning zero, with a comment three
  lines above it saying so. The file and line are not yet cited.
- The 27 of 27 readiness result, the 52 `roundtable_review` calls, the 2.3× per
  call and the 2.5× round trips are all uncited so far.
