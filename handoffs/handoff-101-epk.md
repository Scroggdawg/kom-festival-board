# handoff-101-epk

## Where we left off

**This turn (Sep 9, 2026, Opus 5):** Luke asked for the credit cards built in Illustrator and put in the Illustrator Projects folder on the Drive. **Done — three real `.ai` files with live, editable text.** `press/epk.json` unchanged at rev 20.

Pushed before the work commit, per 088.

### They are generated, not drawn by hand

`tools/build-credit-card-ai.py` does **not** redraw the card. It replays `build-credit-card.py`'s own layout against a **recording canvas** that mimics the reportlab API, turns the recorded operations into ExtendScript, and hands that to Illustrator over AppleScript. **The `.ai` and the `.pdf` come out of one set of coordinates and cannot disagree** — which is the entire reason for doing it this way rather than by hand or by placing a PDF.

Change a name with `epk.py`, rebuild, and both follow.

| File | Artboards | Text frames | Size |
|---|---|---|---|
| `KillerOfMen_Credits.ai` | 3 | 230 | 11.5 MB |
| `KillerOfMen_Credits_medium.ai` | 7 | ~500 | 23.7 MB |
| `KillerOfMen_Credits_large.ai` | 10 | 245 | 35.3 MB |

Each has **three layers**: `TYPE` carrying every credit as live point text in Baskerville with the tracking converted to Illustrator's thousandths-of-an-em, and `BACKGROUND` carrying the ground, the backdrop still and its scrim, **locked**. There is no separate transparent `.ai` on purpose — hiding one layer does it, which is better than a second file to keep in sync.

Verified from inside Illustrator rather than by guessing: layer count, artboard count, frame count, the resolved font name (`Baskerville`, so the text is live and not outlined), and a PNG export of a page from each.

### Three things that had to be solved

1. **The first render looked wrong and was not.** Reading the `.ai` with a PDF renderer showed the backdrop far brighter than the PDF. Illustrator's own export shows it correct. A PDF library does not composite an `.ai`'s layers the way Illustrator does, so **an `.ai` has to be checked by Illustrator**, not by a PDF tool.
2. **Illustrator's canvas ran out.** Artboards in a single row failed at the seventh with error 5001: the canvas is 227 inches square and centred on the first artboard, so a row of 18-inch pages hits the edge. They are laid out in a **grid, four across**.
3. **AppleScript timed out at two minutes** on the bigger documents, reported only as error -1712. The bridge now allows an hour.

### Where they live, and where they do not

**On the Drive:** `KILLER OF MEN / 05 MARKETING / 00 PRESS / Illustrator Projects`, all three verified byte-identical after copying.

**Not in git.** The three files are 70 MB together and this repo publishes Pages, which caps a published site at 1 GB — the repo is already around 835 MB. `press/illustrator/` is in `.gitignore` with the reason written there. They are **generated artefacts**: the tool is committed, so anyone can rebuild them in a few minutes.

Content unchanged, so the same three things still print: no sound department, `JORDAN UWHUBETINE` on the AFI page against `JORDAN BETINE` elsewhere, `© MMXXV` against a 2026 completion year.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-100-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Luke picks a size** — then the other two `.ai` files can go, and only one needs maintaining. Then Jordan on his name and on the sound designer.

## Files

- Illustrator Projects on the Drive: https://drive.google.com/drive/folders/1Ii4lF5yfhSZBIxWafFALb7aJR4d3sTk_
- The builder: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-credit-card-ai.py
- The layout it replays: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-credit-card.py
- PDFs, all three sizes: https://github.com/Scroggdawg/kom-festival-board/tree/main/press
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-100-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-101-epk.md
