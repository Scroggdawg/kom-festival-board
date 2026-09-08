# handoff-045-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, duck):** no writes. The Sep 16 defect I flagged last turn is fixed at its source, verified forward, and nothing in `todo.json` needed changing.

### The defect was one field away from where I was looking

I had asked whether `close` means the final door or the next tier date. **It always meant the final door** — `board.html` says so in three places, including *"read top to bottom as the order the doors close."* I read the field correctly. That lane supplied the defect by setting `provenance: official` on SBIFF while leaving a **tier** date in the **door** field.

Fixed at source rather than papered over on my page:

- **SBIFF `close` 2026-09-18 → 2026-12-02.** The tier ladder stays in `feesText`, where the money question belongs.
- **Short Shorts `close` 2026-09-30 → 2027-01-15**, found sweeping for the same shape. That record contradicted *itself* — its own `feesText` named a Jan 15 2027 final. **Third correction to one record in a week**, and the previous fix moved it from one wrong tier to another. `provenance` correctly left unset, since the warrant is the record's own fee text and not a first-party read.

**Verified forward rather than trusted.** Simulating my tile: today Rotterdam Sep 15; on Sep 16 **SBIFF Dec 2**, a real door. Before the fix the same simulation gave SBIFF Sep 18. The lie is dead. One honest future state: after Dec 2 the tile reads "none verified yet", because only two targets are verified — that is the truth, and it clears as the backlog does.

### The rule became a test

Two checks now live in their validator: a structural error when `close` precedes a tier the record's own `feesText` explicitly dates, and an advisory flagging unverified records whose fee text says "final" or "late". **15 of 97 targets match** — Sundance, SXSW, Tampere, Atlanta, Flickerfest among them. A far better-shaped backlog than "73 lack provenance", because each entry names what to check.

**I reproduced their 15 exactly from `data.json`, and declined to put it on the homepage.** Re-deriving their rule in my page means two implementations of one rule, which is what `source` and `sourceUrl` cost us earlier today. Proposed instead: a flag on each record, which my tile reads. Then the validator and the dashboard cannot disagree, and the rule sharpens in one place.

They also shipped that check with a bug and caught it on read-back — it warned that SBIFF "may be a fee tier" for the one record just verified, because the test sat inside the provenance block without testing provenance. **A gate that cries wolf about the record it should trust teaches people to skim it, which is how the original error survived three rounds.**

Rev 63, valid, unchanged.

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-044-docket.md
**Model:** Opus 5. **Duck turn** — a fix verified forward, a number declined on principle.

## Next action (the one thing)

Unchanged and still nobody's but Luke's: **ask Jordan whether downloading is enabled on the YouTube link (D.3.1)**, which decides whether the campaign Vimeo must exist by Sep 15. Behind it, whether Luke has a file to upload at all.

## Files

- Dashboard: https://scroggdawg.github.io/kom-festival-board/
- Docket: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-044-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-045-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-489-docket.md
