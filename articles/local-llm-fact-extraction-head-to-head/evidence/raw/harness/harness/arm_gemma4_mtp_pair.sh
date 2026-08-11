#!/bin/bash
# One side of a same-card Gemma 4 UD-QAT MTP pair.
#
# Usage: SIZE=12b|26b|31b CARD=5080|xtx MTP=on|off bash this-script
# The queue wrapper keeps both sides of every model on the same physical card.
set -u
cd "$(dirname "$0")/../.." || exit 1

SIZE=${SIZE:?set SIZE=12b, 26b or 31b}
CARD=${CARD:?set CARD=5080 or xtx}
MTP=${MTP:?set MTP=on or off}
OUT=results/gemma4-mtp-pairs-20260810
GOLD=corpus/data/corpora/v5/gold_small.jsonl
EXPECT=$(grep -c . "$GOLD")
mkdir -p "$OUT"
say() { echo "[$(date -u +%H:%M:%SZ)] $*" | tee -a "$OUT/arms.log"; }

case "$SIZE" in
  12b) REPO=unsloth/gemma-4-12B-it-qat-GGUF:UD-Q4_K_XL
       DRAFT=unsloth/gemma-4-12B-it-qat-GGUF:MTP/mtp-gemma-4-12B-it-Q8_0.gguf
       WANT=gemma-4-12B-it-qat; SIZE_LABEL=12B ;;
  26b) REPO=unsloth/gemma-4-26B-A4B-it-qat-GGUF:UD-Q4_K_XL
       DRAFT=unsloth/gemma-4-26B-A4B-it-qat-GGUF:MTP/mtp-gemma-4-26B-A4B-it-Q8_0.gguf
       WANT=gemma-4-26B-A4B-it-qat; SIZE_LABEL=26B-A4B ;;
  31b) REPO=unsloth/gemma-4-31B-it-qat-GGUF:UD-Q4_K_XL
       DRAFT=unsloth/gemma-4-31B-it-qat-GGUF:MTP/mtp-gemma-4-31B-it-Q8_0.gguf
       WANT=gemma-4-31B-it-qat; SIZE_LABEL=31B ;;
  *) say "SIZE must be 12b, 26b or 31b"; exit 1 ;;
esac

case "$MTP" in
  on) DRAFT_ARG="-hfd $DRAFT"; WANT_SPEC=True ;;
  off) DRAFT_ARG=""; WANT_SPEC=False ;;
  *) say "MTP must be on or off"; exit 1 ;;
esac

case "$CARD" in
  5080)
    [ "$SIZE" != 31b ] || { say "31B does not fit the 5080; refusing cross-card substitution"; exit 1; }
    HOST=root@192.168.1.253
    EP=$(ssh -n -o ConnectTimeout=15 "$HOST" "pct exec 140 -- hostname -I" 2>/dev/null | awk '{print $1}')
    [ -n "$EP" ] || { say "could not resolve CT140 address"; exit 1; }
    PORT=8994
    BIN=/opt/llama.cpp/build-cuda/bin/llama-server
    HF_HOME_REMOTE=/opt/hf
    REMOTE_LOG_DIR=/opt/tierA
    ;;
  xtx)
    [ "$SIZE" = 31b ] || { say "$SIZE_LABEL is assigned to the 5080; refusing cross-card substitution"; exit 1; }
    HOST=admin@192.168.1.254
    EP=127.0.0.1
    PORT=8118
    BIN=/mnt/media/tierbench/bin/llama-b10210/llama-server
    HF_HOME_REMOTE=/mnt/media/tierbench/hf
    REMOTE_LOG_DIR=/tmp
    ;;
  *) say "CARD must be 5080 or xtx"; exit 1 ;;
esac

LBL="gemma-4-${SIZE_LABEL}-it.qat-UD-Q4_K_XL.${CARD}.mtp-${MTP}"
PRED="$OUT/$LBL.pred.jsonl"
SCORE="$OUT/$LBL.score.json"
SERVER_LOG="$REMOTE_LOG_DIR/arm-$LBL.log"

if [ -f "$PRED" ]; then
  HAVE=$(grep -c . "$PRED")
  if [ "$HAVE" -eq "$EXPECT" ]; then
    say "SKIP $LBL, already banked ($HAVE notes)"
    exit 0
  fi
  QUAR="$PRED.interrupted-${HAVE}rows-$(date -u +%Y%m%dT%H%M%SZ)"
  say "QUARANTINE $HAVE of $EXPECT rows from interrupted $LBL as $(basename "$QUAR")"
  mv "$PRED" "$QUAR"
fi

remote_pid() {
  if [ "$CARD" = 5080 ]; then
    ssh -n -o ConnectTimeout=15 "$HOST" "pct exec 140 -- ss -ltnpH 'sport = :$PORT'" 2>/dev/null
  else
    ssh -n -o ConnectTimeout=15 "$HOST" "ss -ltnpH 'sport = :$PORT'" 2>/dev/null
  fi | grep -oE 'pid=[0-9]+' | head -1 | cut -d= -f2
}

# The XTX does not open its HTTP listener until a large model has finished
# loading. Track the launched server process as well as the listening socket so
# a normal multi-minute load is not mistaken for an early exit.
server_process_pid() {
  local pattern="^$BIN .*--port $PORT( |$)"
  if [ "$CARD" = 5080 ]; then
    ssh -n -o ConnectTimeout=15 "$HOST" \
      "pct exec 140 -- pgrep -f '$pattern'" 2>/dev/null | head -1
  else
    ssh -n -o ConnectTimeout=15 "$HOST" \
      "pgrep -f '$pattern'" 2>/dev/null | head -1
  fi
}

stop_server() {
  local pid
  pid=$(remote_pid)
  [ -n "$pid" ] || return 0
  if [ "$CARD" = 5080 ]; then
    ssh -n -o ConnectTimeout=15 "$HOST" "pct exec 140 -- kill -TERM $pid" >/dev/null 2>&1 || true
  else
    ssh -n -o ConnectTimeout=15 "$HOST" "kill -TERM $pid" >/dev/null 2>&1 || true
  fi
  sleep 4
}

TUNNEL_PID=""
cleanup() {
  [ -n "$TUNNEL_PID" ] && kill "$TUNNEL_PID" 2>/dev/null || true
  stop_server
}
trap cleanup EXIT INT TERM

stop_server
say "=== $LBL"
say "model=$REPO draft=${DRAFT_ARG:-(none)} card=$CARD corpus=$GOLD rows=$EXPECT concurrency=1"

if [ "$CARD" = 5080 ]; then
  ssh -n -o ConnectTimeout=25 "$HOST" \
    "pct exec 140 -- bash -lc 'HF_HOME=$HF_HOME_REMOTE nohup setsid $BIN -hf $REPO $DRAFT_ARG --host 0.0.0.0 --port $PORT -c 8192 -np 1 --cache-ram 1024 --no-webui --no-mmproj -ngl 99 >$SERVER_LOG 2>&1 </dev/null &'" >/dev/null 2>&1
else
  ssh -n -o ConnectTimeout=25 "$HOST" \
    "HF_HOME=$HF_HOME_REMOTE nohup setsid $BIN -hf $REPO $DRAFT_ARG --host 127.0.0.1 --port $PORT -c 8192 -np 1 --device Vulkan1 --cache-ram 1024 --no-webui --no-mmproj -ngl 99 >$SERVER_LOG 2>&1 </dev/null &" >/dev/null 2>&1
fi

while true; do
  ssh -n -o ConnectTimeout=10 "$HOST" "curl -sf --max-time 5 http://$EP:$PORT/health" >/dev/null 2>&1 && break
  [ -n "$(remote_pid)" ] || [ -n "$(server_process_pid)" ] \
    || { say "FAIL: server exited while loading"; exit 1; }
  sleep 15
done

PROPS=$(ssh -n -o ConnectTimeout=15 "$HOST" "curl -sf --max-time 8 http://$EP:$PORT/props")
LOADED=$(printf '%s' "$PROPS" | python3 -c "import json,sys;print((json.load(sys.stdin).get('model_path') or '').split('/')[-1])")
case "$LOADED" in
  *"$WANT"*UD-Q4_K_XL*) say "loaded=$LOADED" ;;
  *) say "IDENTITY GUARD FAILED: loaded '$LOADED', expected $WANT UD-Q4_K_XL"; exit 1 ;;
esac

SPEC=$(ssh -n -o ConnectTimeout=15 "$HOST" "curl -sf --max-time 8 http://$EP:$PORT/slots" \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print((d[0] if d else {}).get('speculative'))")
[ "${SPEC,,}" = "${WANT_SPEC,,}" ] || { say "SPECULATION GUARD FAILED: got $SPEC, expected $WANT_SPEC"; exit 1; }
say "speculative=$SPEC as intended"

if ss -ltnH "sport = :$PORT" 2>/dev/null | grep -q .; then
  say "FAIL: local port $PORT already occupied"
  exit 1
fi
setsid ssh -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -L "$PORT:$EP:$PORT" "$HOST" >/dev/null 2>&1 &
TUNNEL_PID=$!
for _ in $(seq 1 15); do
  curl -sf --max-time 4 "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break
  sleep 2
done
curl -sf --max-time 4 "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 || { say "FAIL: tunnel"; exit 1; }

T0=$(date +%s)
python3 harness/harness/run_llamacpp.py --base-url "http://127.0.0.1:$PORT" --model "$LBL" \
  --gold "$GOLD" --out "$PRED" --thinking --max-tokens 8192 --concurrency 1 \
  || { say "FAIL: client"; exit 1; }
T1=$(date +%s)

if ! python3 harness/harness/score.py --gold "$GOLD" --pred "$PRED" --json-out "$SCORE" 2>"$OUT/$LBL.err"; then
  if grep -q 'thinking:true' "$OUT/$LBL.err"; then
    python3 harness/harness/score.py --gold "$GOLD" --pred "$PRED" --allow-thinking-off --json-out "$SCORE" >/dev/null 2>&1
  else
    say "BLOCKED: scorer rejected $LBL"
    exit 1
  fi
fi
rm -f "$OUT/$LBL.err"
say "OK $LBL $(python3 -c "import json;d=json.load(open('$SCORE'));s=d['strict'];print('F1=%.4f P=%.4f R=%.4f'%(s['f1'],s['precision'],s['recall']))") wall=$(((T1-T0)/60))m"
if [ "$MTP" = on ]; then
  python3 harness/harness/draft_acceptance.py "$PRED" | sed 's/^/  /' | tee -a "$OUT/arms.log"
else
  # Test the VALUE, not the key. Every row carries draft_n in every run; it is
  # null with speculation off and an integer with it on. Grepping for the key
  # fired on every clean off-arm (defect 43).
  if ! python3 -c "
import json,sys
for line in open(sys.argv[1]):
    line = line.strip()
    if not line:
        continue
    if (json.loads(line).get('draft_n') or 0) > 0:
        sys.exit(1)
sys.exit(0)
" "$PRED"; then
    say "FAIL: MTP-off artifact unexpectedly contains draft counters"
    exit 1
  fi
fi
