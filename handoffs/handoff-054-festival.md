# handoff-054-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** The Docket lane overruled my suggested due date and labelled its reasoning as an inference. I checked it. **It was right and I was wrong** — and checking it properly surfaced a second thing I had not considered, and a mistake I made while fixing the first.

### The date question, settled with evidence

| Festival | Date | Verified on its own FilmFreeway panel | In the nine? | Fee |
|---|---|---|---|---|
| Curta Cinema Rio | **Sep 12** | Earlybird tier | yes | **$10.73 / $14.30 / $19.07; student $4.47–5.96 — under the ~$20 threshold** |
| **SBIFF** | **Sep 18** | **Official Deadline — a real door** | yes | **$60 at that tier** (listing runs $50–125) |
| Aspen | Sep 25 | Regular Deadline — real | yes | $80 → $95 |

The Docket lane set D.1.1 and D.1.5 to **Sep 18** on the reasoning that a task whose purpose is *to precede a payment* cannot be dated after the first door where money changes. Better than my suggestion of Sep 30, which would have dated a nine-festival task by one festival's own calendar. Curta's Sep 12 is earlier and is a genuine money change, but its fees fall below Joan's ~$20 threshold, so it does not trigger the email task. **Sep 18 stands.**

### `data.json` corrected — and a self-inflicted error, caught and reverted

Corrected on the board with notes and fresh `lastChecked`: **short-shorts-2027** (close Sep 9 → **Sep 30**; the Sep 9 date was the pitch competition), **flickerfest-36th** (early bird passed Aug 14), **sbiff-42nd** (Sep 18 verified as the Official Deadline, fees restated), **aspen-shortsfest-36th** (Sep 25 verified).

**Then I corrupted a record.** My matcher keyed on the prefix `curta`, which hit **`curtas-vila-do-conde-35th`** — a Portuguese festival with nothing to do with Curta Cinema Rio, which is not on the board at all (it came from the thesis list). It took Rio's close date, fee text and correction note. Caught on the read-back, restored verbatim from `HEAD~1`, and confirmed only the four intended records now carry a Sep 8 note. 151 festivals, validation clean, snapshot refreshed.

**Rule adopted: never match a festival record by name prefix. Match on the full id, and read the record back before committing.**

### Worth keeping about how this went

The Docket lane refused twice — once on my timezone reasoning, once on my date — and both refusals caught something real. Its habit of labelling an inference and naming the one fact that would overturn it is why this took four minutes instead of an argument. Said so to it directly.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-053-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**Luke: the end-credit roll and the ~100-word synopsis — both need nobody.** The real festival clock is **SBIFF Sep 18 (ten days)** and **Aspen Sep 25 (seventeen days)**; Aspen reportedly gives about half off on request, so the discount emails should target those two first.

## Files

- Board data: https://github.com/Scroggdawg/kom-festival-board/blob/main/data.json
- Corrected recipients: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/discount-email.md
- One sheet: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk-one-sheet.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-053-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-054-festival.md
