#!/bin/bash
# Find the SMALLEST number of layers whose experts must go to CPU for a MoE
# model to fit the card. Runs INSIDE CT 140. Prints the number on stdout.
#
#   TARGET=<hf spec> [DRAFT=<hf spec>] tune_ncmoe.sh
#
# WHY THIS EXISTS. run_arm.sh previously used -cmoe, which moves EVERY expert
# tensor to system RAM. For gemma-4-26B-A4B at UD-Q4_K_XL that is catastrophic
# overkill: the model is 16,222 MiB against roughly 15,600 MiB usable -- about
# 600 MiB over -- and -cmoe answered that by shipping some 12 GiB to host RAM
# and leaving 11.5 GiB of a 16 GiB card idle. The arm served from 4,094 MiB of
# VRAM at 40.97 tok/s, against 179.69 tok/s for the smaller DENSE 12B.
#
# -ncmoe N offloads the experts of only the first N layers, so the card fills
# and only the remainder spills. The right N is the smallest one that fits, and
# measuring it is cheaper than guessing: a probe costs one model load and the
# arm it informs runs for hours.
set -u

BIN=${BIN:-/opt/llama.cpp/build-cuda/bin/llama-server}
PORT=${PORT:-8117}
CTX=${CTX:-8192}
CTK=${CTK:-f16}
CTV=${CTV:-f16}
TARGET=${TARGET:?set TARGET}
DRAFT=${DRAFT:-}
# Leave room for the KV cache to grow during a real run. A configuration that
# only just fits at load will fail later once context accumulates.
VRAM_CEILING=${VRAM_CEILING:-14200}
READY_TRIES=${READY_TRIES:-90}
export HF_HOME=${HF_HOME:-/opt/hf}

log() { echo "[tune] $*" >&2; }

# Try one N. Success means the server became healthy AND stayed under ceiling.
try_n() {
  local n=$1
  pkill -f "$BIN" 2>/dev/null
  for _ in $(seq 1 30); do
    pgrep -f "$BIN" > /dev/null 2>&1 || break
    sleep 2
  done
  sleep 3

  local args=(-hf "$TARGET" --host 127.0.0.1 --port "$PORT" -c "$CTX"
              -np 1 --cache-ram 1024 --no-webui --no-mmproj -ngl 99
              -ctk "$CTK" -ctv "$CTV" -ncmoe "$n")
  if [ -n "$DRAFT" ]; then
    args+=(-hfd "$DRAFT" --spec-draft-n-max 3 --spec-draft-n-min 1
           -ctkd "$CTK" -ctvd "$CTV")
  fi

  "$BIN" "${args[@]}" > "/tmp/tune-n$n.log" 2>&1 &
  local srv=$!
  local ok=1
  for _ in $(seq 1 "$READY_TRIES"); do
    if curl -sf --max-time 5 "http://127.0.0.1:$PORT/health" > /dev/null 2>&1; then
      ok=0; break
    fi
    kill -0 $srv 2>/dev/null || break
    sleep 4
  done

  local used=0
  if [ "$ok" = 0 ]; then
    used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)
  fi

  kill $srv 2>/dev/null; sleep 2; kill -9 $srv 2>/dev/null; sleep 3

  if [ "$ok" != 0 ]; then
    log "n=$n did not load"
    return 1
  fi
  if [ "${used:-99999}" -gt "$VRAM_CEILING" ]; then
    log "n=$n loaded but used ${used}MiB, over the ${VRAM_CEILING}MiB ceiling"
    return 1
  fi
  log "n=$n loaded, ${used}MiB used"
  return 0
}

# Binary search for the smallest workable N. Above the model's layer count
# -ncmoe behaves like -cmoe, so a model that can run at all is found by the
# upper bound and the search only narrows from there.
LO=0
HI=${HI:-64}
BEST=""

if try_n "$HI"; then
  BEST=$HI
else
  log "even n=$HI failed; this model cannot be served on this card"
  exit 1
fi

while [ $((HI - LO)) -gt 1 ]; do
  MID=$(( (LO + HI) / 2 ))
  if try_n "$MID"; then
    HI=$MID; BEST=$MID
  else
    LO=$MID
  fi
done

log "smallest workable n-cpu-moe = $BEST"
echo "$BEST"
