#!/bin/bash
# Run Muse Glimmer 30B K-Quant-17GB on the fact-extraction corpus after the
# Gemma 4 31B UD-QAT MTP off/on pair has been fully banked on this same XTX.
set -u
cd "$(dirname "$0")/../.." || exit 1

OUT=results/muse-glimmer-30b-xtx-20260810
GEMMA_OUT=results/gemma4-mtp-pairs-20260810
GOLD=corpus/data/corpora/v5/gold_small.jsonl
EXPECT=$(grep -c . "$GOLD")
HOST=admin@192.168.1.254
EP=127.0.0.1
PORT=8119
BIN=/mnt/media/tierbench/bin/llama-b10356/llama-server
HF_HOME_REMOTE=/mnt/media/tierbench/hf
TARGET_REPO=meta-models/Muse-Glimmer-30B-GGUF
TARGET_FILE=muse-glimmer-30B-kquant-17gb.gguf
DRAFT_REPO=meta-models/Muse-Glimmer-30B-GGUF:dflash-kquant
WANT=muse-glimmer-30B-kquant-17gb.gguf
mkdir -p "$OUT"

say() { echo "[$(date -u +%H:%M:%SZ)] $*" | tee -a "$OUT/queue.log"; }

artifact_complete() {
  local pred=$1 score=$2
  [ -f "$pred" ] && [ "$(grep -c . "$pred")" -eq "$EXPECT" ] && [ -f "$score" ]
}

xtx_gemma_queue_alive() {
  local pid
  for pid in $(pgrep -f 'bash harness/harness/queue_gemma4_mtp_pairs[.]sh' 2>/dev/null); do
    tr '\0' '\n' < "/proc/$pid/environ" 2>/dev/null | grep -qx 'CARD=xtx' && return 0
  done
  return 1
}

GEMMA_OFF="$GEMMA_OUT/gemma-4-31B-it.qat-UD-Q4_K_XL.xtx.mtp-off.pred.jsonl"
GEMMA_OFF_SCORE="$GEMMA_OUT/gemma-4-31B-it.qat-UD-Q4_K_XL.xtx.mtp-off.score.json"
GEMMA_ON="$GEMMA_OUT/gemma-4-31B-it.qat-UD-Q4_K_XL.xtx.mtp-on.pred.jsonl"
GEMMA_ON_SCORE="$GEMMA_OUT/gemma-4-31B-it.qat-UD-Q4_K_XL.xtx.mtp-on.score.json"

say "WAIT: Muse Glimmer is queued behind the complete Gemma 4 31B off/on pair"
while ! artifact_complete "$GEMMA_OFF" "$GEMMA_OFF_SCORE" \
   || ! artifact_complete "$GEMMA_ON" "$GEMMA_ON_SCORE"; do
  if ! xtx_gemma_queue_alive; then
    say "BLOCKED: Gemma 4 31B queue exited before both 1001-row scored artifacts were banked"
    exit 1
  fi
  sleep 30
done
say "PREREQUISITE OK: Gemma 4 31B off/on are both banked and scored"

# The Gemma arm owns port 8118 and cleans up its exact server/tunnel on exit.
# Do not claim Vulkan1 until both sides of that ownership boundary are clear.
for _ in $(seq 1 40); do
  REMOTE_8118=$(ssh -n -o ConnectTimeout=15 "$HOST" \
    "ss -ltnpH 'sport = :8118'" 2>/dev/null)
  LOCAL_8118=$(ss -ltnpH 'sport = :8118' 2>/dev/null)
  [ -z "$REMOTE_8118" ] && [ -z "$LOCAL_8118" ] && break
  sleep 5
done
[ -z "${REMOTE_8118:-}" ] && [ -z "${LOCAL_8118:-}" ] \
  || { say "BLOCKED: Gemma 4 still owns XTX port 8118"; exit 1; }

remote_pid() {
  ssh -n -o ConnectTimeout=15 "$HOST" \
    "ss -ltnpH 'sport = :$PORT'" 2>/dev/null \
    | grep -oE 'pid=[0-9]+' | head -1 | cut -d= -f2
}

server_process_pid() {
  ssh -n -o ConnectTimeout=15 "$HOST" \
    "pgrep -f '^$BIN .*--port $PORT( |$)'" 2>/dev/null | head -1
}

stop_server() {
  local pid
  pid=$(remote_pid)
  [ -n "$pid" ] || pid=$(server_process_pid)
  [ -n "$pid" ] || return 0
  ssh -n -o ConnectTimeout=15 "$HOST" "kill -TERM $pid" >/dev/null 2>&1 || true
  sleep 4
}

TUNNEL_PID=""
cleanup() {
  [ -n "$TUNNEL_PID" ] && kill "$TUNNEL_PID" 2>/dev/null || true
  TUNNEL_PID=""
  stop_server
}
trap cleanup EXIT
trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

run_arm() {
  local speculation=$1 label pred score server_log draft_args want_spec
  if [ "$speculation" = on ]; then
    draft_args="-hfd $DRAFT_REPO --spec-type draft-dflash --spec-draft-n-max 16"
    want_spec=True
  else
    draft_args=""
    want_spec=False
  fi

  label="Muse-Glimmer-30B.K-Quant-17GB.xtx.dflash-$speculation"
  pred="$OUT/$label.pred.jsonl"
  score="$OUT/$label.score.json"
  server_log="/tmp/arm-$label.log"

  if [ -f "$pred" ]; then
    local have quarantine
    have=$(grep -c . "$pred")
    if [ "$have" -eq "$EXPECT" ] && [ -f "$score" ]; then
      say "SKIP $label, already banked and scored ($have notes)"
      return 0
    fi
    quarantine="$pred.interrupted-${have}rows-$(date -u +%Y%m%dT%H%M%SZ)"
    say "QUARANTINE: $have of $EXPECT rows as $(basename "$quarantine")"
    mv "$pred" "$quarantine"
  fi

  stop_server
  say "START $label model=$TARGET_REPO draft=${draft_args:-(none)} rows=$EXPECT"
  ssh -n -o ConnectTimeout=25 "$HOST" \
    "HF_HOME=$HF_HOME_REMOTE nohup setsid $BIN -hf $TARGET_REPO -hff $TARGET_FILE $draft_args --host $EP --port $PORT -c 8192 -np 1 --device Vulkan1 --cache-ram 1024 --no-webui --no-mmproj -ngl 99 >$server_log 2>&1 </dev/null &" \
    >/dev/null 2>&1

  while true; do
    ssh -n -o ConnectTimeout=10 "$HOST" \
      "curl -sf --max-time 5 http://$EP:$PORT/health" >/dev/null 2>&1 && break
    [ -n "$(remote_pid)" ] || [ -n "$(server_process_pid)" ] \
      || { say "FAIL: $label server exited while loading"; return 1; }
    sleep 15
  done

  local props loaded spec
  props=$(ssh -n -o ConnectTimeout=15 "$HOST" \
    "curl -sf --max-time 8 http://$EP:$PORT/props")
  loaded=$(printf '%s' "$props" | python3 -c \
    "import json,sys;print((json.load(sys.stdin).get('model_path') or '').split('/')[-1])")
  [ "$loaded" = "$WANT" ] \
    || { say "IDENTITY GUARD FAILED: loaded '$loaded', expected '$WANT'"; return 1; }
  say "loaded=$loaded"

  spec=$(ssh -n -o ConnectTimeout=15 "$HOST" \
    "curl -sf --max-time 8 http://$EP:$PORT/slots" \
    | python3 -c "import json,sys;d=json.load(sys.stdin);print((d[0] if d else {}).get('speculative'))")
  [ "${spec,,}" = "${want_spec,,}" ] \
    || { say "SPECULATION GUARD FAILED: got $spec, expected $want_spec"; return 1; }
  say "speculative=$spec as intended"

  if ss -ltnH "sport = :$PORT" 2>/dev/null | grep -q .; then
    say "FAIL: local port $PORT already occupied"
    return 1
  fi
  setsid ssh -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 \
    -L "$PORT:$EP:$PORT" "$HOST" >/dev/null 2>&1 &
  TUNNEL_PID=$!
  for _ in $(seq 1 15); do
    curl -sf --max-time 4 "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break
    sleep 2
  done
  curl -sf --max-time 4 "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 \
    || { say "FAIL: $label tunnel"; return 1; }

  local t0 t1
  t0=$(date +%s)
  python3 harness/harness/run_llamacpp.py --base-url "http://127.0.0.1:$PORT" \
    --model "$label" --gold "$GOLD" --out "$pred" --thinking \
    --max-tokens 8192 --concurrency 1 \
    || { say "FAIL: $label client"; return 1; }
  t1=$(date +%s)

  if ! python3 harness/harness/score.py --gold "$GOLD" --pred "$pred" \
      --json-out "$score" 2>"$OUT/$label.err"; then
    if grep -q 'thinking:true' "$OUT/$label.err"; then
      python3 harness/harness/score.py --gold "$GOLD" --pred "$pred" \
        --allow-thinking-off --json-out "$score" >/dev/null 2>&1 \
        || { say "BLOCKED: scorer rejected $label"; return 1; }
    else
      say "BLOCKED: scorer rejected $label"
      return 1
    fi
  fi
  rm -f "$OUT/$label.err"
  say "OK $label $(python3 -c "import json;d=json.load(open('$score'));s=d['strict'];print('F1=%.4f P=%.4f R=%.4f'%(s['f1'],s['precision'],s['recall']))") wall=$(((t1-t0)/60))m"

  if [ "$speculation" = on ]; then
    python3 harness/harness/draft_acceptance.py "$pred" \
      | sed 's/^/  /' | tee -a "$OUT/queue.log"
  elif grep -q '"draft_n"[[:space:]]*:[[:space:]]*[0-9]' "$pred"; then
    say "FAIL: DFlash-off artifact unexpectedly contains draft counters"
    return 1
  fi
  cleanup
}

say "PAIR START Muse Glimmer 30B K-Quant-17GB order=off,on card=xtx"
run_arm off || exit 1
run_arm on || exit 1
say "PAIR COMPLETE Muse Glimmer 30B K-Quant-17GB card=xtx"
