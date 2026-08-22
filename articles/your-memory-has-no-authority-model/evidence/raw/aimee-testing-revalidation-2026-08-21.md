# Aimee testing revalidation

Collection time: 2026-08-21 UTC.

Repository: `RakuenSoftware/aimee`.

Pinned tree: `origin/testing` at
`1d36f8c186bf91267ee878a06f1c1d92615a7783`.

Method: fetched the public origin, created a detached worktree at the pinned
commit, traced the typed-fact admission, correction, provenance, recall and
maintenance paths, and read the repository's validation record at
`docs/validation/typed-fact-write-authority.md`. The article audit did not run
the binaries or repeat the PostgreSQL validation.

Current result:

- user authority is bounded by attested transport at the server and authenticated
  actor at the knowledge service;
- model-composed context-block text is explicitly assigned model authority;
- stored-memory provenance defaults to agent-authored and is read back when the
  asynchronous fact drain assigns authority;
- a functional correction compares A/B/C rank, dropping a write that is
  outranked by the current value;
- supersession and tombstoning retain typed-fact rows; and
- current semantic edges participate in graph recall while superseded and
  suppressed rows do not.

Validation limit: the repository's record reports a real clean-container and
PostgreSQL run, but says the live mTLS actor branch and the model-delete retire
path were not exercised in that run. This reporting pass verified the recorded
scope rather than extending it.
