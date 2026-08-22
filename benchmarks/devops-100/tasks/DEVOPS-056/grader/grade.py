#!/usr/bin/env python3
"""Private grader for DEVOPS-056."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    points: int
    passed: bool
    detail: str


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_source(source: Path, destination: Path) -> None:
    ignored = shutil.ignore_patterns("build", "out-*", ".git", ".devops-bench", "__pycache__")
    shutil.copytree(source, destination, ignore=ignored, symlinks=True)


def run_make(workspace: Path, *targets: str, build_dir: Path | str | None = None, actor: str = "builder") -> subprocess.CompletedProcess[str]:
    command = ["make", "--no-print-directory", "-s"]
    if build_dir is not None:
        command.append(f"BUILD_DIR={build_dir}")
    command.extend(targets or ("all",))
    environment = os.environ.copy()
    environment.update(
        {
            "TZ": "Pacific/Chatham" if actor == "builder-a" else "America/St_Johns",
            "LANG": "C",
            "LC_ALL": "C",
            "USER": actor,
            "LOGNAME": actor,
        }
    )
    return subprocess.run(
        command,
        cwd=workspace,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=20,
        check=False,
    )


def artifact_for(workspace: Path, build_dir: Path | str | None = None) -> Path:
    if build_dir is None:
        return workspace / "build" / "artifact.txt"
    path = Path(build_dir)
    return (path if path.is_absolute() else workspace / path) / "artifact.txt"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    workspace = parser.parse_args().workspace.resolve()
    checks: list[Check] = []

    with tempfile.TemporaryDirectory(prefix="devops-056-grade-") as raw_temporary:
        temporary = Path(raw_temporary)

        basic = temporary / "basic"
        copy_source(workspace, basic)
        basic_result = run_make(basic, "all")
        basic_artifact = artifact_for(basic)
        basic_ok = basic_result.returncode == 0 and basic_artifact.is_file()
        checks.append(Check("build succeeds", 15, basic_ok, basic_result.stderr.strip()[-300:]))

        semantic_ok = False
        if basic_ok:
            text = basic_artifact.read_text(encoding="utf-8", errors="replace")
            semantic_ok = (
                "version=1.4.0\n" in text
                and "feature=artifact-provenance\n" in text
                and "format=devops-100\n" in text
            )
        checks.append(Check("artifact preserves version and payload", 15, semantic_ok, "required semantic lines are present" if semantic_ok else "required semantic lines are missing"))

        first = temporary / "short-checkout"
        second = temporary / "a-very-long-checkout-name-used-to-detect-path-dependent-output"
        copy_source(workspace, first)
        copy_source(workspace, second)
        first_output = temporary / "absolute-output-a"
        second_output = Path("nested") / "relative-output-b"
        first_result = run_make(first, "all", build_dir=first_output, actor="builder-a")
        time.sleep(1.1)
        second_result = run_make(second, "all", build_dir=second_output, actor="builder-b")
        first_artifact = artifact_for(first, first_output)
        second_artifact = artifact_for(second, second_output)
        reproducible = (
            first_result.returncode == 0
            and second_result.returncode == 0
            and first_artifact.is_file()
            and second_artifact.is_file()
            and digest(first_artifact) == digest(second_artifact)
        )
        checks.append(Check("clean builds are reproducible", 25, reproducible, "artifact hashes match across time path timezone actor and output mode" if reproducible else "artifact hashes differ or a variant failed"))

        incremental = temporary / "incremental"
        copy_source(workspace, incremental)
        incremental_result = run_make(incremental, "all")
        incremental_artifact = artifact_for(incremental)
        unchanged = False
        if incremental_result.returncode == 0 and incremental_artifact.is_file():
            before_hash = digest(incremental_artifact)
            before_mtime = incremental_artifact.stat().st_mtime_ns
            second_incremental = run_make(incremental, "all")
            unchanged = (
                second_incremental.returncode == 0
                and digest(incremental_artifact) == before_hash
                and incremental_artifact.stat().st_mtime_ns == before_mtime
            )
        checks.append(Check("unchanged build is incremental", 15, unchanged, "artifact is not rewritten" if unchanged else "unchanged make rewrote or changed the artifact"))

        mutation = temporary / "mutation"
        copy_source(workspace, mutation)
        mutation_result = run_make(mutation, "all")
        mutation_artifact = artifact_for(mutation)
        rebuilds = False
        if mutation_result.returncode == 0 and mutation_artifact.is_file():
            old_hash = digest(mutation_artifact)
            payload = mutation / "src" / "payload.txt"
            with payload.open("a", encoding="utf-8") as handle:
                handle.write("fixture=private-source-mutation\n")
            artifact_mtime = mutation_artifact.stat().st_mtime_ns
            os.utime(payload, ns=(artifact_mtime + 2_000_000_000, artifact_mtime + 2_000_000_000))
            changed_result = run_make(mutation, "all")
            if changed_result.returncode == 0 and mutation_artifact.is_file():
                changed_text = mutation_artifact.read_text(encoding="utf-8", errors="replace")
                rebuilds = digest(mutation_artifact) != old_hash and "fixture=private-source-mutation\n" in changed_text
        checks.append(Check("source edit changes artifact", 15, rebuilds, "source dependency is tracked" if rebuilds else "source mutation did not rebuild into the artifact"))

        clean_case = temporary / "clean"
        copy_source(workspace, clean_case)
        clean_output = Path("nested") / "custom-output"
        clean_build = run_make(clean_case, "all", build_dir=clean_output)
        sentinel = clean_case / "nested" / "keep.txt"
        sentinel.parent.mkdir(parents=True, exist_ok=True)
        sentinel.write_text("preserve me\n", encoding="utf-8")
        clean_result = run_make(clean_case, "clean", build_dir=clean_output)
        clean_safe = (
            clean_build.returncode == 0
            and clean_result.returncode == 0
            and not artifact_for(clean_case, clean_output).exists()
            and sentinel.read_text(encoding="utf-8") == "preserve me\n"
        )
        checks.append(Check("overridden clean is scoped", 5, clean_safe, "only the requested artifact is removed" if clean_safe else "clean failed or removed an unrelated file"))

    documentation = workspace / "REPRODUCIBILITY.md"
    documentation_ok = False
    if documentation.is_file():
        doc = documentation.read_text(encoding="utf-8", errors="replace").lower()
        documentation_ok = (
            len(doc) >= 180
            and "reproduc" in doc
            and ("modified" in doc or "uncommitted" in doc or "dirty" in doc)
            and ("identity" in doc or "hash" in doc or "digest" in doc)
        )
    checks.append(Check("reproducibility contract is documented", 10, documentation_ok, "contract covers reproducibility and modified-source identity" if documentation_ok else "REPRODUCIBILITY.md is absent or incomplete"))

    score = sum(check.points for check in checks if check.passed)
    report = {
        "task_id": "DEVOPS-056",
        "score": score,
        "max_score": 100,
        "checks": [
            {"name": check.name, "points": check.points, "passed": check.passed, "detail": check.detail}
            for check in checks
        ],
    }
    print(json.dumps(report, sort_keys=True))
    return 0 if score == 100 else 1


if __name__ == "__main__":
    raise SystemExit(main())
