# handoff-053-festival

## The correction

**I was wrong about the September deadlines, for many turns, and pushed the wrong urgency hard.**

The Docket lane refused to move a due date on my timezone reasoning and asked for confirmation. Going to get it produced the opposite answer: the date itself was wrong. Every date below is now read from the festival's own **Dates & Deadlines** panel on FilmFreeway, not from a list field.

| Festival | Sep date I was quoting | What it actually is | Real deadlines |
|---|---|---|---|
| **Short Shorts Tokyo** | Sep 9 | **"Pitch Comp. Final Deadline — 1 Category"** — the Short Drama Pitch Competition, for pitching a project. **Does not apply to a finished short.** | **Sep 30 early** · Nov 30 regular · **Jan 15 2027 final** |
| **Curta Cinema Rio** | Sep 12 | **Earlybird** price tier | Nov 20 · Dec 14 late · Jan 8 2027 extended |
| **Flickerfest** | Sep 14 | Early Bird was **Aug 14 — already passed** | Oct 14 |
| **SBIFF** | Sep 18 | **Official Deadline — real** | Oct 30 late |
| **Aspen Shortsfest** | Sep 25 | **Regular Deadline — real** (Earlybird was Jul 31) | Nov 13 |
| **SFFILM** | Sep 30 | EARLY — all films | Nov 11 |
| Cleveland · Florida | Sep 30 | Early price tiers | Dec 15 · Dec 9 |

**There is no hard door closing in early September.** The nearest genuine deadlines are **SBIFF Sep 18** and **Aspen Sep 25**.

### How it happened, recorded so it does not repeat

The nine dates came from a FilmFreeway **list** scrape, whose "Next Deadline" field reports whatever tier or category comes next without saying which. **`handoff-018` on Sep 4 identified exactly this trap** — *"handoff 017's September run conflated fee tiers with real deadlines… September is mostly a money deadline, not a door deadline"* — and then on Sep 7, in `handoff-043`, I resolved the Short Shorts discrepancy **in favour of the scrape over `data.json`'s stored Jan 15**, called it settled, and escalated it in every handoff since. The board's original date was right. I overwrote a correct record with a worse reading and then repeated it.

**Rule adopted: a deadline is only citable from the festival's own Dates & Deadlines panel, never from a list view's "Next Deadline" field.** The list field does not name the category or tier it refers to.

### Done this turn

- `press/discount-email.md` — recipients table replaced with verified dates and what each one actually is.
- `press/epk-inventory.md` — the clock note corrected.
- Messaged the Docket lane: **do not** move D.1.1/D.1.5 to Sep 8; move to **2026-09-30** (the real early deadline) or 2027-01-15. Its urgency treatment stays and will now point at true dates.
- Earlier in the turn it had already retitled D.2.7 to carry killerofmen.com, and shipped urgency marking on dated items using brightness and a rule rather than colour, since the four status colours and five section colours are both spoken for.

### What is actually urgent

Nothing tonight. The next real doors are **SBIFF Sep 18** (ten days) and **Aspen Sep 25** (seventeen days) — Aspen gives about half off on request, so the discount email genuinely wants to go out before paying either. Everything else in September is money, not access.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-052-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**Luke: the end-credit roll and the ~100-word synopsis — both need nobody, and now neither is racing a fake clock.** One message to Yeo clears six page-3 spec fields. The discount emails should still go out before paying, targeting SBIFF and Aspen first.

## Files

- Corrected recipients: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/discount-email.md
- One sheet: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk-one-sheet.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-052-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-053-festival.md
