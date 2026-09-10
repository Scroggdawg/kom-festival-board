# handoff-109-epk

## Where we left off

**This turn (Sep 10, 2026, Fable 5.1, ultracode):** Luke asked how to build the kit in Canva, plan first, execution with him logged in. **The plan is written: `press/canva-plan.md`.** Research ran as a 194-agent workflow over canva.dev and canva.com/help (read in a real browser; canva.com returns 403 to fetchers), 175 verification passes on the load-bearing claims; the run hit the account's monthly spend limit at the synthesis stage, Luke restored credits, and it resumed from cache. My own draft and the workflow's synthesis reached the same recommendation independently and were merged.

**The recommendation: a Canva app that replays the kit's operation list.** Same architecture as the Illustrator project (one layout in `build-epk-kit.py`, replayed through the recording canvas), third target. Only route that is repeatable, keeps every text run live, places at exact coordinates, and carries all nineteen links, since every link in this kit is on text and Canva's richtext API sets links on text. The Connect REST API cannot place elements at all; browser automation is 17–33 hours of approximate tracking; PDF import loses the links and, because the kit draws each line separately, would arrive as one text box per line.

**Facts that bound it:** apps run in Developer Portal Preview with no review and no plan gate; Node 24 / npm 11 are already installed; the press assets are already public over HTTPS with no redirect on GitHub Pages, so images upload by URL; apps cannot use Pro or custom fonts, so the build will be in Libre Baskerville with a post-build swap only on Pro; the 18 × 24 in pixel size is unpublished and read at runtime; a 300 dpi page cannot exist (25 M px² cap), so PDF Print governs output; Flatten must stay off. **Luke's account rendered as Canva Free on 2026-09-10.**

**Corrected on the record this turn:** the Night Feeds kit was built in Canva (PDF creator and producer fields) and carries thirty hyperlinks on pages 3, 5, 6 and 7. The kit docstring and handoff-100 said it had none; the docstring is fixed, this note corrects the handoff.

---

**Timestamp:** 2026-09-10
**Lane:** `epk`
**Continues:** handoff-108-epk.md
**Model:** Fable 5.1, ultracode. Handoff number chosen by an existence test that gates the write (the 107 lesson).

## Next action (the one thing)

**Luke answers the six decisions at the foot of `press/canva-plan.md`** (plan tier, typeface, source of truth, the mailto fallback, line-break tolerance, per-action OK for driving his editor). Then execution starts with the three probes and the page-3 pilot.

## Files

- The plan: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/canva-plan.md
- Research lanes and verdicts (session scratchpad, not committed): `scratchpad/canva/lanes.json`, `verdicts.json`, `plan.md`
- The layout the app will replay: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-kit.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-108-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-109-epk.md
