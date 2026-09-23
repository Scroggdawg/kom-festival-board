# shelf/ — the Drive shelf, indexed in git

*2026-09-23, KOM build 1. Tool: `shelf/sync_shelf.py` (Petrol's `sync_assets.py` v4 with this project's names and one added mode; its falsification run is `shelf/FALSIFY-sync_shelf.md`, re-run with `bash shelf/test-sync_shelf.sh --record shelf/FALSIFY-sync_shelf.md`). Registry: `shelf/registry.json` (committed). Local mirror: `shelf/local/` (gitignored, empty until something is pulled).*

## What the shelf is

The Google Drive folder **`My Drive/KILLER OF MEN`** in camerawrap@gmail.com's Drive, mounted on this Mac at `$HOME/Library/CloudStorage/GoogleDrive-camerawrap@gmail.com/My Drive/KILLER OF MEN`. It holds the big files: press stills, behind-the-scenes photographs, the poster, the kit PDFs and their old versions, the Illustrator sources, the screener (1.09 GB), laurels, logos, captions. Git holds the words, the code, the small files, and **this registry**: one sha256 per shelf file, so any machine can tell what the shelf holds and whether a copy is the right bytes.

The shelf carries a stamp, `.store_id` = `585e402c-d6f9-4974-88de-f4d87c4d0691`, which the registry names. The tool refuses to touch a folder whose stamp is not the registry's (`WRONG STORE`, exit 2), so a wrong Drive account or a copied folder can never be written into by mistake. **Never stamp a second folder.**

Bases (the four Drive subfolders; every file under them, keys are shelf-relative paths):

| Base | Registered 2026-09-23 | Note |
|---|---|---|
| `05 MARKETING/00 PRESS` | 292 files, 2.64 GB, every subfolder except `EPK-2026-09-23` | the press assets; the EPK lane writes `EPK-<date>/` send-ready folders here — register one when its lane says it is done |
| `05 MARKETING/07 FESTIVALS` | nothing: its seven subfolders are empty | register when files arrive |
| `DELIVERY` | nothing: empty | register when files arrive |
| `HANDOFFS` | nothing registered | a text mirror of `handoffs/` (see `handoffs/LEDGER.md`); registering it is optional |

Never covered: `.DS_Store`, `.store_id`, `.locks/`, `.quarantine/`, and Drive's document shortcuts (`.gdoc`, `.gsheet`, ...; they hold a URL, not the document).

## The commands (from the repo root; every exit code read on its own line)

| Command | What it does | Touches the shelf |
|---|---|---|
| `python3 shelf/sync_shelf.py register --only "<shelf path>"` | adopt what is already on the shelf: hash every file under the path the registry does not know and write its line. Registered keys count `ok` by size; `--deep` hashes them too; a copy that differs from its line is `STORE DIFFERS FROM REGISTRY`, re-registered only with `--force`. Never copies bytes. | reads |
| `python3 shelf/sync_shelf.py push --only "<shelf path>"` | `shelf/local/<path>` → shelf, then registers. A shelf copy the registry does not know, or that differs from it, is `STORE CONFLICT (hash)`: nothing copied unless `--force`, which moves the displaced copy to the shelf's `.quarantine/` first. A registered file edited locally is `LOCAL CHANGED` unless `--update`. | writes |
| `python3 shelf/sync_shelf.py pull --only "<shelf path>"` | shelf → `shelf/local/<path>`, checked against the registry. A differing local file goes to `shelf/local/.quarantine/`. **A bare `pull` is refused.** | reads |
| `python3 shelf/sync_shelf.py verify --only "<shelf path>" [--deep] [--strict]` | both sides against the registry. A registered file not pulled is `NOT PULLED`, never a problem. | reads |
| `python3 shelf/sync_shelf.py status` | the local view only; never opens a shelf file (the session-start hook runs this). | never |
| `python3 shelf/sync_shelf.py merge-registry <other.json>` | union by key; any conflict refuses with nothing written. | never |
| `python3 shelf/sync_shelf.py --version` | `sync_shelf 4 (KOM build 1)` | never |

Exit codes: **0** ran clean, **1** ran and found problems (read the labelled lines), **2** refused before touching anything (no shelf, wrong stamp, `--only` matching nothing, a flag on the wrong mode, a bare pull, ...). The last line is always `SYNC|<mode>|ok= copied= ...|registry= store=`.

The environment variable `KOM_SHELF` names the folder explicitly (needed only when two Drive accounts are signed in, or the folder is a shortcut with another name).

## Putting a new big file on the shelf

1. Put it at `shelf/local/<where it goes on the shelf>` (make the folders).
2. `python3 shelf/sync_shelf.py push --only "<that path>"`, then `echo $?` on its own line: 0.
3. Commit `shelf/registry.json` with the work. The bytes are on the Drive; the line that proves them is in git.

A file dropped straight into the Drive folder (Finder, a Canva export, another lane's script) is fine too: `register --only` its folder afterwards, and commit the registry.

## Nothing is deleted

A copy the tool displaces, on either side, moves to that side's `.quarantine/<key>.<UTC>.<sha256 first 12>` and gets one line in `.quarantine/INDEX.tsv`; the tool never removes a payload. Registry lines are removed only by an explicit `push --prune --yes`, never by a file being absent.

## What Petrol's tool guarantees, and this one keeps

Every store write runs under a per-key lock; a store copy that changed after it was hashed is `STORE CHANGED DURING PUSH`, nothing copied; installs are `link()` calls that fail rather than replace a path; the registry is saved under a lock and merged with lines other runs saved meanwhile. The audit history (four Codex rounds) is in Petrol's `blender/scripts/harness/FALSIFY-sync_assets-v4.md`; the parts that changed here are the constants at the top of the file, the `register` mode, the bare-pull refusal and the Drive-hydration allowance in `shelf_hash()`, each marked `KOM` in the source.
