# handoff-077-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** the docket verified the `close` fix by **simulating its tile forward** — today Rotterdam Sep 15, on Sep 16 now SBIFF Dec 2 rather than the old Sep 18 lie. Then it made a request this lane should have anticipated.

### One rule, one implementation

It wanted the suspect count on the homepage but **refused to re-derive the rule in its own page**: *"two implementations of one rule drift, and we have already paid for that once today with `source` and `sourceUrl`."* Correct, and the right precedent.

So the rule stays in `tools/validate-data.py`, once, and `--write-flags` writes its result onto each record as **`closeUnverifiedTier: true`**. The dashboard reads a field instead of reimplementing a regex. When the rule sharpens again — it has sharpened three times today — it sharpens in one place.

### Derived data that cannot rot silently

A stale embedded snapshot in `board.html` was this week's lesson, so the flag was not shipped bare: **a plain validator run recomputes every flag and errors when a stored one disagrees.** Verified the detection fires rather than assuming it — flipped one record's `provenance` to `official` the way a browser publish would, without re-running the tool, and the gate refused:

> `ERROR sxsw-2027: stored closeUnverifiedTier=True but computed False — run --write-flags`

Then restored. **Known window:** a board publish that edits `feesText` or `provenance` leaves the flag stale until the tool runs. Offered the docket a publish-loop recompute if that matters to its surface.

### The 15, and one that is louder than the rest

Flagged: sundance, aspen, ann-arbor, sxsw, flickerfest, regard, tampere, atlanta, florida, cleveland, siff, short-shorts, palm-springs, raindance, indy-shorts.

**`sundance-2027` is the loudest.** Its `feesText` reads "$95 **(late tier)**" — it says outright that `close` holds a tier — and that date, 2026-08-31, is **eight days past**. So the board currently shows a closed door for a festival that may still be open. **Not touched:** it needs a first-party read, not a third inference in one day.

### Kept from the docket

Its Dec 2 future state — the tile reading "none verified yet" once both verified records pass — **is the truth and should not be papered over.** A tile that says nothing beats one that says something false, and it is the most honest argument for clearing the backlog: the front page goes blank until someone does the work.

And its framing of the buggy check beats mine. This lane framed it as catching an error; the docket framed it as **catching it before it trained anyone to skim** — which is the actual damage a noisy gate does, and why the original error survived three rounds rather than one.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-076-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**Sundance needs a first-party read** — its close is a self-declared late tier, eight days past, and the board is calling it closed.

Then the three still with Luke: **does he have a file to upload** (decides whether IFFR is reachable at all), **IFFR yes or no**, and **open the Aspen FilmFreeway listing** (403 to automated fetch; he has an account).

## Files

- Board data: https://github.com/Scroggdawg/kom-festival-board/blob/main/data.json
- The gate: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/validate-data.py
- Page draft v6 (for Jordan): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/filmfreeway-page-v6.docx
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-076-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-077-festival.md
