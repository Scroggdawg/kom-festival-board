# handoff-099-epk

## Where we left off

**This turn (Sep 9, 2026, Opus 5):** Luke asked for a version of the credit card with bigger, more legible text. **Two enlarged sizes exist now, and the layout had to change shape to get there.** `press/epk.json` unchanged at rev 20.

Pushed before the work commit, per 088.

### Why bigger meant a different layout, not just a bigger number

The first attempt simply scaled the type 1.75x and it **broke**: role labels ran off the left edge, names ran off the right, and the two columns collided. Measured rather than eyeballed afterwards — a crew column is 546pt wide and leaves **284pt for the label**, while the longest one, "Department head makeup and SFX makeup", needs **388pt at 1x already**. The two-column reference layout works today because that label happens to land beside empty space. That is luck, not design, and enlarging it removes the luck.

So both enlarged sizes **stack the role over the name, centred**, the way an end crawl does. That is also what lets the names get properly big.

| Build | Type | Layout | Pages |
|---|---|---|---|
| default | 1.0x | two columns, the reference look | 3 |
| `--medium` | 1.3x | stacked, centred | 7 |
| `--large` | 1.75x | stacked, centred | 10 |

Each carries its heading, and `CONTINUED` under it on later pages. Pages are flowed, not crammed, and a department heading is never orphaned at the foot of a column.

### Two defects found by measuring, not by looking

1. **The 1x card was overflowing its right margin and nobody had noticed** — "COSTUME, HAIR AND MAKEUP", "SAFETY AND SPECIAL EFFECTS" and "CLAUDIO DEL PINO MERCADO" all ran past it, by up to 31pt. There is now a `condense()` guard on both labels and names: anything too wide for its room shrinks a little rather than running off. **All three sizes now report zero spans outside the margins**, checked span by span rather than by block, because block grouping merges across columns and hides exactly this.
2. **The right column's labels were measured against the page margin, not the column's own left bound**, so a long label could reach back across the gutter into the other column. Fixed.

### The files got 20x smaller on the way

Ten pages each embedding a full-resolution still made a **35 MB** PDF. The backdrop sits at 16% under a 55% scrim, so it does not need six megapixels: it is now capped at 1600px and encoded as JPEG. **All six PDFs together are 2.5 MB**, down from about 48 MB. The stills themselves in `press/assets/STILLS` are untouched — this is the card's own artwork, not a delivered asset.

Transparent PNGs for all three sizes are in `press/assets/CREDITS`, 200 dpi with real alpha.

**Note on zsh:** building several variants in one loop silently produced the wrong files, because zsh does not word-split an unquoted variable and the flags arrived as one bogus argument. Each variant needs its own invocation.

Content is unchanged, so the three unresolved things still print: no sound department, `JORDAN UWHUBETINE` on the AFI page against `JORDAN BETINE` elsewhere, and `© MMXXV` against a 2026 completion year.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-098-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Luke picks a size**, and the other two can be dropped. Then, still: Jordan on Betine-or-Uwhubetine and on who designed the sound.

## Files

- Medium, 1.3x: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_Credits_medium.pdf
- Large, 1.75x: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_Credits_large.pdf
- Original, 1x: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_Credits.pdf
- Transparent PNGs, all sizes: https://github.com/Scroggdawg/kom-festival-board/tree/main/press/assets/CREDITS
- The tool: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-credit-card.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-098-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-099-epk.md
