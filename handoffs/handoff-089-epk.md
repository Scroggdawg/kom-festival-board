# handoff-089-epk

## Where we left off

**This turn (Sep 9, 2026, Opus 5):** Luke marked up the "what is left" list with owners and pushed back on `5.7` still appearing after he had just sent the Instagram and IMDb links. **`press/epk.json` rev 17 · 37 of 47 = 79%.** Changes are on git and on the Drive.

### He was right to push back, and the fault was the label

`5.7` was called **"Instagram and IMDb links"**. He had just supplied the film's Instagram and IMDb, so seeing that label still open read as the list ignoring him. It is a different field — `3.18` and `3.19` are **the film's** accounts, `5.7` is **each filmmaker's own**, which the bios link out to — but nothing in the wording said so.

Relabelled **"Instagram and IMDb, per filmmaker"**. Numbers are permanent; wording is not, and this is exactly the case for changing it. `set_label()` added, and it stamps history so the change survives a merge.

**Still worth a decision:** `5.7` may not be wanted at all. `press/epk-spec.md` has bios linking to Instagram and IMDb per person, which is why it exists, but if Luke does not want per-person links in the kit it should be retired rather than sit on the list. One word.

### Who each open item waits on

A field may now carry **`waiting`** — who, never what; the material always lives in `value`. From Luke:

| | | |
|---|---|---|
| `2.1` Logline | pick one of three | Jordan Betine |
| `2.2` Synopsis | pick one of two | Jordan Betine |
| `3.12` Exhibition formats | | You Wu |
| `A.5` 60-second introduction | | Jordan Betine |

The page shows it beside the label. **The PDF now reads `waiting` from the data** rather than its own static holder table, so the two can no longer disagree — the table was already stale on several rows.

**"YW" is read as You Wu**, the credited editor; exports are the editor's to produce. That also makes the long-standing **"Yeo" almost certainly a transcription of "You Wu"** — the name Yeo appears nowhere in the credit roll. Flagged, not asserted, and not written into the file as a fact.

Luke's other markings are recorded but not turned into `waiting`, because he did not assign them: `7.1` cast bios, `11.2` partner logos, `A.2` trailer, `A.3` laurels.

### A merge that git could not do

A concurrent write from the other account filled **`5.6` headshots** — four, full resolution — while this lane was setting the owners. Git hit a content conflict on `epk.json` and then kept replaying a stale pre-merge commit through two rebase attempts.

Resolved by **not letting git decide**: the branch was reset to origin, and `tools/epk.py merge` redone against the current head — per field, newest history entry wins, both histories kept. Both sides survived: their `5.6` value and this lane's four `waiting` values and the `5.7` relabel. The result was validated, written, and **re-read from disk and compared before committing**.

### Landed, and retired

In: `3.18` Instagram, `3.19` IMDb (new field on the links footer), `5.6` headshots.
Retired last turn, numbers withdrawn: `2.3` hero still, `4.2` photo behind the text, `9.3` still behind the credits.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-087-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Jordan picks the logline and the synopsis** — `2.1` and `2.2`, both written, both one click, and section 2 is the only one still at zero. Then `3.17` press contact, which waits on nobody. Of the eight genuinely missing, only `7.1` cast bios is writing; the rest are files to collect. Unanswered since handoff-062: decimal `3.15` or Roman `III.15`.

## Files

- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/epk.py
- PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/EPK-breakdown.pdf
- On the Drive: `05 MARKETING/00 PRESS/EPK INFO (Claude).docx` · `EPK BUILDS/EPK-breakdown.pdf`
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-087-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-089-epk.md
