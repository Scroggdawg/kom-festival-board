# press/assets

Delivered EPK materials, named to the Drive and delivery skeletons in `press/epk-spec.md`. Every film file is byte-identical to what arrived. Contact sheets are derivatives, marked as such.

| File | What | Source | Arrived |
|---|---|---|---|
| `POSTER/KillerOfMen_Poster_2160x2700.jpg` | Key art, 2160×2700 JPG, 5.7 MB, billing block on the image | Jordan's Drive, as `edit kom fin (1).JPG` | 2026-09-08 |
| `SRT/KillerOfMen_English.srt` | English SDH captions, 214 cues, hour-one timecode | Drive folder `KOM Caption`, Dec 2025 | 2026-09-08 |
| `SRT/KillerOfMen_English.scc` | Same captions, Scenarist SCC (broadcast) | Drive folder `KOM Caption`, Dec 2025 | 2026-09-08 |
| `STILLS/Still 2026-09-08 210640_1.1.N.png` | 41 frame grabs, PNG 1920×1080 letterboxed, picture in rows 138–941 (2.39:1). `1.1.25` and `1.1.26` are the same frame | `FINAL/KOM Stills (Additional)`, Resolve export 210640 | 2026-09-08 |
| `BTS/*.jpg`, `BTS/*.JPG` | 102 behind-the-scenes photographs, camera originals, unmodified, 714 MB | `FINAL/BTS Selects`, same files as the shared Drive folder | 2026-09-08 |
| `STILLS/contact-sheet.jpg`, `BTS/contact-sheet.jpg` | Every frame, numbered or named. **Derivatives**, for choosing | built from the sets | 2026-09-08 |

Resolve gallery names and camera filenames are kept, because they are how a frame is found again in the project.

## Where these files also live

Everything here is also in a Google Drive folder that syncs to Luke's Mac through Drive
for Desktop, so it is on the Drive and on the machine at the same time. That folder, not
this repository, is the home for the full-resolution assets, and the EPK links out to it.

- Project root — <https://drive.google.com/drive/folders/1OUOykJpMq5o91PkZ54qvMpoVJgKpDPx7>
- Press folder — <https://drive.google.com/drive/folders/1utGEFQb5gDuUOC9JU7zvuslwRlwbRorx>
- `EPK INFO` and `EPK LINKS` are Google Docs inside it. `EPK INFO` is generated from
  `press/epk.json` by `tools/build-epk-info.py`; `epk.json` stays the master.

Separate from ours, and not ours to reorganise: AFI's own Delivery tree, owned by
`asigel@afi.com`. Its Trailers, FEST, Poster Blu-Ray and Closed Captions folders were
checked on 8 September 2026 and are all empty.

## The BTS photographs are the camera originals

All 102 as shot, 714 MB, largest file 53 MB. They match the shared Drive folder file for file.

**This repository is now around 835 MB, and a published GitHub Pages site may be no larger than 1 GB.** The live board at `scroggdawg.github.io/kom-festival-board` builds from this repository, so the headshots and trailer still to come have roughly 165 MB of room between them. When that runs out, the move is to serve the masters from Drive and link to them, which is what `press/epk-spec.md` already describes: the EPK is a link hub. Nothing here is resized, and nothing here will be resized without asking first.

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
