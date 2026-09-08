# handoff-036-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** no data change. The festival lane's validator failed on its own file; I audited mine for the same drift, found none, and made the validator say so.

That lane built `tools/validate-data.py` and it failed on first run: three records carried `festDate: ""` where they should carry `null` — tolerated by the renderer, one step from a bug.

### Audited todo.json for the same species

| Check | Result |
|---|---|
| Empty strings where null is meant | **None.** 68 absent values, every one `null` |
| Field types across all 37 items | Uniform: `due` str-or-null, `waitingOn` str-or-null, the rest all str |
| Items missing a field the others carry | None |
| Unparseable dates, in `due` or in any history entry | None |
| Section ids unique, colours well formed, status maps complete | All true |

**Nothing was keeping it that way.** `check()` tested four things. It now states the rest: rev a whole number, updated a real timestamp, the status maps complete, section ids unique and colours actually colours, owner and title filled, `waitingOn` null rather than empty, `due` a date that parses, and every history entry carrying a timestamp, a known status and an author.

Because `check()` gates both `save()` and `push()`, this is a gate **today** rather than an aspiration — `todo.json` passes it as written, so there is no backlog behind it. That is the difference from the other lane's position, where `--strict` would fail 73 of 97 records and turning it on is a research project, not a switch. Their recommendation there — advisory now, gate once the backlog clears — is the right call and I said so.

Tested against fifteen injected faults, one per rule: all fifteen refused, nothing written. Then a real click through the server and back, to confirm the stricter gate does not block legitimate writes; and the compare-and-set still refuses a stale click.

**A rail fired during this turn, correctly.** Two test clicks left `todo.json` modified while `tools/todo.py` was also mid-edit, and the background push refused with "tools/todo.py modified in the docket clone; commit or discard them first" rather than publishing a half-finished writer. The test writes were then discarded rather than published — D.3.5 ended where it began, so no fake activity is in the record.

### Standing state

Data at rev 38, valid, 0 of 37 complete. D.1.1 and D.1.5 due 2026-09-18. Clone clean and in sync, server pull loop current, published page live.

Prior turns: the peer's fuzzy-match rule applied inward, closing a read-back gap in `push()` (handoff-035); the reset-over-unpushed-commit bug (handoff-034); Sep 18 confirmed (handoff-033).

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-035-docket.md
**Model:** Opus 5. **Goose turn** — an audit that found nothing, and a validator that now keeps it that way.

## Next action (the one thing)

**Luke opens the published page on his phone, adds a fine-grained token, and clicks one status.** The last unproven inch of the write path, and still the only thing outstanding here.

## Files

- Live page, laptop: http://localhost:8642/docket.html
- Live page, anywhere: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/todo.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-035-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-036-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-480-docket.md
