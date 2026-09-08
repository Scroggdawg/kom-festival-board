# handoff-060-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** Luke asked for a dedicated worktree session, **Electronic Press Kit**, caught up on everything, to audit the worksheet widget, rebuild it constrained, and then run the intake as he pastes materials into chat. Spawned as `task_b6db4052` with a full self-contained brief.

### What he asked the new session to do

1. **Audit the widget** built in handoff-050 against what he has now said he wants.
2. **Rebuild it constrained.** His words: *"I don't want any commentary, I just want the list of the items, like the title and then what it is."* Numbered `3.1`, `3.3` — he said "Roman numeral" but gave a decimal example, so the brief tells the session to **default to decimal and ask him in one line** whether the page part should be Roman (`III.1`), rather than guessing. **The numbers must be stable** — they are how he will refer to items when sending material, so a number may never be reassigned; new fields go at the end of their section, and every field gains a stable `id` in `epk.json`.
3. **Make it work from another machine** — *"accessible from the git repo from another machine as well, to add to it, to push and pull."* This is the requirement that shapes the build: `epk.json` is the truth, `epk.html` on Pages reads and writes it. The brief points at `docket.html` / `tools/todo.py` / `tools/docket_server.py` as the working pattern to copy rather than reinvent.
4. **Run the intake.** He pastes materials in any order; the session sorts each into its numbered slot, writes, commits, pushes, and reports in one line. Told explicitly not to invent a field when something does not fit — ask.

### Lessons handed forward rather than left to be rediscovered

The brief carries the Docket lane's hard-won failures verbatim: run from **your own clone**; **`reset --hard` in a background loop needs an ahead-check** (it silently deleted an unpushed commit); **validate, write, re-read from disk, compare, revert rather than commit**; **never match by prefix** (a `curta` prefix wrote one festival's data onto another); **merge, never overwrite** (a naive rejection path destroyed a phone edit); and a field edit with no status change must still stamp history or the merge discards it. Also: the toolchain reality on this machine, and that the existing PDF was built wrong first and only rendering caught it.

Plus the highest-value intake fact: **the end-credit roll unblocks six of the eleven pages** and needs no hard drives.

### Boundary

The new session owns the EPK: `press/epk.json`, `press/epk*.md`, `epk.html`, and the EPK handoff lane (`handoff-NNN-epk.md`). It is told **not** to write `todo.json` or `docket.html` — those belong to `KOM FEST TASK LIST`. This lane keeps the board, the loglines, the page draft and the festival research.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-059-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**Luke: click the chip to start the Electronic Press Kit session**, then send it the end-credit roll — that is the single biggest intake event available and it needs nobody. Meanwhile in this lane, still unanswered: pick a logline, and whether to import the FilmFreeway export so the board stops recording 0 submissions against a real 30. Real clock starts **Sep 15**.

## Files

- Worksheet data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Spec: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk-spec.md
- PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/EPK-breakdown.pdf
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-059-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-060-festival.md
