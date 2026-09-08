# handoff-063-epk

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** Luke asked for a background colour per section — saturated header band, less saturated rows beneath it, text staying white. Applied to `epk.html` and to the in-chat render. Still no intake; nothing has been sorted into the list yet.

### The colours were computed, not chosen

`dataviz` loaded first, per the standing rule. Every candidate had to clear **WCAG 4.5:1 against cream** before it was considered at all, and the eleven-band chain was solved for the largest adjacent separation the constraints allow, using the skill's own OKLab and Machado CVD simulation.

**Measured, then verified again in the live DOM rather than trusted from the generator:**

| | Result | Gate |
|---|---|---|
| Cream on the header bands | 4.51 – 7.56 : 1 | 4.5 : 1 · **pass** |
| Cream on the row bands | 10.52 – 10.71 : 1 | 10.5 : 1 · **pass** |
| Worst adjacent, protan/deutan | ΔE 8.5 | target 8 · **pass** |
| Worst adjacent, normal vision | ΔE 11.8 | floor 15 · **below** |

### The one thing that does not pass, stated plainly

Eleven bands cannot clear a normal-vision floor built for eight categorical series. The skill is explicit that secondary encoding does **not** excuse this particular gate, so this is a deliberate departure, not an oversight: here colour is wayfinding for a document, and identity is carried by the number and the section name in cream on every band and every row. Nothing is encoded by colour alone.

**The trade curve, measured** — how much header-lightness variation buys how much separation:

| Header L spread | Normal ΔE | CVD ΔE | |
|---|---|---|---|
| 0.06 | 8.0 | 6.1 | cvd warn |
| 0.10 | 8.9 | 7.0 | cvd warn |
| **0.14** | **11.8** | **8.5** | **chosen — cvd passes, hierarchy still uniform** |
| 0.18 | 14.5 | 8.4 | |
| 0.23 | 17.8 | 10.0 | both pass, headers visibly uneven |
| 0.28 | 22.4 | 15.7 | both pass, hierarchy gone |

A free solve did clear both gates at ΔE 21.4/14.1, and was rejected on looking at it: it alternated very dark and bright headers, and section 1's header landed within 0.1 of its own rows — the opposite of what was asked for. **Luke's hierarchy is the governing constraint; the floor is the one that gave way.** If he would rather clear it, the route is fewer bands — group the eleven sections into about five families — and that is his call, not mine.

### Also this turn

- Row numbers are cream at 65% (worst 5.39:1 measured across all eleven bands); header text is full cream, because any reduction there drops under 4.5:1.
- `press/EPK-breakdown.pdf` was **not** recoloured. It is a light-ground artifact meant to be printed and marked up; a dark banded palette is wrong for that, and Luke was talking about the list on screen.
- `tools/build-epk-pdf.py`, `tools/epk.py`, `tools/epk_server.py` and `press/epk.json` are untouched. This was a stylesheet change plus one line that hands each section its pair of colours.

---

**Timestamp:** 2026-09-08
**Lane:** `epk`
**Continues:** handoff-062-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Luke: paste the end-credit roll.** It fills `3.14`, `3.15`, `7.1`, `9.1`, `9.2`, `10.1`, `11.1` and `11.3` — eight fields across six pages, no hard drives needed. `2.1` and `2.2` cost a minute each and need nobody. Still open from last turn: decimal `3.15` or Roman `III.15`.

## Files

- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Page source: https://github.com/Scroggdawg/kom-festival-board/blob/main/epk.html
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-062-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-063-epk.md
