# handoff-065-epk

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** the festival lane locked the logline in **two versions** and is presenting both to Jordan rather than choosing. That made `2.1` a schema question, not a formatting one, and it was handed to this lane to decide. **`press/epk.json` rev 2, schema 3 · 10 of 49 filled, 1 undecided.**

### The decision: a field may carry candidates

```json
"id": "p2-logline", "n": "2.1", "value": "",
"options": [
  {"key": "A", "note": "title front, concrete ending", "value": "KILLER OF MEN -- In 1834 …"},
  {"key": "B", "note": "title drop, identity ending",  "value": "In 1834 … a KILLER OF MEN."}
]
```

The constraint the lane set was that neither version may be primary, because both ship and one comes back chosen. Three shapes were on the table and this one was picked for a specific reason:

| Shape | Why not |
|---|---|
| Two fields, `2.1` and a new number | A new field appends to the **end** of section 2, so B would sit after "Hero still" — and giving A the `2.1` slot makes it primary, which is the one thing that was ruled out |
| One field holding both, with labels | Costs nothing, but when Jordan picks, someone hand-edits a 356-character string down to one. That edit is exactly the drift this file exists to prevent |
| **`options` on the field** | Neither is primary, the field's own `value` stays empty until a choice returns, and **choosing copies the stored bytes** rather than retyping them |

`2.1` keeps its number. No new numbers were minted, so the numbering discipline holds.

**`value` empty is the honest state**, not a regression: the writing is locked, the choice is not, and page 2 cannot be printed until it comes back. The counters say `10 filled · 1 undecided` rather than pretending. The PDF now shows `2.1` amber, "2 versions — with Jordan".

### Verbatim, and checked

Both strings were taken from `press/logline-idea-box.md` — the committed artifact — and then byte-compared against the message that asked for them.

| | Length | Matches the lane's count | Byte-identical to the message |
|---|---|---|---|
| A | 356 chars · 65 words | yes | yes |
| B | 354 chars · 64 words | yes | yes |

Everything flagged do-not-normalise survives: the literal `--` in A, the `...` in B (it replaces an em dash Luke has a standing rule against), lowercase `faith`, ALL CAPS on the title, and no em dash anywhere in either. The lane's claim that the shared span is identical checks out — 49 words plus the seven-word open seam `who he must now face to decide`, which is 56 as they said, and which appears identically in both, so a later edit to it hits both at once.

The **superseded 62-word morning lock is still in the field's history** and recoverable.

### Tested

The 24-check rig still passes whole under schema 3. On top of it: a single candidate, a keyless candidate, duplicate keys and a non-text candidate value are each refused by the validator; candidates survive a merge byte-identical while both machines' other edits land; and a candidate set written on the other machine arrives here without clobbering ours.

Then the real page against the real server: clicking **Use this** on B wrote a value byte-identical to the stored candidate, kept the ellipsis and the lowercase `faith`, marked B "in use", kept both candidates on record, and moved the header from `10 filled · 1 undecided` to `11 of 49 filled`. That was in the isolated rig — the committed file is still undecided, as it should be.

---

**Timestamp:** 2026-09-08
**Lane:** `epk`
**Continues:** handoff-064-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Jordan picks A or B**, and whoever has the page open clicks Use this — nobody retypes it. Meanwhile the end-credit roll still fills eight fields across six pages and needs nobody, and `2.2` the synopsis is still unpicked (three drafts in `press/synopsis-draft.md`, recommendation C — and it is now a candidate set waiting to happen, if Luke wants both finalists held the same way). Still unanswered from handoff-062: decimal `3.15` or Roman `III.15`.

## Files

- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/epk.py
- Both locked versions: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/logline-idea-box.md
- Page draft v6: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/filmfreeway-page-v6.md
- Synopsis drafts: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/synopsis-draft.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-064-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-065-epk.md
