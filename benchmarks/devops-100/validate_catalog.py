#!/usr/bin/env python3
"""Validate the DevOps-100 task catalog using only the standard library."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


CATALOG = Path(__file__).with_name("tasks.tsv")
FIELDS = {
    "id",
    "domain",
    "difficulty",
    "operation",
    "environment",
    "title",
    "scenario",
    "success",
}
DOMAINS = {
    "linux",
    "network",
    "containers",
    "kubernetes",
    "iac-cloud",
    "cicd",
    "observability",
    "security",
    "data",
    "platform",
}
DIFFICULTIES = {"foundation", "intermediate", "advanced", "expert"}
OPERATIONS = {
    "diagnose",
    "repair",
    "build",
    "migrate",
    "respond",
    "optimize",
    "recover",
    "review",
}


def main() -> None:
    with CATALOG.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
        headers = set(reader.fieldnames or [])

    errors: list[str] = []
    if headers != FIELDS:
        errors.append(f"headers differ: expected {sorted(FIELDS)} got {sorted(headers)}")
    if len(rows) != 100:
        errors.append(f"expected 100 tasks; found {len(rows)}")

    expected_ids = [f"DEVOPS-{number:03d}" for number in range(1, 101)]
    actual_ids = [row.get("id", "") for row in rows]
    if actual_ids != expected_ids:
        errors.append("task IDs must be ordered DEVOPS-001 through DEVOPS-100")

    for number, row in enumerate(rows, 2):
        missing = sorted(field for field in FIELDS if not row.get(field, "").strip())
        if missing:
            errors.append(f"line {number}: empty fields: {', '.join(missing)}")
        if row.get("domain") not in DOMAINS:
            errors.append(f"line {number}: invalid domain {row.get('domain')!r}")
        if row.get("difficulty") not in DIFFICULTIES:
            errors.append(f"line {number}: invalid difficulty {row.get('difficulty')!r}")
        if row.get("operation") not in OPERATIONS:
            errors.append(f"line {number}: invalid operation {row.get('operation')!r}")

    domain_counts = Counter(row.get("domain") for row in rows)
    if domain_counts != Counter({domain: 10 for domain in DOMAINS}):
        errors.append(f"domains must contain 10 tasks each; got {dict(domain_counts)}")

    for field in ("id", "title"):
        counts = Counter(row.get(field) for row in rows)
        duplicates = sorted(value for value, count in counts.items() if count > 1)
        if duplicates:
            errors.append(f"duplicate {field} values: {duplicates}")

    operation_counts = Counter(row.get("operation") for row in rows)
    absent_operations = sorted(OPERATIONS - operation_counts.keys())
    if absent_operations:
        errors.append(f"operations not represented: {absent_operations}")
    if len({row.get("environment") for row in rows}) < 20:
        errors.append("catalog must exercise at least 20 distinct environments")

    if errors:
        raise SystemExit("Catalog validation failed:\n- " + "\n- ".join(errors))

    difficulty_counts = Counter(row["difficulty"] for row in rows)
    print("DevOps-100 catalog is valid")
    print("domains:", ", ".join(f"{key}={domain_counts[key]}" for key in sorted(DOMAINS)))
    print("difficulty:", ", ".join(f"{key}={difficulty_counts[key]}" for key in sorted(difficulty_counts)))
    print("operations:", ", ".join(f"{key}={operation_counts[key]}" for key in sorted(OPERATIONS)))


if __name__ == "__main__":
    main()
