#!/bin/bash
# kom-check.sh — is this machine ready for KILLER OF MEN? Read-only: writes nothing, sets
# nothing, fetches nothing. One line per check, the verdict last, exit 1 when any FAIL.
#
#   bash bin/kom-check.sh
#
# Checks: the checkout (a kom-festival-board clone, its branch, dirty count), git identity,
# gh login, jq and python3, the Drive shelf (mount, .store_id against shelf/registry.json),
# the git guard (core.hooksPath), the Claude hooks file, and the next handoff number.
# Lines: CHECK|OK|<step>|<detail>  CHECK|WARN|<step>|<detail>  CHECK|FAIL|<step>|<the fix>
# Every URL prints through redact (an https origin can carry a token); every path as $HOME/...
set -u
export GIT_OPTIONAL_LOCKS=0
OK=0; WARN=0; FAIL=0
say() { # level step detail
  case "$1" in OK) OK=$((OK + 1)) ;; WARN) WARN=$((WARN + 1)) ;; FAIL) FAIL=$((FAIL + 1)) ;; esac
  printf 'CHECK|%s|%s|%s\n' "$1" "$2" "$(redact "${3//$HOME/\$HOME}")"
}
redact() {  # $1 -> printed with every URL's credentials as *** — the rule of kom-status.py's
  # redact_url: (a) scheme://authority, the authority ending at the first / ? # or blank: all
  # of it before its LAST @ is ***; (b) the scp form, a word with no ://: user:token@host:path
  # -> ***@host:path, a bare git@host:path stays. Idempotent.
  local s="$1" out="" auth w ws user host
  while :; do
    case "$s" in *://*) ;; *) break ;; esac
    out="$out${s%%://*}://"; s="${s#*://}"
    auth="${s%%[/?#[:space:]]*}"
    case "$auth" in *@*) out="$out***@"; s="${s#"${auth%@*}"@}" ;; esac
  done
  s="$out$s"; out=""
  while [ -n "$s" ]; do
    ws="${s%%[![:space:]]*}"; s="${s#"$ws"}"
    w="${s%%[[:space:]]*}"; s="${s#"$w"}"
    [ -n "$ws$w" ] || { out="$out$s"; break; }
    case "$w" in
      *://*) ;;
      *)
        auth="${w%%/*}"
        case "$auth" in
          *@*) user="${auth%@*}"; host="${auth##*@}"
               case "$user" in *:*) case "$host" in *:*) w="***@${w#"$user"@}" ;; esac ;; esac ;;
        esac ;;
    esac
    out="$out$ws$w"
  done
  printf '%s' "$out"
}

ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || { say FAIL checkout "not inside a git checkout; cd into kom-festival-board"; echo "CHECK|steps=1 ok=0 warn=0 fail=1|NOT READY"; exit 1; }
cd "$ROOT" || exit 1
ORIGIN=$(git remote get-url origin 2>/dev/null || echo "")
case "$ORIGIN" in
  *Scroggdawg/kom-festival-board*) say OK checkout "origin $ORIGIN at $ROOT" ;;
  *) say FAIL checkout "origin is '$ORIGIN', not Scroggdawg/kom-festival-board; gh repo clone Scroggdawg/kom-festival-board" ;;
esac
BRANCH=$(git symbolic-ref --short -q HEAD 2>/dev/null || echo "detached")
DIRTY=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
if [ "$BRANCH" = main ]; then say WARN branch "on main with $DIRTY uncommitted path(s): work on a branch (git switch -c <lane>); Luke merges main"; else say OK branch "$BRANCH, $DIRTY uncommitted path(s)"; fi

NAME=$(git config user.name 2>/dev/null || echo ""); EMAIL=$(git config user.email 2>/dev/null || echo "")
if [ -n "$NAME" ] && [ -n "$EMAIL" ]; then say OK git_identity "$NAME <$EMAIL>"; else say FAIL git_identity "git config --global user.name '<name>' && git config --global user.email '<email>'"; fi
if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then say OK gh "gh auth status: logged in"; else say FAIL gh "gh auth login"; fi
else say FAIL gh "brew install gh && gh auth login"; fi
command -v jq >/dev/null 2>&1 && say OK jq "$(jq --version 2>/dev/null)" || say FAIL jq "brew install jq (the Claude hooks read their input with it)"
command -v python3 >/dev/null 2>&1 && say OK python3 "$(python3 --version 2>/dev/null)" || say FAIL python3 "install python3 (the shelf tool and the status script need it)"

SHELF=${KOM_SHELF:-}
if [ -z "$SHELF" ]; then
  n=0
  for d in "$HOME"/Library/CloudStorage/GoogleDrive-*/"My Drive/KILLER OF MEN"; do [ -d "$d" ] && { n=$((n + 1)); SHELF=$d; }; done
  [ "$n" -gt 1 ] && say FAIL shelf "several Drive mounts hold KILLER OF MEN; export KOM_SHELF=\"<the one to use>\" in ~/.zshenv"
fi
if [ -z "$SHELF" ] || [ ! -d "$SHELF" ]; then
  say WARN shelf "no Drive shelf on this machine (sign Drive for desktop in as camerawrap@gmail.com, or export KOM_SHELF); git work still fine, the big files are not here"
else
  WANT=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("store_id",""))' shelf/registry.json 2>/dev/null || echo "")
  HAVE=$(cat "$SHELF/.store_id" 2>/dev/null || echo "")
  if [ -z "$WANT" ]; then say WARN shelf "shelf at $SHELF; no shelf/registry.json in this checkout (merge main)";
  elif [ -z "$HAVE" ]; then say FAIL shelf "shelf at $SHELF carries no .store_id; the registry names $WANT — this is not the stamped shelf, or Drive has not synced .store_id yet";
  elif [ "$WANT" != "$HAVE" ]; then say FAIL shelf "WRONG SHELF: registry names $WANT, $SHELF carries $HAVE";
  else say OK shelf "$SHELF, .store_id $HAVE matches shelf/registry.json ($(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))["files"]))' shelf/registry.json 2>/dev/null) files registered)"; fi
fi

HP=$(git config core.hooksPath 2>/dev/null || echo "")
if [ "$HP" = "bin/githooks" ] || [ "$HP" = "$ROOT/bin/githooks" ]; then say OK git_guard "core.hooksPath = $HP (pre-commit refuses big files, secrets, duplicate handoff numbers, home paths)";
else say WARN git_guard "core.hooksPath unset: git config core.hooksPath bin/githooks (one line per clone; refuses big files, secrets, duplicate handoff numbers, home paths)"; fi
[ -f .claude/settings.json ] && say OK claude_hooks ".claude/settings.json wires kom-session-start.sh, kom-prompt.sh, kom-stop.sh" || say WARN claude_hooks "no .claude/settings.json here (merge main)"

nums() { grep -oE '^handoff-[0-9]+' | grep -oE '[0-9]+' | sort -n | tail -1; }
HERE_MAX=$(ls handoffs 2>/dev/null | nums); HERE_MAX=$((10#${HERE_MAX:-0}))
REF_MAX=$(git for-each-ref --format='%(refname)' refs/heads refs/remotes 2>/dev/null | while IFS= read -r r; do git ls-tree --name-only "$r:handoffs" 2>/dev/null; done | nums); REF_MAX=$((10#${REF_MAX:-0}))
WT_MAX=0
while IFS= read -r wt; do wt=${wt#worktree }; [ -n "$wt" ] && [ "$wt" != "$ROOT" ] || continue; n=$(ls "$wt/handoffs" 2>/dev/null | nums); n=$((10#${n:-0})); [ "$n" -gt "$WT_MAX" ] && WT_MAX=$n; done < <(git worktree list --porcelain 2>/dev/null | grep '^worktree ')
DRIVE_MAX=0; [ -n "$SHELF" ] && [ -d "$SHELF/HANDOFFS" ] && { DRIVE_MAX=$(ls "$SHELF/HANDOFFS" 2>/dev/null | nums); DRIVE_MAX=$((10#${DRIVE_MAX:-0})); }
MAX=$HERE_MAX; for v in $REF_MAX $WT_MAX $DRIVE_MAX; do [ "$v" -gt "$MAX" ] && MAX=$v; done
say OK next_handoff "handoffs/handoff-$((MAX + 1))-<lane>.md (newest: here $HERE_MAX, refs $REF_MAX, other checkouts $WT_MAX, Drive ledger $DRIVE_MAX)"

TOTAL=$((OK + WARN + FAIL))
if [ "$FAIL" -eq 0 ]; then V=READY; else V="NOT READY"; fi
echo "CHECK|steps=$TOTAL ok=$OK warn=$WARN fail=$FAIL|$V"
[ "$FAIL" -eq 0 ]
