# handoff-118-epk

## Where we left off, newest first

1. **The worksheet now mirrors the Canva design (2026-09-14, ~13:00 local).** Luke renamed the design **EPK _ KoM 2026** and edited the thank-you page, and asked for the worksheet to mirror the design's current state with no edits to the design. Done through a new mechanism, not by eye: the app's *Read design* now reads each text element's plain text (`readback.ts`, `el.text.readPlaintext()`) and posts the read-back to `tools/canva-readback-server.py` on localhost:8787, which writes `canva/readback/latest.json`; `tools/canva-readback-diff.py` diffs it against the contract page by page. The design was not touched (read-only session, no `sync()`).

2. **What the diff found, and what the worksheet now says.**
   - **Page 11.** Every couple is now two lines of their own (Ping Guo / Baozhen Ling; Mallik Ragampudi / Preethi Ragampudi; Raghuram / Kanchan; Nellai Subramaniam / Shaila Nellai; Yuhong Lai / Chunhui Wu; Santos Velazquez / Anadelis Figueroa); Dawn & J. Martin stays one line; Xie Linchen and Pervis Louder sit at the end of the last column after Xuanning Zhang. 11.1 rewritten in the design's column order, 58 lines (rev 32). **As typed in the design: "Devaraonda", both lines. The crawl spells it Devarakonda.** Mirrored, not corrected; Luke's call.
   - **Pages 2, 7, 10.** Luke deleted the three PROOF marks. The kit retires the proof class (`PROOF_SLUGS = False`; the conditions still print to the console) so a rebuild never puts them back. Page 2's synopsis, shown without a draft mark, is written into 2.2 verbatim from the design (rev 31): the worksheet's logline and synopsis are now both chosen.
   - **Page 9.** "OLAOLUWA OLUWASEUN OGUNSEYE" joined on one line (the contract wraps it at the poster measure in Libre; his line starts 6 pt left of the page edge). Layout only; nothing to mirror. A rebuild of page 9 would re-wrap it, so page 9 is not rebuilt.
   - Everything else on all eleven pages matches the contract word for word (the page-3 genre line already followed his edit).
   - Remaining differences after the rebuild are layout only: six long single names the card wraps at the four-column measure in Libre (Indu / Radhakrishnan, Sriram / Chintalapati, Ibukunoluwa / Soyebo, Raghuram / Devaraonda, Kanchan / Devaraonda, Nellai / Subramaniam) that Luke keeps on one line, overrunning the column.

3. **Rebuilt from the mirrored worksheet:** the PDF (`KillerOfMen_EPK_1005_14092026_compressed.pdf`, on the Drive) and the contract (416 elements, checker clean). **Canva was not rebuilt and must not be from this contract without Luke's word**: the design is ahead of the kit on layout (page 9's joined name, page 11's unwrapped names).

4. Earlier today (handoff-117): the dedication line, the genre rule, Spectators off page 9, the five-on-one page cancelled, the AFI wordmark, the page-2 fade, the 53-name list, the Libre-measured rebuilds.

## Next

1. Luke: "Devaraonda" on page 11, intended or a slip? If a slip, fix it in Canva and say so; the worksheet is re-mirrored the same way (read back, diff, set).
2. Export (Luke's click: Share › Download › PDF · Print · RGB · All pages · crop marks off · Flatten off); the file will be named after the design, `EPK _ KoM 2026.pdf`. Verify with `venv/bin/python tools/check-canva-export.py "$HOME/Downloads/EPK _ KoM 2026.pdf"` (its overlap check will flag the two Devaraonda lines that overrun the column; that is the design as he made it). Copy to the Drive under `05 MARKETING / 00 PRESS / EPK BUILDS / CANVA`, share.
3. Standing: whenever Luke says he edited the design, run the mirror (server, Read design, diff, set). Never rebuild a Canva page from the contract without his word.

## Blockers and open items

- The read-back's element counts differ from the contract's (images read as other types); the diff is text-only by design.
- The app's tab must be the front tab in Chrome while the panel is driven; the dev server (`preview_start canva-app`) stops between sessions.

---

**Timestamp:** 2026-09-14 · **Lane:** `epk` · **Continues:** handoff-117-epk.md · **Model:** Fable 5.1 (goose turn).

## Files

- The design: https://www.canva.com/design/DAHU6a7HKPs/IoGNd4lGSEhtiq4phlGwCg/edit
- The read-back: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/readback/latest.json · receiver: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/canva-readback-server.py · diff: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/canva-readback-diff.py
- The worksheet (2.2, 11.1): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json · the kit (`PROOF_SLUGS`): https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-kit.py
- PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_EPK_1005_14092026_compressed.pdf · contract: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/ops/epk-canva.json
- STATE: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/STATE.json · runbook: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/README.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-117-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-118-epk.md
