#!/bin/bash
# Launch the registered 3,002-note 31B QAT pair on the RX 7900 XTX, 2026-08-11.
#
# This is a thin wrapper around harness/mid3k_pairs.sh. It changes NOTHING about
# the protocol: same corpus (gold_mid.jsonl, 3002 notes), same NPROC=1, same
# CACHE_RAM_MIB=1024, same port, both halves of the pair on the same physical
# card, same closing paired bootstrap. The registered prediction in that script
# -- that the 31B half-width falls from 0.0124 to about 0.0072 and clears zero --
# stands as written, and is not adjusted here or afterwards.
#
# The wrapper exists only to give the run a log outside the results directory and
# a single pid to supervise. The 12B half of the campaign is deliberately NOT
# launched: its half-width goes from 0.019 to about 0.011 and is not expected to
# resolve, and it would occupy the 5080 for a full night to say so.
#
# Preconditions verified before launch on 2026-08-11:
#   - evidence/src pin matches aimee c2b44220217c for BOTH files, so
#     prompt.verify_against_source() passes and rescoring still reproduces
#   - a 12-note smoke run completed 12/12 with 81.9% draft acceptance, parsed
#     every row, and scored without error
#   - XTX idle, no llama-server resident, port 8810 free
#   - both 31B repos and their MTP drafts resident in the host cache
set -u
cd "$(dirname "$0")" || exit 1

LOG=/home/virant/dev/rakuen-blog/.claude/worktrees/rescue-ten-ready-articles/articles/local-llm-fact-extraction-head-to-head/evidence/raw/harness/mid3k-xtx-20260811.log

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] launching mid3k_pairs.sh xtx" >> "$LOG"
bash harness/mid3k_pairs.sh xtx >> "$LOG" 2>&1
rc=$?
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] mid3k_pairs.sh xtx exited rc=$rc" >> "$LOG"
exit $rc
