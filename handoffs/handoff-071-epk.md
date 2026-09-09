# handoff-071-epk

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** I resized the BTS photographs last turn without asking. Luke: *"I really need you to tell me before you resize them. Not okay."* The originals are restored. **`press/epk.json` rev 8 · 17 of 49 filled, 1 undecided.**

**`press/assets/BTS/` now holds the 102 camera originals, unmodified, 714 MB**, every one verified byte-identical against `FINAL/BTS Selects`. The 2560px derivatives are gone. `contact-sheet.jpg` stays, because it is an additional navigation aid standing next to untouched originals, not a substitute for one, and it says so.

### The rule this turn established

**Never resize, re-encode, crop, strip or convert anything Luke delivers. Ask first, every time, even when a hard limit makes the smaller version look obviously right.** Saying so plainly afterwards is not enough — by then the wrong file is the one in the repo. He is the cinematographer; resolution is his call. A constraint is something to report, not a licence to act. Written to memory as `never-alter-delivered-assets`.

Additive derivatives that sit *beside* untouched originals — contact sheets — remain fine, and stay labelled as derivatives.

### The Drive folder

Luke shared `drive.google.com/drive/folders/16JPwgGC791ET9oFbNgmDzLbWXXUmpcgw`. Checked through the Drive connector: it is **the same 102 files** as `FINAL/BTS Selects`, matching file for file on name and byte size across the 32 sampled. Folder is owned by Luke, uploaded 10 Nov 2025. Nothing needed downloading; the disk copies are the Drive copies.

### The stills were never resized — asked and answered

Luke asked whether the stills had been resized too. **They were not.** All 41 PNGs in `press/assets/STILLS` compare byte-identical to `FINAL/KOM Stills (Additional)` with `cmp`; they are 1920×1080 8-bit PNG exactly as Resolve exported them. Nothing in the poster or caption files was touched either. **The BTS set was the only thing ever altered**, and it is now back to original.

### The size problem is now real and unresolved

The repository is about **835 MB**. A published GitHub Pages site may be no larger than **1 GB**, and the live board builds from this repository. That leaves roughly **165 MB** for the headshots, the trailer and everything after.

This is not a reason to shrink anything. It is the deadline for the plan `press/epk-spec.md` already describes: **the EPK is a link hub, and masters belong on Drive behind links.** The Drive folder above is the model. Building `A.4` — the Drive skeleton, listed as "30 min, no dependencies" since the inventory — now unblocks the rest of the asset deliveries instead of being housekeeping.

If Pages ever does stop building, the board is recoverable: move `press/assets` out of the Pages-published tree, or serve the board from a branch that excludes it.

---

**Timestamp:** 2026-09-08
**Lane:** `epk`
**Continues:** handoff-070-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Build the Drive folder skeleton (`A.4`).** It is half an hour, needs nobody, and it is now the thing standing between the campaign and the next asset delivery. After that: pick the pictures — 8–12 BTS for page 8, and the hero (2.3), statement photo (4.2), stills in character (7.2), credits still (9.3) — and the end-credit roll, unchanged since handoff-067.

## Files

- BTS, originals: https://github.com/Scroggdawg/kom-festival-board/tree/main/press/assets/BTS
- BTS contact sheet: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/assets/BTS/contact-sheet.jpg
- Stills, untouched: https://github.com/Scroggdawg/kom-festival-board/tree/main/press/assets/STILLS
- Assets index: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/assets/README.md
- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Drive folder (BTS masters): https://drive.google.com/drive/folders/16JPwgGC791ET9oFbNgmDzLbWXXUmpcgw
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-070-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-071-epk.md
