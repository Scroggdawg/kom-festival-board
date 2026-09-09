# handoff-092-epk

## Where we left off

**This turn (Sep 9, 2026, Opus 5):** Luke moved the contents into the Google Doc himself and deleted this lane's `.docx`, leaving one primary document called *EPK INFO — all the text*. He then asked for a colour formatting pass, matching the scheme on the progress bars. Delivered as two files in chat, not into `00 PRESS` — the folder stays at one document. **`press/epk.json` unchanged at rev 19 · 38 of 47 = 81%.**

### Colour now carries authorship, and that is a deliberate change

Each section is set in the hue its bar uses. That same hue carries the authorship signal: **coloured body text is Claude's and wants checking; black body text is a person's.**

That replaces "blue is Claude", and the reason is measured. Keeping a separate authorship blue alongside coloured section headings would have put `#1a5fb4` **five ΔE** from section 2's `#0051a1` — far under the 15 floor, a pair no reader can reliably separate. Two signals would have collided; one signal cannot. What Luke wanted from the convention — seeing at a glance what he still has to check — survives intact.

**All eleven hues were re-validated against white before use.** They were chosen for cream on a dark ground, so their behaviour on paper was not safe to assume:

| worst | best | gate |
|---|---|---|
| 5.32 : 1 (section 8) | 8.91 : 1 (section 9) | 4.5 : 1 body text — all pass |

### What could not be done, again, and the way round it

Writing into the `.gdoc` is still impossible from this machine — no Docs connector, no API client, no CLI, and the file on disk is a 175-byte pointer. Luke solved it by hand this turn.

So the colour pass ships as **two routes**, and he picks:

- **`.docx`** — Drive → right-click → Open with → Google Docs, then paste or replace.
- **`.html`** — open in a browser, select all, copy, paste into the Doc; colours travel with a paste.

Neither was written into `00 PRESS`, because the point of the last two turns was to stop having two documents in there.

**One honest limit:** whether Google Docs preserves every run colour on paste cannot be tested from here. The `.docx` route is the safer of the two, because its colours are in the file rather than in a clipboard.

### A conversion bug worth remembering

`textutil` shifts colours on the way into `.docx` — it moved thirteen distinct values, so `#635ad0` and friends arrived as near-misses. The build now snaps every run colour back to the nearest authored value and asserts that the finished file contains **only** authored hues. Without that check the document would have looked right and been subtly off-palette from the bars.

`tools/build-epk-doc.py` is committed so the document regenerates from `epk.json` instead of being hand-assembled, with the hues inlined rather than read from a scratch file.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-091-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Jordan on `2.1` and `2.2`.** Section 2 is the only one at zero, both items are written, and settling `2.2` also settles section 4 — the statement is one of its two candidates, which is why that bar is hatched. Then `3.12` and `A.2` are both You Wu, and `A.5` is Jordan. Unanswered since handoff-062: decimal `3.15` or Roman `III.15`.

## Files

- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Document builder: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-doc.py
- PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/EPK-breakdown.pdf
- On the Drive: `05 MARKETING/00 PRESS/EPK INFO — all the text` (Luke's Google Doc, now primary)
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-091-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-092-epk.md
