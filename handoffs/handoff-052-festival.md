# handoff-052-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** Coordination with the Docket lane. It applied the cinematographer correction — **`todo.json` is at rev 31 and D.4.5 now reads "Luke's cinematographer bio gets the 'why' test"** — and reported back two things.

### The bug the Docket lane found, worth recording

Correcting the wording exposed a real defect in its own writer: **a title-only edit carries no status change, so the merge read both sides as identical, concluded there was nothing to publish, and reset to origin — the edit would have been discarded silently.** Luke would have corrected something, watched it be accepted, and found it gone later with no error anywhere. Fixed before the correction was applied: field edits now stamp their own history entry so they win the merge. It also added `tools/todo.py title <id> "<text>"`, which did not exist — wording could previously only be changed by hand-editing the file, which the deny hooks forbid.

**Standing arrangement:** wrong wording in `todo.json` gets reported to the Docket lane, which runs the change. This lane does not write that file.

### Answered back

Asked it to **retitle D.2.7 to carry the URL** — "…decide the website — killerofmen.com is the donate page" — because the website is no longer a placeholder question but a live decision with a specific shape, and its page does not render notes, which is precisely why the fact belongs in the visible title. Context passed along: Luke's own question today, and the recommendation against pointing programmers at a donate page, with the three options (drop the URL · point at the FilmFreeway project · build a one-screen landing with donate below the fold). He has not ruled.

Agreed the poster fact stays in the EPK files; it makes no item wrong.

Also flagged to that lane, since it owns the surface Luke actually looks at: **todo.json is 0/37 complete, D.1.1 is at bat, and its hard date expires tonight.**

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-051-festival.md
**Model:** Opus 5. Coordination turn — no campaign material changed.

## Next action (the one thing)

**Luke: the end-credit roll and the ~100-word synopsis — both need nobody.** And a single message to Yeo clears six page-3 spec fields at once. **Short Shorts Tokyo closes today; no discount email has been sent.**

## Files

- Worksheet data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- One sheet: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk-one-sheet.md
- Docket truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-051-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-052-festival.md
