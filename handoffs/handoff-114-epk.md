# handoff-114-epk

## Where we left off, newest first

1. **Luke reviewed the Canva build and gave five notes (2026-09-11, before a context compact). They are the next work, listed under "After the compact" below, with the plan for each.** Nothing from them has been executed yet.

2. **The kit is built in Canva.** Design `DAHU6a7HKPs` (`https://www.canva.com/design/DAHU6a7HKPs/IoGNd4lGSEhtiq4phlGwCg/edit`), 18 × 24 in, 1728 × 2304 px: eleven pages in order, every element placed, the all-pages read-back reports no wrapped lines. Luke exported it (PDF, Print preset, RGB, Flatten off, crop marks off) to `~/Downloads/Untitled design.pdf`; pymupdf:

    EXPORT Untitled design.pdf 14.5 MB; 11 pages
      p01 1296x1728 pt      0 chars  0 links
      p02 1296x1728 pt    879 chars  0 links
      p03 1296x1728 pt    947 chars  10 links
      p04 1296x1728 pt   2406 chars  0 links
      p05 1296x1728 pt   1714 chars  16 links
      p06 1296x1728 pt   1209 chars  11 links
      p07 1296x1728 pt   2440 chars  0 links
      p08 1296x1728 pt     51 chars  0 links
      p09 1296x1728 pt    557 chars  0 links
      p10 1296x1728 pt   1880 chars  0 links
      p11 1296x1728 pt   1587 chars  0 links
      links total: 37 | fonts: ['LibreBaskerville-Bold', 'LibreBaskerville-Regular']

   The two mailto rows are plain text by design, so 18 live links is the target; the letterspaced titles are not phrase-searchable (the kit's tracking idiom, same in the PDF). Not yet on the Drive, not yet shared (runbook steps 7 to 9 remain).

3. **What the live editor taught, and what changed for it (all committed, `canva/kom-epk-builder/BUILD-REPORT.md` has the table):** the Preview button's fresh design is bypassed by appending its `ui=` parameter to the poster design's URL; 18 × 24 in is 1728 × 2304 px (96 px/in exactly); Libre Baskerville sets wider than Baskerville, so every line box is now generous and anchored on its own alignment edge and each key/value pair is one line with two colour runs; `addPage` lands each new page after the previously added one, so Build all runs 1 to 11 into a blank page (a reverse run came out backwards and was deleted in the grid view); `addPage` rejects more than 100 elements (undocumented), so page 10 (126) is placed element by element onto the selected page ("Place page N on the current page"); `addElementAtPoint` has its own rate limit, so placement is paced 150 ms apart with backoff to 16 s. Luke ratified the ghost recipe at alpha 0.48 under a 0.32 scrim from four rendered strengths (kit, derivatives, Bible amended). Canva's picker also lists ITC New Baskerville (Pro): a real Baskerville in the editor without uploading Apple's file.

4. Earlier today: the taste-pass draft (handoff-113-epk), the Codex audit answered, preflight answered by Luke.

## After the compact: Luke's notes and the plan

**Root cause shared by notes B, C and D:** the Canva contract is laid out with macOS Baskerville metrics; Canva renders Libre Baskerville, which is wider and taller, so paragraphs run more lines than the kit reserved (the statement clips at the foot; cast bios eat the 48 pt gap before the next lockup) and any line placed after a heading sits at a Baskerville-measured x (the handles land on the lockup). **Plan:** lay the Canva contract out with Libre Baskerville's own metrics. Fetch the OFL TTFs (Libre Baskerville Regular, Bold, Italic from github.com/google/fonts, licence file alongside) into `press/assets/derived/fonts/`; give the emitter a `--face libre` mode that registers them as `Bask` (Regular), `Bask-SB` (Bold, the contract's fallback weight) and `Bask-B` (Bold) before the kit's replay, so every fit(), wrap, width and position is computed in the face Canva will draw; the PDF and the .ai keep Baskerville. Then regenerate the contract and derivatives, push, and rebuild the affected pages in Canva (with Libre metrics every text page changes, so: delete all pages in the grid view, Reset progress, Build all ascending into a blank page, Place page 10, delete the blank page, read back, export).

A. **Logline (field 2.1).** Write through the worksheet tool, never by hand:
   `venv/bin/python tools/epk.py set 2.1 "Killer of Men follows Mace, an enslaved man forced into mandingo fights. After killing an opponent, he stumbles upon the burial of the man he killed, igniting a reckoning with guilt, faith, and the violence shaping his life and identity."`
   Page 2 then reads the worksheet's logline; its PROOF slug stays until 2.2 (the synopsis) is chosen too. Rebuild the kit, regenerate the contract.

B. **Director's statement clips off the foot of the page in Canva.** The Libre-metrics plan above; verify page 4's last baseline and signature sit inside the page after the rebuild.

C. **Filmmaker pages: the Instagram handle and IMDB overlap the ROLE | NAME lockup on every block.** Libre-metrics plan. **And Jordan's portrait:** Luke attached the real headshot (studio portrait, sepia, chain necklace, locs; the set photograph Day3-43 was the wrong picture). Get the file: ask Luke for its path or Drive location (check `~/Downloads` for a new image first); it is a master, so it goes to `press/assets/HEADSHOTS/` unmodified and to the Drive HEADSHOTS folder as `KILLER_OF_MEN_Jordan_Betine_Director.jpg`; `PORTRAITS["5.1"]` becomes that headshot number (no grade, no zoom), `DIRECTOR_PORTRAIT_CONFIRMED = True` (the page 5 slug goes), `HEADSHOT_DRIVE` in `tools/build-epk-ai.py` gains the mapping, `press/assets/README.md` and field 5.6 record the fifth master.

D. **Cast page: no space after each bio before the next lockup.** Libre-metrics plan; the kit's 48 pt gap is right, Canva's reflow was consuming it.

E. **Luke's question, "what's the workaround for page 11 with the large number of assets?"** The cap is per `addPage` call: 100 elements. Page 11 (Thanks, 76 elements) built in one call; it was page 10 (CREW, 126) that hit it, and the workaround is in place and documented: the app creates the background-only page, the operator selects it in the editor, and "Place page N on the current page" adds the elements one by one, paced for Canva's element rate limit (126 of 126 on the second pass). Possible refinement, not done: add the first 100 with `addPage` and place only the remainder, halving the per-element time.

F. Then runbook steps 7 to 9: verify the new export, copy it to the Drive under `05 MARKETING / 00 PRESS / EPK BUILDS / CANVA`, rename the design (it is still "Untitled design"), share (edit link to director and producer, view link for press), record in STATE, write the next handoff.

## Blockers and open items

- Jordan's headshot file: needs Luke to say where it is (the chat attachment is not on disk).
- Runbook step 4's PDF-import comparison was skipped (the app route worked first time).
- The one-object-or-two ruling on pages 9 to 11 and the rest of handoff-113's CONFIRM list are still open.

---

**Timestamp:** 2026-09-11 · **Lane:** `epk` · **Continues:** handoff-113-epk.md · **Model:** Fable 5.1 (goose turn: executing the Canva build with Luke at the keyboard).

## Files

- The design: https://www.canva.com/design/DAHU6a7HKPs/IoGNd4lGSEhtiq4phlGwCg/edit
- The export on disk: `~/Downloads/Untitled design.pdf` (not yet in the repo or on the Drive)
- Runbook: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/README.md · STATE: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/STATE.json · live-run findings: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/kom-epk-builder/BUILD-REPORT.md
- The app: https://github.com/Scroggdawg/kom-festival-board/tree/main/canva/kom-epk-builder · the emitter: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-canva.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-113-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-114-epk.md
