# handoff-173-screener — Screener method filed as a doctrine playbook

## Recap (newest first)
- **Doctrine published.** `PLAYBOOKS/festival-screeners.md` is pushed to `Scroggdawg/bmf-doctrine` (`2ab8e09..5b2a43f`, in sync with origin). Index rows were added to `PLAYBOOKS/README.md` and `START_HERE.md`. The README was also missing a row for `claude-surfaces-2026-09.md`, so I added it and corrected the index count to 16.
- **The playbook's script is a generic `screener.sh`, not the KOM one.** It reads the frame size and audio layout from the master and boxes any aspect ratio into 1920×1080 at the nearest even size. It picks Level 4.1 or 5.1 from the bitrate, puts `setsar=1` in the filter chain, and keeps the lossless tag-fix remux. Tested on the KOM master (2048×858, 5.1): its audio matches the shipped screener at −23.6 LUFS on the same 10 s. Also tested on a synthetic 1998×1080 1.85 source, which came out 1920×1038 at y=20.
- **Testing the script caught three bugs**, all fixed and recorded in the playbook. `$H:flags` triggers zsh's history modifiers. ffmpeg 9's csv writer emits a blank first line, which left the channel count empty. That empty count made the script fall through to plain `-ac 2` without a word, so it now aborts on an unknown layout. The shipped KOM screener was not affected: its script hard-codes the fold-down, and its −21.8 LUFS confirms it.
- The doctrine audit flags 12 stale playbooks, 1 with no date, and 19 root files against a soft cap of 18. All of that predates this turn. The new playbook passes.
- handoff-172: the Berlinale screener `FINAL/BERLINALE SCREENER/KillerOfMen.mp4` is encoded and verified, but not watched end to end and not uploaded.

## Next
1. Luke watches and listens to `KillerOfMen.mp4`, then uploads it once and clicks Release within 3 days. This is unchanged from handoff-172.
2. Optional: a doctrine audit pass to re-verify or prune the 12 stale playbooks.

---
**Timestamp:** 2026-11-02 · **Lane:** `screener` · **Continues:** handoff-172-screener.md · **Model:** Opus 5.5 (duck turn, executed directly; no goose).
