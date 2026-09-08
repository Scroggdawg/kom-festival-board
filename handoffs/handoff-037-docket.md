# handoff-037-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** the festival lane closed the reciprocal-audit loop and made one last request, which was the right one. Built.

That lane's ledger, worth keeping: seven real defects came out of four exchanges — my silent discard of title-only edits, my `reset --hard` deleting an unpushed commit, my publish path bypassing validation, my `check()` covering four rules of fifteen; their prefix match corrupting a festival record, their total absence of validation on `data.json`, their three empty-string dates. None would have been found alone. Against that, their honest counterweight: **0 of 37 done, no discount email sent, the logline unpicked, the EPK worksheet 9 of 47, Jordan unasked, Yeo unmessaged.** Two agents spent an evening making the instruments trustworthy while the work stood still. They called a halt on tooling and I agree.

### The one thing worth building

The page said "0 of 37 complete" and nothing about what to do next. A strip under the header now carries two facts:

- **Next** — the first item nobody else is holding. Rule: no `waitingOn`, status `not_started` or `started`, preferring work already in flight over an untouched item, in the file's own order. Currently **D.1.1**, the discount emails.
- **Waiting on** — every unfinished item that is either awaiting a reply or parked on a person, grouped by the holder, taking the part before the separator so "Jordan · MFA tense (E.2)" counts as Jordan. Currently **Jordan 4 · master access 1 · Yeo 1**.

No new colour, no new interaction, one line of plain text in the existing palette. It hides itself when everything is complete, and says "every remaining item is waiting on someone" when nothing is unblocked.

Tested: an item in flight further down the file wins over the untouched first item; everything blocked; everything complete; nothing blocked; and the restore after each. `docket.html` and `tools/widget.py` produce the same strip, tie-breaks included — an ordering mismatch between them was caught and fixed before commit.

### Standing state

Data at rev 38, valid, 0 of 37. D.1.1 and D.1.5 due 2026-09-18. Clone clean, server pull loop current, published page carrying the strip.

Prior turns: the validator stating the file's invariants (handoff-036); the read-back gap in `push()` (handoff-035); the reset-over-unpushed-commit bug (handoff-034).

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-036-docket.md
**Model:** Opus 5. **Goose turn** — tooling closed, one surface change that points at the work.

## Next action (the one thing)

Not tooling. **D.1.1 — the discount emails.** The page now says so itself. Behind it, the phone-and-token click that proves the last inch of the write path.

## Files

- Live page, laptop: http://localhost:8642/docket.html
- Live page, anywhere: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Page: https://github.com/Scroggdawg/kom-festival-board/blob/main/docket.html
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-036-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-037-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-481-docket.md
