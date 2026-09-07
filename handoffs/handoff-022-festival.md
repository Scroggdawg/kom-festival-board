# handoff-022-festival

## Where we left off

**This turn (Sep 6, 2026, Fable 5.1 — a duck turn on the model Luke set):** Luke read the digest, gave rulings, and asked for a plan — not a build — for "a beautiful sexy functional efficient dashboard of widgets" to track the campaign to-do list (not the festivals), divided by the digest's lanes, after reading the doctrine playbooks on data visualisation, Arnheim/Block composition, infographics and widgets.

### Rulings applied to the digest (committed `22ca0b6`)

- **KOM has only ever been 13 minutes.** The "19-minute cut for the longest time" on the call was Joan describing her own film (her Vimeo shows 19:12 → 15:57). The agents misattributed it; the digest §A, §C.9, §E.1, §G.10 and the page draft were corrected. §G.10 withdrawn.
- Completion date: Luke will set a 2026 date preceding the first acceptance (ABFF notified Apr 24, 2026) and regenerate the DCP/masters so metadata agrees. Recorded as his decision (§C.9, D.2.6, D.3.6); the honesty concern was raised once and not relitigated.
- YouTube link stays; new Vimeo links dilute it going forward. Student ID: redact the number. Student status: a student thesis; not an issue. Accounts: Luke owns and pays. Palawa: dropped. P7 placement: fine as drafted. Team line for the email: roots in Nigeria, China, India, United States — factual, no joke, sent by Luke as Luke. Approval model: Jordan approves the direction and scope once; Luke edits without per-word sign-off.
- Luke liked §G.2 and §G.5.

### The plan — `PLAN-docket.md` (committed this turn)

Read the shelf first: `data-visualisation`, `composition-for-data`, `the-beautiful-canon`, `living-infographics`, `widget-mastery`, `claude-surfaces-2026-09`, plus `CONTROL_SURFACES`, `SHOWING_THE_WORK`, `WORKING_WITH_LUKE`, the dataviz skill's form/palette references, and the press-lane `notes.json` precedent. Then a 5-agent judge panel: three designs (cockpit-first, time-first, sparsest) → two judges (doctrine compliance; Luke's eye). Judges split on the winner (sparse vs time) but converged on the hero, the asks rule, authored 60-character short titles, the single writer, and colour-by-contact-sheet. The plan is the blend.

**The plan in one line:** one number (days to the soonest date with unfinished work), one sentence (what is at bat), one ask card; a 14-day ruler that tells the story by position; five fixed lanes with one mark per item; tone carries everything, gold is the one hue, status colour is decided by a contact sheet. Truth in `todo.json`; single writer `tools/todo.py` with `PreToolUse` deny hooks; the widget as the per-turn snapshot; `docket.html` on Pages reusing the board's publish loop. Panel budget six. Build order: BRAND.md → seed → writer → static proof + contact sheet → widget → Pages → motion → validator record.

**Measured this turn** (validator, dark, on the board's panel `#201a14`): Luke's yellow/red/green trio FAILS (red↔gold 14.7; green↔gold 7.0 protan); the board's own open/closing pair FAILS; the dataviz reserved status set FAILS on this surface; the muted→text-2 strip ramp PASSES. Gold 7.99:1, text 13.65, text-2 6.29, muted 3.53. Recorded in the plan §6; to be filed in `data-visualisation.md` §7 at build.

**Settled without asking:** Short Shorts Tokyo's deadline — the judges flagged "Sep 9 vs the board's Jan 15, 2027"; FilmFreeway's own listing (scraped Sep 4) says *Next Deadline: September 9, 2026*. The board lacks the tier; the fix is D.5.1.

**Shown in chat:** a static mockup of the resting frame on today's data (six zones, 680 px) with the three colour variants beneath it, labelled as a mockup drawn from the digest, not a live render.

### Gaps found

- **No `BRAND.md`** in this project (doctrine rule 13). Plan step 0 writes it from the tokens `index.html` already uses; Luke ratifies.
- The board refetches on load and after publish; it does not poll. The plan adds a 30 s poll with hold-at-60 %-opacity on `docket.html`.
- Pushes to this public repo are deploys in effect; the deploy guard did not fire. Plan question 8 asks Luke to ratify a standing exception for `todo.json` or require a per-action OK.

---

**Timestamp:** 2026-09-06
**Lane:** `festival`
**Continues:** handoff-021-festival.md
**Model:** Fable 5.1. **Duck turn** — read, panel, plan, mockup. Nothing built; no data changed except the digest corrections.

## Next action (the one thing)

**Luke: answer the eight questions at the end of `PLAN-docket.md`** — starting with the prediction (which colour variant he thinks he will pick) and the name. Then the goose builds step 0–3 (BRAND.md, seed, writer, static proof + contact sheet) and stops for his pick.

## Files

- Plan: https://github.com/Scroggdawg/kom-festival-board/blob/main/PLAN-docket.md
- Digest (corrected): https://github.com/Scroggdawg/kom-festival-board/blob/main/meetings/2026-09-06-joan-call.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-021-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-022-festival.md
