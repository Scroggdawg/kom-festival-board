# press/assets

Delivered EPK materials, named to the Drive and delivery skeletons in `press/epk-spec.md`. Film files are byte-identical to what arrived, except the BTS set, which is resized for the reason given below. Contact sheets are derivatives, marked as such.

| File | What | Source | Arrived |
|---|---|---|---|
| `POSTER/KillerOfMen_Poster_2160x2700.jpg` | Key art, 2160×2700 JPG, 5.7 MB, billing block on the image | Jordan's Drive, as `edit kom fin (1).JPG` | 2026-09-08 |
| `SRT/KillerOfMen_English.srt` | English SDH captions, 214 cues, hour-one timecode | Drive folder `KOM Caption`, Dec 2025 | 2026-09-08 |
| `SRT/KillerOfMen_English.scc` | Same captions, Scenarist SCC (broadcast) | Drive folder `KOM Caption`, Dec 2025 | 2026-09-08 |
| `STILLS/Still 2026-09-08 210640_1.1.N.png` | 41 frame grabs, PNG 1920×1080 letterboxed, picture in rows 138–941 (2.39:1). `1.1.25` and `1.1.26` are the same frame | `FINAL/KOM Stills (Additional)`, Resolve export 210640 | 2026-09-08 |
| `BTS/*.jpg` | 102 behind-the-scenes photographs, long edge 2560, original filenames. **Resized** from the camera originals | `FINAL/BTS Selects` | 2026-09-08 |
| `STILLS/contact-sheet.jpg`, `BTS/contact-sheet.jpg` | Every frame, numbered or named. **Derivatives**, for choosing | built from the sets | 2026-09-08 |

Resolve gallery names and camera filenames are kept, because they are how a frame is found again in the project.

## Why the BTS photographs are not the camera originals

The originals are 714 MB across 102 files, up to 53 MB each. This repository also publishes the campaign board through GitHub Pages, and **a published Pages site may be no larger than 1 GB**. The repository is about 121 MB today. Adding the originals would take it to roughly 835 MB, leaving no room for the headshots and trailer still to come, and the first delivery that crossed the line would stop the live board from building.

So the repository carries all 102 photographs at long edge 2560, JPEG quality 86, which is 48 MB and comfortably larger than page 8 of the EPK needs. **Nothing was dropped from the selection**; only the pixel dimensions changed. The camera originals stay on Luke's disk at `FINAL/BTS Selects` and belong in the Drive folder that `press/epk-spec.md` already plans for, since the EPK is a link hub and full-resolution assets are exactly what it links to.

By shoot day, from the files' own capture dates:

| Count | Prefix | Date | What |
|---|---|---|---|
| 58 | `KOM_Day3_TheFarm-` | 8 Jul 2025 | The farm and the barn |
| 21 | `KOM_Day4_Soundstage-` | 4 Jul 2025 | The soundstage |
| 6 | `KOM_Stage-` | 23 May 2025 | |
| 5 | `KOM_Anamorphic*` | 21 May 2025 | Anamorphic frames, several black and white |
| 8 | `DSCF*`, `_DSF*` | 21–22 May 2025 | |
| 4 | `IMG_*` | 27 Jun 2025 | |

Four cameras: Sony A7 IV for most of it, Fujifilm X100VI, Fujifilm GFX50S II, Canon EOS R5 C. No GPS data in any file.

**Two things to settle before page 8 is laid out.** No photographer is named in any file, and page 8 needs a credit line. And the May frames predate both July shoot days, so they may be camera and lens tests rather than set photography.

## The stills replaced two earlier sets

The 41-frame export supersedes the 10 scope stills and 33 letterboxed stills committed earlier the same day (`eb9e75f`, still in git history). Coverage was checked frame by frame before the old sets were removed:

- All **33** of the earlier letterboxed stills appear in this export.
- **8 of 10** of the December scope stills appear in it.
- **Two December frames are not in it.** The old `1.1.9`, a warm barn close-up of Mace shirtless with his head lowered, is the only *shot* missing altogether. The old `1.1.4`, Mace in profile at the cabin, is a different moment of a shot that is here as `1.1.16` and `1.1.17`.

Both are still on Luke's disk in `FINAL/KOM Stills`, and both are in this repository's history. Restore either with `git checkout eb9e75f -- 'press/assets/STILLS/set-2025-12-18'`.

Left out on purpose: the `.drx` files that came with an earlier stills export. They are Resolve grade sidecars, not press material.

Still to arrive: headshots, trailer, laurels (see `press/epk.json`, fields 5.6, A.2, A.3). Still to choose: the hero still (2.3), the photo behind the statement (4.2), stills in character (7.2), the still behind the credits (9.3), the best 12 stills for the Drive, and 8–12 BTS photographs for page 8.
