# handoff-064-epk

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** first real intake. The festival lane sent word that Luke locked the logline and asked this lane to write it into `2.1`. Done. **`press/epk.json` rev 1 · 11 of 49 filled.**

### The logline was taken from the file, not from the message

The request arrived as a cross-session message quoting the text. Rather than retype it, the string was extracted from `press/logline-idea-box.md` — the committed artifact — and then compared byte-for-byte with what the message carried.

| Check | Result |
|---|---|
| File and message identical | yes, byte for byte |
| Length | 330 characters · 62 words — matches the count the lane stated |
| Capital F on "Faith" | intact (dictated that way, flagged to Luke once, kept) |
| "finds it **being** held" | intact (deliberate — the ceremony is in progress and he interrupts it) |

Written through `tools/epk.py`, so it validated, stamped history as `festival lane — Luke locked it Sep 8`, and was **read back from disk** and confirmed byte-identical before the commit. `updatedBy` is `festival lane via epk-intake`. `press/EPK-breakdown.pdf` regenerated from the new data.

**Why the check mattered rather than being ceremony:** the whole point of this lane is that `epk.json` is the one place the EPK's text is correct. A logline that picks up a re-punctuation on its way through a chat message is exactly the kind of drift the file exists to prevent, and reading the committed file instead of the message removes the risk rather than reducing it.

### Verified before writing

The message's claims were checked against the repo rather than taken on trust: `press/filmfreeway-page-v5.md` and `.docx` exist, `press/logline-idea-box.md` carries the LOCKED banner dated September 8 with Luke's *"i think lock this for now"*, and the festival lane had already rebased onto this lane's colour-band commit (`0b39125`). Both lanes are on `main`.

### Still true

`2.2` the synopsis remains unpicked — three drafts in `press/synopsis-draft.md`, 96–101 words, recommendation C. That is now the only thing in section 2 that needs nobody but Luke.

---

**Timestamp:** 2026-09-08
**Lane:** `epk`
**Continues:** handoff-063-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**The end-credit roll.** It fills `3.14`, `3.15`, `7.1`, `9.1`, `9.2`, `10.1`, `11.1` and `11.3` — eight fields across six pages, no hard drives, just the YouTube link. Then `2.2`, a one-minute pick. Still unanswered from handoff-062: decimal `3.15` or Roman `III.15`.

## Files

- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- The locked logline: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/logline-idea-box.md
- Page draft v5: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/filmfreeway-page-v5.md
- Synopsis drafts: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/synopsis-draft.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-063-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-064-epk.md
