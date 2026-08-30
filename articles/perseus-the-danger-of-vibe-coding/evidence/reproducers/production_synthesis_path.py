#!/usr/bin/env python3
"""Report what the reviewed public synthesis entry point returns."""

import importlib.util
import json
from pathlib import Path
import sys


def load_perseus(path: str):
    spec = importlib.util.spec_from_file_location("perseus_review", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


perseus = load_perseus(sys.argv[1])
source = Path(sys.argv[2]).resolve()
result, exit_code = perseus.synthesize_question(
    "Who audited Perseus?",
    [str(source)],
    {
        "render": {"allow_outside_workspace": True},
        "generation": {"max_claims": 6},
    },
    source.parent,
    llm="configured-but-unused",
    enable_generation=True,
)
print(
    json.dumps(
        {
            "exit_code": exit_code,
            "generated": result["generated"],
            "claims": result["claims"],
            "dropped_claims": result["dropped_claims"],
            "prompt_present": bool(result["prompt"]),
            "note": result.get("note"),
        },
        indent=2,
        sort_keys=True,
    )
)
