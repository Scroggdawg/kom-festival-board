# handoff-016-festival

## Where we left off

**This turn (Sep 3, 2026):** Luke ordered all 75 of Joan's picks onto the yes list, starred "JOAN PICK," and the site updated. DONE and pushed (commit `1bdacd0`).

- **The merge** (`site/tools/joan-merge.py`, re-runnable): 25 existing targets flagged `joanPick` · 12 promotions enriched to full target shape (bench: Slamdance, Interfilm, SLIFF, NHFF, Raindance, Virginia, Oberhausen, ZINEBI, deadCenter · ruled-out: Sidewalk, IFFR, RiverRun — caveats carried in their `why`) · 38 brand-new target records built from Joan's sheet + the Sep 3 research raid (verified deadlines where we have them, `estimated` flags where we don't).
- **Board now:** 151 researched (past Luke's 150 goal) · **97 targets** · 43 bench · 11 out. Rev `f821ae3d`.
- **UI:** gold ★ JOAN PICK chip on rows, cards, and the festival sheet; small gold ★ on gantt labels. `generate-data.py` preserves `joanPick` through regeneration.
- **Verified locally:** zero console errors, `validate()` clean, 75 chips render, tiles/meter derive correctly. Found and cleared a stale localStorage test draft (my own, from Aug 26 verification — browser-local only, never touched the repo).
- **Timeline note:** the 38 new records lack `open` dates (not fabricated), so they appear in rows/heat but not as gantt bars until opens are researched.
- **Mirror artifact republished** (label "Joan's 75 merged").

**Direction we were going:** The board is Joan-merged. Still hanging: (1) Luke confirm/deny ABFF + MVAAFF 2026 "ACCEPTED" — decides REGARD's qualifying play and premiere ledger; (2) the Sep 14–Oct 1 deadline run (Flickerfest 14 · IFFR 15 · PAFF ~16 · SBIFF ~18 · Gary 21 · **Clermont 24 = the France call** · Ann Arbor 30 · SXSW/Tampere/In-the-Palace Oct 1); (3) AFRIFF email (deadline passed Aug 26); (4) whether Sundance was submitted by Aug 31; (5) Luke's PAT for in-page publish.

---

**Timestamp:** 2026-09-03
**Lane:** `festival`
**Continues:** handoff-015-festival.md
**Model:** Fable 5. **Goose turn** — merge, UI, deploy, verify.

## Next action (the one thing)

**Luke: ABFF/MVAAFF confirm-or-deny, then sequence the September deadline run.**

## Files

- Live board: https://scroggdawg.github.io/kom-festival-board/
- Mirror: https://claude.ai/code/artifact/5dadab1f-b512-47eb-a2b4-e04cc9d18ff5
- Joan readout: https://claude.ai/code/artifact/46eeb56a-63da-472d-9a3f-1d74d33d4384
- Merge script: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/FESTIVAL%20CAMPAIGN/site/tools/joan-merge.py
- Prior handoff: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-015-festival.md

file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-016-festival.md
