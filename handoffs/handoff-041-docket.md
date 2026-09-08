# handoff-041-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** v6 pinned, and a duplicate field in the board data resolved before it could mislead anyone.

### D.2.1 pinned to v6

`press/filmfreeway-page-v6.md` has landed. The logline is locked in **two versions**, not one — Luke is presenting both to Jordan and choosing with him. A ends on the act, B ends on what he becomes; the 56 words between "In 1834" and "…to decide" are identical in both. One seam still open in Luke's words: he may revise "who he must now face to decide".

D.2.1 now reads: *"Send Jordan press/filmfreeway-page-v6.md — bio, statement, the scope of page changes, and two logline versions for him and Luke to choose between; he approves the direction once"*. The old text implied a single logline. Due stays 2026-09-15. Rev 54.

### One field for one thing

The festival lane created `sourceUrl` by hand on the IFFR record so my dashboard tile could test it — then found `source` already existed for exactly that purpose, populated on 124 of 151 records, and it is the field `tools/validate-data.py --provenance` actually checks. Two fields for one thing, with the two validators disagreeing on which is authoritative.

**Checked before switching, not after.** All 124 `source` values are URLs. The verified count is **1 either way**, so the tile does not move and there was never a window where the front page could read zero. The dashboard now tests `provenance === 'official' && source`; `sourceUrl` is free to delete and that lane has been told it is live.

They also asked whether the tile reads a scalar `note` they invented on that record. It does not — nothing on the dashboard touches it, so it can be folded back into the schema's `notes[]`.

### The palette conclusion, sharpened

Their framing is better than mine and it is the one to keep: **two independent colour sets both failing means the palette was never validated as a categorical system, only chosen to look right on dark navy.** Violet against periwinkle, and green against gold, are symptoms rather than the finding. `paletteNote` in `todo.json` carries the measurements.

They audited the board's own publish loop for my merge bug and it is clean: it deep-clones the fetched remote and mutates it rather than rebuilding from a field list, PUTs the whole object with the sha, and its rev is a uuid so it cannot go backwards. Unmodelled keys survive there.

Data at rev 54, valid, published.

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-040-docket.md
**Model:** Opus 5. **Goose turn** — a version pinned, a duplicate field retired, no data moved by guesswork.

## Next action (the one thing)

**D.1.1 — the discount emails.** Seven days to IFFR, and it is still the first unblocked item on the board.

## Files

- Dashboard: https://scroggdawg.github.io/kom-festival-board/
- Docket: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Dashboard source: https://github.com/Scroggdawg/kom-festival-board/blob/main/index.html
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-040-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-041-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-485-docket.md
