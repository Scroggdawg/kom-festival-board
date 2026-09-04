# handoff-017-festival

## Where we left off

**This turn (Sep 3, 2026):** Luke asked for Joan's picks to reach the submission-window timeline and the fit heat map, and for research on every missing site/FilmFreeway link. All three done and pushed (commit `234fda4`).

- **Windows:** 50 targets had no `open` date and so never plotted. All 50 researched — **every one of the 97 targets now draws a bar on the timeline** (was 47).
- **Heat map:** expanded **17 → 97 rows**, every target scored on the existing five dimensions, sorted by tier then total score, Joan picks starred. Scoring rubric documented at the top of `tools/heat-expand.py`. Note the `oscar` dimension now explicitly scores *the 100th Awards specifically* — a qualifying festival whose reachable edition falls outside Oct 1 2026–Sep 30 2027 scores low, because it cannot help this cycle.
- **Links:** +32 official sites, +45 FilmFreeway. Remaining gaps are correct data, not holes: **19 festivals genuinely don't use FilmFreeway** (Cannes both sections, Berlinale, Venice, SXSW, Clermont → ShortFilmDepot, Oberhausen → FilmChief, IFFR, Interfilm → ShortFilmDepot, REGARD → Zone Festival, Krakow → MyKFF, FESPACO, JCC, Luxor, College TV, DGA, BAFICI, ISCA → kc-i.jp, Anonimul → email); the real portal is named in each record's `why`. Only S16 and AFFA lack a website — neither has one (FilmFreeway/Facebook are their whole presence).

### Corrections the research forced (these change plans)

- **LA Shorts moved to Mar 4–10, 2027** — was July. It now sits weeks after PAFF/Slamdance, so the one-LA-premiere problem is *tighter*, not looser. Submissions open now, final deadline Jan 22, 2027.
- **St. Louis (SLIFF) is out for this cycle** — the Nov 2026 entry deadline closed Aug 1, 2026 (notifications went Sep 1). Nov 2027 is past the window. Heat `oscar` dropped 9 → 2. It was previously described as "the earliest qualifying swing"; that is no longer true.
- **Gary Int'l Black FF entry closed Aug 23, 2026** — the Sep 21 date I flagged as urgent last turn is materials-in-hand for accepted films, not an entry deadline. Heat `access` 9 → 5.
- **Cascade Festival of African Films is still OPEN** — deadline Sep 21, 2026, confirmed. Previously guessed as passed.
- Several held deadlines were early-bird tiers, not finals — MSPIFF actually Dec 1 2026 (held Sep 1), Ashland Nov 23 (held Oct 1), Denton Nov 4 (held Oct 15), SLO Nov 30 (held Sep 30), Show Me Shorts Jul 1 2027 (held Apr 1), FNC May 31 2027 (held May 1). All corrected — more runway than we thought.
- **Sundance now takes FilmFreeway entries** (filmfreeway.com/Sundance), contrary to the old own-portal assumption.
- **MSPIFF** is listed as the 46th edition on FilmFreeway, not the 45th (name unchanged; noted in `why`).
- **Dirty Popcorn (DE): no 2026 edition found anywhere** — dormancy risk, flagged in `why`. **NC Black FF** window is the weakest estimate on the board.

### Build notes

- Timeline and heat map are now bounded (`max-height: 72vh; min-height: 320px`) with sticky headers — the gantt's natural height is 3,837px, which would have been a wall.
- Estimated dates carry `estimated: true` and render with `~`; ~30 windows are pattern-estimates (previous cycle +1yr) because the 2027 editions aren't announced yet.
- Scripts: `tools/heat-expand.py` (scores + sort), `tools/apply-windows.py` (re-runnable JSONL merge). Research JSONL archived in the session scratchpad.

**Verification:** `validate(DATA)` clean, zero console errors, 97 gantt rows / 97 gantt bars / 97 heat rows / 75 Joan stars, 173 link buttons live. **Screenshots would not render in the Browser pane this session** (blank frames, `innerHeight: 0` — the same pane instability logged in handoffs 010–011); verification was done via DOM and computed-style checks instead. Stated plainly rather than claimed as visual confirmation.

**Direction we were going:** Board data is now complete enough to run the campaign off. Still open: (1) **ABFF/MVAAFF 2026 confirm-or-deny** — still the one blocking question; (2) the September run, now re-dated below; (3) AFRIFF email; (4) whether Sundance went in by Aug 31; (5) Luke's PAT.

---

**Timestamp:** 2026-09-03
**Lane:** `festival`
**Continues:** handoff-016-festival.md
**Model:** Fable 5 for the merge, then **Opus 5** after Fable hit its monthly spend limit mid-turn (five research agents died and were relaunched on Sonnet). **Goose turn** — research, merge, deploy, verify.

## Next action (the one thing)

**Luke: ABFF/MVAAFF confirm-or-deny.** Then the corrected near deadlines: **Flickerfest Sep 14 · IFFR Sep 15 · PAFF ~Sep 16 · SBIFF ~Sep 18 · Cascade Sep 21 · Clermont Sep 24 (the France call) · Ann Arbor Sep 30 · SXSW Oct 1 · Tampere Oct 1 · In the Palace Oct 1 · Slamdance Oct 6.** (Gary is closed — remove it from the run.)

## Files

- Live board: https://scroggdawg.github.io/kom-festival-board/
- Mirror: https://claude.ai/code/artifact/5dadab1f-b512-47eb-a2b4-e04cc9d18ff5
- Joan readout: https://claude.ai/code/artifact/46eeb56a-63da-472d-9a3f-1d74d33d4384
- Heat script: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/FESTIVAL%20CAMPAIGN/site/tools/heat-expand.py
- Window merge script: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/FESTIVAL%20CAMPAIGN/site/tools/apply-windows.py
- Prior handoff: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-016-festival.md

file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-017-festival.md
