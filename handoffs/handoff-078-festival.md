# handoff-078-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** checked Sundance instead of queueing it, as the docket urged. **The flag was a false positive — and the check earned its keep anyway, on something that is not a date.**

### Sundance's close was right all along

Verified on sundance.org's own submit page. Shorts ladder: **early Jul 13 $55 · official Aug 3 $75 · LATE Aug 31 $95.** "Late" is **the name of the final tier**, not evidence of a later one. `close 2026-08-31` was correct and the board showing Sundance closed is correct. `provenance: official`. Verified **3 of 97**; flagged **15 → 14**.

**The false-positive mode is general and is now written into the validator's own docstring** rather than fixed by tightening the regex — tightening trades false positives for false negatives, and the flag's job is to say *worth checking*. **A flag means WORTH CHECKING, never DEFECT.**

### What the check actually caught — an eligibility contradiction, not a date

Sundance states two rules that conflict for this film, both verbatim from the same page:

> "Only projects retaining world premiere status are eligible for open submission to this category."

> "Projects completed after December 31, 2025 are still eligible to submit to the Festival, regardless of premiere status."

*Killer of Men*'s world premiere is **spent**, which the first excludes. It was **picture-locked Jan 2026**, which the second includes. **NOT RESOLVED** — the 2027 Submissions Rules PDF is unread, and a premiere-eligibility question should not be settled by inference. Both quotes and the PDF link are on the record.

Moot for 2027 shorts (Aug 31 passed). **Decisive for the next cycle, and it generalises:** any festival requiring world-premiere status is off the board unless that completion-date exemption is real. **That touches the premiere ledger, not one record.**

### `flagsComputedAt` shipped

At the docket's request, and it correctly asked for the cheap half first:

```
{"rev": "be53ab1c-…", "at": "2026-09-08", "flagged": 14, "by": "tools/validate-data.py --write-flags"}
```

`flagsComputedAt.rev != data.rev` means a board publish moved the data after the flags were computed, so the dashboard can go quiet instead of rendering stale flags silently. **Publish-loop recompute deliberately not done** — the stamp makes the window visible, which was the actual problem.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-077-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**Read the Sundance 2027 Rules PDF** and settle the premiere-status contradiction. It is not about Sundance — it decides whether a whole class of world-premiere festivals is reachable, and the premiere ledger currently assumes they are not.

Then Luke's three, still unanswered: **does he have a file to upload** (decides whether IFFR Sep 15 is reachable at all), **IFFR yes or no**, and **the Aspen tier names off FilmFreeway** (403 to automated fetch; he has an account).

## Files

- Board data: https://github.com/Scroggdawg/kom-festival-board/blob/main/data.json
- The gate: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/validate-data.py
- Page draft v6 (for Jordan): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/filmfreeway-page-v6.docx
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-077-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-078-festival.md
