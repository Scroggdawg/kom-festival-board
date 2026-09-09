# press/assets

Delivered EPK materials, named to the Drive and delivery skeletons in `press/epk-spec.md`. Every film file is byte-identical to what arrived. The only derivative is the contact sheet, marked below.

| File | What | Source | Arrived |
|---|---|---|---|
| `POSTER/KillerOfMen_Poster_2160x2700.jpg` | Key art, 2160×2700 JPG, 5.7 MB, billing block on the image | Jordan's Drive, as `edit kom fin (1).JPG` | 2026-09-08 |
| `SRT/KillerOfMen_English.srt` | English SDH captions, 214 cues, hour-one timecode | Drive folder `KOM Caption`, Dec 2025 | 2026-09-08 |
| `SRT/KillerOfMen_English.scc` | Same captions, Scenarist SCC (broadcast) | Drive folder `KOM Caption`, Dec 2025 | 2026-09-08 |
| `STILLS/Still 2026-09-08 210640_1.1.N.png` | 41 frame grabs, PNG 1920×1080 letterboxed, picture in rows 138–941 (2.39:1). `1.1.25` and `1.1.26` are the same frame | `FINAL/KOM Stills (Additional)`, Resolve export 210640 | 2026-09-08 |
| `STILLS/contact-sheet.jpg` | All 41, numbered by gallery index. **Derivative**, for choosing | built from the set | 2026-09-08 |

Resolve gallery names are kept, because `1.1.N` is how a frame is found again in the project.

## The stills replaced two earlier sets

This one export supersedes the 10 scope stills and 33 letterboxed stills committed earlier the same day (`eb9e75f`, still in git history). Coverage was checked frame by frame before the old sets were removed:

- All **33** of the earlier letterboxed stills appear in this export.
- **8 of 10** of the December scope stills appear in it.
- **Two December frames are not in it.** The old `1.1.9`, a warm barn close-up of Mace shirtless with his head lowered, is the only *shot* missing altogether. The old `1.1.4`, Mace in profile at the cabin, is a different moment of a shot that is here as `1.1.16` and `1.1.17`.

Both are still on Luke's disk in `FINAL/KOM Stills`, and both are in this repository's history. Restore either with `git checkout eb9e75f -- 'press/assets/STILLS/set-2025-12-18'`.

Left out on purpose: the `.drx` files that came with an earlier export. They are Resolve grade sidecars, not press material.

Still to arrive: BTS, headshots, trailer, laurels (see `press/epk.json`, fields 5.6, 8.1, A.2, A.3). Still to choose from the stills: 2.3, 4.2, 7.2, 9.3 and the best 12 for the Drive.
