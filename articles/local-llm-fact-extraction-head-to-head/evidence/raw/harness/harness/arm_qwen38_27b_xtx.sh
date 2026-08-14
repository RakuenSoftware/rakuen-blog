#!/bin/bash
# Qwen3.8-27B Q4_K_M with its repository MTP sidecar on the RX 7900 XTX.
#
# This is a native 1,001-note head-to-head arm. It uses the live production
# prompt, thinking enabled, greedy decoding, one server slot and the same
# gold_small.jsonl population as the saved Qwen3.6 arms.
set -euo pipefail

cd "$(dirname "$0")/../.."

HOST=admin@192.168.1.254
PORT=8117
BIN=/mnt/media/tierbench/bin/llama-b10356/llama-server
REPO=ggml-org/Qwen3.8-27B-GGUF
TARGET="$REPO:Q4_K_M"
WANT=Qwen3.8-27B-Q4_K_M
GOLD=corpus/data/corpora/v5/gold_small.jsonl
OUT=results/qwen38-27b-xtx-20260814
LBL=Qwen3.8-27B.Q4_K_M.xtx.mtp-on
PRED="$OUT/$LBL.pred.jsonl"
SCORE="$OUT/$LBL.score.json"
SERVER_LOG="$OUT/$LBL.server.log"
RUN_LOG="$OUT/$LBL.run.log"
mkdir -p "$OUT"

say() {
  echo "[$(date -u +%H:%M:%SZ)] $*" | tee -a "$RUN_LOG"
}

if [ -e "$PRED" ] || [ -e "$SCORE" ]; then
  say "refusing to overwrite an existing result"
  exit 1
fi

say "target=$TARGET draft_repo=$REPO"
say "official_source=Qwen/Qwen3.8-27B@1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0"
say "gguf_source=$REPO@0669b98607d47046c7c2b3f801011d54a08cfccf"
say "llama_server_sha256=$(ssh -n "$HOST" "sha256sum '$BIN'" | awk '{print $1}')"

ssh -n "$HOST" "pkill -f llama-server" >/dev/null 2>&1 || true
sleep 3
ssh -n -o ConnectTimeout=25 "$HOST" \
  "HF_HOME=/mnt/media/storage/models/hf nohup setsid '$BIN' -hf '$TARGET' -hfd '$REPO' --host 127.0.0.1 --port '$PORT' --jinja -c 8192 -np 1 -b 2048 -ub 2048 --cache-ram 1024 --device Vulkan1 --no-webui --no-mmproj -ngl 99 -fa on >'/tmp/$LBL.server.log' 2>&1 </dev/null &" \
  >/dev/null 2>&1

while true; do
  if ssh -n -o ConnectTimeout=10 "$HOST" \
    "curl -sf --max-time 5 http://127.0.0.1:$PORT/health" >/dev/null 2>&1; then
    break
  fi
  if ! ssh -n -o ConnectTimeout=10 "$HOST" "pgrep -f llama-server >/dev/null" 2>/dev/null; then
    say "server exited during load"
    ssh -n "$HOST" "tail -30 '/tmp/$LBL.server.log'" | tee -a "$RUN_LOG"
    exit 1
  fi
  sleep 10
done

LOADED=$(ssh -n "$HOST" "curl -s http://127.0.0.1:$PORT/props" |
  python3 -c "import json,sys; print((json.load(sys.stdin).get('model_path') or '').split('/')[-1])")
case "$LOADED" in
  *$WANT*) say "loaded=$LOADED" ;;
  *) say "identity guard failed: loaded=$LOADED wanted=*$WANT*"; exit 1 ;;
esac

SPEC=$(ssh -n "$HOST" "curl -s http://127.0.0.1:$PORT/slots" |
  python3 -c "import json,sys; d=json.load(sys.stdin); print((d[0] if d else {}).get('speculative'))")
[ "${SPEC,,}" = true ] || { say "speculation guard failed: speculative=$SPEC"; exit 1; }
say "speculative=$SPEC"
ssh -n "$HOST" "$BIN --list-devices 2>/dev/null | sed -n 2,4p" | tee -a "$RUN_LOG"

pkill -f "ssh -N -L $PORT:" >/dev/null 2>&1 || true
setsid nohup ssh -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 \
  -L "$PORT:127.0.0.1:$PORT" "$HOST" >/dev/null 2>&1 </dev/null &
sleep 4

python3 harness/harness/run_llamacpp.py \
  --base-url "http://127.0.0.1:$PORT" \
  --model "$LBL" \
  --gold "$GOLD" \
  --out "$PRED" \
  --thinking \
  --max-tokens 8192 \
  --concurrency 1

python3 harness/harness/score.py --gold "$GOLD" --pred "$PRED" --json-out "$SCORE"
ssh -n "$HOST" "cp '/tmp/$LBL.server.log' /tmp/qwen38-server-copy.log && cat /tmp/qwen38-server-copy.log" >"$SERVER_LOG"

python3 - "$SCORE" <<'PY' | tee -a "$RUN_LOG"
import json
import sys

strict = json.load(open(sys.argv[1], encoding="utf-8"))["strict"]
print(
    "OK F1={:.4f} precision={:.4f} recall={:.4f}".format(
        strict["f1"], strict["precision"], strict["recall"]
    )
)
PY
