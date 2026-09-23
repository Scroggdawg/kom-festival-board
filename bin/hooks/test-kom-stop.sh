#!/bin/bash
# test-kom-stop.sh — falsification harness for kom-stop.sh, kom-prompt.sh, kom-session-start.sh,
# bin/kom-status.py, bin/kom-check.sh's redact and bin/githooks/pre-commit (KOM build 1, from
# petrol-brand-bible's bin/hooks/test-petrol-stop.sh).
#
#   bash bin/hooks/test-kom-stop.sh [--record bin/hooks/FALSIFY-kom-stop.md]
#
# --record also runs the mutant suite (a control copy with no defect, which must pass, then
# copies of the hooks and scripts, each with one known defect; the harness must exit 1 on
# every one) and writes the record with a header read back out of the transcript.
#
# Every case feeds the hook a synthetic hook JSON on stdin and reads the exit code on its
# own line. Scratch only: repos under $TMPDIR with a never-contacted origin URL, HOME,
# KOM_STATUS_DIR and KOM_SHELF redirected into the scratch directory, so nothing in this
# checkout, in the real $HOME/.kom, on the Drive, or on any remote is touched. The hook runs
# behind a git shim that logs every git call and refuses push/add/stash/checkout/commit/
# merge/fetch/pull/reset/rm (exit 99), so "the hook never runs those" is measured, not
# asserted. The harness's own repo setup runs with the real git.
#
# Cases 1-6: clean+pushed, dirty tree, unpushed commits, subagent, main, and the cap resetting
# on a new turn. Then: a foreign origin, no upstream, upstream=origin/main on a non-main
# branch, claude/* with and without kom.lane (the lane guessed from the newest handoff),
# KOM_STOP_GUARD off|warn, --failure, an unwritable status directory (fail closed), path names
# that need shell quoting, the origin URL forms, the publish line by upstream form in both
# hooks (no line ever targets main), the handoff number over refs, a sibling worktree's
# uncommitted handoff and the Drive ledger (KOM), the collision note (KOM), the git add line
# as one valid shell command, paths named like options, the multi-turn sequence, the git shim
# tally, kom-status.py's state transitions and its "saved to GitHub" evidence, one set of URLs
# through every redactor, a token never printed, settings.json, the session-start cloud line,
# and the pre-commit guard in a scratch repo (KOM).
# Exit 0 when every check passes, 1 otherwise.
set -u

HERE=$(cd "$(dirname "$0")" && pwd)
SELF="$HERE/$(basename "$0")"
HOOK="$HERE/kom-stop.sh"
PROMPT_HOOK="$HERE/kom-prompt.sh"
SESSION_HOOK="$HERE/kom-session-start.sh"
SETTINGS="$HERE/../../.claude/settings.json"
STATUS_PY="$HERE/../kom-status.py"
CHECK_SH="$HERE/../kom-check.sh"
PRECOMMIT="$HERE/../githooks/pre-commit"
RECORD=""
[ "${1:-}" = "--record" ] && RECORD=${2:?--record needs a path}

REAL_HOME=$HOME
REAL_GIT=$(command -v git)
S=$(mktemp -d "${TMPDIR:-/tmp}/kom-stop-test.XXXXXX") || exit 2
S=$(cd "$S" && pwd -P)
export HOME="$S/home"
mkdir -p "$HOME"
export KOM_STATUS_DIR="$HOME/.kom/status"
export KOM_SHELF="$S/no-shelf"       # no Drive ledger unless a case makes one
unset KOM_STOP_GUARD CLAUDE_CODE_REMOTE
export PYTHONDONTWRITEBYTECODE=1
SHIM_LOG="$S/git-shim.log"
export GIT_SHIM_LOG="$SHIM_LOG"
mkdir -p "$S/bin"
cat > "$S/bin/git" <<EOF
#!/bin/bash
printf '%s\n' "\$*" >> "\$GIT_SHIM_LOG"
case "\${1:-}" in
  push|add|stash|checkout|commit|merge|fetch|pull|reset|rm|rebase|switch|restore|clean)
    echo "FORBIDDEN: git \$1 (called by the hook)" >&2; exit 99 ;;
esac
exec "$REAL_GIT" "\$@"
EOF
chmod +x "$S/bin/git"
# kom-status.py's git: every call logged; "git fetch ... origin" is served from the scratch
# bare repository $FAKE_GITHUB standing in for GitHub; the origin URL is never contacted.
export STATUS_GIT_LOG="$S/status-git.log"
mkdir -p "$S/statusbin"
cat > "$S/statusbin/git" <<EOF
#!/bin/bash
printf '%s\n' "\$*" >> "\$STATUS_GIT_LOG"
if [ "\${1:-}" = fetch ]; then
  shift
  flags=(); where=""
  for a in "\$@"; do case "\$a" in -*) flags+=("\$a") ;; *) where="\$a" ;; esac; done
  if [ "\${FAKE_FETCH:-ok}" = fail ]; then
    echo "fatal: unable to access 'https://github.com/Scroggdawg/kom-festival-board.git/': Could not resolve host: github.com" >&2
    exit 128
  fi
  if [ -n "\${FAKE_FETCH_ERR:-}" ]; then printf '%s\n' "\$FAKE_FETCH_ERR" >&2; exit 128; fi
  [ "\$where" = origin ] || { echo "statusbin shim: only 'git fetch ... origin' is served (got '\$where')" >&2; exit 97; }
  exec "$REAL_GIT" fetch "\${flags[@]}" "\$FAKE_GITHUB" '+refs/heads/*:refs/remotes/origin/*'
fi
exec "$REAL_GIT" "\$@"
EOF
chmod +x "$S/statusbin/git"

PASS=0; FAIL=0
ok()   { PASS=$((PASS + 1)); echo "  PASS  $1"; }
bad()  { FAIL=$((FAIL + 1)); echo "  FAIL  $1"; }
check() { local d=$1; shift; if "$@" >/dev/null 2>&1; then ok "$d"; else bad "$d"; fi; }
contains() { printf '%s' "$1" | grep -qF -- "$2"; }
not_contains() { ! printf '%s' "$1" | grep -qF -- "$2"; }
no_bare_push() { ! printf '%s\n' "$1" | grep -qE 'git push[[:space:]]*$'; }
is_empty() { [ -z "$1" ]; }
file_absent() { [ ! -e "$1" ]; }
ctx() { printf '%s' "$1" | jq -r '.hookSpecificOutput.additionalContext // empty' 2>/dev/null; }
sysmsg() { printf '%s' "$1" | jq -r '.systemMessage // empty' 2>/dev/null; }
scrub() { sed -e "s#/private$S#\$SCRATCH#g" -e "s#$S#\$SCRATCH#g" -e "s#$REAL_HOME#\$HOME#g"; }

G="$REAL_GIT -c user.name=test -c user.email=test@example.invalid -c commit.gpgsign=false"
ORIGIN_URL=https://github.com/Scroggdawg/kom-festival-board.git
mkrepo() { # name branch upstream-branch|none  -> prints the path
  local d="$S/$1"
  mkdir -p "$d"
  ( cd "$d" \
    && $G init -q -b "$2" \
    && printf 'a\n' > a.txt && $G add a.txt && $G commit -q -m init \
    && $G remote add origin "$ORIGIN_URL" \
    && if [ "$3" != none ]; then
         $G update-ref "refs/remotes/origin/$3" HEAD \
         && $G config "branch.$2.remote" origin \
         && $G config "branch.$2.merge" "refs/heads/$3"
       fi ) || { echo "mkrepo $1 failed"; exit 2; }
  printf '%s' "$d"
}
mkgithub() { # name repo [branch...] -> a scratch bare repository standing in for GitHub
  local d="$S/$1.git" src=$2 b
  shift 2
  "$REAL_GIT" init -q --bare "$d" || { echo "mkgithub $1 failed"; exit 2; }
  for b in "$@"; do
    "$REAL_GIT" --git-dir="$d" fetch -q "$src" "refs/heads/$b:refs/heads/$b" || { echo "mkgithub $1 $b failed"; exit 2; }
  done
  printf '%s' "$d"
}
ledger_tree() { # repo base-tree name... -> a tree = base-tree plus handoffs/<name> (each holding "h")
  local r=$1 base=$2 sub lines=""
  shift 2
  ( cd "$r" && bh=$(printf 'h\n' | $G hash-object -w --stdin) \
    && for n in "$@"; do lines="$lines$(printf '100644 blob %s\t%s' "$bh" "$n")
"; done \
    && sub=$(printf '%s' "$lines" | $G mktree) \
    && { $G ls-tree "$base" | grep -v $'\thandoffs$'; printf '040000 tree %s\thandoffs\n' "$sub"; } | $G mktree )
}
mkin() { # sid prompt_id cwd transcript stop_hook_active(true|false) [agent_id] [error]
  jq -nc --arg sid "$1" --arg pid "$2" --arg cwd "$3" --arg tp "$4" --argjson sha "$5" \
     --arg aid "${6:-}" --arg er "${7:-}" \
     '({session_id:$sid, prompt_id:$pid, cwd:$cwd, transcript_path:$tp, hook_event_name:"Stop",
        stop_hook_active:$sha, permission_mode:"default"}
       + (if $aid != "" then {agent_id:$aid} else {} end)) as $base
      | if $er != "" then ($base + {error:$er, error_details:"synthetic", hook_event_name:"StopFailure"}) | del(.stop_hook_active)
        else $base end'
}
run_hook() { # json [hook args...]  -> sets OUT and RC; prints both
  local json=$1; shift
  OUT=$(printf '%s' "$json" | PATH="$S/bin:$PATH" bash "$HOOK" "$@" 2>"$S/stderr.txt")
  RC=$?
  echo "  stdout: $(printf '%s' "$OUT" | scrub | head -c 1500)"
  echo "  exit:"
  echo "  $RC"
  if [ -s "$S/stderr.txt" ]; then echo "  stderr: $(scrub < "$S/stderr.txt" | head -c 400)"; fi
  cat "$S/stderr.txt" >> "$S/stderr-all.txt" 2>/dev/null
}
run_prompt() { # json -> RC
  printf '%s' "$1" | bash "$PROMPT_HOOK" >/dev/null 2>&1
  RC=$?
  echo "  kom-prompt.sh exit:"
  echo "  $RC"
}
run_session() { # cwd [env assignments...] -> OUT RC
  local cwd=$1; shift
  OUT=$(jq -nc --arg cwd "$cwd" '{session_id:"s-ss", cwd:$cwd, hook_event_name:"SessionStart", source:"startup"}' \
        | env "$@" KOM_SESSION_NO_FETCH=1 PATH="$S/bin:$PATH" bash "$SESSION_HOOK" 2>&1)
  RC=$?
}
guard() { cat "$KOM_STATUS_DIR/$1.guard" 2>/dev/null || echo "(no guard file)"; }
snap()  { jq -c "$2" "$KOM_STATUS_DIR/$1.json" 2>/dev/null || echo "(no snapshot)"; }
add_args() { # the "2. git add ..." line evaluated as shell words, joined by | (or by $2)
  local l sep='|'
  [ "$#" -ge 2 ] && sep=$2
  l=$(printf '%s\n' "$1" | sed -n 's/^2\. git add //p' | head -1)
  ( eval "set -- $l" 2>/dev/null && IFS=$sep && printf '%s' "$*" )
}
add_line() { printf '%s\n' "$1" | sed -n '/^2\. git add /{s/^2\. //p;q;}'; }
note_line() { printf '%s\n' "$1" | sed -n '/^2\. git add /{n;p;q;}'; }
add_line_parses() {
  add_line "$1" > "$S/add-line.sh"
  [ -s "$S/add-line.sh" ] && bash -n "$S/add-line.sh"
}
steps() { printf '%s\n' "$1" | sed -n 's/^\([0-9][0-9]*\)\. .*/\1/p' | tr '\n' ' ' | sed 's/ $//'; }
in_order() { # text needle...: every needle occurs, each one after the previous one's first occurrence
  local t=$1 n
  shift
  for n in "$@"; do
    case "$t" in *"$n"*) t=${t#*"$n"} ;; *) return 1 ;; esac
  done
}
leads() { # text first other...: every needle occurs, and first occurs before any of the others
  local t=$1 a=$2 b pa
  shift 2
  case "$t" in *"$a"*) pa=${t%%"$a"*} ;; *) return 1 ;; esac
  for b in "$@"; do
    case "$pa" in *"$b"*) return 1 ;; esac
    case "$t" in *"$b"*) ;; *) return 1 ;; esac
  done
}
TP="$HOME/.claude/projects/x/session.jsonl"
H=handoffs

main() {
  echo "test-kom-stop.sh — $(date -u +%Y-%m-%dT%H:%M:%SZ) — bash $BASH_VERSION — $(jq --version) — $($REAL_GIT --version)"
  echo "hook: $(shasum -a 256 "$HOOK" | cut -c1-12)  prompt hook: $(shasum -a 256 "$PROMPT_HOOK" | cut -c1-12)  session hook: $(shasum -a 256 "$SESSION_HOOK" | cut -c1-12)  status: $(shasum -a 256 "$STATUS_PY" | cut -c1-12)  check: $(shasum -a 256 "$CHECK_SH" | cut -c1-12)  pre-commit: $(shasum -a 256 "$PRECOMMIT" | cut -c1-12)  harness: $(shasum -a 256 "$SELF" | cut -c1-12)"
  echo "scratch: \$SCRATCH (under \$TMPDIR); HOME, KOM_STATUS_DIR and KOM_SHELF redirected there; git shim refuses write verbs"
  local r u i

  echo "== case 1: clean + pushed (work/t-clean == origin/work/t-clean, tree clean) — expect silence, snapshot stopped =="
  r=$(mkrepo clean work/t-clean work/t-clean)
  run_hook "$(mkin s-clean p1 "$r" "$TP" false)"
  check "exit 0" [ "$RC" -eq 0 ]
  check "no output" is_empty "$OUT"
  check "snapshot state=stopped dirty=0 ahead=0 emitted=false" [ "$(snap s-clean '[.state,.dirty,.ahead,.emitted]')" = '["stopped",0,0,false]' ]
  check "guard created as p1:0" [ "$(guard s-clean)" = "p1:0" ]
  check "lane from the branch's last component" [ "$(snap s-clean '.lane')" = '"t-clean"' ]
  echo "  snapshot: $(snap s-clean '{state,lane,branch,upstream,dirty,ahead,publish_line,guard}')"

  echo "== case 2: dirty tree (one modified, one untracked) — expect the four lines in order: 1. write handoffs/handoff-1-t-dirty.md, 2. git add -- a.txt b.txt handoffs/handoff-1-t-dirty.md (named though it does not exist yet), 3. git commit, 4. git push origin HEAD:work/t-dirty; nudge 1 of 2 =="
  r=$(mkrepo dirty work/t-dirty work/t-dirty)
  printf 'b\n' >> "$r/a.txt"; printf 'new\n' > "$r/b.txt"
  run_hook "$(mkin s-dirty p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  check "exit 0" [ "$RC" -eq 0 ]
  check "valid Stop feedback JSON" [ "$(printf '%s' "$OUT" | jq -r '.hookSpecificOutput.hookEventName' 2>/dev/null)" = "Stop" ]
  check "names a.txt and b.txt for git add, after --" contains "$C" "git add -- a.txt b.txt"
  check "1. write handoffs/handoff-1-t-dirty.md (no ref holds a handoff: next is 1)" contains "$C" "1. write $H/handoff-1-t-dirty.md ("
  check "the handoff does not exist yet" file_absent "$r/$H/handoff-1-t-dirty.md"
  check "2. git add: --, the changed files, then the not-yet-written handoff by name" [ "$(add_args "$C")" = "--|a.txt|b.txt|$H/handoff-1-t-dirty.md" ]
  check "the git add line alone through bash -n: one valid shell command" add_line_parses "$C"
  check "the steps are numbered 1 2 3 4" [ "$(steps "$C")" = "1 2 3 4" ]
  check "in order: the handoff, git add, git commit, git push" in_order "$C" "1. write $H/handoff-1-t-dirty.md" "2. git add" "3. git commit" "4. git push origin HEAD:work/t-dirty"
  check "no git add, commit or push before the handoff" leads "$C" "$H/handoff-1-t-dirty.md" "git add" "git commit" "git push"
  check "publish line names the upstream branch" contains "$C" "git push origin HEAD:work/t-dirty"
  check "never a bare git push" no_bare_push "$C"
  check "nudge 1 of 2" contains "$C" "Nudge 1 of 2"
  check "guard bumped to p1:1" [ "$(guard s-dirty)" = "p1:1" ]
  check "snapshot dirty=2 emitted=true" [ "$(snap s-dirty '[.dirty,.emitted]')" = '[2,true]' ]
  printf '%s\n' "$C" | scrub | sed 's/^/  ctx| /'

  echo "== case 3: clean but ahead of origin/work/t-ahead — (a) the last commit carries handoffs/handoff-1-t-ahead.md: nothing to add, 1 commit not yet on GitHub, the publish line alone; (b) the last commit carries none: the handoff first, alone to add; (c) a merge of main that brings another lane's handoff carries none of its own =="
  r=$(mkrepo ahead work/t-ahead work/t-ahead)
  ( cd "$r" && printf 'c\n' > c.txt && mkdir -p $H && printf 'h\n' > $H/handoff-1-t-ahead.md && $G add c.txt $H/handoff-1-t-ahead.md && $G commit -q -m second )
  run_hook "$(mkin s-ahead p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  check "exit 0" [ "$RC" -eq 0 ]
  check "reports ahead:1 dirty:0" contains "$C" "dirty:0 ahead:1"
  check "publish line" contains "$C" "git push origin HEAD:work/t-ahead"
  check "never a bare git push" no_bare_push "$C"
  check "a: nothing to add; 1 commit not yet on GitHub; publish with: <the line>" contains "$C" "nothing to add; 1 commit not yet on GitHub; publish with: git push origin HEAD:work/t-ahead"
  check "a: names the handoff the last commit carries" contains "$C" "(the last commit carries $H/handoff-1-t-ahead.md)"
  check "a: no handoff demanded" not_contains "$C" "write $H"
  check "a: no git add, no git commit" [ -z "$(printf '%s\n' "$C" | grep -E 'git (add|commit)')" ]
  printf '%s\n' "$C" | scrub | sed 's/^/  ctx| /'
  OUT=$(mkin s-ahead-w p1 "$r" "$TP" false | KOM_STOP_GUARD=warn PATH="$S/bin:$PATH" bash "$HOOK")
  RC=$?
  echo "  a, warn: $(sysmsg "$OUT" | scrub)"; echo "  exit:"; echo "  $RC"
  check "a, warn: nothing to add; 1 commit not yet on GitHub; publish with: <the line>" contains "$(sysmsg "$OUT")" "nothing to add; 1 commit not yet on GitHub; publish with: git push origin HEAD:work/t-ahead"
  ( cd "$r" && printf 'd\n' > d.txt && $G add d.txt && $G commit -q -m third )
  run_hook "$(mkin s-ahead2 p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  check "b: reports dirty:0 ahead:2" contains "$C" "dirty:0 ahead:2"
  check "b: says the last commit carries no handoff" contains "$C" "carries no handoff"
  check "b: 1. write handoffs/handoff-2-t-ahead.md (a local ref holds 1: next is 2)" contains "$C" "1. write $H/handoff-2-t-ahead.md ("
  check "b: 2. git add names the handoff alone, after --" [ "$(add_args "$C")" = "--|$H/handoff-2-t-ahead.md" ]
  check "b: the git add line alone through bash -n" add_line_parses "$C"
  check "b: the steps are numbered 1 2 3 4" [ "$(steps "$C")" = "1 2 3 4" ]
  check "b: in order: the handoff, git add, git commit, git push" in_order "$C" "1. write $H/handoff-2-t-ahead.md" "2. git add" "3. git commit" "4. git push origin HEAD:work/t-ahead"
  check "b: never 'nothing to add' after asking for a handoff" not_contains "$C" "nothing to add"
  printf '%s\n' "$C" | scrub | sed 's/^/  ctx| /'
  OUT=$(mkin s-ahead2-w p1 "$r" "$TP" false | KOM_STOP_GUARD=warn PATH="$S/bin:$PATH" bash "$HOOK")
  RC=$?
  echo "  b, warn: $(sysmsg "$OUT" | scrub)"; echo "  exit:"; echo "  $RC"
  check "b, warn: the handoff alone to add, after --" contains "$(sysmsg "$OUT")" "git add -- $H/handoff-2-t-ahead.md, commit, then: git push origin HEAD:work/t-ahead"
  r=$(mkrepo merge work/t-merge work/t-merge)
  # a merge made with plumbing (no git merge): origin/main gains handoffs/handoff-7-hub.md, the
  # lane merges it cleanly, the working tree and index follow the merge
  ( cd "$r" && th=$(ledger_tree "$r" HEAD handoff-7-hub.md) \
    && cm=$($G commit-tree "$th" -p HEAD -m 'main: handoff-7-hub') \
    && $G update-ref refs/remotes/origin/main "$cm" \
    && cx=$($G commit-tree "$th" -p HEAD -p "$cm" -m 'merge origin/main') \
    && $G update-ref refs/heads/work/t-merge "$cx" \
    && mkdir -p $H && printf 'h\n' > $H/handoff-7-hub.md && $G add $H/handoff-7-hub.md ) || { echo "merge setup failed"; exit 2; }
  echo "  c: git status --porcelain after the merge: '$(cd "$r" && $REAL_GIT status --porcelain)'; parents of HEAD: $(( $(cd "$r" && $REAL_GIT rev-list --parents -1 HEAD | wc -w) - 1 ))"
  run_hook "$(mkin s-merge p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  check "c: a clean merge, 2 ahead (dirty:0 ahead:2)" contains "$C" "dirty:0 ahead:2"
  check "c: main's handoff-7-hub.md is not the merge's own: carries no handoff" contains "$C" "carries no handoff"
  check "c: 1. write handoffs/handoff-8-t-merge.md (refs hold 7: next is 8)" contains "$C" "1. write $H/handoff-8-t-merge.md ("
  printf '%s\n' "$C" | sed -n '1,3p' | scrub | sed 's/^/  ctx| /'

  echo "== case 4: subagent (transcript under /subagents/, dirty repo) — expect silence and NO snapshot or guard written =="
  r="$S/dirty"
  run_hook "$(mkin s-sub p1 "$r" "$HOME/.claude/projects/x/subagents/agent-1.jsonl" false)"
  check "exit 0" [ "$RC" -eq 0 ]
  check "no output" is_empty "$OUT"
  check "no snapshot written" file_absent "$KOM_STATUS_DIR/s-sub.json"
  check "no guard written" file_absent "$KOM_STATUS_DIR/s-sub.guard"
  run_hook "$(mkin s-sub2 p1 "$r" "$TP" false agent-abc)"
  check "agent_id variant: exit 0" [ "$RC" -eq 0 ]
  check "agent_id variant: no output" is_empty "$OUT"
  check "agent_id variant: no snapshot" file_absent "$KOM_STATUS_DIR/s-sub2.json"
  check "agent_id variant: no guard" file_absent "$KOM_STATUS_DIR/s-sub2.guard"

  echo "== case 5: main branch, dirty, then clean but ahead — expect 'main is not a working branch', no publish line, move the work to a branch and there the handoff first; never a block =="
  r=$(mkrepo main main main)
  printf 'x\n' >> "$r/a.txt"
  run_hook "$(mkin s-main p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  check "exit 0" [ "$RC" -eq 0 ]
  check "says main is not a working branch" contains "$C" "main is not a working branch"
  check "no git push line on main" not_contains "$C" "git push"
  check "feedback, never decision:block" [ "$(printf '%s' "$OUT" | jq -r '.decision // "none"')" = "none" ]
  check "snapshot branch=main lane=main" [ "$(snap s-main '[.branch,.lane]')" = '["main","main"]' ]
  check "reminds: move the work to a branch, git switch -c <lane>" in_order "$C" "move the work to a branch" "1. git switch -c <lane>"
  check "says no publish line on main" contains "$C" "No publish line on main"
  check "the steps are numbered 1 to 5" [ "$(steps "$C")" = "1 2 3 4 5" ]
  check "on the branch, in order: write handoffs/handoff-1-<lane>.md, git add -- with it, git commit, publish" \
    in_order "$C" "2. on the branch: write $H/handoff-1-<lane>.md" "3. on the branch: git add -- <the changed files> $H/handoff-1-<lane>.md" "4. on the branch: git commit" "5. on the branch: publish"
  check "no git add, commit or publish before the handoff" leads "$C" "$H/handoff-1-<lane>.md" "git add" "commit" "publish"
  check "snapshot publish_line: main has none" [ "$(snap s-main '.publish_line')" = '"(main is not a working branch: no publish line)"' ]
  printf '%s\n' "$C" | scrub | sed 's/^/  ctx| /'
  ( cd "$r" && $G commit -q -am 'on main' )
  run_hook "$(mkin s-main2 p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  echo "  clean but ahead on main: $(printf '%s\n' "$C" | sed -n 2p | scrub)"
  check "main, clean but ahead: dirty:0 ahead:1, still not a working branch" in_order "$C" "main is not a working branch" "dirty:0 ahead:1 on main"
  check "main, clean but ahead: no git push, no 'publish with:'" [ -z "$(printf '%s\n' "$C" | grep -E 'git push|publish with:')" ]
  check "main, clean but ahead: the handoff still leads" leads "$C" "$H/handoff-1-<lane>.md" "git add" "commit" "publish"

  echo "== case 6: the cap resets on a new turn — guard seeded at the cap, then a new prompt =="
  r="$S/dirty"
  printf 'T1:2\n' > "$KOM_STATUS_DIR/s-reset.guard"
  run_hook "$(mkin s-reset T1 "$r" "$TP" true)"
  echo "  guard after a Stop in the capped turn T1: $(guard s-reset)"
  check "capped turn T1: silent" is_empty "$OUT"
  check "capped turn T1: guard stays T1:2" [ "$(guard s-reset)" = "T1:2" ]
  check "capped turn T1: snapshot still written, count 2" [ "$(snap s-reset '.guard.count')" = "2" ]
  PJ=$(jq -nc --arg cwd "$r" '{session_id:"s-reset", prompt_id:"T2", cwd:$cwd, hook_event_name:"UserPromptSubmit", prompt:"next turn"}')
  run_prompt "$PJ"
  echo "  guard after the new prompt T2: $(guard s-reset)"
  check "the prompt hook resets the guard to T2:0" [ "$(guard s-reset)" = "T2:0" ]
  run_hook "$(mkin s-reset T2 "$r" "$TP" false)"
  echo "  guard after the first Stop of T2: $(guard s-reset)"
  check "first Stop of the new turn emits again" [ -n "$(ctx "$OUT")" ]
  check "and counts from 1 (nudge 1 of 2)" contains "$(ctx "$OUT")" "Nudge 1 of 2"
  check "guard T2:1" [ "$(guard s-reset)" = "T2:1" ]
  printf 'T2:2\n' > "$KOM_STATUS_DIR/s-reset.guard"
  run_hook "$(mkin s-reset T3 "$r" "$TP" false)"
  echo "  guard after a Stop carrying a new prompt_id T3 with no prompt-hook write: $(guard s-reset)"
  check "a Stop whose prompt_id is not the guard's turn is a fresh turn: emits" [ -n "$(ctx "$OUT")" ]
  check "guard T3:1" [ "$(guard s-reset)" = "T3:1" ]
  printf 'T3:2\n' > "$KOM_STATUS_DIR/s-reset.guard"
  run_hook "$(mkin s-reset T3 "$r" "$TP" true)"
  echo "  guard after a Stop in the still-capped turn T3: $(guard s-reset)"
  check "same turn id at the cap: still silent (a reset needs a new turn id)" is_empty "$OUT"
  check "guard stays T3:2" [ "$(guard s-reset)" = "T3:2" ]

  echo "== case 7: a foreign origin, dirty — expect silence and nothing written =="
  r=$(mkrepo other work/t-other work/t-other)
  ( cd "$r" && $G remote set-url origin https://github.com/example/other-repo.git && printf 'x\n' >> a.txt )
  run_hook "$(mkin s-other p1 "$r" "$TP" false)"
  check "exit 0" [ "$RC" -eq 0 ]
  check "no output" is_empty "$OUT"
  check "no snapshot written" file_absent "$KOM_STATUS_DIR/s-other.json"
  check "no guard written" file_absent "$KOM_STATUS_DIR/s-other.guard"

  echo "== case 8: no upstream at all (a fresh branch), dirty — expect git push -u origin HEAD =="
  r=$(mkrepo noup work/t-noup none)
  printf 'x\n' >> "$r/a.txt"
  run_hook "$(mkin s-noup p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  check "publish is the -u form" contains "$C" "4. git push -u origin HEAD"
  check "never a bare git push" no_bare_push "$C"
  check "upstream shown as none" contains "$C" "upstream:none"

  echo "== case 9: upstream = origin/main on a non-main branch, one commit ahead — expect git push -u origin HEAD =="
  r=$(mkrepo infra infra/t-setup main)
  ( cd "$r" && printf 'c\n' > c.txt && $G add c.txt && $G commit -q -m second )
  run_hook "$(mkin s-infra p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  check "publish is the -u form, never HEAD:main" contains "$C" "4. git push -u origin HEAD"
  check "never a bare git push" no_bare_push "$C"
  check "never names main as the destination" not_contains "$C" "HEAD:main"
  check "lane derived from the branch (t-setup)" contains "$C" "(t-setup)"

  echo "== case 10: claude/* branches (the app's random names) — (a) kom.lane set: the lane names the handoff, publish -u; (b) kom.lane unset, a committed handoffs/handoff-5-epk.md: lane guessed epk, next 6, the hint printed; (c) no kom.lane and no handoff: <lane> and the hint =="
  r=$(mkrepo app claude/busy-test-1234 none)
  ( cd "$r" && $G config kom.lane corner-workstation && printf 'x\n' >> a.txt )
  run_hook "$(mkin s-app p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  check "a: publish is git push -u origin HEAD (the branch keeps its name)" contains "$C" "4. git push -u origin HEAD"
  check "a: handoff name carries the lane" contains "$C" "$H/handoff-1-corner-workstation.md"
  check "a: no lane hint when kom.lane is set" not_contains "$C" "kom.lane"
  r=$(mkrepo app2 claude/quiet-test-5678 none)
  ( cd "$r" && mkdir -p $H && printf 'h\n' > $H/handoff-5-epk.md && $G add $H/handoff-5-epk.md && $G commit -q -m h5 && printf 'x\n' >> a.txt )
  run_hook "$(mkin s-app2 p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  printf '%s\n' "$C" | scrub | sed 's/^/  ctx| /'
  check "b: 1. write handoffs/handoff-6-epk.md (lane guessed from handoff-5-epk.md)" contains "$C" "1. write $H/handoff-6-epk.md ("
  check "b: the hint names the guess and the config line" contains "$C" "(lane epk is a guess from $H/handoff-5-epk.md; fix it: git config --worktree kom.lane <lane>)"
  check "b: snapshot lane epk" [ "$(snap s-app2 '.lane')" = '"epk"' ]
  r=$(mkrepo app3 claude/blank-test-0001 none)
  printf 'x\n' >> "$r/a.txt"
  run_hook "$(mkin s-app3 p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  check "c: the handoff is named with <lane>" contains "$C" "1. write $H/handoff-1-<lane>.md ("
  check "c: the hint says set the lane first" contains "$C" "(set the lane first: git config --worktree kom.lane <lane>)"

  echo "== case 11: KOM_STOP_GUARD=off then =warn on the dirty repo =="
  r="$S/dirty"
  OUT=$(mkin s-guard p1 "$r" "$TP" false | KOM_STOP_GUARD=off PATH="$S/bin:$PATH" bash "$HOOK")
  RC=$?
  echo "  off: stdout: '$OUT'"; echo "  exit:"; echo "  $RC"
  check "off: exit 0" [ "$RC" -eq 0 ]
  check "off: silent" is_empty "$OUT"
  check "off: snapshot still written" [ "$(snap s-guard '.state')" = '"stopped"' ]
  OUT=$(mkin s-guard p1 "$r" "$TP" false | KOM_STOP_GUARD=warn PATH="$S/bin:$PATH" bash "$HOOK")
  RC=$?
  M=$(sysmsg "$OUT")
  echo "  warn: stdout: $(printf '%s' "$OUT" | scrub)"; echo "  exit:"; echo "  $RC"
  check "warn: exit 0" [ "$RC" -eq 0 ]
  check "warn: a systemMessage notice for the user" [ -n "$M" ]
  check "warn: no additionalContext, so no continuation" [ -z "$(ctx "$OUT")" ]
  check "warn: one line" [ "$(printf '%s\n' "$M" | wc -l | tr -d ' ')" = "1" ]
  check "warn: carries the publish line" contains "$M" "git push origin HEAD:work/t-dirty"
  check "warn: in order: the handoff, git add -- with it, commit, the publish line" in_order "$M" "write $H/handoff-1-t-dirty.md" "git add -- <the changes> $H/handoff-1-t-dirty.md" "commit" "git push origin HEAD:work/t-dirty"
  check "warn: counted against the cap (guard p1:1)" [ "$(guard s-guard)" = "p1:1" ]

  echo "== case 12: --failure (StopFailure; the CLI's field is error) on the dirty repo — expect silence, snapshot failed:<error> =="
  r="$S/dirty"
  run_hook "$(mkin s-fail p1 "$r" "$TP" false "" rate_limit)" --failure
  check "exit 0" [ "$RC" -eq 0 ]
  check "no output" is_empty "$OUT"
  check "snapshot state failed:rate_limit, event StopFailure" [ "$(snap s-fail '[.state,.hook_event]')" = '["failed:rate_limit","StopFailure"]' ]
  check "--failure writes no guard" file_absent "$KOM_STATUS_DIR/s-fail.guard"
  echo "  snapshot: $(snap s-fail '{state,hook_event,dirty,ahead}')"
  run_hook "$(jq -nc --arg cwd "$r" '{session_id:"s-fail2", cwd:$cwd, hook_event_name:"StopFailure", error_type:"authentication_failed"}')" --failure
  check "legacy error_type field read as a fallback" [ "$(snap s-fail2 '.state')" = '"failed:authentication_failed"' ]
  run_hook "$(jq -nc --arg cwd "$r" '{session_id:"s-fail3", cwd:$cwd, hook_event_name:"StopFailure", error:"bad value; rm -rf"}')" --failure
  check "an error value outside [A-Za-z0-9._-] is recorded as failed:unrecognised" [ "$(snap s-fail3 '.state')" = '"failed:unrecognised"' ]

  echo "== case 13: status directory cannot be written (dirty repo) — expect silence: no guard, no nudge (fail closed) =="
  mkdir -p "$S/ro" && chmod 555 "$S/ro"
  OUT=$(mkin s-ro p1 "$S/dirty" "$TP" false | KOM_STATUS_DIR="$S/ro/status" PATH="$S/bin:$PATH" bash "$HOOK" 2>"$S/stderr.txt")
  RC=$?
  echo "  stdout: '$OUT'"; echo "  exit:"; echo "  $RC"
  check "exit 0" [ "$RC" -eq 0 ]
  check "silent: a cap that cannot be recorded is never emitted" is_empty "$OUT"
  check "nothing created" file_absent "$S/ro/status"
  check "no stderr noise from the failed writes" [ ! -s "$S/stderr.txt" ]
  printf '%s' "$(jq -nc --arg cwd "$S/dirty" '{session_id:"s-ro", prompt_id:"p2", cwd:$cwd, hook_event_name:"UserPromptSubmit", prompt:"x"}')" \
    | KOM_STATUS_DIR="$S/ro/status" bash "$PROMPT_HOOK" > "$S/ro-prompt.out" 2> "$S/ro-prompt.err"
  echo "  kom-prompt.sh with the same unwritable directory, exit:"; echo "  $?"
  check "prompt hook: nothing on stdout" [ ! -s "$S/ro-prompt.out" ]
  check "prompt hook: nothing on stderr" [ ! -s "$S/ro-prompt.err" ]
  chmod 755 "$S/ro"

  echo "== case 14: path names that need quoting (space, apostrophe, non-ASCII, a staged rename, an untracked dir with a space) =="
  r=$(mkrepo odd work/t-odd work/t-odd)
  ( cd "$r" && $G mv a.txt 'renamed a.txt' && printf 'x\n' > "it's.txt" && printf 'y\n' > 'café.txt' \
    && mkdir 'sub dir' && printf 'z\n' > 'sub dir/f.txt' )
  run_hook "$(mkin s-odd p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  printf '%s\n' "$C" | sed -n '/^2\. /p' | sed 's/^/  ctx| /'
  echo "  the git add line as shell words: $(add_args "$C")"
  check "dirty counts entries (4; the rename once)" contains "$C" "dirty:4 "
  check "the git add line parses to --, exactly the four paths, then the handoff" [ "$(add_args "$C")" = "--|renamed a.txt|café.txt|it's.txt|sub dir/|$H/handoff-1-t-odd.md" ]
  check "the rename's source a.txt is not among the paths" not_contains "|$(add_args "$C")|" "|a.txt|"
  check "the git add line alone through bash -n" add_line_parses "$C"

  echo "== case 15: origin URL forms — ssh, mixed case and a git-proxy path are this repo; a fork name and another host are not =="
  r=$(mkrepo forms work/t-forms work/t-forms)
  printf 'x\n' >> "$r/a.txt"
  i=0
  for u in git@github.com:Scroggdawg/kom-festival-board.git https://github.com/scroggdawg/KOM-Festival-Board \
           http://local_proxy@127.0.0.1:43123/git/Scroggdawg/kom-festival-board; do
    i=$((i + 1))
    ( cd "$r" && $G remote set-url origin "$u" )
    OUT=$(mkin "s-form$i" p1 "$r" "$TP" false | PATH="$S/bin:$PATH" bash "$HOOK" 2>/dev/null)
    check "in scope: $u" [ -n "$(ctx "$OUT")" ]
  done
  for u in https://github.com/Scroggdawg/kom-festival-board-fork.git https://gitlab.com/Scroggdawg/kom-festival-board.git; do
    i=$((i + 1))
    ( cd "$r" && $G remote set-url origin "$u" )
    OUT=$(mkin "s-form$i" p1 "$r" "$TP" false | PATH="$S/bin:$PATH" bash "$HOOK" 2>/dev/null)
    check "out of scope, silent: $u" is_empty "$OUT"
    check "out of scope, no snapshot: $u" file_absent "$KOM_STATUS_DIR/s-form$i.json"
  done

  echo "== case 16: the publish line by upstream form, in both hooks (dirty repos) — local main, backup/main, origin/x, none, origin/main: only an origin/<x> upstream with x not main is named; no line ever targets main =="
  local form br want warn ref wa SL
  for form in local backup originx none originmain; do
    br="work/t-up-$form"
    case $form in
      originx)    r=$(mkrepo "up-$form" "$br" x) ;;
      originmain) r=$(mkrepo "up-$form" "$br" main) ;;
      *)          r=$(mkrepo "up-$form" "$br" none) ;;
    esac
    case $form in
      local)  ( cd "$r" && $G branch -q main && $G config "branch.$br.remote" . && $G config "branch.$br.merge" refs/heads/main ) ;;
      backup) ( cd "$r" && $G remote add backup https://example.invalid/kom-backup.git && $G update-ref refs/remotes/backup/main HEAD \
                && $G config "branch.$br.remote" backup && $G config "branch.$br.merge" refs/heads/main ) ;;
    esac
    case $form in
      local)      want="git push -u origin HEAD";  ref=refs/heads/main;          wa=1; warn="warning: upstream refs/heads/main is a local branch, not GitHub" ;;
      backup)     want="git push -u origin HEAD";  ref=refs/remotes/backup/main; wa=1; warn="warning: upstream refs/remotes/backup/main is on remote backup, not origin" ;;
      originx)    want="git push origin HEAD:x";   ref=refs/remotes/origin/x;    wa=0; warn="" ;;
      none)       want="git push -u origin HEAD";  ref="";                       wa=1; warn="" ;;
      originmain) want="git push -u origin HEAD";  ref=refs/remotes/origin/main; wa=0; warn="warning: upstream refs/remotes/origin/main is main, never a publish target" ;;
    esac
    echo "  -- $form: branch $br, upstream ${ref:-none}"
    if [ "$form" = local ]; then
      run_hook "$(mkin "s-up-$form-clean" p1 "$r" "$TP" false)"
      check "$form, clean: ahead is counted against origin, not the local upstream (dirty:0 ahead:1)" contains "$(ctx "$OUT")" "dirty:0 ahead:1"
    fi
    printf 'x\n' >> "$r/a.txt"
    run_hook "$(mkin "s-up-$form" p1 "$r" "$TP" false)"
    C=$(ctx "$OUT")
    printf '%s\n' "$C" | grep -E '^(4\. |   \(warning)' | scrub | sed 's/^/  ctx| /'
    check "$form, stop hook: exit 0" [ "$RC" -eq 0 ]
    check "$form, stop hook: 4. $want" contains "$C" "4. $want"
    check "$form, stop hook: dirty:1 ahead:$wa" contains "$C" "dirty:1 ahead:$wa"
    check "$form, stop hook: never HEAD:main" not_contains "$C" "HEAD:main"
    check "$form, stop hook: never a bare git push" no_bare_push "$C"
    if [ -n "$warn" ]; then
      check "$form, stop hook: the warning names the upstream" contains "$C" "$warn"
    else
      check "$form, stop hook: no warning" not_contains "$C" "warning:"
    fi
    check "$form, snapshot: publish_line and upstream_ref" \
      [ "$(snap "s-up-$form" '[.publish_line,.upstream_ref]')" = "$(jq -nc --arg p "$want" --arg u "$ref" '[$p,$u]')" ]
    run_session "$r"
    SL=$(printf '%s\n' "$OUT" | sed -n 's/^\[kom\] publish line: //p')
    echo "  session-start publish line: $(printf '%s' "$SL" | scrub)"
    echo "  session-start exit:"; echo "  $RC"
    check "$form, session-start: exit 0" [ "$RC" -eq 0 ]
    check "$form, session-start: $want" [ "${SL%%   (*}" = "$want" ]
    check "$form, session-start: never HEAD:main" not_contains "$SL" "HEAD:main"
    if [ -n "$warn" ]; then
      check "$form, session-start: the warning names the upstream" contains "$SL" "$warn"
    else
      check "$form, session-start: no warning" not_contains "$SL" "warning:"
    fi
  done

  echo "== case 17: the handoff by its exact name — next = max + 1 over the refs (the branch holds 3, a remote-only ref holds 9); 14 dirty paths keep the handoff in the add line and count the rest on the next line, a # comment; a handoff already written this turn is named once, never a second one =="
  r=$(mkrepo hand work/t-hand work/t-hand)
  ( cd "$r" && mkdir -p $H && printf 'h\n' > $H/handoff-3-t-hand.md && $G add $H/handoff-3-t-hand.md && $G commit -q -m h3 \
    && $G update-ref refs/remotes/origin/work/t-hand HEAD \
    && t9=$(ledger_tree "$r" HEAD handoff-9-other.md) \
    && c9=$($G commit-tree "$t9" -m 'other lane: handoff-9') \
    && $G update-ref refs/remotes/origin/work/other "$c9" ) || { echo "case 17 setup failed"; exit 2; }
  for i in $(seq 1 14); do printf 'f\n' > "$r/f$(printf '%02d' "$i").txt"; done
  run_hook "$(mkin s-hand p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  u="--|$(for i in $(seq 1 12); do printf 'f%02d.txt|' "$i"; done)$H/handoff-10-t-hand.md"
  printf '%s\n' "$C" | sed -n '/^[12]\. /p; /^   # /p' | scrub | sed 's/^/  ctx| /'
  check "1. write handoffs/handoff-10-t-hand.md (refs hold 3 and 9: next is 10)" contains "$C" "1. write $H/handoff-10-t-hand.md ("
  check "the handoff does not exist yet" file_absent "$r/$H/handoff-10-t-hand.md"
  check "14 paths: the add line shows 12, then the handoff" [ "$(add_args "$C")" = "$u" ]
  check "the add line ends at the handoff: no note inside it" [ "$(add_line "$C")" = "git add $(printf '%s' "$u" | tr '|' ' ')" ]
  check "the count of the rest on the next line, a # comment" [ "$(note_line "$C")" = "   # + 2 more not listed: git status --porcelain" ]
  check "the git add line alone through bash -n (14 paths)" add_line_parses "$C"
  printf 'h\n' > "$r/$H/handoff-10-t-hand.md"
  run_hook "$(mkin s-hand2 p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  printf '%s\n' "$C" | sed -n '/^[12]\. /p; /^   # /p' | scrub | sed 's/^/  ctx| /'
  check "written this turn: dirty:15 counts it" contains "$C" "dirty:15 "
  check "1. names the written handoff" contains "$C" "1. $H/handoff-10-t-hand.md is written and on no ref yet"
  check "no second handoff asked for (no handoff-11)" not_contains "$C" "handoff-11"
  check "the add line names it once, after the 12 shown paths" [ "$(add_args "$C")" = "$u" ]
  check "the count of the rest on the next line, a # comment (the handoff not among them)" [ "$(note_line "$C")" = "   # + 2 more not listed: git status --porcelain" ]
  check "the git add line alone through bash -n (15 paths)" add_line_parses "$C"
  rm -f "$r/$H/handoff-10-t-hand.md"

  echo "== case 17b (KOM): a sibling worktree of the same repository holds an UNCOMMITTED handoffs/handoff-12-x.md — next is 13 in both hooks; a handoff-12 written here is a collision, named with the number to take =="
  ( cd "$r" && $G worktree add -q -b work/sibling "$S/hand-wt" HEAD && mkdir -p "$S/hand-wt/$H" && printf 'h\n' > "$S/hand-wt/$H/handoff-12-x.md" ) || { echo "case 17b setup failed"; exit 2; }
  run_hook "$(mkin s-hand3 p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  printf '%s\n' "$C" | sed -n '/^1\. /p' | scrub | sed 's/^/  ctx| /'
  check "1. write handoffs/handoff-13-t-hand.md (the sibling holds 12)" contains "$C" "1. write $H/handoff-13-t-hand.md ("
  check "snapshot handoff_max_elsewhere 12" [ "$(snap s-hand3 '.handoff_max_elsewhere')" = "12" ]
  run_session "$r"
  echo "  session-start: $(printf '%s\n' "$OUT" | sed -n 's/^\[kom\] handoffs: //p' | scrub)"
  check "session-start: next handoff number: 13, naming the other checkout" contains "$(printf '%s' "$OUT" | scrub)" "next handoff number: 13 (max over the refs is 9, over the other checkouts on this Mac 12 (\$SCRATCH/hand-wt)"
  printf 'h\n' > "$r/$H/handoff-12-t-hand.md"
  run_hook "$(mkin s-hand4 p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  printf '%s\n' "$C" | grep -E '^1\. |already held' | scrub | sed 's/^/  ctx| /'
  check "collision: the note names the file, the holder and the number to take" contains "$(printf '%s' "$C" | scrub)" "($H/handoff-12-t-hand.md here is uncommitted and its number 12 is already held by the checkout \$SCRATCH/hand-wt: rename it to handoff-13-<lane>.md before committing)"
  check "collision: still asks for 13" contains "$C" "1. write $H/handoff-13-t-hand.md ("
  check "collision: the snapshot carries it" contains "$(snap s-hand4 '.handoff_collision')" "already held by the checkout"
  rm -f "$r/$H/handoff-12-t-hand.md"

  echo "== case 17c (KOM): the Drive ledger — KOM_SHELF names a scratch shelf whose HANDOFFS/ holds handoff-20-drive.md: next is 21 in both hooks =="
  mkdir -p "$S/drive/HANDOFFS" && printf 'h\n' > "$S/drive/HANDOFFS/handoff-20-drive.md"
  OUT=$(mkin s-hand5 p1 "$r" "$TP" false | KOM_SHELF="$S/drive" PATH="$S/bin:$PATH" bash "$HOOK" 2>/dev/null)
  C=$(ctx "$OUT")
  printf '%s\n' "$C" | sed -n '/^1\. /p' | scrub | sed 's/^/  ctx| /'
  check "1. write handoffs/handoff-21-t-hand.md (the Drive ledger holds 20)" contains "$C" "1. write $H/handoff-21-t-hand.md ("
  run_session "$r" KOM_SHELF="$S/drive"
  echo "  session-start: $(printf '%s\n' "$OUT" | sed -n 's/^\[kom\] handoffs: //p' | scrub)"
  check "session-start: next handoff number: 21 ... over the Drive ledger 20" contains "$OUT" "next handoff number: 21 (max over the refs is 9, over the other checkouts on this Mac 12"
  check "session-start: names the Drive ledger's 20" contains "$OUT" "over the Drive ledger 20)"

  echo "== case 18: the printed git add line is one valid shell command — 14 changed paths, the 12 listed named with shell metacharacters, a tab and a newline: the add line alone passes bash -n and evaluates to exactly those 12, then the handoff; the other 2 are counted on the next line, a # comment =="
  local nl tb rc18 want18 names18
  nl=$(printf '\nx'); nl=${nl%x}
  tb=$(printf '\t')
  names18=( "#e.txt" "\$(:).txt" "a${nl}b'c\\d.txt" "a (1).txt" "c${tb}d.txt" "g\`:\`.txt" "i;j.txt" "it's.txt" "k&l.txt" "m|n.txt" "o<p.txt" "q*\"r.txt" )
  r=$(mkrepo over work/t-over work/t-over)
  for i in "${names18[@]}" zz1.txt zz2.txt; do printf 'f\n' > "$r/$i" || { echo "case 18 setup failed"; exit 2; }; done
  run_hook "$(mkin s-over p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  printf '%s\n' "$C" | sed -n '/^2\. /p; /^   # /p' | scrub | sed 's/^/  ctx| /'
  add_line "$C" > "$S/add-line-18.sh"
  bash -n "$S/add-line-18.sh" 2> "$S/add-line-18.err"
  rc18=$?
  echo "  bash -n on the printed git add line alone, exit:"; echo "  $rc18"
  if [ -s "$S/add-line-18.err" ]; then echo "  bash -n stderr: $(scrub < "$S/add-line-18.err" | head -c 300)"; fi
  want18=$(set -- -- "${names18[@]}" "$H/handoff-1-t-over.md"; IFS=$'\037'; printf '%s' "$*")
  check "exit 0" [ "$RC" -eq 0 ]
  check "dirty:14" contains "$C" "dirty:14 "
  check "bash -n exit 0: the printed git add line alone is one valid shell command" [ "$rc18" -eq 0 ]
  check "evaluated, the add line is exactly --, the 12 names in git status order, then the handoff" [ "$(add_args "$C" $'\037')" = "$want18" ]
  check "the other 2 are counted on the next line, a # comment" [ "$(note_line "$C")" = "   # + 2 more not listed: git status --porcelain" ]
  check "the 2 not listed are not on the add line" not_contains "$(add_line "$C")" "zz"
  check "the steps are still numbered 1 2 3 4 (no name split a line)" [ "$(steps "$C")" = "1 2 3 4" ]

  echo "== case 19: paths named like git options — untracked --all and -e: the printed git add puts -- before its paths, so git reads both as paths =="
  r=$(mkrepo dash work/t-dash work/t-dash)
  printf 'f\n' > "$r/--all" && printf 'f\n' > "$r/-e" || { echo "case 19 setup failed"; exit 2; }
  run_hook "$(mkin s-dash p1 "$r" "$TP" false)"
  C=$(ctx "$OUT")
  printf '%s\n' "$C" | sed -n '/^2\. /p' | scrub | sed 's/^/  ctx| /'
  check "exit 0" [ "$RC" -eq 0 ]
  check "dirty:2" contains "$C" "dirty:2 "
  check "the add line reads git add -- --all -e handoffs/handoff-1-t-dash.md" [ "$(add_line "$C")" = "git add -- --all -e $H/handoff-1-t-dash.md" ]
  check "as shell words: --, then --all and -e as paths, then the handoff" [ "$(add_args "$C")" = "--|--all|-e|$H/handoff-1-t-dash.md" ]
  check "the git add line alone through bash -n" add_line_parses "$C"

  echo "== sequence: prompt -> Stop (emits, 1) -> Stop stop_hook_active (emits, 2) -> Stop (silent, cap) -> prompt (reset) -> Stop (emits) =="
  r="$S/dirty"
  PJ=$(jq -nc --arg cwd "$r" '{session_id:"s-seq", prompt_id:"P1", cwd:$cwd, hook_event_name:"UserPromptSubmit", prompt:"go"}')
  run_prompt "$PJ"
  echo "  guard after prompt P1: $(guard s-seq)   snapshot state: $(snap s-seq '.state')"
  check "prompt writes P1:0" [ "$(guard s-seq)" = "P1:0" ]
  check "prompt marks working" [ "$(snap s-seq '.state')" = '"working"' ]
  run_hook "$(mkin s-seq P1 "$r" "$TP" false)"
  check "Stop 1 emits" [ -n "$(ctx "$OUT")" ]
  check "Stop 1 says nudge 1 of 2" contains "$(ctx "$OUT")" "Nudge 1 of 2"
  check "guard P1:1" [ "$(guard s-seq)" = "P1:1" ]
  check "snapshot state stopped after Stop 1" [ "$(snap s-seq '.state')" = '"stopped"' ]
  run_hook "$(mkin s-seq P1 "$r" "$TP" true)"
  check "Stop 2 (stop_hook_active) still emits — not an early return" [ -n "$(ctx "$OUT")" ]
  check "Stop 2 says nudge 2 of 2" contains "$(ctx "$OUT")" "Nudge 2 of 2"
  check "guard P1:2" [ "$(guard s-seq)" = "P1:2" ]
  check "snapshot records stop_hook_active=true" [ "$(snap s-seq '.stop_hook_active')" = "true" ]
  TS2=$(snap s-seq '.ts')
  sleep 1
  run_hook "$(mkin s-seq P1 "$r" "$TP" true)"
  check "Stop 3 silent (cap 2 reached)" is_empty "$OUT"
  check "guard stays P1:2" [ "$(guard s-seq)" = "P1:2" ]
  check "snapshot still written at the capped Stop (ts advanced)" [ "$(snap s-seq '.ts')" != "$TS2" ]
  PJ=$(jq -nc --arg cwd "$r" '{session_id:"s-seq", prompt_id:"P2", cwd:$cwd, hook_event_name:"UserPromptSubmit", prompt:"again"}')
  run_prompt "$PJ"
  check "prompt resets to P2:0" [ "$(guard s-seq)" = "P2:0" ]
  run_hook "$(mkin s-seq P2 "$r" "$TP" false)"
  check "Stop 4 emits again after the reset" [ -n "$(ctx "$OUT")" ]
  check "guard P2:1" [ "$(guard s-seq)" = "P2:1" ]
  run_hook "$(mkin s-seq P3 "$r" "$TP" false)"
  check "a new prompt_id without a prompt-hook write is a fresh turn: emits" [ -n "$(ctx "$OUT")" ]
  check "guard P3:1" [ "$(guard s-seq)" = "P3:1" ]
  OUT=$(jq -nc --arg cwd "$r" --arg tp "$TP" '{session_id:"s-noid", cwd:$cwd, transcript_path:$tp, hook_event_name:"Stop", stop_hook_active:false}' | PATH="$S/bin:$PATH" bash "$HOOK")
  RC=$?
  echo "  no prompt_id at all (older CLI): guard: $(guard s-noid)"; echo "  exit:"; echo "  $RC"
  check "no prompt_id: guard unknown:1 after one emission" [ "$(guard s-noid)" = "unknown:1" ]

  echo "== the git shim: every git verb the hook called, and whether any write verb was attempted =="
  awk '{print $1}' "$SHIM_LOG" | sort | uniq -c | sed 's/^/  /'
  check "no forbidden git verb reached the shim" [ "$(grep -cE '^(push|add|stash|checkout|commit|merge|fetch|pull|reset|rm|rebase|switch|restore|clean)( |$)' "$SHIM_LOG")" = "0" ]
  touch "$S/stderr-all.txt"
  check "no hook stderr across every run carried FORBIDDEN" [ "$(grep -c FORBIDDEN "$S/stderr-all.txt")" = "0" ]
  echo "  hook stderr across every run: $(wc -c < "$S/stderr-all.txt" | tr -d ' ') bytes"

  echo "== state transitions on a scratch branch (kom-status.py --repo --status-dir; its git fetch --prune origin served from a scratch bare repository standing in for GitHub; snapshots from real Stops of the hook) =="
  local r7 sd7 st ct_expect gh7 nw rc
  r7=$(mkrepo lane7 work/t-lane work/t-lane)
  ( cd "$r7" && printf 'renders/\n' > .gitignore && $G add .gitignore && $G commit -q -m gitignore && $G update-ref refs/remotes/origin/work/t-lane HEAD )
  gh7=$(mkgithub github7 "$r7" work/t-lane)
  sd7="$S/status7"; mkdir -p "$sd7"
  st7() { FAKE_GITHUB="$gh7" PATH="$S/statusbin:$PATH" python3 "$STATUS_PY" --repo "$r7" --status-dir "$sd7" --json 2>>"$S/status-stderr.txt" \
          | jq -c '{fetch} + (.checkouts[0] | {state, state_reason, dirty, ahead, suffix, commit_time, upstream_kind, origin_is_github, origin_contains_head, snapshot: (.snapshot.state // "none")})'; }
  mkin s7 P1 "$r7" "$TP" false | KOM_STATUS_DIR="$sd7" PATH="$S/bin:$PATH" bash "$HOOK" >/dev/null
  echo "  Stop 1 exit:"; echo "  $?"
  st=$(st7); echo "  after Stop 1 (clean, pushed): $st"
  check "the fetch ran and succeeded (fetch: ok)" [ "$(printf '%s' "$st" | jq -r .fetch)" = "ok" ]
  check "kom-status ran git fetch --prune ... origin (the shim's log)" [ "$(grep -cE '^fetch .*--prune.* origin$' "$STATUS_GIT_LOG")" -ge 1 ]
  check "every fetch it ran carried --prune and named origin" [ "$(grep -E '^fetch( |$)' "$STATUS_GIT_LOG" | grep -cvE -- '--prune.* origin$')" = "0" ]
  check "saved to GitHub after a clean pushed Stop" [ "$(printf '%s' "$st" | jq -r .state)" = "saved to GitHub" ]
  check "on its evidence: an origin upstream, a GitHub origin URL, origin/<x> containing HEAD" \
    [ "$(printf '%s' "$st" | jq -c '[.upstream_kind,.origin_is_github,.origin_contains_head]')" = '["origin",true,true]' ]
  ct_expect=$(cd "$r7" && $REAL_GIT log -1 --format=%ct '@{u}')
  check "commit time equals git log -1 --format=%ct @{u} ($ct_expect)" [ "$(printf '%s' "$st" | jq -r .commit_time)" = "$ct_expect" ]
  sleep 1.2
  printf 'edit\n' >> "$r7/a.txt"
  st=$(st7); echo "  after touching a tracked file, no new Stop: $st"
  check "unsaved changes" [ "$(printf '%s' "$st" | jq -r .state)" = "unsaved changes" ]
  check "suffix names the snapshot time" contains "$(printf '%s' "$st" | jq -r '.suffix|join(";")')" "snapshot "
  check "suffix names the files-changed time" contains "$(printf '%s' "$st" | jq -r '.suffix|join(";")')" "files changed "
  mkdir -p "$r7/renders" && printf 'png\n' > "$r7/renders/frame.png"
  st=$(st7); echo "  after writing an ignored file (renders/frame.png), no new Stop: $st"
  check "working (an ignored file newer than the snapshot)" [ "$(printf '%s' "$st" | jq -r .state)" = "working" ]
  check "suffix names the ignored file" contains "$(printf '%s' "$st" | jq -r '.suffix|join(";")')" "renders/frame.png"
  sleep 1.2
  mkin s7 P1 "$r7" "$TP" true | KOM_STATUS_DIR="$sd7" PATH="$S/bin:$PATH" bash "$HOOK" >/dev/null
  echo "  Stop 2 (the continuation, stop_hook_active) exit:"; echo "  $?"
  st=$(st7); echo "  after the continuation's Stop: $st"
  check "back to unsaved changes once a newer Stop snapshot exists" [ "$(printf '%s' "$st" | jq -r .state)" = "unsaved changes" ]
  jq -nc --arg cwd "$r7" '{session_id:"s7", prompt_id:"P2", cwd:$cwd, hook_event_name:"UserPromptSubmit", prompt:"next"}' \
    | KOM_STATUS_DIR="$sd7" bash "$PROMPT_HOOK" >/dev/null
  echo "  prompt P2 exit:"; echo "  $?"
  st=$(st7); echo "  after the next prompt (snapshot says working), no Stop yet: $st"
  check "working while the snapshot says working" [ "$(printf '%s' "$st" | jq -r .state)" = "working" ]
  check "suffix says which session marked it working" contains "$(printf '%s' "$st" | jq -r '.suffix|join(";")')" "marked working at"
  mkin s7 P2 "$r7" "$TP" false | KOM_STATUS_DIR="$sd7" PATH="$S/bin:$PATH" bash "$HOOK" >/dev/null
  ( cd "$r7" && $G add a.txt && $G commit -q -m edit )
  st=$(st7); echo "  after a Stop, then commit, before publish: $st"
  check "not on GitHub" [ "$(printf '%s' "$st" | jq -r .state)" = "not on GitHub" ]
  check "origin/work/t-lane does not contain HEAD yet" [ "$(printf '%s' "$st" | jq -r .origin_contains_head)" = "false" ]
  "$REAL_GIT" --git-dir="$gh7" fetch -q "$r7" "refs/heads/work/t-lane:refs/heads/work/t-lane"
  echo "  the publish, simulated (the stand-in GitHub fetches the branch; no git push anywhere), exit:"; echo "  $?"
  st=$(st7); echo "  after publish, still no new Stop: $st"
  check "saved to GitHub without a newer snapshot" [ "$(printf '%s' "$st" | jq -r .state)" = "saved to GitHub" ]
  ct_expect=$(cd "$r7" && $REAL_GIT log -1 --format=%ct '@{u}')
  check "commit time equals %ct of @{u} after the publish ($ct_expect)" [ "$(printf '%s' "$st" | jq -r .commit_time)" = "$ct_expect" ]
  FAKE_GITHUB="$gh7" PATH="$S/statusbin:$PATH" python3 "$STATUS_PY" --repo "$r7" --status-dir "$sd7" --json 2>/dev/null | python3 -m json.tool >/dev/null
  echo "  --json | python3 -m json.tool exit:"; echo "  $?"
  FAKE_GITHUB="$gh7" PATH="$S/statusbin:$PATH" python3 "$STATUS_PY" --repo "$r7" --status-dir "$sd7" --plain 2>/dev/null | scrub | sed 's/^/  plain| /'
  st=$(python3 "$STATUS_PY" --repo "$r7" --status-dir "$sd7" --no-fetch --json 2>>"$S/status-stderr.txt" | jq -c '{fetch} + (.checkouts[0] | {state, state_reason})')
  echo "  the same clean, published checkout with --no-fetch: $st"
  check "--no-fetch: unknown (not fetched this run), never saved to GitHub" \
    [ "$(printf '%s' "$st" | jq -c '[.fetch,.state,.state_reason]')" = '["skipped","unknown","not fetched this run (--no-fetch)"]' ]
  st=$(FAKE_FETCH=fail FAKE_GITHUB="$gh7" PATH="$S/statusbin:$PATH" python3 "$STATUS_PY" --repo "$r7" --status-dir "$sd7" --json 2>>"$S/status-stderr.txt" \
       | jq -c '{fetch} + (.checkouts[0] | {state, state_reason})')
  echo "  the same checkout with the fetch failing (offline): $st"
  check "a failing fetch: unknown (fetch failed), never saved to GitHub" \
    [ "$(printf '%s' "$st" | jq -c '[.fetch,.state,.state_reason]')" = '["failed","unknown","fetch failed"]' ]
  # a claude/* worktree with no upstream, no kom.lane, an uncommitted handoffs/handoff-2-t-lane.md
  ( cd "$r7" && $G worktree add -q -b claude/test-app-99 "$S/lane7-app" HEAD && mkdir -p "$S/lane7-app/$H" && printf 'h\n' > "$S/lane7-app/$H/handoff-2-t-lane.md" )
  st=$(FAKE_GITHUB="$gh7" PATH="$S/statusbin:$PATH" python3 "$STATUS_PY" --repo "$r7" --status-dir "$sd7" --json 2>>"$S/status-stderr.txt" \
       | jq -c '.checkouts[] | select(.branch == "claude/test-app-99") | {state, lane, lane_source, last_handoff, unknown_reason, suffix}')
  echo "  claude/* worktree, no upstream, HEAD on origin/work/t-lane, handoff-2-t-lane.md uncommitted: $st"
  check "no upstream is unknown" [ "$(printf '%s' "$st" | jq -r .state)" = "unknown" ]
  check "lane guessed from the newest handoff (t-lane)" [ "$(printf '%s' "$st" | jq -r '[.lane,.lane_source]|join(" ")')" = "t-lane guessed from $H/handoff-2-t-lane.md" ]
  check "last handoff 2 (the ledger directory, uncommitted counts)" [ "$(printf '%s' "$st" | jq -r .last_handoff)" = "2" ]
  check "suffix names the one origin ref holding HEAD and the upstream command" contains "$(printf '%s' "$st" | jq -r '.suffix|join(";")')" "set it: git branch --set-upstream-to=origin/work/t-lane"
  touch "$S/marker7"; sleep 1.1
  st7 >/dev/null
  FAKE_GITHUB="$gh7" PATH="$S/statusbin:$PATH" python3 "$STATUS_PY" --repo "$r7" --status-dir "$sd7" --plain >/dev/null 2>>"$S/status-stderr.txt"
  nw=$(find "$r7" "$S/lane7-app" -newer "$S/marker7" ! -name .git ! -path '*/.git/*' 2>/dev/null | scrub)
  echo "  paths inside either checkout newer than a marker made before two more scans: ${nw:-none}"
  check "the scan writes nothing inside any checkout (its one write is the fetch's, in the shared .git)" is_empty "$nw"

  echo "== evidence for saved to GitHub — a branch deleted on GitHub, a local upstream, another remote, an origin that is not GitHub (each its own scratch branch and stand-in GitHub) =="
  local r8 gh8 r9 gh9 r10 gh10 r11 gh11
  stq() { FAKE_GITHUB="$2" PATH="$S/statusbin:$PATH" python3 "$STATUS_PY" --repo "$1" --status-dir "$sd7" --json 2>>"$S/status-stderr.txt" \
      | jq -c '{fetch} + (.checkouts[0] | {state, state_reason, upstream, upstream_kind, origin_is_github, origin_contains_head, suffix})'; }
  r8=$(mkrepo stale work/t-stale work/t-stale)
  gh8=$(mkgithub github8 "$r8" work/t-stale)
  st=$(stq "$r8" "$gh8"); echo "  branch while the stand-in GitHub still has work/t-stale: $st"
  check "stale: saved to GitHub while the branch exists there" [ "$(printf '%s' "$st" | jq -r .state)" = "saved to GitHub" ]
  "$REAL_GIT" --git-dir="$gh8" update-ref -d refs/heads/work/t-stale
  echo "  work/t-stale deleted on the stand-in GitHub, exit:"; echo "  $?"
  st=$(stq "$r8" "$gh8"); echo "  the same branch after the deletion: $st"
  check "stale: never saved to GitHub once the branch is gone" [ "$(printf '%s' "$st" | jq -r .state)" != "saved to GitHub" ]
  check "stale: unknown (upstream gone: origin has no work/t-stale)" \
    [ "$(printf '%s' "$st" | jq -c '[.state,.state_reason]')" = '["unknown","upstream gone: origin has no work/t-stale"]' ]
  ( cd "$r8" && "$REAL_GIT" show-ref --verify --quiet refs/remotes/origin/work/t-stale )
  rc=$?
  echo "  git show-ref --verify refs/remotes/origin/work/t-stale exit:"; echo "  $rc"
  check "stale: the fetch pruned refs/remotes/origin/work/t-stale (show-ref exit 1)" [ "$rc" -eq 1 ]
  r9=$(mkrepo localup work/t-localup none)
  ( cd "$r9" && $G branch -q main && $G config branch.work/t-localup.remote . && $G config branch.work/t-localup.merge refs/heads/main )
  gh9=$(mkgithub github9 "$r9")
  st=$(stq "$r9" "$gh9"); echo "  a local upstream (refs/heads/main), clean: $st"
  check "local upstream, clean: not on GitHub (upstream is local)" \
    [ "$(printf '%s' "$st" | jq -c '[.state,.state_reason,.upstream_kind]')" = '["not on GitHub","upstream is local","local"]' ]
  FAKE_GITHUB="$gh9" PATH="$S/statusbin:$PATH" python3 "$STATUS_PY" --repo "$r9" --status-dir "$sd7" --plain > "$S/plain9.txt" 2>>"$S/status-stderr.txt"
  echo "  --plain exit:"; echo "  $?"
  scrub < "$S/plain9.txt" | sed 's/^/  plain| /'
  check "local upstream, --plain reads: not on GitHub (upstream is local)" grep -qF "t-localup — not on GitHub (upstream is local)" "$S/plain9.txt"
  printf 'x\n' >> "$r9/a.txt"
  st=$(stq "$r9" "$gh9"); echo "  the same local-upstream branch, dirty: $st"
  check "local upstream, dirty: unsaved changes, the suffix still says upstream is local" \
    [ "$(printf '%s' "$st" | jq -c '[.state, (.suffix | any(. == "upstream is local"))]')" = '["unsaved changes",true]' ]
  r10=$(mkrepo backupup work/t-backupup none)
  ( cd "$r10" && $G remote add backup https://example.invalid/kom-backup.git && $G update-ref refs/remotes/backup/main HEAD \
    && $G config branch.work/t-backupup.remote backup && $G config branch.work/t-backupup.merge refs/heads/main )
  gh10=$(mkgithub github10 "$r10")
  st=$(stq "$r10" "$gh10"); echo "  an upstream on another remote (backup/main), clean: $st"
  check "another remote, clean: not on GitHub (upstream is on backup, not origin)" \
    [ "$(printf '%s' "$st" | jq -c '[.state,.state_reason]')" = '["not on GitHub","upstream is on backup, not origin"]' ]
  r11=$(mkrepo notgh work/t-notgh work/t-notgh)
  gh11=$(mkgithub github11 "$r11" work/t-notgh)
  ( cd "$r11" && $G remote set-url origin https://oauth2:s3cr3t@gitlab.com/Scroggdawg/kom-festival-board.git )
  st=$(stq "$r11" "$gh11"); echo "  origin on another host (a token in its URL), clean and level: $st"
  check "origin not GitHub: unknown (origin is not the GitHub repo), never saved" \
    [ "$(printf '%s' "$st" | jq -c '[.state,.state_reason]')" = '["unknown","origin is not the GitHub repo: https://***@gitlab.com/Scroggdawg/kom-festival-board.git"]' ]
  check "origin not GitHub: the token in the URL is never printed" not_contains "$st" "s3cr3t"
  check "status scanner wrote nothing to stderr" [ ! -s "$S/status-stderr.txt" ]

  echo "== case 20: one set of URLs through every redactor — plain https, https://user:token@, https://us@er:tok@en@, ssh git@host:path, ssh://user:token@host/, no credential (a port, an @ in the path): kom-status.py's redact_url and the redact of kom-stop.sh, kom-session-start.sh and kom-check.sh (cut out of the files, never run whole) print one credential-free line each; then the scp form with a token =="
  local rroot="$HERE/../.." rj
  local -a rlabel rurl rwant
  rlabel=( "plain https" "https://user:token@" "https://us@er:tok@en@" "ssh git@host:path" "ssh://user:token@host/"
           "no credential: a port, an @ in the path" "scp form with a token, user:token@host:path" )
  rurl=( "https://github.com/Scroggdawg/kom-festival-board.git"
         "https://user:token@github.com/Scroggdawg/kom-festival-board.git"
         "https://us@er:tok@en@github.com/Scroggdawg/kom-festival-board.git"
         "git@github.com:Scroggdawg/kom-festival-board.git"
         "ssh://user:token@github.com/Scroggdawg/kom-festival-board.git"
         "git+https://github.com:443/Scroggdawg/kom-festival-board.git@v1#egg=kom"
         "user:token@github.com:Scroggdawg/kom-festival-board.git" )
  rwant=( "https://github.com/Scroggdawg/kom-festival-board.git"
          "https://***@github.com/Scroggdawg/kom-festival-board.git"
          "https://***@github.com/Scroggdawg/kom-festival-board.git"
          "git@github.com:Scroggdawg/kom-festival-board.git"
          "ssh://***@github.com/Scroggdawg/kom-festival-board.git"
          "git+https://github.com:443/Scroggdawg/kom-festival-board.git@v1#egg=kom"
          "***@github.com:Scroggdawg/kom-festival-board.git" )
  cat > "$S/redactors.py" <<'PY'
"""argv: the checkout root, the JSON output path, then the URLs. Every redactor is read from its
file without running the file: kom-status.py is imported (main() stays unrun); each script's
bash redact() is cut out of the file and run alone in bash -c.
Writes {redactor: [one output per URL]}, null for a redactor that could not be found or run."""
import importlib.util, json, os, re, subprocess, sys

root, dest, urls = sys.argv[1], sys.argv[2], sys.argv[3:]
out = {}
try:
    spec = importlib.util.spec_from_file_location("kom_status", os.path.join(root, "bin", "kom-status.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out["kom-status.py redact_url"] = [mod.redact_url(u) for u in urls]
except Exception:
    out["kom-status.py redact_url"] = None
for name, rel in (("kom-stop.sh redact", "bin/hooks/kom-stop.sh"),
                  ("kom-session-start.sh redact", "bin/hooks/kom-session-start.sh"),
                  ("kom-check.sh redact", "bin/kom-check.sh")):
    try:
        src = open(os.path.join(root, rel), encoding="utf-8").read()
    except OSError:
        out[name] = None
        continue
    m = re.search(r"^redact\(\) \{.*?^\}$", src, re.S | re.M)
    if not m:
        out[name] = None
        continue
    p = subprocess.run(["bash", "-c", "set -u\n" + m.group(0) + '\nfor u in "$@"; do redact "$u"; printf "\\0"; done',
                        "redact"] + urls, capture_output=True, text=True)
    out[name] = p.stdout.split("\0")[:-1] if p.returncode == 0 else None
with open(dest, "w", encoding="utf-8") as fh:
    json.dump(out, fh)
PY
  rj="$S/redactors.json"
  python3 "$S/redactors.py" "$rroot" "$rj" "${rurl[@]}" 2>"$S/redactors.err"
  echo "  redactors.py exit:"; echo "  $?"
  if [ -s "$S/redactors.err" ]; then echo "  redactors.py stderr: $(scrub < "$S/redactors.err" | head -c 300)"; fi
  echo "  redactors run: $(jq -r '[to_entries[] | .key + (if .value == null then " (NOT FOUND)" else "" end)] | join(" | ")' "$rj" 2>/dev/null)"
  check "all four redactors found and run" [ "$(jq '[.[] | select(. != null)] | length' "$rj" 2>/dev/null)" = "4" ]
  for i in 0 1 2 3 4 5 6; do
    echo "  $((i + 1)) ${rlabel[$i]} — ${rurl[$i]}"
    jq -r --argjson i "$i" 'to_entries | map(select(.value != null) | {k: .key, v: .value[$i]}) | group_by(.v)[]
      | "    -> \(.[0].v)   (\(map(.k) | join(", ")))"' "$rj" 2>/dev/null
  done
  for i in 0 1 2 3 4 5 6; do
    check "$((i + 1)) ${rlabel[$i]} — all four print ${rwant[$i]}" \
      [ "$(jq -c --argjson i "$i" '[.[] | if . == null then null else .[$i] end] | unique' "$rj" 2>/dev/null)" = "$(jq -nc --arg w "${rwant[$i]}" '[$w]')" ]
  done
  check "no redactor prints a credential (user:, token, us@er, tok@en)" \
    [ "$(jq '[.[] | select(. != null) | .[0:6][] | select(test("user:|token|us@er|tok@en"))] | length' "$rj" 2>/dev/null)" = "0" ]

  echo "== case 21: a token is never printed — kom-status.py --json and --plain and both hooks, on branches whose origin or branch remote is https://me@example.com:S3CR3T@gitlab.com/... (an @ in the user part), a fetch error that quotes it, and a handoff recap that carries it =="
  local TOK='https://me@example.com:S3CR3T@gitlab.com/Scroggdawg/kom-festival-board.git'
  local TOKR='https://***@gitlab.com/Scroggdawg/kom-festival-board.git'
  local J PL r21 gh21 SO want21
  st21() { J=$(FAKE_GITHUB="$2" PATH="$S/statusbin:$PATH" python3 "$STATUS_PY" --repo "$1" --status-dir "$sd7" --json 2>>"$S/status-stderr21.txt")
           PL=$(FAKE_GITHUB="$2" PATH="$S/statusbin:$PATH" python3 "$STATUS_PY" --repo "$1" --status-dir "$sd7" --plain 2>>"$S/status-stderr21.txt"); }
  ( cd "$r11" && $G remote set-url origin "$TOK" )
  st21 "$r11" "$gh11"
  st=$(printf '%s' "$J" | jq -c '.checkouts[0] | [.state, .state_reason, .origin_url]')
  echo "  (a) origin $TOKR, clean and level: $st"
  check "(a) origin: unknown (origin is not the GitHub repo), its URL printed as $TOKR" \
    [ "$st" = "$(jq -nc --arg u "$TOKR" '["unknown", "origin is not the GitHub repo: " + $u, $u]')" ]
  check "(a) --plain names it the same way" contains "$PL" "origin is not the GitHub repo: $TOKR"
  check "(a) the token is in neither --json nor --plain" not_contains "$J$PL" "S3CR3T"
  check "(a) nor the user part" not_contains "$J$PL" "me@example.com"
  r21=$(mkrepo tokb work/t-tokb none)
  ( cd "$r21" && $G config branch.work/t-tokb.remote "$TOK" && $G config branch.work/t-tokb.merge refs/heads/work/t-tokb ) || { echo "case 21 setup failed"; exit 2; }
  gh21=$(mkgithub github21b "$r21")
  st21 "$r21" "$gh21"
  st=$(printf '%s' "$J" | jq -c '.checkouts[0] | [.state, .state_reason]')
  echo "  (b) branch.<b>.remote is the URL (what git push -u <url> writes; @{u} does not resolve): $st"
  check "(b) upstream gone, the remote printed as $TOKR" \
    [ "$st" = "$(jq -nc --arg u "$TOKR" '["unknown", "upstream gone: " + $u + " has no work/t-tokb"]')" ]
  check "(b) the token is in neither --json nor --plain" not_contains "$J$PL" "S3CR3T"
  r21=$(mkrepo tokc work/t-tokc none)
  ( cd "$r21" && $G config "remote.$TOK.fetch" '+refs/heads/*:refs/remotes/glab/*' && $G update-ref refs/remotes/glab/work/t-tokc HEAD \
    && $G config branch.work/t-tokc.remote "$TOK" && $G config branch.work/t-tokc.merge refs/heads/work/t-tokc ) || { echo "case 21 setup failed"; exit 2; }
  gh21=$(mkgithub github21c "$r21")
  st21 "$r21" "$gh21"
  st=$(printf '%s' "$J" | jq -c '.checkouts[0] | [.state, .state_reason, .upstream_kind]')
  echo "  (c) the same URL as a remote with a fetch refspec (@{u} resolves to refs/remotes/glab/work/t-tokc), clean: $st"
  check "(c) not on GitHub; state_reason and upstream_kind print the remote as $TOKR" \
    [ "$st" = "$(jq -nc --arg u "$TOKR" '["not on GitHub", "upstream is on " + $u + ", not origin", "remote " + $u]')" ]
  check "(c) the token is in neither --json nor --plain" not_contains "$J$PL" "S3CR3T"
  printf 'x\n' >> "$r21/a.txt"
  run_hook "$(mkin s-tokc p1 "$r21" "$TP" false)"
  C=$(ctx "$OUT")
  check "(c) stop hook: the warning names the remote as $TOKR" contains "$C" "is on remote $TOKR, not origin"
  check "(c) stop hook: the snapshot's publish_warning names it the same way" contains "$(snap s-tokc '.publish_warning')" "is on remote $TOKR, not origin"
  check "(c) stop hook: the token is in neither its output nor its snapshot" \
    not_contains "$OUT$(cat "$KOM_STATUS_DIR/s-tokc.json" 2>/dev/null)" "S3CR3T"
  mkdir -p "$r21/$H"
  printf '# handoff-1-t-tokc\n\n## Where we left off, newest first\n- pushed to %s, and the scp form me:S3CR3T@gitlab.com:Scroggdawg/kom-festival-board.git\n' "$TOK" > "$r21/$H/handoff-1-t-tokc.md"
  run_session "$r21"
  SO=$OUT
  printf '%s\n' "$SO" | grep -E 'publish line|pushed to' | scrub | sed 's/^/  out| /'
  echo "  session-start exit:"; echo "  $RC"
  check "(c) session-start: the publish warning names the remote as $TOKR" contains "$SO" "is on remote $TOKR, not origin"
  check "(c) session-start: the recap line prints both URLs redacted" \
    contains "$SO" "- pushed to $TOKR, and the scp form ***@gitlab.com:Scroggdawg/kom-festival-board.git"
  check "(c) session-start: the token is nowhere in its output" not_contains "$SO" "S3CR3T"
  want21="fatal: unable to access '$TOKR/': Could not resolve host: gitlab.com"
  J=$(FAKE_FETCH_ERR="fatal: unable to access '$TOK/': Could not resolve host: gitlab.com" FAKE_GITHUB="$gh21" PATH="$S/statusbin:$PATH" \
      python3 "$STATUS_PY" --repo "$r21" --status-dir "$sd7" --json 2>>"$S/status-stderr21.txt")
  PL=$(FAKE_FETCH_ERR="fatal: unable to access '$TOK/': Could not resolve host: gitlab.com" FAKE_GITHUB="$gh21" PATH="$S/statusbin:$PATH" \
      python3 "$STATUS_PY" --repo "$r21" --status-dir "$sd7" --plain 2>>"$S/status-stderr21.txt")
  st=$(printf '%s' "$J" | jq -c '[.fetch, .fetch_detail]')
  echo "  (d) the fetch fails with an error that quotes the URL, token and all: $st"
  check "(d) fetch_detail prints the URL as $TOKR" [ "$st" = "$(jq -nc --arg d "$want21" '["failed", $d]')" ]
  check "(d) --plain prints the same detail" contains "$PL" "($want21)"
  check "(d) the token is in neither --json nor --plain" not_contains "$J$PL" "S3CR3T"
  check "kom-status.py wrote nothing to stderr in this case" [ ! -s "$S/status-stderr21.txt" ]
  check "the git shim, whole run so far: no forbidden git verb (these hook runs included)" \
    [ "$(grep -cE '^(push|add|stash|checkout|commit|merge|fetch|pull|reset|rm|rebase|switch|restore|clean)( |$)' "$SHIM_LOG")" = "0" ]

  echo "== settings.json: valid JSON; every hook command is bash \"\$CLAUDE_PROJECT_DIR/bin/hooks/<file>\" and the file exists =="
  python3 -m json.tool "$SETTINGS" >/dev/null
  echo "  python3 -m json.tool exit:"; echo "  $?"
  jq -r '.hooks | to_entries[] | .key as $e | .value[].hooks[] | "\($e)\t\(.command)"' "$SETTINGS" | sed 's/^/  /'
  check "events are exactly SessionStart, UserPromptSubmit, Stop, StopFailure" \
    [ "$(jq -r '.hooks | keys | join(",")' "$SETTINGS")" = "SessionStart,Stop,StopFailure,UserPromptSubmit" ]
  check "every command matches bash \"\$CLAUDE_PROJECT_DIR/bin/hooks/<name>.sh\"[ --failure]" \
    [ "$(jq -r '.hooks[][].hooks[].command' "$SETTINGS" | grep -cvE '^bash "\$CLAUDE_PROJECT_DIR/bin/hooks/[a-z-]+\.sh"( --failure)?$')" = "0" ]
  check "StopFailure passes --failure" [ "$(jq -r '.hooks.StopFailure[0].hooks[0].command' "$SETTINGS")" = 'bash "$CLAUDE_PROJECT_DIR/bin/hooks/kom-stop.sh" --failure' ]
  for f in $(jq -r '.hooks[][].hooks[].command' "$SETTINGS" | grep -oE 'bin/hooks/[a-z-]+\.sh' | sort -u); do
    check "exists: $f" [ -f "$HERE/../../$f" ]
  done

  echo "== session-start: CLAUDE_CODE_REMOTE=true says it is a cloud session and skips the shelf (scratch repo, no fetch); a local session runs the shelf tool's status =="
  r=$(mkrepo ss work/t-ss work/t-ss)
  mkdir -p "$r/shelf" && printf 'VERSION = 4\nraise SystemExit("store tool ran")\n' > "$r/shelf/sync_shelf.py"
  run_session "$r" CLAUDE_CODE_REMOTE=true
  printf '%s\n' "$OUT" | scrub | sed 's/^/  out| /'
  echo "  exit:"; echo "  $RC"
  check "exit 0" [ "$RC" -eq 0 ]
  check "cloud line present" contains "$OUT" "cloud session: no Drive shelf on this machine"
  check "the shelf tool did not run" not_contains "$OUT" "store tool ran"
  run_session "$r"
  echo "  local session (no CLAUDE_CODE_REMOTE), exit:"; echo "  $RC"
  check "local session: no cloud line" not_contains "$OUT" "cloud session"
  check "local session: the shelf tool is run" contains "$OUT" "shelf: sync_shelf.py status printed no summary"

  echo "== pre-commit guard (bin/githooks/pre-commit) in a scratch repo with core.hooksPath set: a 60 MB blob, .env vs .env.example, a duplicate handoff number against a fake origin/main, two handoffs staged with one number, a home-folder literal in code vs a comment vs a docstring; a normal commit timed =="
  local rp hooks rc t0 t1
  rp=$(mkrepo guard work/t-guard main)
  hooks="$S/githooks"; mkdir -p "$hooks" && cp "$PRECOMMIT" "$hooks/pre-commit" && chmod +x "$hooks/pre-commit"
  ( cd "$rp" && $G config core.hooksPath "$hooks" )
  gc() { # commit message; prints the hook's lines and the exit code
    ( cd "$rp" && $G commit -q -m "$1" ) > "$S/gc.out" 2>&1; rc=$?
    grep -E '^(REJECT|pre-commit:)' "$S/gc.out" | scrub | sed 's/^/  hook| /'
    echo "  git commit exit:"; echo "  $rc"
  }
  ( cd "$rp" && head -c 62914560 /dev/zero > big.bin && $G add big.bin ); gc "big"
  check "SIZE: a 60 MB blob is rejected" [ "$rc" -ne 0 ] && check "SIZE line printed" grep -q 'REJECT big.bin: SIZE' "$S/gc.out"
  ( cd "$rp" && $G rm -q --cached big.bin && rm big.bin && printf 'TOKEN=x\n' > .env && printf 'TOKEN=\n' > .env.example && $G add .env .env.example ); gc "env"
  check "SECRET: .env rejected" grep -q 'REJECT .env: SECRET' "$S/gc.out"
  check "SECRET: .env.example allowed (not rejected)" [ "$(grep -c 'REJECT .env.example' "$S/gc.out")" = "0" ]
  ( cd "$rp" && $G rm -q --cached .env && rm .env ); gc "env example alone"
  check ".env.example alone commits" [ "$rc" -eq 0 ]
  ( cd "$rp" && mkdir -p $H && printf 'h\n' > $H/handoff-005-a.md && $G add $H/handoff-005-a.md ); gc "h005"
  check "a new handoff-005-a.md commits (nothing holds 005)" [ "$rc" -eq 0 ]
  ( cd "$rp" && $G update-ref refs/remotes/origin/main HEAD && printf 'h\n' > $H/handoff-005-b.md && $G add $H/handoff-005-b.md ); gc "h005b"
  check "HANDOFF: number 005 already on origin/main (another lane) is rejected" grep -q 'REJECT handoffs/handoff-005-b.md: HANDOFF number 005 already on origin/main' "$S/gc.out"
  ( cd "$rp" && $G rm -q --cached $H/handoff-005-b.md && rm $H/handoff-005-b.md && printf 'h\n' > $H/handoff-006-a.md && printf 'h\n' > $H/handoff-006-b.md && $G add $H/handoff-006-a.md $H/handoff-006-b.md ); gc "h006 twice"
  check "HANDOFF: two handoffs staged with one number are rejected" grep -q 'HANDOFF number 006 staged twice' "$S/gc.out"
  ( cd "$rp" && $G rm -q --cached $H/handoff-006-a.md $H/handoff-006-b.md && rm $H/handoff-006-a.md $H/handoff-006-b.md \
    && printf 'p = "/%s/someone/x"\n' Users > code.py && $G add code.py ); gc "home path in code"
  check "HOMEPATH: a home-folder literal in code is rejected" grep -q 'REJECT code.py: HOMEPATH new line 1' "$S/gc.out"
  ( cd "$rp" && printf '# the old path was /%s/someone/x\n"""docs at /%s/someone too"""\nimport os\np = os.path.expanduser("~/x")\n' Users Users > code.py && $G add code.py ); gc "home path in a comment and a docstring"
  check "HOMEPATH: the literal in a comment or docstring passes" [ "$rc" -eq 0 ]
  ( cd "$rp" && printf 'plain\n' > note.txt && $G add note.txt )
  t0=$(python3 -c 'import time; print(time.time())'); gc "normal"; t1=$(python3 -c 'import time; print(time.time())')
  check "a normal commit passes" [ "$rc" -eq 0 ]
  echo "  normal commit, seconds: $(python3 -c "print(round($t1 - $t0, 3))")"

  echo "== timing: one dirty-tree Stop =="
  local t0s t1s
  t0s=$(python3 -c 'import time; print(time.time())')
  mkin s-time p1 "$S/dirty" "$TP" false | PATH="$S/bin:$PATH" bash "$HOOK" >/dev/null
  t1s=$(python3 -c 'import time; print(time.time())')
  echo "  seconds: $(python3 -c "print(round($t1s - $t0s, 3))")"

  echo "== summary: PASS $PASS  FAIL $FAIL =="
  [ "$FAIL" -eq 0 ]
}

# ------------------------------------------------------------------ mutants (--record)
mutate() { # file old new: replace every occurrence; exit 3 when old is absent
  python3 - "$1" "$2" "$3" <<'PY'
import sys
p, old, new = sys.argv[1:4]
s = open(p, encoding="utf-8").read()
if old not in s:
    sys.exit(3)
open(p, "w", encoding="utf-8").write(s.replace(old, new))
PY
}
MUT_TOTAL=0; MUT_CAUGHT=0
mkcopy() { # dir: the hooks, this harness, kom-status.py, kom-check.sh, the pre-commit guard and settings.json
  local d=$1
  mkdir -p "$d/bin/hooks" "$d/bin/githooks" "$d/.claude" \
    && cp "$HERE"/*.sh "$d/bin/hooks/" && cp "$STATUS_PY" "$CHECK_SH" "$d/bin/" && cp "$PRECOMMIT" "$d/bin/githooks/" && cp "$SETTINGS" "$d/.claude/"
}
control() {
  local d="$S/mutants/control" rc sum
  if ! mkcopy "$d"; then echo "control: the copy could not be made — every catch below is suspect"; return 1; fi
  HOME="$REAL_HOME" bash "$d/bin/hooks/test-kom-stop.sh" > "$d/out.txt" 2>&1
  rc=$?
  sum=$(grep -E '^== summary: ' "$d/out.txt" | sed 's/^== summary: //; s/ ==$//')
  if [ "$rc" -eq 0 ]; then
    echo "control: the unmutated copy — harness exit $rc, $sum — passes, so each catch below is its defect's"
    return 0
  fi
  echo "control: the unmutated copy — harness exit $rc, $sum — FAILS, so every catch below is suspect; first failing check: $(grep -m1 -E '^  FAIL  ' "$d/out.txt" | sed 's/^  FAIL  //')"
  return 1
}
mutant() { # name file old new [file old new ...]
  local name=$1; shift
  local d="$S/mutants/m$((MUT_TOTAL + 1))" applied=1 rc sum
  MUT_TOTAL=$((MUT_TOTAL + 1))
  mkcopy "$d" || applied=0
  while [ "$#" -ge 3 ]; do
    mutate "$d/$1" "$2" "$3" || applied=0
    shift 3
  done
  if [ "$applied" = 0 ]; then
    echo "mutant $MUT_TOTAL: $name — edit NOT applied — NOT caught"
    return
  fi
  HOME="$REAL_HOME" bash "$d/bin/hooks/test-kom-stop.sh" > "$d/out.txt" 2>&1
  rc=$?
  sum=$(grep -E '^== summary: ' "$d/out.txt" | sed 's/^== summary: //; s/ ==$//')
  if [ "$rc" -ne 0 ]; then
    MUT_CAUGHT=$((MUT_CAUGHT + 1))
    echo "mutant $MUT_TOTAL: $name — harness exit $rc, $sum — caught; first failing check: $(grep -m1 -E '^  FAIL  ' "$d/out.txt" | sed 's/^  FAIL  //')"
  else
    echo "mutant $MUT_TOTAL: $name — harness exit $rc, $sum — NOT caught"
  fi
}
run_mutants() {
  local crc
  control
  crc=$?
  mutant "stop_hook_active as an early return" \
    bin/hooks/kom-stop.sh 'case "$TRANSCRIPT" in */subagents/*) exit 0 ;; esac' \
    'case "$TRANSCRIPT" in */subagents/*) exit 0 ;; esac
[ "$STOP_HOOK_ACTIVE" = true ] && exit 0'
  mutant "the prompt hook never resets the guard" \
    bin/hooks/kom-prompt.sh "printf '%s:0\n' \"\$PROMPT_ID\"" "true || printf '%s:0\n' \"\$PROMPT_ID\""
  mutant "the cap is 3, not 2" bin/hooks/kom-stop.sh 'CAP=2' 'CAP=3'
  mutant "the snapshot is written after the cap return (order step 5 after step 6)" \
    bin/hooks/kom-stop.sh 'write_snapshot false "$COUNT"
' '' \
    bin/hooks/kom-stop.sh '[ "$COUNT" -ge "$CAP" ] && exit 0
' '[ "$COUNT" -ge "$CAP" ] && exit 0
write_snapshot false "$COUNT"
'
  mutant "subagents not exempt (agent_id ignored)" bin/hooks/kom-stop.sh '[ -n "$AGENT_ID" ] && exit 0' ':'
  mutant "origin not checked" bin/hooks/kom-stop.sh '[[ "$ORIGIN" =~ $ORIGIN_RE ]] || exit 0' ':'
  mutant "a bare git push when there is no upstream" \
    bin/hooks/kom-stop.sh '  PUBLISH="git push -u origin HEAD"
  if [ -n "$UPSTREAM_REF" ]; then' '  PUBLISH="git push"
  if [ -n "$UPSTREAM_REF" ]; then'
  mutant "warn is still a continuation" bin/hooks/kom-stop.sh 'emit notice ' 'emit context '
  mutant "fail open when the guard cannot be written" \
    bin/hooks/kom-stop.sh '    rm -f "$GF.tmp.$$" 2>/dev/null
    exit 0
' '    rm -f "$GF.tmp.$$" 2>/dev/null
'
  mutant "paths not shell-quoted" bin/hooks/kom-stop.sh 'then . else @sh end' 'then . else . end'
  mutant "session-start ignores CLAUDE_CODE_REMOTE" \
    bin/hooks/kom-session-start.sh '[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] && REMOTE_SESSION=1' ':'
  mutant "kom-status ignores a snapshot that says working" \
    bin/kom-status.py 'elif snap and snap.get("state") == "working":' 'elif False:'
  mutant "stop: the audited publish logic (only the literal origin/main refused, remote prefix stripped)" \
    bin/hooks/kom-stop.sh 'elif [ -n "$ORIGIN_BRANCH" ] && [ "$ORIGIN_BRANCH" != main ]; then
  PUBLISH="git push origin HEAD:$ORIGIN_BRANCH"' 'elif [ -n "$UPSTREAM" ] && [ "$UPSTREAM" != "origin/main" ]; then
  PUBLISH="git push origin HEAD:${UPSTREAM#*/}"'
  mutant "session-start: the audited publish logic (only the literal origin/main refused, remote prefix stripped)" \
    bin/hooks/kom-session-start.sh 'elif [ -n "$ORIGIN_BRANCH" ] && [ "$ORIGIN_BRANCH" != main ]; then
  PUBLISH="git push origin HEAD:$ORIGIN_BRANCH"' 'elif [ -n "$UPSTREAM" ] && [ "$UPSTREAM" != "origin/main" ]; then
  PUBLISH="git push origin HEAD:${UPSTREAM#*/}"'
  mutant "stop: main allowed as the push target" \
    bin/hooks/kom-stop.sh 'elif [ -n "$ORIGIN_BRANCH" ] && [ "$ORIGIN_BRANCH" != main ]; then' 'elif [ -n "$ORIGIN_BRANCH" ]; then'
  mutant "session-start: main allowed as the push target" \
    bin/hooks/kom-session-start.sh 'elif [ -n "$ORIGIN_BRANCH" ] && [ "$ORIGIN_BRANCH" != main ]; then' 'elif [ -n "$ORIGIN_BRANCH" ]; then'
  mutant "stop: ahead counted against a local or backup upstream" \
    bin/hooks/kom-stop.sh 'if [ -n "$ORIGIN_BRANCH" ]; then
  AHEAD=' 'if [ -n "$UPSTREAM" ]; then
  AHEAD='
  mutant "kom-status: one fetch without --prune" \
    bin/kom-status.py 'FETCH_CMD = ["fetch", "--prune", ' 'FETCH_CMD = ["fetch", '
  mutant "kom-status: any resolving upstream is evidence" \
    bin/kom-status.py '    elif note:
        state, reason = "not on GitHub", note
' '' \
    bin/kom-status.py 'rec["unknown_reason"] = saved_blocker(rec, fetch_state)' 'rec["unknown_reason"] = None'
  mutant "kom-status: saved to GitHub without a successful fetch in this run" \
    bin/kom-status.py '    if fetch_state == "skipped":
        return "not fetched this run (--no-fetch)"
    if fetch_state != "ok":
        return "fetch " + str(fetch_state)
' ''
  mutant "kom-status: origin URL not checked" \
    bin/kom-status.py 'rec["origin_is_github"] = bool(GITHUB_ORIGIN_RE.match(url))' 'rec["origin_is_github"] = True'
  mutant "stop, main: commit and publish before the handoff" \
    bin/hooks/kom-stop.sh '2. on the branch: $MAIN_H
3. on the branch: git add -- <the changed files> $HANDOFF_SHOWN
4. on the branch: git commit -m \"<lane>: <what changed>\"
5. on the branch: publish with the -u form the hook prints there, never from main' '2. on the branch: git add -- <the changed files>, commit, publish with the -u form the hook prints there
3. on the branch: $MAIN_H'
  mutant "stop: the git add list built before the handoff exists" \
    bin/hooks/kom-stop.sh '\($rest[0:12] + $h | map(q) | join(" "))' '\($all[0:12] | map(q) | join(" "))'
  mutant "stop, clean but ahead: a handoff demanded, then nothing to add or commit" \
    bin/hooks/kom-stop.sh '    COMMITLINE="git commit -m \"$LANE_SHOWN: <what changed>\""
' '    COMMITLINE="git commit -m \"$LANE_SHOWN: <what changed>\""
    if [ "$DIRTY" -eq 0 ]; then ADDLINE="(nothing to add: the tree is clean)"; COMMITLINE="(nothing to commit: $AHEAD commit(s) wait for the publish line)"; fi
'
  mutant "stop, clean but ahead: no handoff demanded though the last commit carries none" \
    bin/hooks/kom-stop.sh 'HEAD_HANDOFF=${HEAD_HANDOFF% }' 'HEAD_HANDOFF=handoffs/handoff-0-mutant.md'
  mutant "stop, clean but ahead: a handoff demanded though the last commit carries one" \
    bin/hooks/kom-stop.sh '[ "$DIRTY" -eq 0 ] && [ -n "$HEAD_HANDOFF" ] && PUBLISH_ONLY=1' ':'
  mutant "stop: the last commit read against each parent (-m): a merge of main borrows main's handoffs" \
    bin/hooks/kom-stop.sh 'git diff-tree -r -c --root' 'git diff-tree -r -m --root'
  mutant "stop: the '+ N more' note inside the git add line" \
    bin/hooks/kom-stop.sh '    [ "$OTHERS" -gt 12 ] && ADDLINE="$ADDLINE
   # + $((OTHERS - 12)) more not listed: git status --porcelain"' '    [ "$OTHERS" -gt 12 ] && ADDLINE="$ADDLINE  (+ $((OTHERS - 12)) more: git status --porcelain)"'
  mutant "stop: a name with a control character left to @sh (its newline splits the git add line)" \
    bin/hooks/kom-stop.sh 'if (explode | any(. < 32 or . == 127)) then' 'if false then'
  mutant "kom-status: redact_url cuts at the first @" \
    bin/kom-status.py '    return re.sub(r"\S+", _redact_scp, URL_AUTHORITY_CREDENTIALS.sub("://***@", s))' '    s = re.sub(r"(?<=://)[^/@]*@", "", s)
    return re.sub(r"^[^/@:]+@(?=[^/:]+:)", "", s)'
  mutant "kom-status: no scp rule (user:token@host:path printed as is)" \
    bin/kom-status.py '    if at and ":" in user and ":" in host:' '    if False:'
  mutant "kom-status: a gone upstream's remote printed as configured" \
    bin/kom-status.py '(redact_url(remote) or "?", name)' '(remote or "?", name)'
  mutant "kom-status: upstream_kind carries the remote as configured" \
    bin/kom-status.py 'rec["upstream_kind"] = "remote " + (redact_url(remote) or "?")' 'rec["upstream_kind"] = "remote " + (remote or "?")'
  mutant "kom-status: git fetch's error text printed as is" \
    bin/kom-status.py 'fetch_state, fetch_detail = "failed", redact_url(err)' 'fetch_state, fetch_detail = "failed", err'
  mutant "stop: the remote in the publish warning printed as configured" \
    bin/hooks/kom-stop.sh 'WHY="on remote $(redact "${UPS_REMOTE:-?}"), not origin"' 'WHY="on remote ${UPS_REMOTE:-?}, not origin"'
  mutant "stop: redact without the scp rule" \
    bin/hooks/kom-stop.sh 'case "$user" in *:*) case "$host" in *:*) w="***@${w#"$user"@}" ;; esac ;; esac ;;' ': ;;'
  mutant "session-start: the remote in the publish warning printed as configured" \
    bin/hooks/kom-session-start.sh 'WHY="on remote $(redact "${UPS_REMOTE:-?}"), not origin"' 'WHY="on remote ${UPS_REMOTE:-?}, not origin"'
  mutant "session-start: redact without the scp rule" \
    bin/hooks/kom-session-start.sh 'case "$user" in *:*) case "$host" in *:*) w="***@${w#"$user"@}" ;; esac ;; esac ;;' ': ;;'
  mutant "session-start: the recap printed as written" \
    bin/hooks/kom-session-start.sh 'while IFS= read -r line; do redact "$line"; printf' 'while IFS= read -r line; do printf "%s" "$line"; printf'
  mutant "kom-check: redact without the scp rule" \
    bin/kom-check.sh 'case "$user" in *:*) case "$host" in *:*) w="***@${w#"$user"@}" ;; esac ;; esac ;;' ': ;;'
  mutant "stop: the printed git add line without --" \
    bin/hooks/kom-stop.sh 'ADDLINE="git add -- $ADD_WORDS"' 'ADDLINE="git add $ADD_WORDS"'
  mutant "stop, main: the branch's git add template without --" \
    bin/hooks/kom-stop.sh '3. on the branch: git add -- <the changed files>' '3. on the branch: git add <the changed files>'
  mutant "stop, warn: the dirty notice's git add without --" \
    bin/hooks/kom-stop.sh 'git add -- <the changes> $HANDOFF_SHOWN' 'git add the changes and $HANDOFF_SHOWN'
  mutant "stop, warn: the no-handoff notice's git add without --" \
    bin/hooks/kom-stop.sh 'git add -- $HANDOFF_SHOWN, commit' 'git add $HANDOFF_SHOWN, commit'
  mutant "stop (KOM): the next number ignores the other checkouts on this Mac" \
    bin/hooks/kom-stop.sh '[ "$WT_MAX" -gt "$ELSEWHERE_MAX" ] && { ELSEWHERE_MAX=$WT_MAX; ELSEWHERE="the checkout $WT_WHERE"; }' ':'
  mutant "stop (KOM): the next number ignores the Drive ledger" \
    bin/hooks/kom-stop.sh '[ "$DRIVE_MAX" -gt "$ELSEWHERE_MAX" ] && { ELSEWHERE_MAX=$DRIVE_MAX; ELSEWHERE="the Drive ledger HANDOFFS/"; }' ':'
  mutant "session-start (KOM): the next number ignores the Drive ledger" \
    bin/hooks/kom-session-start.sh '[ "$DRIVE_MAX" -gt "$ELSEWHERE_MAX" ] && { ELSEWHERE_MAX=$DRIVE_MAX; ELSEWHERE="the Drive ledger HANDOFFS/"; }' ':'
  mutant "stop (KOM): a colliding handoff number not reported" \
    bin/hooks/kom-stop.sh 'COLLISION="$LEDGER/$NEWEST_FILE here is uncommitted and its number' 'COLLISION=""; NOTE="$LEDGER/$NEWEST_FILE here is uncommitted and its number'
  mutant "stop (KOM): the lane never guessed from the newest handoff" \
    bin/hooks/kom-stop.sh 'LANE=$(printf '"'"'%s'"'"' "$NEWEST_FILE" | sed -nE' 'LANE=""; NOPE=$(printf '"'"'%s'"'"' "$NEWEST_FILE" | sed -nE'
  mutant "kom-status (KOM): the lane never guessed from the newest handoff" \
    bin/kom-status.py '        m = HANDOFF_LANE_RE.match(name or "")' '        m = None'
  mutant "pre-commit (KOM): the size limit dropped" \
    bin/githooks/pre-commit 'LIMIT = 50 * 1024 * 1024' 'LIMIT = 50 * 1024 * 1024 * 1024'
  mutant "pre-commit (KOM): the handoff number not checked against origin/main" \
    bin/githooks/pre-commit '                if origin and nnn in origin and p not in origin[nnn]:' '                if False:'
  echo "mutants caught: $MUT_CAUGHT of $MUT_TOTAL"
  [ "$crc" -eq 0 ] && [ "$MUT_CAUGHT" -eq "$MUT_TOTAL" ]
}

LOG="$S/run.log"
main > "$LOG" 2>&1
MAIN_RC=$?
scrub < "$LOG"
echo "harness exit:"
echo "$MAIN_RC"
if [ -n "$RECORD" ]; then
  MLOG="$S/mutants.log"
  run_mutants > "$MLOG" 2>&1
  MUT_RC=$?
  scrub < "$MLOG"
  echo "mutant suite exit:"
  echo "$MUT_RC"
  STARTED=$(sed -n 1p "$LOG" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z' | head -1)
  TOOLS=$(sed -n 1p "$LOG" | sed 's/^test-kom-stop\.sh — [^ ]* — //')
  HASHES=$(sed -n 2p "$LOG")
  SUMMARY=$(grep -E '^== summary: ' "$LOG" | sed 's/^== summary: //; s/ ==$//')
  MSUM=$(grep -E '^mutants caught: ' "$MLOG" | sed 's/^mutants caught: //')
  CTRL=$(grep -E '^control: ' "$MLOG" | sed 's/^control: //')
  {
    echo "# FALSIFY-kom-stop — recorded run of bin/hooks/test-kom-stop.sh"
    echo
    echo "Run started $STARTED on $(uname -s) $(uname -r) ($TOOLS). Files under test, then the harness that ran them (sha256, first 12): $HASHES."
    echo
    echo "Result: $SUMMARY; harness exit $MAIN_RC (0 = every check passed). Control: $CTRL. Mutants: $MSUM caught; mutant suite exit $MUT_RC (0 = the control copy passed and the harness failed on every deliberately broken copy)."
    echo
    echo "Sections of the run, in transcript order:"
    echo
    grep -E '^== ' "$LOG" | grep -vE '^== summary: ' | sed 's/^== /- /; s/ ==$//' | scrub
    echo
    echo "Method: each case pipes a synthetic hook JSON into the hook and reads the exit code on its own line, never piped. Scratch repos under \$TMPDIR only (an origin URL that is never contacted; remote-tracking refs made with update-ref; kom-status.py's git fetch --prune origin served by a second shim from a scratch bare repository standing in for GitHub, so pruning and a failing fetch are real git behavior, and nothing is ever pushed); HOME, KOM_STATUS_DIR and KOM_SHELF point into the scratch directory; the hook runs behind a git shim that refuses every write verb and logs every call. The pre-commit guard runs with the real git in a scratch repo whose core.hooksPath names a copy of it. Each mutant is a copy of the hooks and scripts with one known defect, run through the same harness, which must exit 1; a control copy with no defect runs first and must exit 0, so no catch is the copy's own failure. What this harness cannot see: whether the CLI acts on the hook's output."
    echo
    echo "Re-run: \`bash bin/hooks/test-kom-stop.sh --record bin/hooks/FALSIFY-kom-stop.md\`"
    echo
    echo '```text'
    scrub < "$LOG"
    echo "harness exit:"
    echo "$MAIN_RC"
    echo '```'
    echo
    echo "Mutant suite:"
    echo
    echo '```text'
    scrub < "$MLOG"
    echo "mutant suite exit:"
    echo "$MUT_RC"
    echo '```'
  } > "$RECORD"
  echo "recorded: $RECORD"
  [ "$MAIN_RC" -eq 0 ] && [ "$MUT_RC" -ne 0 ] && MAIN_RC=1
fi
exit "$MAIN_RC"
