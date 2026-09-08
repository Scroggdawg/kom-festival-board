# handoff-059-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** Luke asked for the one sheet as a PDF. Delivered `press/EPK-breakdown.pdf` — one page, Letter, all eleven page-sections plus Assets, 47 fields, each with a colour chip (green have it · blue you can get it, nobody blocking · amber waiting on someone) and a right-aligned note naming who holds it. Two footer blocks: **The one unlock** (the end-credit roll) and **Tonight, needing nobody** (six numbered actions). Print-appropriate light ground, not the dark board palette — a dark fill is wrong for something the team will print and mark up.

**Built twice.** The first attempt broke the column balance: everything piled into column one, page 11 ran off the bottom, and both footer blocks were lost below the fold. **Caught by rendering the PDF in the browser and looking at it**, not by assuming it worked. Rebuilt to balance the eleven blocks across two columns by total height and draw the footer beneath whichever column runs longer. Verified by rendering again.

Also committed `tools/build-epk-pdf.py` so the PDF regenerates from `epk.json` and never drifts from the data — it prints a warning if the footer creeps toward the bottom margin, which is the failure the first build had.

**Toolchain note for this machine:** no LibreOffice, no pandoc, no pdftoppm. PDFs are built with `reportlab` in the session scratch venv (`$SCRATCH/venv`), and rendered for checking by opening the `file://` URL in the browser pane.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-058-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**Luke: send the two drafted messages (Yeo, the HoDs) — a minute each, a column of fields apiece.** Then the end-credit roll. Standing offer, unanswered: this lane can import the FilmFreeway export into `data.json` so the live board stops recording 0 submissions against a real 30. Real clock starts **Sep 15** (Rotterdam, Carthage), then SBIFF 18th, Clermont 24th, Aspen 25th.

## Files

- PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/EPK-breakdown.pdf
- Rebuild script: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-pdf.py
- Worksheet data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Messages: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/messages-to-send.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-058-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-059-festival.md
