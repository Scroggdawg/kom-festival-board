# handoff-047-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** the staleness window is now visible on the homepage, and the flag that prompted it turned out to be a false positive that paid for itself anyway.

### A stale number can no longer pass as current

The festival lane added `flagsComputedAt` to `data.json`:

```
{"rev": "be53ab1c-…", "at": "2026-09-08", "flagged": 14, "by": "tools/validate-data.py --write-flags"}
```

The tile compares `flagsComputedAt.rev` to `data.rev`. **Matching → "may be a price step · 14". After a board publish moves the file past the stamp → "14 · as of Sep 8".** Tested both paths by handing the page a `data.json` with a later rev, watching the label change, and restoring. The silent window is a visible one, and the publish-loop recompute stays unbuilt — the cheap half was the right half.

### Sundance: the flag was wrong and the check was right

`close 2026-08-31` was correct. Sundance's own ladder is early Jul 13 $55 · official Aug 3 $75 · **late Aug 31 $95** — *"late" is the name of the final tier*, not evidence of a later one. `provenance: official` set. **Verified 3 of 97, flagged 15 → 14.**

That lane wrote the false-positive mode into the validator's docstring rather than tightening the regex, on the grounds that tightening trades false positives for false negatives. **A flag means WORTH CHECKING, never DEFECT** — and the tile's wording stays matched to that. A flag that only fired on real errors would have to be as smart as the check it replaces, which would make it the check.

### The thing that is not about dates at all

Sundance's page states two eligibility rules that contradict each other for this film, both quoted verbatim from the same page:

> "Only projects retaining world premiere status are eligible for open submission to this category."

> "Projects completed after December 31, 2025 are still eligible to submit to the Festival, regardless of premiere status."

*Killer of Men*'s world premiere is spent — excluded by the first. It was picture-locked Jan 2026 — included by the second. **Unresolved**; the 2027 Submissions Rules PDF is unread and that lane declined to settle a premiere-eligibility question by inference. Recorded on the record with both quotes and the link.

Moot for 2027 shorts, since Aug 31 has passed. **Decisive for whether Sundance is a target next cycle, and it generalises: if the completion-date exemption is not real, every world-premiere-only festival comes off the board.** That is a shape-of-the-campaign question, and it lands on the premiere ledger — D.5.9 in my file, which currently only records that the world premiere is spent.

**Not written into `todo.json`.** It is a question with two quotes and an unread PDF, not a task; inventing an item would be deciding the campaign has a new workstream. If Luke says it does, the wording comes from him.

Rev 63 unchanged.

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-046-docket.md
**Model:** Opus 5. **Goose turn** — a staleness window closed, a false positive that earned its keep, a question left as a question.

## Next action (the one thing)

**The Sundance eligibility contradiction, to Luke, above everything else tonight** — it decides whether a class of festivals is on the board at all. Then the two still only he can answer: is Jordan's YouTube link downloadable (D.3.1), and does he have a file to upload (D.3.3).

## Files

- Dashboard: https://scroggdawg.github.io/kom-festival-board/
- Docket: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Dashboard source: https://github.com/Scroggdawg/kom-festival-board/blob/main/index.html
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-046-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-047-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-491-docket.md
