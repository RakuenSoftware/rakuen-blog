# Maintainer verification

Copy the reference `Makefile` and `REPRODUCIBILITY.md` to a freshly prepared
workspace. Run the public check, then grade it through the harness. The
reference result is 100/100. The seeded workspace should score below 100 because
it rebuilds unconditionally, embeds wall-clock time, ignores payload dependency
changes, and has no reproducibility contract.
