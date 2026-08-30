#!/usr/bin/env python3
"""Force Perseus's documented fail-open lock path and race two claimers."""

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import threading


def load_perseus(path: str):
    spec = importlib.util.spec_from_file_location("perseus_review", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


perseus = load_perseus(sys.argv[1])
results = []
results_lock = threading.Lock()
barrier = threading.Barrier(2)

with tempfile.TemporaryDirectory(prefix="perseus-agora-review-") as temp_dir:
    task = Path(temp_dir) / "task-1-demo.md"
    task.write_text(
        "---\n"
        "id: task-1\n"
        "title: Demo\n"
        "status: open\n"
        "scope: small\n"
        "depends_on: []\n"
        "claimed_by: null\n"
        "opened: 2026-08-30\n"
        "closed: null\n"
        "---\n"
        "# Demo\n",
        encoding="utf-8",
    )
    original_load = perseus._load_task_file

    def synchronized_open_read(path):
        frontmatter, body = original_load(path)
        if frontmatter.get("status") == "open":
            barrier.wait(timeout=5)
        return frontmatter, body

    perseus._load_task_file = synchronized_open_read
    perseus._lock_file_handle = lambda _handle: None
    perseus._unlock_file_handle = lambda _handle: None

    def claim(agent):
        outcome = perseus._claim_task_under_lock(task, agent)
        with results_lock:
            results.append({"agent": agent, "won": outcome[0], "holder": outcome[1]})

    threads = [threading.Thread(target=claim, args=(agent,)) for agent in ("agent-a", "agent-b")]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=10)

    final_frontmatter, _ = original_load(task)
    print(
        json.dumps(
            {
                "simulated_condition": "advisory lock acquisition failed and helper continued",
                "claim_results": sorted(results, key=lambda item: item["agent"]),
                "final_claimed_by": final_frontmatter.get("claimed_by"),
                "final_status": final_frontmatter.get("status"),
            },
            indent=2,
            sort_keys=True,
        )
    )
