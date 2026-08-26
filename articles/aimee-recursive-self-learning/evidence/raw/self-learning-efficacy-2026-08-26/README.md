# Paired self-learning study

Collected on 26 August 2026 from `pvetest` at Aimee commit
`ceea316ca12ad2f49ecc7ea9842e00701a6b7300`.

The control and treatment received the same two failed observations for each of
24 repeated tasks. The control withheld synthesis before the consumer phase.
The treatment ran Aimee's production synthesis and read the resulting failed
approaches through the production recall command. A fixed consumer began with
the same choice in both conditions and changed it only when recall identified
that choice as failed. Another 24 tasks had no matching history.

| task class | control | treatment |
|---|---:|---:|
| repeated | 12/24 | 24/24 |
| novel | 12/24 | 12/24 |

Both `run-1` and `run-2` passed 12 harness checks with no failures. Their
`results.csv` files are byte-identical, with SHA-256
`250a617ff71ad3f069fdd5bd9c82ebc142f3e694693fb368c971706abafaf62c`.
Each directory contains the cell-level result, summary, 96 recall outputs,
synthesis output, environment record, and service and module logs.

The deterministic consumer isolates whether recalled failure can change a
later outcome. This is not a model-reasoning benchmark and does not measure how
often a model follows the same record during open-ended work.

Three invalid attempts are recorded in the Aimee validation report but are not
included here: one stopped at database setup, one at the readiness probe, and
one produced the same cell results but failed three reporting assertions. The
valid runs and the study method are documented in
`docs/validation/self-learning-efficacy-2026-08-26.md` on the Aimee study
branch.
