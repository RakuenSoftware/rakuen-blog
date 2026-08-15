#!/usr/bin/env python3
"""Run the matched synthesis candidate matrix on one RX 7900 XTX.

The controller is intentionally single-slot. MTP is repeatable within an MTP
arm but does not compose safely with multi-slot concurrency on the pinned
llama.cpp backend. All Gemma and Qwen targets therefore run with MTP enabled at
one slot; Muse Glimmer runs with DFlash disabled. Every arm uses the same GPU,
runtime, context, prompt cache, fixture, runner, scorer, and request order.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import platform
import signal
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


CANDIDATES: tuple[dict[str, Any], ...] = (
    {
        "label": "gemma4_e2b_qat_udq4_mtp",
        "family": "Gemma 4",
        "target_training": "QAT",
        "target_quantization": "UD-Q4_K_XL",
        "target": "unsloth/gemma-4-E2B-it-qat-GGUF:UD-Q4_K_XL",
        "draft": "unsloth/gemma-4-E2B-it-qat-GGUF:MTP/mtp-gemma-4-E2B-it-Q8_0.gguf",
        "expected_model": "gemma-4-E2B-it-qat-UD-Q4_K_XL",
        "speculative": True,
    },
    {
        "label": "gemma4_e4b_qat_udq4_mtp",
        "family": "Gemma 4",
        "target_training": "QAT",
        "target_quantization": "UD-Q4_K_XL",
        "target": "unsloth/gemma-4-E4B-it-qat-GGUF:UD-Q4_K_XL",
        "draft": "unsloth/gemma-4-E4B-it-qat-GGUF:MTP/mtp-gemma-4-E4B-it-Q8_0.gguf",
        "expected_model": "gemma-4-E4B-it-qat-UD-Q4_K_XL",
        "speculative": True,
    },
    {
        "label": "gemma4_12b_qat_udq4_mtp",
        "family": "Gemma 4",
        "target_training": "QAT",
        "target_quantization": "UD-Q4_K_XL",
        "target": "unsloth/gemma-4-12B-it-qat-GGUF:UD-Q4_K_XL",
        "draft": "unsloth/gemma-4-12B-it-qat-GGUF:MTP/mtp-gemma-4-12B-it-Q8_0.gguf",
        "expected_model": "gemma-4-12B-it-qat-UD-Q4_K_XL",
        "speculative": True,
    },
    {
        "label": "gemma4_26b_a4b_qat_udq4_mtp",
        "family": "Gemma 4",
        "target_training": "QAT",
        "target_quantization": "UD-Q4_K_XL",
        "target": "unsloth/gemma-4-26B-A4B-it-qat-GGUF:UD-Q4_K_XL",
        "draft": "unsloth/gemma-4-26B-A4B-it-qat-GGUF:MTP/mtp-gemma-4-26B-A4B-it-Q8_0.gguf",
        "expected_model": "gemma-4-26B-A4B-it-qat-UD-Q4_K_XL",
        "speculative": True,
    },
    {
        "label": "gemma4_31b_qat_udq4_mtp",
        "family": "Gemma 4",
        "target_training": "QAT",
        "target_quantization": "UD-Q4_K_XL",
        "target": "unsloth/gemma-4-31B-it-qat-GGUF:UD-Q4_K_XL",
        "draft": "unsloth/gemma-4-31B-it-qat-GGUF:MTP/mtp-gemma-4-31B-it-Q8_0.gguf",
        "expected_model": "gemma-4-31B-it-qat-UD-Q4_K_XL",
        "speculative": True,
    },
    {
        "label": "qwen36_27b_q4_mtp",
        "family": "Qwen 3.6",
        "target_quantization": "Q4_K_M",
        "target": "ggml-org/Qwen3.6-27B-GGUF:Q4_K_M",
        "draft": "ggml-org/Qwen3.6-27B-GGUF",
        "hf_home": "/mnt/media/storage/models/hf",
        "expected_model": "Qwen3.6-27B-Q4_K_M",
        "speculative": True,
    },
    {
        "label": "qwen36_35b_a3b_q4_mtp",
        "family": "Qwen 3.6",
        "target_quantization": "Q4_K_M",
        "target": "ggml-org/Qwen3.6-35B-A3B-GGUF:Q4_K_M",
        "draft": "ggml-org/Qwen3.6-35B-A3B-GGUF",
        "hf_home": "/mnt/media/storage/models/hf",
        "expected_model": "Qwen3.6-35B-A3B-Q4_K_M",
        "speculative": True,
    },
    {
        "label": "qwen38_27b_q4_mtp",
        "family": "Qwen 3.8",
        "target_quantization": "Q4_K_M",
        "target": "ggml-org/Qwen3.8-27B-GGUF:Q4_K_M",
        "draft": "ggml-org/Qwen3.8-27B-GGUF",
        "hf_home": "/mnt/media/storage/models/hf",
        "expected_model": "Qwen3.8-27B-Q4_K_M",
        "official_revision": "1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0",
        "gguf_revision": "0669b98607d47046c7c2b3f801011d54a08cfccf",
        "speculative": True,
    },
    {
        "label": "muse_glimmer_30b_kquant_dflash_off",
        "family": "Muse Glimmer",
        "target_quantization": "K-Quant 17 GB",
        "target": "meta-models/Muse-Glimmer-30B-GGUF",
        "target_file": "muse-glimmer-30B-kquant-17gb.gguf",
        "expected_model": "muse-glimmer-30B-kquant-17gb.gguf",
        "chat_template_kwargs": {"reasoning_strength": "low"},
        "speculative": False,
    },
)

LOAD_PROFILE = {
    "workers": 1,
    "parallel_slots": 1,
    "context_tokens": 8192,
    "logical_batch_tokens": 2048,
    "physical_batch_tokens": 2048,
    "prompt_cache_mib": 1024,
    "gpu_layers": 99,
    "device": "Vulkan1",
    "flash_attention": True,
    "output_constraint": "response_format strict json_schema",
}


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def json_request(url: str, timeout: int = 10) -> Any:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.load(response)


def wait_for_server(process: subprocess.Popen[str], url: str, timeout: int) -> float:
    started = time.monotonic()
    deadline = started + timeout
    last_error = ""
    while time.monotonic() < deadline:
        returncode = process.poll()
        if returncode is not None:
            raise RuntimeError(f"llama-server exited {returncode} during load")
        try:
            payload = json_request(url, timeout=5)
            if payload.get("status") == "ok":
                return time.monotonic() - started
            last_error = f"unexpected health status {payload!r}"
        except (OSError, ValueError, urllib.error.URLError) as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        time.sleep(5)
    raise RuntimeError(f"llama-server did not become healthy: {last_error}")


def port_is_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.25)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def stop_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.send_signal(signal.SIGTERM)
    try:
        process.wait(timeout=30)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=10)


def hardware_snapshot() -> dict[str, int]:
    result: dict[str, int] = {}
    gpu = Path("/sys/class/drm/card0/device")
    paths = {
        "vram_used_bytes": gpu / "mem_info_vram_used",
        "vram_total_bytes": gpu / "mem_info_vram_total",
        "gpu_busy_percent": gpu / "gpu_busy_percent",
    }
    for name, path in paths.items():
        if path.exists():
            result[name] = int(path.read_text(encoding="utf-8").strip())
    for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
        key, _, raw = line.partition(":")
        if key in {"MemAvailable", "SwapTotal", "SwapFree"}:
            result[f"{key.lower()}_bytes"] = int(raw.strip().split()[0]) * 1024
    return result


def hardware_identity() -> dict[str, Any]:
    gpu = Path("/sys/class/drm/card0/device")
    identity: dict[str, Any] = {"drm_device": "card0"}
    uevent = gpu / "uevent"
    if uevent.exists():
        for line in uevent.read_text(encoding="utf-8").splitlines():
            key, _, value = line.partition("=")
            if key in {"DRIVER", "PCI_CLASS", "PCI_ID", "PCI_SLOT_NAME"}:
                identity[key.lower()] = value
    lspci = shutil.which("lspci")
    slot = identity.get("pci_slot_name")
    if lspci and slot:
        completed = subprocess.run(
            [lspci, "-nn", "-s", str(slot)],
            capture_output=True,
            text=True,
            check=False,
        )
        identity["lspci"] = completed.stdout.strip()
    return identity


def llama_device_listing(llama_server: Path) -> str:
    environment = os.environ.copy()
    prior_library_path = environment.get("LD_LIBRARY_PATH", "")
    environment["LD_LIBRARY_PATH"] = str(llama_server.parent) + (
        f":{prior_library_path}" if prior_library_path else ""
    )
    completed = subprocess.run(
        [str(llama_server), "--list-devices"],
        capture_output=True,
        text=True,
        check=False,
        env=environment,
    )
    if completed.returncode:
        raise RuntimeError(f"llama-server --list-devices exited {completed.returncode}")
    return (completed.stdout + completed.stderr).strip()


def latest_rows(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return rows
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                row = json.loads(line)
                rows[str(row["case_id"])] = row
    return rows


def expected_case_ids(bundle: Path, max_cases: int) -> list[str]:
    result: list[str] = []
    with (bundle / "synthesis.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            result.append(str(json.loads(line)["case_id"]))
            if max_cases and len(result) >= max_cases:
                break
    return result


def validate_result(
    bundle: Path,
    result_dir: Path,
    candidate: dict[str, Any],
    max_cases: int,
) -> dict[str, Any]:
    label = str(candidate["label"])
    ids = expected_case_ids(bundle, max_cases)
    raw_path = result_dir / f"raw_{label}.jsonl"
    summary_path = result_dir / f"summary_{label}.json"
    hardware_path = result_dir / "hardware_synthesis.json"
    latest = latest_rows(raw_path)
    if set(latest) != set(ids):
        raise RuntimeError(
            f"{label}: result population differs: "
            f"missing={len(set(ids) - set(latest))}, extra={len(set(latest) - set(ids))}"
        )
    failed = [case_id for case_id, row in latest.items() if not row.get("ok")]
    if failed:
        raise RuntimeError(f"{label}: {len(failed)} latest rows are unsuccessful")
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    suite_hash = sha256(bundle / "manifest.json")
    if summary.get("suite_manifest_sha256") != suite_hash:
        raise RuntimeError(f"{label}: suite manifest hash mismatch")
    if int(summary.get("overall", {}).get("n", -1)) != len(ids):
        raise RuntimeError(f"{label}: summary case count mismatch")
    hardware = json.loads(hardware_path.read_text(encoding="utf-8"))
    if hardware.get("load_profile") != LOAD_PROFILE:
        raise RuntimeError(f"{label}: load profile mismatch")
    if hardware.get("candidate") != candidate:
        raise RuntimeError(f"{label}: candidate configuration mismatch")
    if str(candidate["expected_model"]).lower() not in str(
        hardware.get("model_path", "")
    ).lower():
        raise RuntimeError(f"{label}: recorded model identity mismatch")
    if hardware.get("speculative") is not bool(candidate["speculative"]):
        raise RuntimeError(f"{label}: recorded speculation state mismatch")
    return {
        "latest_rows": len(latest),
        "suite_manifest_sha256": suite_hash,
        "overall": summary["overall"],
    }


def candidate_command(
    candidate: dict[str, Any], llama_server: Path, port: int
) -> list[str]:
    command = [
        str(llama_server),
        "-hf", candidate["target"],
        "--host", "127.0.0.1",
        "--port", str(port),
        "--jinja",
        "-c", str(LOAD_PROFILE["context_tokens"]),
        "-np", str(LOAD_PROFILE["parallel_slots"]),
        "-b", str(LOAD_PROFILE["logical_batch_tokens"]),
        "-ub", str(LOAD_PROFILE["physical_batch_tokens"]),
        "--cache-ram", str(LOAD_PROFILE["prompt_cache_mib"]),
        "--device", str(LOAD_PROFILE["device"]),
        "--no-webui",
        "--no-mmproj",
        "-ngl", str(LOAD_PROFILE["gpu_layers"]),
        "-fa", "on",
    ]
    if candidate.get("target_file"):
        command += ["-hff", str(candidate["target_file"])]
    if candidate.get("draft"):
        command += ["-hfd", str(candidate["draft"])]
    return command


def validate_candidate_matrix() -> None:
    """Refuse a mixed Gemma matrix before starting or downloading anything."""
    for candidate in CANDIDATES:
        if candidate["family"] != "Gemma 4":
            continue
        target = str(candidate["target"]).lower()
        if candidate.get("target_training") != "QAT" or "qat" not in target:
            raise RuntimeError(f"{candidate['label']}: Gemma target is not QAT")
        quant = str(candidate.get("target_quantization", ""))
        if not quant.startswith("UD-Q4") or "ud-q4" not in target:
            raise RuntimeError(f"{candidate['label']}: Gemma target is not UD-Q4")


def run_candidate(
    candidate: dict[str, Any],
    *,
    bundle: Path,
    results_root: Path,
    llama_server: Path,
    hf_home: Path,
    port: int,
    max_cases: int,
    server_timeout: int,
    request_timeout: int,
) -> dict[str, Any]:
    label = str(candidate["label"])
    result_dir = results_root / label
    result_dir.mkdir(parents=True, exist_ok=True)
    log_path = result_dir / "server.log"
    raw_path = result_dir / f"raw_{label}.jsonl"
    expected = len(expected_case_ids(bundle, max_cases))
    if len(latest_rows(raw_path)) == expected and (result_dir / f"summary_{label}.json").exists():
        print(f"SKIP {label}: already has {expected} latest rows", flush=True)
        return validate_result(bundle, result_dir, candidate, max_cases)
    if port_is_open(port):
        raise RuntimeError(f"refusing to start: port {port} is already occupied")

    command = candidate_command(candidate, llama_server, port)
    environment = os.environ.copy()
    candidate_hf_home = Path(str(candidate.get("hf_home", hf_home)))
    if not candidate_hf_home.is_dir():
        raise RuntimeError(f"{label}: HF_HOME does not exist: {candidate_hf_home}")
    environment["HF_HOME"] = str(candidate_hf_home)
    prior_library_path = environment.get("LD_LIBRARY_PATH", "")
    environment["LD_LIBRARY_PATH"] = str(llama_server.parent) + (
        f":{prior_library_path}" if prior_library_path else ""
    )
    before_load = hardware_snapshot()
    with log_path.open("a", encoding="utf-8") as server_log:
        server_log.write(f"\n=== {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {label} ===\n")
        server_log.write(json.dumps({"command": command, "load_profile": LOAD_PROFILE}, sort_keys=True) + "\n")
        server_log.flush()
        process = subprocess.Popen(
            command,
            stdout=server_log,
            stderr=subprocess.STDOUT,
            text=True,
            env=environment,
        )
        try:
            cold_load_seconds = wait_for_server(
                process, f"http://127.0.0.1:{port}/health", server_timeout
            )
            props = json_request(f"http://127.0.0.1:{port}/props")
            slots = json_request(f"http://127.0.0.1:{port}/slots")
            model_path = str(props.get("model_path", ""))
            if str(candidate["expected_model"]).lower() not in model_path.lower():
                raise RuntimeError(
                    f"{label}: identity guard failed: loaded {model_path!r}, "
                    f"expected {candidate['expected_model']!r}"
                )
            speculative = bool(slots and slots[0].get("speculative"))
            if speculative is not bool(candidate["speculative"]):
                raise RuntimeError(
                    f"{label}: speculation guard failed: {speculative} != {candidate['speculative']}"
                )
            after_load = hardware_snapshot()
            runner = [
                sys.executable,
                str(Path(__file__).with_name("run_synthesis_ab.py")),
                "--endpoint", f"http://127.0.0.1:{port}",
                "--model", label,
                "--label", label,
                "--bundle", str(bundle),
                "--output-dir", str(result_dir),
                "--workers", "1",
                "--timeout", str(request_timeout),
                "--chat-template-kwargs-json",
                json.dumps(
                    candidate.get("chat_template_kwargs", {"enable_thinking": False}),
                    separators=(",", ":"),
                    sort_keys=True,
                ),
            ]
            if max_cases:
                runner += ["--max-cases", str(max_cases)]
            with (result_dir / "runner.log").open("a", encoding="utf-8") as runner_log:
                completed = subprocess.run(
                    runner,
                    stdout=runner_log,
                    stderr=subprocess.STDOUT,
                    text=True,
                    check=False,
                )
            after_run = hardware_snapshot()
            hardware = {
                "before_load": before_load,
                "after_load": after_load,
                "after_run": after_run,
                "cold_load_seconds": cold_load_seconds,
                "load_profile": LOAD_PROFILE,
                "candidate": candidate,
                "hf_home": str(candidate_hf_home),
                "model_path": model_path,
                "speculative": speculative,
                "llama_server": str(llama_server),
                "llama_server_sha256": sha256(llama_server),
            }
            (result_dir / "hardware_synthesis.json").write_text(
                json.dumps(hardware, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            if completed.returncode:
                raise RuntimeError(f"{label}: synthesis runner exited {completed.returncode}")
        finally:
            stop_process(process)
    result = validate_result(bundle, result_dir, candidate, max_cases)
    print(
        f"OK {label}: n={result['latest_rows']} "
        f"content_f1={result['overall']['content_f1']:.6f} "
        f"p50={result['overall']['latency_s']['p50']:.3f}s",
        flush=True,
    )
    return result


def main() -> int:
    validate_candidate_matrix()
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--results-root", type=Path, required=True)
    parser.add_argument(
        "--llama-server",
        type=Path,
        default=Path("/mnt/media/tierbench/bin/llama-b10356/llama-server"),
    )
    parser.add_argument("--hf-home", type=Path, default=Path("/mnt/media/tierbench/hf"))
    parser.add_argument("--port", type=int, default=8920)
    parser.add_argument("--max-cases", type=int, default=0)
    parser.add_argument("--labels", default="")
    parser.add_argument("--server-timeout", type=int, default=21600)
    parser.add_argument("--request-timeout", type=int, default=900)
    args = parser.parse_args()

    args.bundle = args.bundle.resolve()
    args.results_root = args.results_root.resolve()
    args.results_root.mkdir(parents=True, exist_ok=True)
    required = ("corpus.jsonl", "synthesis.jsonl", "manifest.json")
    missing = [name for name in required if not (args.bundle / name).is_file()]
    if missing:
        raise RuntimeError(f"bundle is missing required files: {missing}")
    if not args.llama_server.is_file():
        raise RuntimeError(f"llama-server not found: {args.llama_server}")

    by_label = {str(candidate["label"]): candidate for candidate in CANDIDATES}
    labels = [part.strip() for part in args.labels.split(",") if part.strip()]
    if not labels:
        labels = list(by_label)
    unknown = set(labels) - set(by_label)
    if unknown:
        raise RuntimeError(f"unknown labels: {sorted(unknown)}")

    lock_path = args.results_root / ".matrix.lock"
    with lock_path.open("w", encoding="utf-8") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError(f"another matrix process holds {lock_path}") from exc
        lock.write(str(os.getpid()) + "\n")
        lock.flush()

        state = {
            "status": "running",
            "started_unix": int(time.time()),
            "host": socket.gethostname(),
            "platform": platform.platform(),
            "bundle": {name: sha256(args.bundle / name) for name in required},
            "llama_server": str(args.llama_server),
            "llama_server_sha256": sha256(args.llama_server),
            "script_sha256": {
                "controller": sha256(Path(__file__)),
                "runner": sha256(Path(__file__).with_name("run_synthesis_ab.py")),
                "fixture_builder": sha256(Path(__file__).with_name("build_254_fixtures.py")),
            },
            "hardware_identity": hardware_identity(),
            "llama_device_listing": llama_device_listing(args.llama_server),
            "load_profile": LOAD_PROFILE,
            "selected_labels": labels,
            "candidate_matrix": [by_label[label] for label in labels],
            "max_cases": args.max_cases or 10000,
            "completed": [],
        }
        state_path = args.results_root / "RUN_STATE.json"
        state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        try:
            for label in labels:
                state["active"] = label
                state_path.write_text(
                    json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8"
                )
                run_candidate(
                    by_label[label],
                    bundle=args.bundle,
                    results_root=args.results_root,
                    llama_server=args.llama_server,
                    hf_home=args.hf_home,
                    port=args.port,
                    max_cases=args.max_cases,
                    server_timeout=args.server_timeout,
                    request_timeout=args.request_timeout,
                )
                state["completed"].append(label)
            state.update(
                status="complete",
                active=None,
                completed_unix=int(time.time()),
            )
            state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            return 0
        except Exception as exc:
            state.update(
                status="failed",
                error=f"{type(exc).__name__}: {exc}",
                failed_unix=int(time.time()),
            )
            state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            raise


if __name__ == "__main__":
    sys.exit(main())
