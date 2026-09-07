# handoff-028-docket

## Where we left off

**This turn (Sep 6, 2026, Fable 5.1, goose — Docket session start):** the Docket session came up for the first time.

- Pulled. `todo.json` is at rev 3, all 37 items not started (rev 2–3 were the festival session's live-update demo, reverted to seed in `20a1778`).
- Port 8642 was already held by the festival session's server, serving the **main checkout** (`/Users/scroggdawg/Code/kom-festival-board`). This session runs in a worktree, so its own copy would never reach that page. Decision: the Docket writes and pushes against the main checkout (`python3 /Users/scroggdawg/Code/kom-festival-board/tools/todo.py …`), never `cd`-ing there. Worktree branch `claude/frosty-moore-f514b1` is unused.
- Page verified in the Browser pane: http://localhost:8642/docket.html renders, polling, provenance line shows rev 3.
- New: `tools/widget.py` — renders `todo.json` as the in-chat widget fragment, same markup and colours as `docket.html`, footer says `snapshot · rev · written`. Read-only.
- Widget rendered in chat from rev 3.

**Open:** the 8642 server belongs to another chat; if that session ends, the page dies until this one starts its own (`preview_start` "docket" would then bind 8642 from the worktree, which is the wrong directory — start it from the main checkout instead, or point launch.json at it). The five section colours still unvalidated as a set. `PLAN-docket.md` still stale (festival lane's job).

---

**Timestamp:** 2026-09-06
**Lane:** `docket`
**Continues:** handoff-027-festival.md
**Model:** Fable 5.1. **Goose turn** — session start, renderer added.

## Next action (the one thing)

Wait for Luke's first change. Then `todo.py set … && todo.py push`, confirm ids → statuses in one line, re-render the widget.

## Files

- Live page (local): http://localhost:8642/docket.html
- Live page (Pages): https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/todo.py
- Widget renderer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/widget.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-027-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-028-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-472-docket.md
