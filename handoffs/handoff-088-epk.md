# handoff-088-epk

## Where we left off

**This turn (Sep 9, 2026, Opus 5):** Luke sent four crew headshots. **They are on the Drive and in the git repo**, full resolution, and `5.6` is written.

Numbered **088**, and **this handoff was pushed before the work commit** — the fix proposed in handoff-084 after that session and this one both claimed 083. The push either wins the number or bounces cheaply. It is a one-line change of habit, not a change to the README rule, and it worked.

### The headshots

Four files, from the project's own `Headshots/Edits/` folder, shot September 2024:

```
KOM Headshots v3-1.jpg   6200 × 7134   7.3 MB
KOM Headshots v3-2.jpg   6200 × 7033   5.3 MB
KOM Headshots v3-3.jpg   6200 × 6713   4.7 MB
KOM Headshots v3-4.jpg   6200 × 6372   5.3 MB
```

**In two places, both verified byte-identical with `cmp` after copying:**

- **Drive** — `KILLER OF MEN / 05 MARKETING / 00 PRESS / HEADSHOTS`, which had been empty since the tree was built
- **Git repo** — `press/assets/HEADSHOTS/`, 22 MB

**Nothing was resized, cropped or re-encoded.** They are 6200 pixels wide as delivered. The standing rule from handoff-071 holds: assets go in as they are, and any change is asked about first.

They match the film's look — hard side light, deep falloff, sepia-black. They will sit correctly against pages 5 and 6.

### Two things not done, on purpose

**1. The files are not renamed.** `press/epk-spec.md` wants `KILLER_OF_MEN_First_Last_Role.jpg`, and these are numbered `v3-1` through `v3-4`. Renaming means deciding which file is which person, and **I am not guessing that.** Putting the wrong name on someone's headshot in a press kit is not a mistake you find before a programmer does. Luke maps file number to person in one line and the rename takes a second.

**2. There are four headshots and five credited fellows.** Ruoxiao Li, Rajarajeshwari Ragampudi, Luke Scroggins, Jordan Betine and You Wu all carry a bio slot at `5.1`–`5.5`. Four files cannot cover five people. Either one fellow's headshot has not been taken, or it exists somewhere this folder does not reach. Worth checking before the kit is laid out, because a bio page with no portrait is the thing that looks unfinished.

The older sets are still in the project folder and were not touched: `Headshots/Edits/` also holds a v2 and a five-file v1, and `Headshots/CCD Headshots/` holds four larger v3 files, up to 28 MB, that may be the same four people at a higher grade. Worth a look if print resolution is ever wanted.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-087-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Luke: which file is which person, and who is the fifth?** That renames the four to the spec convention and shows whether a headshot is missing. Still open from 087 and 084: Betine or Uwhubetine, who designed the sound, the press contact at `3.17`, and whether "RE-RAW" is ARRIRAW.

## Files

- Headshots in the repo: https://github.com/Scroggdawg/kom-festival-board/tree/main/press/assets/HEADSHOTS
- Headshots on the Drive: https://drive.google.com/drive/folders/1utGEFQb5gDuUOC9JU7zvuslwRlwbRorx
- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Naming convention: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk-spec.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-087-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-088-epk.md
