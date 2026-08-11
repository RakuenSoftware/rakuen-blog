# Three Zeros and a Wrong Answer

A layer built on Codex to make it cheaper cost three to four times more, and the
reason was round trips rather than the cache. Three confident conclusions came
first, each built on a zero that was never a measurement.

## Status

Draft. Not publication-ready, and deliberately not marked as such.

**The article's mechanism was retracted by the author on 2026-08-11 at 22:00, and
the prose has not been changed to match.** The piece still argues that the
persona generated round trips, using the gateway run against the plugin run as a
natural experiment. That comparison does not hold: the Codex MCP run receives no
aimee persona at all, and the gateway run's lower round-trip count was a
tool-routing defect fixed the same day.

The headline survives. The layer costs about three times baseline, re-measured at
2.97× on credits with identical correctness across all nine cells. What does not
survive is why. Removing `roundtable_review` saves 26% and does not change the
round-trip count, so the cost is per-call weight rather than trip count.

Rewriting the argument around that is an editorial decision, not a filing
correction, so it is left for the author. `evidence/figures.md` records the
retraction, the replacement measurement, and what still stands.

The voice pass is done and `tools/voice_gate.py` passes the article.

Most of this article needs no external artifact. It is a first-person account of
our own debugging, plus a source audit of our own code with a merged fix named in
the text. `evidence/figures.md` now separates the evidence by kind, which is what
`articles/AGENTS.md` asks for.

**One thing blocks publication: the cost table.** A table of token counts and
credits is a measurement rather than an experience, and the artifacts behind this
one are not on this machine. Searched 2026-08-11:

- `codex_results/cells/` has `t01_cache` at `r1` only, and no aimee run
- the only aimee `t01_cache` cell with usage data sits in a directory named
  `aimee-kb-8bc6aa5-superseded`
- `/tmp/ptcodex/cells/` holds aimee working directories with no `summary.json`,
  so fixtures rather than results, and `/tmp` is volatile
- the located cells report figures well outside the article's published ranges,
  so they are a different campaign rather than the table's source

This does not show the table is wrong. It shows the table is the one claim here
that a reader could not check. The author ran the measurement and knows which
tree it came from; naming it closes this.

The article also states three replicates per run, and every located `t01_cache`
cell outside `matrix_results` is `r1` only.

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

- Which results tree was the cost table computed from, and does it span three
  replicates or one.
- The comparison includes a `ponytail add-on` run that comes out slightly worse
  than baseline. If that is a third party's product, the piece makes an adverse
  comparative claim and right of reply applies.
- The 52 `roundtable_review` calls and the `delegate` zero need a counting
  source. The article marks that zero as measured, so by its own standard it has
  to be able to show the count.
