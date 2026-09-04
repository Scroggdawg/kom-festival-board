# handoff-004-festival

## Where we left off

**This session (Aug 25, 2026, 17:57):** Colored the dashboard tiles per Luke's spec — gold researched, green yeses, yellow maybes, red noes, bottom row red-while-zero — and pushed to all three surfaces (live site, artifact, project copies).

- **Aug 25 17:57** — Status tiles shipped; live site verified carrying the change (HTTP 200, new classes present).
- **Aug 25 ~17:20** — Board went public: https://scroggdawg.github.io/kom-festival-board/ (repo `Scroggdawg/kom-festival-board`); 8-counter dashboard + Key Dates section; tier tints through table and heat map; DP mentions scrubbed.
- **Aug 25 PM** — Luke's first notes: distinct tier colors, A-list re-entered, DP Craft Sheet split off.
- **Aug 25 AM** — The research raid (117 festivals) and first publish.

**Direction we were going:** Board is live and shareable; the campaign itself starts now — wave-1 submissions, then the next-ring raid toward ~150 winnable festivals.

---

**Timestamp:** 2026-08-25 17:57 PDT
**Lane:** `festival`
**Continues:** handoff-003-festival.md
**Model:** Fable 5. **This turn was a goose** — a small styling change on Luke's exact spec.

## What changed

- Tile status colors, with a live rule (flagged to Luke, awaiting veto): bottom-row tiles are red at zero; once numbers land, applied → gold, accepted → green, pending → yellow, rejected stays red. Logic lives in the `counters()` function of the board file.
- Republished artifact (same URL), synced `FESTIVAL CAMPAIGN/` copies, committed + pushed `site/` — live page verified.

## Open uncertainty

- Unchanged: Vercel import (Luke's two clicks at vercel.com/new), PAFF ladder, AFI email answers, premiere assumption, College TV Awards window.
- The red-while-zero rule is my extrapolation of "red for now, cause they're all at zeros" — confirm or I'll pin them permanently red.

## Next action (the one thing)

**Submit Sundance before Aug 31** — 6 days on the live counter.

## Files

- Live site: https://scroggdawg.github.io/kom-festival-board/
- Artifact: https://claude.ai/code/artifact/5dadab1f-b512-47eb-a2b4-e04cc9d18ff5
- Prior handoff: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-003-festival.md

file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-004-festival.md
