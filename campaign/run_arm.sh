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
if [ -s "$ARM/score.json" ] && [ -s "$ARM/pred.jsonl" ] &&
   [ "$(wc -l < "$ARM/pred.jsonl")" -ge "$EXPECT" ]; then
  say "SKIP already complete"
  exit 0
fi
# A previously skipped arm stays skipped unless its record is removed by hand.
if [ -s "$ARM/SKIPPED_TOO_SLOW" ]; then
  say "SKIP previously gated as too slow"
  exit 0
fi

pkill -f "$BIN" 2>/dev/null
sleep 3

# ---------------------------------------------------------------- serve
export HF_HOME=${HF_HOME:-/opt/hf}
SRV_ARGS=(-hf "$TARGET" --host 127.0.0.1 --port "$PORT" -c "$CTX"
          --no-webui --no-mmproj -ngl 99)
if [ "$DRAFT" != "-" ]; then
  SRV_ARGS+=(-hfd "$DRAFT" --draft-max 3 --draft-min 1)
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

cleanup() { kill "$SRV" 2>/dev/null; sleep 2; pkill -f "$BIN" 2>/dev/null; }
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

# Layers on GPU vs total, straight out of the loader.
OFFLOAD=$(grep -oiE "offloaded [0-9]+/[0-9]+ layers" "$SRVLOG" | tail -1)
[ -n "$OFFLOAD" ] || OFFLOAD="unrecorded"

# Resident memory of the server process: the number that decides whether the
# next arm up the ladder can run at all.
RSS_KB=$(ps -o rss= -p "$SRV" 2>/dev/null | tr -d ' ')
[ -n "$RSS_KB" ] || RSS_KB=0
VRAM_MIB=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)

say "DEVICE offload=$OFFLOAD rss=$((RSS_KB / 1024))MiB vram=${VRAM_MIB}MiB"

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
    python3 - "$ARM/SKIPPED_TOO_SLOW" "$LABEL" "$MODEL" "$WIDTH" "$TPS" "$BASE" "$RATIO" "$OFFLOAD" "$RSS_KB" <<'PY'
import json, sys
p, label, model, width, tps, base, ratio, offload, rss = sys.argv[1:10]
json.dump({
    "label": label, "model": model, "width": width,
    "outcome": "SKIPPED_TOO_SLOW",
    "measured_tok_per_s": float(tps),
    "q4_baseline_tok_per_s": float(base),
    "slowdown_vs_q4": float(ratio),
    "offload": offload,
    "server_rss_mib": int(rss) // 1024,
    "note": "Gated before the extraction run. No score exists for this arm and "
            "its ladder is incomplete. This is a recorded outcome, not a failure.",
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
  --base-url "http://127.0.0.1:$PORT" >> "$ARM/extract.log" 2>&1
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

# ------------------------------------------------------------------- record
python3 - "$META" "$LABEL" "$MODEL" "$TRAIN" "$WIDTH" "$TARGET" "$DRAFT" \
         "$TPS" "$OFFLOAD" "$RSS_KB" "$VRAM_MIB" "$EXTRACT_SECS" \
         "$ARM/score.json" "$ARM/pred.jsonl" "$EXPECT" "$GATE" <<'PY'
import json, sys
(p, label, model, train, width, target, draft, tps, offload, rss, vram,
 secs, scorep, predp, expect, gate) = sys.argv[1:17]
score = json.load(open(scorep))
rows = sum(1 for _ in open(predp))
json.dump({
    "label": label, "model": model, "training": train, "width": width,
    "target": target, "draft": draft if draft != "-" else None,
    "speculation": draft != "-",
    "outcome": "COMPLETE",
    "warmed_tok_per_s": float(tps),
    "gate": gate,
    "offload": offload,
    "server_rss_mib": int(rss) // 1024,
    "gpu_mem_used_mib": int(vram),
    "extraction_seconds": int(secs),
    "rows": rows, "expected_rows": int(expect),
    "score": score,
}, open(p, "w"), indent=2)
PY

F1=$(python3 -c "import json;print(json.load(open('$ARM/score.json')).get('f1'))" 2>/dev/null)
say "COMPLETE f1=$F1 ${EXTRACT_SECS}s ${TPS}tok/s"
exit 0
