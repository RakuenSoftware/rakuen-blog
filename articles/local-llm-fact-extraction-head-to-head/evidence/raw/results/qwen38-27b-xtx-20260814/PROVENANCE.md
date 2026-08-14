# Qwen3.8-27B Q4_K_M head-to-head run

## Collection

- **Time:** 2026-08-14 16:05:25 to 18:20:43 UTC
- **Population:** all 1,001 rows of `corpus/data/corpora/v5/gold_small.jsonl`,
  in file order
- **Prompt:** production prompt version `v8`, thinking enabled
- **Runtime:** `llama.cpp` b10356,
  SHA-256 `04fb990c970cf5ac299b07c26deb549f3f87b32fed7d3eaa9f4fa592e466d2c7`
- **Hardware:** AMD RX 7900 XTX, `Vulkan1`, one server slot and one client
  worker
- **Context:** 8,192 tokens
- **Model:** `ggml-org/Qwen3.8-27B-GGUF` revision
  `0669b98607d47046c7c2b3f801011d54a08cfccf`, file
  `Qwen3.8-27B-Q4_K_M.gguf`, 18,973,870,432 bytes
- **Draft model:** same repository and revision, file
  `mtp-Qwen3.8-27B-Q4_0.gguf`, 1,680,271,648 bytes
- **Official source revision:** `Qwen/Qwen3.8-27B` revision
  `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`
- **Persistent model copy:**
  `/mnt/media/storage/models/hf/hub/models--ggml-org--Qwen3.8-27B-GGUF`
  on `admin@192.168.1.254`
- **Command:** `harness/harness/arm_qwen38_27b_xtx.sh`

## Expected and observed result

The run was expected to produce one prediction for every corpus row, preserve
the row order and identifiers, use speculative decoding, and finish without a
transport error. The validator confirmed all four conditions.

Strict F1 was 0.7030: 0.6463 precision and 0.7705 recall. Median latency was
4.5076 seconds and median decode throughput was 72.0720 tokens per second. The
draft model accepted 303,888 of 507,481 proposed tokens, an acceptance rate of
0.5988.

One response, `g000191`, reached the 8,192-token context boundary. It failed
JSON parsing and schema validation. The raw runner marked `truncated: false`
because that older field only detects a completion equal to `--max-tokens`;
`validation.json` derives the context limit from 602 prompt tokens plus 7,589
completion tokens. The raw prediction remains unchanged.

## Artifact disposition

This is a valid native head-to-head result. It supports a Qwen3.8 Q4_K_M row
and comparisons that retain the runtime, quant and hardware limits above. It
does not support treating Q4_K_M as an Unsloth dynamic (UD) quant or attributing
the difference from a Qwen3.6 run solely to the model generation.
