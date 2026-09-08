# handoff-032-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** the deadline that drove yesterday's urgency was wrong, and the file now says so.

Last turn I refused to move D.1.1 and D.1.5 to Sep 8 on a time-zone argument and put the question back to the festival lane. That lane went to each festival's own Dates and Deadlines panel and found the date was wrong at the root: **September 9 is Short Shorts Tokyo's pitch-competition deadline, not its film deadline.** The film tiers are Sep 30 early, Nov 30 regular, Jan 15 2027 final. The cause was a FilmFreeway list scrape whose "next deadline" field reports whichever tier or category comes next without naming it.

### Applied

| Item | Was | Now |
|---|---|---|
| D.1.1 | due 2026-09-09 | due **2026-09-18** |
| D.1.5 | due 2026-09-09, title said "Short Shorts Tokyo closes Sep 9" | due **2026-09-18**, retitled "…the nearest real doors are SBIFF Sep 18 and Aspen Sep 25" |

**I did not use the date the lane suggested,** and said so to them. They proposed Sep 30, the Short Shorts early tier. But the same message verified two earlier real doors — SBIFF Sep 18 and Aspen Sep 25 — and D.1.1 exists to send discount emails *before paying*, so it cannot carry a date twelve days after the first door where money changes. Sep 18 is the earliest verified door. **Labelled as inference:** it assumes SBIFF is among the nine shortlisted festivals with a fee over $20. If not, the date becomes Aspen's Sep 25. That question is with the festival lane.

`tools/todo.py` gained `due <id> <YYYY-MM-DD|->`, with the date validated — a bad date is refused, not stored.

### Consequence on the page

Nothing is flagged. The header reads "0 of 37 complete" with no urgency clause, and both dated items show a plain Sep 18 with no countdown, because the treatment only speaks within a day. Yesterday's "2 items due tomorrow" was pointing at a date that did not exist.

### Caution worth keeping

A wrong date is worse than no date, and it propagates fast: it drove the urgency treatment I built, the header, and several turns of pressure in the other lane. The lane's own handoff-018 had already named this exact trap on Sep 4 and it still recurred. Any date arriving here from now on comes with the festival's own panel behind it.

Prior turns: D.2.7 retitled to carry the website URL and the due-date treatment built (handoff-031); the cinematographer correction and the `title` command with its merge fix (handoff-030); click-to-write, the adversarial review, and the move to a dedicated clone (handoff-029).

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-031-docket.md
**Model:** Opus 5. **Goose turn** — a wrong deadline corrected at the root.

## Next action (the one thing)

**Luke opens the published page on his phone, adds a fine-grained token, and clicks one status** — still the last unproven inch of the write path. Behind it: the festival lane confirms whether SBIFF is in the nine, which settles whether Sep 18 or Sep 25 is right.

## Files

- Live page, laptop: http://localhost:8642/docket.html
- Live page, anywhere: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/todo.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-031-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-032-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-476-docket.md
