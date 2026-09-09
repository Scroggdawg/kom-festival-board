# handoff-072-epk

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** Luke asked for a watch folder — one tree that lives on Google Drive and on this Mac at once, holding BTS, stills, trailer, everything, with Google Docs in it for the bios. **Built.** `press/epk.json` rev 9 · 18 of 49 filled. `A.4`, open since the inventory, is closed.

### Drive for Desktop was already running

Mounted at `~/Library/CloudStorage/GoogleDrive-camerawrap@gmail.com`, symlinked to `~/Google Drive`, account `camerawrap@gmail.com`. `~/BMF Headquarters` is **not** mirrored — it is a plain local folder. So the watch folder had to be created inside the Drive mount, which is what was done. Anything dropped on either side now appears on the other.

### The tree, built to `press/epk-spec.md`

```
~/Google Drive/My Drive/KILLER OF MEN/          965 MB · 151 files
  05 MARKETING/
    00 PRESS/
      BTS/         102 camera originals + contact sheet    715 MB
      STILLS/       41 Resolve PNGs + contact sheet         244 MB
      POSTER/       the 2160x2700 key art                   5.4 MB
      SRT/          English srt + scc                        52 KB
      HEADSHOTS/   empty — one per person
      TRAILER/     empty — Yeo
      LAURELS/     empty — email the three festivals
      EPK BUILDS/  the breakdown PDF
      z_Old_EPKs/
      EPK INFO — all the text          (Google Doc)
      EPK LINKS — every share URL      (Google Doc)
    07 FESTIVALS/  accepted · cover letters · details · laurels · social · receipts · IG
  DELIVERY/
```

Every file copied was verified byte-identical with `cmp` — 41 stills, 102 BTS, the poster, both caption files. **Nothing was resized, converted or re-encoded.** Confirmed present on Drive through the API afterwards, at full byte size.

- Root: <https://drive.google.com/drive/folders/1OUOykJpMq5o91PkZ54qvMpoVJgKpDPx7>
- Press: <https://drive.google.com/drive/folders/1utGEFQb5gDuUOC9JU7zvuslwRlwbRorx>

### The two Google Docs

**EPK INFO** carries all 49 fields — logline in both versions, the director's statement in full, credits, cast, specs — with every gap printed as `NEEDED` and who owns it. It is **generated** from `press/epk.json` by the new `tools/build-epk-info.py`. `epk.json` stays the master; regenerate and repaste rather than treating the doc as source. This is the doc the team writes bios into.

**EPK LINKS** holds every share URL, including AFI's tree, with a standing note on what is empty.

### What the Drive survey turned up — this is the real finding

There is an **AFI-owned production tree** shared with Luke: `2513 Killer Of Men`, owned by `asigel@afi.com`, with `6) Post-Production Docs / Delivery` underneath it. The BTS folder Luke linked sits inside it.

**Four of its delivery folders are empty**, checked through the API on Sep 8: **Trailers, FEST, Poster Blu-Ray, Closed Captions.** They were created as a template in June 2024 and never filled. That is why the trailer, the poster and the captions have been scattered across Jordan's, Ruoxiao's and Luke's personal folders instead of sitting in delivery. Do not point a festival at them.

Also found: `Delivery/BTS/BTS KOM`, owned by **Ruoxiao Li**, holds the *full* BTS set — more anamorphic and stage frames than the 102 selects, plus a `jordan photos` subfolder and large Sony frames from Jordan. Worth a look before page 8 is chosen from the selects alone.

### On the repository

The 965 MB now lives on Drive as well as in git. The repo still carries its copy and still builds Pages. **Moving the assets out of the repo is not done and is Luke's call** — it would take the repo back under 150 MB and give Pages room again, at the cost of the GitHub links in the worksheet needing to become Drive links. The `EPK LINKS` doc is already the place those links would live.

---

**Timestamp:** 2026-09-08
**Lane:** `epk`
**Continues:** handoff-071-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Look in `Delivery/BTS/BTS KOM`** — Ruoxiao's full BTS set, which has frames the 102 selects do not, before page 8 gets picked. Then: pick the pictures, ask the photographer's name, and the end-credit roll. Standing decision for Luke: whether to drop the assets from the git repo now that Drive holds them.

## Files

- Drive root: https://drive.google.com/drive/folders/1OUOykJpMq5o91PkZ54qvMpoVJgKpDPx7
- Press folder: https://drive.google.com/drive/folders/1utGEFQb5gDuUOC9JU7zvuslwRlwbRorx
- EPK INFO: https://docs.google.com/document/d/1ae-MPbAq1otTtYA5-SSYYGd13jjvuz1Co2Zi0IrGvSI/edit
- EPK LINKS: https://docs.google.com/document/d/16x38uawE0Iq91JCj3AC7cVV7SnpCO7kNdBJ0Dj8vUKg/edit
- AFI Delivery (theirs): https://drive.google.com/drive/folders/1AyMfvwEesioGba1_wztrKfpXpIUmi2FH
- Ruoxiao's full BTS: https://drive.google.com/drive/folders/1L5A4FAc8H6fCJF9LqF8gYjTZSw4Qpd4Z
- The worksheet: https://scroggdawg.github.io/kom-festival-board/epk.html
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-071-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-072-epk.md
