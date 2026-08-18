#!/bin/bash
# One arm of the two-task quant ladder. Runs INSIDE CT 140.
#
# Serve -> prove which card served it -> warmed throughput probe -> slow-arm
# gate -> extraction over 1,001 notes -> score. Synthesis is driven separately
# by run_synthesis.sh against the same served model.
#
# Exit-code discipline, and the reason for it: this harness has twice reported a
# suite green that had not run, both times because a filtered pipeline hid a
# failure ("cmd | head -5 && echo OK" prints OK on a compile error, since the
# pipeline's status is head's). Every step below branches on an explicit status
# and prints a distinct outcome token. Nothing prints OK on the back of a pipe.
set -u

ROOT=${ROOT:-/opt/campaign}
BUNDLE="$ROOT/bundle"                 # mirrors evidence/: src/ beside raw/harness/
OUT=${OUT:-$ROOT/results}
STATE="$ROOT/state"
BIN=${BIN:-/opt/llama.cpp/build-cuda/bin/llama-server}
PORT=${PORT:-8110}
CTX=${CTX:-8192}
GOLD=${GOLD:-$BUNDLE/gold_small.jsonl}
SLOW_FACTOR=${SLOW_FACTOR:-10}        # skip an arm projected slower than this x its model's Q4
WARMUP_TOK=128
MEASURE_TOK=400
READY_TRIES=${READY_TRIES:-240}       # 40 min: a cold offloaded load is disk-bound, not hung

LABEL=${LABEL:?set LABEL}
MODEL=${MODEL:?set MODEL}
TRAIN=${TRAIN:?set TRAIN}
WIDTH=${WIDTH:?set WIDTH}
TARGET=${TARGET:?set TARGET}
DRAFT=${DRAFT:?set DRAFT}

mkdir -p "$OUT" "$STATE"
ARM="$OUT/$LABEL"
mkdir -p "$ARM"
SRVLOG="$ARM/server.log"
META="$ARM/arm.json"

say() { echo "[$(date -u +%H:%M:%SZ)] $LABEL: $*"; }

# Idempotence: a finished arm is one with a score file AND a full prediction set.
EXPECT=$(wc -l < "$GOLD")

# A FAILED marker from a SUPERSEDED attempt must not outlive the attempt.
#
# gemma4-e2b.base.q4 failed once because the previous arm's server still held
# the card, then succeeded on the next pass -- and kept the stale marker. That
# matters beyond tidiness: run_campaign.sh skips synthesis for any arm whose
# FAILED text mentions a server, so a completed arm would have been left with no
# synthesis half, permanently, with nothing in the log to explain it.
if [ -s "$ARM/FAILED" ] && [ -s "$ARM/score.json" ] && [ -s "$ARM/pred.jsonl" ] &&
   [ "$(wc -l < "$ARM/pred.jsonl")" -ge "$EXPECT" ]; then
  rm -f "$ARM/FAILED"
  say "cleared a stale FAILED marker: this arm has a complete scored result"
fi
if [ -s "$ARM/score.json" ] && [ -s "$ARM/pred.jsonl" ] &&
   [ "$(wc -l < "$ARM/pred.jsonl")" -ge "$EXPECT" ]; then
  say "SKIP already complete"
  exit 0
fi
# A previously recorded non-result stays recorded unless removed by hand, so a
# resumed campaign does not re-attempt an arm this card has already refused.
if [ -s "$ARM/SKIPPED_TOO_SLOW" ]; then
  say "SKIP previously gated as too slow"
  exit 0
fi
if [ -s "$ARM/INVALID_DENSE_SPILL" ]; then
  say "SKIP previously invalidated by dense spill"
  exit 0
fi

# Wait for the card to be genuinely clear before starting, not merely for a
# signal to have been sent.
#
# A stale server from a previous run held 2,640 MiB while gemma4-e2b.base.q4
# loaded and ran. CUDA context teardown outlives process exit, so `pkill` then
# `sleep 3` is not enough: that arm recorded 4,727 MiB of VRAM for a model using
# 2,072 MiB, and its throughput was measured while sharing the card. Both
# numbers were wrong and the VRAM one was wrong by 2.6x.
pkill -f "$BIN" 2>/dev/null
for _ in $(seq 1 60); do
  if ! pgrep -f "$BIN" > /dev/null 2>&1; then
    # No process left; now wait for the driver to actually release the memory.
    FREE_MIB=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)
    [ "${FREE_MIB:-99999}" -lt 500 ] && break
  fi
  sleep 2
done
RESIDUAL=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)
if [ "${RESIDUAL:-99999}" -ge 500 ]; then
  say "FAIL card not clear before start: ${RESIDUAL}MiB still allocated"
  printf 'card not clear before start: %sMiB still allocated\n' "$RESIDUAL" > "$ARM/FAILED"
  nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader >> "$ARM/FAILED" 2>&1
  exit 1
fi

# ---------------------------------------------------------------- serve
#
# Offload strategy differs by architecture, and getting this wrong is the
# difference between an arm that runs fine and an arm that crawls.
#
# MoE: if the weights exceed the card, keep attention and the dense path on the
# GPU and push the expert FFNs to system RAM with -cmoe. A token routes to a
# couple of experts out of many, so the CPU-side work per token is a small
# fraction of the model. This is cheap and expected; it is NOT a reason to gate
# an arm, and MoE spill is not treated as a hazard anywhere below.
#
# Dense: there is no such escape hatch. -ngl short of every layer puts WHOLE
# layers on the CPU, and every token traverses every layer, so a dense spill is
# a genuine cliff. Dense arms therefore demand full residency, and an arm that
# cannot get it is recorded as DENSE_SPILL rather than quietly run slow.
#
# The card reports 15880 MiB usable / 15611 free, not the 16303 nvidia-smi
# advertises, so the budget below is set against the smaller number.
export HF_HOME=${HF_HOME:-/opt/hf}
VRAM_BUDGET_GIB=${VRAM_BUDGET_GIB:-13.5}   # leaves room for KV cache and draft

case "$MODEL" in
  *-a[0-9]b|*-a[0-9][0-9]b) ARCH=moe ;;
  *) ARCH=dense ;;
esac

# -np 1 is explicit and load-bearing. Left to its default this build starts four
# slots with a unified KV cache, which is a shared-state difference between arms
# and exactly the shape this harness already has two investigations into
# (investigate_np32_nondeterminism.sh, check_parallel_determinism.py). The
# synthesis load profile pins one slot for the same reason; the extraction side
# now matches it.
# --cache-ram 1024 is NOT a tuning knob here, it is a correctness requirement.
#
# Left unset, the first live arm's prompt cache grew until the server held
# 9.3 GB RSS for a 1.6 GiB model, logged hundreds of "making room for prompt
# cache entry" evictions, and then deadlocked in futex_do_wait during shutdown
# while the client sat on the socket. The arm froze at 247/1001 and the
# campaign could not advance.
#
# Independently of the crash, this value is RESULTS-AFFECTING in this series:
# the 10,000-note ladder had to be quarantined and re-taken because two model
# families had been run at different --cache-ram settings, and 1024 is the
# value the re-take standardised on. The synthesis load profile pins the same
# 1024. An arm run at an unbounded default would not be comparable to anything
# else measured here, even if it completed.
#
# KV cache type is per-arm and defaults to f16, which is llama.cpp's default and
# what every weight-ladder rung uses, so the ladder step stays one-variable. The
# KV sweep arms vary it deliberately on FIXED bf16 weights, which makes cache
# precision its own axis rather than a confound inside the width ladder.
CTK=${CTK:-f16}
CTV=${CTV:-f16}
SRV_ARGS=(-hf "$TARGET" --host 127.0.0.1 --port "$PORT" -c "$CTX"
          -np 1 --cache-ram 1024 --no-webui --no-mmproj -ngl 99
          -ctk "$CTK" -ctv "$CTV")

OFFLOAD_MODE=full-gpu
if [ "$ARCH" = "moe" ]; then
  FITS=$(python3 -c "print(1 if float('${EST_GIB:-0}') <= float('$VRAM_BUDGET_GIB') else 0)")
  if [ "$FITS" != "1" ]; then
    SRV_ARGS+=(-cmoe)
    OFFLOAD_MODE=moe-experts-on-cpu
  fi
fi

if [ "$DRAFT" != "-" ]; then
  # The draft model keeps its own KV cache and defaults to f16 independently.
  # Left alone, a "q4_0 KV" arm would quietly be running a q4_0 target cache
  # against an f16 draft cache, which is not the configuration being claimed.
  # --draft-max / --draft-min were REMOVED in this llama.cpp build; it exits
  # immediately with "the argument has been removed. use --spec-draft-n-max".
  # The replacements are --spec-draft-n-max / --spec-draft-n-min.
  #
  # This cost twelve arms. Every LFM2.5 arm ran clean because that family ships
  # no draft model, so the first arm to pass -hfd was the thirteenth of the
  # campaign, and the flag error was never exercised until then. Draft flags are
  # only reachable on speculating arms, so "the LFM ladder works" said nothing
  # about them.
  SRV_ARGS+=(-hfd "$DRAFT" --spec-draft-n-max 3 --spec-draft-n-min 1
             -ctkd "$CTK" -ctvd "$CTV")
fi
say "ARCH=$ARCH OFFLOAD=$OFFLOAD_MODE est=${EST_GIB:-?}GiB budget=${VRAM_BUDGET_GIB}GiB ctk=$CTK ctv=$CTV"

# Preflight every flag against the binary's own help BEFORE spending a model
# load on it.
#
# llama.cpp keeps removed arguments in --help with the text "the argument has
# been removed", so the set of dead flags is machine-readable. --draft-max and
# --draft-min were removed in this build and the server exits instantly when
# given them, which cost twelve arms before anyone looked at a FAILED file.
#
# This costs one --help invocation per arm and turns a class of silent
# campaign-wide failure into a named error on the first arm that would hit it.
HELP=$("$BIN" --help 2>&1)
DEAD=""
for arg in "${SRV_ARGS[@]}"; do
  case "$arg" in
    -*) ;;
    *) continue ;;
  esac
  # A removed flag's help line NAMES ITS REPLACEMENT on the same line:
  #
  #   --draft, --draft-max N   the argument has been removed. use --spec-draft-n-max or
  #
  # so matching the whole line flags the replacement as removed too, which is
  # exactly what the first version of this check did -- it rejected
  # --spec-draft-n-max, the correct flag. Cut the description away and match
  # only the flag column that precedes it.
  if printf '%s' "$HELP" | grep -F "the argument has been removed" \
       | sed 's/the argument has been removed.*//' \
       | grep -qE "(^|[ ,])${arg}([ ,]|$)"; then
    DEAD="$DEAD $arg"
  fi
done
if [ -n "$DEAD" ]; then
  say "FAIL removed server flags:$DEAD"
  printf 'server flags removed in this llama.cpp build:%s\n' "$DEAD" > "$ARM/FAILED"
  printf 'run "%s --help" and use the replacement named there.\n' "$BIN" >> "$ARM/FAILED"
  exit 1
fi

say "SERVE $TARGET"
"$BIN" "${SRV_ARGS[@]}" > "$SRVLOG" 2>&1 &
SRV=$!

ready=0
for _ in $(seq 1 "$READY_TRIES"); do
  if curl -sf --max-time 5 "http://127.0.0.1:$PORT/health" > /dev/null 2>&1; then
    ready=1; break
  fi
  if ! kill -0 "$SRV" 2>/dev/null; then
    say "FAIL server exited during load"
    printf '%s\n' "server exited during load" > "$ARM/FAILED"
    tail -40 "$SRVLOG" >> "$ARM/FAILED"
    exit 1
  fi
  sleep 10
done
if [ "$ready" != 1 ]; then
  say "FAIL server never healthy within $((READY_TRIES * 10))s"
  printf '%s\n' "server never became healthy" > "$ARM/FAILED"
  kill "$SRV" 2>/dev/null
  exit 1
fi
say "READY"

# Kill THIS arm's server by pid, escalating if it will not go. The previous
# version ended with `pkill -f "$BIN"`, which matches any llama-server on the
# box regardless of which arm owns it -- a cross-kill waiting to happen the
# moment two things run at once.
cleanup() {
  kill "$SRV" 2>/dev/null
  for _ in $(seq 1 10); do
    kill -0 "$SRV" 2>/dev/null || return 0
    sleep 1
  done
  # A server that ignores SIGTERM for ten seconds is the deadlock case: it can
  # hold VRAM indefinitely and block the next arm, so do not wait politely.
  kill -9 "$SRV" 2>/dev/null
  sleep 2
}
trap cleanup EXIT

# ------------------------------------------------- provenance, not assumption
# "-ngl 99 was requested" is exactly what the series recorded when it was in
# fact serving from an 8GB iGPU. Record what the driver says served it, and how
# much of the model actually landed on the card.
nvidia-smi --query-gpu=index,name,pci.bus_id,memory.total,memory.used \
           --format=csv,noheader > "$ARM/device.txt" 2>&1
{
  echo "--- compute apps ---"
  nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader
  echo "--- offload lines ---"
  grep -iE "offload|layers|tensor|buffer size|CUDA[0-9]" "$SRVLOG" | tail -40
} >> "$ARM/device.txt" 2>&1

# Residency is measured, not parsed. This build emits no "offloaded N/M layers"
# line at any verbosity, so the original grep matched nothing and reported
# "unrecorded" -- which silently disabled the dense-spill check entirely, since
# that check only ran when the string was present. A grep that matches nothing
# looking like a clean result is the exact failure this harness keeps repeating.
#
# The replacement is a physical invariant rather than a log format: weights
# resident on the card must occupy at least their own file size in VRAM. If the
# server is using less VRAM than the model file is large, some of that model is
# demonstrably not on the card. This cannot silently pass by failing to match.
# Measured BEFORE the residency check that consumes them. Resident memory of
# the server process is also the number that decides whether the next arm up
# the ladder can run at all.
RSS_KB=$(ps -o rss= -p "$SRV" 2>/dev/null | tr -d ' ')
[ -n "$RSS_KB" ] || RSS_KB=0
VRAM_MIB=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)
[ -n "$VRAM_MIB" ] || VRAM_MIB=0

# Exactly one process may hold the card while this arm is measured. Anything
# else means the VRAM figure is a sum over strangers and the throughput was
# measured under contention -- which is how one arm reported 4,727 MiB for a
# 2,072 MiB model and a throughput number that cannot be compared to its peers.
APPS=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader | grep -c .)
if [ "${APPS:-0}" -ne 1 ]; then
  say "FAIL $APPS processes hold the GPU; measurement would be contaminated"
  printf 'expected exactly 1 GPU compute app during the arm, found %s\n' "$APPS" > "$ARM/FAILED"
  nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader >> "$ARM/FAILED" 2>&1
  exit 1
fi

MODEL_PATH=$(curl -s --max-time 10 "http://127.0.0.1:$PORT/props" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin).get("model_path",""))' 2>/dev/null)
MODEL_FTYPE=$(curl -s --max-time 10 "http://127.0.0.1:$PORT/props" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin).get("model_ftype",""))' 2>/dev/null)

FILE_MIB=0
if [ -n "$MODEL_PATH" ] && [ -f "$MODEL_PATH" ]; then
  FILE_MIB=$(( $(stat -Lc %s "$MODEL_PATH") / 1048576 ))
fi
{
  echo "--- served model ---"
  echo "model_path=$MODEL_PATH"
  echo "model_ftype=$MODEL_FTYPE"
  echo "model_file_mib=$FILE_MIB"
  echo "gpu_mem_used_mib=$VRAM_MIB"
} >> "$ARM/device.txt"

if [ "$FILE_MIB" -gt 0 ]; then
  OFFLOAD="vram ${VRAM_MIB}MiB vs weights ${FILE_MIB}MiB"
else
  OFFLOAD="unmeasured (model_path not resolvable)"
fi

# A DENSE model that did not get every layer INVALIDATES the arm, and the arm
# stops here. There is no expert sparsity to absorb it: every token traverses
# every layer, so a partially resident dense model is not the same experiment
# as its fully resident siblings, and its number is not a bit-width result. It
# would be a measurement of this card's capacity wearing a quantization label.
#
# MoE arms are exempt by design. Experts on CPU is the intended way to serve
# them and does not change what is being measured.
DENSE_SPILL=0
if [ "$ARCH" = "dense" ]; then
  if [ "$FILE_MIB" -eq 0 ]; then
    # Refuse to guess. An unmeasurable dense arm is not silently accepted,
    # because accepting it is how a spilled arm would reach the article.
    say "FAIL cannot measure residency: model_path unresolved"
    printf 'residency unmeasurable; model_path=%s\n' "$MODEL_PATH" > "$ARM/FAILED"
    exit 1
  fi
  # VRAM below file size is NOT sufficient evidence of a spill.
  #
  # The gemma-4 E-series keeps its per-layer embeddings on the CPU by design --
  # they are lookup tables, not compute -- so E2B Q4 loads ~2.0 GiB to the card
  # from a 3.0 GiB file with 2.5 GiB resident in host RAM, entirely correctly.
  # The published article's own size chart lists E2B at 2.01 GiB, which is that
  # resident figure rather than the file. The first version of this check called
  # that a spill and invalidated a 2 GiB model on a 16 GiB card.
  #
  # A CAPACITY spill can only occur when the card is full. If the server is
  # using a small fraction of available VRAM, nothing was evicted for want of
  # room, whatever the file size says. So both conditions must hold: less VRAM
  # than weights, AND the card at its ceiling.
  CARD_TOTAL_MIB=${CARD_TOTAL_MIB:-15880}
  NEAR_CEILING=$(python3 -c "print(1 if float('$VRAM_MIB') >= 0.90 * float('$CARD_TOTAL_MIB') else 0)")
  if [ "$VRAM_MIB" -lt "$FILE_MIB" ] && [ "$NEAR_CEILING" = "1" ]; then
    DENSE_SPILL=1
    say "INVALID_DENSE_SPILL vram ${VRAM_MIB}MiB < weights ${FILE_MIB}MiB at card ceiling ${CARD_TOTAL_MIB}MiB"
    python3 - "$ARM/INVALID_DENSE_SPILL" "$LABEL" "$MODEL" "$WIDTH" "$TARGET" \
             "$DRAFT" "$VRAM_MIB" "$FILE_MIB" "$RSS_KB" "$MODEL_PATH" <<'PY'
import json, sys
(p, label, model, width, target, draft, vram, filemib, rss, path) = sys.argv[1:11]
json.dump({
    "label": label, "model": model, "width": width, "target": target,
    "draft": draft if draft != "-" else None,
    "architecture": "dense",
    "outcome": "INVALID_DENSE_SPILL",
    "gpu_mem_used_mib": int(vram),
    "model_file_mib": int(filemib),
    "server_rss_mib": int(rss) // 1024,
    "model_path": path,
    "evidence": "GPU memory in use is smaller than the model file AND the card "
                "is at its ceiling, so weights were evicted for want of room. "
                "The ceiling condition matters: some architectures keep tensors "
                "on the CPU by design (the gemma-4 E-series holds per-layer "
                "embeddings there), and VRAM below file size alone does not "
                "distinguish that from a capacity spill.",
    "note": "Not run. A dense model missing layers from the card is not the "
            "same experiment as its fully resident siblings, so no score is "
            "produced and none should be inferred. This is a capacity result "
            "about a 15880 MiB card, not a result about this bit width. The "
            "ladder is reported as reaching only as far as its resident rungs.",
}, open(p, "w"), indent=2)
PY
    exit 0
  fi
fi

say "DEVICE $OFFLOAD rss=$((RSS_KB / 1024))MiB vram=${VRAM_MIB}MiB ftype=$MODEL_FTYPE"

# --------------------------------------------------------- warmed throughput
# Warmed and long enough to average. The first moe-tune probe was discarded for
# timing a cold 100-token generation, which measured page-fault-in and produced
# results that got faster with MORE offload.
probe() {
  curl -s --max-time 3600 "http://127.0.0.1:$PORT/completion" \
    -H 'Content-Type: application/json' \
    -d "{\"prompt\":\"Write a detailed technical description of how a B-tree index works.\",\"n_predict\":$1,\"temperature\":0,\"cache_prompt\":false}"
}

probe "$WARMUP_TOK" > /dev/null 2>&1
PROBE_JSON=$(probe "$MEASURE_TOK" 2>/dev/null)
TPS=$(printf '%s' "$PROBE_JSON" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
    print(round(float(d["timings"]["predicted_per_second"]), 3))
except Exception:
    print("")
' 2>/dev/null)

if [ -z "$TPS" ]; then
  say "FAIL warmed probe produced no timings"
  printf '%s\n' "warmed probe returned no timings" > "$ARM/FAILED"
  exit 1
fi
say "PROBE ${TPS} tok/s"

# ------------------------------------------------------------ slow-arm gate
# The Q4 arm of each model is the baseline. Anything projected past SLOW_FACTOR
# times its wall-clock is recorded and skipped rather than allowed to block the
# queue -- the operator's rule, and the skipped set is itself a deliverable.
BASEFILE="$STATE/$MODEL.q4.tps"
GATE="not applied"
if [ "$WIDTH" = "q4" ] && [ "$TRAIN" = "base" ]; then
  printf '%s\n' "$TPS" > "$BASEFILE"
  GATE="baseline recorded"
elif [ -s "$BASEFILE" ]; then
  BASE=$(cat "$BASEFILE")
  RATIO=$(python3 -c "print(round(float('$BASE') / max(float('$TPS'), 1e-9), 2))")
  TOO_SLOW=$(python3 -c "print(1 if float('$BASE') / max(float('$TPS'), 1e-9) > float('$SLOW_FACTOR') else 0)")
  GATE="ratio ${RATIO}x vs Q4 baseline ${BASE} tok/s"
  if [ "$TOO_SLOW" = "1" ]; then
    say "SKIPPED_TOO_SLOW $GATE"
    python3 - "$ARM/SKIPPED_TOO_SLOW" "$LABEL" "$MODEL" "$WIDTH" "$TPS" "$BASE" "$RATIO" "$OFFLOAD" "$RSS_KB" "$ARCH" "$OFFLOAD_MODE" "$DENSE_SPILL" <<'PY'
import json, sys
(p, label, model, width, tps, base, ratio, offload, rss,
 arch, mode, dense_spill) = sys.argv[1:13]
json.dump({
    "label": label, "model": model, "width": width,
    "outcome": "SKIPPED_TOO_SLOW",
    "architecture": arch,
    "offload_mode": mode,
    "dense_layer_spill": dense_spill == "1",
    "measured_tok_per_s": float(tps),
    "q4_baseline_tok_per_s": float(base),
    "slowdown_vs_q4": float(ratio),
    "offload": offload,
    "server_rss_mib": int(rss) // 1024,
    "note": "Gated before the extraction run. No score exists for this arm and "
            "its ladder is incomplete. This is a recorded outcome, not a failure. "
            "If dense_layer_spill is true the cause is layer offload on a dense "
            "model, which is a hardware-capacity result about this card, not a "
            "statement about the quantization.",
}, open(p, "w"), indent=2)
PY
    exit 0
  fi
fi
say "GATE $GATE"

# ---------------------------------------------------------------- extraction
# Driven from raw/harness/ so that "harness/run_llamacpp.py" resolves and
# prompt.py finds the pinned ontology at REPO/src (REPO = parents[3]).
say "EXTRACT start ($EXPECT notes)"
EXTRACT_START=$(date -u +%s)
python3 "$BUNDLE/raw/harness/harness/run_llamacpp.py" \
  --model "$LABEL" --gold "$GOLD" --out "$ARM/pred.jsonl" \
  --thinking --max-tokens "$CTX" --concurrency 1 \
  --base-url "http://127.0.0.1:$PORT" >> "$ARM/extract.log" 2>&1 &
EXTRACT_PID=$!

# Watchdog. The client's own timeout is an hour, and it spends that hour
# waiting politely on a socket whose server has died -- which is how one dead
# arm froze the whole 33-arm queue with nothing in any log to say so. Two
# independent liveness signals, because the freeze presented as "slow":
#
#   1. the server answers /health
#   2. the prediction file is still growing
#
# Either one failing for its grace period kills the arm and lets the queue move
# on. A stalled arm must cost minutes, not an hour, and must never cost the
# whole campaign.
STALL_LIMIT=${STALL_LIMIT:-1200}      # 20 min with no new row
LAST_ROWS=0
LAST_PROGRESS=$(date -u +%s)
DIED=""

while kill -0 "$EXTRACT_PID" 2>/dev/null; do
  sleep 30

  if ! curl -sf --max-time 10 "http://127.0.0.1:$PORT/health" > /dev/null 2>&1; then
    sleep 20   # one retry: do not kill an arm over a single slow health check
    if ! curl -sf --max-time 10 "http://127.0.0.1:$PORT/health" > /dev/null 2>&1; then
      DIED="server stopped answering /health"
      break
    fi
  fi

  NOW_ROWS=$(wc -l < "$ARM/pred.jsonl" 2>/dev/null || echo 0)
  if [ "$NOW_ROWS" -gt "$LAST_ROWS" ]; then
    LAST_ROWS=$NOW_ROWS
    LAST_PROGRESS=$(date -u +%s)
  elif [ $(( $(date -u +%s) - LAST_PROGRESS )) -ge "$STALL_LIMIT" ]; then
    DIED="no new prediction row in ${STALL_LIMIT}s (stuck at $NOW_ROWS/$EXPECT)"
    break
  fi
done

if [ -n "$DIED" ]; then
  kill "$EXTRACT_PID" 2>/dev/null
  sleep 3
  kill -9 "$EXTRACT_PID" 2>/dev/null
  EXTRACT_SECS=$(( $(date -u +%s) - EXTRACT_START ))
  GOT_ROWS=$(wc -l < "$ARM/pred.jsonl" 2>/dev/null || echo 0)
  say "SERVER_DIED $DIED after ${EXTRACT_SECS}s at $GOT_ROWS/$EXPECT rows"
  printf 'server died during extraction: %s\nrows=%s/%s seconds=%s\n' \
    "$DIED" "$GOT_ROWS" "$EXPECT" "$EXTRACT_SECS" > "$ARM/FAILED"
  tail -30 "$SRVLOG" >> "$ARM/FAILED"
  exit 1
fi

wait "$EXTRACT_PID"
EXTRACT_RC=$?
EXTRACT_SECS=$(( $(date -u +%s) - EXTRACT_START ))

if [ "$EXTRACT_RC" -ne 0 ]; then
  say "EXTRACTFAIL rc=$EXTRACT_RC after ${EXTRACT_SECS}s"
  printf 'extraction exited %s\n' "$EXTRACT_RC" > "$ARM/FAILED"
  tail -40 "$ARM/extract.log" >> "$ARM/FAILED"
  exit 1
fi

GOT=$(wc -l < "$ARM/pred.jsonl" 2>/dev/null || echo 0)
if [ "$GOT" -lt "$EXPECT" ]; then
  say "EXTRACTSHORT $GOT/$EXPECT rows after ${EXTRACT_SECS}s"
  printf 'extraction produced %s of %s rows\n' "$GOT" "$EXPECT" > "$ARM/FAILED"
  exit 1
fi
say "EXTRACT done ${EXTRACT_SECS}s"

# --------------------------------------------------------------------- score
# Scored strict and relation-agnostic, as every other arm in the series is.
(cd "$BUNDLE/raw/harness" && python3 harness/score.py \
    --gold "$GOLD" --pred "$ARM/pred.jsonl" --json-out "$ARM/score.json") \
  >> "$ARM/score.log" 2>&1
SCORE_RC=$?
if [ "$SCORE_RC" -ne 0 ] || [ ! -s "$ARM/score.json" ]; then
  say "SCOREFAIL rc=$SCORE_RC"
  printf 'score exited %s\n' "$SCORE_RC" > "$ARM/FAILED"
  tail -40 "$ARM/score.log" >> "$ARM/FAILED"
  exit 1
fi

(cd "$BUNDLE/raw/harness" && python3 harness/score.py \
    --gold "$GOLD" --pred "$ARM/pred.jsonl" --no-alias \
    --json-out "$ARM/score.noalias.json") >> "$ARM/score.log" 2>&1
# The relation-agnostic score is supporting detail; its failure does not void
# the arm, but it is never silently absent.
if [ ! -s "$ARM/score.noalias.json" ]; then
  say "WARN relation-agnostic score missing"
fi

# ------------------------------------------------- throughput, from the run
# Speed is a reported result of this article, not a diagnostic, so it is
# measured over the whole arm rather than from the single warmed probe. The
# extraction run yields one generation timing per note -- ~1000 samples -- and
# they are tight enough (under 2% spread on the first arm) that the median is a
# far stronger figure than one 400-token probe.
#
# The exclusion matters: llama.cpp logs "prompt eval time" for PREFILL and
# "eval time" for GENERATION, and the former runs ~45x faster. A grep for
# "eval time" catches both and silently reports a mean of ~8000 tok/s for a
# model generating at 370. Prefill is captured separately, not discarded.
if ! python3 "$ROOT/throughput.py" "$SRVLOG" "$ARM/throughput.json"; then
  say "WARN throughput summary failed"
fi

if [ -s "$ARM/throughput.json" ]; then
  GEN_MED=$(python3 -c "
import json
t = json.load(open('$ARM/throughput.json')).get('generation_tok_per_s') or {}
print(t.get('median', 'na'), 'over', t.get('n', 0), 'samples')" 2>/dev/null)
  say "THROUGHPUT generation median $GEN_MED"
else
  say "WARN throughput summary not produced"
fi

# ------------------------------------------------------------------- record
python3 - "$META" "$LABEL" "$MODEL" "$TRAIN" "$WIDTH" "$TARGET" "$DRAFT" \
         "$TPS" "$OFFLOAD" "$RSS_KB" "$VRAM_MIB" "$EXTRACT_SECS" \
         "$ARM/score.json" "$ARM/pred.jsonl" "$EXPECT" "$GATE" \
         "$ARCH" "$OFFLOAD_MODE" "$DENSE_SPILL" "$ARM/throughput.json" "$CTK" "$CTV" <<'PY'
import json, os, sys
(p, label, model, train, width, target, draft, tps, offload, rss, vram,
 secs, scorep, predp, expect, gate, arch, mode, dense_spill, thrup,
 ctk, ctv) = sys.argv[1:23]
score = json.load(open(scorep))
rows = sum(1 for _ in open(predp))
throughput = None
if os.path.exists(thrup):
    throughput = json.load(open(thrup))
json.dump({
    "label": label, "model": model, "training": train, "width": width,
    "target": target, "draft": draft if draft != "-" else None,
    "speculation": draft != "-",
    "outcome": "COMPLETE",
    "architecture": arch,
    "offload_mode": mode,
    # True only for a DENSE model that did not get every layer on the card.
    # MoE arms running experts on CPU are not spills in this sense and are
    # never flagged here; that is the intended way to serve them.
    "dense_layer_spill": dense_spill == "1",
    # Single 400-token probe, used only by the slow-arm gate. For a reported
    # speed figure use throughput.generation_tok_per_s, which is the median of
    # roughly a thousand real generations from this arm.
    "warmed_tok_per_s": float(tps),
    "throughput": throughput,
    "cache_type_k": ctk,
    "cache_type_v": ctv,
    "gate": gate,
    "offload": offload,
    "server_rss_mib": int(rss) // 1024,
    "gpu_mem_used_mib": int(vram),
    "extraction_seconds": int(secs),
    "rows": rows, "expected_rows": int(expect),
    "score": score,
}, open(p, "w"), indent=2)
PY

# score.py nests its verdicts under strict / lenient / relation_agnostic; there
# is no top-level "f1", so the original lookup printed "f1=None" on a perfectly
# good arm. Cosmetic only -- arm.json embeds the whole score object -- but a
# summary line that says None on success is the same class of mistake as a
# green suite that never ran, and it is what a human scans first across 33 arms.
F1=$(python3 -c "
import json
s = json.load(open('$ARM/score.json'))
print('strict=%s lenient=%s relagnostic=%s' % (
    s.get('strict', {}).get('f1'),
    s.get('lenient', {}).get('f1'),
    s.get('relation_agnostic', {}).get('f1')))" 2>/dev/null)
say "COMPLETE $F1 ${EXTRACT_SECS}s ${TPS}tok/s"
exit 0
