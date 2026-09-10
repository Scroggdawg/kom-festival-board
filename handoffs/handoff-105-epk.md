# handoff-105-epk

## Where we left off

**This turn (Sep 9–10, 2026, Fable 5.1 as orchestrator, Opus/Fable subagents):** Luke sent the NightFeeds EPK and said *"using this as the guide, edit and improve upon the full credit cards."* **Done: the three-page card is rebuilt to the reference's structure, verified twice by adversarial panels, regenerated as PDF, PNG and Illustrator, and on the Drive.** `press/epk.json` untouched (rev 20 at the start; other lanes moved it since).

Pushed before the work commit, per 088. Numbered 105: 104 is the other EPK session's.

### What Luke will see first, so it is said first

**"SOUND DESIGNER — STILL UNKNOWN" is printed on the CREW page as a credit line.** That is deliberate: the design's rule is that data gaps stay visible, and the previous card's filter that hid it is gone. It is the most honest thing on the page and the one thing that must not ship. It disappears the moment Jordan names the sound designer and the worksheet is updated; nothing else changes.

### How it was built

A workflow, because the brief was a redesign against a reference: four analysis lenses (typography, layout, imagery, content) read the reference and the old card and measured them; three designers drafted from three angles (faithful, film-first, legibility-first); three judges scored; a synthesis produced one spec; one builder rewrote `tools/build-credit-card.py`; four adversarial verifiers tried to refute it and **all four passed in round one**. A fix round then applied their should-fix items. The harness killed that fix-round builder mid-edit — it goes silent for three minutes while regenerating a twelve-hundred-line file and the stall detector reads that as dead — after it had landed all but one item. I applied the last one by hand (page 3's crop), rebuilt, and ran a second, builder-free verification workflow. **Second verification, five agents, builder-free: four of four lenses PASS, zero blocking, three should-fix, seven nits.** The should-fixes: (1) page 3's lantern at anchor 0.50 sat under the middle thanks column — applied: `P3 = (25, 0.45, 0.70)`, lantern in the margin and the page nearer the guide's brightness, gate 49.7 against 75; (2) on the *enlarged* sets the final THANKS page opens with a blank head (medium p9 at y 437, large p12 at y 285) because the legal tail is foot-anchored even when it is alone on the page — left open until Luke picks a size, the fix is in `page_thanks()`; (3) this handoff had to state the reference-p11 sections the card lacks, which the next paragraph does.

**The critic's one line, verbatim in spirit: the pictures run two to three times darker than the guide's.** NightFeeds carries every page on its still (page means 41–46); ours read as black cards with a hint of image (14–20). That is the spec's chosen alphas, not a build error, and the gate has headroom — page 3 is now brighter for it. Whether the whole card should come up further is a cinematographer's call, so it is Luke's.

**Absent from page 3, as data, not tool bugs:** SPECIAL THANK YOU TO, the footage and equipment courtesy lines, and the animal-welfare line — all unresolved in 11.3, so the page gains lines when they resolve. **Printed twice, as the data reads:** Still photographer and Colorist appear in both 9.1 and 10.1, so both appear on CREW; a worksheet decision removes one. **Five role labels wrap on CREW** (SECOND ASSISTANT | DIRECTOR and four others) where the reference wraps none; inherent to 17 pt on a four-column axis and accepted by the spec.

**FILM-FIRST won the panel (121 aggregate):** the reference's structure executed in this film's own light. Not a NightFeeds template with different names.

### The card now

| Page | What it is | Reference page |
|---|---|---|
| CREDITS | key creatives stacked left over the hero still, then CAST with the lead at 30 pt | p9 |
| CREW | four columns (two role-name pairs), no department headings, groups separated by one blank pitch, 48 pt margins | p10 |
| THANKS | extras (3 col) · thanks (3 col) · PARTNER LOGOS slot · Avid line · three AFI paragraphs · fellows (2 col) · copyright · AFI CONSERVATORY LOGO slot | p11 |

One face, one weight, one colour: **Baskerville Bold, cream `#efe6d6`**, all caps, on a **full-bleed still per page** (`GROUND_RECIPE`: CREDITS still 1.1.29 at alpha 1.0 anchored 0.20; CREW 1.1.27 at 0.60; THANKS 1.1.25 at 0.45 anchored 0.70). No scrim, no gradient. Text selectable on every page — the reference's are rasterised, and `press/epk-spec.md` names that as the thing to do better.

Measured, not eyeballed: legibility gate p1 28 / p2 62 / p3 50 against limits 60 / 65 / 75; zero spans outside the per-page margins; zero overlapping spans; every one of seven UI words searchable; 4,089 selectable characters.

**Sizes:** `--medium` (1.3x, 9 pages) and `--large` (1.75x, 12 pages) still stack role over name and still build clean; a few enlarged pages run under-filled (medium p7 at 45 %, large p3 at 54 %). Known, acceptable until Luke picks a size.

### The two-rooms contract, honoured

Two other tools import this file. `tools/build-epk-kit.py` draws EPK pages 9–11 through it; `tools/build-epk-ai.py` replays it into Illustrator. The rewrite kept every name and signature they call, kept `tracked()`/`c.line`/`ground()` as the only primitives, forbade gradients (stacked alpha rects instead), draws the still as a cover crop into the full page box, sets `.path`/`.region`/`._kom_path` on the image, and publishes `GROUND_RECIPE`. The kit was run as a check with `--out` to scratch twice and completed both times; no dated release file was created in `press/`. **One line of the peer's file was touched by the builder:** `"Bask-B": "Baskerville-Bold"` added to the FONT map of `tools/build-epk-ai.py`, without which its replay raises KeyError on the new face. Left unstaged; handed to the peer.

### Branding Bible: contradictions introduced, on purpose

`BRAND.md` v0.1 DRAFT (unratified) was sampled from the OLD card before Luke's redirect. The new card contradicts these DEFINED rows and I did **not** edit the Bible — the list goes to the peer session, which owns it, to append as PROPOSED with the affected rows flipped to CONTESTED: **(a)** type weight is Bold (index 1), which BRAND forbids, and SemiBold is no longer drawn; **(b)** role labels are CREAM, not DIM; **(c)** department headings are off by default; **(d)** the ghost recipe (still at 16–22 % under a 50–55 % scrim) is replaced by a full-strength still with no scrim; **(e)** titles are single words CREDITS / CREW at 60 / 56 pt tracked 2.0 with no rule, not spaced `C A S T` at 40 pt with the 236 pt rule; **(f)** sizes step up throughout (names 26, lead 30, crew 17, boilerplate 20); **(g)** CREW margins 48 against the 74 pt page geometry; **(h)** the tracking table replaces the scaled 6.0 / 1.35 / 0.95.

**The design question this raises is Luke's, and the peer is putting it to him too:** pages 1–8 of the EPK are cream Baskerville Regular on near-black; pages 9–11 are now bold on full-bleed picture. Either the whole kit follows the redirect or the credit pages stand apart.

### Where everything is

- `press/KillerOfMen_Credits{,_medium,_large}{,_transparent}.pdf` — six PDFs, 0.03–0.3 MB each (the backdrops are page-shaped JPEG crops now)
- `press/assets/CREDITS/` — 24 transparent PNGs at 200 dpi (opaque renders are on the Drive only, 40 MB)
- `press/illustrator/*.ai` — three files, live Baskerville Bold text, locked BACKGROUND layer, verified from inside Illustrator (244 / 249 / 251 frames). Gitignored; on the Drive
- `press/credit-redesign/` — gitignored: it holds another film's rendered pages
- Drive: `00 PRESS / EPK BUILDS` (PDFs, opaque renders) and `00 PRESS / Illustrator Projects` (.ai)

Unchanged and still open: no sound designer named; Jordan Uwhubetine vs Jordan Betine (the card prints both, as the data does); © MMXXV against a 2026 completion; no logo files (two labelled slots).

---

**Timestamp:** 2026-09-10
**Lane:** `epk`
**Continues:** handoff-104-epk.md
**Model:** Fable 5.1, orchestrating.

## Next action (the one thing)

**Luke: does the whole kit follow the guide, or only the credit pages?** Everything else waits on that: the Bible amendment, whether pages 1–8 get the same treatment, and which card size to keep. Then Jordan on the sound designer and his name.

## Files

- The card: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_Credits.pdf
- The tool: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-credit-card.py
- Transparent PNGs: https://github.com/Scroggdawg/kom-festival-board/tree/main/press/assets/CREDITS
- Illustrator files on the Drive: https://drive.google.com/drive/folders/1Ii4lF5yfhSZBIxWafFALb7aJR4d3sTk_
- PDFs and opaque renders on the Drive: https://drive.google.com/drive/folders/1utGEFQb5gDuUOC9JU7zvuslwRlwbRorx
- The Branding Bible this contradicts: https://github.com/Scroggdawg/kom-festival-board/blob/main/BRAND.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-104-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-105-epk.md
