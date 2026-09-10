# handoff-102-epk

## Where we left off

**This turn (Sep 9, 2026, Fable 5.1, ultracode on at Luke's word):** Luke asked for the EPK as an Illustrator project file with every asset linked ON the Drive, then switched the session to ultracode and asked for an edit sexy pass after reading the visual playbooks. Both delivered.

**The project file.** `05 MARKETING / 00 PRESS / Illustrator Projects / KillerOfMen_EPK.ai` (0.7 MB): eleven artboards on a 4 × 3 grid, layers Images and Type, every image a LINK to its Drive master (`00 PRESS/POSTER`, `STILLS`, `BTS`, and the four named `HEADSHOTS`), cropped with clipping masks, all type live Baskerville. Its export `KillerOfMen_EPK_2029_09092026_compressed.pdf` (11.1 MB, also in `press/` and `EPK BUILDS`) carries the nine page-3 links as annotations added by pypdf, since Illustrator has none. Superseded builds moved to `z_Old_EPKs`.

**One layout, two outputs.** `tools/build-epk-ai.py` does not lay pages out. It replays `tools/build-epk-kit.py` against a recording canvas, writes the recorded operations into an ExtendScript, and hands that to Illustrator through osascript. So the reportlab PDF, the `.ai` and its PDF share one set of coordinates and cannot disagree. Three Illustrator facts cost time and are now in the tool's docstring and the memory note: the canvas is ~16,000 pt square centred on the origin (a row of eleven boards throws 'CoOA'); boards need a 1,600 pt gap or a cover-fit image spills onto the neighbour's PDF page; `PDFSaveOptions` ignores its dpi values unless a downsampling METHOD is set (the first export was 75 MB, the `.ai` 800 MB with `pdfCompatible` on).

**The sexy pass.** A 51-agent workflow: five critics (typography, imagery, festival programmer, model conformance, the checklist), one merge, two judges per finding prompted to refute, one synthesis. 22 findings survived merge, 20 survived verification, all 20 applied. Full list with measurements: `review/changes.md` in the session scratchpad, summarised here:

| Page | What changed |
|---|---|
| 2 | Text at the 74 pt margin on a 900 pt measure; one label class (15.6 / 2.35 DIM) shared with pages 7 and 11; proof slug DIM not RULE |
| 3 | Title law (40 / 6.0 with the rule) extended here; column at one size, 19 pt on a 28 pt step; keys DIM, values CREAM on one baseline; link underlines DIM, footer links underlined |
| 4 | 720 pt measure, signature 56 pt under the last line; ghost 0.20 with focus 0.62 so both silhouettes stand whole |
| 5–6 | Portraits 333 × 396 on both pages; spare split evenly above, between, below; the director's block is only as tall as his words (no empty slot) |
| 7 | Hero to 1230 pt while there is no cast bio; billed rows 15.6 / 17 on a 28 pt step |
| 8 | Ten photographs on a held thirds grid, the 45-face crew frame full width as the one size break; rows land on 1296 exactly; 74 pt credit strip |
| 9–11 | Ghost stills swapped to frames bright enough to read (14, 13, 15); crew columns split at a department heading; long labels wrap instead of shrinking; boilerplate on a 540 pt measure, legal block anchored at the foot, thanks centred above it; fellows divider 180 pt |

Pages 9–11 changes live in `tools/build-credit-card.py`, so the standalone cards changed too and were regenerated (`press/KillerOfMen_Credits*.pdf`). **The sibling session that owns the card tool should pull before touching it**; I messaged it.

**BRAND.md v0.1 DRAFT** now exists at the repo root with `tokens.css`, sampled from the poster, the stills and the card constants, six chapters honestly MISSING with owners. **Codex audited it read-only and returned UNSOUND as a binding standard**: the ghost recipe did not match the pages (fixed), RULE carried text it said it never would (narrowed), the poster red reproduces one step off (sampler not committed), and the strongest ignored argument is that the spec wants a programmer routed to assets in one click, not a mood object. All of it is in the Bible's new counter-evidence table for Luke's ratification. It remains unratified.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-101-epk.md (the sibling session's) and handoff-100-epk.md (mine)
**Model:** Fable 5.1, ultracode. Two rooms worked this repo tonight; explicit paths on every commit.

## Next action (the one thing)

**Luke ratifies or amends BRAND.md v0.1**, starting with the counter-evidence table. Everything visual downstream binds to it.

## Decisions Luke owns (from the pass, in order of visibility)

1. Director's portrait: a set frame of Jordan (`KOM_Day3_TheFarm-43/-45/-46` or the centre of `Day4_Soundstage-93`), or none. Ships as none.
2. Ruoxiao Li's portrait crop: her head fills 28% of the box against 40% for the others; a crop-only zoom changes how a delivered headshot is cropped, so it is his yes/no.
3. Page 8 credit strip (kept) or full bleed like the model, since Jedidiah Woods is billed on page 10.
4. The `.ai` links absolute paths under `/Users/scrogdawg/Google Drive/...`; on another Mac Illustrator will ask to relink once, then find the rest beside the file.
5. Still open from before: logline and synopsis picks (2.1, 2.2), Betine vs Uwhubetine, MMXXV vs 2026, the post-sound department.

## Files

- The project: `KILLER OF MEN / 05 MARKETING / 00 PRESS / Illustrator Projects / KillerOfMen_EPK.ai` (Drive)
- The PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_EPK_2029_09092026_compressed.pdf
- Illustrator builder: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-ai.py
- Layout (the one source): https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-kit.py
- Card tool, amended: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-credit-card.py
- BRAND.md v0.1 DRAFT: https://github.com/Scroggdawg/kom-festival-board/blob/main/BRAND.md
- tokens.css: https://github.com/Scroggdawg/kom-festival-board/blob/main/tokens.css
- Prior handoffs: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-101-epk.md · https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-100-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-102-epk.md
