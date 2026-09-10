# handoff-108-epk

## Where we left off

**This turn (Sep 10, 2026, Fable 5.1):** Luke sent the filmmakers' Instagram handles and IMDb links; the card session wrote them to `press/epk.json` 5.7 (rev 22). **The bio pages now carry them**: each filmmaker's handle, exactly as typed, and IMDB sit on the heading baseline in the label tone, after the heading when it sits left, before it when it sits right, every one a live PDF link. Ten new annotations; the kit has 19 in all. Rebuilt and current: `KillerOfMen_EPK.ai` on the Drive and `press/KillerOfMen_EPK_1234_10092026_compressed.pdf` (9.8 MB). The 11:12 build moved to `z_Old_EPKs`.

**The Google Doc did not get updated, and here is the honest state.** Luke also said "add these to the doc." That is the `build-epk-doc.py → gdoc.py push` pipeline from handoff-096, which recorded one successful push on Sep 9 with a token at `~/.kom-gdoc/token.json`. That directory does not exist on this Mac now, and no token exists anywhere under `$HOME`. Neither this room nor the card session can push, and re-consenting is an OAuth grant that only Luke's own click can make. **Two ways forward, both his:** run `gdoc.py auth` once in his browser (the token lands back where the tool expects it) and either room pushes rev 22; or File → Import → Replace in the Doc from the `.docx` that `build-epk-doc.py` writes.

**Standing from last turn, unchanged:** the kit is two objects (pages 1–8 cream Regular, 9–11 the Night Feeds form) and BRAND.md carries the eight contested rows. Luke's one-kit-or-two ruling is still the thing everything waits on.

---

**Timestamp:** 2026-09-10
**Lane:** `epk`
**Continues:** handoff-106-epk.md
**Model:** Fable 5.1. Two rooms, one tree, explicit paths.

## Next action (the one thing)

**Luke: `gdoc.py auth` in your browser, then say so**, and the EPK INFO Doc gets rev 22 within the minute. Until then the Doc is one revision behind the worksheet and the kit.

## Files

- The PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_EPK_1234_10092026_compressed.pdf
- The project: `KILLER OF MEN / 05 MARKETING / 00 PRESS / Illustrator Projects / KillerOfMen_EPK.ai` (Drive)
- The layout with the 5.7 reader: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-kit.py
- The Doc pipeline this room did not run: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/gdoc.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-106-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-108-epk.md
