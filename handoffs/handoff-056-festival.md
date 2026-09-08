# handoff-056-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** The Docket lane ran this lane's rule ("never write by fuzzy match; read back before committing") against its own writer and found a real gap — its publish step wrote the merged document raw and committed it, bypassing the validation the normal save path performs. Now fixed: validate the merge, write, re-read from disk, compare against intent, revert rather than commit if either check disagrees; tested with a merge rigged to return an invalid document.

**So this lane ran the same rule against itself, and came off worse.**

### The finding

Every `data.json` edit made this week has been an ad-hoc inline Python script with **no validation and no read-back**. The curtas-vila-do-conde collision was caught because the script happened to print its results, not because anything checked. That is luck, not process.

### Built: `tools/validate-data.py`

- **Structural gate** (always errors): schema is 2 · required top-level keys · ids unique and non-empty · every festival has a name · disposition in target/bench/out · `open`/`close`/`festDate` are ISO dates that actually parse · close not before open · event types known · premiere ledger ids unique and states valid.
- **`--provenance`** (advisory): the rule learned the hard way — a close date is only trustworthy with the festival's own page behind it (`source` URL) and the tier or category named beside it (`feesText`/`why`).
- **`--strict`**: promotes provenance warnings to errors.

**It failed on its first run and found three real defects:** `college-television-awards-46th`, `dga-student-awards-2027` and `student-academy-awards-54th` each carried `festDate: ""` where they should carry `null`. Not a render bug — the page's `parseD` treats falsy as missing — but exactly the drift that becomes one. Normalised, re-validated clean, snapshot refreshed, pushed.

### The hook proposal, now with its real cost

**73 of 97 targets would fail `--strict` today**: 26 have a close date with no source URL, 47 name no tier or category anywhere. So the hook is not a switch, it is a **research backlog of about 73 records**. Recommendation to Luke: leave it advisory, put `--strict` in CI only once the backlog is cleared, and in the meantime hold new dates to the standard by hand.

### Standing between the lanes

Both lanes wrote destructively against something fuzzy today, both found it, both closed it. The reciprocal audit — each running the other's rule against its own code — found three defects between them that neither would have found alone. Worth keeping as a habit.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-055-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**Luke: the end-credit roll and the ~100-word synopsis — still the two cheapest, still blocked on nobody.** Then whether any of the five playbook items get filed, and whether the 73-record provenance backlog is worth clearing. Real clock: **SBIFF Sep 18, Aspen Sep 25** (about half off on request).

## Files

- Validator: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/validate-data.py
- Board data: https://github.com/Scroggdawg/kom-festival-board/blob/main/data.json
- One sheet: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk-one-sheet.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-055-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-056-festival.md
