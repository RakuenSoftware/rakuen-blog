# Ornith Against the Base It Came From

Every Ornith model is a finetune of a Qwen base, so it can be measured against
the exact thing it was made from rather than against a leaderboard.

## Status

Draft. No run has been taken yet, so the article carries the design and the
findings that came out of setting it up, and no accuracy result. The results
sections name what is missing rather than leaving a gap a later edit could fill
quietly.

This is a study of one lineage on two tasks at four bits. It is not a
quantization ladder and it is not a leaderboard, and it inherits the harness,
the corpora and the card from `which-quant-beats-how-many-bits/` so that a
finetune and its base are separated by the finetune and nothing else.

Split from that article's change on 2026-08-23. The two were briefly proposed
together; Ornith is a separate question with its own pairs, and neither Ornith
nor Qwen3.5-9B was an agreed measurement for the quantization piece.

## The plan is registered

`evidence/ornith-plan-2026-08-23.md` was written before any run started, to the
same rule as the quantization campaign's plan: the design, the pairs, the known
weaknesses and **the expectation** are on record before the numbers exist.

The expectation is that a finetune does not shift measurably from its base in
either direction on this work. That is deliberately falsifiable and symmetric —
a large loss contradicts it exactly as much as a large win — so that whichever
way the intervals fall, the reading was not chosen afterwards to fit them.

## What is already measured

Nothing about accuracy. Two things about serving, both found while building the
study, both of which change how a reader should read a throughput number:

- **No 9B model here can speculate on this build.** A separate draft model
  passed with `-hfd` works; MTP layers baked into the model are discarded at
  load. The MTP build serves at 133.11 tok/s against 133.6 for the ordinary
  one — a larger download for no speedup.
- **The 35B pair is not matched on speculation.** The Qwen3.6 base ships a
  draft and Ornith-1.5-35B-A3B does not. That is a real difference between two
  things a reader can download, not an artefact to correct away.

The base half of the 35B pair is reused rather than re-run:
`qwen36-35b-a3b.base.q4` from the quantization campaign, strict F1 **0.7194** on
the same 1,001-note corpus.

## Outstanding

- Four runs, both tasks: `qwen35-9b.base.q4`, `ornith10-9b.base.q4`,
  `ornith15-9b.base.q4`, `ornith15-35b-a3b.base.q4`. The arms are registered in
  `campaign/arms.tsv`.
- Paired bootstrap against the base half of each pair, seed `20260809`, 20,000
  replicates on extraction and 5,000 on synthesis.
- A measurement log, once there is something to log.
- `evidence/figures.md`, once there is a figure.

## Reporting record

First-party measurement only. No external sources, interviews or vendor claims,
so there is no right-of-reply obligation outstanding. Model cards are read for
lineage and quantization recipe only, and lineage is taken from `config.json`
rather than the card text, which never names an upstream.
