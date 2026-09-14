# handoff-117-epk

## Where we left off, newest first

1. **The thank-you list is now the film's own (2026-09-14).** Luke sent the crawl's "The Filmmakers Wish To Thank" card beside the kit's page 11. Fifty-three names on the crawl, twenty-eight on the kit; twenty-five were missing: George Dewey Stanyard Jr., Kay Ann Scroggins, Elijah Anglin, Alex Benton, Ayanna Carrington, Elijah Catalan, Derrick Clarke, Zaire Davis, Roxanne Elliott, Kevin Fobes, Jillian Green, Abdullah Jeffers, Farzana Khan, Pervis Louder, Randy McKinnon, Joshua Montrel, Gage Phillips, Indu Radhakrishnan, Libby Richman, Isaac Richter, Toluwani Roberts, Camille Ryan, Ibukunoluwa Soyebo, Corey Taylor, Osewanne Uwadiale. Field 11.1 rewritten through `tools/epk.py set` (rev 27) as the crawl's list in the crawl's order: Stanyard Jr. and Kay Ann Scroggins first, then alphabetical by surname (AFI's own rule, which the old sheet did not follow). Two names normalised to the crawl: the sheet's "Tracey B" is Tracey Belizaire; "Dawn and J. Martin" is "Dawn & J. Martin". The crawl's "Baozhen ling" is kept as Ling. Not carried: the crawl's dedication line, "In Loving Memory of George Dewey Stanyard Jr." (Luke's call whether page 11 should open with it).

2. **The card sets a long list in four columns** (commits ef3d01c, 5749143). `COLS4` in `tools/build-credit-card.py` is the mirrored idiom with two columns each side of the centre gutter inside the CREW margins; `page_thanks` builds its blocks per column layout and takes four columns when the list is longer than 36 or three overflow the page at 1x (the extras band keeps three; the count rule keeps the Canva contract, measured in Libre at scale 0.96 where three just fit, on the PDF's layout). `amp_wrap` keeps a generational suffix with its surname ("GEORGE DEWEY / STANYARD JR.") and breaks an '&' entry too wide for its column at its last space ("RAGHURAM & KANCHAN / DEVARAKONDA") instead of stepping the whole block down. Type: 19 pt in Baskerville, 18 pt in Libre. PDF `KillerOfMen_EPK_1005_14092026_compressed.pdf` (replaces 1715_11092026; on the Drive). Contract 423 elements, checker clean, on Pages.

3. **Canva page 11 still carries the 28-name list.** The app's tab must be the front tab in Chrome for the app panel to take input (the same freeze as handoff-116); the dev server had also stopped overnight and was restarted (`preview_start canva-app`). A fresh tab with the app is open beside Luke's (the one titled STILLS with the app panel); the older duplicate tabs are closed. Once it is in front: Load (423 elements), Read page size, pick the three fonts, delete page 11, select page 10, Build page 11, read back.

4. Before this: page 7 rebuilt without the Spectator rows, the five-on-one test page, the Libre-measured rebuild (handoffs 115–116). Luke has been editing links and verbiage himself; the design's title in Canva now reads "STILLS".

## Next

1. Luke: the dedication line on page 11, yes or no; the five-on-one filmmakers page, yes or no; Spectators off pages 3 and 9, yes or no.
2. Export (Luke's click: Share › Download › PDF · Print · RGB · All · crop marks off · Flatten off), verify with `tools/check-canva-export.py`, Drive copy under `EPK BUILDS / CANVA`, share.
3. Open from before: field 2.2 (synopsis) so page 2's slug can go; the one-object-or-two ruling on pages 9–11; the CONFIRM list.

---

**Timestamp:** 2026-09-14 · **Lane:** `epk` · **Continues:** handoff-116-epk.md · **Model:** Fable 5.1 (goose turn).

## Files

- The design: https://www.canva.com/design/DAHU6a7HKPs/IoGNd4lGSEhtiq4phlGwCg/edit
- The thanks field, 11.1, in the worksheet: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json · the card: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-credit-card.py
- Contract on Pages: https://scroggdawg.github.io/kom-festival-board/canva/ops/epk-canva.json · PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_EPK_1005_14092026_compressed.pdf
- STATE: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/STATE.json
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-116-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-117-epk.md
