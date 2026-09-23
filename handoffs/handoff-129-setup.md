# handoff-129-setup

## Where we left off, newest first

1. **The operating setup is built, proven and published (2026-09-23), on branch `claude/beautiful-elbakyan-a3e095`; Luke merges.** The branch sits on `origin/main` (785ddf0, handoff-127) plus two commits: the setup (d8a2b59) and this handoff (with the session-start recap fix and RUNBOOK §8.2's list of the twelve JPEGs). The recorded hook run follows in a third. Everything Petrol has, adapted: `RUNBOOK.md`, `AGENTS.md`, the three Claude hooks and the commit guard with their falsification harness, `bin/kom-status.py`, `bin/kom-check.sh`, the shelf tool with its registry, and one handoff ledger. Direction: Luke's four decisions in RUNBOOK §8 (turn the guard on; the twelve BTS JPEGs in git; the Drive mirror; registering send-ready folders). Nothing else is owed by this lane.

2. **The shelf is registered.** The Drive folder `My Drive/KILLER OF MEN` is stamped `.store_id` = `585e402c-d6f9-4974-88de-f4d87c4d0691`; `shelf/registry.json` names it and holds every file of `05 MARKETING/00 PRESS` except `EPK-2026-09-23/` (the EPK lane was writing it during this turn: register it when that lane says it is done): 292 files, 2,637,978,196 bytes, 0 problems, hashed over the Drive mount (the screener at 1.09 GB included). A second pass re-hashed every registered copy (`register --deep`): ok=292, copied=0, problems=0. Transcript: `shelf/REGISTER-2026-09-23.md`. `07 FESTIVALS` and `DELIVERY` are empty folders; `HANDOFFS` is text. The tool is Petrol's `sync_assets.py` v4 with this project's constants, a `register` mode (adopt what is already on the Drive), a refusal of bare pulls, and an allowance for Drive hydrating a file during its first read; its own falsification run, `shelf/FALSIFY-sync_shelf.md`, passes 91 checks and reads the real shelf once, where the tool refuses as designed.

3. **The hooks and the guard.** `bin/hooks/kom-stop.sh`, `kom-prompt.sh`, `kom-session-start.sh` are Petrol's with the ledger moved to `handoffs/`, the lane taken from `kom.lane` (else guessed from the newest handoff on a `claude/*` branch, said so), no lane renaming (publish is `git push -u origin HEAD` or `HEAD:<branch>`), and the next handoff number measured over the refs, every other checkout on this Mac and the Drive ledger, with a collision named when a written handoff reuses a number. `bin/githooks/pre-commit` refuses a blob over 50 MB, an `.env` file, a handoff number already on `origin/main`, a `/Users/` literal in new code; it is tracked, not installed (`core.hooksPath` is one line in the clone and reaches every worktree, other sessions included: Luke's call, RUNBOOK §8.1). The harness `bin/hooks/test-kom-stop.sh` passes 322 checks (PASS 322, FAIL 0, three runs in a row after two harness fixes); the recorded run with the mutant suite (a control copy, then 50 copies each carrying one defect, every one of which must fail the harness) was started at 23:52Z as this turn closed, about 30 minutes; its verdict and `bin/hooks/FALSIFY-kom-stop.md` land in the next handoff of this lane. Run by hand on this branch's index, the guard flagged exactly the four folded-in handoffs that reuse numbers 082 to 084 and 105 (history, recorded in LEDGER.md) and nothing else.

4. **One ledger.** `handoffs/LEDGER.md` carries the rule and the mapping table. Folded in verbatim: `104-festival` and `105-festival` (Drive only), `082-festival`, `083-connectors`, `084-bio` (untracked in the main checkout on this Mac since September 8 to 21, never committed). The EPK lane did the same fold-in on its branch the same afternoon and copied the five repo-only files onto the Drive (its handoff-128-epk); the copies are byte-identical in both branches, so the branches merge without conflict. Numbers 001 to 128 are all present now; the Drive `HANDOFFS/` is a mirror from here on, read only for the number.

5. **What a new session sees.** The session-start hook, run live on this checkout: branch, lane `setup` (set with `git config --worktree kom.lane setup`), upstream, `behind:0 ahead:0`, the publish line, `next handoff number: 129 (max over the refs is 128, over the other checkouts on this Mac 128, over the Drive ledger 128)`, this recap, and `shelf: registry 292 files; 0 pulled here; 292 not pulled (normal)`. `bash bin/kom-check.sh` prints `READY` with one WARN, the guard not installed.

## For Luke

The decisions are in RUNBOOK.md §8 and in the widget of this turn's readout: (1) turn the commit guard on in the main clone; (2) the twelve BTS JPEGs committed to git on September 8 (18 to 53 MB each; the shelf holds the same pictures); (3) keep or stop the Drive `HANDOFFS/` mirror; (4) register each `EPK-<date>/` send-ready folder when its lane is done. Merging this branch and the EPK lane's (`claude/vigorous-mayer-7773b9`, handoff-128) into main brings both; they do not conflict.

## What this turn did not do

- Did not set `core.hooksPath` (shared with other sessions' worktrees), did not push to main, did not deploy anything.
- Did not register `EPK-2026-09-23/` (live in the EPK lane) nor the empty `07 FESTIVALS` and `DELIVERY`.
- Did not touch `press/assets/BTS/` in git history, nor the Drive `HANDOFFS/` folder (the EPK lane wrote there).
- Wrote to the Drive once: `.store_id` and an empty `.locks/` folder at the root of `KILLER OF MEN`; nothing else on the shelf changed.

---

**Timestamp:** 2026-09-23 · **Lane:** `setup` (new; the KOM operating setup) · **Continues:** handoff-587-kom (OpenClaw, the brief) and handoff-127-epk (the base commit); beside handoff-128-epk (the EPK lane, same afternoon) · **Model:** Fable 5.1 (goose turn: a briefed build; the brief was the duck).

## Files

- RUNBOOK: file:///Users/scroggdawg/Code/kom-festival-board/.claude/worktrees/vigilant-newton-922afd/RUNBOOK.md
- AGENTS: file:///Users/scroggdawg/Code/kom-festival-board/.claude/worktrees/vigilant-newton-922afd/AGENTS.md
- Ledger rule and mapping: file:///Users/scroggdawg/Code/kom-festival-board/.claude/worktrees/vigilant-newton-922afd/handoffs/LEDGER.md
- Shelf README: file:///Users/scroggdawg/Code/kom-festival-board/.claude/worktrees/vigilant-newton-922afd/shelf/README.md
- Shelf registry: file:///Users/scroggdawg/Code/kom-festival-board/.claude/worktrees/vigilant-newton-922afd/shelf/registry.json
- Registration transcript and deep certificate: file:///Users/scroggdawg/Code/kom-festival-board/.claude/worktrees/vigilant-newton-922afd/shelf/REGISTER-2026-09-23.md
- Shelf tool falsification: file:///Users/scroggdawg/Code/kom-festival-board/.claude/worktrees/vigilant-newton-922afd/shelf/FALSIFY-sync_shelf.md
- Hook falsification (with mutants): file:///Users/scroggdawg/Code/kom-festival-board/.claude/worktrees/vigilant-newton-922afd/bin/hooks/FALSIFY-kom-stop.md
- The guard: file:///Users/scroggdawg/Code/kom-festival-board/.claude/worktrees/vigilant-newton-922afd/bin/githooks/README.md
- The branch on GitHub: https://github.com/Scroggdawg/kom-festival-board/tree/claude/beautiful-elbakyan-a3e095
- The EPK lane's branch (handoff-128): https://github.com/Scroggdawg/kom-festival-board/tree/claude/vigorous-mayer-7773b9
- The shelf: file:///Users/scroggdawg/Library/CloudStorage/GoogleDrive-camerawrap@gmail.com/My%20Drive/KILLER%20OF%20MEN
- The brief: file:///Users/scroggdawg/openclaw-handoffs/handoff-587-kom.md
- This handoff: file:///Users/scroggdawg/Code/kom-festival-board/.claude/worktrees/vigilant-newton-922afd/handoffs/handoff-129-setup.md
