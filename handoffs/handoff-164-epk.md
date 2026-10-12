# handoff-164-epk — New Canva design "KoM Laurel Stills 2026": every still with each laurel, laurel movable

## Recap (newest first)
- Luke: make a new Canva design with every still and each logo, so he can move the laurels himself.
- **Design `DAHXxZui49I`, "KoM Laurel Stills 2026", 1920×803 px** (the stills' 2.39:1 picture at full width). Built by the kom-epk-builder app from `canva/ops/laurel-stills-canva.json` (`tools/build-laurel-stills-canva.py`): 160 pages, grouped SCAD (pages 2–41), AFI Fest (42–81), Reel Black Men (82–121), B.E.S.T. (122–161); page 1 is the blank page the design started with. Each page: the still as a full-bleed image, the laurel as its own image element. 40 stills (1.1.26 skipped, it repeats 1.1.25). Page names read "SCAD · 1.1.N".
- Starting positions: the 12 hand-boxed frames use the clean-area boxes from `tools/laurel-stills.py`; the rest use the calmest of nine edge spots by luminance spread. White marks (B.E.S.T. gold) except black on 1.1.41. B.E.S.T. is the stacked build (wreath over centred awards) on tall boxes, the wide winner laurel elsewhere.
- Hosting: cropped stills `press/assets/derived/canva-laurel-stills/` and stacked B.E.S.T. PNGs, on GitHub Pages. App change: an ops file with no fonts is buildable (`fontsFresh` no longer requires a font key).

## Next
1. Luke arranges the laurels and exports from Canva (his click). Page 1 is blank: delete it or leave it.
2. The design's build record lives in the app's storage for this design; "Build all" skips recorded pages if a run needs resuming.

---
**Timestamp:** 2026-10-11 · **Lane:** `epk` · **Continues:** handoff-163-epk.md · **Model:** Opus 5.5 (goose turn).

## Files
- Canva: https://www.canva.com/design/DAHXxZui49I/edit
- Ops file: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/ops/laurel-stills-canva.json · tool: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-laurel-stills-canva.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-163-epk.md · This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-164-epk.md
