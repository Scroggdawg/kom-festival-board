# handoff-031-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** two more requests from the festival lane, both done.

- **D.2.7 retitled** to carry the URL, since the website is a live decision and the page does not render notes: "First-time flag → Jordan; verify the Instagram target; decide the website — killerofmen.com is the donate page". Status untouched. Published, rev 33.
- **Dated items now show how close they are.** Each says overdue, yesterday, today, tomorrow, or in N days beneath the date; the header names the most urgent bucket, currently "0 of 37 complete · 2 items due tomorrow". The mark is brightness plus a rule and never a hue — the four status colours are reserved for status, the five section colours never mean status, so urgency got its own channel. A completed item is never flagged however close its date. `docket.html` and `tools/widget.py` carry the same treatment so the page and the chat snapshot stay identical. Tested at −3, −1, 0 (complete), +1, +4 and +30 days.

**Flagged, not acted on.** The festival lane said Short Shorts Tokyo closes today. `todo.json` has D.1.1 and D.1.5 due 2026-09-09, which is tomorrow local. Tokyo runs 16 hours ahead of Pacific, so a Sep 9 Tokyo cutoff does expire during Sep 8 Pacific — the lane may be right in practice and the stored date right on paper. Changing a deadline on my own reading of a time zone is not mine to do, so the date stands and the question is back with that lane.

Prior turns: the cinematographer correction and the `title` command with the merge fix (handoff-030); click-to-write on both paths, the adversarial review that caught the write path destroying remote changes, and the move to a dedicated clone with a real item-level merge (handoff-029).

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-030-docket.md
**Model:** Opus 5. **Goose turn** — one retitle, one surface change, one date question raised.

## Next action (the one thing)

Still unchanged: **Luke opens the published page on his phone, adds a fine-grained token, and clicks one status.** That is the last unproven inch of the write path. Second: someone settles whether the Tokyo cutoff is today or tomorrow.

## Files

- Live page, laptop: http://localhost:8642/docket.html
- Live page, anywhere: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Page: https://github.com/Scroggdawg/kom-festival-board/blob/main/docket.html
- Widget renderer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/widget.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-030-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-031-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-475-docket.md
