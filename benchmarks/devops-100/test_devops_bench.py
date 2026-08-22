#!/usr/bin/env python3
"""End-to-end tests for the DevOps-100 harness and reference fixture."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
HARNESS = ROOT / "devops_bench.py"
CATALOG_VALIDATOR = ROOT / "validate_catalog.py"
REFERENCE_SOLUTION = ROOT / "tasks" / "DEVOPS-056" / "solution"


def run(*command: str | Path, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(part) for part in command],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        check=False,
    )


class HarnessTests(unittest.TestCase):
    def test_catalog_and_packages_validate(self) -> None:
        catalog = run("python3", CATALOG_VALIDATOR)
        self.assertEqual(catalog.returncode, 0, catalog.stderr)
        packages = run("python3", HARNESS, "validate")
        self.assertEqual(packages.returncode, 0, packages.stderr)
        self.assertIn("catalog=100", packages.stdout)
        self.assertIn("runnable_packages=1", packages.stdout)

    def test_prepare_exposes_no_private_grader_or_solution(self) -> None:
        with tempfile.TemporaryDirectory(prefix="devops-100-test-") as raw:
            workspace = Path(raw) / "workspace"
            prepared = run("python3", HARNESS, "prepare", "DEVOPS-056", workspace)
            self.assertEqual(prepared.returncode, 0, prepared.stderr)
            self.assertTrue((workspace / "TASK.md").is_file())
            self.assertTrue((workspace / ".devops-bench" / "public" / "check.py").is_file())
            self.assertFalse((workspace / "grader").exists())
            self.assertFalse((workspace / "solution").exists())

    def test_seed_fails_private_checks_and_reference_scores_100(self) -> None:
        with tempfile.TemporaryDirectory(prefix="devops-100-test-") as raw:
            workspace = Path(raw) / "workspace"
            prepared = run("python3", HARNESS, "prepare", "DEVOPS-056", workspace)
            self.assertEqual(prepared.returncode, 0, prepared.stderr)

            public = run("python3", ".devops-bench/public/check.py", cwd=workspace)
            self.assertEqual(public.returncode, 0, public.stderr)

            seeded = run("python3", HARNESS, "grade", "DEVOPS-056", workspace)
            self.assertEqual(seeded.returncode, 1, seeded.stderr)
            seeded_report = json.loads(seeded.stdout)
            self.assertLess(seeded_report["score"], 100)

            shutil.copy2(REFERENCE_SOLUTION / "Makefile", workspace / "Makefile")
            shutil.copy2(
                REFERENCE_SOLUTION / "REPRODUCIBILITY.md",
                workspace / "REPRODUCIBILITY.md",
            )
            reference = run("python3", HARNESS, "grade", "DEVOPS-056", workspace)
            self.assertEqual(reference.returncode, 0, reference.stderr)
            reference_report = json.loads(reference.stdout)
            self.assertEqual(reference_report["score"], 100)
            self.assertTrue(all(check["passed"] for check in reference_report["checks"]))

    def test_prepare_refuses_to_overwrite_a_workspace(self) -> None:
        with tempfile.TemporaryDirectory(prefix="devops-100-test-") as raw:
            workspace = Path(raw) / "workspace"
            workspace.mkdir()
            marker = workspace / "keep.txt"
            marker.write_text("keep\n", encoding="utf-8")
            prepared = run("python3", HARNESS, "prepare", "DEVOPS-056", workspace)
            self.assertEqual(prepared.returncode, 2)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep\n")


if __name__ == "__main__":
    unittest.main()
