# handoff-109-festival

2026-09-10 · lane: festival · model: Opus 5 · goose turn (research, write, deploy, verify)

## Where we left off, newest first

1. **Manaki Brothers added to the list for next year** — Luke sent filmfreeway.com/ManakiBrothers and asked for it on the list for next year. It was already on the bench from the Aug 25 sweep; promoted to **target (strong)** for the **48th edition, ~Sep 2027**. Commit `4d09ea8`, verified live.
2. handoffs 104–105 (not in this repo by design): AFI handbook read on festival authority.
3. handoff-018: the full campaign published to this repo.

## What was verified (FilmFreeway rules for the 47th edition, read Sep 10, 2026)

| Item | Fact |
|---|---|
| Right lane | Student Films Competition: narrative and documentary student films under 20 minutes |
| Award | Crystal Camera 300 for Best Cinematography |
| Fee | $3 early / $5 regular / $7 late (2026) |
| Hospitality | Festival pays travel and accommodation for the cinematographer of every selected short and student film |
| Premiere | Macedonian premiere only; intact |
| 2026 cycle | Opened Feb 9, final (late) deadline Jun 20, notification Aug 20, festival Sep 19–25 |
| Oscar path | None; not a qualifier |

**The 2027 dates on the board are the 2026 pattern moved forward one year** (open ~Feb 9, close ~Jun 20, festival ~Sep 18), flagged estimated. The validator marks it `closeUnverifiedTier` (15 flagged, was 14). Correct until the 48th call posts.

## The eligibility gate, recorded in the record's `why`

Rules Art. III.3: *"Production of films submitted for participation must have been completed within 18 months prior to the dates of the Festival."* For a ~Sep 18, 2027 festival that means completion after ~Mar 18, 2026. **The Jan 2026 picture lock alone misses by about two months.** Entry therefore rests on the certified completion (delivery) date AFI holds. The Short Films Competition additionally requires release within the past 12 months, which the spent premiere likely rules out.

This converges with the open question from handoffs 104–105 (whether KOM is marked delivered): one answer from AFI's Post Production & Delivery office settles both.

## Notes

- "Next year" has no separate list in the schema (dispositions are target / bench / out). Next-cycle festivals are targets whose `edition` names the future edition — same convention as SLIFF, NHFF, FNC.
- Manaki is also on the DP craft sheet. Luke's Aug 25 call kept the DP lane off the main board; this one was added to the main board at his explicit request.
- Not starred as a Joan pick — it is Luke's.
- Heat row: prestige 6, craft 10, story 5, oscar 1, access 4 (rank 42 of 98). Access is held down by the eligibility gate.
- Shared tree: committed by explicit paths only; a peer session's uncommitted `tools/build-epk-kit.py` was left untouched.

## Verification

Validator clean (`--write-flags` then plain). Browser on localhost: board row, no Joan chip, heat row, estimated gantt bar, removed from the bench list, `validate(DATA)` 0, zero console errors; dashboard `index.html` reads 98 targets with zero errors. Live Pages: `data.json` rev `258c81b9` serving Manaki as target/strong, 98 targets, heat row present in `board.html`.

## Next action (the one thing)

**Ask AFI Post Production & Delivery for KOM's certified completion/delivery date.** It decides Manaki 2027 eligibility and answers the delivery question already open in handoffs 104–105.

## Files

- Live board: https://scroggdawg.github.io/kom-festival-board/board.html
- Manaki on FilmFreeway: https://filmfreeway.com/ManakiBrothers
- Commit: https://github.com/Scroggdawg/kom-festival-board/commit/4d09ea8
- Previous public handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-108-epk.md
