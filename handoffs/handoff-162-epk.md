# handoff-162-epk — "&" on page 2; 24 laurel stills on the Drive; seven arrangement options to choose from

## Recap (newest first)
- Luke (voice): six stills per festival with the laurel on, original aspect ratio, for SCAD, AFI Fest, Reel Black Men and B.E.S.T.; change AWARDS AND SELECTIONS to "&"; show six or seven other arrangements of the laurels (sizes, rows).
- **Canva page 2 title now reads A W A R D S & S E L E C T I O N S** (same box, letters spaced as before). STATE updated.
- **Laurel stills:** `tools/laurel-stills.py` crops each 1920×1080 export to its 2.39:1 picture (rows 138–941 → 1920×803) and composites the laurel top-centre, 6% down, 22–26% of the frame height (the proportion of SCAD's own social still). Light or dark laurel chosen by the luminance under it; all six frames are dark there, so every laurel is white (B.E.S.T. gold). Stills used: 1.1.5 (barn), 1.1.13 (oaks), 1.1.14 (burial), 1.1.17 (cabin), 1.1.35 (chandelier), 1.1.41 (the Elder at the tree). 24 files on the Drive: `00 PRESS/LAURELS/Stills with laurels/<FEST>/`, plus the contact sheet. In the repo only the contact sheet and the tool are committed (the 24 JPEGs are 17 MB; the repo sits near the Pages 1 GB cap); rerun the tool for any other frame numbers.
- **Arrangement options:** `press/proofs/laurels-options-2026-10-11/option-A…G.png` and `contact-sheet-options.jpg` (also on the Drive beside the laurels). PIL mock-ups on the page ground with the real assets; A is the page as built. B keeps the three originals at 370 with AFI Fest fourth and Reel Black Men beside the winner; C stacks 3 + 2 + winner; D puts the winner first and large; E shortens the still to 600 so the laurels grow (3 + 2 at 400, winner 1200); F makes the winner a 1400-wide band with a small row at the foot; G drops the still.
- Not changed: anything else in Canva; the kit, contract and worksheet (no laurel page).

## Next
1. Luke picks an option (or a mix). Applying it is the 11 Oct hand procedure in the harness: Layers tab to select, Ratio lock on, width then X/Y.
2. If he wants other frames for the stills: `venv/bin/python tools/laurel-stills.py 3 4 16 ...` and copy to the Drive folder.
3. Re-export the design when page 2 settles; the 5 Oct PDFs are stale.

---
**Timestamp:** 2026-10-11 · **Lane:** `epk` · **Continues:** handoff-161-epk.md · **Model:** Fable 5.1 (goose turn).

## Files
- Options sheet: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/proofs/laurels-options-2026-10-11/contact-sheet-options.jpg
- Stills sheet: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/assets/derived/laurel-stills/contact-sheet-laurel-stills.jpg · tool: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/laurel-stills.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-161-epk.md · This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-162-epk.md
