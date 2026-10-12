# handoff-163-epk — Laurel stills redone with per-frame placement; page-2 options v2 with title and photo locked

## Recap (newest first)
- Model switched to Opus 5.5 by Luke for this turn. His notes: page-2 options must keep the title and photo where they are and move only the laurels; selections no smaller than option D's small ones, winner never as big as F's. The laurel stills need real placement in clean areas of each frame.
- **Laurel stills, redone.** `tools/laurel-stills.py` now carries a hand-drawn clean-area box for each of 12 frames, chosen from gridded sheets of 32 candidates (box and reason listed in the tool). Laurels are trimmed to their ink, fitted to the box, white or gold with a faint shadow, black on the one light frame (1.1.41, leaf bokeh). B.E.S.T. uses the wide winner laurel in wide boxes and a new stacked build (wreath over the awards, every line centred) in tall ones. Frames: SCAD 18, 22, 31, 17, 41, 33 · AFI Fest 25, 37, 2, 23, 32, 36 · Reel Black Men 23, 18, 22, 41, 2, 37 · B.E.S.T. 25, 22 (wide), 31, 18, 37, 33 (stacked). The earlier top-centre set is replaced on the Drive (`00 PRESS/LAURELS/Stills with laurels/`, 24 files + sheet).
- **Page-2 options v2.** `tools/laurel-page-options.py` renders the page with title (249), rule (339), photo (429–1289) and label (1314) fixed; laurels trimmed to ink and matched by height; asserts the D minimum (ink 187 px) and the F maximum (winner ink < 1306 px); group centred between the label and 150 px above the foot. Seven options in `press/proofs/laurels-options-2026-10-11b/`; the run prints every ink box. The v1 sheet (photo moved) is superseded.

## Next
1. Luke picks an option. To apply in Canva: convert each ink box to the element box (the Canva element is the full PNG, so scale by full/ink size and offset by the ink bbox), then set W/X/Y with the Ratio lock on (harness procedure of 11 Oct).
2. Re-export after page 2 settles.

---
**Timestamp:** 2026-10-11 · **Lane:** `epk` · **Continues:** handoff-162-epk.md · **Model:** Opus 5.5 (goose turn).

## Files
- Options v2: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/proofs/laurels-options-2026-10-11b/contact-sheet-options.jpg
- Stills sheet: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/assets/derived/laurel-stills/contact-sheet-laurel-stills.jpg
- Tools: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/laurel-stills.py · https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/laurel-page-options.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-162-epk.md · This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-163-epk.md
