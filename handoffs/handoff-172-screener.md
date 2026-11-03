# handoff-172-screener — Berlinale selection screener encoded and verified

## Recap (newest first)
- **Verified against every line of the Berlinale spec.** The file is `FINAL/BERLINALE SCREENER/KillerOfMen.mp4`, 8.81 GB. It is H.264 High at 90 Mbps two-pass, 1920×1080 with the 2.39 picture letterboxed (1920×804 at y=138), exactly 24.000 fps progressive, and 18,720 frames, the same count as the master. Audio is AAC LC stereo, 48 kHz, 320 kbps. Square pixels, BT.709 1-1-1 tags, moov atom at the front. Full-film VMAF against the master: mean 98.6, worst 1% 92.9.
- **Tag fix after the encode.** The first output flagged its pixel aspect as 2144:2145 (left behind by the scaler) and its transfer as "unknown" (ffmpeg 9 ignored `-color_trc`). I fixed both with a stream-copy remux. The decoded video and audio MD5 hashes match the pre-fix file exactly, so no pixel or sample changed.
- **Audio is a 5.1 to stereo fold-down (Lo/Ro).** Centre and surrounds go in at −3 dB and the LFE is dropped. The raw fold-down peaked at +0.1 dBTP, so it carries a static −2 dB trim with no limiter. Result: −21.8 LUFS and −1.6 dBTP after AAC. The existing Vimeo stereo measured −20.2 LUFS and −1.9 dBTP, so the two are close. No stereo printmaster WAV exists anywhere on disk.
- **The bitrate comes from a measured ladder.** I tested the hardest 20 s of the film (10:20–10:40, a dark and grainy interior), with x264 preset slow, tune film, aq-mode 3:

| Encode | VMAF mean | Worst 1% |
|---|---|---|
| Existing 1 GB file (Resolve, 10.8 Mbps) | 86.3 | 78.6 |
| x264 10 Mbps | 89.7 | 80.5 |
| x264 20 Mbps | 91.9 | 83.2 |
| x264 40 Mbps | 94.2 | 87.6 |
| x264 60 Mbps | 95.4 | 89.5 |
| x264 90 Mbps (shipped) | 96.6 | 92.3 |

  The curve was still rising at 90 Mbps, which is why the encode uses most of the 10 GB cap. The artifacts Luke saw in the 1 GB file are grain smeared into waxy skin, plus macroblocking in near-black. The comparison crops show both.
- **Why ffmpeg and not Resolve:** no DaVinci MCP is connected. Resolve's H.264 export is also weaker per bit than x264, which can do 2-pass and dark-scene AQ.

## Not verified
- Nobody has watched or listened to the file end to end. That has to happen before upload, because a released upload cannot be replaced.
- How Berlinale processes the file. Their page says files are "processed and encrypted". **Inference:** they probably transcode it for their viewing platform, so the committee sees their re-encode. A clean source keeps artifacts from stacking, but the committee will not see 90 Mbps.
- Level 5.1 H.264. The spec only asks for High profile, and any modern decoder handles 5.1. If their processing rejects it, the fallback is a 50 Mbps Level 4.1 encode of about 5 GB. A file can be re-uploaded until it is released.

## Next
1. Luke watches and listens to `KillerOfMen.mp4`, at least the opening, 10:20–10:40 and the credits, and confirms the stereo fold-down sounds right.
2. Upload it once through Berlinale "My Film Entry". No test upload. Check the processed file (2–3 h, up to 24 h near deadlines), then click **Release** within 3 days.
3. Optional: free 33 GB of disk (98% full). `~/Downloads` holds duplicate copies of the 4444 XQ master and the 1 GB Vimeo file. Nothing has been deleted.

**Recipe** (reusable for other festivals' specs): `encode_screener.sh` and `verify_screener.sh` sit next to the screener.

---
**Timestamp:** 2026-11-02 · **Lane:** `screener` · **Continues:** handoff-171-letters.md · **Model:** Opus 5.5 (duck turn, executed directly; no goose).
