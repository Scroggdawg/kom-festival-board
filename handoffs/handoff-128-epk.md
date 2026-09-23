# handoff-128-epk

## Where we left off, newest first

1. **The send-ready folder exists (2026-09-23).** `05 MARKETING/00 PRESS/EPK-2026-09-23/` on the Drive: 44 files, 149 MB, all copies, nothing moved or deleted from the source folders. `00 READ ME.md` inside lists every file with its MD5 and the table of what is still owed and by whom. Kit PDF `KillerOfMen_EPK_1625_23092026_compressed.pdf` (11 pages, 20 links, page text identical to the 21 Sep build); poster; twelve stills under programmer names with the gallery number kept in the file name; the ten page-8 photographs; five headshots as `KILLER_OF_MEN_First_Last_Role.jpg`; six laurels; SRT and SCC; the AFI wordmark; all the kit text as one `.txt`; FilmFreeway v7 as `.md` and `.docx`; the status one-sheet.

2. **Worksheet rev 40, 45 of 48 fields filled** (`press/epk.json`, through `epk.py set`, checker clean). New: A.3 laurels (three festivals, black and white versions, arrived on the Drive 23 Sep 11:43 to 11:47; the AFI Fest 2022 laurel in the same folder is generic and not used); 7.2 stills in character (one primary and one alternate for Mace, Kenner, Kojo, the Elder; Fred, Kojo's Master and Girl not identified in the frames); A.1 the twelve press stills and the four page picks the kit already draws; 8.1 the ten page-8 photographs; 3.12 what the files on hand show (a 1080p H.264 stereo Vimeo master dated 8 Dec 2025; a DCP of unconfirmed date), still owed by You Wu. Empty: A.2 trailer (You Wu), A.5 60-second intro (Jordan), 11.2 partner logos (nobody named).

3. **Three views are generated from the worksheet now, not hand-written.** `tools/build-epk-one-sheet.py` writes `press/epk-one-sheet.md` (replaces the 8 Sep sheet, which described 47 fields); `tools/build-filmfreeway-page.py --version 7` writes `press/filmfreeway-page-v7.md` and `.docx` (v6 was the last hand-written draft; v7 carries 2.1 as filled, with the three alternates named, 2.2, 5.1, 4.1 as Jordan supplied it, the specs, credits, cast, screenings, the twelve stills, the attachments); `tools/build-epk-info.py` output is kept as `press/epk-info.txt`. `epk.html` needs no regeneration: it reads `press/epk.json` from `main` through the GitHub API, so it shows rev 40 once this branch is merged.

4. **One builder bug found and fixed.** The 16:22 build printed the whole of 3.12 in capitals on page 3 (the builder printed the field verbatim). `tools/build-epk-kit.py` now prints 3.12's first line only, and not while it begins PARTIAL. The 16:22 PDF went to `z_Old_EPKs`; 16:25 is the build in the package and in `EPK BUILDS`.

5. **Ledgers reconciled, additively.** The repo's `handoffs/` and the Drive's `HANDOFFS/` now hold the same 165 files. Into the repo: 104-festival and 105-festival (Drive only), and 082-festival, 083-connectors, 084-bio (sitting untracked in the `main` checkout at `$HOME/Code/kom-festival-board`, which is at 9ba0bca while `origin/main` is at 785ddf0, handoff-127). Onto the Drive: 100-epk, 102-epk, 106-epk, 109-epk, 109-festival and the same three. Numbers 082 to 084 exist twice with different lane suffixes (epk and festival/connectors/bio); the files do not collide and neither was renamed. Next number across both: 129.

## What the kit is still missing, and who supplies it

| Item | Who | Field |
|---|---|---|
| Trailer file | You Wu | A.2 |
| Exhibition formats: 2K/4K DCP, ProRes masters, whether the DCP is the current cut | You Wu | 3.12 |
| Jordan's 60-second introduction | Jordan Betine | A.5 |
| Sandra McDaniels's own bio (hers is the only draft left) | Sandra McDaniels or NTA Talent Agency | 7.1 |
| Sound designer and the post-sound credits | Jordan Betine | 9.1 |
| Director's name on the fellows list (Betine or Uwhubetine); copyright year MMXXV against completion 2026 | Jordan Betine | 11.3 |
| Logline: the filled text or one of three alternates | Jordan Betine | 2.1 |
| Cinematographer bio: four rewrites recorded, none chosen (handoff-084-bio's interview is at round 1 of 3) | Luke | 5.3 |
| Partner or vendor logos, if any | Jordan Betine | 11.2 |
| Laurels laid on the poster and trailer | Luke (Jordan holds the poster source) | A.3 |
| Names in frames 1.1.31 to 1.1.37 | Luke or Jordan | 7.2 |
| Canva export of the design (the kit's other form) | Luke's click: Share › Download › PDF Print · RGB · all pages · crop marks off · Flatten off, then `tools/check-canva-export.py` | — |

## Not done, on purpose

- The Canva design was not touched and not exported (the download is Luke's click). The package carries the reportlab kit, whose page text matches the 21 Sep build.
- No laurels were placed on any page or on the poster; that is a design change for Luke to rule on.
- The EPK INFO Google Doc was not edited; `press/epk-info.txt` is the text to paste when he wants it refreshed.
- `main` was not pushed. This branch is `claude/vigorous-mayer-7773b9`, published with `git push -u origin HEAD`; Luke merges.

## Next action

Send You Wu the message in `press/messages-to-send.md` (six specs, the trailer, the DCP); it clears 3.12 and A.2, the two fields a programmer reads first. Then Jordan's one message (logline pick, fellows-list name, copyright year, sound designer, the intro).

---

**Timestamp:** 2026-09-23 16:30 PDT · **Lane:** `epk` · **Continues:** handoff-127-epk.md (and handoff-084-bio.md for 5.3) · **Model:** Fable 5.1 (goose turn: the brief in handoff-587-kom, executed; the readout widget was the only design work).

## Files

- The send-ready folder: file:///Users/scroggdawg/Library/CloudStorage/GoogleDrive-camerawrap%40gmail.com/My%20Drive/KILLER%20OF%20MEN/05%20MARKETING/00%20PRESS/EPK-2026-09-23/
- Its README: file:///Users/scroggdawg/Library/CloudStorage/GoogleDrive-camerawrap%40gmail.com/My%20Drive/KILLER%20OF%20MEN/05%20MARKETING/00%20PRESS/EPK-2026-09-23/00%20READ%20ME.md
- Kit PDF: https://github.com/Scroggdawg/kom-festival-board/blob/claude/vigorous-mayer-7773b9/press/KillerOfMen_EPK_1625_23092026_compressed.pdf
- Worksheet: https://github.com/Scroggdawg/kom-festival-board/blob/claude/vigorous-mayer-7773b9/press/epk.json
- One-sheet: https://github.com/Scroggdawg/kom-festival-board/blob/claude/vigorous-mayer-7773b9/press/epk-one-sheet.md
- FilmFreeway v7: https://github.com/Scroggdawg/kom-festival-board/blob/claude/vigorous-mayer-7773b9/press/filmfreeway-page-v7.md
- Laurels: https://github.com/Scroggdawg/kom-festival-board/tree/claude/vigorous-mayer-7773b9/press/assets/LAURELS
- Harness: https://github.com/Scroggdawg/kom-festival-board/blob/claude/vigorous-mayer-7773b9/handoffs/HARNESS-epk.md
- Prior handoffs: https://github.com/Scroggdawg/kom-festival-board/blob/claude/vigorous-mayer-7773b9/handoffs/handoff-127-epk.md · https://github.com/Scroggdawg/kom-festival-board/blob/claude/vigorous-mayer-7773b9/handoffs/handoff-084-bio.md
- Readout thumbnails (derivatives, 222 KB, for the widget only): https://github.com/Scroggdawg/kom-festival-board/tree/claude/vigorous-mayer-7773b9/press/assets/derived/readout-2026-09-23
- This handoff: file:///Users/scroggdawg/Code/kom-festival-board/.claude/worktrees/frosty-moore-f514b1/handoffs/handoff-128-epk.md
