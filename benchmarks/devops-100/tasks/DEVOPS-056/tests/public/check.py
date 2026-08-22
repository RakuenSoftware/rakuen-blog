#!/usr/bin/env python3
"""Limited checks visible to the benchmark participant."""

from __future__ import annotations

import subprocess
from pathlib import Path


workspace = Path.cwd()
subprocess.run(["make", "clean"], cwd=workspace, check=True)
subprocess.run(["make", "all"], cwd=workspace, check=True)
artifact = workspace / "build" / "artifact.txt"
assert artifact.is_file(), "make all did not create build/artifact.txt"
contents = artifact.read_text(encoding="utf-8")
assert "version=1.4.0\n" in contents, "artifact lost its release version"
assert "feature=artifact-provenance\n" in contents, "artifact lost its payload"
print("public contract checks passed")
