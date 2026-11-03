# handoff-174-screener — Spec re-audit: the screener meets every required line

## Recap (newest first)
- **Luke's call:** the Yoruba chant (0:09–0:36, sung, untranslated in the master and in the SDH captions) needs no subtitles. He found the Codex audit excessive for a "does it match" question; that is recorded as feedback in memory.
- **Re-audit from scratch of `KillerOfMen.mp4`:** every required line of the Berlinale spec passes. MP4 (`isom`), H.264 High, AAC-LC stereo, a single file, 8.81 GB, 24 fps constant and progressive (all 18,720 frames are 1/24 s; the bitstream is progressive-only), 1920×1080 16:9, AAC at 320 kbps and 48 kHz, filename 15 ASCII letters.
- **One difference from the *suggested* settings:** video runs at 90 Mbit/s against their suggested 10. This is deliberate. The binding limit is the 10 GB cap, and 10 Mbit/s is the rate that smeared the grain.
- **Audio sync is sample-exact against the master** at the start, middle and end. L and R are not swapped.
- **Codex (`gpt-5.6-sol`) verdict: READY-WITH-CAVEATS.** It agreed that all mandatory limits pass. It suggested re-encoding near 10 Mbit/s at a lower H.264 level; I disagree, because that brings back the grain loss Luke rejected. Its other caveats were the Yoruba (since settled by Luke) and picture lock (the film is finished).
- **Tooling note:** `~/.codex/config.toml` sets `model = "gpt-6.1-sol"`. Codex 0.145 rejects that model on the ChatGPT login. `-m gpt-5.6-sol` works. The config is unchanged; Luke decides.

## Next
1. Luke watches and listens to the file, then uploads it once and clicks Release within 3 days.

---
**Timestamp:** 2026-11-02 · **Lane:** `screener` · **Continues:** handoff-173-screener.md · **Model:** Opus 5.5 (duck turn; Codex gpt-5.6-sol as cross-family check).
