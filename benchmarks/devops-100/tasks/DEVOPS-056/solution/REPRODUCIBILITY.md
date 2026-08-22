# Reproducibility contract

`make` derives the artifact only from `VERSION`, `src/payload.txt`, and the
recipe in `Makefile`. It records the declared version and a SHA-256 identity of
the exact payload instead of the checkout path, actor, locale, timezone, or
wall clock. Identical inputs therefore produce identical bytes.

A locally modified or uncommitted payload is intentionally a different input:
it rebuilds the artifact and produces a different payload hash. The build does
not claim that those bytes came from the pristine release source.
