# handoff-127-epk

## Where we left off, newest first

1. **Erik Orjiako's bio is in, in the worksheet and in every form of the kit (2026-09-21).** Luke sent it in chat: "Update this bio on epk and worksheet." It replaces the 10 Sep draft, which stays in field 7.1's history. The other three blocks are byte-identical to rev 34.

| Form | State | Check |
|---|---|---|
| Worksheet `press/epk.json` 7.1 | rev 35, through the worksheet's writer | `epk.py check` clean; the three untouched blocks compared byte for byte |
| Kit PDF | `press/KillerOfMen_EPK_1250_21092026_compressed.pdf` (replaces 0958_20092026); in the Drive `EPK BUILDS` | 11 pages, 20 links; page 7 has the new text, not the old |
| Canva contract | rev 35, 420 elements, served on Pages | `check-canva-contract.py`: 0 problems |
| **Canva design, page 7 (the master)** | edited in place through the connector and committed; ids unchanged; eleven pages | `press/proofs/canva-page7-2026-09-21.png`, exported after the commit |
| Illustrator project | `KillerOfMen_EPK.ai` rebuilt, export `KillerOfMen_EPK_1252_21092026` beside it; yesterday's export to `z_Old_EPKs` | 11 pages, 20 links, no overflow |

2. **Three slips in the supplied text were corrected, and only those.** "performaces" became "performances", "Malcom X" became "Malcolm X" (the play's title in the same sentence spells it right), and the semicolon in `production of; "When Yuri Met Malcolm."` came out. Everything else is as Luke typed it, including the comma after "humor" and the unhyphenated "Los Angeles based" and "character driven". A character diff against his message shows exactly those three changes. The field's note lists them, so the supplied wording is on record. Reason for not leaving them: this is the page a programmer reads, and neither is a style choice. One word from Luke puts them back.

3. **The claim checks out.** East West Players' own page (eastwestplayers.org/wymm, read 21 Sep) lists Erik Orjiako among three actors alternating as Malcolm X in *When Yuri Met Malcolm*, the Theatre for Youth Tour 2026-2027. "Currently touring" will date; the note says to revisit it when the tour ends.

4. **Canva spacing.** His new bio sets one line shorter in Canva (7 lines, was 8). The freed 32 px is shared evenly: the gap from each bio to the next lockup is 62.67 px (47 pt), up from yesterday's 54.67. The ALSO BILLED rows did not move and still rest on the foot margin. Correction to yesterday's record: a body box of n lines is 32 × (n − 1) + 24.29 px, so yesterday's two boxes were 18 and 12 lines, not 17 and 11; the layout used the measured heights, so nothing on the page was off. STATE and the harness are corrected.

## For Luke

- Sandra McDaniels's is now the only draft left, and the only bio that ends "In Killer of Men she plays the Elder." Her own bio is still wanted (she, or NTA Talent Agency). The conservative version of hers still waits for a yes or no.
- The EPK INFO Google Doc still shows all four 10 Sep drafts (and is behind on 2.2, 3.1, 5.7, 11.1). Not touched; he asked for the EPK and the worksheet.
- Export is still his click: Share › Download › PDF Print · RGB · all pages · crop marks off · Flatten off, then `tools/check-canva-export.py`.

---

**Timestamp:** 2026-09-21 · **Lane:** `epk` · **Continues:** handoff-126-epk.md · **Model:** Fable 5.1 (goose turn: Luke's one-line brief, executed).

## Files

- Proof, Canva page 7 after the commit: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/proofs/canva-page7-2026-09-21.png
- The design: https://www.canva.com/design/DAHU6a7HKPs/IoGNd4lGSEhtiq4phlGwCg/edit
- The worksheet (7.1): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Kit PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_EPK_1250_21092026_compressed.pdf
- Contract on Pages: https://scroggdawg.github.io/kom-festival-board/canva/ops/epk-canva.json
- STATE: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/STATE.json
- Harness: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/HARNESS-epk.md
- East West Players, the production's page: https://www.eastwestplayers.org/wymm
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-126-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-127-epk.md
