# handoff-116-epk

## Where we left off, newest first

1. **Luke's three asks after viewing the rebuilt design in Canva (2026-09-11, he had not exported); his ruling on the crew pages: "keep the existing crew pages for now" (no merging into fewer elements).**
   - *"A test page where all 5 filmmakers fit on a single page."* Built as a variant, not wired in: `page_bios_single()` in the kit, rendered by the new `tools/build-epk-variants.py` to `press/drafts/2026-09-11/p05-variant-five-on-one.pdf` and `.png`. Pages 5–6's law unchanged (one text edge, portrait alternating sides); the portrait height is what one page allows: 224 × 188 pt against 396 × 333, and every bio still sets at 19 pt in Baskerville (in Libre the longer bios would step down). Luke rules; if yes, it replaces pages 5 and 6 (the kit becomes ten pages, the credit pages shift to 8–10, and the Canva design is rebuilt from page 5 on).
   - *"Cast page: lose the two spectator billings."* `CAST_PAGE_DROP = ("spectator",)` filters page 7's ALSO BILLED rows (commit 916cf12); the contract (395 elements) is on Pages. Pages 3 (the programmer's CAST block) and 9 (CREDITS) still list the two Spectators from the same fields; not dropped there without his word. **Page 7 in the Canva design is rebuilt** (19 of 19 elements, page id PByp6bRzmnfzd0gT): once Luke brought the app's tab to the front, Load, three font picks, delete the old page 7, select page 6, Build page 7; it landed after page 6, eleven pages in order.
   - *"Did we solve the element ceiling for the crew page?"* The ceiling is Canva's, per `addPage` call, 100 elements, undocumented, and it is not lifted; it is worked around. Page 10 (CREW) has 135 elements in Libre (126 in the first build) and both times went on in full through the Place mode (`addElementAtPoint` one by one on the selected page, paced 150 ms, backoff to 16 s). The refinement not done: `addPage` the first 100 and place only the remainder. The way to get under 100 would be merging each role | name pair into one two-tone line (the pairs are separated by the gutter, so the current merge does not take them); not done, it changes how a collaborator edits the page.

2. **The Libre-measured rebuild (handoff-115):** design `DAHU6a7HKPs`, eleven pages, 399 of 399 elements, then 395 after the cast change. Not exported yet; the Share › Download dialog settings are PDF · Print · RGB · All pages · crop marks off · Flatten off. `tools/check-canva-export.py <pdf>` verifies an export against the contract.

3. Earlier today: Luke's five notes executed (handoff-115), the first full build and his review (114), the taste pass (113).

## Blockers and open items

- The app's tab (`…/edit?ui=…`) must be the front tab in Chrome while the app is driven; Luke's second tab of the design froze the app's iframe until he brought the app's tab forward ("you should be up on the tab group"). Keystrokes meant for a frozen app panel reach the editor instead: a Backspace deleted page 2 (2026-09-11 ~17:35 local); Undo restored it, eleven pages confirmed. Drive the editor only with the app's tab in front.

## Next

1. Luke rules on the five-on-one page (yes → wire it in, ten pages, rebuild from page 5) and says whether the Spectators also leave pages 3 and 9.
2. Export (Luke's click), verify with `tools/check-canva-export.py`, Drive copy under `05 MARKETING / 00 PRESS / EPK BUILDS / CANVA`, rename the design, share.
3. Open from before: field 2.2 (synopsis) so page 2's slug can go; the one-object-or-two ruling on pages 9–11; the CONFIRM list.

---

**Timestamp:** 2026-09-11 · **Lane:** `epk` · **Continues:** handoff-115-epk.md · **Model:** Fable 5.1 (goose turn).

## Files

- The design: https://www.canva.com/design/DAHU6a7HKPs/IoGNd4lGSEhtiq4phlGwCg/edit
- Five-on-one test page: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/drafts/2026-09-11/p05-variant-five-on-one.pdf (PNG beside it) · renderer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-variants.py
- The kit (page_bios_single, CAST_PAGE_DROP): https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-kit.py
- Contract: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/ops/epk-canva.json · reportlab PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_EPK_1715_11092026_compressed.pdf
- STATE: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/STATE.json · runbook: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/README.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-115-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-116-epk.md
