#!/bin/bash
# test-sync_shelf.sh — falsification harness for shelf/sync_shelf.py (KOM build 1).
#
#   bash shelf/test-sync_shelf.sh [--record shelf/FALSIFY-sync_shelf.md]
#
# Scratch only: a scratch checkout (a copy of the tool at <scratch>/co/shelf/sync_shelf.py,
# so its REPO, LOCAL and registry resolve there) and scratch shelves under $TMPDIR, named
# through $KOM_SHELF. Nothing in this checkout, on the real shelf (Drive) or on any remote is
# written; the one read of the real shelf is section R (its .store_id is looked for, and the
# tool must refuse). Every tool command is printed after "$ ", its output follows, then
# "$ echo $?" and the exit code on its own line, never piped. PASS/FAIL lines are this
# harness's assertions on printed state (sha256 of files on both sides, registry lines,
# quarantine names, INDEX.tsv lines, the SYNC line last, no Traceback), never on the exit
# code alone. Exit 0 when every check passes, 1 otherwise.
set -u

HERE=$(cd "$(dirname "$0")" && pwd)
TOOL_SRC="$HERE/sync_shelf.py"
RECORD=""
[ "${1:-}" = "--record" ] && RECORD=${2:?--record needs a path}

S=$(mktemp -d "${TMPDIR:-/tmp}/sync_shelf_falsify.XXXXXX") || exit 2
S=$(cd "$S" && pwd -P)
CO="$S/co"                # the scratch checkout
mkdir -p "$CO/shelf" "$CO/.git"   # .git: inside_checkout() sees a checkout root
cp "$TOOL_SRC" "$CO/shelf/sync_shelf.py"
TOOL="$CO/shelf/sync_shelf.py"
REG="$CO/shelf/registry.json"
LOCAL="$CO/shelf/local"
SHELF="$S/shelf"          # the scratch shelf (stands in for My Drive/KILLER OF MEN)
export KOM_SHELF="$SHELF"
export PYTHONDONTWRITEBYTECODE=1
REAL_HOME=$HOME
PRESS="05 MARKETING/00 PRESS"

PASS=0; FAIL=0
ok()  { PASS=$((PASS + 1)); echo "  PASS  $1"; }
bad() { FAIL=$((FAIL + 1)); echo "  FAIL  $1"; }
check() { local d=$1; shift; if "$@" >/dev/null 2>&1; then ok "$d"; else bad "$d"; fi; }
contains() { printf '%s' "$1" | grep -qF -- "$2"; }
not_contains() { ! printf '%s' "$1" | grep -qF -- "$2"; }
scrub() { sed -e "s#/private$S#\$SCRATCH#g" -e "s#$S#\$SCRATCH#g" -e "s#$REAL_HOME#\$HOME#g"; }
sha() { shasum -a 256 "$1" | cut -d' ' -f1; }
run() { # prints the command, runs it unpiped into OUT, prints output and the exit code
  echo "\$ ${*//$S/\$SCRATCH}"
  OUT=$("$@" 2>&1)
  RC=$?
  printf '%s\n' "$OUT" | scrub | sed 's/^/  /'
  echo "\$ echo \$?"
  echo "$RC"
  printf '%s\n' "$OUT" >> "$S/all-output.txt"
}
regkey() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); e=d["files"].get(sys.argv[2]); print("" if e is None else e.get(sys.argv[3]))' "$REG" "$1" "$2"; }
regcount() { python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["files"]))' "$REG"; }
regid() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["store_id"])' "$REG"; }
last_is_sync() { printf '%s\n' "$1" | tail -1 | grep -q '^SYNC|'; }
syncline() { printf '%s\n' "$1" | grep '^SYNC|' | tail -1; }
mkfile() { # path bytes seed
  mkdir -p "$(dirname "$1")"
  python3 -c 'import sys,random; random.seed(int(sys.argv[3])); open(sys.argv[1],"wb").write(bytes(random.getrandbits(8) for _ in range(int(sys.argv[2]))))' "$1" "$2" "$3"
}

main() {
  echo "test-sync_shelf.sh — $(date -u +%Y-%m-%dT%H:%M:%SZ) — $(python3 --version) — tool sha256 $(sha "$TOOL_SRC" | cut -c1-12) — $(python3 "$TOOL" --version)"
  echo "scratch: \$SCRATCH (under \$TMPDIR); KOM_SHELF=\$SCRATCH/shelf; the checkout under test is \$SCRATCH/co"

  echo "== A: the scratch shelf, unstamped, holding four files (two covered, a .DS_Store, a .gdoc) =="
  mkfile "$SHELF/$PRESS/POSTER/poster.jpg" 20000 1
  mkfile "$SHELF/$PRESS/BTS/day 3/frame (1).jpg" 30000 2
  printf 'ds\n' > "$SHELF/$PRESS/.DS_Store"
  printf '{"url":"x"}\n' > "$SHELF/$PRESS/EPK INFO.gdoc"
  SHA_POSTER=$(sha "$SHELF/$PRESS/POSTER/poster.jpg"); SHA_FRAME=$(sha "$SHELF/$PRESS/BTS/day 3/frame (1).jpg")
  echo "  independent sha256: poster $SHA_POSTER"
  echo "  independent sha256: frame  $SHA_FRAME"

  echo "== 1: register on an unstamped shelf without --init-store — expect exit 2, no .store_id, no registry =="
  run python3 "$TOOL" register --only "$PRESS"
  check "exit 2 (refused)" [ "$RC" -eq 2 ]
  check "names --init-store" contains "$OUT" "--init-store"
  check "no .store_id created" [ ! -e "$SHELF/.store_id" ]
  check "no registry written" [ ! -e "$REG" ]

  echo "== 2: register --init-store — expect the stamp, two lines registered with the independent hashes, the .DS_Store and .gdoc skipped =="
  run python3 "$TOOL" register --only "$PRESS" --init-store
  check "exit 0" [ "$RC" -eq 0 ]
  check "SYNC line is last" last_is_sync "$OUT"
  check "summary: copied=2 (two lines written) problems=0" contains "$(syncline "$OUT")" "ok=0 copied=2 skipped=0 unregistered=0 not_pulled=0 problems=0|registry=2"
  check ".store_id written and equals the registry's store_id" [ "$(cat "$SHELF/.store_id")" = "$(regid)" ]
  check "registry holds exactly 2 keys" [ "$(regcount)" = "2" ]
  check "poster.jpg registered with the independent sha256" [ "$(regkey "$PRESS/POSTER/poster.jpg" sha256)" = "$SHA_POSTER" ]
  check "frame (1).jpg (a space, parentheses, a subfolder with a space) registered with the independent sha256" [ "$(regkey "$PRESS/BTS/day 3/frame (1).jpg" sha256)" = "$SHA_FRAME" ]
  check "bytes recorded (20000)" [ "$(regkey "$PRESS/POSTER/poster.jpg" bytes)" = "20000" ]
  check ".DS_Store not registered" [ -z "$(regkey "$PRESS/.DS_Store" sha256)" ]
  check ".gdoc not registered (a Drive shortcut, not bytes)" [ -z "$(regkey "$PRESS/EPK INFO.gdoc" sha256)" ]
  check "shelf/local untouched (register never copies)" [ ! -e "$LOCAL" ]
  check "the store_id lock released" [ ! -e "$SHELF/.locks/store_id.lock" ]

  echo "== 3: register again — expect ok=2 copied=0, registry unchanged =="
  R1=$(sha "$REG")
  run python3 "$TOOL" register --only "$PRESS"
  check "exit 0" [ "$RC" -eq 0 ]
  check "ok=2 copied=0" contains "$(syncline "$OUT")" "ok=2 copied=0"
  check "registry file byte-identical" [ "$(sha "$REG")" = "$R1" ]

  echo "== 4: --only that matches nothing — expect exit 2, never a pass =="
  run python3 "$TOOL" register --only "05 MARKETING/00 PRESS/NOPE"
  check "exit 2" [ "$RC" -eq 2 ]
  check "says it matched 0" contains "$OUT" "matched 0 of"

  echo "== 5: the shelf copy of poster.jpg rewritten in place, same size, other bytes — register (size only) passes it, --deep catches it, --force re-registers =="
  mkfile "$SHELF/$PRESS/POSTER/poster.jpg" 20000 99
  touch -t 202001010000 "$SHELF/$PRESS/POSTER/poster.jpg"   # an old mtime, so case 9 can be newer than the registry yet not "being written"
  SHA_POSTER2=$(sha "$SHELF/$PRESS/POSTER/poster.jpg")
  run python3 "$TOOL" register --only "$PRESS/POSTER"
  check "size-only register: exit 0 (a registered key counted ok by size)" [ "$RC" -eq 0 ]
  run python3 "$TOOL" register --only "$PRESS/POSTER" --deep
  check "--deep: exit 1 (a problem)" [ "$RC" -eq 1 ]
  check "--deep: STORE DIFFERS FROM REGISTRY" contains "$OUT" "STORE DIFFERS FROM REGISTRY (hash)  $PRESS/POSTER/poster.jpg"
  check "--deep: registry line unchanged" [ "$(regkey "$PRESS/POSTER/poster.jpg" sha256)" = "$SHA_POSTER" ]
  run python3 "$TOOL" register --only "$PRESS/POSTER" --deep --force
  check "--force: exit 0" [ "$RC" -eq 0 ]
  check "--force: re-registered line" contains "$OUT" "re-registered (--force)  $PRESS/POSTER/poster.jpg"
  check "--force: registry now names the new bytes" [ "$(regkey "$PRESS/POSTER/poster.jpg" sha256)" = "$SHA_POSTER2" ]
  SHA_POSTER=$SHA_POSTER2

  echo "== 6: status never touches the shelf (KOM_SHELF pointed at a path that does not exist) =="
  run env KOM_SHELF="$S/does-not-exist" python3 "$TOOL" status
  check "exit 0" [ "$RC" -eq 0 ]
  check "registered=2 not_pulled=2 for the press base" contains "$OUT" "registered=2      present=0      not_pulled=2"
  check "SYNC line: not_pulled=2" contains "$(syncline "$OUT")" "not_pulled=2"

  echo "== 7: a bare pull is refused (KOM build 1 enforces the rule) =="
  run python3 "$TOOL" pull
  check "exit 2" [ "$RC" -eq 2 ]
  check "says --only" contains "$OUT" "bare pull is refused"
  check "nothing pulled" [ ! -e "$LOCAL" ]

  echo "== 8: pull --only the poster — expect the local copy with the registered hash; a second pull is ok=1 =="
  run python3 "$TOOL" pull --only "$PRESS/POSTER"
  check "exit 0" [ "$RC" -eq 0 ]
  check "local copy hashes to the registry" [ "$(sha "$LOCAL/$PRESS/POSTER/poster.jpg")" = "$SHA_POSTER" ]
  check "the frame (not asked for) is not pulled" [ ! -e "$LOCAL/$PRESS/BTS/day 3/frame (1).jpg" ]
  run python3 "$TOOL" pull --only "$PRESS/POSTER"
  check "second pull: ok=1 copied=0" contains "$(syncline "$OUT")" "ok=1 copied=0"

  echo "== 9: the local poster edited, dated 5 minutes ago — pull skips it (LOCAL IS NEWER); --force displaces it to the quarantine, listed in INDEX.tsv, never deleted =="
  mkfile "$LOCAL/$PRESS/POSTER/poster.jpg" 20000 7
  SHA_EDIT=$(sha "$LOCAL/$PRESS/POSTER/poster.jpg")
  touch -t "$(date -v-300S +%Y%m%d%H%M.%S)" "$LOCAL/$PRESS/POSTER/poster.jpg"   # 5 min ago: newer than the registry's 2020 mtime, not "being written"
  run python3 "$TOOL" pull --only "$PRESS/POSTER"
  check "exit 0 with skipped=1" contains "$(syncline "$OUT")" "skipped=1"
  check "says LOCAL IS NEWER" contains "$OUT" "LOCAL IS NEWER"
  check "the edited local file is untouched" [ "$(sha "$LOCAL/$PRESS/POSTER/poster.jpg")" = "$SHA_EDIT" ]
  run python3 "$TOOL" pull --only "$PRESS/POSTER" --force
  check "--force: exit 0" [ "$RC" -eq 0 ]
  check "--force: the local copy is the registry's bytes again" [ "$(sha "$LOCAL/$PRESS/POSTER/poster.jpg")" = "$SHA_POSTER" ]
  Q=$(printf '%s\n' "$OUT" | sed -n 's/^quarantined differing local -> //p' | head -1)
  echo "  quarantine path: $Q"
  check "the edited bytes are in shelf/local/.quarantine under a versioned name" [ -n "$Q" ] && [ "$(sha "$LOCAL/$Q")" = "$SHA_EDIT" ]
  check "INDEX.tsv lists it with its sha256" grep -qF "$SHA_EDIT" "$LOCAL/.quarantine/INDEX.tsv"

  echo "== 10: verify --deep --strict over the press base — the certificate form: ok=1 (poster pulled), not_pulled=1 (frame), unregistered=0 problems=0 =="
  run python3 "$TOOL" verify --only "$PRESS" --deep --strict
  check "exit 0" [ "$RC" -eq 0 ]
  check "summary reads ok=1 ... not_pulled=1 problems=0" contains "$(syncline "$OUT")" "ok=1 copied=0 skipped=0 unregistered=0 not_pulled=1 problems=0"
  check "the frame is NOT PULLED, not a problem" contains "$OUT" "NOT PULLED  $PRESS/BTS/day 3/frame (1).jpg"

  echo "== 11: push a new local file into EPK BUILDS — registered and on the shelf; a shelf copy changed behind the registry is STORE CONFLICT until --force, which quarantines it on the shelf =="
  mkfile "$LOCAL/$PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf" 40000 11
  SHA_PDF=$(sha "$LOCAL/$PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf")
  run python3 "$TOOL" push --only "$PRESS/EPK BUILDS"
  check "exit 0" [ "$RC" -eq 0 ]
  check "copied=1" contains "$(syncline "$OUT")" "copied=1"
  check "shelf copy hashes to the local file" [ "$(sha "$SHELF/$PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf")" = "$SHA_PDF" ]
  check "registered" [ "$(regkey "$PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf" sha256)" = "$SHA_PDF" ]
  check "registry holds 3 keys" [ "$(regcount)" = "3" ]
  mkfile "$SHELF/$PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf" 40000 12
  SHA_FOREIGN=$(sha "$SHELF/$PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf")
  run python3 "$TOOL" push --only "$PRESS/EPK BUILDS"
  check "shelf copy changed by another writer: exit 1" [ "$RC" -eq 1 ]
  check "STORE CONFLICT (hash), nothing copied" contains "$OUT" "STORE CONFLICT (hash)  $PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf"
  check "the foreign shelf bytes untouched" [ "$(sha "$SHELF/$PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf")" = "$SHA_FOREIGN" ]
  run python3 "$TOOL" push --only "$PRESS/EPK BUILDS" --force
  check "--force: exit 0" [ "$RC" -eq 0 ]
  check "--force: the shelf holds the local bytes again" [ "$(sha "$SHELF/$PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf")" = "$SHA_PDF" ]
  QS=$(printf '%s\n' "$OUT" | sed -n 's/.*(prior store bytes -> \(.*\))$/\1/p' | head -1)
  echo "  shelf quarantine path: $QS"
  check "the foreign bytes are in the shelf's .quarantine, never deleted" [ -n "$QS" ] && [ "$(sha "$SHELF/$QS")" = "$SHA_FOREIGN" ]
  check "the shelf's INDEX.tsv lists them" grep -qF "$SHA_FOREIGN" "$SHELF/.quarantine/INDEX.tsv"

  echo "== 12: a shelf stamped with another id — every mode that opens the shelf refuses (WRONG STORE), nothing touched =="
  mkdir -p "$S/other-shelf/$PRESS/POSTER" && printf 'ffffffff-0000-0000-0000-000000000000' > "$S/other-shelf/.store_id"
  cp "$SHELF/$PRESS/POSTER/poster.jpg" "$S/other-shelf/$PRESS/POSTER/"
  for m in verify register pull push; do
    case $m in verify|register) o=$PRESS ;; *) o="$PRESS/POSTER" ;; esac
    run env KOM_SHELF="$S/other-shelf" python3 "$TOOL" "$m" --only "$o"
    check "$m --only '$o': exit 2" [ "$RC" -eq 2 ]
    check "$m: says WRONG STORE" contains "$OUT" "WRONG STORE"
  done
  check "the other shelf's id untouched" [ "$(cat "$S/other-shelf/.store_id")" = "ffffffff-0000-0000-0000-000000000000" ]

  echo "== 13: a flag on a mode it means nothing in — refused, exit 2 =="
  run python3 "$TOOL" status --deep
  check "status --deep: exit 2" [ "$RC" -eq 2 ]
  run python3 "$TOOL" register --only "$PRESS" --update
  check "register --update: exit 2" [ "$RC" -eq 2 ]
  run python3 "$TOOL" verify --only "$PRESS" --init-store
  check "verify --init-store: exit 2" [ "$RC" -eq 2 ]

  echo "== 14: no shelf at all (KOM_SHELF unset, no Drive glob match under a scratch HOME) — exit 2 naming KOM_SHELF =="
  run env -u KOM_SHELF HOME="$S/home" python3 "$TOOL" verify --only "$PRESS"
  check "exit 2" [ "$RC" -eq 2 ]
  check "names \$KOM_SHELF" contains "$OUT" "KOM_SHELF"

  echo "== 15: a local base that is a symlink out of the checkout — pull refuses (SYMLINKED BASE), nothing written through it =="
  mkfile "$SHELF/DELIVERY/master.mov" 5000 15
  run python3 "$TOOL" register --only DELIVERY
  check "DELIVERY registered" [ "$RC" -eq 0 ]
  mkdir -p "$S/elsewhere" && ln -s "$S/elsewhere" "$LOCAL/DELIVERY"
  run python3 "$TOOL" pull --only DELIVERY
  check "exit 2" [ "$RC" -eq 2 ]
  check "SYMLINKED BASE named" contains "$OUT" "SYMLINKED BASE  DELIVERY"
  check "nothing written into the link's target" [ -z "$(ls -A "$S/elsewhere")" ]
  rm "$LOCAL/DELIVERY"

  echo "== 16: merge-registry — a second checkout's registry (one new key) merges; a conflicting line refuses with nothing written =="
  python3 - "$REG" "$S/other.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
o = {"store_id": d["store_id"], "files": {"HANDOFFS/handoff-999-test.md": {"type": "file", "bytes": 3, "mtime": 0, "sha256": "a" * 64}}}
json.dump(o, open(sys.argv[2], "w"))
PY
  run python3 "$TOOL" merge-registry "$S/other.json"
  check "exit 0, added=1" contains "$(syncline "$OUT")" "added=1"
  check "registry holds 5 keys" [ "$(regcount)" = "5" ]
  python3 - "$REG" "$S/conflict.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
o = {"store_id": d["store_id"], "files": {"HANDOFFS/handoff-999-test.md": {"type": "file", "bytes": 3, "mtime": 0, "sha256": "b" * 64}}}
json.dump(o, open(sys.argv[2], "w"))
PY
  R2=$(sha "$REG")
  run python3 "$TOOL" merge-registry "$S/conflict.json"
  check "conflict: exit 2" [ "$RC" -eq 2 ]
  check "MERGE CONFLICT printed" contains "$OUT" "MERGE CONFLICT  HANDOFFS/handoff-999-test.md"
  check "registry byte-identical (nothing written)" [ "$(sha "$REG")" = "$R2" ]

  echo "== 17: nothing this run deleted — every byte version that existed is still on disk (in place or in a quarantine) =="
  check "the original poster bytes (v1) were replaced in place by this harness, not by the tool; the tool's displaced versions: edited local -> quarantine" [ "$(sha "$LOCAL/$Q")" = "$SHA_EDIT" ]
  check "foreign shelf pdf -> shelf quarantine" [ "$(sha "$SHELF/$QS")" = "$SHA_FOREIGN" ]
  check "no .part left anywhere" [ -z "$(find "$S" -name '*.part' -print -quit)" ]
  check "no lock left anywhere" [ -z "$(find "$S" -path '*/.locks/*' -name '*.lock' -print -quit)" ]

  echo "== R: the real shelf, read-only — with no registry id to match, the tool must refuse before touching it; no .store_id is created there =="
  REAL=$(ls -d "$REAL_HOME"/Library/CloudStorage/GoogleDrive-*/"My Drive/KILLER OF MEN" 2>/dev/null | head -1)
  if [ -z "$REAL" ]; then
    echo "  (no Drive mount on this Mac: section skipped)"
  else
    HAD_ID=0; [ -e "$REAL/.store_id" ] && HAD_ID=1
    mkdir -p "$S/fresh/shelf" "$S/fresh/.git" && cp "$TOOL_SRC" "$S/fresh/shelf/sync_shelf.py"
    run env -u KOM_SHELF HOME="$REAL_HOME" python3 "$S/fresh/shelf/sync_shelf.py" register --only "$PRESS"
    check "a fresh registry against the real shelf without --init-store: exit 2" [ "$RC" -eq 2 ]
    if [ "$HAD_ID" = 1 ]; then
      check "the real shelf is already stamped, so the refusal is WRONG STORE (its id is not this fresh registry's)" contains "$OUT" "WRONG STORE"
    else
      check "the real shelf is unstamped: the refusal names --init-store, and no .store_id appeared" [ ! -e "$REAL/.store_id" ]
    fi
    check "no registry written in the fresh checkout" [ ! -e "$S/fresh/shelf/registry.json" ]
  fi

  echo "== no Traceback in any output of this run =="
  check "0 tracebacks" [ "$(grep -c Traceback "$S/all-output.txt")" = "0" ]

  echo "== summary: PASS $PASS  FAIL $FAIL =="
  [ "$FAIL" -eq 0 ]
}

LOG="$S/run.log"
main > "$LOG" 2>&1
RC_MAIN=$?
scrub < "$LOG"
echo "harness exit:"
echo "$RC_MAIN"
if [ -n "$RECORD" ]; then
  {
    echo "# FALSIFY-sync_shelf — recorded run of shelf/test-sync_shelf.sh"
    echo
    echo "Tool under test: shelf/sync_shelf.py, sha256 \`$(sha "$TOOL_SRC")\` ($(wc -l < "$TOOL_SRC" | tr -d ' ') lines), \`--version\` prints \`$(python3 "$TOOL_SRC" --version)\`. Harness sha256 \`$(sha "$HERE/test-sync_shelf.sh")\`. Run $(sed -n 1p "$LOG" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]+Z') on $(uname -s) $(uname -r), $(python3 --version)."
    echo
    echo "Result: $(grep -E '^== summary: ' "$LOG" | sed 's/^== summary: //; s/ ==$//'); harness exit $RC_MAIN (0 = every check passed)."
    echo
    echo "Sections, in transcript order:"
    echo
    grep -E '^== ' "$LOG" | grep -vE '^== summary: ' | sed 's/^== /- /; s/ ==$//' | scrub
    echo
    echo "Method: a scratch checkout holds a copy of the tool (so its checkout, local mirror and registry resolve into the scratch directory) and \$KOM_SHELF names a scratch shelf; every command runs unpiped, its exit code read on its own line; assertions are on printed state (sha256 of both sides, registry lines, quarantine names, INDEX.tsv, the SYNC line last), never on the exit code alone. The real shelf is read once (section R) and must be refused; nothing is written there. Re-run: \`bash shelf/test-sync_shelf.sh --record shelf/FALSIFY-sync_shelf.md\`."
    echo
    echo '```text'
    scrub < "$LOG"
    echo "harness exit:"
    echo "$RC_MAIN"
    echo '```'
  } > "$RECORD"
  echo "recorded: $RECORD"
fi
exit "$RC_MAIN"
