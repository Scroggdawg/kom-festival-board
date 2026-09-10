# handoff-098-epk

## Where we left off

**This turn (Sep 9, 2026, Opus 5):** Luke liked the credit card and asked for the background to be transparent. Done, and delivered in two forms because one of them has a trap in it. `press/epk.json` unchanged at rev 20.

Pushed before the work commit, per 088.

### What transparent means here, and the trap

`tools/build-credit-card.py` gained two flags:

```
--transparent   draw no ground at all, so the pages keep their alpha
--png           also render each page to press/assets/CREDITS at 200 dpi
```

**The trap: a transparent PDF opened in Preview looks blank.** The type is cream, and a viewer paints white behind a page that carries no ground of its own. That is the format working, not failing, and it will look like a broken file to anyone who double-clicks it. It is written into the tool's own docstring so the next person does not file a bug against it.

So both were built:

| File | What it is for |
|---|---|
| `press/KillerOfMen_Credits.pdf` | the opaque card, unchanged, **12.7 MB** |
| `press/KillerOfMen_Credits_transparent.pdf` | vector, no ground, for placing in a layout app. **33 KB** — the stills were the whole weight |
| `press/assets/CREDITS/*_transparent.png` | 3600 × 4800, real alpha, for an edit or a comp |

### Verified, not assumed

The PNGs were checked rather than trusted: mode RGBA, alpha spanning the full 0–255, corner pixels at 0, type at 255. **Only 2.51% of pixels carry any opacity** — that is the type and nothing else. Composited over a checkerboard and over the wheel-of-fire still to prove both cases.

**One thing to know when you use it:** over hot areas of a frame the cream loses contrast. Over the flames in that still it is still readable but it is close. A layout that lands the card over a bright plate wants a scrim under it, which the opaque version already has at 55%.

The card content is unchanged. The three unresolved things from 097 still print exactly as they did: no sound department, `JORDAN UWHUBETINE` on page 3 against `JORDAN BETINE` on pages 1 and 2, and `© MMXXV` against a 2026 completion year.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-097-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Jordan, two questions, one message: Betine or Uwhubetine, and who designed the sound.** Unchanged since 097 and still the only thing between this card and finished.

## Files

- Transparent PNGs: https://github.com/Scroggdawg/kom-festival-board/tree/main/press/assets/CREDITS
- Transparent PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_Credits_transparent.pdf
- Opaque card: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_Credits.pdf
- The tool: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-credit-card.py
- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-097-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-098-epk.md
