# handoff-100-epk

## Where we left off

**This turn (Sep 9, 2026, Fable 5.1, a goose run off Luke's one-line brief):** Luke sent the Night Feeds EPK (11 pages, Illustrator) and asked for one like it for Killer of Men, built in Illustrator. **Built: `press/KillerOfMen_EPK_1922_09092026_compressed.pdf`, eleven pages, 4.6 MB**, plus `tools/build-epk-kit.py` that regenerates it. Also on the Drive at `05 MARKETING / 00 PRESS / EPK BUILDS`. `press/epk.json` unchanged at rev 20.

**Not built in Illustrator, and here is why.** Illustrator 2026 on this Mac answers ExtendScript (version 30.8.1, 993 fonts, a two-artboard test document was created) but the plan has lapsed: a "Your Adobe Illustrator plan is out of date, renew to unlock" modal with a US$34.49/month payment form is sitting over the window. That is Luke's to decide and click, not mine. macOS also raised a one-time prompt asking to let the Claude app control other apps; that also needs a click. So the kit was built with the pipeline the lane already trusts, the reportlab one behind the credit card, which does two things Illustrator cannot do natively anyway: every page's text is selectable (11,438 characters extract) and the nine links on page 3 are real link annotations.

### The kit, page by page

| Page | Content | Source | State |
|---|---|---|---|
| 1 | Poster, whole, fitted to width | `1.1` | done |
| 2 | Hero still 1.1.5, logline, synopsis | logline A from `logline-final-three.md`, synopsis C from `synopsis-draft.md` | **DRAFTS**, carries a PROOF slug until 2.1 and 2.2 are filled |
| 3 | Specs, team, cast, rights, five links, footer links | `3.x`, `1.3`, `3.18`, `3.19` | done; all five asset links point at the press folder, not subfolders |
| 4 | Director's statement over ghosted 1.1.10 | `4.1` | text is Jordan's, unsettled per the checklist |
| 5 | Director, producer, cinematographer bios with portraits | `5.1` to `5.3` | **portraits unassigned**, PROOF slug |
| 6 | Production designer, editor bios | `5.4`, `5.5` | editor has no portrait (four files, five people), PROOF slug |
| 7 | Mace still 1.1.40, billed cast | `3.15` | no cast bios exist (`7.1` empty), page shows the list only |
| 8 | Twelve BTS photographs, credit line Jedidiah Woods | `press/assets/BTS` | done |
| 9-11 | Cast, crew, thanks | `build-credit-card.py`, imported | identical to the credit card, with its known holes (sound, Uwhubetine, MMXXV) |

### Three things only Luke can settle, in order of visibility

1. **Which headshot is who.** `PORTRAITS` at the top of the tool maps bio field to file number. It is currently a guess in file order and the pages say so. Set the mapping, flip `PORTRAITS_CONFIRMED = True`, rebuild. One minute.
2. **Logline and synopsis picks.** Jordan owns them per the Sep 9 checklist. Once `epk.py set 2.1` and `2.2` are run, the tool prefers the worksheet and the slug disappears.
3. **Per-subfolder Drive links.** Page 3 has BTS, STILLS, POSTER, TRAILER, HEADSHOTS all going to the press folder. The share URLs live in the EPK LINKS doc, which this session could not read (no Drive token on the machine). Paste them into `LINKS` in the tool.

There is still **no `BRAND.md`**. The kit inherits the credit card's look (Baskerville, cream on near-black) rather than a ratified one.

### Illustrator, if Luke renews

The bridge works: `osascript -e 'tell application id "com.adobe.illustrator" to do javascript (read POSIX file "script.jsx")'`. Note `open -a "Adobe Illustrator 2026"` fails because that path is a folder; the app is inside it. A JSX version of this kit would be a rewrite of the same layout with no hyperlinks, so the recommendation is to keep this tool and open the PDF in Illustrator page by page for hand edits when they are wanted.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-099-epk.md
**Model:** Fable 5.1 (goose; the brief was Luke's one line and the spec in `press/epk-spec.md`).

## Next action (the one thing)

**Luke maps the four headshots to names** in `tools/build-epk-kit.py` and rebuilds. Then the kit is a proof with two draft paragraphs instead of a proof with unassigned faces.

## Files

- The kit: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/KillerOfMen_EPK_1922_09092026_compressed.pdf
- The tool: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-kit.py
- The spec it follows: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk-spec.md
- Logline drafts: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/logline-final-three.md
- Synopsis drafts: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/synopsis-draft.md
- The credit card it imports: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-credit-card.py
- On the Drive: `KILLER OF MEN / 05 MARKETING / 00 PRESS / EPK BUILDS`
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-099-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-100-epk.md
