# handoff-030-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** the festival lane sent a content correction. Applied and published.

- **D.4.5 retitled.** Luke is the **cinematographer** on Killer of Men, not the producer — he said so directly. The item now reads "…Luke's cinematographer bio gets the 'why' test". Status untouched, still not started. Published at rev 31.
- **`todo.py` gained `title`.** The writer had no way to correct wording, and doctrine says wording changes go through the writer, not a hand edit. `set_field` covers title, owner, waitingOn and due.
- **A merge bug found while adding it.** A wording change carries no status change, so `merge()` read both sides as identical, `push()` concluded there was nothing to publish, and reset to origin — a title-only edit would have been discarded silently. Field edits now stamp their own history entry (`{at, status, by, field}`), which makes them win the merge. Covered by a test before the real edit was applied.
- **Not written.** The festival lane also passed on two facts: a poster exists and Jordan holds the file, and the website is https://www.killerofmen.com/ but it is the donate page. Neither makes any item text wrong — D.2.7 already says "decide on the website" — and `todo.json` does not render notes, so recording them here would hide them. They stay in the festival lane's EPK files.

Prior turn (Sep 6): click-to-write shipped on both paths, an adversarial review caught the write path destroying remote changes, and the fix moved the Docket into its own clone at `~/.kom-docket` with a real item-level merge. See handoff-029-docket.md.

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-029-docket.md
**Model:** Opus 5. **Goose turn** — one correction, one writer extension, one merge bug fixed.

## Next action (the one thing)

Unchanged from last turn: **Luke opens the published page on his phone, adds a fine-grained token, and clicks one status.** That is the last unproven inch of the write path.

## Files

- Live page, laptop: http://localhost:8642/docket.html
- Live page, anywhere: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/todo.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-029-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-030-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-474-docket.md
