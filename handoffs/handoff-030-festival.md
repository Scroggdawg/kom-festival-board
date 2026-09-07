# handoff-030-festival

## Where we left off

**This turn (Sep 6, 2026, Fable 5.1):** Luke reported two things about the preview: it showed "an old version of the widget," and clicking a dial did nothing. The first was the festival board (`index.html` at the server root) not the Docket (`/docket.html`); the second was real — I had shipped the page read-only. Before I could fix it, the **Docket session** (lane `docket`, its own clone at `~/.kom-docket`) reported click-to-write shipped and verified, with a 92-agent review that caught and fixed a destructive push in its first build (see `handoffs/handoff-029-docket.md`).

Done here: stopped my duplicate :8642 server; pulled the Docket session's work (`todo.json` rev 24, seed state; `tools/todo.py` with merge + compare-and-set; `tools/docket_server.py`; `docket.html` with two write paths — localhost POST, or GitHub API with a pasted token on the published copy); **added a "☰ The Docket" link to the board's header** (the one item the Docket session left to me) and pushed.

Rules from the Docket session, now standing for this lane: pull before touching `todo.py`, `docket_server.py`, `docket.html`; never run `docket_server.py` from this checkout (it refuses without the `.docket-clone` marker); the Docket's server runs from the clone on :8642.

---

**Timestamp:** 2026-09-06
**Lane:** `festival`
**Continues:** handoff-027-festival.md (028–029 are the `docket` lane)
**Model:** Fable 5.1. Small goose turn — sync, one link, no other change.

## Next action (the one thing)

**Luke: open http://localhost:8642/docket.html (not the root) and click a dial** — that is the laptop path. For the phone, the published page needs a fine-grained token pasted once; the Docket session's handoff says that last inch is unproven until he clicks. Festival lane after that: rewrite `PLAN-docket.md` to what shipped; the nine discount emails are still at bat.

## Files

- Docket, laptop: http://localhost:8642/docket.html
- Docket, anywhere: https://scroggdawg.github.io/kom-festival-board/docket.html
- Board (now links to the Docket): https://scroggdawg.github.io/kom-festival-board/
- Docket handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-029-docket.md
- Prior festival handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-027-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-030-festival.md
