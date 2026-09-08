# handoff-076-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** the docket predicted that on **Sep 16** its dashboard would call SBIFF's $10 price step the "next deadline" — the error we had corrected three times, rendered automatically. It asked me to define what `close` means, since it is this lane's field.

### The answer: no new field. The contract already existed and this lane broke it.

`board.html`'s own section note has always said it:

> "Each bar runs from the day submissions open to the **final deadline**… **Sorted by final deadline: read top to bottom as the order the doors close.**"

**The bug: I set `provenance: official` on a record whose `close` held a tier date.** That made SBIFF authoritative with Sep 18 — the regular fee tier — sitting in the door field. The docket spotted the rendering; this lane supplied the defect, one field from where it was looking.

### Two records corrected

- **SBIFF `close` 2026-09-18 → 2026-12-02.** Tier ladder stays in `feesText`. The dashboard now reads IFFR Sep 15, then SBIFF Dec 2. Nothing to change on the docket's side.
- **short-shorts-2027 `close` 2026-09-30 → 2027-01-15.** Found by sweeping for the same shape. The record contradicted *itself*: its feesText reads "early tier to Sep 30 · regular Nov 30 · **final Jan 15, 2027**". **Third correction to this one record in a week** — "Sep 9" was the pitch competition, and the fix for that moved it from one wrong tier to another. Warrant is the record's own feesText, **not** a first-party check, so `provenance` stays unset and the note says so.

### The rule is now a test that can fail

Added to `tools/validate-data.py`:

1. **Structural, always an error** — `close` may not be earlier than a tier the record's own `feesText` explicitly dates. Caught short-shorts today; would have caught SBIFF and the original Sep 9. The year must be written out, because inferring one would guess and guessing is the bug.
2. **Advisory under `--provenance`** — an unverified record whose feesText names "final" or "late" may be holding a tier date. **15 targets match**, including Sundance, SXSW, Flickerfest, Tampere, Atlanta.

That 15 is a better-shaped backlog than "73 records lack provenance": every entry names what to check and why.

### Shipped with a bug, caught on the read-back

The advisory check warned that **SBIFF** "may be a fee tier" — the one record just verified — because it sat inside the provenance block without testing provenance. Fixed in the next commit. A gate that cries wolf about the record it should trust teaches people to skim it, which is how the original error survived three rounds.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-075-festival.md
**Model:** Opus 5.

## Next action (the one thing)

Three questions to Luke, unanswered and now sharper because **IFFR Sep 15 is the only September door there ever was**:

1. **Does he have a file he can upload?** Decides whether IFFR is reachable at all.
2. **IFFR — yes or no?**
3. **Open the Aspen FilmFreeway listing and read the tier names** — automated fetch is 403; he has an account.

## Files

- Board data: https://github.com/Scroggdawg/kom-festival-board/blob/main/data.json
- The gate: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/validate-data.py
- Page draft v6 (for Jordan): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/filmfreeway-page-v6.docx
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-075-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-076-festival.md
