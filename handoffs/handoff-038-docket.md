# handoff-038-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** D.2.1 unblocked, and a loss I had reported as recovered turned out to be half-recovered.

### D.2.1 is no longer waiting on anyone

The festival lane reported the logline locked, which was the last missing input. I checked the recorded blocker rather than taking the conclusion: `waitingOn` read "Jordan · MFA tense (E.2)", and E.2 is *"Jordan's MFA: earned, or completing?"* — a question **the send itself asks him**, not a precondition for sending. `press/messages-to-send.md` says the same: one message to Jordan covering the drives, the MFA tense, the "why he directs" sentence and the approval, "drafted once the page draft is final". The draft is now final, so the send is Luke's to make and nobody is holding it.

- `waitingOn` cleared. Roll-up went from Jordan 4 to **Jordan 3 · master access 1 · Yeo 1**.
- Retitled to name the package: "…the scope of page changes — press/filmfreeway-page-v5.md; he approves the direction once".
- Status untouched at not started. Published, rev 43.

**Not written.** The locked logline — 62 words — belongs in the press files, not in an item title, and no item's text is wrong without it. The lane also mentioned "the real clock starts Sep 15" with no explanation; I have asked what it is rather than putting an unexplained date in the file.

### A recovery I reported as complete was not

Auditing every commit this clone has ever made against origin turned up **six that never reached it**. Four are fine: two data commits from the two-writer tests that the merge superseded, one from today's test clicks that I discarded on purpose, and the handoff I did recover. The fifth is real:

**`62d549b`, the `due` command, was destroyed by the same `reset --hard` bug** — the one fixed in `17f4bd4`. That reset ate two commits, not one. I noticed the handoff, recovered it, and wrote in handoff-034 that the recovery was done. I never re-ran `todo.py due`, so the loss stayed invisible for four commits until I reached for the command today and it was not there. Restored from the reflog: the command and `set_field`'s date validation.

To be sure nothing else went the same way, I compared every function and command that has ever existed in the writer against the current file. One absent: `_rebuild_onto`, the git plumbing deliberately removed when the clone replaced it. Nothing else.

**The lesson is not the bug, which was already fixed. It is that "recovered" was asserted from one file rather than checked against the whole set.** A reset takes commits, not files, so the check has to be commit-shaped.

### Also this turn

`todo.py waiting <id> <who|->` added, so a blocker can be set or cleared through the writer. Both it and `due` refuse an empty value.

### Standing state

Data at rev 43, valid, 0 of 37. Next reads D.1.1; D.2.1 is now the second unblocked item and, per the festival lane, four items queue behind it — a dependency the file does not record, so the strip cannot know it.

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-037-docket.md
**Model:** Opus 5. **Goose turn** — one unblock, one half-recovery finished properly.

## Next action (the one thing)

**Send Jordan the package** — D.2.1, `press/filmfreeway-page-v5.md`. It is unblocked and the most downstream work depends on it, even though the strip still names D.1.1 by file order.

## Files

- Live page, laptop: http://localhost:8642/docket.html
- Live page, anywhere: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/todo.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-037-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-038-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-482-docket.md
