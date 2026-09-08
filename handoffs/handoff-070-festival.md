# handoff-070-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** the docket session moved the board. `index.html` is now a campaign dashboard reading all three data files; **the board lives at `board.html`**. Luke asked the docket for this directly.

### Verified before accepting

- **`board.html` is byte-identical** to `index.html` at the commit before the swap. Ran `cmp` against `91e6aecd^:index.html` rather than taking the claim.
- **The docket's "1 of 97 verified" is correct.** Counted independently: exactly one target carries `provenance` and `sourceUrl`, and it is IFFR. It also declined to headline Carthage Sep 15, which is right — that record is still sourced to a Malian news site.

### Three things the swap broke in this lane, all fixed

1. **`tools/embed-snapshot.py` and `tools/heat-expand.py` both read and wrote `index.html`.** Traced both: neither could corrupt the dashboard (each fails its assert before writing), but neither could do its job. Retargeted to `board.html`.
2. **The embedded offline snapshot in the board was stale** — surfaced by running `embed-snapshot.py` after retargeting. It predated the IFFR verification, so the offline fallback still served `feesText: "€85"` and a null provenance. Refreshed. **That staleness was this lane's, not the docket's**; the swap just made it visible. Nothing re-embeds automatically, so any hand-edit of `data.json` leaves the fallback behind until someone runs the tool.
3. **`README.md` documented `index.html` as "the whole application."** Rewritten for four surfaces; it now also records that `todo.json` and `press/epk.json` are not written from this lane.

Added a `← Campaign dashboard` link to `board.html`'s header, matching `docket.html`'s. Without it the board was a dead end.

`PLAN-v2.md`, `PLAN-editable-board.md`, `PLAN-docket.md` left alone — historical build specs; rewriting them would falsify the record.

### The colour finding is bigger than the dashboard

The docket ran the validator instead of trusting its eye and found **violet against periwinkle at ΔE 3.2 deutan / 10.4 normal-vision** — far under the floor. That is a constraint on the five section colours as a *categorical set*, not a fact about one page: they cannot be used to distinguish categories anywhere, including the Docket's own status blocks and any chart either lane builds. Asked the docket to record it where the colours are defined.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-069-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**IFFR closes Sep 15, 17:00 CEST — seven days**, verified in 067, still unanswered. Its blocker is a **screener link**, not the logline.

Logline is one word from settled: *"his last opponent"* reads as both "most recent" and "final ever"; **"the opponent he killed"** (65 words) fixes it. Then v6, then message the docket to pin the version and the EPK session to update field 2.1.

## Files

- Board (was index.html): https://github.com/Scroggdawg/kom-festival-board/blob/main/board.html
- Dashboard: https://github.com/Scroggdawg/kom-festival-board/blob/main/index.html
- README, rewritten: https://github.com/Scroggdawg/kom-festival-board/blob/main/README.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-069-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-070-festival.md
