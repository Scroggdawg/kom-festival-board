# handoff-029-docket

## Where we left off

**This turn (Sep 6, 2026, Opus 5, goose — ultracode):** Luke asked to click a subtask and cycle its status, with the change reaching the repo so another account and machine see it. Both write paths are built, reviewed, fixed and verified.

### What changed

| File | What |
|---|---|
| `docket.html` | The status dial is a button. Click or Enter cycles not started → started → awaiting response → complete. Two write paths, chosen by where the page is served from. |
| `tools/docket_server.py` | Localhost server. `POST /set` writes through `todo.py`, publishes ~4 s after the last click so a burst is one commit, pulls origin every 20 s, and reports the real push result on `/status`. Refuses Host and Origin that are not its own page. Refuses to run outside the Docket clone. |
| `tools/todo.py` | Gains `merge()`, compare-and-set on `set_status`, and a `push()` that merges instead of overwriting. `pull` added. |
| `~/.kom-docket` | **New: the Docket's own clone.** Its git work never touches the checkout the festival session shares. Marked by a `.docket-clone` file, which is what `push()` and the server check before doing anything destructive. |

### The two paths

- **Laptop, `http://localhost:8642/docket.html`** — the page posts to the local server, which writes `todo.json` and pushes. No token anywhere.
- **Any machine or phone, the published copy** — the page reads and writes `todo.json` straight through `api.github.com`, sha-bound, with a fine-grained token the viewer pastes once. Same storage key as the board, so one token serves both pages. With a token it polls GitHub with an ETag every 10 s and sees the truth immediately; without one it reads the published copy, about a minute behind, and clicking asks for a token.

### The review, and what it caught

A five-dimension adversarial workflow (92 agents, three refuters per finding) reviewed the first build. It confirmed a serious flaw: on a rejected push the old code stamped this machine's `todo.json` over origin's tree, so **a status set on the phone was destroyed by the next click on the laptop**, silently, with the rev number matching either way. It also left every other file that had landed on origin staged as a reversion in the shared checkout. Three verifiers reproduced both effects in sandboxes.

The fix is the dedicated clone plus a real merge: origin is the base, per item the side with the newer history entry wins, both histories are kept. Also fixed from the same review: compare-and-set so a click on a stale row is refused rather than silently reverting someone; re-render keyed on rev, time and writer together, since two writers bump rev from the same base; colours validated before reaching the DOM; a 403 no longer deletes the token, only a 401 does; the provenance ticker no longer wipes an error a second after it appears; and the page no longer claims a change was published before the push actually returned.

### Verified

Merge unit cases (different items, same item either direction, identical, stale local, remote-only item) all pass. End to end against the real remote: a phone write followed by a laptop click on a stale copy keeps both. The clone takes origin's changes on its own. In the browser: the four-way cycle, the conflict refusal, the published-at line, error persistence and recovery, no stuck rows. The published page reads correctly and asks for a token on click. The GitHub write path was exercised with a mocked transport — request shape, sha, branch, message, history entry, and a byte-identical JSON round trip against `todo.py`'s own formatting — but **no real token has been used, so the last inch of that path is unproven until Luke clicks once from the published copy**.

### Housekeeping

Tonight's tests wrote real statuses and a simulated second machine into the history. `todo.json` was reset to the seed state and published: 37 items, all not started, no history beyond the seed.

---

**Timestamp:** 2026-09-06
**Lane:** `docket`
**Continues:** handoff-028-docket.md
**Model:** Opus 5. **Goose turn** — built, reviewed by workflow, rebuilt, verified.

## Next action (the one thing)

**Luke: open the published page on the phone, add a fine-grained token, and click one status.** That proves the last unproven inch. Then the Docket is just: tell it a change, or click it.

## Files

- Live page, laptop: http://localhost:8642/docket.html
- Live page, anywhere: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/todo.py
- Server: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/docket_server.py
- Page: https://github.com/Scroggdawg/kom-festival-board/blob/main/docket.html
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-028-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-029-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-473-docket.md
