# handoff-062-epk

## Where we left off

**This turn (Sep 8, 2026, Opus 5) — first turn of the Electronic Press Kit lane.** Read the lane in, audited the chat widget from handoff-050, rebuilt it constrained, and made it reachable from any machine. Nothing has been sorted into it yet; the intake has not started.

### The audit — four findings, all verified rather than assumed

| | Finding | Evidence |
|---|---|---|
| 1 | **Commentary everywhere.** 40 of 47 fields carried a `hint`, 12 of them questions or instructions — "does a poster exist?", "Jordan's drives — or the crew's phones", "LUKE — why do you shoot". Rejected. | `press/epk.json` at rev 2 |
| 2 | **No stable identifier.** Fields had `label`, `hint`, `value` and nothing else. Position was the only handle, so a field could not be referred to and adding one shifted everything after it. | same |
| 3 | **Nothing persisted and nothing was reachable.** The widget has no source anywhere in the repo — it existed only as a chat snapshot and cannot be regenerated. `epk.json` was committed beside it but nothing read or wrote it from a browser. | `find . -iname "*epk*"` returns no HTML |
| 4 | **The widget and the data had already drifted.** handoff-050 records 38 fields; `epk.json` holds 47. With the widget unversioned there is no way to say which was right. | handoff-050 vs the file |

A fifth, not in the brief: **five values held notes rather than material** — `"[final draft in press/filmfreeway-page-v4.md — awaiting Jordan's approval]"` where the statement itself should be. A truth file that holds pointers is not a container for the intake.

### The rebuild

`press/epk.json` is **schema 2**: 11 sections, **49 fields**, 10 filled. Every field has a permanent number (`3.1` … `A.6`) and a stable id (`p3-aspect-ratio`). Rendered at **[epk.html](https://scroggdawg.github.io/kom-festival-board/epk.html)** as number, title, and what is in it — no hints, no status colour, no editorial.

**Numbering:** decimal, per Luke's own example. He said "Roman numeral"; the file carries `numbering: "decimal"` and the page renders Roman from the same stored numbers when it is flipped, so answering the question is a one-word edit that renumbers nothing. Verified in the browser: stored `3.15` renders `III.15`.

**Three schema-1 fields split**, each because its halves have different owners and one half can be filled while the other cannot — this is why 47 became 49:

| Was | Became |
|---|---|
| Language / SRTs | `3.6` Language (English, filled) + `3.7` Subtitle files (Yeo) |
| Rights + contact | `3.16` Rights holder (AFI Conservatory, filled) + `3.17` Press contact (empty — the gap is now visible) |
| Instagram / website / email | `3.18` Instagram; the website is `1.3`; the email is part of `3.17` |

**Two annotations were dropped from values**, each because it is already tracked elsewhere: the killerofmen.com donate-page decision is `D.2.7` in `todo.json`, and the missing rights contact is now the empty `3.17`. **`4.1` and `5.1` now hold the statement and the director's bio as text** rather than pointing at `filmfreeway-page-v4.md`.

### Reachable from another machine

`epk.html` copies `docket.html` exactly rather than reinventing it — two write paths, the localhost server here and a direct GitHub contents-API write with a fine-grained token the viewer pastes once, **same `kom-token` storage key** so one token serves the board, the Docket and this. Polls, holds the previous render during refetch, merges rather than overwriting.

`tools/epk.py` is the only writer; `tools/epk_server.py` serves this machine. Dedicated clone at **`~/.kom-epk`**, marked `.epk-clone`; both refuse to run without the marker.

### What was tested, and what was not

A rig — bare origin, dedicated clone, a second clone standing in for another machine — asserts the Docket lane's failures rather than trusting them. **24 of 24 pass:** ids match in full and never by prefix (`3.1` does not match `3.10`); a value and its history cannot disagree; numbers cannot be reassigned; a merge keeps both machines' fields; the same field written on both keeps the loser in the history; **push refuses rather than resetting when a commit is unpushed**, and the commit and the local edit both survive; an invalid merge is reverted, not committed.

Then the real page against the real server: an edit committed, merged and pushed; the editor survived five seconds of polling underneath it; a conflict was **blocked, named, and recoverable** — the typed text stayed in the box and a second Save went through, with the replaced value still in the history.

**Two things found by testing, not by reading.** An unreachable origin threw a traceback instead of returning a message — `_fetch` now returns False and every caller stops rather than resetting. `tools/todo.py` has the same shape and would traceback the same way; that is the Docket lane's to fix. And a conflict left the editor's baseline stale, so Save would have failed forever; it now re-baselines and offers "Save anyway".

**Not tested: the GitHub-token write path.** It is the same code as `docket.html`'s, which works, but exercising it needs Luke's token and I will not handle one. The first save from another machine is the real test.

### Toolchain

The brief says this machine has no pdftoppm — true, but **PyMuPDF is installed** (`import fitz`) and rasterises a PDF to PNG for checking. `reportlab` is 5.0.0 system-wide; the scratch venv is unnecessary. The PDF was rebuilt from the new data, now carries the numbers, and **was rendered and looked at** — two balanced columns, footer at y=354 against a 36pt margin.

`press/epk-one-sheet.md` and `press/epk-inventory.md` now open with a line saying they predate the numbering and describe 47 fields where there are 49.

### Written after this handoff was first saved

- `press/epk-one-sheet.md` and `press/epk-inventory.md` each open with a line saying they predate the numbering and describe 47 fields where there are 49.
- Memory: `pdf-rendering-on-this-mac.md` — this Mac has `reportlab` and PyMuPDF (`import fitz`) system-wide and no poppler, so a built PDF is checked with `fitz.open(p)[0].get_pixmap(dpi=150).save(png)` and then read as an image. The brief's "build PDFs in a scratch venv" is out of date; no venv is needed.
- The 49-item list was rendered in chat as a widget, generated from `epk.json` so it cannot drift from the file.

---

**Timestamp:** 2026-09-08
**Lane:** `epk`
**Continues:** handoff-060-festival.md (the spawn brief)
**Model:** Opus 5.

## Next action (the one thing)

**Luke: paste the end-credit roll.** It fills `3.14`, `3.15`, `7.1`, `9.1`, `9.2`, `10.1`, `11.1` and `11.3` — eight fields across six pages — and needs no hard drives, only the YouTube link. Two others cost a minute each and need nobody: **`2.1`** (three loglines finalists, unpicked — `press/logline-final-three.md`) and **`2.2`** (three synopsis drafts, recommendation C — `press/synopsis-draft.md`). Also open: decimal or Roman.

## Files

- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/epk.py
- Local server: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/epk_server.py
- Page source: https://github.com/Scroggdawg/kom-festival-board/blob/main/epk.html
- PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/EPK-breakdown.pdf
- Spawn brief: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-060-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-062-epk.md
