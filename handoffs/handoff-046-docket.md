# handoff-046-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** the tier-suspicion rule is now a field, and the homepage reads it.

### One rule, one implementation

The festival lane wrote `closeUnverifiedTier: true` onto each record its validator suspects of holding a fee tier in the door field. **The dashboard reads that flag rather than re-deriving the rule** — the position taken last turn, and the reason is the `source` / `sourceUrl` fork we paid for earlier today. When the rule sharpens again, and it has sharpened three times in a day, it sharpens in one place.

The board tile now carries **"may be a price step · 15"** beside "verified at the festival · 2 of 97".

**Checked before trusting it:** the flagged set is identical to what my own derivation picks, all 15, and no verified record carries it. That comparison was a one-off to confirm I was reading the right field, not a second implementation.

### Staleness, named rather than assumed

The flag is derived, so it can rot — and **derived data rotting silently is the stale board snapshot in a different costume.** A plain validator run now recomputes every flag and errors if a stored one disagrees; they verified the detection fires by flipping a record's `provenance` the way a browser publish would and watching the gate refuse.

The window that remains: if Luke publishes an edit to `feesText` or `provenance` from the board, the flag is stale until someone runs the tool. Their offer was to recompute in the publish loop. **Countered with the cheaper half:** the data carries no marker for when the flags were computed, so my page cannot tell fresh from stale. One field holding that rev or timestamp would let the tile say "as of the last check" and go quiet when the file has moved on — a visible staleness window instead of a silent one, at no publish-loop surgery.

### The one that is not a data item

Of the 15, three fall inside four months. **Sundance is the loudest and it is not hygiene.** Its `close` is `2026-08-31`, explicitly labelled *"$95 (late tier)"* in its own fee text, and **eight days in the past** — so the board currently shows a closed door for a festival that may still be open, and it is Sundance. That lane correctly refused to infer a replacement date after making two inferences today. **It deserves to reach Luke as a question, not to sit as one of fifteen.**

Rev 63 unchanged; `todo.json` needed nothing this turn.

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-045-docket.md
**Model:** Opus 5. **Goose turn** — a rule read as a field, a staleness window named, one item escalated out of a queue.

## Next action (the one thing)

**Sundance** — whether its door is genuinely past or the board is showing a late tier as a close. Then, still Luke's alone: is Jordan's YouTube link downloadable (D.3.1), and does Luke have a file to upload at all.

## Files

- Dashboard: https://scroggdawg.github.io/kom-festival-board/
- Docket: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Dashboard source: https://github.com/Scroggdawg/kom-festival-board/blob/main/index.html
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-045-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-046-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-490-docket.md
