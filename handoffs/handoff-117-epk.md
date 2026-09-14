# handoff-117-epk

## Where we left off, newest first

1. **The AFI Conservatory wordmark and the page 2 fade (2026-09-14, later).** Luke put `AFIC-logo-blk.webp` (622 × 52, dark on transparent) in his Downloads; it is a master in `press/assets/LOGOS/` (Drive twin in `00 PRESS/LOGOS/`) with `AFIC-logo-cream.png` beside it, the same alpha recoloured to the page's cream so the mark reads on the dark ground (a derivative; AFI's own white version replaces it if one comes). The card draws it contained in a 330 × 56 box centred on the old slot (`contain_image`, `LOGO_BOX`); the four hairlines and the label are gone, so page 11 is 101 elements. The director's note on page 2 ("the line at the bottom of the photo is too hard"): `cover(..., fade=)` blends the bottom 16 per cent of the hero into the ground on a smoothstep ramp (`HERO_FADE`, `fade_bottom_pixels`); the Canva emitter bakes the same ramp into the derivative, so Canva shows the fade without any Canva feature (Canva itself has no image feather; the workaround there would be a gradient element overlay). Commit 3fd2901; PDF rebuilt under the same name; contract 419 elements on Pages. Canva pages 2 and 11 rebuilt (16:00–16:02Z): page 2 batch, 7 of 7, id PB3mndGH40zlgFy2, the fade visible in the editor; page 11 per-element (101 is still over the addPage cap), 101 of 101, id PBfFVhgdjlrtgm4R, the wordmark at the foot.

2. **The thank-you list is now the film's own (2026-09-14).** Luke sent the crawl's "The Filmmakers Wish To Thank" card beside the kit's page 11. Fifty-three names on the crawl, twenty-eight on the kit; twenty-five were missing: George Dewey Stanyard Jr., Kay Ann Scroggins, Elijah Anglin, Alex Benton, Ayanna Carrington, Elijah Catalan, Derrick Clarke, Zaire Davis, Roxanne Elliott, Kevin Fobes, Jillian Green, Abdullah Jeffers, Farzana Khan, Pervis Louder, Randy McKinnon, Joshua Montrel, Gage Phillips, Indu Radhakrishnan, Libby Richman, Isaac Richter, Toluwani Roberts, Camille Ryan, Ibukunoluwa Soyebo, Corey Taylor, Osewanne Uwadiale. Field 11.1 rewritten through `tools/epk.py set` (rev 27) as the crawl's list in the crawl's order: Stanyard Jr. and Kay Ann Scroggins first, then alphabetical by surname (AFI's own rule, which the old sheet did not follow). Two names normalised to the crawl: the sheet's "Tracey B" is Tracey Belizaire; "Dawn and J. Martin" is "Dawn & J. Martin". The crawl's "Baozhen ling" is kept as Ling. Not carried: the crawl's dedication line, "In Loving Memory of George Dewey Stanyard Jr." (Luke's call whether page 11 should open with it).

3. **The card sets a long list in four columns** (commits ef3d01c, 5749143). `COLS4` in `tools/build-credit-card.py` is the mirrored idiom with two columns each side of the centre gutter inside the CREW margins; `page_thanks` builds its blocks per column layout and takes four columns when the list is longer than 36 or three overflow the page at 1x (the extras band keeps three; the count rule keeps the Canva contract, measured in Libre at scale 0.96 where three just fit, on the PDF's layout). `amp_wrap` keeps a generational suffix with its surname ("GEORGE DEWEY / STANYARD JR.") and breaks an '&' entry too wide for its column at its last space ("RAGHURAM & KANCHAN / DEVARAKONDA") instead of stepping the whole block down. Type: 19 pt in Baskerville, 18 pt in Libre. PDF `KillerOfMen_EPK_1005_14092026_compressed.pdf` (replaces 1715_11092026; on the Drive). Contract 423 elements, checker clean, on Pages.

4. **Canva page 11 is rebuilt with the 53 names** (page id PBxcCj2L32qhQBrr, 105 of 105 elements). The page now exceeds the 100-element addPage cap, so Build page 11 fell to the per-element placement on its own, met the rate limit once (Canva's Dev Toolkit pops open on the alert; it is only a monitor) and the backoff carried it through. The app's tab had to be brought to the front by Luke again, and the dev server had stopped overnight (`preview_start canva-app` restarts it). The older duplicate tabs are closed; the app lives in the tab titled STILLS with the panel.

5. Before this: page 7 rebuilt without the Spectator rows, the five-on-one test page, the Libre-measured rebuild (handoffs 115–116). Luke has been editing links and verbiage himself; the design's title in Canva now reads "STILLS".

**Seen on the read-back after the rebuild (2026-09-14):** page 3's genre line in Canva now reads "SOUTHERN GOTHIC, ACTION" (Luke's own edit in the editor; the worksheet still says historical drama, Southern gothic). The line reads 60 px tall to the app, two lines' worth, though it draws as one; it is his edit and was left alone. If the genre has changed, the worksheet field should say so too (`tools/epk.py set`), or the PDF and any future rebuild of page 3 will carry the old wording.

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
