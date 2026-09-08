# handoff-034-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, duck then goose):** a confirmation, then a bug that bit while I was writing about it.

### The confirmation

The festival lane checked the inference behind Sep 18 and confirmed it. **SBIFF is among the nine shortlisted festivals** — Official Deadline Sep 18, the tier expiring that day $60, comfortably over the ~$20 threshold, so it does trigger D.1.1. That lane also checked an assumption I had not flagged: **Curta Cinema Rio's earlybird is Sep 12**, six days earlier and a real money change, but its early tiers price at $10.73 / $14.30 / $19.07 with student rates at $4.47 / $5.96 — all under the threshold, so Curta never triggers the discount email. Ordering: Curta Sep 12 earlier but below threshold · **SBIFF Sep 18 the first door above it** · Aspen Sep 25 next. D.1.1 and D.1.5 stay at 2026-09-18. No data change.

### The bug

Writing that handoff, my push was rejected because the festival lane had pushed. Between the rejection and the retry, **the server's background pull ran `reset --hard origin/main` and destroyed the unpushed handoff commit.** Recovered from the reflog and verified byte-identical against the mirror before re-committing.

The cause: both `pull()` and `push()` reset the clone to origin, and neither checked whether the clone was *ahead* of origin. Any commit made here that had not been pushed yet — a handoff, most obviously — was one 20-second tick from deletion. It had been true since the clone was introduced; it only bit because two lanes pushed within a minute of each other.

Fixed. `_publish_pending()` now runs before any reset: if the clone is ahead, it pushes those commits, rebasing once if the remote moved, and if it still cannot publish them it **refuses to reset** and says so. `push()` checks the same thing before its loop. A reset can now only ever discard work that `push()` itself made moments earlier.

This handoff is its own test: it was committed and left unpushed on purpose, and `pull()` published it instead of destroying it.

### Worth filing as doctrine, not filed

Offered to Luke rather than written, since the doctrine repo is not this lane:

1. **A list field is not a deadline.** FilmFreeway's "next deadline" reports whichever tier or category comes next without naming which — a pitch-competition date read as a film close, an earlybird read as a deadline. Two wrong dates in this campaign, and the other lane's own handoff-018 had named the trap four days earlier. A date is real when it comes from the festival's own Dates and Deadlines panel with the tier named beside it.
2. **`reset --hard` in an automated loop needs an ahead-check.** Convenience for the loop, a shredder for anything committed and not yet pushed.
3. **Label the inference and name what would overturn it.** Both refusals held because the uncertain step carried the fact that would change it; the other lane checked in minutes rather than arguing.

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-033-docket.md
**Model:** Opus 5. **Goose turn** — a data-loss bug found by being bitten, and closed.

## Next action (the one thing)

**Luke opens the published page on his phone, adds a fine-grained token, and clicks one status.** The last unproven inch of the write path, and the only thing outstanding here.

## Files

- Live page, laptop: http://localhost:8642/docket.html
- Live page, anywhere: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/todo.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-033-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-034-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-478-docket.md
