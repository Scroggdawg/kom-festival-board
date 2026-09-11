# handoff-115-epk

## Where we left off, newest first

1. **The Canva design is rebuilt from the Libre-measured contract and waits for Luke's Download click (2026-09-11 ~21:25Z).** Design `DAHU6a7HKPs`: eleven pages in order, 399 of 399 elements placed (Build all 1 to 11 into a blank page at 21:10Z; page 10's 135 elements placed one by one on the selected page at 21:13Z, none lost to the rate limit; the blank page deleted). The Share › Download dialog is open in the editor with PDF · Print · RGB · All pages · crop marks off · Flatten off. The export is the check that closes Luke's notes B, C and D: run `venv/bin/python tools/check-canva-export.py ~/Downloads/<file>.pdf` (new; per page it compares the characters carried against the contract, every paragraph's rendered bottom against its measured lines, words overlapping on one baseline, links and fonts).

2. **What the editor showed before the export.** Page 4 drawn with the signature under the last paragraph inside the foot margin; page 5 zoomed: handles clear of the lockups, Jordan's headshot in the 5.1 slot; page 7 with its gaps. The app's all-pages read back paired pages by element count and pages 4/8 and 5/7 share counts, so its WRAPPED flags for those pages were the other page's images and paragraphs; `matchOpsPage` now pairs by position on a full read (committed with this handoff, typechecks). The 33 px it reports for a 15.6 pt handle against 24.96 expected is Canva's box, not a wrap (one line is 25 px of leading; a wrapped handle would read 50+).

3. **Luke's five notes, resolved (commits ffc96ca, d6f24c4):**
   - A. Logline into 2.1 through `tools/epk.py set` (rev 25). Page 2 keeps its PROOF slug until 2.2 (synopsis) is chosen.
   - B, C, D. One cause: the contract was measured in macOS Baskerville, Canva draws Libre Baskerville (Regular 28 per cent wider on running text, Bold 9 to 11). `tools/build-epk-canva.py --face libre` (default) registers the OFL Libre files under the kit's font names before the kit loads; running text is one element per paragraph (Canva made each `\n\n` a full empty line, 81 pt on the statement); the credit card steps to scale 0.96 in Libre; `tools/check-canva-contract.py` proved the contract (0 overlaps, nothing past the foot margin) and rendered it in Libre before Canva was touched.
   - C. Jordan's portrait: the attachment was in the transcript at 1860 × 2000, but the master was on the Drive all along: `00 PRESS/HEADSHOTS/KOM Headshots-1.jpg`, 6200 × 6667, Hasselblad X1D II 50C, 14 Sep 2024, the same session as the four named headshots. Fifth master in `press/assets/HEADSHOTS` unmodified (md5 62cb6ea7…), Drive twin `Director_Jordan_Betine.jpg`, `PORTRAITS["5.1"]` points at it (no grade, no zoom), the page 5 slug is gone, field 5.6 rewritten (rev 26), `press/assets/README.md` updated.
   - E. The 100-element cap is per `addPage`; page 11 (76) fits; page 10 (now 135, CREW at the 16 pt cascade in Libre) uses the Place mode. Refinement not done: addPage the first 100, place the rest.

4. **Reportlab PDF rebuilt in Baskerville** with the logline and the headshot: `press/KillerOfMen_EPK_1603_11092026_compressed.pdf` (4.2 MB, replaces 1544_10092026 in the repo; both on the Drive under EPK BUILDS).

5. Earlier today: the first full Canva build and Luke's review (handoff-114-epk), the taste pass (113), the Codex audit (112).

## Next

1. Luke presses **Download** in the open dialog (or re-opens Share › Download › PDF Print, RGB, Flatten off, crop marks off, All pages). Canva names the file after the design: `Untitled design.pdf` in `~/Downloads`.
2. `venv/bin/python tools/check-canva-export.py "$HOME/Downloads/Untitled design.pdf"` — expect 11 pages at 1296 × 1728, 0 findings, 18 to 20 link annotations (Canva splits each link into several boxes), fonts LibreBaskerville-Regular and -Bold. If a paragraph reads longer than its measured lines, the fix is in the emitter (never the JSON): compare against `press/drafts`-style renders from `check-canva-contract.py --render`.
3. Copy the export to the Drive: `05 MARKETING / 00 PRESS / EPK BUILDS / CANVA / KillerOfMen_EPK_Canva_<date>.pdf`; rename the design (still "Untitled design"); share links (edit to director and producer, view for press); record in STATE.
4. Still open from 113/114: the one-object-or-two ruling on pages 9 to 11; the CONFIRM list; field 2.2 (synopsis) so page 2's slug can go; the PDF-import probe (skipped).

## Blockers and open items

- The Download click is Luke's.
- The app's read back cannot separate a wrapped 15.6 pt handle (50+ px) from Canva's box height (33 px) with the 1.3 factor; the export checker is the arbiter.

---

**Timestamp:** 2026-09-11 · **Lane:** `epk` · **Continues:** handoff-114-epk.md · **Model:** Fable 5.1 (goose turn: Luke's five notes executed and the design rebuilt).

## Files

- The design: https://www.canva.com/design/DAHU6a7HKPs/IoGNd4lGSEhtiq4phlGwCg/edit
- The contract (Libre-measured): https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/ops/epk-canva.json · emitter: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-canva.py · contract checker: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/check-canva-contract.py · export checker: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/check-canva-export.py
- Libre Baskerville files and provenance: https://github.com/Scroggdawg/kom-festival-board/tree/main/press/assets/derived/fonts/libre-baskerville
- The fifth headshot: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/assets/HEADSHOTS/KOM%20Headshots-1.jpg · assets README: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/assets/README.md
- Runbook: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/README.md · STATE: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/STATE.json · live-run findings: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/kom-epk-builder/BUILD-REPORT.md
- The reportlab PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_EPK_1603_11092026_compressed.pdf
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-114-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-115-epk.md
