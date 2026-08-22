#!/usr/bin/env python3
"""Prepare, validate, and grade DevOps-100 task packages."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
TASKS = ROOT / "tasks"
CATALOG = ROOT / "tasks.tsv"
REQUIRED_TOP_LEVEL = {"id", "version", "execution", "workspace", "grading"}
EXECUTION_KINDS = {"local", "oci", "vm", "kind", "control-plane"}
NETWORK_MODES = {"none", "fixture-only"}


class PackageError(ValueError):
    """A task package violates the benchmark contract."""


def read_catalog() -> dict[str, dict[str, str]]:
    with CATALOG.open(encoding="utf-8", newline="") as handle:
        return {row["id"]: row for row in csv.DictReader(handle, delimiter="\t")}


def task_dir(task_id: str) -> Path:
    path = TASKS / task_id
    if task_id not in read_catalog():
        raise PackageError(f"unknown task ID: {task_id}")
    if not path.is_dir():
        raise PackageError(f"task {task_id} has no runnable package")
    return path


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PackageError(f"cannot read {path}: {error}") from error
    if not isinstance(value, dict):
        raise PackageError(f"{path} must contain a JSON object")
    return value


def relative_member(package: Path, value: object, field: str, *, directory: bool) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise PackageError(f"{field} must be a non-empty relative path")
    candidate = (package / value).resolve()
    try:
        candidate.relative_to(package.resolve())
    except ValueError as error:
        raise PackageError(f"{field} escapes its task package") from error
    valid = candidate.is_dir() if directory else candidate.is_file()
    if not valid:
        kind = "directory" if directory else "file"
        raise PackageError(f"{field} does not name a {kind}: {value}")
    return candidate


def validate_package(package: Path) -> dict[str, Any]:
    manifest = load_manifest(package / "task.json")
    unknown = set(manifest) - REQUIRED_TOP_LEVEL
    missing = REQUIRED_TOP_LEVEL - set(manifest)
    if missing or unknown:
        raise PackageError(
            f"{package.name}: manifest keys missing={sorted(missing)} unknown={sorted(unknown)}"
        )
    if manifest["id"] != package.name:
        raise PackageError(f"{package.name}: manifest ID differs from directory")
    if not isinstance(manifest["version"], int) or manifest["version"] < 1:
        raise PackageError(f"{package.name}: version must be a positive integer")

    execution = manifest["execution"]
    if not isinstance(execution, dict):
        raise PackageError(f"{package.name}: execution must be an object")
    if execution.get("kind") not in EXECUTION_KINDS:
        raise PackageError(f"{package.name}: unsupported execution kind")
    timeout = execution.get("timeout_seconds")
    if not isinstance(timeout, int) or not 30 <= timeout <= 14400:
        raise PackageError(f"{package.name}: timeout must be between 30 and 14400 seconds")
    if execution.get("network") not in NETWORK_MODES:
        raise PackageError(f"{package.name}: unsupported network mode")
    capabilities = execution.get("capabilities")
    if not isinstance(capabilities, list) or any(not isinstance(item, str) for item in capabilities):
        raise PackageError(f"{package.name}: capabilities must be a string list")
    if len(capabilities) != len(set(capabilities)):
        raise PackageError(f"{package.name}: capabilities must be unique")

    workspace = manifest["workspace"]
    if not isinstance(workspace, dict):
        raise PackageError(f"{package.name}: workspace must be an object")
    relative_member(package, workspace.get("seed"), "workspace.seed", directory=True)
    relative_member(package, workspace.get("prompt"), "workspace.prompt", directory=False)
    relative_member(package, workspace.get("public_tests"), "workspace.public_tests", directory=True)

    grading = manifest["grading"]
    if not isinstance(grading, dict) or grading.get("max_score") != 100:
        raise PackageError(f"{package.name}: grading.max_score must equal 100")
    command = grading.get("command")
    if (
        not isinstance(command, list)
        or len(command) != 2
        or command[0] != "python3"
        or any(not isinstance(item, str) for item in command)
    ):
        raise PackageError(f"{package.name}: grading.command must be ['python3', '<grader>']")
    relative_member(package, command[1], "grading.command[1]", directory=False)
    return manifest


def command_validate(_: argparse.Namespace) -> int:
    catalog = read_catalog()
    package_ids = sorted(path.name for path in TASKS.glob("DEVOPS-[0-9][0-9][0-9]") if path.is_dir())
    for task_id in package_ids:
        if task_id not in catalog:
            raise PackageError(f"runnable package missing from catalog: {task_id}")
        validate_package(TASKS / task_id)
    print(f"validated catalog={len(catalog)} runnable_packages={len(package_ids)}")
    return 0


def command_list(_: argparse.Namespace) -> int:
    runnable = {path.name for path in TASKS.glob("DEVOPS-[0-9][0-9][0-9]") if path.is_dir()}
    for task_id, row in read_catalog().items():
        state = "runnable" if task_id in runnable else "specified"
        print(f"{task_id}\t{state}\t{row['domain']}\t{row['title']}")
    return 0


def command_prepare(args: argparse.Namespace) -> int:
    package = task_dir(args.task_id)
    manifest = validate_package(package)
    destination = args.destination.resolve()
    if destination.exists():
        raise PackageError(f"destination already exists: {destination}")

    workspace = manifest["workspace"]
    seed = relative_member(package, workspace["seed"], "workspace.seed", directory=True)
    shutil.copytree(seed, destination)
    shutil.copy2(package / workspace["prompt"], destination / "TASK.md")
    public_destination = destination / ".devops-bench" / "public"
    shutil.copytree(package / workspace["public_tests"], public_destination)
    print(destination)
    return 0


def command_grade(args: argparse.Namespace) -> int:
    package = task_dir(args.task_id)
    manifest = validate_package(package)
    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        raise PackageError(f"workspace is not a directory: {workspace}")

    raw_command = manifest["grading"]["command"]
    command = [raw_command[0], str(package / raw_command[1]), "--workspace", str(workspace)]
    result = subprocess.run(
        command,
        cwd=package,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=manifest["execution"]["timeout_seconds"],
        check=False,
    )
    if result.returncode not in (0, 1):
        raise PackageError(f"grader failed ({result.returncode}): {result.stderr.strip()}")
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise PackageError(f"grader emitted invalid JSON: {error}") from error
    if not isinstance(report, dict) or not isinstance(report.get("score"), int):
        raise PackageError("grader report must contain an integer score")
    if not 0 <= report["score"] <= manifest["grading"]["max_score"]:
        raise PackageError("grader score is outside its declared range")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["score"] == manifest["grading"]["max_score"] else 1


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subparsers = result.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate", help="validate all implemented packages")
    validate.set_defaults(handler=command_validate)
    listing = subparsers.add_parser("list", help="list specified and runnable tasks")
    listing.set_defaults(handler=command_list)
    prepare = subparsers.add_parser("prepare", help="create an agent workspace")
    prepare.add_argument("task_id")
    prepare.add_argument("destination", type=Path)
    prepare.set_defaults(handler=command_prepare)
    grade = subparsers.add_parser("grade", help="run the private grader")
    grade.add_argument("task_id")
    grade.add_argument("workspace", type=Path)
    grade.set_defaults(handler=command_grade)
    return result


def main() -> int:
    try:
        args = parser().parse_args()
        return args.handler(args)
    except (PackageError, subprocess.TimeoutExpired) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
