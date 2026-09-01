#!/usr/bin/env python3
"""Show that Perseus accepts an unrelated exact quote as support for a claim."""

import importlib.util
import json
import sys


def load_perseus(path: str):
    spec = importlib.util.spec_from_file_location("perseus_review", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


perseus = load_perseus(sys.argv[1])
source = {
    "id": "src1",
    "path": "source.md",
    "label": "source.md",
    "lines": ["# Source", "", "The resolver builds a dependency graph."],
}
raw = {
    "claims": [
        {
            "text": "Perseus was independently audited by NASA.",
            "citations": [
                {
                    "source_id": "src1",
                    "line_start": 3,
                    "line_end": 3,
                    "quote": "The resolver builds a dependency graph.",
                }
            ],
        }
    ]
}
accepted, dropped = perseus._validate_synthesis_claims(raw, [source], 6)
print(json.dumps({"accepted": accepted, "dropped": dropped}, indent=2, sort_keys=True))
