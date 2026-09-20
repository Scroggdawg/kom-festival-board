# handoff-126-epk

## Where we left off, newest first

1. **Cast bios for Eric Pargac and Jamal Dennis are in, everywhere the kit lives (2026-09-20).** Luke sent the two bios in chat: "Update the EPK with these two bios." They went in word for word (the em dash, "10 productions", the straight quotes round "Be Someone", "Wu-Shu" and "Ninjitsu" as typed). Erik Orjiako's and Sandra McDaniels's blocks were not touched and are byte-identical to rev 23.

| Form | State | Check |
|---|---|---|
| Worksheet `press/epk.json` 7.1 | rev 34, written through the worksheet's own writer; a bio's paragraphs are one per line inside its block | `epk.py check` clean; the two untouched blocks compared byte for byte |
| Kit PDF | `press/KillerOfMen_EPK_0958_20092026_compressed.pdf` (replaces 1005_14092026); also in the Drive `EPK BUILDS` | 11 pages, 20 links, page 7 text present, lowest text 1515 of 1728 pt |
| Canva contract | `canva/ops/epk-canva.json`, rev 34, 420 elements, served on Pages | `check-canva-contract.py`: 0 problems |
| **Canva design, page 7 (the master)** | edited in place and committed; page id and element ids unchanged; eleven pages | `export-design` PNG after the commit: `press/proofs/canva-page7-2026-09-20.png` |
| Illustrator project | `Illustrator Projects/KillerOfMen_EPK.ai` rebuilt from today's kit (it had stood since 10 Sep), export `KillerOfMen_EPK_1014_20092026` beside it, the 10 Sep export moved to `z_Old_EPKs` | 11 pages, 20 links, no overflow in the build log |

2. **How Canva was changed, and why not a rebuild.** Before touching it I read page 7 from the design: its words were exactly the 14 Sep contract's (Luke's only change there was deleting the PROOF mark), so nothing of his was at risk. The design tab a session opens starts hidden and the app's panel takes no input there, so instead of the app I used the claude.ai **Canva connector**: `read-design` with a transaction, `edit-design` `replace_text` on the two bio boxes (the element keeps Libre Baskerville, 20.8 px, its leading and colour), then `position_element` on the 13 elements below, checked on the transaction's render, then commit. One limit found by test and cancelled cleanly: `add_text` arrives in Canva's default face and nothing in the connector sets a font family, so each bio stays **one text box with a blank line between its paragraphs** rather than the contract's one element per paragraph. Spacing: one uniform 54.67 px (41 pt) gap from each bio to the next lockup (was about 67 px), the last ALSO BILLED row's baseline on the 74 pt foot margin. The procedure is written into `HARNESS-epk.md` and `canva/STATE.json` (`connector_route`, page 7's `edited_in_place`).

3. **Kit changes that made it fit.** `cast_blocks` keeps a bio's paragraphs (one per line in the field) instead of joining them; `page_cast` measures its column before drawing and lets the gap between bios give way (48 pt down to a 36 pt floor) so the last row rests no lower than page 3's footer baseline. In Baskerville nothing moves (checked block by block against the build before the rule). In Libre, the contract's face, the longer bios had run the last row 3 pt under the margin; the gap is now 41 pt there.

4. **Where the supplied text comes from.** Luke did not say who wrote the two bios. Their wording matches each actor's self-written IMDb mini biography wherever the 10 Sep captures quote it (`press/cast-bios-evidence.md`: "IMDb mini biography by: Eric Pargac" and "by: JD"). The field's note says so, and says the 10 Sep drafts stay in the field's history.

## For Luke

- The two new bios do not end with "In Killer of Men he plays …" as Erik's and Sandra's do. Left as supplied. Say the word and the sentence goes on the two new ones, or comes off the other two.
- Erik Orjiako's and Sandra McDaniels's bios are still the 10 Sep drafts. The conservative versions in `press/cast-bios-proposed-2026-09-15.md` still wait for a yes or no, and Sandra still has no bio of her own anywhere.
- Not touched: the **EPK INFO Google Doc**. Its 7.1 still shows the four 10 Sep drafts, and it is also behind on 2.2, 3.1, 5.7 and 11.1. It holds text people typed that exists nowhere else, so it can only be edited in place through a browser tab in front, one field at a time. Worth one deliberate refresh rather than a patch.
- Page 7 in Canva is now full to the foot margin. A fifth bio, or a longer one for Sandra, will need a ruling: smaller body on that page, or the ALSO BILLED rows moving.
- Export is still yours: Share › Download › PDF Print · RGB · all pages · crop marks off · Flatten off, then `tools/check-canva-export.py`.

---

**Timestamp:** 2026-09-20 · **Lane:** `epk` · **Continues:** handoff-125-epk.md · **Model:** Fable 5.1 (goose turn: Luke's one-line brief, executed).

## Files

- Proof, Canva page 7 after the commit: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/proofs/canva-page7-2026-09-20.png
- The design: https://www.canva.com/design/DAHU6a7HKPs/IoGNd4lGSEhtiq4phlGwCg/edit
- The worksheet (7.1): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Kit PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_EPK_0958_20092026_compressed.pdf
- Contract on Pages: https://scroggdawg.github.io/kom-festival-board/canva/ops/epk-canva.json
- The kit (cast_blocks, page_cast): https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-kit.py
- STATE: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/STATE.json
- Harness (the connector procedure): https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/HARNESS-epk.md
- Where the supplied wording was captured on 10 Sep: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/cast-bios-evidence.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-125-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-126-epk.md
