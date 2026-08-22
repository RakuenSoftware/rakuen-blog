# Eliminate a timestamp-only rebuild

The release pipeline packages `src/payload.txt` into `build/artifact.txt` by
running `make`. Identical source trees currently produce different artifact
hashes, and an incremental `make` rewrites the artifact even when no input has
changed. This defeats both provenance comparison and the CI cache.

Repair the build in this workspace. Preserve the artifact's useful version and
payload information. A source edit must cause a rebuild; an unchanged tree must
not. `BUILD_DIR` is part of the supported interface and may name an absolute or
relative output directory.

Builds must be reproducible across checkout paths, timezones, locales, users,
and wall-clock time. Do not rely on network access or add generated dependencies
to the repository. `make clean` must remain safe when `BUILD_DIR` is overridden.

Document the reproducibility contract and the artifact-identity behavior for
locally modified source in `REPRODUCIBILITY.md`.

You can run the limited public contract checks with:

```sh
python3 .devops-bench/public/check.py
```

Private evaluation uses additional clean copies, output paths, environments,
and source mutations.
