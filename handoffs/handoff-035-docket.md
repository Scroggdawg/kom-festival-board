# handoff-035-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** no data change. The festival lane's near-miss produced a rule, and applying that rule to my own writer found a gap worth closing.

That lane corrected four festival records by matching on a name prefix; `curta` also hit `curtas-vila-do-conde-35th`, an unrelated Portuguese festival, which took Curta Cinema Rio's date, fees and note. Caught on read-back and restored. Their rule: **never write by fuzzy or prefix match against a keyed record; match the full id and read back before committing.**

### Audited against this lane

| Half of the rule | Result |
|---|---|
| Fuzzy matching | **Clean.** Every id match in `tools/todo.py` and `docket.html` is exact equality — `it["id"] == iid`, `it.id === id`. No prefix, substring or startswith anywhere in a write path. The failure mode cannot occur here. |
| Read back before committing | **Gap, now closed.** `push()` wrote the merged document with a raw `open()` and committed it, bypassing the validation `save()` performs. A merge bug could have committed an invalid `todo.json`. |

`push()` now runs `check()` on the merge, writes, re-reads the file from disk, compares it against what was intended, and reverts rather than commits if either step disagrees. Tested with a merge rigged to return an invalid document: refused, file untouched, data still valid.

### Playbook

The festival lane put all three of my candidates to Luke, credited here, plus one of its own and a hook proposal for its own file. Filing is Luke's call; the doctrine repo is not either lane's.

### Standing state

Data at rev 38, valid, 0 of 37 complete. D.1.1 and D.1.5 due 2026-09-18, confirmed on both assumptions. Clone clean and in sync, server running from it, published copy live.

Prior turns: the reset-over-unpushed-commit bug found by being bitten (handoff-034); Sep 18 confirmed (handoff-033); the wrong deadline corrected at the root (handoff-032).

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-034-docket.md
**Model:** Opus 5. **Goose turn** — a peer's rule applied inward, one gap closed.

## Next action (the one thing)

**Luke opens the published page on his phone, adds a fine-grained token, and clicks one status.** The last unproven inch of the write path, and still the only thing outstanding in this lane.

## Files

- Live page, laptop: http://localhost:8642/docket.html
- Live page, anywhere: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/todo.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-034-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-035-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-479-docket.md
