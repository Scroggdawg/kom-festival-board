# AGENTS.md — for Codex (and any non-Claude agent) arriving on kom-festival-board

Claude sessions get their rules from the hooks in `.claude/settings.json` and from `RUNBOOK.md`; Codex loads this file. Same project, same rules. Read, in order:

1. `RUNBOOK.md` — what KILLER OF MEN's campaign runs on, what lives where (GitHub vs the Drive "shelf"), how to arrive on any Mac or account, the tools, the open decisions.
2. `README.md` — the surfaces (the board, the docket, the EPK worksheet) and the conventions of the data files.
3. `handoffs/LEDGER.md`, then the newest `handoffs/handoff-NNN-<lane>.md` for your lane — the current state. The EPK lane also keeps `handoffs/HARNESS-epk.md`, its standing pickup.
4. `BRAND.md` before any visual or copy work.

## Non-negotiables

- Never push to `main`. Work on a branch of your own (`git switch -c <lane>` from an up-to-date main, or a worktree) and publish with `git push -u origin HEAD`; Luke merges.
- Every turn ends in this order: write `handoffs/handoff-NNN-<lane>.md` (NNN = the highest number anywhere + 1: every branch, every checkout on this Mac, the Drive folder; `bash bin/kom-check.sh` prints it; the file must not exist before you write it), `git add -- <your paths> handoffs/handoff-NNN-<lane>.md`, commit, push.
- Never `git add -A`, `git stash`, `git reset`, `git checkout --`: other sessions share these checkouts. Add and commit by path.
- Big files are not in git. They live on the shelf (`My Drive/KILLER OF MEN`, a Google Drive folder) and are indexed by `shelf/registry.json`. Move them only with `python3 shelf/sync_shelf.py register|push|pull|verify --only "<shelf path>"`. Never a bare pull (the tool refuses it). Read every exit code unpiped, on its own line: 0 clean, 1 problems, 2 refused.
- Never delete anything; quarantine or move to a `z_Old_...` folder. No hard-coded home-folder paths in files: write `$HOME` or repo-relative paths.
- Never commit tokens, `.env` values, credential maps, cap-table or deal terms. Never deploy, push to Pages, or send anything outward without Luke's per-action OK.
- Luke is not a coder. Every readout to him is plain English: what happened, what it means, what he decides. A decision goes with its explanation.
- Machine readiness: `bash bin/kom-check.sh` (writes nothing). Where every checkout stands: `python3 bin/kom-status.py --plain`.

## What reaches Codex and what does not

- The git hook in `bin/githooks/pre-commit` (a blob over 50 MB, an `.env`-named file, a handoff number already on `origin/main`, a `/Users/` literal in new code) applies to any tool once the clone has run `git config core.hooksPath bin/githooks`. It is the guard that covers Codex commits.
- The Claude-only hooks in `.claude/` (the session-start recap, the end-of-turn reminder) do not run for Codex. Do the same by hand: before you stop, write the handoff, add by path, commit, push.
- Audits: the house rule for a cross-family review is `codex exec --sandbox read-only "…"` from the repo root. A contributing session writes inside its own branch only.
