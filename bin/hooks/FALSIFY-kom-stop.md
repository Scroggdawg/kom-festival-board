# FALSIFY-kom-stop — recorded run of bin/hooks/test-kom-stop.sh

Run started 2026-09-23T23:52:47Z on Darwin 25.4.0 (bash 3.2.57(1)-release — jq-1.7.1-apple — git version 2.50.1 (Apple Git-155)). Files under test, then the harness that ran them (sha256, first 12): hook: 460db860f2b6  prompt hook: 474d87db190c  session hook: f5ec1d397e37  status: 8872a4b471fd  check: e1b0688d0f61  pre-commit: c1fa2f8f5718  harness: 17fa5545ec19.

Result: PASS 322  FAIL 0; harness exit 0 (0 = every check passed). Control: the unmutated copy — harness exit 0, PASS 322  FAIL 0 — passes, so each catch below is its defect's. Mutants: 52 of 52 caught; mutant suite exit 0 (0 = the control copy passed and the harness failed on every deliberately broken copy).

Sections of the run, in transcript order:

- case 1: clean + pushed (work/t-clean == origin/work/t-clean, tree clean) — expect silence, snapshot stopped
- case 2: dirty tree (one modified, one untracked) — expect the four lines in order: 1. write handoffs/handoff-1-t-dirty.md, 2. git add -- a.txt b.txt handoffs/handoff-1-t-dirty.md (named though it does not exist yet), 3. git commit, 4. git push origin HEAD:work/t-dirty; nudge 1 of 2
- case 3: clean but ahead of origin/work/t-ahead — (a) the last commit carries handoffs/handoff-1-t-ahead.md: nothing to add, 1 commit not yet on GitHub, the publish line alone; (b) the last commit carries none: the handoff first, alone to add; (c) a merge of main that brings another lane's handoff carries none of its own
- case 4: subagent (transcript under /subagents/, dirty repo) — expect silence and NO snapshot or guard written
- case 5: main branch, dirty, then clean but ahead — expect 'main is not a working branch', no publish line, move the work to a branch and there the handoff first; never a block
- case 6: the cap resets on a new turn — guard seeded at the cap, then a new prompt
- case 7: a foreign origin, dirty — expect silence and nothing written
- case 8: no upstream at all (a fresh branch), dirty — expect git push -u origin HEAD
- case 9: upstream = origin/main on a non-main branch, one commit ahead — expect git push -u origin HEAD
- case 10: claude/* branches (the app's random names) — (a) kom.lane set: the lane names the handoff, publish -u; (b) kom.lane unset, a committed handoffs/handoff-5-epk.md: lane guessed epk, next 6, the hint printed; (c) no kom.lane and no handoff: <lane> and the hint
- case 11: KOM_STOP_GUARD=off then =warn on the dirty repo
- case 12: --failure (StopFailure; the CLI's field is error) on the dirty repo — expect silence, snapshot failed:<error>
- case 13: status directory cannot be written (dirty repo) — expect silence: no guard, no nudge (fail closed)
- case 14: path names that need quoting (space, apostrophe, non-ASCII, a staged rename, an untracked dir with a space)
- case 15: origin URL forms — ssh, mixed case and a git-proxy path are this repo; a fork name and another host are not
- case 16: the publish line by upstream form, in both hooks (dirty repos) — local main, backup/main, origin/x, none, origin/main: only an origin/<x> upstream with x not main is named; no line ever targets main
- case 17: the handoff by its exact name — next = max + 1 over the refs (the branch holds 3, a remote-only ref holds 9); 14 dirty paths keep the handoff in the add line and count the rest on the next line, a # comment; a handoff already written this turn is named once, never a second one
- case 17b (KOM): a sibling worktree of the same repository holds an UNCOMMITTED handoffs/handoff-12-x.md — next is 13 in both hooks; a handoff-12 written here is a collision, named with the number to take
- case 17c (KOM): the Drive ledger — KOM_SHELF names a scratch shelf whose HANDOFFS/ holds handoff-20-drive.md: next is 21 in both hooks
- case 18: the printed git add line is one valid shell command — 14 changed paths, the 12 listed named with shell metacharacters, a tab and a newline: the add line alone passes bash -n and evaluates to exactly those 12, then the handoff; the other 2 are counted on the next line, a # comment
- case 19: paths named like git options — untracked --all and -e: the printed git add puts -- before its paths, so git reads both as paths
- sequence: prompt -> Stop (emits, 1) -> Stop stop_hook_active (emits, 2) -> Stop (silent, cap) -> prompt (reset) -> Stop (emits)
- the git shim: every git verb the hook called, and whether any write verb was attempted
- state transitions on a scratch branch (kom-status.py --repo --status-dir; its git fetch --prune origin served from a scratch bare repository standing in for GitHub; snapshots from real Stops of the hook)
- evidence for saved to GitHub — a branch deleted on GitHub, a local upstream, another remote, an origin that is not GitHub (each its own scratch branch and stand-in GitHub)
- case 20: one set of URLs through every redactor — plain https, https://user:token@, https://us@er:tok@en@, ssh git@host:path, ssh://user:token@host/, no credential (a port, an @ in the path): kom-status.py's redact_url and the redact of kom-stop.sh, kom-session-start.sh and kom-check.sh (cut out of the files, never run whole) print one credential-free line each; then the scp form with a token
- case 21: a token is never printed — kom-status.py --json and --plain and both hooks, on branches whose origin or branch remote is https://me@example.com:S3CR3T@gitlab.com/... (an @ in the user part), a fetch error that quotes it, and a handoff recap that carries it
- settings.json: valid JSON; every hook command is bash "$CLAUDE_PROJECT_DIR/bin/hooks/<file>" and the file exists
- session-start: CLAUDE_CODE_REMOTE=true says it is a cloud session and skips the shelf (scratch repo, no fetch); a local session runs the shelf tool's status
- pre-commit guard (bin/githooks/pre-commit) in a scratch repo with core.hooksPath set: a 60 MB blob, .env vs .env.example, a duplicate handoff number against a fake origin/main, two handoffs staged with one number, a home-folder literal in code vs a comment vs a docstring; a normal commit timed
- timing: one dirty-tree Stop

Method: each case pipes a synthetic hook JSON into the hook and reads the exit code on its own line, never piped. Scratch repos under $TMPDIR only (an origin URL that is never contacted; remote-tracking refs made with update-ref; kom-status.py's git fetch --prune origin served by a second shim from a scratch bare repository standing in for GitHub, so pruning and a failing fetch are real git behavior, and nothing is ever pushed); HOME, KOM_STATUS_DIR and KOM_SHELF point into the scratch directory; the hook runs behind a git shim that refuses every write verb and logs every call. The pre-commit guard runs with the real git in a scratch repo whose core.hooksPath names a copy of it. Each mutant is a copy of the hooks and scripts with one known defect, run through the same harness, which must exit 1; a control copy with no defect runs first and must exit 0, so no catch is the copy's own failure. What this harness cannot see: whether the CLI acts on the hook's output.

Re-run: `bash bin/hooks/test-kom-stop.sh --record bin/hooks/FALSIFY-kom-stop.md`

```text
test-kom-stop.sh — 2026-09-23T23:52:47Z — bash 3.2.57(1)-release — jq-1.7.1-apple — git version 2.50.1 (Apple Git-155)
hook: 460db860f2b6  prompt hook: 474d87db190c  session hook: f5ec1d397e37  status: 8872a4b471fd  check: e1b0688d0f61  pre-commit: c1fa2f8f5718  harness: 17fa5545ec19
scratch: $SCRATCH (under $TMPDIR); HOME, KOM_STATUS_DIR and KOM_SHELF redirected there; git shim refuses write verbs
== case 1: clean + pushed (work/t-clean == origin/work/t-clean, tree clean) — expect silence, snapshot stopped ==
  stdout: 
  exit:
  0
  PASS  exit 0
  PASS  no output
  PASS  snapshot state=stopped dirty=0 ahead=0 emitted=false
  PASS  guard created as p1:0
  PASS  lane from the branch's last component
  snapshot: {"state":"stopped","lane":"t-clean","branch":"work/t-clean","upstream":"origin/work/t-clean","dirty":0,"ahead":0,"publish_line":"git push origin HEAD:work/t-clean","guard":{"turn":"p1","count":0,"setting":"on"}}
== case 2: dirty tree (one modified, one untracked) — expect the four lines in order: 1. write handoffs/handoff-1-t-dirty.md, 2. git add -- a.txt b.txt handoffs/handoff-1-t-dirty.md (named though it does not exist yet), 3. git commit, 4. git push origin HEAD:work/t-dirty; nudge 1 of 2 ==
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-dirty (t-dirty): dirty:2 ahead:0 upstream:origin/work/t-dirty. End the turn with, in this order:\n1. write handoffs/handoff-1-t-dirty.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt b.txt handoffs/handoff-1-t-dirty.md\n3. git commit -m \"t-dirty: <what changed>\"\n4. git push origin HEAD:work/t-dirty\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  exit 0
  PASS  valid Stop feedback JSON
  PASS  names a.txt and b.txt for git add, after --
  PASS  1. write handoffs/handoff-1-t-dirty.md (no ref holds a handoff: next is 1)
  PASS  the handoff does not exist yet
  PASS  2. git add: --, the changed files, then the not-yet-written handoff by name
  PASS  the git add line alone through bash -n: one valid shell command
  PASS  the steps are numbered 1 2 3 4
  PASS  in order: the handoff, git add, git commit, git push
  PASS  no git add, commit or push before the handoff
  PASS  publish line names the upstream branch
  PASS  never a bare git push
  PASS  nudge 1 of 2
  PASS  guard bumped to p1:1
  PASS  snapshot dirty=2 emitted=true
  ctx| [kom-stop] unpublished work on work/t-dirty (t-dirty): dirty:2 ahead:0 upstream:origin/work/t-dirty. End the turn with, in this order:
  ctx| 1. write handoffs/handoff-1-t-dirty.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)
  ctx| 2. git add -- a.txt b.txt handoffs/handoff-1-t-dirty.md
  ctx| 3. git commit -m "t-dirty: <what changed>"
  ctx| 4. git push origin HEAD:work/t-dirty
  ctx| Nudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)
== case 3: clean but ahead of origin/work/t-ahead — (a) the last commit carries handoffs/handoff-1-t-ahead.md: nothing to add, 1 commit not yet on GitHub, the publish line alone; (b) the last commit carries none: the handoff first, alone to add; (c) a merge of main that brings another lane's handoff carries none of its own ==
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-ahead (t-ahead): dirty:0 ahead:1 upstream:origin/work/t-ahead.\nnothing to add; 1 commit not yet on GitHub; publish with: git push origin HEAD:work/t-ahead\n   (the last commit carries handoffs/handoff-1-t-ahead.md)\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  exit 0
  PASS  reports ahead:1 dirty:0
  PASS  publish line
  PASS  never a bare git push
  PASS  a: nothing to add; 1 commit not yet on GitHub; publish with: <the line>
  PASS  a: names the handoff the last commit carries
  PASS  a: no handoff demanded
  PASS  a: no git add, no git commit
  ctx| [kom-stop] unpublished work on work/t-ahead (t-ahead): dirty:0 ahead:1 upstream:origin/work/t-ahead.
  ctx| nothing to add; 1 commit not yet on GitHub; publish with: git push origin HEAD:work/t-ahead
  ctx|    (the last commit carries handoffs/handoff-1-t-ahead.md)
  ctx| Nudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)
  a, warn: [kom-stop] unpublished work on work/t-ahead: dirty:0 ahead:1 upstream:origin/work/t-ahead — nothing to add; 1 commit not yet on GitHub; publish with: git push origin HEAD:work/t-ahead  (notice 1 of 2 this turn; KOM_STOP_GUARD=warn)
  exit:
  0
  PASS  a, warn: nothing to add; 1 commit not yet on GitHub; publish with: <the line>
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-ahead (t-ahead): dirty:0 ahead:2 upstream:origin/work/t-ahead; the last commit (dbb386b) carries no handoff. End the turn with, in this order:\n1. write handoffs/handoff-2-t-ahead.md (recap first, newest first; 2 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- handoffs/handoff-2-t-ahead.md\n3. git commit -m \"t-ahead: <what changed>\"\n4. git push origin HEAD:work/t-ahead\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  b: reports dirty:0 ahead:2
  PASS  b: says the last commit carries no handoff
  PASS  b: 1. write handoffs/handoff-2-t-ahead.md (a local ref holds 1: next is 2)
  PASS  b: 2. git add names the handoff alone, after --
  PASS  b: the git add line alone through bash -n
  PASS  b: the steps are numbered 1 2 3 4
  PASS  b: in order: the handoff, git add, git commit, git push
  PASS  b: never 'nothing to add' after asking for a handoff
  ctx| [kom-stop] unpublished work on work/t-ahead (t-ahead): dirty:0 ahead:2 upstream:origin/work/t-ahead; the last commit (dbb386b) carries no handoff. End the turn with, in this order:
  ctx| 1. write handoffs/handoff-2-t-ahead.md (recap first, newest first; 2 = max over the refs, the other checkouts and the Drive ledger + 1)
  ctx| 2. git add -- handoffs/handoff-2-t-ahead.md
  ctx| 3. git commit -m "t-ahead: <what changed>"
  ctx| 4. git push origin HEAD:work/t-ahead
  ctx| Nudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)
  b, warn: [kom-stop] unpublished work on work/t-ahead: dirty:0 ahead:2 upstream:origin/work/t-ahead — the last commit carries no handoff: write handoffs/handoff-2-t-ahead.md, git add -- handoffs/handoff-2-t-ahead.md, commit, then: git push origin HEAD:work/t-ahead  (notice 1 of 2 this turn; KOM_STOP_GUARD=warn)
  exit:
  0
  PASS  b, warn: the handoff alone to add, after --
  c: git status --porcelain after the merge: ''; parents of HEAD: 2
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-merge (t-merge): dirty:0 ahead:2 upstream:origin/work/t-merge; the last commit (682e0af) carries no handoff. End the turn with, in this order:\n1. write handoffs/handoff-8-t-merge.md (recap first, newest first; 8 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- handoffs/handoff-8-t-merge.md\n3. git commit -m \"t-merge: <what changed>\"\n4. git push origin HEAD:work/t-merge\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  c: a clean merge, 2 ahead (dirty:0 ahead:2)
  PASS  c: main's handoff-7-hub.md is not the merge's own: carries no handoff
  PASS  c: 1. write handoffs/handoff-8-t-merge.md (refs hold 7: next is 8)
  ctx| [kom-stop] unpublished work on work/t-merge (t-merge): dirty:0 ahead:2 upstream:origin/work/t-merge; the last commit (682e0af) carries no handoff. End the turn with, in this order:
  ctx| 1. write handoffs/handoff-8-t-merge.md (recap first, newest first; 8 = max over the refs, the other checkouts and the Drive ledger + 1)
  ctx| 2. git add -- handoffs/handoff-8-t-merge.md
== case 4: subagent (transcript under /subagents/, dirty repo) — expect silence and NO snapshot or guard written ==
  stdout: 
  exit:
  0
  PASS  exit 0
  PASS  no output
  PASS  no snapshot written
  PASS  no guard written
  stdout: 
  exit:
  0
  PASS  agent_id variant: exit 0
  PASS  agent_id variant: no output
  PASS  agent_id variant: no snapshot
  PASS  agent_id variant: no guard
== case 5: main branch, dirty, then clean but ahead — expect 'main is not a working branch', no publish line, move the work to a branch and there the handoff first; never a block ==
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] main is not a working branch; move the work to a branch of its own.\ndirty:1 ahead:0 on main (the main checkout may carry another session's files: check git status before touching anything).\n1. git switch -c <lane>   (keeps the unsaved changes; a new branch off main)\n2. on the branch: write handoffs/handoff-1-<lane>.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n3. on the branch: git add -- <the changed files> handoffs/handoff-1-<lane>.md\n4. on the branch: git commit -m \"<lane>: <what changed>\"\n5. on the branch: publish with the -u form the hook prints there, never from main\nNo publish line on main; Luke merges branches into main. Nudge 1 of 2 this turn. Nothing was pushed, added or stashed by this hook."}}
  exit:
  0
  PASS  exit 0
  PASS  says main is not a working branch
  PASS  no git push line on main
  PASS  feedback, never decision:block
  PASS  snapshot branch=main lane=main
  PASS  reminds: move the work to a branch, git switch -c <lane>
  PASS  says no publish line on main
  PASS  the steps are numbered 1 to 5
  PASS  on the branch, in order: write handoffs/handoff-1-<lane>.md, git add -- with it, git commit, publish
  PASS  no git add, commit or publish before the handoff
  PASS  snapshot publish_line: main has none
  ctx| [kom-stop] main is not a working branch; move the work to a branch of its own.
  ctx| dirty:1 ahead:0 on main (the main checkout may carry another session's files: check git status before touching anything).
  ctx| 1. git switch -c <lane>   (keeps the unsaved changes; a new branch off main)
  ctx| 2. on the branch: write handoffs/handoff-1-<lane>.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)
  ctx| 3. on the branch: git add -- <the changed files> handoffs/handoff-1-<lane>.md
  ctx| 4. on the branch: git commit -m "<lane>: <what changed>"
  ctx| 5. on the branch: publish with the -u form the hook prints there, never from main
  ctx| No publish line on main; Luke merges branches into main. Nudge 1 of 2 this turn. Nothing was pushed, added or stashed by this hook.
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] main is not a working branch; move the work to a branch of its own.\ndirty:0 ahead:1 on main (the main checkout may carry another session's files: check git status before touching anything).\n1. git switch -c <lane>   (keeps the unsaved changes; a new branch off main)\n2. on the branch: write handoffs/handoff-1-<lane>.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n3. on the branch: git add -- <the changed files> handoffs/handoff-1-<lane>.md\n4. on the branch: git commit -m \"<lane>: <what changed>\"\n5. on the branch: publish with the -u form the hook prints there, never from main\nNo publish line on main; Luke merges branches into main. Nudge 1 of 2 this turn. Nothing was pushed, added or stashed by this hook."}}
  exit:
  0
  clean but ahead on main: dirty:0 ahead:1 on main (the main checkout may carry another session's files: check git status before touching anything).
  PASS  main, clean but ahead: dirty:0 ahead:1, still not a working branch
  PASS  main, clean but ahead: no git push, no 'publish with:'
  PASS  main, clean but ahead: the handoff still leads
== case 6: the cap resets on a new turn — guard seeded at the cap, then a new prompt ==
  stdout: 
  exit:
  0
  guard after a Stop in the capped turn T1: T1:2
  PASS  capped turn T1: silent
  PASS  capped turn T1: guard stays T1:2
  PASS  capped turn T1: snapshot still written, count 2
  kom-prompt.sh exit:
  0
  guard after the new prompt T2: T2:0
  PASS  the prompt hook resets the guard to T2:0
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-dirty (t-dirty): dirty:2 ahead:0 upstream:origin/work/t-dirty. End the turn with, in this order:\n1. write handoffs/handoff-1-t-dirty.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt b.txt handoffs/handoff-1-t-dirty.md\n3. git commit -m \"t-dirty: <what changed>\"\n4. git push origin HEAD:work/t-dirty\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  guard after the first Stop of T2: T2:1
  PASS  first Stop of the new turn emits again
  PASS  and counts from 1 (nudge 1 of 2)
  PASS  guard T2:1
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-dirty (t-dirty): dirty:2 ahead:0 upstream:origin/work/t-dirty. End the turn with, in this order:\n1. write handoffs/handoff-1-t-dirty.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt b.txt handoffs/handoff-1-t-dirty.md\n3. git commit -m \"t-dirty: <what changed>\"\n4. git push origin HEAD:work/t-dirty\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  guard after a Stop carrying a new prompt_id T3 with no prompt-hook write: T3:1
  PASS  a Stop whose prompt_id is not the guard's turn is a fresh turn: emits
  PASS  guard T3:1
  stdout: 
  exit:
  0
  guard after a Stop in the still-capped turn T3: T3:2
  PASS  same turn id at the cap: still silent (a reset needs a new turn id)
  PASS  guard stays T3:2
== case 7: a foreign origin, dirty — expect silence and nothing written ==
  stdout: 
  exit:
  0
  PASS  exit 0
  PASS  no output
  PASS  no snapshot written
  PASS  no guard written
== case 8: no upstream at all (a fresh branch), dirty — expect git push -u origin HEAD ==
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-noup (t-noup): dirty:1 ahead:1 upstream:none. End the turn with, in this order:\n1. write handoffs/handoff-1-t-noup.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt handoffs/handoff-1-t-noup.md\n3. git commit -m \"t-noup: <what changed>\"\n4. git push -u origin HEAD\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  publish is the -u form
  PASS  never a bare git push
  PASS  upstream shown as none
== case 9: upstream = origin/main on a non-main branch, one commit ahead — expect git push -u origin HEAD ==
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on infra/t-setup (t-setup): dirty:0 ahead:1 upstream:origin/main; the last commit (a35e96c) carries no handoff. End the turn with, in this order:\n1. write handoffs/handoff-1-t-setup.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- handoffs/handoff-1-t-setup.md\n3. git commit -m \"t-setup: <what changed>\"\n4. git push -u origin HEAD\n   (warning: upstream refs/remotes/origin/main is main, never a publish target; the -u form publishes this branch to origin and re-points the upstream)\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  publish is the -u form, never HEAD:main
  PASS  never a bare git push
  PASS  never names main as the destination
  PASS  lane derived from the branch (t-setup)
== case 10: claude/* branches (the app's random names) — (a) kom.lane set: the lane names the handoff, publish -u; (b) kom.lane unset, a committed handoffs/handoff-5-epk.md: lane guessed epk, next 6, the hint printed; (c) no kom.lane and no handoff: <lane> and the hint ==
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on claude/busy-test-1234 (corner-workstation): dirty:1 ahead:1 upstream:none. End the turn with, in this order:\n1. write handoffs/handoff-1-corner-workstation.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt handoffs/handoff-1-corner-workstation.md\n3. git commit -m \"corner-workstation: <what changed>\"\n4. git push -u origin HEAD\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  a: publish is git push -u origin HEAD (the branch keeps its name)
  PASS  a: handoff name carries the lane
  PASS  a: no lane hint when kom.lane is set
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on claude/quiet-test-5678 (epk): dirty:1 ahead:2 upstream:none. End the turn with, in this order:\n1. write handoffs/handoff-6-epk.md (recap first, newest first; 6 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt handoffs/handoff-6-epk.md\n3. git commit -m \"epk: <what changed>\"\n4. git push -u origin HEAD\n   (lane epk is a guess from handoffs/handoff-5-epk.md; fix it: git config --worktree kom.lane <lane>)\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  ctx| [kom-stop] unpublished work on claude/quiet-test-5678 (epk): dirty:1 ahead:2 upstream:none. End the turn with, in this order:
  ctx| 1. write handoffs/handoff-6-epk.md (recap first, newest first; 6 = max over the refs, the other checkouts and the Drive ledger + 1)
  ctx| 2. git add -- a.txt handoffs/handoff-6-epk.md
  ctx| 3. git commit -m "epk: <what changed>"
  ctx| 4. git push -u origin HEAD
  ctx|    (lane epk is a guess from handoffs/handoff-5-epk.md; fix it: git config --worktree kom.lane <lane>)
  ctx| Nudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)
  PASS  b: 1. write handoffs/handoff-6-epk.md (lane guessed from handoff-5-epk.md)
  PASS  b: the hint names the guess and the config line
  PASS  b: snapshot lane epk
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on claude/blank-test-0001 (<lane>): dirty:1 ahead:1 upstream:none. End the turn with, in this order:\n1. write handoffs/handoff-1-<lane>.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt 'handoffs/handoff-1-<lane>.md'\n3. git commit -m \"<lane>: <what changed>\"\n4. git push -u origin HEAD\n   (set the lane first: git config --worktree kom.lane <lane>)\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  c: the handoff is named with <lane>
  PASS  c: the hint says set the lane first
== case 11: KOM_STOP_GUARD=off then =warn on the dirty repo ==
  off: stdout: ''
  exit:
  0
  PASS  off: exit 0
  PASS  off: silent
  PASS  off: snapshot still written
  warn: stdout: {"systemMessage":"[kom-stop] unpublished work on work/t-dirty: dirty:2 ahead:0 upstream:origin/work/t-dirty — write handoffs/handoff-1-t-dirty.md, git add -- <the changes> handoffs/handoff-1-t-dirty.md, commit, then: git push origin HEAD:work/t-dirty  (notice 1 of 2 this turn; KOM_STOP_GUARD=warn)"}
  exit:
  0
  PASS  warn: exit 0
  PASS  warn: a systemMessage notice for the user
  PASS  warn: no additionalContext, so no continuation
  PASS  warn: one line
  PASS  warn: carries the publish line
  PASS  warn: in order: the handoff, git add -- with it, commit, the publish line
  PASS  warn: counted against the cap (guard p1:1)
== case 12: --failure (StopFailure; the CLI's field is error) on the dirty repo — expect silence, snapshot failed:<error> ==
  stdout: 
  exit:
  0
  PASS  exit 0
  PASS  no output
  PASS  snapshot state failed:rate_limit, event StopFailure
  PASS  --failure writes no guard
  snapshot: {"state":"failed:rate_limit","hook_event":"StopFailure","dirty":2,"ahead":0}
  stdout: 
  exit:
  0
  PASS  legacy error_type field read as a fallback
  stdout: 
  exit:
  0
  PASS  an error value outside [A-Za-z0-9._-] is recorded as failed:unrecognised
== case 13: status directory cannot be written (dirty repo) — expect silence: no guard, no nudge (fail closed) ==
  stdout: ''
  exit:
  0
  PASS  exit 0
  PASS  silent: a cap that cannot be recorded is never emitted
  PASS  nothing created
  PASS  no stderr noise from the failed writes
  kom-prompt.sh with the same unwritable directory, exit:
  0
  PASS  prompt hook: nothing on stdout
  PASS  prompt hook: nothing on stderr
== case 14: path names that need quoting (space, apostrophe, non-ASCII, a staged rename, an untracked dir with a space) ==
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-odd (t-odd): dirty:4 ahead:0 upstream:origin/work/t-odd. End the turn with, in this order:\n1. write handoffs/handoff-1-t-odd.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- 'renamed a.txt' 'café.txt' 'it'\\''s.txt' 'sub dir/' handoffs/handoff-1-t-odd.md\n3. git commit -m \"t-odd: <what changed>\"\n4. git push origin HEAD:work/t-odd\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  ctx| 2. git add -- 'renamed a.txt' 'café.txt' 'it'\''s.txt' 'sub dir/' handoffs/handoff-1-t-odd.md
  the git add line as shell words: --|renamed a.txt|café.txt|it's.txt|sub dir/|handoffs/handoff-1-t-odd.md
  PASS  dirty counts entries (4; the rename once)
  PASS  the git add line parses to --, exactly the four paths, then the handoff
  PASS  the rename's source a.txt is not among the paths
  PASS  the git add line alone through bash -n
== case 15: origin URL forms — ssh, mixed case and a git-proxy path are this repo; a fork name and another host are not ==
  PASS  in scope: git@github.com:Scroggdawg/kom-festival-board.git
  PASS  in scope: https://github.com/scroggdawg/KOM-Festival-Board
  PASS  in scope: http://local_proxy@127.0.0.1:43123/git/Scroggdawg/kom-festival-board
  PASS  out of scope, silent: https://github.com/Scroggdawg/kom-festival-board-fork.git
  PASS  out of scope, no snapshot: https://github.com/Scroggdawg/kom-festival-board-fork.git
  PASS  out of scope, silent: https://gitlab.com/Scroggdawg/kom-festival-board.git
  PASS  out of scope, no snapshot: https://gitlab.com/Scroggdawg/kom-festival-board.git
== case 16: the publish line by upstream form, in both hooks (dirty repos) — local main, backup/main, origin/x, none, origin/main: only an origin/<x> upstream with x not main is named; no line ever targets main ==
  -- local: branch work/t-up-local, upstream refs/heads/main
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-up-local (t-up-local): dirty:0 ahead:1 upstream:refs/heads/main; the last commit (560566c) carries no handoff. End the turn with, in this order:\n1. write handoffs/handoff-1-t-up-local.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- handoffs/handoff-1-t-up-local.md\n3. git commit -m \"t-up-local: <what changed>\"\n4. git push -u origin HEAD\n   (warning: upstream refs/heads/main is a local branch, not GitHub; the -u form publishes this branch to origin and re-points the upstream)\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  local, clean: ahead is counted against origin, not the local upstream (dirty:0 ahead:1)
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-up-local (t-up-local): dirty:1 ahead:1 upstream:refs/heads/main. End the turn with, in this order:\n1. write handoffs/handoff-1-t-up-local.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt handoffs/handoff-1-t-up-local.md\n3. git commit -m \"t-up-local: <what changed>\"\n4. git push -u origin HEAD\n   (warning: upstream refs/heads/main is a local branch, not GitHub; the -u form publishes this branch to origin and re-points the upstream)\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  ctx| 4. git push -u origin HEAD
  ctx|    (warning: upstream refs/heads/main is a local branch, not GitHub; the -u form publishes this branch to origin and re-points the upstream)
  PASS  local, stop hook: exit 0
  PASS  local, stop hook: 4. git push -u origin HEAD
  PASS  local, stop hook: dirty:1 ahead:1
  PASS  local, stop hook: never HEAD:main
  PASS  local, stop hook: never a bare git push
  PASS  local, stop hook: the warning names the upstream
  PASS  local, snapshot: publish_line and upstream_ref
  session-start publish line: git push -u origin HEAD   (warning: upstream refs/heads/main is a local branch, not GitHub; the -u form publishes this branch to origin and re-points the upstream)
  session-start exit:
  0
  PASS  local, session-start: exit 0
  PASS  local, session-start: git push -u origin HEAD
  PASS  local, session-start: never HEAD:main
  PASS  local, session-start: the warning names the upstream
  -- backup: branch work/t-up-backup, upstream refs/remotes/backup/main
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-up-backup (t-up-backup): dirty:1 ahead:1 upstream:refs/remotes/backup/main. End the turn with, in this order:\n1. write handoffs/handoff-1-t-up-backup.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt handoffs/handoff-1-t-up-backup.md\n3. git commit -m \"t-up-backup: <what changed>\"\n4. git push -u origin HEAD\n   (warning: upstream refs/remotes/backup/main is on remote backup, not origin; the -u form publishes this branch to origin and re-points the upstream)\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  ctx| 4. git push -u origin HEAD
  ctx|    (warning: upstream refs/remotes/backup/main is on remote backup, not origin; the -u form publishes this branch to origin and re-points the upstream)
  PASS  backup, stop hook: exit 0
  PASS  backup, stop hook: 4. git push -u origin HEAD
  PASS  backup, stop hook: dirty:1 ahead:1
  PASS  backup, stop hook: never HEAD:main
  PASS  backup, stop hook: never a bare git push
  PASS  backup, stop hook: the warning names the upstream
  PASS  backup, snapshot: publish_line and upstream_ref
  session-start publish line: git push -u origin HEAD   (warning: upstream refs/remotes/backup/main is on remote backup, not origin; the -u form publishes this branch to origin and re-points the upstream)
  session-start exit:
  0
  PASS  backup, session-start: exit 0
  PASS  backup, session-start: git push -u origin HEAD
  PASS  backup, session-start: never HEAD:main
  PASS  backup, session-start: the warning names the upstream
  -- originx: branch work/t-up-originx, upstream refs/remotes/origin/x
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-up-originx (t-up-originx): dirty:1 ahead:0 upstream:origin/x. End the turn with, in this order:\n1. write handoffs/handoff-1-t-up-originx.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt handoffs/handoff-1-t-up-originx.md\n3. git commit -m \"t-up-originx: <what changed>\"\n4. git push origin HEAD:x\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  ctx| 4. git push origin HEAD:x
  PASS  originx, stop hook: exit 0
  PASS  originx, stop hook: 4. git push origin HEAD:x
  PASS  originx, stop hook: dirty:1 ahead:0
  PASS  originx, stop hook: never HEAD:main
  PASS  originx, stop hook: never a bare git push
  PASS  originx, stop hook: no warning
  PASS  originx, snapshot: publish_line and upstream_ref
  session-start publish line: git push origin HEAD:x
  session-start exit:
  0
  PASS  originx, session-start: exit 0
  PASS  originx, session-start: git push origin HEAD:x
  PASS  originx, session-start: never HEAD:main
  PASS  originx, session-start: no warning
  -- none: branch work/t-up-none, upstream none
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-up-none (t-up-none): dirty:1 ahead:1 upstream:none. End the turn with, in this order:\n1. write handoffs/handoff-1-t-up-none.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt handoffs/handoff-1-t-up-none.md\n3. git commit -m \"t-up-none: <what changed>\"\n4. git push -u origin HEAD\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  ctx| 4. git push -u origin HEAD
  PASS  none, stop hook: exit 0
  PASS  none, stop hook: 4. git push -u origin HEAD
  PASS  none, stop hook: dirty:1 ahead:1
  PASS  none, stop hook: never HEAD:main
  PASS  none, stop hook: never a bare git push
  PASS  none, stop hook: no warning
  PASS  none, snapshot: publish_line and upstream_ref
  session-start publish line: git push -u origin HEAD
  session-start exit:
  0
  PASS  none, session-start: exit 0
  PASS  none, session-start: git push -u origin HEAD
  PASS  none, session-start: never HEAD:main
  PASS  none, session-start: no warning
  -- originmain: branch work/t-up-originmain, upstream refs/remotes/origin/main
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-up-originmain (t-up-originmain): dirty:1 ahead:0 upstream:origin/main. End the turn with, in this order:\n1. write handoffs/handoff-1-t-up-originmain.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt handoffs/handoff-1-t-up-originmain.md\n3. git commit -m \"t-up-originmain: <what changed>\"\n4. git push -u origin HEAD\n   (warning: upstream refs/remotes/origin/main is main, never a publish target; the -u form publishes this branch to origin and re-points the upstream)\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  ctx| 4. git push -u origin HEAD
  ctx|    (warning: upstream refs/remotes/origin/main is main, never a publish target; the -u form publishes this branch to origin and re-points the upstream)
  PASS  originmain, stop hook: exit 0
  PASS  originmain, stop hook: 4. git push -u origin HEAD
  PASS  originmain, stop hook: dirty:1 ahead:0
  PASS  originmain, stop hook: never HEAD:main
  PASS  originmain, stop hook: never a bare git push
  PASS  originmain, stop hook: the warning names the upstream
  PASS  originmain, snapshot: publish_line and upstream_ref
  session-start publish line: git push -u origin HEAD   (warning: upstream refs/remotes/origin/main is main, never a publish target; the -u form publishes this branch to origin and re-points the upstream)
  session-start exit:
  0
  PASS  originmain, session-start: exit 0
  PASS  originmain, session-start: git push -u origin HEAD
  PASS  originmain, session-start: never HEAD:main
  PASS  originmain, session-start: the warning names the upstream
== case 17: the handoff by its exact name — next = max + 1 over the refs (the branch holds 3, a remote-only ref holds 9); 14 dirty paths keep the handoff in the add line and count the rest on the next line, a # comment; a handoff already written this turn is named once, never a second one ==
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-hand (t-hand): dirty:14 ahead:0 upstream:origin/work/t-hand. End the turn with, in this order:\n1. write handoffs/handoff-10-t-hand.md (recap first, newest first; 10 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- f01.txt f02.txt f03.txt f04.txt f05.txt f06.txt f07.txt f08.txt f09.txt f10.txt f11.txt f12.txt handoffs/handoff-10-t-hand.md\n   # + 2 more not listed: git status --porcelain\n3. git commit -m \"t-hand: <what changed>\"\n4. git push origin HEAD:work/t-hand\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  ctx| 1. write handoffs/handoff-10-t-hand.md (recap first, newest first; 10 = max over the refs, the other checkouts and the Drive ledger + 1)
  ctx| 2. git add -- f01.txt f02.txt f03.txt f04.txt f05.txt f06.txt f07.txt f08.txt f09.txt f10.txt f11.txt f12.txt handoffs/handoff-10-t-hand.md
  ctx|    # + 2 more not listed: git status --porcelain
  PASS  1. write handoffs/handoff-10-t-hand.md (refs hold 3 and 9: next is 10)
  PASS  the handoff does not exist yet
  PASS  14 paths: the add line shows 12, then the handoff
  PASS  the add line ends at the handoff: no note inside it
  PASS  the count of the rest on the next line, a # comment
  PASS  the git add line alone through bash -n (14 paths)
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-hand (t-hand): dirty:15 ahead:0 upstream:origin/work/t-hand. End the turn with, in this order:\n1. handoffs/handoff-10-t-hand.md is written and on no ref yet: keep its recap current (newest first)\n2. git add -- f01.txt f02.txt f03.txt f04.txt f05.txt f06.txt f07.txt f08.txt f09.txt f10.txt f11.txt f12.txt handoffs/handoff-10-t-hand.md\n   # + 2 more not listed: git status --porcelain\n3. git commit -m \"t-hand: <what changed>\"\n4. git push origin HEAD:work/t-hand\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  ctx| 1. handoffs/handoff-10-t-hand.md is written and on no ref yet: keep its recap current (newest first)
  ctx| 2. git add -- f01.txt f02.txt f03.txt f04.txt f05.txt f06.txt f07.txt f08.txt f09.txt f10.txt f11.txt f12.txt handoffs/handoff-10-t-hand.md
  ctx|    # + 2 more not listed: git status --porcelain
  PASS  written this turn: dirty:15 counts it
  PASS  1. names the written handoff
  PASS  no second handoff asked for (no handoff-11)
  PASS  the add line names it once, after the 12 shown paths
  PASS  the count of the rest on the next line, a # comment (the handoff not among them)
  PASS  the git add line alone through bash -n (15 paths)
== case 17b (KOM): a sibling worktree of the same repository holds an UNCOMMITTED handoffs/handoff-12-x.md — next is 13 in both hooks; a handoff-12 written here is a collision, named with the number to take ==
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-hand (t-hand): dirty:14 ahead:0 upstream:origin/work/t-hand. End the turn with, in this order:\n1. write handoffs/handoff-13-t-hand.md (recap first, newest first; 13 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- f01.txt f02.txt f03.txt f04.txt f05.txt f06.txt f07.txt f08.txt f09.txt f10.txt f11.txt f12.txt handoffs/handoff-13-t-hand.md\n   # + 2 more not listed: git status --porcelain\n3. git commit -m \"t-hand: <what changed>\"\n4. git push origin HEAD:work/t-hand\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  ctx| 1. write handoffs/handoff-13-t-hand.md (recap first, newest first; 13 = max over the refs, the other checkouts and the Drive ledger + 1)
  PASS  1. write handoffs/handoff-13-t-hand.md (the sibling holds 12)
  PASS  snapshot handoff_max_elsewhere 12
  session-start: newest here handoff-3-t-hand.md; next handoff number: 13 (max over the refs is 9, over the other checkouts on this Mac 12 ($SCRATCH/hand-wt), over the Drive ledger 0)
  PASS  session-start: next handoff number: 13, naming the other checkout
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-hand (t-hand): dirty:15 ahead:0 upstream:origin/work/t-hand. End the turn with, in this order:\n1. write handoffs/handoff-13-t-hand.md (recap first, newest first; 13 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- f01.txt f02.txt f03.txt f04.txt f05.txt f06.txt f07.txt f08.txt f09.txt f10.txt f11.txt f12.txt handoffs/handoff-13-t-hand.md\n   # + 3 more not listed: git status --porcelain\n3. git commit -m \"t-hand: <what changed>\"\n4. git push origin HEAD:work/t-hand\n   (handoffs/handoff-12-t-hand.md here is uncommitted and its number 12 is already held by the checkout $SCRATCH/hand-wt: rename it to handoff-13-<lane>.md before committing)\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  ctx| 1. write handoffs/handoff-13-t-hand.md (recap first, newest first; 13 = max over the refs, the other checkouts and the Drive ledger + 1)
  ctx|    (handoffs/handoff-12-t-hand.md here is uncommitted and its number 12 is already held by the checkout $SCRATCH/hand-wt: rename it to handoff-13-<lane>.md before committing)
  PASS  collision: the note names the file, the holder and the number to take
  PASS  collision: still asks for 13
  PASS  collision: the snapshot carries it
== case 17c (KOM): the Drive ledger — KOM_SHELF names a scratch shelf whose HANDOFFS/ holds handoff-20-drive.md: next is 21 in both hooks ==
  ctx| 1. write handoffs/handoff-21-t-hand.md (recap first, newest first; 21 = max over the refs, the other checkouts and the Drive ledger + 1)
  PASS  1. write handoffs/handoff-21-t-hand.md (the Drive ledger holds 20)
  session-start: newest here handoff-3-t-hand.md; next handoff number: 21 (max over the refs is 9, over the other checkouts on this Mac 12 ($SCRATCH/hand-wt), over the Drive ledger 20)
  PASS  session-start: next handoff number: 21 ... over the Drive ledger 20
  PASS  session-start: names the Drive ledger's 20
== case 18: the printed git add line is one valid shell command — 14 changed paths, the 12 listed named with shell metacharacters, a tab and a newline: the add line alone passes bash -n and evaluates to exactly those 12, then the handoff; the other 2 are counted on the next line, a # comment ==
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-over (t-over): dirty:14 ahead:0 upstream:origin/work/t-over. End the turn with, in this order:\n1. write handoffs/handoff-1-t-over.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- '#e.txt' '$(:).txt' $'a\\x0ab\\'c\\\\d.txt' 'a (1).txt' $'c\\x09d.txt' 'g`:`.txt' 'i;j.txt' 'it'\\''s.txt' 'k&l.txt' 'm|n.txt' 'o<p.txt' 'q*\"r.txt' handoffs/handoff-1-t-over.md\n   # + 2 more not listed: git status --porcelain\n3. git commit -m \"t-over: <what changed>\"\n4. git push origin HEAD:work/t-over\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  ctx| 2. git add -- '#e.txt' '$(:).txt' $'a\x0ab\'c\\d.txt' 'a (1).txt' $'c\x09d.txt' 'g`:`.txt' 'i;j.txt' 'it'\''s.txt' 'k&l.txt' 'm|n.txt' 'o<p.txt' 'q*"r.txt' handoffs/handoff-1-t-over.md
  ctx|    # + 2 more not listed: git status --porcelain
  bash -n on the printed git add line alone, exit:
  0
  PASS  exit 0
  PASS  dirty:14
  PASS  bash -n exit 0: the printed git add line alone is one valid shell command
  PASS  evaluated, the add line is exactly --, the 12 names in git status order, then the handoff
  PASS  the other 2 are counted on the next line, a # comment
  PASS  the 2 not listed are not on the add line
  PASS  the steps are still numbered 1 2 3 4 (no name split a line)
== case 19: paths named like git options — untracked --all and -e: the printed git add puts -- before its paths, so git reads both as paths ==
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-dash (t-dash): dirty:2 ahead:0 upstream:origin/work/t-dash. End the turn with, in this order:\n1. write handoffs/handoff-1-t-dash.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- --all -e handoffs/handoff-1-t-dash.md\n3. git commit -m \"t-dash: <what changed>\"\n4. git push origin HEAD:work/t-dash\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  ctx| 2. git add -- --all -e handoffs/handoff-1-t-dash.md
  PASS  exit 0
  PASS  dirty:2
  PASS  the add line reads git add -- --all -e handoffs/handoff-1-t-dash.md
  PASS  as shell words: --, then --all and -e as paths, then the handoff
  PASS  the git add line alone through bash -n
== sequence: prompt -> Stop (emits, 1) -> Stop stop_hook_active (emits, 2) -> Stop (silent, cap) -> prompt (reset) -> Stop (emits) ==
  kom-prompt.sh exit:
  0
  guard after prompt P1: P1:0   snapshot state: "working"
  PASS  prompt writes P1:0
  PASS  prompt marks working
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-dirty (t-dirty): dirty:2 ahead:0 upstream:origin/work/t-dirty. End the turn with, in this order:\n1. write handoffs/handoff-1-t-dirty.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt b.txt handoffs/handoff-1-t-dirty.md\n3. git commit -m \"t-dirty: <what changed>\"\n4. git push origin HEAD:work/t-dirty\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  Stop 1 emits
  PASS  Stop 1 says nudge 1 of 2
  PASS  guard P1:1
  PASS  snapshot state stopped after Stop 1
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-dirty (t-dirty): dirty:2 ahead:0 upstream:origin/work/t-dirty. End the turn with, in this order:\n1. write handoffs/handoff-1-t-dirty.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt b.txt handoffs/handoff-1-t-dirty.md\n3. git commit -m \"t-dirty: <what changed>\"\n4. git push origin HEAD:work/t-dirty\nNudge 2 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  Stop 2 (stop_hook_active) still emits — not an early return
  PASS  Stop 2 says nudge 2 of 2
  PASS  guard P1:2
  PASS  snapshot records stop_hook_active=true
  stdout: 
  exit:
  0
  PASS  Stop 3 silent (cap 2 reached)
  PASS  guard stays P1:2
  PASS  snapshot still written at the capped Stop (ts advanced)
  kom-prompt.sh exit:
  0
  PASS  prompt resets to P2:0
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-dirty (t-dirty): dirty:2 ahead:0 upstream:origin/work/t-dirty. End the turn with, in this order:\n1. write handoffs/handoff-1-t-dirty.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt b.txt handoffs/handoff-1-t-dirty.md\n3. git commit -m \"t-dirty: <what changed>\"\n4. git push origin HEAD:work/t-dirty\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  Stop 4 emits again after the reset
  PASS  guard P2:1
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-dirty (t-dirty): dirty:2 ahead:0 upstream:origin/work/t-dirty. End the turn with, in this order:\n1. write handoffs/handoff-1-t-dirty.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt b.txt handoffs/handoff-1-t-dirty.md\n3. git commit -m \"t-dirty: <what changed>\"\n4. git push origin HEAD:work/t-dirty\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  a new prompt_id without a prompt-hook write is a fresh turn: emits
  PASS  guard P3:1
  no prompt_id at all (older CLI): guard: unknown:1
  exit:
  0
  PASS  no prompt_id: guard unknown:1 after one emission
== the git shim: every git verb the hook called, and whether any write verb was attempted ==
   161 config
    47 diff-tree
    54 for-each-ref
   122 ls-tree
    50 remote
    58 rev-list
   223 rev-parse
    54 status
    54 symbolic-ref
    54 worktree
  PASS  no forbidden git verb reached the shim
  PASS  no hook stderr across every run carried FORBIDDEN
  hook stderr across every run: 0 bytes
== state transitions on a scratch branch (kom-status.py --repo --status-dir; its git fetch --prune origin served from a scratch bare repository standing in for GitHub; snapshots from real Stops of the hook) ==
  Stop 1 exit:
  0
  after Stop 1 (clean, pushed): {"fetch":"ok","state":"saved to GitHub","state_reason":null,"dirty":0,"ahead":0,"suffix":[],"commit_time":1790207723,"upstream_kind":"origin","origin_is_github":true,"origin_contains_head":true,"snapshot":"stopped"}
  PASS  the fetch ran and succeeded (fetch: ok)
  PASS  kom-status ran git fetch --prune ... origin (the shim's log)
  PASS  every fetch it ran carried --prune and named origin
  PASS  saved to GitHub after a clean pushed Stop
  PASS  on its evidence: an origin upstream, a GitHub origin URL, origin/<x> containing HEAD
  PASS  commit time equals git log -1 --format=%ct @{u} (1790207723)
  after touching a tracked file, no new Stop: {"fetch":"ok","state":"unsaved changes","state_reason":null,"dirty":1,"ahead":0,"suffix":["snapshot 16:55, files changed 16:55"],"commit_time":1790207723,"upstream_kind":"origin","origin_is_github":true,"origin_contains_head":true,"snapshot":"stopped"}
  PASS  unsaved changes
  PASS  suffix names the snapshot time
  PASS  suffix names the files-changed time
  after writing an ignored file (renders/frame.png), no new Stop: {"fetch":"ok","state":"working","state_reason":null,"dirty":1,"ahead":0,"suffix":["snapshot 16:55, files changed 16:55","untracked or ignored file newer than the snapshot: renders/frame.png"],"commit_time":1790207723,"upstream_kind":"origin","origin_is_github":true,"origin_contains_head":true,"snapshot":"stopped"}
  PASS  working (an ignored file newer than the snapshot)
  PASS  suffix names the ignored file
  Stop 2 (the continuation, stop_hook_active) exit:
  0
  after the continuation's Stop: {"fetch":"ok","state":"unsaved changes","state_reason":null,"dirty":1,"ahead":0,"suffix":[],"commit_time":1790207723,"upstream_kind":"origin","origin_is_github":true,"origin_contains_head":true,"snapshot":"stopped"}
  PASS  back to unsaved changes once a newer Stop snapshot exists
  prompt P2 exit:
  0
  after the next prompt (snapshot says working), no Stop yet: {"fetch":"ok","state":"working","state_reason":null,"dirty":1,"ahead":0,"suffix":["session s7 marked working at 16:55, no Stop since"],"commit_time":1790207723,"upstream_kind":"origin","origin_is_github":true,"origin_contains_head":true,"snapshot":"working"}
  PASS  working while the snapshot says working
  PASS  suffix says which session marked it working
  after a Stop, then commit, before publish: {"fetch":"ok","state":"not on GitHub","state_reason":null,"dirty":0,"ahead":1,"suffix":[],"commit_time":1790207723,"upstream_kind":"origin","origin_is_github":true,"origin_contains_head":false,"snapshot":"stopped"}
  PASS  not on GitHub
  PASS  origin/work/t-lane does not contain HEAD yet
  the publish, simulated (the stand-in GitHub fetches the branch; no git push anywhere), exit:
  0
  after publish, still no new Stop: {"fetch":"ok","state":"saved to GitHub","state_reason":null,"dirty":0,"ahead":0,"suffix":[],"commit_time":1790207727,"upstream_kind":"origin","origin_is_github":true,"origin_contains_head":true,"snapshot":"stopped"}
  PASS  saved to GitHub without a newer snapshot
  PASS  commit time equals %ct of @{u} after the publish (1790207727)
  --json | python3 -m json.tool exit:
  0
  plain| kom-status 2026-09-23 16:55 — 1 checkouts — fetch --prune origin: ok — snapshots read: 1 from $SCRATCH/status7
  plain| t-lane — saved to GitHub — commit time 1 s ago — handoff none — work/t-lane dirty:0 ahead:0 behind:0 — last file change 16:55 — $SCRATCH/lane7
  plain| shelf: no shelf/sync_shelf.py in this checkout
  the same clean, published checkout with --no-fetch: {"fetch":"skipped","state":"unknown","state_reason":"not fetched this run (--no-fetch)"}
  PASS  --no-fetch: unknown (not fetched this run), never saved to GitHub
  the same checkout with the fetch failing (offline): {"fetch":"failed","state":"unknown","state_reason":"fetch failed"}
  PASS  a failing fetch: unknown (fetch failed), never saved to GitHub
  claude/* worktree, no upstream, HEAD on origin/work/t-lane, handoff-2-t-lane.md uncommitted: {"state":"unknown","lane":"t-lane","lane_source":"guessed from handoffs/handoff-2-t-lane.md","last_handoff":2,"unknown_reason":"no upstream","suffix":["lane guessed from handoffs/handoff-2-t-lane.md: kom.lane unset (git config --worktree kom.lane <lane>)","1 uncommitted file(s)","HEAD is on origin/work/t-lane","set it: git branch --set-upstream-to=origin/work/t-lane","no snapshot"]}
  PASS  no upstream is unknown
  PASS  lane guessed from the newest handoff (t-lane)
  PASS  last handoff 2 (the ledger directory, uncommitted counts)
  PASS  suffix names the one origin ref holding HEAD and the upstream command
  paths inside either checkout newer than a marker made before two more scans: none
  PASS  the scan writes nothing inside any checkout (its one write is the fetch's, in the shared .git)
== evidence for saved to GitHub — a branch deleted on GitHub, a local upstream, another remote, an origin that is not GitHub (each its own scratch branch and stand-in GitHub) ==
  branch while the stand-in GitHub still has work/t-stale: {"fetch":"ok","state":"saved to GitHub","state_reason":null,"upstream":"origin/work/t-stale","upstream_kind":"origin","origin_is_github":true,"origin_contains_head":true,"suffix":["no snapshot"]}
  PASS  stale: saved to GitHub while the branch exists there
  work/t-stale deleted on the stand-in GitHub, exit:
  0
  the same branch after the deletion: {"fetch":"ok","state":"unknown","state_reason":"upstream gone: origin has no work/t-stale","upstream":null,"upstream_kind":null,"origin_is_github":null,"origin_contains_head":null,"suffix":["1 commit(s) on no remote ref","publish first: git push -u origin HEAD","no snapshot"]}
  PASS  stale: never saved to GitHub once the branch is gone
  PASS  stale: unknown (upstream gone: origin has no work/t-stale)
  git show-ref --verify refs/remotes/origin/work/t-stale exit:
  1
  PASS  stale: the fetch pruned refs/remotes/origin/work/t-stale (show-ref exit 1)
  a local upstream (refs/heads/main), clean: {"fetch":"ok","state":"not on GitHub","state_reason":"upstream is local","upstream":"main","upstream_kind":"local","origin_is_github":null,"origin_contains_head":null,"suffix":["publish first: git push -u origin HEAD","no snapshot"]}
  PASS  local upstream, clean: not on GitHub (upstream is local)
  --plain exit:
  0
  plain| kom-status 2026-09-23 16:55 — 1 checkouts — fetch --prune origin: ok — snapshots read: 1 from $SCRATCH/status7
  plain| t-localup — not on GitHub (upstream is local) (publish first: git push -u origin HEAD; no snapshot) — commit time ? — handoff none — work/t-localup dirty:0 ahead:0 behind:0 — last file change 16:55 — $SCRATCH/localup
  plain| shelf: no shelf/sync_shelf.py in this checkout
  PASS  local upstream, --plain reads: not on GitHub (upstream is local)
  the same local-upstream branch, dirty: {"fetch":"ok","state":"unsaved changes","state_reason":null,"upstream":"main","upstream_kind":"local","origin_is_github":null,"origin_contains_head":null,"suffix":["upstream is local","publish first: git push -u origin HEAD","no snapshot"]}
  PASS  local upstream, dirty: unsaved changes, the suffix still says upstream is local
  an upstream on another remote (backup/main), clean: {"fetch":"ok","state":"not on GitHub","state_reason":"upstream is on backup, not origin","upstream":"backup/main","upstream_kind":"remote backup","origin_is_github":null,"origin_contains_head":null,"suffix":["publish first: git push -u origin HEAD","no snapshot"]}
  PASS  another remote, clean: not on GitHub (upstream is on backup, not origin)
  origin on another host (a token in its URL), clean and level: {"fetch":"ok","state":"unknown","state_reason":"origin is not the GitHub repo: https://***@gitlab.com/Scroggdawg/kom-festival-board.git","upstream":"origin/work/t-notgh","upstream_kind":"origin","origin_is_github":false,"origin_contains_head":true,"suffix":["no snapshot"]}
  PASS  origin not GitHub: unknown (origin is not the GitHub repo), never saved
  PASS  origin not GitHub: the token in the URL is never printed
  PASS  status scanner wrote nothing to stderr
== case 20: one set of URLs through every redactor — plain https, https://user:token@, https://us@er:tok@en@, ssh git@host:path, ssh://user:token@host/, no credential (a port, an @ in the path): kom-status.py's redact_url and the redact of kom-stop.sh, kom-session-start.sh and kom-check.sh (cut out of the files, never run whole) print one credential-free line each; then the scp form with a token ==
  redactors.py exit:
  0
  redactors run: kom-status.py redact_url | kom-stop.sh redact | kom-session-start.sh redact | kom-check.sh redact
  PASS  all four redactors found and run
  1 plain https — https://github.com/Scroggdawg/kom-festival-board.git
    -> https://github.com/Scroggdawg/kom-festival-board.git   (kom-status.py redact_url, kom-stop.sh redact, kom-session-start.sh redact, kom-check.sh redact)
  2 https://user:token@ — https://user:token@github.com/Scroggdawg/kom-festival-board.git
    -> https://***@github.com/Scroggdawg/kom-festival-board.git   (kom-status.py redact_url, kom-stop.sh redact, kom-session-start.sh redact, kom-check.sh redact)
  3 https://us@er:tok@en@ — https://us@er:tok@en@github.com/Scroggdawg/kom-festival-board.git
    -> https://***@github.com/Scroggdawg/kom-festival-board.git   (kom-status.py redact_url, kom-stop.sh redact, kom-session-start.sh redact, kom-check.sh redact)
  4 ssh git@host:path — git@github.com:Scroggdawg/kom-festival-board.git
    -> git@github.com:Scroggdawg/kom-festival-board.git   (kom-status.py redact_url, kom-stop.sh redact, kom-session-start.sh redact, kom-check.sh redact)
  5 ssh://user:token@host/ — ssh://user:token@github.com/Scroggdawg/kom-festival-board.git
    -> ssh://***@github.com/Scroggdawg/kom-festival-board.git   (kom-status.py redact_url, kom-stop.sh redact, kom-session-start.sh redact, kom-check.sh redact)
  6 no credential: a port, an @ in the path — git+https://github.com:443/Scroggdawg/kom-festival-board.git@v1#egg=kom
    -> git+https://github.com:443/Scroggdawg/kom-festival-board.git@v1#egg=kom   (kom-status.py redact_url, kom-stop.sh redact, kom-session-start.sh redact, kom-check.sh redact)
  7 scp form with a token, user:token@host:path — user:token@github.com:Scroggdawg/kom-festival-board.git
    -> ***@github.com:Scroggdawg/kom-festival-board.git   (kom-status.py redact_url, kom-stop.sh redact, kom-session-start.sh redact, kom-check.sh redact)
  PASS  1 plain https — all four print https://github.com/Scroggdawg/kom-festival-board.git
  PASS  2 https://user:token@ — all four print https://***@github.com/Scroggdawg/kom-festival-board.git
  PASS  3 https://us@er:tok@en@ — all four print https://***@github.com/Scroggdawg/kom-festival-board.git
  PASS  4 ssh git@host:path — all four print git@github.com:Scroggdawg/kom-festival-board.git
  PASS  5 ssh://user:token@host/ — all four print ssh://***@github.com/Scroggdawg/kom-festival-board.git
  PASS  6 no credential: a port, an @ in the path — all four print git+https://github.com:443/Scroggdawg/kom-festival-board.git@v1#egg=kom
  PASS  7 scp form with a token, user:token@host:path — all four print ***@github.com:Scroggdawg/kom-festival-board.git
  PASS  no redactor prints a credential (user:, token, us@er, tok@en)
== case 21: a token is never printed — kom-status.py --json and --plain and both hooks, on branches whose origin or branch remote is https://me@example.com:S3CR3T@gitlab.com/... (an @ in the user part), a fetch error that quotes it, and a handoff recap that carries it ==
  (a) origin https://***@gitlab.com/Scroggdawg/kom-festival-board.git, clean and level: ["unknown","origin is not the GitHub repo: https://***@gitlab.com/Scroggdawg/kom-festival-board.git","https://***@gitlab.com/Scroggdawg/kom-festival-board.git"]
  PASS  (a) origin: unknown (origin is not the GitHub repo), its URL printed as https://***@gitlab.com/Scroggdawg/kom-festival-board.git
  PASS  (a) --plain names it the same way
  PASS  (a) the token is in neither --json nor --plain
  PASS  (a) nor the user part
  (b) branch.<b>.remote is the URL (what git push -u <url> writes; @{u} does not resolve): ["unknown","upstream gone: https://***@gitlab.com/Scroggdawg/kom-festival-board.git has no work/t-tokb"]
  PASS  (b) upstream gone, the remote printed as https://***@gitlab.com/Scroggdawg/kom-festival-board.git
  PASS  (b) the token is in neither --json nor --plain
  (c) the same URL as a remote with a fetch refspec (@{u} resolves to refs/remotes/glab/work/t-tokc), clean: ["not on GitHub","upstream is on https://***@gitlab.com/Scroggdawg/kom-festival-board.git, not origin","remote https://***@gitlab.com/Scroggdawg/kom-festival-board.git"]
  PASS  (c) not on GitHub; state_reason and upstream_kind print the remote as https://***@gitlab.com/Scroggdawg/kom-festival-board.git
  PASS  (c) the token is in neither --json nor --plain
  stdout: {"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[kom-stop] unpublished work on work/t-tokc (t-tokc): dirty:1 ahead:1 upstream:refs/remotes/glab/work/t-tokc. End the turn with, in this order:\n1. write handoffs/handoff-1-t-tokc.md (recap first, newest first; 1 = max over the refs, the other checkouts and the Drive ledger + 1)\n2. git add -- a.txt handoffs/handoff-1-t-tokc.md\n3. git commit -m \"t-tokc: <what changed>\"\n4. git push -u origin HEAD\n   (warning: upstream refs/remotes/glab/work/t-tokc is on remote https://***@gitlab.com/Scroggdawg/kom-festival-board.git, not origin; the -u form publishes this branch to origin and re-points the upstream)\nNudge 1 of 2 this turn. Never a bare git push. This hook pushed, added and stashed nothing. (KOM_STOP_GUARD=warn|off quiets it on this machine.)"}}
  exit:
  0
  PASS  (c) stop hook: the warning names the remote as https://***@gitlab.com/Scroggdawg/kom-festival-board.git
  PASS  (c) stop hook: the snapshot's publish_warning names it the same way
  PASS  (c) stop hook: the token is in neither its output nor its snapshot
  out| [kom] publish line: git push -u origin HEAD   (warning: upstream refs/remotes/glab/work/t-tokc is on remote https://***@gitlab.com/Scroggdawg/kom-festival-board.git, not origin; the -u form publishes this branch to origin and re-points the upstream)
  out| - pushed to https://***@gitlab.com/Scroggdawg/kom-festival-board.git, and the scp form ***@gitlab.com:Scroggdawg/kom-festival-board.git
  out| [kom] every turn ends: handoff in handoffs/ -> git add -- <paths> -> commit -> the publish line above. Read RUNBOOK.md before working.
  session-start exit:
  0
  PASS  (c) session-start: the publish warning names the remote as https://***@gitlab.com/Scroggdawg/kom-festival-board.git
  PASS  (c) session-start: the recap line prints both URLs redacted
  PASS  (c) session-start: the token is nowhere in its output
  (d) the fetch fails with an error that quotes the URL, token and all: ["failed","fatal: unable to access 'https://***@gitlab.com/Scroggdawg/kom-festival-board.git/': Could not resolve host: gitlab.com"]
  PASS  (d) fetch_detail prints the URL as https://***@gitlab.com/Scroggdawg/kom-festival-board.git
  PASS  (d) --plain prints the same detail
  PASS  (d) the token is in neither --json nor --plain
  PASS  kom-status.py wrote nothing to stderr in this case
  PASS  the git shim, whole run so far: no forbidden git verb (these hook runs included)
== settings.json: valid JSON; every hook command is bash "$CLAUDE_PROJECT_DIR/bin/hooks/<file>" and the file exists ==
  python3 -m json.tool exit:
  0
  SessionStart	bash "$CLAUDE_PROJECT_DIR/bin/hooks/kom-session-start.sh"
  UserPromptSubmit	bash "$CLAUDE_PROJECT_DIR/bin/hooks/kom-prompt.sh"
  Stop	bash "$CLAUDE_PROJECT_DIR/bin/hooks/kom-stop.sh"
  StopFailure	bash "$CLAUDE_PROJECT_DIR/bin/hooks/kom-stop.sh" --failure
  PASS  events are exactly SessionStart, UserPromptSubmit, Stop, StopFailure
  PASS  every command matches bash "$CLAUDE_PROJECT_DIR/bin/hooks/<name>.sh"[ --failure]
  PASS  StopFailure passes --failure
  PASS  exists: bin/hooks/kom-prompt.sh
  PASS  exists: bin/hooks/kom-session-start.sh
  PASS  exists: bin/hooks/kom-stop.sh
== session-start: CLAUDE_CODE_REMOTE=true says it is a cloud session and skips the shelf (scratch repo, no fetch); a local session runs the shelf tool's status ==
  out| [kom] work/t-ss — lane t-ss — upstream origin/work/t-ss — behind:0 ahead:0 dirty:1 (fetch: skipped) — checkout: $SCRATCH/ss
  out| [kom] publish line: git push origin HEAD:work/t-ss
  out| [kom] handoffs: newest here none; next handoff number: 1 (max over the refs is 0, over the other checkouts on this Mac 0, over the Drive ledger 0)
  out| [kom] cloud session: no Drive shelf on this machine — text, audit and page work only (shelf status skipped)
  out| [kom] every turn ends: handoff in handoffs/ -> git add -- <paths> -> commit -> the publish line above. Read RUNBOOK.md before working.
  exit:
  0
  PASS  exit 0
  PASS  cloud line present
  PASS  the shelf tool did not run
  local session (no CLAUDE_CODE_REMOTE), exit:
  0
  PASS  local session: no cloud line
  PASS  local session: the shelf tool is run
== pre-commit guard (bin/githooks/pre-commit) in a scratch repo with core.hooksPath set: a 60 MB blob, .env vs .env.example, a duplicate handoff number against a fake origin/main, two handoffs staged with one number, a home-folder literal in code vs a comment vs a docstring; a normal commit timed ==
  hook| REJECT big.bin: SIZE 60.0 MB > 50 MB — big files go to the Drive shelf (shelf/sync_shelf.py push)
  hook| pre-commit: 1 rejection(s) across 1 staged path(s); nothing committed
  git commit exit:
  1
  PASS  SIZE: a 60 MB blob is rejected
  PASS  SIZE line printed
  hook| REJECT .env: SECRET .env-named or private-context file
  hook| pre-commit: 1 rejection(s) across 2 staged path(s); nothing committed
  git commit exit:
  1
  PASS  SECRET: .env rejected
  PASS  SECRET: .env.example allowed (not rejected)
  hook| pre-commit: 1 staged path(s) OK
  git commit exit:
  0
  PASS  .env.example alone commits
  hook| pre-commit: 1 staged path(s) OK
  git commit exit:
  0
  PASS  a new handoff-005-a.md commits (nothing holds 005)
  hook| REJECT handoffs/handoff-005-b.md: HANDOFF number 005 already on origin/main in this ledger: handoffs/handoff-005-a.md — take max+1
  hook| REJECT handoffs/handoff-005-b.md: HANDOFF number 005 already in the index: handoffs/handoff-005-a.md — take max+1
  hook| pre-commit: 2 rejection(s) across 1 staged path(s); nothing committed
  git commit exit:
  1
  PASS  HANDOFF: number 005 already on origin/main (another lane) is rejected
  hook| REJECT handoffs/handoff-006-a.md: HANDOFF number 006 already in the index: handoffs/handoff-006-b.md — take max+1
  hook| REJECT handoffs/handoff-006-a.md: HANDOFF number 006 staged twice: handoffs/handoff-006-a.md, handoffs/handoff-006-b.md
  hook| REJECT handoffs/handoff-006-b.md: HANDOFF number 006 already in the index: handoffs/handoff-006-a.md — take max+1
  hook| REJECT handoffs/handoff-006-b.md: HANDOFF number 006 staged twice: handoffs/handoff-006-a.md, handoffs/handoff-006-b.md
  hook| pre-commit: 4 rejection(s) across 2 staged path(s); nothing committed
  git commit exit:
  1
  PASS  HANDOFF: two handoffs staged with one number are rejected
  hook| REJECT code.py: HOMEPATH new line 1 carries a '/Users/' literal outside a comment/docstring — use $HOME / os.path.expanduser / a repo-relative path
  hook| pre-commit: 1 rejection(s) across 1 staged path(s); nothing committed
  git commit exit:
  1
  PASS  HOMEPATH: a home-folder literal in code is rejected
  hook| pre-commit: 1 staged path(s) OK
  git commit exit:
  0
  PASS  HOMEPATH: the literal in a comment or docstring passes
  hook| pre-commit: 1 staged path(s) OK
  git commit exit:
  0
  PASS  a normal commit passes
  normal commit, seconds: 0.085
== timing: one dirty-tree Stop ==
  seconds: 0.312
== summary: PASS 322  FAIL 0 ==
harness exit:
0
```

Mutant suite:

```text
control: the unmutated copy — harness exit 0, PASS 322  FAIL 0 — passes, so each catch below is its defect's
mutant 1: stop_hook_active as an early return — harness exit 1, PASS 314  FAIL 8 — caught; first failing check: capped turn T1: snapshot still written, count 2
mutant 2: the prompt hook never resets the guard — harness exit 1, PASS 319  FAIL 3 — caught; first failing check: the prompt hook resets the guard to T2:0
mutant 3: the cap is 3, not 2 — harness exit 1, PASS 311  FAIL 11 — caught; first failing check: nudge 1 of 2
mutant 4: the snapshot is written after the cap return (order step 5 after step 6) — harness exit 1, PASS 316  FAIL 6 — caught; first failing check: capped turn T1: snapshot still written, count 2
mutant 5: subagents not exempt (agent_id ignored) — harness exit 1, PASS 319  FAIL 3 — caught; first failing check: agent_id variant: no output
mutant 6: origin not checked — harness exit 1, PASS 315  FAIL 7 — caught; first failing check: no output
mutant 7: a bare git push when there is no upstream — harness exit 1, PASS 305  FAIL 17 — caught; first failing check: publish is the -u form
mutant 8: warn is still a continuation — harness exit 1, PASS 316  FAIL 6 — caught; first failing check: a, warn: nothing to add; 1 commit not yet on GitHub; publish with: <the line>
mutant 9: fail open when the guard cannot be written — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: silent: a cap that cannot be recorded is never emitted
mutant 10: paths not shell-quoted — harness exit 1, PASS 319  FAIL 3 — caught; first failing check: the git add line parses to --, exactly the four paths, then the handoff
mutant 11: session-start ignores CLAUDE_CODE_REMOTE — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: cloud line present
mutant 12: kom-status ignores a snapshot that says working — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: working while the snapshot says working
mutant 13: stop: the audited publish logic (only the literal origin/main refused, remote prefix stripped) — harness exit 1, PASS 312  FAIL 10 — caught; first failing check: local, stop hook: 4. git push -u origin HEAD
mutant 14: session-start: the audited publish logic (only the literal origin/main refused, remote prefix stripped) — harness exit 1, PASS 315  FAIL 7 — caught; first failing check: local, session-start: git push -u origin HEAD
mutant 15: stop: main allowed as the push target — harness exit 1, PASS 316  FAIL 6 — caught; first failing check: publish is the -u form, never HEAD:main
mutant 16: session-start: main allowed as the push target — harness exit 1, PASS 319  FAIL 3 — caught; first failing check: originmain, session-start: git push -u origin HEAD
mutant 17: stop: ahead counted against a local or backup upstream — harness exit 1, PASS 319  FAIL 3 — caught; first failing check: local, clean: ahead is counted against origin, not the local upstream (dirty:0 ahead:1)
mutant 18: kom-status: one fetch without --prune — harness exit 1, PASS 317  FAIL 5 — caught; first failing check: kom-status ran git fetch --prune ... origin (the shim's log)
mutant 19: kom-status: any resolving upstream is evidence — harness exit 1, PASS 314  FAIL 8 — caught; first failing check: --no-fetch: unknown (not fetched this run), never saved to GitHub
mutant 20: kom-status: saved to GitHub without a successful fetch in this run — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: --no-fetch: unknown (not fetched this run), never saved to GitHub
mutant 21: kom-status: origin URL not checked — harness exit 1, PASS 319  FAIL 3 — caught; first failing check: origin not GitHub: unknown (origin is not the GitHub repo), never saved
mutant 22: stop, main: commit and publish before the handoff — harness exit 1, PASS 318  FAIL 4 — caught; first failing check: the steps are numbered 1 to 5
mutant 23: stop: the git add list built before the handoff exists — harness exit 1, PASS 313  FAIL 9 — caught; first failing check: 2. git add: --, the changed files, then the not-yet-written handoff by name
mutant 24: stop, clean but ahead: a handoff demanded, then nothing to add or commit — harness exit 1, PASS 318  FAIL 4 — caught; first failing check: b: 2. git add names the handoff alone, after --
mutant 25: stop, clean but ahead: no handoff demanded though the last commit carries none — harness exit 1, PASS 310  FAIL 12 — caught; first failing check: a: names the handoff the last commit carries
mutant 26: stop, clean but ahead: a handoff demanded though the last commit carries one — harness exit 1, PASS 317  FAIL 5 — caught; first failing check: a: nothing to add; 1 commit not yet on GitHub; publish with: <the line>
mutant 27: stop: the last commit read against each parent (-m): a merge of main borrows main's handoffs — harness exit 1, PASS 320  FAIL 2 — caught; first failing check: c: main's handoff-7-hub.md is not the merge's own: carries no handoff
mutant 28: stop: the '+ N more' note inside the git add line — harness exit 1, PASS 312  FAIL 10 — caught; first failing check: 14 paths: the add line shows 12, then the handoff
mutant 29: stop: a name with a control character left to @sh (its newline splits the git add line) — harness exit 1, PASS 319  FAIL 3 — caught; first failing check: bash -n exit 0: the printed git add line alone is one valid shell command
mutant 30: kom-status: redact_url cuts at the first @ — harness exit 1, PASS 305  FAIL 17 — caught; first failing check: origin not GitHub: unknown (origin is not the GitHub repo), never saved
mutant 31: kom-status: no scp rule (user:token@host:path printed as is) — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: 7 scp form with a token, user:token@host:path — all four print ***@github.com:Scroggdawg/kom-festival-board.git
mutant 32: kom-status: a gone upstream's remote printed as configured — harness exit 1, PASS 320  FAIL 2 — caught; first failing check: (b) upstream gone, the remote printed as https://***@gitlab.com/Scroggdawg/kom-festival-board.git
mutant 33: kom-status: upstream_kind carries the remote as configured — harness exit 1, PASS 319  FAIL 3 — caught; first failing check: (c) not on GitHub; state_reason and upstream_kind print the remote as https://***@gitlab.com/Scroggdawg/kom-festival-board.git
mutant 34: kom-status: git fetch's error text printed as is — harness exit 1, PASS 319  FAIL 3 — caught; first failing check: (d) fetch_detail prints the URL as https://***@gitlab.com/Scroggdawg/kom-festival-board.git
mutant 35: stop: the remote in the publish warning printed as configured — harness exit 1, PASS 319  FAIL 3 — caught; first failing check: (c) stop hook: the warning names the remote as https://***@gitlab.com/Scroggdawg/kom-festival-board.git
mutant 36: stop: redact without the scp rule — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: 7 scp form with a token, user:token@host:path — all four print ***@github.com:Scroggdawg/kom-festival-board.git
mutant 37: session-start: the remote in the publish warning printed as configured — harness exit 1, PASS 320  FAIL 2 — caught; first failing check: (c) session-start: the publish warning names the remote as https://***@gitlab.com/Scroggdawg/kom-festival-board.git
mutant 38: session-start: redact without the scp rule — harness exit 1, PASS 319  FAIL 3 — caught; first failing check: 7 scp form with a token, user:token@host:path — all four print ***@github.com:Scroggdawg/kom-festival-board.git
mutant 39: session-start: the recap printed as written — harness exit 1, PASS 320  FAIL 2 — caught; first failing check: (c) session-start: the recap line prints both URLs redacted
mutant 40: kom-check: redact without the scp rule — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: 7 scp form with a token, user:token@host:path — all four print ***@github.com:Scroggdawg/kom-festival-board.git
mutant 41: stop: the printed git add line without -- — harness exit 1, PASS 312  FAIL 10 — caught; first failing check: names a.txt and b.txt for git add, after --
mutant 42: stop, main: the branch's git add template without -- — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: on the branch, in order: write handoffs/handoff-1-<lane>.md, git add -- with it, git commit, publish
mutant 43: stop, warn: the dirty notice's git add without -- — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: warn: in order: the handoff, git add -- with it, commit, the publish line
mutant 44: stop, warn: the no-handoff notice's git add without -- — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: b, warn: the handoff alone to add, after --
mutant 45: stop (KOM): the next number ignores the other checkouts on this Mac — harness exit 1, PASS 317  FAIL 5 — caught; first failing check: 1. write handoffs/handoff-13-t-hand.md (the sibling holds 12)
mutant 46: stop (KOM): the next number ignores the Drive ledger — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: 1. write handoffs/handoff-21-t-hand.md (the Drive ledger holds 20)
mutant 47: session-start (KOM): the next number ignores the Drive ledger — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: session-start: next handoff number: 21 ... over the Drive ledger 20
mutant 48: stop (KOM): a colliding handoff number not reported — harness exit 1, PASS 320  FAIL 2 — caught; first failing check: collision: the note names the file, the holder and the number to take
mutant 49: stop (KOM): the lane never guessed from the newest handoff — harness exit 1, PASS 319  FAIL 3 — caught; first failing check: b: 1. write handoffs/handoff-6-epk.md (lane guessed from handoff-5-epk.md)
mutant 50: kom-status (KOM): the lane never guessed from the newest handoff — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: lane guessed from the newest handoff (t-lane)
mutant 51: pre-commit (KOM): the size limit dropped — harness exit 1, PASS 320  FAIL 2 — caught; first failing check: SIZE: a 60 MB blob is rejected
mutant 52: pre-commit (KOM): the handoff number not checked against origin/main — harness exit 1, PASS 321  FAIL 1 — caught; first failing check: HANDOFF: number 005 already on origin/main (another lane) is rejected
mutants caught: 52 of 52
mutant suite exit:
0
```
