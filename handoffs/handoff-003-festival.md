# handoff-003-festival

## Where we left off

**This session (Aug 25, 2026, evening):** Rebuilt the board's top into Luke's 8-counter dashboard + Key Dates section, tinted the dream list and heat map into the tier color system, scrubbed all DP-sheet mentions, and put the board on a public URL: **https://scroggdawg.github.io/kom-festival-board/**

- **Aug 25 PM (this turn)** — Dashboard reworked (117 researched / 46 yes / 57 maybe / 14 no, then applied/accepted/rejected/pending at 0); Key Dates cards (Sundance days-left with date, Oscar-window days-left without); dream-list rows tinted by tier; heat map rows now per-tier sequential ramps (all validator-passed); day counts compute live from the viewer's date; GitHub repo `Scroggdawg/kom-festival-board` created (public) and GitHub Pages verified live (HTTP 200).
- **Aug 25 PM (prior turn)** — Luke's first notes applied: distinct tier colors, A-list re-entered on the completion argument, DP Craft Sheet split off, asks trimmed.
- **Aug 25 AM** — Research raid (117 festivals) and first board publish.

**Direction we were going:** Board is now shareable; next is wave-1 submissions and the next-ring raid toward ~150 winnable festivals.

---

**Timestamp:** 2026-08-25 ~17:20 PDT
**Lane:** `festival`
**Continues:** handoff-002-festival.md
**Model:** Fable 5. **This turn was a goose** — build and deploy on Luke's spec.

## What changed

- **Public site live:** https://scroggdawg.github.io/kom-festival-board/ — repo https://github.com/Scroggdawg/kom-festival-board (public; Pages from main). Source of truth for the live page: `FESTIVAL CAMPAIGN/site/index.html` (a git repo — commit + push there to update the site).
- **Artifact updated** (same URL): https://claude.ai/code/artifact/5dadab1f-b512-47eb-a2b4-e04cc9d18ff5
- **Campaign ledger convention:** the `CAMPAIGN` const at the top of the board file holds `applied/accepted/rejected` arrays — update those as submissions go out; the dashboard and pending count derive from them.
- New heat ramps (validator-passed on #171310): blue #3a4a66→#63a2f2 · orange #63402b→#e37b42 · green #2e4f3e→#45c493.
- DP Craft Sheet no longer referenced anywhere on the board (sheet itself unchanged: https://claude.ai/code/artifact/179b2978-aa52-4762-803d-d01666d3103d).

## Decisions + assumptions

- **Repo is PUBLIC** — required for free GitHub Pages, and the point is a sendable link. Contents are the campaign strategy; Luke asked for hosting to share, so treated as authorized. Flag if the premiere-chess details feel too open; a Vercel deploy from a private repo is the alternative.
- Maybes = 117 researched − 46 on board − 14 ruled out = 57 (derived).

## Open uncertainty

- **Vercel is NOT done** — no CLI installed and no token; needs Luke: either import the repo at vercel.com/new (auto-deploys on every push thereafter) or authorize the Vercel connector in claude.ai settings so an agent can drive it.
- Visual pass this round was header-only + DOM checks (Browser pane kept hiding); worth one human scroll of the live site.
- Prior opens unchanged: PAFF ladder, AFI email answers, premiere assumption, College TV Awards window.

## Next action (the one thing)

**Submit Sundance before Aug 31** — the live site's hero counter is now literally counting it down.

## Files

- Live site: https://scroggdawg.github.io/kom-festival-board/
- Repo: https://github.com/Scroggdawg/kom-festival-board
- Artifact: https://claude.ai/code/artifact/5dadab1f-b512-47eb-a2b4-e04cc9d18ff5
- Site source: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/FESTIVAL%20CAMPAIGN/site/index.html
- Prior handoff: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-002-festival.md

file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-003-festival.md
