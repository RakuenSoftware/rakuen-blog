#!/usr/bin/env python3
"""Build and validate the six static fact-extraction corpus tiers."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


EUROBERT_LANGUAGES = (
    "en", "fr", "de", "es", "zh", "it", "ru", "pl", "pt", "ja", "vi",
    "nl", "ar", "tr", "hi",
)
NON_ENGLISH_LANGUAGES = EUROBERT_LANGUAGES[1:]
REQUIRED_GOLD_FIELDS = ("id", "note", "gold")
REQUIRED_MULTILINGUAL_FIELDS = (
    "id", "language", "note", "gold", "source", "provenance",
)


class CorpusError(ValueError):
    """A corpus input or generated output violates the benchmark contract."""


@dataclass(frozen=True)
class Row:
    data: dict[str, Any]
    raw: bytes

    @property
    def row_id(self) -> str:
        return self.data["id"]


@dataclass(frozen=True)
class Tier:
    name: str
    target_count: int
    english_path: Path
    english_output: str
    expanded_output: str


@dataclass(frozen=True)
class Plan:
    config_path: Path
    multilingual_pool: Path
    output_dir: Path
    tiers: tuple[Tier, ...]


def _resolve(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def load_plan(config_path: Path) -> Plan:
    config_path = config_path.resolve()
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CorpusError(f"config does not exist: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise CorpusError(f"invalid config JSON at {config_path}: {exc}") from exc
    if config.get("schema_version") != 1:
        raise CorpusError("config schema_version must be 1")
    if config.get("language_set") != "eurobert-15":
        raise CorpusError("config language_set must be 'eurobert-15'")
    base = config_path.parent
    raw_tiers = config.get("tiers")
    if not isinstance(raw_tiers, list) or not raw_tiers:
        raise CorpusError("config tiers must be a non-empty list")
    tiers = []
    outputs: set[str] = set()
    for index, item in enumerate(raw_tiers):
        try:
            tier = Tier(
                name=item["name"],
                target_count=item["target_count"],
                english_path=_resolve(base, item["english_path"]),
                english_output=item["english_output"],
                expanded_output=item["expanded_output"],
            )
        except (KeyError, TypeError) as exc:
            raise CorpusError(f"invalid tier {index}: {exc}") from exc
        if not isinstance(tier.target_count, int) or tier.target_count < 1:
            raise CorpusError(f"tier {tier.name} target_count must be positive")
        for output in (tier.english_output, tier.expanded_output):
            if not isinstance(output, str) or Path(output).name != output:
                raise CorpusError(f"tier {tier.name} output must be a filename")
            if output in outputs:
                raise CorpusError(f"duplicate output filename: {output}")
            outputs.add(output)
        tiers.append(tier)
    counts = [tier.target_count for tier in tiers]
    if counts != sorted(counts) or len(counts) != len(set(counts)):
        raise CorpusError("target counts must be strictly increasing")
    try:
        pool = _resolve(base, config["multilingual_pool"])
        output_dir = _resolve(base, config["output_dir"])
    except KeyError as exc:
        raise CorpusError(f"config is missing {exc.args[0]!r}") from exc
    return Plan(config_path, pool, output_dir, tuple(tiers))


def read_jsonl(path: Path, *, required: Iterable[str]) -> list[Row]:
    try:
        content = path.read_bytes()
    except FileNotFoundError as exc:
        raise CorpusError(f"JSONL input does not exist: {path}") from exc
    if content and not content.endswith(b"\n"):
        raise CorpusError(f"JSONL input must end with a newline: {path}")
    rows = []
    seen: set[str] = set()
    for number, raw in enumerate(content.splitlines(keepends=True), 1):
        if not raw.strip():
            raise CorpusError(f"blank JSONL row at {path}:{number}")
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CorpusError(f"invalid UTF-8 JSON at {path}:{number}: {exc}") from exc
        if not isinstance(data, dict):
            raise CorpusError(f"row at {path}:{number} must be an object")
        missing = [field for field in required if field not in data]
        if missing:
            raise CorpusError(f"row at {path}:{number} is missing {', '.join(missing)}")
        row_id = data["id"]
        if not isinstance(row_id, str) or not row_id:
            raise CorpusError(f"row id at {path}:{number} must be a non-empty string")
        if row_id in seen:
            raise CorpusError(f"duplicate row id {row_id!r} in {path}")
        if not isinstance(data["note"], str) or not data["note"].strip():
            raise CorpusError(f"row {row_id!r} has an empty note")
        if not isinstance(data["gold"], list):
            raise CorpusError(f"row {row_id!r} has non-list gold")
        rows.append(Row(data, raw))
        seen.add(row_id)
    return rows


def _by_id(rows: Iterable[Row]) -> dict[str, Row]:
    return {row.row_id: row for row in rows}


def validate_english_tiers(english: list[list[Row]], tiers: tuple[Tier, ...]) -> None:
    for lower_rows, upper_rows, lower, upper in zip(
        english, english[1:], tiers, tiers[1:]
    ):
        lower_by_id = _by_id(lower_rows)
        upper_by_id = _by_id(upper_rows)
        missing = sorted(set(lower_by_id) - set(upper_by_id))
        if missing:
            raise CorpusError(
                f"English tier {lower.name} is not contained in {upper.name}: {missing[0]}"
            )
        changed = sorted(
            row_id for row_id, row in lower_by_id.items()
            if row.raw != upper_by_id[row_id].raw
        )
        if changed:
            raise CorpusError(
                f"English tier {lower.name} changes inside {upper.name}: {changed[0]}"
            )


def validate_multilingual(rows: list[Row], english_ids: set[str]) -> None:
    notes: set[str] = set()
    for row in rows:
        data = row.data
        if row.row_id in english_ids:
            raise CorpusError(f"multilingual id collides with English: {row.row_id}")
        language = data["language"]
        if language not in NON_ENGLISH_LANGUAGES:
            raise CorpusError(f"row {row.row_id} has unsupported language {language!r}")
        if data["provenance"] != "generated-from-open-source":
            raise CorpusError(f"row {row.row_id} lacks open-source provenance")
        source = data["source"]
        if not isinstance(source, dict) or not all(
            source.get(field) for field in ("repo", "url", "sha", "paths")
        ):
            raise CorpusError(f"row {row.row_id} has incomplete source provenance")
        if data["note"] in notes:
            raise CorpusError(f"duplicate multilingual note at {row.row_id}")
        notes.add(data["note"])
        for fact in data["gold"]:
            if not isinstance(fact, dict):
                raise CorpusError(f"row {row.row_id} has malformed gold")
            for field in ("subject", "relation", "object"):
                if not isinstance(fact.get(field), str) or not fact[field]:
                    raise CorpusError(f"row {row.row_id} has malformed gold field {field}")
            if fact["subject"] not in data["note"] or fact["object"] not in data["note"]:
                raise CorpusError(f"row {row.row_id} has ungrounded gold")


def sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def derive(plan: Plan) -> tuple[dict[str, bytes], dict[str, Any]]:
    english = [
        read_jsonl(tier.english_path, required=REQUIRED_GOLD_FIELDS)
        for tier in plan.tiers
    ]
    validate_english_tiers(english, plan.tiers)
    multilingual = read_jsonl(
        plan.multilingual_pool, required=REQUIRED_MULTILINGUAL_FIELDS
    )
    expected_pool_rows = plan.tiers[-1].target_count - len(english[-1])
    if len(multilingual) != expected_pool_rows:
        raise CorpusError(
            f"multilingual pool must contain {expected_pool_rows} rows, "
            f"found {len(multilingual)}"
        )
    validate_multilingual(multilingual, set(_by_id(english[-1])))
    outputs: dict[str, bytes] = {}
    manifest_tiers = []
    previous_expanded: dict[str, bytes] = {}
    for tier, english_rows in zip(plan.tiers, english):
        additions_needed = tier.target_count - len(english_rows)
        if additions_needed < 0 or additions_needed > len(multilingual):
            raise CorpusError(f"cannot fill expanded tier {tier.name}")
        selected = multilingual[:additions_needed]
        english_content = b"".join(row.raw for row in english_rows)
        expanded_rows = english_rows + selected
        expanded_by_id = {row.row_id: row.raw for row in expanded_rows}
        if len(expanded_by_id) != len(expanded_rows):
            raise CorpusError(f"duplicate id in expanded tier {tier.name}")
        if any(
            expanded_by_id.get(row_id) != raw
            for row_id, raw in previous_expanded.items()
        ):
            raise CorpusError(f"expanded tier {tier.name} does not contain its predecessor")
        expanded_content = b"".join(row.raw for row in expanded_rows)
        if len(expanded_rows) != tier.target_count:
            raise CorpusError(f"tier {tier.name} has {len(expanded_rows)} rows")
        outputs[tier.english_output] = english_content
        outputs[tier.expanded_output] = expanded_content
        counts = Counter(row.data["language"] for row in selected)
        if len(selected) >= len(NON_ENGLISH_LANGUAGES) and set(counts) != set(
            NON_ENGLISH_LANGUAGES
        ):
            raise CorpusError(f"tier {tier.name} does not cover all 14 added languages")
        if counts and max(counts.values()) - min(counts.values()) > 1:
            raise CorpusError(f"tier {tier.name} has imbalanced languages")
        manifest_tiers.extend([
            {
                "name": tier.english_output.removesuffix(".jsonl"),
                "rows": len(english_rows),
                "languages": {"en": len(english_rows)},
                "sha256": sha256(english_content),
                "source": os.path.relpath(tier.english_path, plan.config_path.parent),
            },
            {
                "name": tier.expanded_output.removesuffix(".jsonl"),
                "rows": len(expanded_rows),
                "languages": {"en": len(english_rows), **dict(sorted(counts.items()))},
                "sha256": sha256(expanded_content),
            },
        ])
        previous_expanded = expanded_by_id
    pool_content = b"".join(row.raw for row in multilingual)
    manifest = {
        "schema_version": 1,
        "language_set": "eurobert-15",
        "languages": list(EUROBERT_LANGUAGES),
        "multilingual_pool": os.path.relpath(plan.multilingual_pool, plan.config_path.parent),
        "multilingual_pool_sha256": sha256(pool_content),
        "tiers": manifest_tiers,
    }
    outputs["manifest.json"] = (
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    return outputs, manifest


def write_outputs(output_dir: Path, outputs: dict[str, bytes]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".build-", dir=output_dir) as raw:
        temporary = Path(raw)
        for name, content in outputs.items():
            (temporary / name).write_bytes(content)
        for name in outputs:
            os.replace(temporary / name, output_dir / name)


def validate_outputs(output_dir: Path, expected: dict[str, bytes]) -> None:
    for name, content in expected.items():
        path = output_dir / name
        try:
            actual = path.read_bytes()
        except FileNotFoundError as exc:
            raise CorpusError(f"generated output does not exist: {path}") from exc
        if actual != content:
            raise CorpusError(f"generated output is stale or modified: {path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "validate"))
    parser.add_argument(
        "--config", type=Path, default=Path(__file__).with_name("corpus-plan.json")
    )
    args = parser.parse_args(argv)
    try:
        plan = load_plan(args.config)
        outputs, manifest = derive(plan)
        if args.command == "build":
            write_outputs(plan.output_dir, outputs)
        else:
            validate_outputs(plan.output_dir, outputs)
    except CorpusError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    action = "built" if args.command == "build" else "validated"
    print(f"{action} " + ", ".join(f"{t['name']}={t['rows']}" for t in manifest["tiers"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
