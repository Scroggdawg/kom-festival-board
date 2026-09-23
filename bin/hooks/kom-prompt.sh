#!/bin/bash
# kom-prompt.sh — UserPromptSubmit hook of kom-festival-board (KOM build 1, from
# petrol-brand-bible's bin/hooks/petrol-prompt.sh v1).
# Wired by .claude/settings.json as  bash "$CLAUDE_PROJECT_DIR/bin/hooks/kom-prompt.sh"
#
# Writes two machine-local files under $HOME/.kom/status/ (or $KOM_STATUS_DIR, the same
# variable kom-stop.sh and bin/kom-status.py read) and nothing else:
#   <session_id>.guard  "<prompt_id>:0"  — the per-turn RESET of kom-stop.sh's cap
#                       (the cap is per user turn; every prompt starts a fresh turn id
#                       with count 0)
#   <session_id>.json   state=working, ts, cwd — a heuristic with false positives;
#                       bin/kom-status.py never trusts it alone: it can only demote a
#                       checkout to `working`.
#
# Without this file the cap would be per session, not per turn. kom-stop.sh also treats a
# Stop whose prompt_id differs from the guard's turn as a fresh turn, so a missed prompt
# write cannot pin the cap.
#
# Prints nothing (a UserPromptSubmit hook's stdout would become model context).
# Never blocks, never exits non-zero, never touches git. Cloud sessions run it too;
# without jq it does nothing.
set -u

command -v jq >/dev/null 2>&1 || exit 0
IN=$(cat 2>/dev/null) || IN=""
[ -n "$IN" ] || exit 0

jf() { printf '%s' "$IN" | jq -r "$1" 2>/dev/null; }
SID=$(jf '.session_id // empty')
[ -n "$SID" ] || exit 0
case "$SID" in *[!A-Za-z0-9._-]*) exit 0 ;; esac    # the session id names files here

PROMPT_ID=$(jf '.prompt_id // empty')
[ -n "$PROMPT_ID" ] || PROMPT_ID="t$(date -u +%s)-$$"   # older CLIs: a fresh id per prompt
case "$PROMPT_ID" in *[!A-Za-z0-9._-]*) PROMPT_ID="t$(date -u +%s)-$$" ;; esac
CWD=$(jf '.cwd // empty')
[ -n "$CWD" ] || CWD=${CLAUDE_PROJECT_DIR:-$PWD}

DIR=${KOM_STATUS_DIR:-$HOME/.kom/status}
mkdir -p "$DIR" 2>/dev/null || exit 0

# 1. the guard: fresh turn, count 0 (temp file, then mv)
printf '%s:0\n' "$PROMPT_ID" 2>/dev/null > "$DIR/$SID.guard.tmp.$$" \
  && mv -f "$DIR/$SID.guard.tmp.$$" "$DIR/$SID.guard" 2>/dev/null
rm -f "$DIR/$SID.guard.tmp.$$" 2>/dev/null

# 2. the snapshot: state=working (merged into the Stop hook's file when one exists)
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
if [ -s "$DIR/$SID.json" ]; then
  jq --arg ts "$TS" --arg cwd "$CWD" --arg pid "$PROMPT_ID" \
     '.state = "working" | .ts = $ts | .cwd = (.cwd // $cwd) | .prompt_id = $pid' \
     "$DIR/$SID.json" 2>/dev/null > "$DIR/$SID.json.tmp.$$"
else
  jq -n --arg sid "$SID" --arg ts "$TS" --arg cwd "$CWD" --arg pid "$PROMPT_ID" \
     '{session_id: $sid, state: "working", ts: $ts, cwd: $cwd, prompt_id: $pid, hook: "kom-prompt.sh v1"}' \
     2>/dev/null > "$DIR/$SID.json.tmp.$$"
fi
if [ -s "$DIR/$SID.json.tmp.$$" ]; then
  mv -f "$DIR/$SID.json.tmp.$$" "$DIR/$SID.json" 2>/dev/null
else
  rm -f "$DIR/$SID.json.tmp.$$" 2>/dev/null
fi
exit 0
