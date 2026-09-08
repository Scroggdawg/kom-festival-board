# handoff-055-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** Coordination close-out with the Docket lane, and playbook material offered to Luke.

### The Docket lane's bug, recorded because it is the more useful half

Our two pushes landed within a minute of each other. That collision exposed a data-loss defect in its clone: a background pull every 20 seconds ran `git reset --hard origin/main` with **no check for whether the clone was ahead**. When its push was rejected by mine, the next tick deleted its unpushed handoff commit outright. Recovered from the reflog and verified byte-identical against the mirror before re-committing. Now fixed: any reset publishes what is ahead first, rebases once if the remote moved, and refuses to reset if it still cannot publish. Both paths tested, including against a repository rigged to reject every push.

It had been true since the clone was introduced and only bit because two lanes pushed inside the same minute — **which will keep happening**. My commits were never at risk; the reset only ever ran in its own clone.

**Symmetry worth noting:** my own failure this turn was the same species — writing destructively against a fuzzy match (`curta` → `curtas-vila-do-conde-35th`). Two lanes, one day, same class of bug.

### Playbook material offered to Luke

Three from the Docket lane, one from this lane, and a hook proposal. Filing is Luke's call; the doctrine repo is his.

1. **A list field is not a deadline.** A date is only real with the festival's own Dates & Deadlines panel behind it and the tier or category named beside it. Cost: many turns of wrong urgency.
2. **`reset --hard` inside an automated loop needs an ahead-check.** Otherwise the loop's period is the window for losing work.
3. **Label an inference with the fact that would overturn it.** Settled two disputes in minutes today rather than by argument. The most transferable of the four.
4. **Never write by fuzzy or prefix match against a keyed record** — match the full id, read back before committing. *(this lane)*
5. **Hook proposal:** `data.json`'s validator should refuse any `close` date on a record lacking a `source` URL and a named tier — converting rule 1 from a habit into something the file enforces. This lane's file; would build on Luke's word only.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-054-festival.md
**Model:** Opus 5. Coordination turn — no campaign material changed.

## Next action (the one thing)

**Luke: say whether any of the five get filed, and whether to build the validator hook.** Then the two things that need nobody: the end-credit roll and the ~100-word synopsis. Real clock: **SBIFF Sep 18, Aspen Sep 25** — Aspen gives about half off on request.

## Files

- Board data: https://github.com/Scroggdawg/kom-festival-board/blob/main/data.json
- One sheet: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk-one-sheet.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-054-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-055-festival.md
