#!/usr/bin/env python3
"""Drive the synthesis fixture across the quant-ladder arms, on the 5080.

This does NOT fork `run_candidate_matrix.py`. It imports it and overrides
exactly three things, so that everything the synthesis article validated —
case-population checks, model-identity checks, artifact hashing, the fail-closed
result validator, the single-slot load profile, the run lock — keeps running
unchanged over the ladder arms.

The three overrides, and why each is necessary:

1. `CANDIDATES` is generated from `arms.tsv` instead of being the article's nine
   hardcoded configurations. Same schema, one entry per ladder arm.

2. `validate_candidate_matrix` is replaced. The original refuses any Gemma
   target that is not QAT UD-Q4:

       if candidate.get("target_training") != "QAT" or "qat" not in target:
           raise RuntimeError(...)
       if not quant.startswith("UD-Q4") ...

   That is exactly right for the article it was written for and exactly wrong
   here — it would reject 20 of the 33 arms, including every non-QAT Gemma rung,
   which is most of the ladder. The replacement enforces what a *ladder* needs
   instead: every arm well-formed, labels unique, and every model's rungs drawn
   from one publisher so that a ladder never mixes weights lineages.

3. `LOAD_PROFILE["device"]` becomes `CUDA0`. The article's profile names
   `Vulkan1`, which is the RX 7900 XTX on the other host. This campaign runs on
   the RTX 5080.

Consequence of (3), stated rather than discovered later: these synthesis numbers
share a fixture and a scorer with the published nine-configuration matrix but
NOT a device, so they do not join that table. They are internally comparable
across ladder arms, which is what the ladder needs.

`prompt_cache_mib` stays at 1024. That value is results-affecting in this series
— the 10,000-note ladder had to be re-taken because two families had been run at
different `--cache-ram` settings — so it is held fixed across every arm.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "bundle" / "synthesis"))

import run_candidate_matrix as rcm  # noqa: E402


ARMS = Path(__file__).resolve().parent / "arms.tsv"


def expected_model_name(target: str) -> str:
    """Reproduce the model identity llama.cpp will report for a -hf target.

    `unsloth/gemma-4-E2B-it-qat-GGUF:UD-Q4_K_XL` -> `gemma-4-E2B-it-qat-UD-Q4_K_XL`
    `LiquidAI/LFM2.5-2.6B-GGUF:Q6_K`             -> `LFM2.5-2.6B-Q6_K`

    The controller checks this substring against the served model path and
    raises on a mismatch, which is the guard that catches a target silently
    resolving to a different file than the one asked for.
    """
    repo, _, quant = target.partition(":")
    stem = repo.split("/")[-1]
    if stem.endswith("-GGUF"):
        stem = stem[: -len("-GGUF")]
    return f"{stem}-{quant}"


def load_arms() -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    with ARMS.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#") or not line.strip():
                continue
            row = line.rstrip("\n").split("\t")
            if row[0] == "order":
                continue
            if len(row) != 10:
                raise RuntimeError(f"arms.tsv: expected 10 fields, got {len(row)}: {row!r}")
            _order, label, model, train, width, target, draft, _est, ctk, ctv = row
            candidates.append(
                {
                    "label": label,
                    "family": model,
                    "target_training": "QAT" if train == "qat" else "base",
                    "target_quantization": width.upper(),
                    "target": target,
                    "draft": draft if draft != "-" else None,
                    "expected_model": expected_model_name(target),
                    "speculative": draft != "-",
                    "cache_type_k": ctk,
                    "cache_type_v": ctv,
                }
            )
    if not candidates:
        raise RuntimeError(f"arms.tsv produced no candidates: {ARMS}")
    return candidates


def validate_ladder(candidates: list[dict[str, object]]) -> None:
    """What a ladder requires, in place of the article's QAT-only rule."""
    labels = [str(c["label"]) for c in candidates]
    duplicates = {label for label in labels if labels.count(label) > 1}
    if duplicates:
        raise RuntimeError(f"duplicate arm labels: {sorted(duplicates)}")

    publishers: dict[str, set[str]] = {}
    for candidate in candidates:
        target = str(candidate["target"])
        if ":" not in target or "/" not in target:
            raise RuntimeError(f"{candidate['label']}: malformed target {target!r}")
        if candidate["speculative"] and not candidate["draft"]:
            raise RuntimeError(f"{candidate['label']}: speculative with no draft")
        publishers.setdefault(str(candidate["family"]), set()).add(target.split("/")[0])

    # A ladder that mixes publishers between its own rungs is not a ladder; it
    # is the mistake quant-clarification-2026-08-09.md records having already
    # been made once, by pairing a Q4 from one campaign against Q6 and Q8 from
    # another. Note this checks TARGET publishers only: Qwen deliberately takes
    # its draft from ggml-org because unsloth ships no MTP sidecar for it, and
    # that draft is identical across all of that model's rungs.
    for model, names in sorted(publishers.items()):
        if len(names) > 1:
            raise RuntimeError(
                f"{model}: rungs span multiple publishers {sorted(names)}; "
                "a ladder must hold weights lineage constant"
            )


def selected_labels() -> set[str]:
    """Whatever --labels names, read from argv before the controller parses it."""
    labels = ""
    for i, arg in enumerate(sys.argv):
        if arg == "--labels" and i + 1 < len(sys.argv):
            labels = sys.argv[i + 1]
        elif arg.startswith("--labels="):
            labels = arg.split("=", 1)[1]
    return {part.strip() for part in labels.split(",") if part.strip()}


def main() -> int:
    candidates = load_arms()
    validate_ladder(candidates)

    wanted = selected_labels()
    selected = [c for c in candidates if not wanted or str(c["label"]) in wanted]
    if not selected:
        raise RuntimeError(f"--labels matched no arm in arms.tsv: {sorted(wanted)}")

    # One load profile per results root. The controller compares each arm's
    # recorded load profile against LOAD_PROFILE and raises on any difference,
    # which is correct and worth keeping -- but KV cache type is part of the
    # serving configuration, so arms with different cache types genuinely cannot
    # share a root. Fail here with a clear reason rather than deep inside a run.
    kv = {(c["cache_type_k"], c["cache_type_v"]) for c in selected}
    if len(kv) > 1:
        raise RuntimeError(
            f"selected arms span multiple KV cache types {sorted(kv)}; the "
            "controller requires one load profile per results root, so these "
            "must be run into separate roots"
        )
    ctk, ctv = next(iter(kv))

    rcm.CANDIDATES = tuple(candidates)
    rcm.validate_candidate_matrix = lambda: validate_ladder(list(rcm.CANDIDATES))
    rcm.LOAD_PROFILE["device"] = "CUDA0"
    # In the profile so the cache type is provable from the artifacts rather
    # than inferred from a label, and so the controller's own equality check
    # catches drift between arms.
    rcm.LOAD_PROFILE["cache_type_k"] = ctk
    rcm.LOAD_PROFILE["cache_type_v"] = ctv
    # Recorded so the divergence from the published matrix's profile is visible
    # in every artifact rather than living only in this comment.
    rcm.LOAD_PROFILE["reasoning"] = "off"
    rcm.LOAD_PROFILE["reasoning_format"] = "none"

    # The stock controller never emits -ctk/-ctv. Without this every arm would
    # serve at the f16 default whatever the manifest said, and the KV sweep
    # would have produced five identical configurations under five different
    # labels -- five runs that agree perfectly and mean nothing.
    stock_command = rcm.candidate_command

    def command_with_cache(candidate, llama_server, port):
        command = stock_command(candidate, llama_server, port)
        command += ["-ctk", str(candidate["cache_type_k"]),
                    "-ctv", str(candidate["cache_type_v"])]
        # Reasoning is forced off at the SERVER, not merely requested through the
        # chat template.
        #
        # The runner asks for {"enable_thinking": false} as a template kwarg. Every
        # model in the published nine-configuration matrix honours it and truncates
        # on zero of 1,000 cases. LFM2.5 does not: it reasons anyway, llama.cpp
        # routes the reasoning into a separate channel from `content`, the model
        # spends all 1,536 tokens thinking, and the harness records
        # finish_reason=length with content='' -- an EMPTY string, not a cut-off
        # answer. That reads as 51-59% "truncation" and a content_f1 of 0.14, none
        # of which measures synthesis quality.
        #
        # --reasoning off applies the same intent the template kwarg expresses,
        # from a layer the model cannot ignore. --reasoning-format none is the
        # backstop: if a template still emits thoughts, they stay in
        # message.content and are scored rather than silently discarded, which is
        # how Muse Glimmer behaved in the published matrix.
        command += ["--reasoning", "off", "--reasoning-format", "none"]
        if candidate.get("draft"):
            # The draft model's cache defaults to f16 independently of the
            # target's, so it has to be set too or the arm is not the
            # configuration its label claims.
            command += ["-ctkd", str(candidate["cache_type_k"]),
                        "-ctvd", str(candidate["cache_type_v"])]
        return command

    rcm.candidate_command = command_with_cache

    print(
        f"ladder: {len(candidates)} arms, {len(selected)} selected, "
        f"device={rcm.LOAD_PROFILE['device']}, "
        f"cache_ram={rcm.LOAD_PROFILE['prompt_cache_mib']}MiB, "
        f"ctk={ctk} ctv={ctv}",
        flush=True,
    )
    return rcm.main()


if __name__ == "__main__":
    raise SystemExit(main())
