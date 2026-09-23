#!/bin/bash
# kom-session-start.sh — SessionStart hook of kom-festival-board (KOM build 1, from
# petrol-brand-bible's bin/hooks/petrol-session-start.sh).
# Wired by .claude/settings.json as  bash "$CLAUDE_PROJECT_DIR/bin/hooks/kom-session-start.sh"
#
# stdout is context the model reads at session start. It prints:
#   behind / ahead / dirty (after one bounded git fetch), the branch, the lane, the upstream,
#   the publish line for this checkout (never a bare git push, never a push to main: the
#   rule of kom-stop.sh), the handoff numbers (newest in handoffs/ here; next = max over the
#   refs, every other checkout on this Mac and the Drive ledger + 1), the recap block of the
#   newest handoff here, and the shelf status from this checkout's shelf/sync_shelf.py
#   (status mode: local only, never opens a shelf file). When CLAUDE_CODE_REMOTE=true the
#   shelf step is skipped and says so.
# A branch's remote (the publish warning) and every recap line print through redact.
# This hook prints no git add line.
#
# Read-only apart from `git fetch --quiet` (remote-tracking refs only; capped at 15 s so a
# dead network cannot stall a session start). Never pulls, adds, commits, pushes or checks out.
#   KOM_SESSION_NO_FETCH=1   skip the fetch (tests; offline)
set -u
export GIT_OPTIONAL_LOCKS=0
export PYTHONDONTWRITEBYTECODE=1
LEDGER=handoffs

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

IN=$(cat 2>/dev/null) || IN=""
CWD=""
if command -v jq >/dev/null 2>&1 && [ -n "$IN" ]; then
  CWD=$(printf '%s' "$IN" | jq -r '.cwd // empty' 2>/dev/null)
fi
[ -n "$CWD" ] || CWD=${CLAUDE_PROJECT_DIR:-$PWD}
cd "$CWD" 2>/dev/null || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$ROOT" || exit 0

REMOTE_SESSION=0
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] && REMOTE_SESSION=1

# one bounded fetch, so "behind" is a number and not a guess
FETCH=skipped
if [ "${KOM_SESSION_NO_FETCH:-0}" != 1 ]; then
  git fetch --quiet >/dev/null 2>&1 &
  fp=$!
  i=0
  while kill -0 "$fp" 2>/dev/null && [ "$i" -lt 15 ]; do sleep 1; i=$((i + 1)); done
  if kill -0 "$fp" 2>/dev/null; then
    kill "$fp" 2>/dev/null; FETCH="timed out after 15 s"
  else
    if wait "$fp"; then FETCH=ok; else FETCH=failed; fi
  fi
fi

BRANCH=$(git symbolic-ref --short -q HEAD 2>/dev/null) || BRANCH="HEAD (detached)"
UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null) || UPSTREAM=""
UPSTREAM_REF=$(git rev-parse --symbolic-full-name '@{u}' 2>/dev/null) || UPSTREAM_REF=""
UPS_REMOTE=$(git config "branch.$BRANCH.remote" 2>/dev/null) || UPS_REMOTE=""
ORIGIN_BRANCH=""
if [ "$UPS_REMOTE" = origin ]; then
  case "$UPSTREAM_REF" in refs/remotes/origin/?*) ORIGIN_BRANCH=${UPSTREAM_REF#refs/remotes/origin/} ;; esac
fi
UPS_SHOWN=${UPSTREAM:-none}
[ -z "$ORIGIN_BRANCH" ] && [ -n "$UPSTREAM_REF" ] && UPS_SHOWN=$UPSTREAM_REF
DIRTY=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
if [ -n "$ORIGIN_BRANCH" ]; then
  BEHIND=$(git rev-list --count 'HEAD..@{u}' 2>/dev/null) || BEHIND=0
  AHEAD=$(git rev-list --count '@{u}..HEAD' 2>/dev/null) || AHEAD=0
else
  BEHIND="?"
  AHEAD=$(git rev-list --count HEAD --not --remotes=origin 2>/dev/null) || AHEAD=0
fi

# handoff numbers (KOM: the handoffs/ ledger; the rule of kom-stop.sh)
nums() { grep -oE '^handoff-[0-9]+' | grep -oE '[0-9]+' | sort -n | tail -1; }
NEWEST_FILE=$(ls "$ROOT/$LEDGER" 2>/dev/null | grep -E '^handoff-[0-9]+' | sort -t- -k2,2n | tail -1)
LAST_HANDOFF=$(printf '%s\n' "$NEWEST_FILE" | nums); LAST_HANDOFF=$((10#${LAST_HANDOFF:-0}))
REF_MAX=$(git for-each-ref --format='%(refname)' refs/heads refs/remotes 2>/dev/null \
  | while IFS= read -r r; do git ls-tree --name-only "$r:$LEDGER" 2>/dev/null; done | nums)
REF_MAX=$((10#${REF_MAX:-0}))
WT_MAX=0; WT_WHERE=""
while IFS= read -r wt; do
  wt=${wt#worktree }
  [ -n "$wt" ] && [ "$wt" != "$ROOT" ] || continue
  n=$(ls "$wt/$LEDGER" 2>/dev/null | nums); n=$((10#${n:-0}))
  if [ "$n" -gt "$WT_MAX" ]; then WT_MAX=$n; WT_WHERE=${wt/#$HOME/\$HOME}; fi
done < <(git worktree list --porcelain 2>/dev/null | grep '^worktree ')
SHELF=${KOM_SHELF:-}
if [ -z "$SHELF" ]; then
  for d in "$HOME"/Library/CloudStorage/GoogleDrive-*/"My Drive/KILLER OF MEN"; do
    [ -d "$d" ] && { SHELF=$d; break; }
  done
fi
DRIVE_MAX=0
if [ -n "$SHELF" ] && [ -d "$SHELF/HANDOFFS" ]; then
  DRIVE_MAX=$(ls "$SHELF/HANDOFFS" 2>/dev/null | nums); DRIVE_MAX=$((10#${DRIVE_MAX:-0}))
fi
ELSEWHERE_MAX=$REF_MAX; ELSEWHERE="the refs"
[ "$WT_MAX" -gt "$ELSEWHERE_MAX" ] && { ELSEWHERE_MAX=$WT_MAX; ELSEWHERE="the checkout $WT_WHERE"; }
[ "$DRIVE_MAX" -gt "$ELSEWHERE_MAX" ] && { ELSEWHERE_MAX=$DRIVE_MAX; ELSEWHERE="the Drive ledger HANDOFFS/"; }

LANE=$(git config --worktree kom.lane 2>/dev/null) || LANE=""
[ -n "$LANE" ] || LANE=$(git config kom.lane 2>/dev/null) || LANE=""
LANE_NOTE=""
if [ -z "$LANE" ]; then
  if [ "$BRANCH" = main ]; then
    LANE=main
  else
    case "$BRANCH" in
      claude/*)
        LANE=$(printf '%s' "$NEWEST_FILE" | sed -nE 's/^handoff-[0-9]+-([A-Za-z0-9_-]+)\.md$/\1/p')
        if [ -n "$LANE" ]; then
          LANE_NOTE=" (a guess from $LEDGER/$NEWEST_FILE; fix it: git config --worktree kom.lane <lane>)"
        else
          LANE="<lane>"; LANE_NOTE=" (kom.lane unset: git config --worktree kom.lane <lane>)"
        fi ;;
      *) LANE=$(basename "$BRANCH") ;;
    esac
  fi
fi

if [ "$BRANCH" = main ]; then
  PUBLISH="none: main is not a working branch (git switch -c <lane>, then git push -u origin HEAD)"
elif [ -n "$ORIGIN_BRANCH" ] && [ "$ORIGIN_BRANCH" != main ]; then
  PUBLISH="git push origin HEAD:$ORIGIN_BRANCH"
else
  PUBLISH="git push -u origin HEAD"
  if [ -n "$UPSTREAM_REF" ]; then
    case "$UPSTREAM_REF" in
      refs/heads/*)             WHY="a local branch, not GitHub" ;;
      refs/remotes/origin/main) WHY="main, never a publish target" ;;
      *)                        WHY="on remote $(redact "${UPS_REMOTE:-?}"), not origin" ;;   # a remote may be a URL
    esac
    PUBLISH="$PUBLISH   (warning: upstream $UPSTREAM_REF is $WHY; the -u form publishes this branch to origin and re-points the upstream)"
  fi
fi

if [ "$LAST_HANDOFF" -gt "$ELSEWHERE_MAX" ]; then
  NEXT_LINE="$LEDGER/$NEWEST_FILE here is on no ref and held nowhere else (uncommitted); the next number after it is $((LAST_HANDOFF + 1))"
else
  NEXT_LINE="next handoff number: $((ELSEWHERE_MAX + 1)) (max over the refs is $REF_MAX, over the other checkouts on this Mac $WT_MAX${WT_WHERE:+ ($WT_WHERE)}, over the Drive ledger $DRIVE_MAX)"
fi

echo "[kom] $BRANCH — lane $LANE$LANE_NOTE — upstream $UPS_SHOWN — behind:$BEHIND ahead:$AHEAD dirty:$DIRTY (fetch: $FETCH) — checkout: ${ROOT/#$HOME/\$HOME}"
echo "[kom] publish line: $PUBLISH"
echo "[kom] handoffs: newest here ${NEWEST_FILE:-none}; $NEXT_LINE"
if [ "$BEHIND" != "?" ] && [ "$BEHIND" -gt 0 ] 2>/dev/null; then
  echo "[kom] behind by $BEHIND: pull first (git pull --ff-only) before any edit."
fi

if [ -n "$NEWEST_FILE" ] && [ -f "$ROOT/$LEDGER/$NEWEST_FILE" ]; then
  echo "[kom] recap of $LEDGER/$NEWEST_FILE:"
  awk 'NR==1 {print; next}
       /RECAP|[Ww]here we left off|[Rr]ecap/ && !started {started=1; print; next}
       started { if ($0 ~ /^## /) exit; if ($0 ~ /^[[:space:]]*$/) next; print; n++; if (n >= 24) { print "  [recap cut at 24 lines: read the file]"; exit } }' \
    "$ROOT/$LEDGER/$NEWEST_FILE" \
    | while IFS= read -r line; do redact "$line"; printf '\n'; done   # a URL in the handoff prints without its credentials
fi

if [ "$REMOTE_SESSION" = 1 ]; then
  echo "[kom] cloud session: no Drive shelf on this machine — text, audit and page work only (shelf status skipped)"
else
  TOOL="$ROOT/shelf/sync_shelf.py"
  if [ ! -f "$TOOL" ]; then
    echo "[kom] shelf: no shelf/sync_shelf.py in this checkout"
  elif grep -qE '^VERSION = [0-9]+' "$TOOL" 2>/dev/null; then
    OUT=$(python3 "$TOOL" status 2>&1)
    RC=$?
    LINE=$(printf '%s\n' "$OUT" | grep -E '^SYNC\|status\|' | tail -1)
    if [ -n "$LINE" ]; then
      f=${LINE#SYNC|status|}
      f=${f%%|*}
      reg=$(printf '%s' "$LINE" | grep -oE 'registry=[0-9]+' | cut -d= -f2)
      ok=$(printf '%s' "$f" | grep -oE 'ok=[0-9]+' | cut -d= -f2)
      np=$(printf '%s' "$f" | grep -oE 'not_pulled=[0-9]+' | cut -d= -f2)
      un=$(printf '%s' "$f" | grep -oE 'unregistered=[0-9]+' | cut -d= -f2)
      pr=$(printf '%s' "$f" | grep -oE 'problems=[0-9]+' | cut -d= -f2)
      echo "[kom] shelf (local view, nothing opened on the Drive): registry ${reg:-?} files; ${ok:-?} pulled here; ${np:-?} not pulled (normal: the Drive mount serves them); ${un:-?} files here not on the shelf; problems ${pr:-?} (exit $RC)"
    else
      echo "[kom] shelf: sync_shelf.py status printed no summary (exit $RC)"
    fi
  else
    echo "[kom] shelf: this checkout's sync_shelf.py carries no VERSION line; read shelf/README.md before running it"
  fi
fi
echo "[kom] every turn ends: handoff in handoffs/ -> git add -- <paths> -> commit -> the publish line above. Read RUNBOOK.md before working."
exit 0
