#!/bin/bash
# Assemble the campaign bundle and put it on CT 140. Runs on the REPO HOST.
#
# The bundle mirrors the evidence tree's shape because prompt.py resolves its
# ontology as REPO = Path(__file__).parents[3], i.e. from
#   <root>/raw/harness/harness/prompt.py
# it reads
#   <root>/src/rel_types.c  and  <root>/src/kb/kb_memory_facts.c
# Get that layout wrong and the scorer raises before it scores, which is the
# failure the pinned-ontology README exists to describe.
set -u

REPO=${REPO:-$(git rev-parse --show-toplevel)}
HOST=${HOST:-root@192.168.1.253}
CT=${CT:-140}
DEST=${DEST:-/opt/campaign}

H2H="$REPO/articles/local-llm-fact-extraction-head-to-head/evidence"
SYN="$REPO/articles/synthesis-model-selection/benchmarks"
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT

fail() { echo "PUSHFAIL: $*" >&2; exit 1; }

# --- verify every source exists BEFORE staging, so a missing file is named
[ -d "$H2H/raw/harness/harness" ] || fail "harness missing: $H2H/raw/harness/harness"
[ -f "$H2H/src/rel_types.c" ] || fail "pinned ontology missing: $H2H/src/rel_types.c"
[ -f "$H2H/src/kb/kb_memory_facts.c" ] || fail "pinned prompt missing: $H2H/src/kb/kb_memory_facts.c"
GOLD="$H2H/raw/corpus/data/corpora/v5/gold_small.jsonl"
[ -f "$GOLD" ] || fail "gold set missing: $GOLD"
# The synthesis controller requires the WHOLE bundle directory, not just the
# fixture: main() refuses to start unless corpus.jsonl, synthesis.jsonl and
# manifest.json are all present, and it hashes run_synthesis_ab.py and
# build_254_fixtures.py as siblings of the controller.
FIXDIR="$SYN/fixtures/ab-v1"
for f in corpus.jsonl synthesis.jsonl manifest.json; do
  [ -f "$FIXDIR/$f" ] || fail "synthesis bundle missing: $FIXDIR/$f"
done
for f in run_candidate_matrix.py analyze_candidate_matrix.py run_synthesis_ab.py build_254_fixtures.py; do
  [ -f "$SYN/ab-v2/$f" ] || fail "synthesis script missing: $SYN/ab-v2/$f"
done

# --- stage
mkdir -p "$STAGE/bundle/raw/harness" "$STAGE/bundle/src/kb" "$STAGE/bundle/synthesis"
cp -r "$H2H/raw/harness/harness" "$STAGE/bundle/raw/harness/harness" || fail "copy harness"
cp "$H2H/src/rel_types.c" "$STAGE/bundle/src/rel_types.c" || fail "copy rel_types.c"
cp "$H2H/src/kb/kb_memory_facts.c" "$STAGE/bundle/src/kb/" || fail "copy kb_memory_facts.c"
cp "$GOLD" "$STAGE/bundle/gold_small.jsonl" || fail "copy gold"

# The controller resolves its siblings by __file__, so the ab-v2 scripts must
# land together in one directory, with the fixture bundle beside them.
cp "$SYN/ab-v2/"*.py "$STAGE/bundle/synthesis/" || fail "copy synthesis scripts"

# run_synthesis_ab.py hardcodes "max_tokens": 1536 with no CLI override. That is
# the published fixture's budget and every model in the nine-configuration
# matrix completes inside it -- zero truncation across all nine. It is not
# enough for a model that cannot be stopped from reasoning, and it is a single
# literal standing between this campaign and a whole task's worth of results.
#
# Patch the BUNDLE COPY only; the published script in the repository is left
# untouched. The replacement reads an environment variable and keeps 1536 as the
# default, so an unset variable reproduces the published behaviour exactly.
#
# The verification below matters more than the patch: a sed that silently
# matches nothing is this campaign's single most common failure shape, and it
# would leave the budget at 1536 while every log claimed otherwise.
sed -i 's/"max_tokens": 1536,/"max_tokens": int(os.environ.get("SYNTH_MAX_TOKENS", "1536")),/' \
  "$STAGE/bundle/synthesis/run_synthesis_ab.py" || fail "max_tokens patch failed"
grep -q 'SYNTH_MAX_TOKENS' "$STAGE/bundle/synthesis/run_synthesis_ab.py" \
  || fail "max_tokens patch matched nothing; the literal must have changed"
grep -q '^import os' "$STAGE/bundle/synthesis/run_synthesis_ab.py" \
  || sed -i '0,/^import /s//import os\nimport /' "$STAGE/bundle/synthesis/run_synthesis_ab.py"
grep -q '^import os' "$STAGE/bundle/synthesis/run_synthesis_ab.py" \
  || fail "could not ensure 'import os' in run_synthesis_ab.py"
python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" \
  "$STAGE/bundle/synthesis/run_synthesis_ab.py" || fail "patched runner does not parse"
mkdir -p "$STAGE/bundle/synthesis/fixture"
cp "$FIXDIR/corpus.jsonl" "$FIXDIR/synthesis.jsonl" "$FIXDIR/manifest.json" \
   "$STAGE/bundle/synthesis/fixture/" || fail "copy synthesis fixture bundle"

for f in arms.tsv run_arm.sh run_campaign.sh run_synthesis_ladder.py run_synthesis_arm.sh throughput.py pair_ci.sh probe_reasoning_flags.sh chain_missing_arm.sh; do
  cp "$REPO/campaign/$f" "$STAGE/" || fail "copy $f"
done

GOLD_LINES=$(wc -l < "$STAGE/bundle/gold_small.jsonl")
[ "$GOLD_LINES" -eq 1001 ] || fail "gold set is $GOLD_LINES lines, expected 1001"

# --- verify PER FILE, not by hashing a file listing.
#
# The previous version hashed the output of `find | sha256sum | sed | sort`
# on both ends and compared the two digests. That compared path *formatting* as
# much as content: the local list yielded "arms.tsv" while the remote list,
# after its sed passed through ssh -> pct exec -> bash -lc quoting, kept the
# "./" prefix. Identical files, different digest, and a warning that meant
# nothing. A guard that cries wolf gets ignored, which is worse than no guard.
#
# A manifest of relative paths shipped with the bundle and checked by
# `sha256sum -c` on the far side compares content and nothing else, and names
# the offending file when it disagrees.
# The manifest must exclude itself: listing it means hashing a file that is
# still being written, which then fails its own check on the far side and
# reports a corrupt bundle when nothing is wrong.
( cd "$STAGE" && find . -type f -not -name MANIFEST.sha256 | sed 's#^\./##' | sort \
    | xargs sha256sum > MANIFEST.sha256 ) || fail "could not build manifest"

# Staged extract then atomic rename, so this is safe to run WHILE the campaign
# is running.
#
# bash reads a script incrementally as it executes, by file offset. Overwriting
# run_arm.sh in place under a live arm leaves the running shell reading from a
# shifted offset, executing fragments of the new file as though they were the
# old one. `mv` uses rename(2): the running instance keeps its original inode
# open and unchanged, while the directory entry points at the new file, so only
# the NEXT arm picks up the change.
#
# tar --unlink-first is not the answer here: it tries to unlink directories too
# and fails with "Cannot unlink: Directory not empty" on any re-push.
( cd "$STAGE" && tar czf - . ) | ssh -o ConnectTimeout=30 "$HOST" \
  "pct exec $CT -- bash -lc 'rm -rf $DEST/.incoming && mkdir -p $DEST/.incoming && tar xzf - -C $DEST/.incoming'"
rc=$?
[ "$rc" -eq 0 ] || fail "staged transfer exited $rc"

ssh -n -o ConnectTimeout=60 "$HOST" "pct exec $CT -- bash -lc '
cd $DEST/.incoming || exit 1
find . -type d -exec mkdir -p $DEST/{} \; || exit 1
find . -type f -exec mv -f {} $DEST/{} \; || exit 1
cd $DEST && rm -rf .incoming'"
rc=$?
[ "$rc" -eq 0 ] || fail "atomic install exited $rc"

VERIFY=$(ssh -n -o ConnectTimeout=60 "$HOST" \
  "pct exec $CT -- bash -lc 'cd $DEST && sha256sum -c --quiet MANIFEST.sha256 2>&1; echo RC=\$?'")
VRC=$(printf '%s' "$VERIFY" | grep -oE 'RC=[0-9]+' | tail -1 | cut -d= -f2)

if [ "${VRC:-1}" -ne 0 ]; then
  echo "PUSHFAIL: bundle verification failed on CT $CT" >&2
  printf '%s\n' "$VERIFY" >&2
  exit 2
fi
FILES=$(wc -l < "$STAGE/MANIFEST.sha256")
echo "PUSHOK $FILES files verified byte-for-byte at $DEST on CT $CT"
