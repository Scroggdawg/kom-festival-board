# handoff-044-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** a wrong fact in my file, corrected, and a dated defect in my dashboard flagged before it fires.

### One hard door in September, not three

The festival lane verified the two dates it had been asserting all day. **D.1.5 carried both, and neither survived.**

| | Sep date | What it actually is |
|---|---|---|
| IFFR | **Sep 15, 17:00 CEST** | a real final deadline, verified first-party |
| SBIFF | Sep 18 | a **$10 price step**; the real door is **Dec 2** |
| Aspen | Sep 25 | **unknown** — Aspen publishes no dates itself and FilmFreeway returns 403 to fetch |

I checked their data rather than the message: SBIFF's `feesText` now names every tier through FINAL Dec 2 with `provenance: official`; Aspen carries no provenance and its own `feesText` already implies a later final at $95; IFFR names its tiers with Sep 15 as late/final. All three hold.

**D.1.5 retitled** to say exactly that. **No due dates moved** — every Sep 15 in the file was keyed to IFFR, never to SBIFF, so the calmer picture does not change them. Verified count 2 of 97; the dashboard tile moved by one.

### A defect that fires on Sep 16

SBIFF's `close` is still `2026-09-18` while its real door is Dec 2. My dashboard picks the earliest `close` among verified targets and labels it **"next deadline"**. Today that is IFFR and it is right. **On Sep 16 it becomes SBIFF Sep 18, and the campaign's front page will call a $10 price step the next deadline** — the error we have now corrected three times, rendered automatically.

Not fixed by guessing: `close` is that lane's field and only they can say what it means. Put to them as two workable shapes — `close` becomes the final door with tier dates in the fee data, or the record gains a field naming which kind of date `close` holds and my tile reads it. If neither, my tile stops saying "deadline" and says something duller. **Better a dull label than a page that lies in eight days.**

### The rule, narrowed

Recorded in `todo.json` as `dateNote`, in their words: **a date is not a deadline until something names its tier**, and **a verification that lives only in prose is not one** — SBIFF and Aspen both said "VERIFIED 2026-09-08" in their prose while the structured data disagreed, and re-fetching showed the SBIFF claim was flatly wrong. The first rule ("cite the festival's own page") was a habit; this one is a test something can fail. It sits beside `paletteNote`.

Rev 63, valid, published.

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-043-docket.md
**Model:** Opus 5. **Goose turn** — a wrong fact removed, a future wrong fact flagged.

## Next action (the one thing)

**Ask Jordan whether downloading is enabled on the YouTube link — D.3.1.** Minutes, and it decides whether the campaign Vimeo has to exist by Sep 15. Still open behind it: whether Luke has a file to upload at all, and what `close` means on the board.

## Files

- Dashboard: https://scroggdawg.github.io/kom-festival-board/
- Docket: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth, with both notes: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-043-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-044-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-488-docket.md
