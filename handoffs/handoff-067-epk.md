# handoff-067-epk

## Where we left off

**This turn (Sep 8, 2026, Fable 5.1, goose):** Luke pointed at three files in Downloads, poster and captions pulled from Jordan's Drive, and asked that they be put where the EPK keeps them. Done and pushed. **`press/epk.json` rev 4 · 15 of 49 filled, 1 undecided** (was 11).

**New folder `press/assets/`**, named to the Drive and delivery skeletons in `press/epk-spec.md`, with its own README:

```
press/assets/POSTER/KillerOfMen_Poster_2160x2700.jpg   5.7 MB, was "edit kom fin (1).JPG"
press/assets/SRT/KillerOfMen_English.srt               214 cues, hour-one timecode
press/assets/SRT/KillerOfMen_English.scc               same captions, Scenarist SCC
```

All three are byte-identical to what arrived (checked with cmp). The zip Luke downloaded held the SRT plus the SCC; the loose SRT in Downloads was the same file. The fourth file in Downloads, `EPK-breakdown.pdf`, was this repo's own PDF downloaded back, so it was not re-uploaded.

**Fields written, all with provenance in the history entry:**

| Field | What went in | Source |
|---|---|---|
| 1.1 Key art | repo path + GitHub link | the file |
| 1.2 Billing block | transcribed line by line | the poster, read at full resolution |
| 3.7 Subtitle files | English only, SRT + SCC, cue counts, timecode offset | the caption files |
| 3.14 Heads of department | five HoDs, `role \| name` | the poster billing block |
| 9.1 Key credits | eight credits filled, sound designer and EPs left as empty slots | the poster; end credits for the two gaps |

**Two things the poster settled that were open questions:** the producer is **Ruoxiao Li** (5.2 asked "who is the producer?"); and the poster's "STARRING ERIK ORJIAKO" corroborates the spelling Luke gave for 3.15. The poster does **not** name Sandra McDaniels or the Kenner actor, so the end-credit check on those stands.

**Caption facts worth knowing before they go to a festival:** the SRT is SDH-style, every cue wrapped in `<b>` tags, 91 dialogue cues and 123 sound-description or lyric cues, and timecode starts at 01:00:00 rather than 00:00:00. A festival wanting plain dialogue-only subtitles at zero-based timecode needs a derivative, not this file. None was made.

**PDF builder** `tools/build-epk-pdf.py`: holder notes updated for the five fields and the footer no longer lists SRTs under "Only Yeo". `press/EPK-breakdown.pdf` rebuilt from rev 4 and rendered to check the layout. `__pycache__/` added to `.gitignore`.

**Flag, public repo:** this is the first time film material, not campaign paperwork, has gone into `Scroggdawg/kom-festival-board`, which is public. The poster is press material by definition. The SRT is the film's complete dialogue. Luke asked for both to go up; if the transcript should not be world-readable, one commit removes it and the README row with it.

---

**Timestamp:** 2026-09-08
**Lane:** `epk`
**Continues:** handoff-066-epk.md
**Model:** Fable 5.1. Goose turn: place, transcribe, verify, publish.

## Next action (the one thing)

**Still the end-credit roll.** It now has two fewer jobs (3.14 and most of 9.1 are done) and the same checks: the three spellings in 3.15, whether the final opponent is a fourth principal, sound designer and EPs for 9.1, and everything in 7.1, 9.2, 10.1, 11.1, 11.3. Also open: Kenner's actor; Jordan's pick between logline A and B; 2.2 the synopsis; a web-size poster derivative for FilmFreeway if the 5.7 MB original is over their limit.

## Files

- Assets index: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/assets/README.md
- Poster: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/assets/POSTER/KillerOfMen_Poster_2160x2700.jpg
- Captions: https://github.com/Scroggdawg/kom-festival-board/tree/main/press/assets/SRT
- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/EPK-breakdown.pdf
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-066-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-067-epk.md
