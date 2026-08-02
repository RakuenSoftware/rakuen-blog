# Reporting and artifact rules

These rules apply to every article under this directory.

## Journalism rewrites

- Read Part I and Part III of `/home/virant/dev/voice-guide/VOICE.md` before
  editing a journalistic article.
- Before cutting or rewriting, inventory every first-party test, measurement,
  interview, observation, document review and source audit in the existing
  article. Record each item and its disposition in the article's `evidence/`
  directory.
- Never silently remove first-party reporting because its provenance is weak or
  incomplete. Preserve it in the article with its limits when it materially
  bears on the finding. At minimum, preserve it in the reporting record and
  state why it cannot carry a published claim.
- Distinguish runtime tests, billing observations, static source audits, vendor
  reports and independent benchmarks. Do not collapse them into one class of
  evidence.
- A rewrite may narrow a claim, relabel its evidentiary weight, or put it on
  publication hold. It may not turn prior reporting into an unrecorded absence.

## Raw artifacts are append-only

- Never delete, overwrite, truncate, normalise or replace a raw reporting
  artifact during drafting, rewriting, migration or cleanup.
- Store new raw outputs under the article's `evidence/raw/` directory. Record
  the command or collection method, time, software version or commit, fixture,
  environment facts that bear on the result, and expected and actual outcome.
- Corrections are additive. If an artifact or run is invalid or incorrect,
  retain it when possible, mark it `INVALID` in an adjacent note, explain why,
  and point to the superseding run. Do not silently substitute a new output.
- Delete a raw artifact only when the artifact itself is invalid or incorrect,
  the reason is recorded in the reporting ledger, and the user explicitly
  approves that deletion. Prefer quarantine and a tombstone to deletion.
- Never commit credentials, private customer data or source material that the
  repository is not authorised to publish. Preventing an unsafe artifact from
  entering the repository is not permission to erase valid reporting later.

## Publication gate

Before publication, confirm that every figure has an artifact or named source,
every prior first-party result has a recorded disposition, and every material
criticism has completed right of reply. Missing raw support changes how a result
is described; it does not make the reporting disappear.
