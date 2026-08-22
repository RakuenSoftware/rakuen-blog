#!/bin/bash
# Which reasoning flag breaks structured output? Runs INSIDE CT 140.
#
# The synthesis harness constrains every response with
# `response_format: {type: json_schema, strict: true}`. After --reasoning off
# and --reasoning-format none were added, every request failed at sampler init:
#
#   E common_sampler_init: error initializing grammar sampler for grammar:
#
# with an EMPTY grammar string. This probe isolates which flag causes it instead
# of reverting both on a guess and hoping.
#
# Runs on a spare port with the smallest model in the campaign, so it can share
# the card with a running extraction arm. It issues one schema-constrained
# request per configuration and reports, for each, whether content came back.
set -u

BIN=${BIN:-/opt/llama.cpp/build-cuda/bin/llama-server}
PORT=${PORT:-8921}
MODEL=${MODEL:-LiquidAI/LFM2.5-2.6B-GGUF:Q4_K_M}
export HF_HOME=${HF_HOME:-/opt/hf}

probe() {  # <name> <extra server args...>
  local name=$1; shift
  local log=/tmp/probe-$name.log
  "$BIN" -hf "$MODEL" --host 127.0.0.1 --port "$PORT" --jinja -c 4096 -np 1 \
    --cache-ram 256 --device CUDA0 --no-webui --no-mmproj -ngl 99 -fa on \
    "$@" > "$log" 2>&1 &
  local srv=$!

  local ready=0
  for _ in $(seq 1 60); do
    curl -sf --max-time 3 "http://127.0.0.1:$PORT/health" > /dev/null 2>&1 && { ready=1; break; }
    kill -0 $srv 2>/dev/null || break
    sleep 2
  done
  if [ "$ready" != 1 ]; then
    echo "$name: SERVER_NEVER_READY"
    kill -9 $srv 2>/dev/null
    return
  fi

  # Same shape the synthesis runner uses: strict json_schema response format.
  local body='{"model":"probe","messages":[{"role":"user","content":"Name one colour."}],
    "temperature":0,"max_tokens":64,
    "response_format":{"type":"json_schema","json_schema":{"name":"p","strict":true,
      "schema":{"type":"object","properties":{"colour":{"type":"string"}},
      "required":["colour"],"additionalProperties":false}}}}'

  local out
  out=$(curl -s --max-time 60 "http://127.0.0.1:$PORT/v1/chat/completions" \
        -H 'Content-Type: application/json' -d "$body")

  printf '%s' "$out" | python3 -c '
import sys, json
name = sys.argv[1]
try:
    d = json.load(sys.stdin)
except Exception:
    print(f"{name}: RESPONSE_NOT_JSON"); raise SystemExit
if "error" in d:
    print(name + ": SERVER_ERROR " + str(d["error"])[:110]); raise SystemExit
try:
    choice = d["choices"][0]
    content = choice["message"].get("content")
except Exception:
    print(name + ": NO_CHOICES " + str(d)[:110]); raise SystemExit
if content:
    print(name + ": OK content=" + repr(content))
else:
    print(name + ": EMPTY_CONTENT finish=" + str(choice.get("finish_reason")))
' "$name"

  # Grammar failures appear in the server log, not the HTTP body.
  if grep -q "error initializing grammar sampler" "$log"; then
    echo "$name:   server log reports GRAMMAR SAMPLER INIT FAILURE"
  fi

  kill $srv 2>/dev/null; sleep 2; kill -9 $srv 2>/dev/null
  sleep 2
}

echo "=== reasoning-flag probe against strict json_schema ==="
probe baseline
probe reasoning-off        --reasoning off
probe format-none          --reasoning-format none
probe both                 --reasoning off --reasoning-format none
echo "=== done ==="
