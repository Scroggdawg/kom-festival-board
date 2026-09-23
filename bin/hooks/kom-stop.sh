#!/bin/bash
# kom-stop.sh — Stop and StopFailure hook of kom-festival-board.
# KOM build 1 (2026-09-23), from petrol-brand-bible's bin/hooks/petrol-stop.sh v3
# (PLAN_SETUP_v1 C6 + C7 and four Codex audit rounds); the differences are marked KOM.
#
# Wired by .claude/settings.json:
#   Stop         bash "$CLAUDE_PROJECT_DIR/bin/hooks/kom-stop.sh"
#   StopFailure  bash "$CLAUDE_PROJECT_DIR/bin/hooks/kom-stop.sh" --failure
#
# Fixed order, nothing before a step may skip a later write:
#   (1) parse the hook JSON on stdin (jq; no jq -> exit 0)
#   (2) subagent: agent_id set, or transcript_path under /subagents/   -> exit 0, nothing written
#   (3) origin is not Scroggdawg/kom-festival-board                     -> exit 0, nothing written
#   (4) measure: branch, lane, ahead, upstream, handoff numbers, this turn's handoff by name,
#       the last commit's handoff, dirty and the add words, guard
#   (5) WRITE THE SNAPSHOT  <status dir>/<session_id>.json  (temp file, then mv)
#   (6) --failure, KOM_STOP_GUARD=off, or the per-turn cap reached       -> exit 0
#   (7) main: feedback "not a working branch": no publish line; move the work to a branch, and
#       there the order of (8); never a block
#   (8) dirty or ahead: feedback in one order: (1) the handoff by its exact name, (2) git add
#       the changed files AND that handoff (named: git status ran before it exists), (3) commit,
#       (4) the publish line. Clean but ahead: nothing to add, the publish line alone, unless
#       the last commit carries no handoff. Guard count + 1. The git add line is one valid
#       shell command whatever the names and the count: past 12 paths the rest are counted on
#       the next line, a # comment. Every printed git add puts -- before its paths.
#
# KOM: the ledger is the handoffs/ directory (handoffs/handoff-NNN-<lane>.md), not the repo
# root. The next number is max + 1 over: every local and remote ref's handoffs/ tree, the
# handoffs/ directory of every other checkout of this repository on this Mac (git worktree
# list: an uncommitted handoff in a sibling worktree already holds its number), and the Drive
# ledger HANDOFFS/ under $KOM_SHELF or the one Drive mount's "My Drive/KILLER OF MEN" (the
# second ledger this repo used to keep; read only). A handoff written here whose number is
# already held elsewhere is named as a collision, with the number to take instead.
# KOM: the lane is git config kom.lane (worktree scope first), else main, else on a claude/*
# branch the suffix of this checkout's newest handoff (a guess, said so, with the config line
# that fixes it), else the branch's last path component. There is no lane-init; the publish
# line for a branch with no origin upstream is `git push -u origin HEAD`, never a rename.
#
# A branch's remote is printed (the publish warning, the snapshot's publish_warning) through
# redact: branch.<b>.remote may be a URL carrying a token.
#
# The publish line is never a bare git push and never names main as its target: only an
# upstream that is refs/remotes/origin/<x> (branch remote origin, x not main) yields
# `git push origin HEAD:<x>`; any other upstream (a local branch, another remote, main on
# any remote) yields the -u form plus a warning. Ahead is counted against the upstream only
# when it is on origin; otherwise against origin's refs (a local or backup upstream is never
# evidence that a commit is on GitHub).
#
# Feedback is {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"..."}} —
# a continuation the model reads, never decision:block. The cap is 2 per USER TURN, kept in
# <status dir>/<session_id>.guard as "<turn>:<count>": kom-prompt.sh writes "<prompt_id>:0"
# at every prompt (the reset); a Stop whose own prompt_id differs from the guard's turn is
# treated as a fresh turn too. stop_hook_active is recorded in the snapshot and is NOT an
# early return. A missing guard reads as "unknown:0" and is created. The guard is written
# BEFORE anything is emitted; if it cannot be written the hook stays silent (a cap that
# cannot be recorded counts as reached).
#
# StopFailure input carries the error type in `error`; `error_type` is read as a fallback.
# --failure only writes the snapshot, state failed:<type>.
#
# Never runs git push, add, fetch, stash, checkout, commit or merge; git runs with
# GIT_OPTIONAL_LOCKS=0, so even `git status` never refreshes or locks the index.
# Exit code is always 0.
#   KOM_STOP_GUARD=warn   a one-line systemMessage notice to the user instead of the
#                         continuation (the model gets no extra turn); still capped
#   KOM_STOP_GUARD=off    snapshot only, no feedback (per machine, no commit)
#   KOM_STATUS_DIR        snapshot + guard directory (default $HOME/.kom/status)
#   KOM_SHELF             the Drive folder (its HANDOFFS/ is read for the next number)
set -u
set -o pipefail
export GIT_OPTIONAL_LOCKS=0

MODE=stop
[ "${1:-}" = "--failure" ] && MODE=failure
GUARD_SETTING=${KOM_STOP_GUARD:-on}
CAP=2
DIR=${KOM_STATUS_DIR:-$HOME/.kom/status}
LEDGER=handoffs
# github.com over ssh or https; /git/<owner>/<repo> is the path form of a git proxy
ORIGIN_RE='(github\.com[:/]|/git/)Scroggdawg/kom-festival-board(\.git)?/?$'

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

# ---------------------------------------------------------------- (1) parse
command -v jq >/dev/null 2>&1 || exit 0
IN=$(cat 2>/dev/null) || IN=""
jf() { printf '%s' "$IN" | jq -r "$1" 2>/dev/null; }
SID=$(jf '.session_id // empty')
[ -n "$SID" ] || SID="nosession"
case "$SID" in *[!A-Za-z0-9._-]*) exit 0 ;; esac        # the id names files
PROMPT_ID=$(jf '.prompt_id // empty')
case "$PROMPT_ID" in *[!A-Za-z0-9._-]*) PROMPT_ID="" ;; esac
TRANSCRIPT=$(jf '.transcript_path // empty')
AGENT_ID=$(jf '.agent_id // empty')
STOP_HOOK_ACTIVE=$(jf 'if .stop_hook_active == true then "true" else "false" end')
[ -n "$STOP_HOOK_ACTIVE" ] || STOP_HOOK_ACTIVE=false   # empty stdin (a manual run): jq prints nothing
ERROR_TYPE=$(jf '.error // .error_type // empty')
case "$ERROR_TYPE" in *[!A-Za-z0-9._-]*) ERROR_TYPE=unrecognised ;; esac
CWD=$(jf '.cwd // empty')
[ -n "$CWD" ] || CWD=${CLAUDE_PROJECT_DIR:-$PWD}

# ---------------------------------------------------------------- (2) subagent
[ -n "$AGENT_ID" ] && exit 0
case "$TRANSCRIPT" in */subagents/*) exit 0 ;; esac

# ---------------------------------------------------------------- (3) scope
cd "$CWD" 2>/dev/null || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
ORIGIN=$(git remote get-url origin 2>/dev/null) || exit 0
shopt -s nocasematch
[[ "$ORIGIN" =~ $ORIGIN_RE ]] || exit 0
shopt -u nocasematch

# ---------------------------------------------------------------- (4) measure
ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$ROOT" || exit 0
BRANCH=$(git symbolic-ref --short -q HEAD 2>/dev/null) || BRANCH="HEAD"
UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null) || UPSTREAM=""
UPSTREAM_REF=$(git rev-parse --symbolic-full-name '@{u}' 2>/dev/null) || UPSTREAM_REF=""
UPS_REMOTE=$(git config "branch.$BRANCH.remote" 2>/dev/null) || UPS_REMOTE=""
ORIGIN_BRANCH=""
if [ "$UPS_REMOTE" = origin ]; then
  case "$UPSTREAM_REF" in refs/remotes/origin/?*) ORIGIN_BRANCH=${UPSTREAM_REF#refs/remotes/origin/} ;; esac
fi

if [ -n "$ORIGIN_BRANCH" ]; then
  AHEAD=$(git rev-list --count '@{u}..HEAD' 2>/dev/null) || AHEAD=0
else
  AHEAD=$(git rev-list --count HEAD --not --remotes=origin 2>/dev/null) || AHEAD=0
fi
case "$AHEAD" in ''|*[!0-9]*) AHEAD=0 ;; esac

# handoff numbers (KOM: the handoffs/ ledger). newest here; the max held elsewhere: every
# local and remote ref, every other checkout's handoffs/ on this Mac, and the Drive ledger.
nums() { grep -oE '^handoff-[0-9]+' | grep -oE '[0-9]+' | sort -n | tail -1; }
NEWEST_FILE=$(ls "$ROOT/$LEDGER" 2>/dev/null | grep -E '^handoff-[0-9]+' | sort -t- -k2,2n | tail -1)
LAST_HANDOFF=$(printf '%s\n' "$NEWEST_FILE" | nums)
LAST_HANDOFF=$((10#${LAST_HANDOFF:-0}))
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
COLLISION=""
if [ "$LAST_HANDOFF" -gt "$ELSEWHERE_MAX" ]; then
  NEXT_HANDOFF=$LAST_HANDOFF          # written this turn, held nowhere else
  HANDOFF_ON_DISK=1
else
  NEXT_HANDOFF=$((ELSEWHERE_MAX + 1))
  HANDOFF_ON_DISK=0
  # a handoff here that is not in HEAD's tree and whose number is held elsewhere collides
  if [ "$LAST_HANDOFF" -gt 0 ] && [ "$LAST_HANDOFF" -eq "$ELSEWHERE_MAX" ] \
     && ! git ls-tree --name-only "HEAD:$LEDGER" 2>/dev/null | grep -qE "^handoff-0*$LAST_HANDOFF([^0-9]|\$)"; then
    [ "$ELSEWHERE" = "the refs" ] && ELSEWHERE="a ref"
    COLLISION="$LEDGER/$NEWEST_FILE here is uncommitted and its number $LAST_HANDOFF is already held by $ELSEWHERE: rename it to handoff-$NEXT_HANDOFF-<lane>.md before committing"
  fi
fi
LANE=$(git config --worktree kom.lane 2>/dev/null) || LANE=""
[ -n "$LANE" ] || LANE=$(git config kom.lane 2>/dev/null) || LANE=""
LANE_HINT=""
if [ -z "$LANE" ]; then
  if [ "$BRANCH" = main ]; then
    LANE=main
  else
    case "$BRANCH" in
      claude/*)
        # KOM: the app names its branches at random; the newest handoff here names the lane
        LANE=$(printf '%s' "$NEWEST_FILE" | sed -nE 's/^handoff-[0-9]+-([A-Za-z0-9_-]+)\.md$/\1/p')
        if [ -n "$LANE" ]; then
          LANE_HINT="lane $LANE is a guess from $LEDGER/$NEWEST_FILE; fix it: git config --worktree kom.lane <lane>"
        else
          LANE_HINT="set the lane first: git config --worktree kom.lane <lane>"
        fi ;;
      *) LANE=$(basename "$BRANCH") ;;
    esac
  fi
fi
LANE_SHOWN=${LANE:-<lane>}

# publish line: never a bare git push, never a push whose target is main. Only an origin
# upstream refs/remotes/origin/<x> with x not main names its branch. Every other upstream
# gets the -u form plus a warning; no upstream gets the -u form alone (KOM: the branch keeps
# its own name on origin; there is no lane branch to rename to).
PUBLISH_WARN=""
if [ "$BRANCH" = main ]; then
  PUBLISH="(main is not a working branch: no publish line)"
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
    PUBLISH_WARN="warning: upstream $UPSTREAM_REF is $WHY; the -u form publishes this branch to origin and re-points the upstream"
  fi
fi

# this turn's handoff by its exact name: the file(s) here with the newest number when nothing
# else holds that number (written this turn), else handoffs/handoff-<next>-<lane>.md, not written yet
HANDOFF_FILES=""
# shellcheck disable=SC2010
[ "$HANDOFF_ON_DISK" = 1 ] && HANDOFF_FILES=$(ls "$ROOT/$LEDGER" 2>/dev/null | grep -E "^handoff-0*$LAST_HANDOFF([^0-9]|\$)" | sed "s|^|$LEDGER/|")
if [ -z "$HANDOFF_FILES" ]; then
  HANDOFF_ON_DISK=0
  if [ "$BRANCH" = main ]; then
    HANDOFF_FILES="$LEDGER/handoff-$NEXT_HANDOFF-<lane>.md"
  else
    HANDOFF_FILES="$LEDGER/handoff-$NEXT_HANDOFF-$LANE_SHOWN.md"
  fi
fi
HANDOFF_SHOWN=$(printf '%s' "$HANDOFF_FILES" | tr '\n' ' ')
# the handoff(s) the last commit itself adds, modifies or renames to, in the ledger. A merge
# counts only what it changed against every parent (-c): merging main borrows none of main's
# handoffs. Empty: the last commit carries no handoff.
HEAD_HANDOFF=$(git diff-tree -r -c --root -z --no-commit-id --name-only --diff-filter=ACMR HEAD 2>/dev/null \
  | tr '\0' '\n' | grep -E "^$LEDGER/handoff-[0-9]+[^/]*$" | tr '\n' ' ')
HEAD_HANDOFF=${HEAD_HANDOFF% }

# dirty = entries of git status --porcelain; -z keeps odd names intact (spaces, quotes,
# non-ASCII); a rename's source field is skipped. The add words: the first 12 paths that are
# not this turn's handoff, then the handoff by name, each shell-quoted where needed. The
# handoff is appended, never read from git status, which runs before the handoff exists.
# A name holding a control character (a newline, a tab) is quoted $'...' with \xHH escapes,
# never @sh, whose quotes would carry the newline into the text and split the add line.
STATUS_OK=true
TAB=$(printf '\t')
PORC_JQ='def hex2: "0123456789abcdef" as $d | $d[(. / 16 | floor):(. / 16 | floor) + 1] + $d[. % 16:. % 16 + 1];
  def q: if (explode | any(. < 32 or . == 127)) then
      ([39] | implode) as $sq
      | "$" + $sq + (explode | map(if . == 92 then "\\\\" elif . == 39 then "\\" + $sq
          elif . < 32 or . == 127 then "\\x" + hex2 else [.] | implode end) | join("")) + $sq
    elif test("^[A-Za-z0-9._/@%+=:,-]+$") then . else @sh end;
  ($hf | split("\n") | map(select(length > 0))) as $h
  | split("\u0000") as $f
  | [foreach range(0; $f | length) as $i ({skip: false, out: null};
       if .skip then {skip: false, out: null}
       elif ($f[$i] | length) < 4 then {skip: false, out: null}
       else ($f[$i][0:2]) as $xy | {skip: ($xy | test("^[RC]|^.[RC]")), out: $f[$i][3:]}
       end; .out) | select(. != null)] as $all
  | [$all[] | select(. as $p | $h | map(. == $p) | any | not)] as $rest
  | "\($all | length)\t\($rest | length)\t\($rest[0:12] + $h | map(q) | join(" "))"'
PORC=$(git status --porcelain -z 2>/dev/null | jq -Rrs --arg hf "$HANDOFF_FILES" "$PORC_JQ" 2>/dev/null) \
  || { STATUS_OK=false; PORC=$(printf '' | jq -Rrs --arg hf "$HANDOFF_FILES" "$PORC_JQ" 2>/dev/null) || PORC="0${TAB}0${TAB}"; }
DIRTY=${PORC%%"$TAB"*}
PORC=${PORC#*"$TAB"}
OTHERS=${PORC%%"$TAB"*}
ADD_WORDS=${PORC#*"$TAB"}
case "$DIRTY" in ''|*[!0-9]*) DIRTY=0; STATUS_OK=false ;; esac
case "$OTHERS" in ''|*[!0-9]*) OTHERS=0 ;; esac

# the per-turn guard (read here; rewritten only when feedback is emitted)
GF="$DIR/$SID.guard"
TURN=unknown; COUNT=0
if [ -s "$GF" ]; then
  line=$(head -1 "$GF" 2>/dev/null)
  TURN=${line%%:*}; COUNT=${line##*:}
fi
[ -n "$TURN" ] || TURN=unknown
case "$COUNT" in ''|*[!0-9]*) COUNT=0 ;; esac
if [ -n "$PROMPT_ID" ] && [ "$TURN" != "$PROMPT_ID" ]; then
  TURN=$PROMPT_ID; COUNT=0            # a turn the prompt hook did not record: fresh
fi

# ---------------------------------------------------------------- (5) snapshot
if [ "$MODE" = failure ]; then
  STATE="failed:${ERROR_TYPE:-unknown}"
  EVENT=StopFailure
else
  STATE=stopped
  EVENT=Stop
fi
mkdir -p "$DIR" 2>/dev/null
write_snapshot() {   # $1 = emitted (true|false), $2 = guard count after this stop
  local tmp="$DIR/$SID.json.tmp.$$"
  jq -n \
    --arg sid "$SID" --arg pid "$PROMPT_ID" --arg event "$EVENT" --arg state "$STATE" \
    --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg cwd "$CWD" --arg root "$ROOT" \
    --arg lane "$LANE" --arg branch "$BRANCH" --arg upstream "$UPSTREAM" \
    --argjson dirty "$DIRTY" --argjson ahead "$AHEAD" --argjson status_ok "$STATUS_OK" \
    --argjson last_handoff "$LAST_HANDOFF" --argjson next_handoff "$NEXT_HANDOFF" \
    --argjson elsewhere_max "$ELSEWHERE_MAX" --arg collision "$COLLISION" --argjson sha "$STOP_HOOK_ACTIVE" \
    --arg turn "$TURN" --argjson count "$2" --argjson emitted "$1" \
    --arg guard "$GUARD_SETTING" --arg publish "$PUBLISH" \
    --arg upstream_ref "$UPSTREAM_REF" --arg publish_warning "$PUBLISH_WARN" \
    '{session_id:$sid, prompt_id:$pid, hook_event:$event, state:$state, ts:$ts,
      cwd:$cwd, root:$root, lane:$lane, branch:$branch, upstream:$upstream, upstream_ref:$upstream_ref,
      dirty:$dirty, ahead:$ahead, git_status_ok:$status_ok,
      last_handoff:$last_handoff, next_handoff:$next_handoff, handoff_max_elsewhere:$elsewhere_max,
      handoff_collision:$collision, publish_line:$publish, publish_warning:$publish_warning,
      stop_hook_active:$sha,
      guard:{turn:$turn, count:$count, setting:$guard}, emitted:$emitted,
      hook:"kom-stop.sh v1 (petrol-stop.sh v3)"}' 2>/dev/null > "$tmp" \
    && mv -f "$tmp" "$DIR/$SID.json" 2>/dev/null
  rm -f "$tmp" 2>/dev/null
}
write_snapshot false "$COUNT"

# ---------------------------------------------------------------- (6) returns
[ "$MODE" = failure ] && exit 0
[ -s "$GF" ] || { printf '%s:%s\n' "$TURN" "$COUNT" > "$GF"; } 2>/dev/null   # a missing guard is created
[ "$GUARD_SETTING" = off ] && exit 0
[ "$COUNT" -ge "$CAP" ] && exit 0

emit() {   # $1 = context|notice, $2 = the text. The guard is bumped FIRST; no guard, no output.
  local n=$((COUNT + 1))
  if ! { printf '%s:%s\n' "$TURN" "$n" > "$GF.tmp.$$" && mv -f "$GF.tmp.$$" "$GF"; } 2>/dev/null; then
    rm -f "$GF.tmp.$$" 2>/dev/null
    exit 0
  fi
  write_snapshot true "$n"
  if [ "$1" = notice ]; then
    jq -nc --arg m "$2" '{systemMessage:$m}'
  else
    jq -nc --arg ctx "$2" '{hookSpecificOutput:{hookEventName:"Stop", additionalContext:$ctx}}'
  fi
}

# ---------------------------------------------------------------- (7) main
# main is not a working branch: no publish line, never a block. The reminder is to move the
# work to a branch of its own (git switch -c keeps the uncommitted changes); there, the order
# of (8): the handoff, git add with the handoff, commit, publish.
if [ "$BRANCH" = main ]; then
  if [ "$DIRTY" -gt 0 ] || [ "$AHEAD" -gt 0 ]; then
    if [ "$HANDOFF_ON_DISK" = 1 ]; then
      MAIN_H="$HANDOFF_SHOWN is written here and on no ref yet: carry it with the change, recap current"
    else
      MAIN_H="write $HANDOFF_FILES (recap first, newest first; $NEXT_HANDOFF = max over the refs, the other checkouts and the Drive ledger + 1)"
    fi
    if [ "$GUARD_SETTING" = warn ]; then
      emit notice "[kom-stop] main is not a working branch (dirty:$DIRTY ahead:$AHEAD); move the work to a branch: git switch -c <lane>; there, in order: $HANDOFF_SHOWN, git add -- <the changes> $HANDOFF_SHOWN, commit, publish with the -u form the hook prints there  (notice $((COUNT + 1)) of $CAP this turn; KOM_STOP_GUARD=warn)"
    else
      emit context "[kom-stop] main is not a working branch; move the work to a branch of its own.
dirty:$DIRTY ahead:$AHEAD on main (the main checkout may carry another session's files: check git status before touching anything).
1. git switch -c <lane>   (keeps the unsaved changes; a new branch off main)
2. on the branch: $MAIN_H
3. on the branch: git add -- <the changed files> $HANDOFF_SHOWN
4. on the branch: git commit -m \"<lane>: <what changed>\"
5. on the branch: publish with the -u form the hook prints there, never from main
No publish line on main; Luke merges branches into main. Nudge $((COUNT + 1)) of $CAP this turn. Nothing was pushed, added or stashed by this hook."
    fi
  fi
  exit 0
fi

# ---------------------------------------------------------------- (8) outstanding work
if [ "$DIRTY" -gt 0 ] || [ "$AHEAD" -gt 0 ]; then
  UPS_SHOWN=${UPSTREAM:-none}
  [ -z "$ORIGIN_BRANCH" ] && [ -n "$UPSTREAM_REF" ] && UPS_SHOWN=$UPSTREAM_REF
  if [ "$AHEAD" -eq 1 ]; then NCOMMITS="1 commit"; else NCOMMITS="$AHEAD commits"; fi
  PUBLISH_ONLY=0
  [ "$DIRTY" -eq 0 ] && [ -n "$HEAD_HANDOFF" ] && PUBLISH_ONLY=1
  if [ "$HANDOFF_ON_DISK" = 1 ]; then
    HSTEP="$HANDOFF_SHOWN is written and on no ref yet: keep its recap current (newest first)"
  else
    HSTEP="write $HANDOFF_FILES (recap first, newest first; $NEXT_HANDOFF = max over the refs, the other checkouts and the Drive ledger + 1)"
  fi
  if [ "$GUARD_SETTING" = warn ]; then
    if [ "$PUBLISH_ONLY" = 1 ]; then
      SAY="nothing to add; $NCOMMITS not yet on GitHub; publish with: $PUBLISH"
    elif [ "$DIRTY" -gt 0 ]; then
      SAY="${HSTEP%% (*}, git add -- <the changes> $HANDOFF_SHOWN, commit, then: $PUBLISH"
    else
      SAY="the last commit carries no handoff: ${HSTEP%% (*}, git add -- $HANDOFF_SHOWN, commit, then: $PUBLISH"
    fi
    emit notice "[kom-stop] unpublished work on $BRANCH: dirty:$DIRTY ahead:$AHEAD upstream:$UPS_SHOWN — $SAY${PUBLISH_WARN:+ ($PUBLISH_WARN)}${COLLISION:+ ($COLLISION)}  (notice $((COUNT + 1)) of $CAP this turn; KOM_STOP_GUARD=warn)"
    exit 0
  fi
  if [ "$PUBLISH_ONLY" = 1 ]; then
    TEXT="[kom-stop] unpublished work on $BRANCH ($LANE_SHOWN): dirty:$DIRTY ahead:$AHEAD upstream:$UPS_SHOWN.
nothing to add; $NCOMMITS not yet on GitHub; publish with: $PUBLISH
   (the last commit carries $HEAD_HANDOFF)"
  else
    WHY=""
    [ "$DIRTY" -eq 0 ] && WHY="; the last commit ($(git rev-parse --short HEAD 2>/dev/null)) carries no handoff"
    # -- ends git's options: a path named -e or --all is added, never read as an option
    ADDLINE="git add -- $ADD_WORDS"
    # past 12 paths the rest are counted on a line of their own, a # comment, so the add line
    # stays one valid shell command (bash -n) however many paths there are
    [ "$OTHERS" -gt 12 ] && ADDLINE="$ADDLINE
   # + $((OTHERS - 12)) more not listed: git status --porcelain"
    COMMITLINE="git commit -m \"$LANE_SHOWN: <what changed>\""
    TEXT="[kom-stop] unpublished work on $BRANCH ($LANE_SHOWN): dirty:$DIRTY ahead:$AHEAD upstream:$UPS_SHOWN$WHY. End the turn with, in this order:
1. $HSTEP
2. $ADDLINE
3. $COMMITLINE
4. $PUBLISH"
  fi
  [ -n "$PUBLISH_WARN" ] && TEXT="$TEXT
   ($PUBLISH_WARN)"
  [ -n "$COLLISION" ] && TEXT="$TEXT
   ($COLLISION)"
  [ -n "$LANE_HINT" ] && TEXT="$TEXT
   ($LANE_HINT)"
  TEXT="$TEXT
Nudge $((COUNT + 1)) of $CAP this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"
  emit context "$TEXT"
fi
exit 0
