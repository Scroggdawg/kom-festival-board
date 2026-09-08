# handoff-050-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** Luke asked for the EPK sheet **divided explicitly by page (Page 1, Page 2 …) with every field editable**, so he can fill it in and hand it back.

Delivered an editable worksheet widget in chat: eleven page sections plus Assets, **38 fields**, each with its label and a hint naming who holds it. Fields auto-grow, turn green when filled, the header counts progress, and the send button packages everything typed into one message back to Claude (`sendPrompt`) grouped by page. Pre-filled where the answer is already known: genre, country, duration, screenings, rights stem, and pointers to the existing statement and director-bio drafts.

Also committed `press/epk.json` — the same worksheet as data (11 pages, 38 fields, `rev`), so his answers can persist in the repo rather than living only in a chat snapshot. Next step if he wants it: an `epk.html` page on the Docket pattern that reads and writes that file.

### Standing findings, unchanged

- **The end-credit roll unblocks six of the eleven pages** — cast, full crew, HoDs, composer, sound designer, thanks, AFI boilerplate — and needs no hard drives, only the YouTube link.
- **The ~100-word synopsis has never been written** and page 2 needs it.
- Five pieces written; about twelve need only Luke; the rest sit behind Jordan (drives, approvals, his bio, the intro) or Yeo (every technical spec, trailer, masters, DCP).

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-049-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**Luke fills in what he knows and presses send; Claude writes it into `press/epk.json` and updates the one sheet and the Docket.** The two highest-value fields are the end credits (page 9/10, which cascade into 3, 7, 11) and the synopsis (page 2). **Short Shorts Tokyo closes today, Sep 9 — no discount email has been sent.**

## Files

- Worksheet data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- One sheet: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk-one-sheet.md
- Spec: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk-spec.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-049-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-050-festival.md
