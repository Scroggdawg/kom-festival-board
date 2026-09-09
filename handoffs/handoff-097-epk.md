# handoff-097-epk

## Where we left off

**This turn (Sep 9, 2026, Opus 5):** Luke sent a crew card from another production as a style reference and asked for one for this film. **Built: `press/KillerOfMen_Credits.pdf`, three pages**, plus `tools/build-credit-card.py` that regenerates it. `press/epk.json` unchanged at rev 20.

Pushed before the work commit, per the rule in 088.

### The card

Three pages at **1296 × 1728 pt** — the EPK's own page size from `press/epk-spec.md`, so they drop straight in as pages 9 to 11 rather than needing a re-layout.

| Page | Content |
|---|---|
| 1 | **CAST** — nine billed roles, then key credits, then the fifteen extras |
| 2 | **CREW** — two columns, role right-aligned, name left, department headings. The reference layout |
| 3 | **THANKS** — thirty thank-yous, the five AFI fellows, and the three required boilerplate paragraphs |

Set in Baskerville with letterspaced caps, cream `#efe6d6` on near-black, roles held back in `#b9a88c` so the names read first. A still sits behind each page at 16% under a 55% scrim. Text is **selectable** — 4,018 characters extract cleanly — which `epk-spec.md` calls out explicitly as the thing the model kit got wrong.

### Nothing is retyped

Every name is parsed out of `press/epk.json` fields 9.1, 9.2, 10.1, 11.1 and 11.3 at build time. **The card has no copy of its own and cannot drift from the worksheet.** Change a name with `epk.py set` and rebuild.

Two details in the tool worth knowing:

- **Parsing stops at the first line that is not `role | name`.** Those fields carry trailing prose — the TBD-sound caveat, the twelve blank positions, the Uwhubetine mismatch — and that prose must never print onto a credit card. It stays in the worksheet.
- **The stills carry their letterbox bars in the pixels.** Drawn as a background they put a hard horizontal edge across the page. `unletterbox()` finds the picture rows and crops them out, detected rather than hardcoded so any still works.

Leading and gaps are scaled by one fitted factor per page, clamped between 1.0 and about 1.6, so a page fills its column instead of stopping two-thirds down. First render did exactly that and it is why the helper exists.

### What the card cannot fix

It is only as good as the workbook, and the workbook is a working document. **These carry forward unchanged and are visible on the card as absences:**

1. **No sound department.** Production sound mixer and boom operator appear because they were on set. Everything post — sound designer, re-recording mixer, editors, foley — was TBD on the sheet, so the CREW page has a two-line SOUND block where the reference card has fifteen. This is the most conspicuous gap on the page.
2. **`JORDAN UWHUBETINE` is printed on page 3**, because that is what the fellows list says, while pages 1 and 2 say `JORDAN BETINE` from the billing block. **The card shows the contradiction rather than hiding it.** That is deliberate — it is not for me to pick which name a person uses — but it must be settled before this goes anywhere.
3. **`© MMXXV`** is on the card against a 2026 completion year in `3.5`.
4. Twelve blank crew positions are simply absent; location manager and property master are the two a programmer would notice.

There is also **no `BRAND.md` for this project** — the card was designed off the poster and the film's own grade rather than a ratified look. Worth building one before more surfaces ship.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-096-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Jordan, two questions, one message: Betine or Uwhubetine, and who designed the sound.** Both are visible holes in a card that is otherwise ready. Then rebuild and the card is current.

## Files

- The card: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_Credits.pdf
- The tool: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-credit-card.py
- On the Drive: `KILLER OF MEN / 05 MARKETING / 00 PRESS / EPK BUILDS`
- Credits source: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/credits/2513%20KOM%20Credits%2011-5-SDnotes.xlsx
- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-096-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-097-epk.md
