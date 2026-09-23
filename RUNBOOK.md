# RUNBOOK — arriving at KILLER OF MEN on any Mac, either Claude login, a cloud session, or Codex

*2026-09-23, KOM operating setup build 1, from Petrol's (`petrol-brand-bible` RUNBOOK.md, 2026-09-22). Main clone on this Mac: `$HOME/Code/kom-festival-board`; the app's worktrees under its `.claude/worktrees/`. Exit codes: the command, then `echo $?` on its own line.*

## 1. What lives where

| Place | Holds |
|---|---|
| **The repo** (`Scroggdawg/kom-festival-board`, public, GitHub Pages) | the festival board, the docket, the EPK worksheet and its tools, research, reviews, the handoff ledger `handoffs/`, the shelf registry `shelf/registry.json`, the hooks (`.claude/settings.json`, `bin/hooks/`), the commit guard (`bin/githooks/`), `bin/kom-status.py`, `bin/kom-check.sh`, `shelf/sync_shelf.py`. Words, code, small files. The only place work is safe. |
| **The shelf** (`My Drive/KILLER OF MEN`, camerawrap@gmail.com's Google Drive) | the big files: `05 MARKETING/00 PRESS` (stills, BTS, poster, kit PDFs, Illustrator sources, the screener, laurels, logos, captions), `05 MARKETING/07 FESTIVALS`, `DELIVERY`, and `HANDOFFS` (a mirror of the ledger). Follows the Google login, not the Claude login. Indexed by `shelf/registry.json`; see `shelf/README.md`. |
| **This Mac only** | `$HOME/.kom/status/` (the hooks' snapshots), `shelf/local/` (pulled copies), `.kom/locks/`, `.git/config` (`core.hooksPath`, `kom.lane`), the Drive mount, the gh login. |
| **Never in git** | tokens, `.env*` values, credential maps, cap-table or deal terms, home-folder literals in code, a blob over 50 MB. The commit guard catches the last three; the rest is discipline. |

Known deviation: twelve behind-the-scenes JPEGs of 18 to 53 MB were committed under `press/assets/BTS/` on September 8, before this setup existed (the same pictures are on the shelf under `00 PRESS/BTS/`). They stay until Luke rules on a supervised move; the guard stops the next one (§8).

## 2. What the readouts say

`bash bin/kom-check.sh` (read-only) prints one `CHECK|OK|...` line per item and `READY` or `NOT READY` last. `python3 bin/kom-status.py --plain` prints one line per checkout of this repository on this Mac, then the branches only GitHub holds, then the shelf line:

| Words | Means; do |
|---|---|
| **saved to GitHub** | nothing unsaved, and GitHub already holds this commit, confirmed by a fresh fetch this run; safe to switch login or Mac |
| **unsaved changes** / **not on GitHub** | not committed / not pushed; end the turn (§4) |
| **working** / **unknown** | a session is mid-turn, wait / no upstream, fetch failed or a missing piece of evidence, look at the reason in brackets |
| **on GitHub, no local view** | a branch only GitHub holds (the laptop, a cloud session), with its commit time and newest handoff |
| **handoff 127** | the newest handoff in that checkout's `handoffs/`; read it first |
| **shelf: This Mac: 0 of 292 shelf files pulled** | normal: the Drive mount serves the files; `pull --only <path>` only what a build needs a checked copy of |

## 3. Arriving: five paths

**A. This Mac (the Hive): under 2 minutes**

1. Open the repo in the Claude desktop app's Code tab; it makes a worktree and a `claude/<name>` branch. Or by hand: `cd "$HOME/Code/kom-festival-board" && git pull --ff-only` (main; never commit here), then `git switch -c <lane>`.
2. `bash bin/kom-check.sh`. Expect `READY`; the one WARN today is `git_guard` until `git config core.hooksPath bin/githooks` is run once per clone (§7).
3. Read the session-start lines (`[kom] ...`): branch, lane, publish line, next handoff number, the newest handoff's recap. Then `RUNBOOK.md` once, and the newest `handoffs/handoff-NNN-<lane>.md` for your lane. The EPK lane also has `handoffs/HARNESS-epk.md`.
4. Set the lane so the hooks stop guessing: `git config --worktree kom.lane <lane>` (lanes so far: festival, docket, epk, cast, connectors, bio, setup).

**B. Another Mac: about 10 minutes**

1. `brew install gh jq && gh auth login` (GitHub `Scroggdawg`); python3 3.9 or newer is on every Mac.
2. Drive for desktop signed in as camerawrap@gmail.com, so `My Drive/KILLER OF MEN` is mounted (another account: §6).
3. `gh repo clone Scroggdawg/kom-festival-board "$HOME/Code/kom-festival-board"` (about 400 MB with the BTS pictures in history), then steps A2 to A4.

**C. The other Claude login on the same Mac: under 2 minutes**

1. Let every turn finish; switch only when `python3 bin/kom-status.py --plain` shows each local checkout `saved to GitHub`, or its handoff names what stays off GitHub.
2. Switch the desktop login, open the same folder, read the session-start lines and the recap. Nothing to install: the repo, the hooks, the shelf and the gh login all follow the machine.

**D. A cloud session (claude.ai/code), either login**

1. Once per login: `/web-setup` from a Mac where `gh auth status` is green.
2. A single-repo session on this repo, on a branch, never main. The session-start line says `cloud session: no Drive shelf on this machine`; text, audit and page work only; no shelf commands, no secrets.
3. End turns per §4; the Hive's status lists the branch under `on GitHub, no local view`.

**E. A Codex session (or any non-Claude agent)**

1. Open a terminal in a worktree or clone on its own branch. Codex reads `AGENTS.md` at the repo root on start; it carries the same rules.
2. `bash bin/kom-check.sh`, then `python3 bin/kom-status.py --plain`, then the newest handoff for the lane.
3. Before stopping: write `handoffs/handoff-NNN-<lane>.md`, `git add --` by path (the handoff included), commit, `git push -u origin HEAD`. The Claude hooks do not fire for Codex; the git guard does.

## 4. Every turn, every lane

- **Every turn ends** in this order: write `handoffs/handoff-NNN-<lane>.md` (recap first, newest first; NNN = the next number the session-start line printed, re-checked with `bash bin/kom-check.sh` at the end), `git add -- <the changed paths> handoffs/handoff-NNN-<lane>.md`, commit, then the publish line the Stop hook prints (`git push origin HEAD:<branch>` once the branch is on GitHub, `git push -u origin HEAD` the first time). The Stop hook prints these four lines when a turn ends with work unpublished, twice per turn at most; `KOM_STOP_GUARD=warn` turns the continuation into a one-line notice, `off` silences it on this machine.
- **Never push to main.** Luke merges branches into main. The hooks print no publish line on main.
- **Never `git add -A`, `git stash`, `git reset`, `git checkout --`:** other sessions share the checkouts. Add by path; commit by path.
- **Never a bare pull of the shelf:** `pull --only <path>`, always (the tool refuses a bare one).
- **Never delete:** the tool quarantines; a person moves a file to a `z_Old_...` folder. Nothing on the shelf or in the ledger is removed.
- **Plain English for Luke.** He is not a coder: a readout tells him what happened and what it means; a decision goes in a widget with the explanation one tap away; a product surface carries no flourish.
- Say whether the turn was a duck (plan, Opus) or a goose (build, Fable, briefed).

## 5. Accounts and cloud

| Account | Holds | Follows |
|---|---|---|
| GitHub `Scroggdawg` (`gh auth login`) | the repo, GitHub Pages | the machine |
| Google camerawrap@gmail.com (Drive for desktop) | the shelf | the machine |
| The two Claude logins | sessions, cloud environments, artifact links; only branch and handoff cross logins | the login |
| Canva (the EPK design) | the press-kit master; the claude.ai connector edits it (HARNESS-epk) | the login the connector is on |

`main` is unprotected (a public repo could carry rulesets; none is set). §4's rule holds by habit and by the hooks, which never print a push to main.

## 6. The shelf, and a Mac whose Drive is another account

`shelf/README.md` is the reference. In short: the folder carries `.store_id` = `585e402c-d6f9-4974-88de-f4d87c4d0691`; `shelf/registry.json` names it and holds one sha256 per shelf file (292 under `00 PRESS` today, 2.64 GB); `register --only` adopts what is already there, `push --only` puts a new file there, `pull --only` fetches a checked copy into `shelf/local/`, `status` never opens the shelf. Every displaced copy goes to a `.quarantine/` folder with a line in its `INDEX.tsv`.

On a Mac whose Drive is another account:

1. From camerawrap@gmail.com, share the folder with it: Viewer to `pull` and `verify`, Editor to `push`.
2. In that account's Drive, add a shortcut to it in My Drive so `ls -d "$HOME"/Library/CloudStorage/GoogleDrive-*/"My Drive/KILLER OF MEN"` prints one path.
3. Two Drive accounts signed in: the tool will not guess; put `export KOM_SHELF="$HOME/Library/CloudStorage/GoogleDrive-<account>/My Drive/KILLER OF MEN"` in `~/.zshenv`.
4. Prove it: `cat "$KOM_SHELF/.store_id"` prints the id above; `python3 shelf/sync_shelf.py verify --only "05 MARKETING/00 PRESS/POSTER"`, then `echo $?`, prints 0 (with `NOT PULLED` lines: nothing is local yet).
5. Never create or stamp a second shelf; a share is the same shelf.

## 7. The hooks and the guard

| Piece | Runs when | Does |
|---|---|---|
| `bin/hooks/kom-session-start.sh` | a Claude session opens | one bounded fetch; prints branch, lane, upstream, behind/ahead/dirty, the publish line, the next handoff number (max over refs, the other checkouts on this Mac, and the Drive ledger, + 1), the newest handoff's recap, the shelf's local status. Read-only. |
| `bin/hooks/kom-prompt.sh` | every prompt | resets the Stop hook's per-turn cap; marks the session `working` for the status script. Prints nothing. |
| `bin/hooks/kom-stop.sh` | a turn ends | writes a snapshot under `$HOME/.kom/status/`; if work is unpublished, prints the four lines of §4 in order (the handoff by its exact name first; `git add --` by path; commit; the publish line), twice per turn at most; never pushes, adds, stashes or blocks; on main says to move to a branch. Names a handoff whose number another checkout or the Drive already holds. |
| `bin/githooks/pre-commit` | every `git commit`, once `git config core.hooksPath bin/githooks` is set in the clone | refuses a blob over 50 MB, an `.env`-named file, a handoff number already on `origin/main`, a `/Users/` literal in new code. Works for Codex too. |
| `bin/kom-status.py` | on demand | §2 |
| `bin/kom-check.sh` | on demand | §2 |

Proof: `bin/hooks/FALSIFY-kom-stop.md` (the recorded run of `bin/hooks/test-kom-stop.sh`: scratch repos, a git shim that refuses every write verb, a stand-in GitHub, and a mutant suite in which every deliberately broken copy must fail) and `shelf/FALSIFY-sync_shelf.md`. Re-run either with the line at its top before changing the file it certifies.

## 8. Open decisions (Luke's)

1. **Turn the commit guard on** in the main clone: `git config core.hooksPath bin/githooks` (one line; it applies to every worktree of that clone, other sessions included, so it was not set for them here).
2. **The twelve BTS JPEGs in git** (`press/assets/BTS/`, committed September 8, 361 MB together; the shelf holds the same pictures under `00 PRESS/BTS/`): leave them, or a later supervised move off history. Leaving them costs nothing but clone time. They are `IMG_4616.jpg` 52.9 MB, `IMG_4408.jpg` 44.9, `IMG_4514.jpg` 44.7, `IMG_4467.jpg` 43.9, `_DSF5180.JPG` 26.4, `_DSF5055.JPG` 26.3, `_DSF6428.jpg` 23.9, `DSCF4727.JPG` 21.9, `DSCF4802.JPG` 19.7, `DSCF4696.JPG` 19.3, `DSCF4718.JPG` 18.8, `_DSF6499.jpg` 18.3; the first four are over GitHub's 50 MB warning line, none over its 100 MB refusal.
3. **The Drive `HANDOFFS/` mirror**: keep copying handoffs there (harmless), or stop (the hooks only read it for the number).
4. **`EPK-2026-09-23/` and future send-ready folders**: register each one on the shelf when its lane is done (`register --only "05 MARKETING/00 PRESS/EPK-<date>"`), so the registry names what was sent.
