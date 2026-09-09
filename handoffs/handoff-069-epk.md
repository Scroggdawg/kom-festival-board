# handoff-069-epk

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** Luke re-exported the stills as one folder, saying he had added the earlier ones so every base was covered, and asked for the repo set replaced. Done and pushed. **`press/epk.json` rev 6 · 16 of 49 filled, 1 undecided.**

**`press/assets/STILLS/` is now one flat set**, 41 PNGs from Resolve export `210640`, 1920×1080 letterboxed, picture in rows 138–941 (2.39:1), gallery names kept. Contact sheet rebuilt as `contact-sheet.jpg`. All 41 checked byte for byte against the source folder. The two subfolders from handoff-068 (`set-2025-12-18`, `set-2026-09-08`) were removed in the same commit.

**Coverage was verified before anything was deleted**, by comparing every old frame's picture area against all 41 new ones:

| Old set | Covered |
|---|---|
| 33 letterboxed (Sep 8, export 190811) | 33 of 33 |
| 10 scope (Dec 18, 2048×858) | 8 of 10 |

**Two December frames did not survive the swap**, and Luke should know which:

- **old `1.1.9`** — the warm barn close-up of Mace, shirtless, head lowered, lamp behind him. This is the only *shot* absent from the new export. Nothing in the 41 is it: `1.1.34` is the grapple, `1.1.35` the wheel of fire, `1.1.37` the priest in yellow.
- **old `1.1.4`** — Mace in profile at the cabin. The shot is here as `1.1.16` and `1.1.17`; the exact frame is not.

Neither is lost. Both sit in `FINAL/KOM Stills` on Luke's machine and in this repo at `eb9e75f`. The README carries the restore command. **I did not re-add them**, because the instruction was to remove the old set, and quietly keeping half of it back would make the folder disagree with what Luke thinks is in it.

**Also true and worth one line:** the December set was full-frame 2048×858 with no bars. Every frame in the repo now carries black bars, top and bottom, about 137 px each. For a programmer's page or a poster crop that is fine, but anyone laying a still into a layout will be cropping the bars off by hand. If Yeo can export a no-bar set, that is a better master; the December set proves Resolve can do it.

**One duplicate inside the new export:** `1.1.25` and `1.1.26` are the same frame. Both kept, noted in A.1 and the README.

**Repo weight** is unchanged in practice, 244 MB against 247 MB, because the swap traded 43 files for 41. Git keeps both, so a fresh clone now carries roughly half a gigabyte of stills history. Still inside GitHub's limits, and still not worth a history rewrite; the fix, if it ever bites, is a web-size JPG set with PNG masters on Drive.

---

**Timestamp:** 2026-09-08
**Lane:** `epk`
**Continues:** handoff-068-epk.md
**Model:** Opus 5. Goose turn: verify coverage, swap, publish.

## Next action (the one thing)

**Pick the stills** from `contact-sheet.jpg`: hero (2.3), behind the statement (4.2), each principal in character (7.2), behind the credits (9.3), best 12 for the Drive. Then the end-credit roll, unchanged since handoff-067. Open question for Yeo, cheap to ask alongside the specs: a no-bar still export.

## Files

- Stills: https://github.com/Scroggdawg/kom-festival-board/tree/main/press/assets/STILLS
- Contact sheet: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/assets/STILLS/contact-sheet.jpg
- Assets index, with the restore command: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/assets/README.md
- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/EPK-breakdown.pdf
- Superseded stills commit: https://github.com/Scroggdawg/kom-festival-board/commit/eb9e75f
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-068-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-069-epk.md
