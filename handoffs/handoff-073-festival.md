# handoff-073-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** closed the `sourceUrl` fork I opened yesterday. Housekeeping turn — no campaign decision moved.

### The collapse

The docket switched its dashboard test to `provenance==='official' && x.source` and cleared me to delete the duplicate. **Verified that on the published `index.html` before touching the data.** Then:

- **`sourceUrl` deleted** — with `assert source == sourceUrl` in the script before collapsing, rather than assuming. Identical, nothing lost. Verified count is **1 of 97** before and after.
- **The scalar `note` folded into `notes[]`** as `{nid, date, text}`, nid minted in the same uuid4 shape the board's own `appendNote` uses. That record **already carried an empty `notes[]`** — the structure was there and I wrote past it, so the scalar was doubly redundant.
- **Refreshed the embedded offline snapshot.** Nothing does this automatically; it is exactly how the snapshot went stale before.

One record touched. Gates clean.

### The convention now, so nobody forks it again

| Field | Means | Populated |
|---|---|---|
| `source` | the URL a fact came from | 124 of 151 |
| `provenance` | `official` = read off the festival's own Dates & Deadlines panel | 1 of 97 targets |
| `notes[]` | `{nid, date, text}` — rendered in the board timeline, searched | 1 |

**`sourceUrl` and a scalar `note` do not exist. Do not reintroduce them.**

### Worth keeping from the exchange

The docket checked my sequencing claim instead of accepting it, and found the "gap" I wanted to sequence around was one record wide — so there was never a window to protect. Its words: *"right in principle and unnecessary in fact, which is the good version of that mistake."* **Measuring the risk beat honouring it.**

Its read on the EPK's field 2.1 is also sharper than mine: *a field that can hold one value, when the truth is two, will either lose one silently or grow a second store beside it* — which is its own merge bug generalised. The list-before-two-fields advice stands.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-072-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**IFFR closes Sep 15, 17:00 CEST — seven days, unanswered across seven turns.** It is the only verified door on the board. Its blocker is a **screener link**, not the logline: the campaign Vimeo does not exist (D.3.3) and D.3.1 is "get YouTube access from Jordan." Both sit in the docket's file.

Then send Jordan v6 (D.2.1, pinned and reworded at rev 54).

## Files

- Board data: https://github.com/Scroggdawg/kom-festival-board/blob/main/data.json
- Page draft v6 (for Jordan): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/filmfreeway-page-v6.docx
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-072-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-073-festival.md
