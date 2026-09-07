# handoff-027-festival

## Where we left off

**This turn (Sep 6, 2026, Fable 5.1, goose — Luke said "start that work tree"):** Luke approved the look (handoff-026) with one swap — **started = sky blue, awaiting response = gold** — and asked for a second session whose only job is to keep the to-do widget current, with a page he can leave open in a browser that updates by itself when he tells that session about a change.

### Built and pushed (`35be2f5`)

| File | What |
|---|---|
| `todo.json` | The truth. 37 items, 5 sections, four statuses (`not_started · started · awaiting · complete`), colours in the file (started `#5fb3e0`, awaiting `#e6a92a`, complete `#2bb673`, not started `#9aa3b8`; sections terracotta / magenta / violet / periwinkle / peach), history per item, `rev` |
| `tools/todo.py` | The only writer: `list · check · set <id> <status>… · note · push`. Atomic write, rev bump, validation, refuses bad statuses. `push` commits, pulls --rebase, pushes |
| `docket.html` | The live page. Polls `todo.json` every 3 s, re-renders on rev change, shows rev / written / checked-ago, dims after 9 s without a good fetch. Same look as the approved widget |
| `.claude/launch.json` | `docket` config: `python3 -m http.server 8642` at the repo root |

### The second session

A task chip was spawned in this session (`task_eee79c1c`, "Run the Docket — keep the campaign to-do live") with a full brief: pull, serve on :8642, open `docket.html` in the Browser pane, print both URLs (localhost and https://scroggdawg.github.io/kom-festival-board/docket.html), render the widget every turn; on any change from Luke run `todo.py set … && todo.py push`. Luke clicks the chip to approve — it opens in its own worktree. The Docket session writes `handoff-NNN-docket.md` in this repo and the machine ledger.

**Mechanics for Luke:** keep http://localhost:8642/docket.html open (needs the Docket session's server running) or the Pages URL (about a minute behind, works on the phone). Tell the Docket session a change in plain words; the page updates within 3 s of the write.

### Not done

`PLAN-docket.md` still describes the superseded six-zone design — to be rewritten to the list. The five section colours are not validated as a set. The page is read-only; edits go through the session (phase 2 would reuse the board's publish loop for in-browser edits).

---

**Timestamp:** 2026-09-06
**Lane:** `festival`
**Continues:** handoff-026-festival.md
**Model:** Fable 5.1. **Goose turn** — scaffold built, pushed, second session briefed.

## Next action (the one thing)

**Luke: click the chip to start the Docket session.** Then, in this lane: rewrite `PLAN-docket.md` to match what shipped; the nine discount emails (D.1.1) are still the campaign's at-bat item.

## Files

- Live page (Pages): https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/todo.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-026-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-027-festival.md
