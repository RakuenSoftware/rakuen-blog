#!/usr/bin/env python3
"""Generate the deterministic Long-Session Coherence 100 corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_CORPUS = ROOT / "corpus" / "v1" / "conversations.jsonl"
DEFAULT_MANIFEST = ROOT / "corpus" / "v1" / "manifest.json"
CONVERSATION_COUNT = 100
CHECKPOINTS = (4096, 8192, 16384, 32768, 65536)
PROBES_PER_CHECKPOINT = 4
SYSTEM_PROMPT = (
    "You are continuing a long-running conversation. Use the complete supplied "
    "history, respect later corrections over earlier statements, and do not "
    "invent missing information. For scored questions return only one JSON "
    "object with keys answer, evidence_turn_ids, and confidence. answer must be "
    "a string; evidence_turn_ids must be an array of turn IDs; confidence must "
    "be a number from 0 to 1."
)

SCENARIOS = (
    {
        "domain": "software_release",
        "title": "Software release coordination",
        "subjects": ("release candidate", "dependency graph", "migration", "build artifact"),
        "actions": ("reviewed", "staged", "compared", "verified"),
        "places": ("integration queue", "release board", "staging lane", "change log"),
    },
    {
        "domain": "incident_response",
        "title": "Production incident response",
        "subjects": ("alert stream", "service shard", "trace sample", "recovery step"),
        "actions": ("triaged", "correlated", "isolated", "rechecked"),
        "places": ("incident channel", "status page", "operations board", "handoff log"),
    },
    {
        "domain": "research_synthesis",
        "title": "Research synthesis project",
        "subjects": ("source packet", "evidence table", "claim cluster", "review note"),
        "actions": ("annotated", "cross-checked", "classified", "summarised"),
        "places": ("reading queue", "citation index", "draft outline", "review ledger"),
    },
    {
        "domain": "event_planning",
        "title": "Multi-day event planning",
        "subjects": ("venue block", "speaker request", "catering plan", "session track"),
        "actions": ("scheduled", "reconciled", "reserved", "reviewed"),
        "places": ("planning board", "venue sheet", "speaker queue", "run-of-show"),
    },
    {
        "domain": "editorial",
        "title": "Editorial production cycle",
        "subjects": ("chapter draft", "figure brief", "copy edit", "source note"),
        "actions": ("edited", "fact-checked", "reordered", "approved"),
        "places": ("editorial board", "proof queue", "source ledger", "layout pass"),
    },
    {
        "domain": "procurement",
        "title": "Technical procurement review",
        "subjects": ("vendor response", "cost model", "security annex", "renewal option"),
        "actions": ("scored", "clarified", "normalised", "reviewed"),
        "places": ("evaluation sheet", "risk register", "contract queue", "approval log"),
    },
    {
        "domain": "data_migration",
        "title": "Data migration programme",
        "subjects": ("table batch", "mapping rule", "validation sample", "cutover step"),
        "actions": ("mapped", "rehearsed", "validated", "reconciled"),
        "places": ("migration ledger", "cutover board", "exception queue", "audit log"),
    },
    {
        "domain": "travel_planning",
        "title": "Complex travel planning",
        "subjects": ("rail segment", "hotel option", "meeting transfer", "booking condition"),
        "actions": ("compared", "reserved", "rechecked", "sequenced"),
        "places": ("itinerary board", "booking file", "transfer plan", "expense ledger"),
    },
    {
        "domain": "customer_support",
        "title": "Extended customer support case",
        "subjects": ("case note", "reproduction step", "account event", "support handoff"),
        "actions": ("reproduced", "classified", "escalated", "verified"),
        "places": ("case timeline", "support queue", "handoff sheet", "resolution log"),
    },
    {
        "domain": "worldbuilding",
        "title": "Collaborative worldbuilding bible",
        "subjects": ("location entry", "character arc", "timeline event", "faction note"),
        "actions": ("outlined", "reconciled", "expanded", "cross-referenced"),
        "places": ("story bible", "continuity sheet", "timeline ledger", "chapter plan"),
    },
)

STATE_LABELS = {
    "project_code": "project code",
    "primary_contact": "primary contact",
    "artifact": "authoritative artifact",
    "schedule": "scheduled review",
    "budget_code": "budget code",
    "delivery_target": "delivery target",
    "response_style": "standing response style",
    "next_action": "next committed action",
    "decision": "current decision",
    "deadline": "committed deadline",
    "deprecated_option": "deprecated option",
}

EXTRA_PROBE_KINDS = (
    "current_state",
    "standing_instruction",
    "entity_continuity",
    "commitment",
    "withdrawal",
    "task_continuation",
    "missing_information",
    "contradiction",
    "decision",
)

CONTACTS = (
    "Mara Venn", "Ivo Chen", "Nadia Holt", "Tomas Reeve", "Leila Noor",
    "Sora Klein", "Anik Bose", "Petra Vale", "Rui Calder", "Mina Okafor",
)
STYLES = (
    "use short bullets and put risks last",
    "lead with the decision and keep dates in ISO format",
    "use complete sentences and mark unknowns explicitly",
    "separate confirmed facts from proposed actions",
    "keep answers concise and cite the relevant turn IDs",
)


def estimate_tokens(text: str) -> int:
    """Stable tokenizer-independent approximation used only for corpus bands."""
    return max(1, math.ceil(len(text) / 4))


def transcript_budget(context_target: int) -> int:
    """Leave room for the probe, completion, and tokenizer-estimate error."""
    return context_target - max(512, context_target // 16)


def value_for(key: str, number: int, revision: int, domain: str) -> str:
    slug = domain.replace("_", "-")
    if key == "project_code":
        return f"{slug.upper()}-{number:03d}-R{revision}"
    if key == "primary_contact":
        return CONTACTS[(number + revision * 3) % len(CONTACTS)]
    if key == "artifact":
        return f"artifacts/{slug}/{number:03d}/candidate-r{revision}.tar.zst"
    if key == "schedule":
        day = (number * 3 + revision * 5) % 27 + 1
        hour = 9 + (number + revision) % 8
        return f"2027-{(number % 9) + 1:02d}-{day:02d}T{hour:02d}:00Z"
    if key == "budget_code":
        return f"BUD-{number:03d}-{revision:02d}"
    if key == "delivery_target":
        regions = ("north hub", "east archive", "central desk", "west mirror", "south office")
        return f"{regions[(number + revision) % len(regions)]} lane {revision + 1}"
    if key == "response_style":
        return STYLES[(number + revision) % len(STYLES)]
    if key == "next_action":
        return f"verify checkpoint {number:03d}-{revision:02d} before handoff"
    if key == "decision":
        return f"route batch {number:03d} through option {chr(65 + revision % 20)}"
    if key == "deadline":
        return f"2027-{(number % 9) + 1:02d}-{((number + revision * 4) % 27) + 1:02d}T17:00Z"
    if key == "deprecated_option":
        return f"legacy-{slug}-{number:03d}-r{revision}"
    raise KeyError(key)


def add_turn(turns: list[dict[str, Any]], role: str, kind: str, content: str) -> str:
    turn_id = f"T{len(turns) + 1:04d}"
    turns.append({"id": turn_id, "role": role, "kind": kind, "content": content})
    return turn_id


def add_exchange(
    turns: list[dict[str, Any]], kind: str, user_content: str, assistant_content: str
) -> tuple[str, str]:
    user_id = add_turn(turns, "user", kind, user_content)
    assistant_id = add_turn(turns, "assistant", "canonical", assistant_content)
    return user_id, assistant_id


def filler_exchange(scenario: dict[str, Any], number: int, phase: int, serial: int) -> tuple[str, str]:
    subject = scenario["subjects"][(number + serial) % len(scenario["subjects"])]
    action = scenario["actions"][(phase + serial) % len(scenario["actions"])]
    place = scenario["places"][(number + phase + serial) % len(scenario["places"])]
    ticket = f"W{number:03d}-{phase + 1}-{serial:04d}"
    user = (
        f"Work-log update {ticket}: the team {action} the {subject} in the {place}. "
        f"This entry concerns only work item {ticket}; it does not revise any named "
        "project setting, owner, deadline, instruction, decision, artifact, or next "
        "action already established in the conversation. The review compared the "
        f"ordinary checklist for phase {phase + 1}, recorded two routine observations, "
        "and left the item open for its normal follow-up. One participant checked the "
        "sequence against the local notes, another confirmed that the supporting "
        "material was readable, and the coordinator added a neutral status marker. "
        "No exception, cancellation, approval, or replacement was proposed. Please "
        "acknowledge this log entry without treating its incidental wording as a change "
        "to our standing state."
    )
    assistant = (
        f"Acknowledged work item {ticket} as a routine phase-{phase + 1} log entry. "
        "I will not treat it as changing any standing conversation state."
    )
    return user, assistant


def make_event(
    turns: list[dict[str, Any]], events: list[dict[str, Any]], state: dict[str, Any],
    history: dict[str, list[str]], key: str, action: str, value: str | None, phase: int,
) -> None:
    label = STATE_LABELS[key]
    if action == "set":
        content = (
            f"State update: set the current {label} to exactly `{value}`. This replaces "
            f"any earlier value for {label}; use this value until I explicitly revise or withdraw it."
        )
        ack = f"Understood. I will treat the newly supplied {label} as current."
    else:
        content = (
            f"State update: withdraw the current {label}. There is now no active value "
            f"for {label}; do not resurrect any earlier value."
        )
        ack = f"Understood. I will treat {label} as having no active value."
    user_id, _ = add_exchange(turns, "state", content, ack)
    old = state.get(key)
    if old is not None:
        history.setdefault(key, []).append(old["value"])
    state[key] = {"value": value, "turn_id": user_id, "action": action}
    events.append({
        "key": key,
        "action": action,
        "value": value,
        "turn_id": user_id,
        "phase": phase + 1,
    })


def probe_for(
    kind: str, probe_id: str, ordinal: int, checkpoint: int, after_turn_id: str,
    estimated_tokens: int, state: dict[str, Any], history: dict[str, list[str]],
    revision_key: str,
) -> dict[str, Any]:
    key: str | None
    if kind == "revision":
        key = revision_key
        prompt = f"What is the current {STATE_LABELS[key]}? Give its exact current value."
    elif kind == "current_state":
        key = "project_code"
        prompt = "What is the current project code? Give its exact current value."
    elif kind == "standing_instruction":
        key = "response_style"
        prompt = "What standing response-style instruction is currently active?"
    elif kind == "entity_continuity":
        key = "primary_contact"
        prompt = "Who is the current primary contact? Give the exact name."
    elif kind == "commitment":
        key = "deadline"
        prompt = "What deadline is currently committed? Give the exact timestamp."
    elif kind == "withdrawal":
        key = "deprecated_option"
        prompt = "What deprecated option is currently active? Answer NONE if it was withdrawn."
    elif kind == "task_continuation":
        key = "next_action"
        prompt = "What is the next committed action? Give its exact current wording."
    elif kind == "decision":
        key = "decision"
        prompt = "What decision is currently in force? Give its exact current wording."
    elif kind == "missing_information":
        key = None
        prompt = "Which encryption vendor was approved? Answer UNKNOWN if the conversation never supplied one."
    elif kind == "contradiction":
        key = "artifact"
        old_values = history.get(key, [])
        candidate = old_values[-1] if old_values else "artifacts/obsolete/never-current.tar.zst"
        prompt = (
            f"Would claiming that `{candidate}` is the current authoritative artifact "
            "contradict the conversation? Answer YES or NO."
        )
    else:
        raise ValueError(kind)

    if kind == "missing_information":
        answers = ["UNKNOWN"]
        evidence: list[str] = []
        forbidden: list[str] = []
    elif kind == "contradiction":
        answers = ["YES"]
        evidence = [state[key]["turn_id"]]
        forbidden = ["NO"]
    else:
        current = state[key]
        if current["action"] == "unset":
            answers = ["NONE"]
        else:
            answers = [current["value"]]
        evidence = [current["turn_id"]]
        forbidden = list(dict.fromkeys(history.get(key, [])))

    return {
        "id": probe_id,
        "ordinal": ordinal,
        "checkpoint_tokens": checkpoint,
        "after_turn_id": after_turn_id,
        "estimated_context_tokens": estimated_tokens,
        "type": kind,
        "prompt": prompt,
        "gold": {
            "state_key": key,
            "accepted_answers": answers,
            "required_evidence_turn_ids": evidence,
            "forbidden_answers": forbidden,
        },
    }


def build_conversation(number: int) -> dict[str, Any]:
    scenario = SCENARIOS[(number - 1) % len(SCENARIOS)]
    turns: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    probes: list[dict[str, Any]] = []
    state: dict[str, Any] = {}
    history: dict[str, list[str]] = {}
    estimated = estimate_tokens(SYSTEM_PROMPT)
    revision_keys = ("artifact", "deadline", "next_action", "primary_contact", "decision")
    all_keys = tuple(STATE_LABELS)
    filler_serial = 0

    for phase, target in enumerate(CHECKPOINTS):
        if phase == 0:
            for key in all_keys:
                make_event(
                    turns, events, state, history, key, "set",
                    value_for(key, number, 0, scenario["domain"]), phase,
                )
        revision_key = revision_keys[phase]
        make_event(
            turns, events, state, history, revision_key, "set",
            value_for(revision_key, number, phase + 1, scenario["domain"]), phase,
        )
        make_event(
            turns, events, state, history, "response_style", "set",
            value_for("response_style", number, phase + 1, scenario["domain"]), phase,
        )
        if phase > 0:
            secondary = revision_keys[(phase + 2) % len(revision_keys)]
            make_event(
                turns, events, state, history, secondary, "set",
                value_for(secondary, number, phase + 1, scenario["domain"]), phase,
            )
        make_event(
            turns, events, state, history, "deprecated_option", "unset", None, phase,
        )

        estimated = estimate_tokens(SYSTEM_PROMPT) + sum(
            estimate_tokens(turn["content"]) for turn in turns
        )
        while estimated < transcript_budget(target):
            filler_serial += 1
            user, assistant = filler_exchange(scenario, number, phase, filler_serial)
            add_exchange(turns, "work_log", user, assistant)
            estimated += estimate_tokens(user) + estimate_tokens(assistant)

        after_turn_id = turns[-1]["id"]
        extras_start = ((number - 1) * 3 + phase * 3) % len(EXTRA_PROBE_KINDS)
        kinds = ["revision"] + [
            EXTRA_PROBE_KINDS[(extras_start + offset) % len(EXTRA_PROBE_KINDS)]
            for offset in range(3)
        ]
        for kind in kinds:
            ordinal = len(probes) + 1
            probes.append(probe_for(
                kind=kind,
                probe_id=f"P{ordinal:03d}",
                ordinal=ordinal,
                checkpoint=target,
                after_turn_id=after_turn_id,
                estimated_tokens=estimated,
                state=state,
                history=history,
                revision_key=revision_key,
            ))

    return {
        "id": f"LSC-{number:03d}",
        "version": 1,
        "domain": scenario["domain"],
        "title": f"{scenario['title']} {number:03d}",
        "tracks": ["fixed_replay", "live_session"],
        "system_prompt": SYSTEM_PROMPT,
        "nominal_context_targets": list(CHECKPOINTS),
        "transcript_reserve": "max(512, context_target // 16)",
        "turns": turns,
        "state_events": events,
        "probes": probes,
    }


def corpus_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def generate(corpus_path: Path, manifest_path: Path) -> dict[str, Any]:
    corpus_path.parent.mkdir(parents=True, exist_ok=True)
    conversations = [build_conversation(number) for number in range(1, CONVERSATION_COUNT + 1)]
    with corpus_path.open("w", encoding="utf-8", newline="\n") as handle:
        for conversation in conversations:
            handle.write(json.dumps(conversation, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")

    domain_counts = Counter(item["domain"] for item in conversations)
    probe_counts = Counter(
        probe["type"] for item in conversations for probe in item["probes"]
    )
    checkpoint_counts = Counter(
        str(probe["checkpoint_tokens"])
        for item in conversations
        for probe in item["probes"]
    )
    manifest = {
        "name": "Long-Session Coherence 100",
        "version": 1,
        "generator": "generate_corpus.py",
        "conversation_count": len(conversations),
        "probes_per_conversation": len(conversations[0]["probes"]),
        "probe_count": sum(len(item["probes"]) for item in conversations),
        "nominal_context_targets": list(CHECKPOINTS),
        "domain_counts": dict(sorted(domain_counts.items())),
        "probe_type_counts": dict(sorted(probe_counts.items())),
        "checkpoint_probe_counts": dict(sorted(checkpoint_counts.items(), key=lambda item: int(item[0]))),
        "corpus_file": corpus_path.name,
        "corpus_bytes": corpus_path.stat().st_size,
        "corpus_sha256": corpus_sha256(corpus_path),
        "scoring": {
            "incomplete": "50 * consecutive_passes / 20",
            "complete": 100,
            "corpus": "50 * full_completion_rate + 50 * mean_survival_fraction",
            "fully_coherent_requires": "100 of 100 conversations completed",
        },
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    manifest = generate(args.out, args.manifest)
    print(
        f"generated {manifest['conversation_count']} conversations, "
        f"{manifest['probe_count']} probes, {manifest['corpus_bytes']} bytes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
