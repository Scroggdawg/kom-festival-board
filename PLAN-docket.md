# PLAN — the Docket: a dashboard for the campaign's to-do list

*2026-09-06. A plan, not a build. Three independent designs (cockpit-first, time-first, sparsest-possible) were produced against the doctrine playbooks and judged twice — once for doctrine compliance, once for Luke's eye. This is the blend. Where the two judges disagreed, the ruling and its reason are stated. Nothing here is built yet; the mockup in chat is a static frame drawn from the Sep 6 digest, not from a truth file.*

**Name:** "the Docket" is the placeholder — Luke's own word for the work list. He names it (see the questions at the end).

---

## 1. The one-frame idea

One number — how many days until the soonest date that still has unfinished work — one sentence beside it saying what is at bat, and either something is waiting on Luke or nothing is. Time is the story; the five lanes are the cockpit underneath it. Composed, not comprehensive: the festival board already draws every festival and every deadline; this surface draws only the work.

The five-second walk-in test it must pass: *what is happening* (the number and the at-bat sentence), *what it has cost* (done of total, with a named baseline), *is anything needed from me* (the ask card, top right).

---

## 2. Medium and truth

| Layer | What | Why this and not the alternative |
|---|---|---|
| **Truth** | `todo.json` at the repo root, beside `data.json` | One file, one schema, versioned in git, served by GitHub Pages. Not a database, not an artifact store (experimental on this account; not exercised live) |
| **Writer, phase 1** | `tools/todo.py` — a typed command-line tool; the only writer | Single-writer rule from the surfaces playbook. Writes a temp file then renames it; bumps `rev`; validates before writing; refuses a short title over 60 characters, an unknown lane, an unknown status, or a `rev` that changed since it read the file. Two `PreToolUse` deny handlers (`Edit` and `Write` on `todo.json`) stop Claude hand-editing the file |
| **Writer, phase 2** | `docket.html`'s edit mode, reusing the board's publish loop (`index.html` ≈ L5100–5160: fetch latest + SHA, rebase the staged changes with previous-value checks, conflict sheet, validate, PUT, poll until live) pointed at `todo.json` | Luke already operates this path on the board with his token. The `rev` field is the guard between the two writers |
| **Surface 1** | The in-chat widget, 680 px, rendered from `todo.json` each turn by `todo.py render` | Luke's preferred medium. It is a snapshot: no fetch, no storage, so it prints the word *snapshot* and two times (file written, widget rendered) and offers Refresh. Every button is a `sendPrompt` sentence Claude acts on with `todo.py`, then re-renders |
| **Surface 2** | `docket.html` on GitHub Pages, same zones, polling `todo.json` every 30 s with `cache: no-store` | Persists; works on the phone; no server to restart. Holds the previous render at 60 % opacity during a refetch; past 60 s without a good fetch prints `stale N m · last good HH:MM` |
| **Not used** | A localhost page as the shipped surface (dies with the app session); an artifact with `db`; a Publish button on the product; a Reset button (undo is a sentence in chat) | |

**Pushing.** `todo.py` commits and pushes to `main`, which is a deploy in effect. Luke's standing instruction for this repo — "always update to git rep" — has covered every push so far. The plan asks him to ratify that as a standing exception for `todo.json` (the doctrine repo has the same exception), or to require a per-action OK.

---

## 3. The truth file — `todo.json`

```json
{
  "schema": 1,
  "rev": 1,
  "updated": "2026-09-06T17:30:00-04:00",
  "updatedBy": "tools/todo.py",
  "source": "meetings/2026-09-06-joan-call.md §D–§E",
  "baseline": { "label": "since the Sep 6 call", "at": "2026-09-06T17:30:00-04:00" },
  "ladder": { "atBat": "D.1.1", "onDeck": ["D.1.5"], "inTheHole": ["D.2.1"] },
  "lanes": [
    { "id": "discount", "n": 1, "name": "Discount emails",    "timing": "today" },
    { "id": "profile",  "n": 2, "name": "Profile page",       "timing": "this week" },
    { "id": "logins",   "n": 3, "name": "Logins and hosting", "timing": "in parallel" },
    { "id": "epk",      "n": 4, "name": "EPK and assets",     "timing": "" },
    { "id": "ledger",   "n": 5, "name": "Ledger — the board", "timing": "" }
  ],
  "items": [
    {
      "id": "D.1.1",
      "lane": "discount",
      "short": "Email the nine festivals for a discount, before paying",
      "detail": "Email every shortlisted festival with a fee over ~$20, before paying. Template in press/discount-email.md",
      "owner": "Luke",
      "status": "not_started",
      "blockedOn": null,
      "due": "2026-09-09",
      "dueLabel": "Short Shorts Tokyo closes",
      "ask": false,
      "answer": null,
      "parts": [
        { "name": "Short Shorts Tokyo", "due": "2026-09-09", "sent": null, "replied": null },
        { "name": "Curta Cinema Rio",   "due": "2026-09-12", "sent": null, "replied": null }
      ],
      "ref": "§D.1.1",
      "history": [ { "at": "2026-09-06T17:30:00-04:00", "status": "not_started", "by": "seed" } ]
    }
  ],
  "asks": [
    { "id": "E.7", "title": "Confirm the colouring-window exchange is a favour for Joan's project, not a KOM task", "who": "Luke", "gates": [], "open": true, "ref": "§E.7" }
  ]
}
```

Rules the writer enforces:

- `status` is one of `not_started | working | complete` — Luke's three words. *At bat*, *on deck*, *in the hole* are positions in `ladder`, never a status. Exactly one `atBat`.
- `short` is authored once, at most 60 characters; `detail` is the digest sentence verbatim, one tap away. This is what removes every ellipsis from the surface.
- `blockedOn` is a person plus what, as text (`"Jordan — MFA earned or completing (E.2)"`), or `null`. Waiting on someone is not an ask.
- `ask: true` on an item, or an entry in `asks[]` with `who: "Luke"`, makes a card. Anyone else's question rides as `blockedOn` text on the item it gates.
- `parts[]` exists only on items that are lists of the same act (the nine discount emails); each part has its own date and `sent` / `replied` stamps.
- `ref` is the digest's own section number and prints beside the title, so the numbering is defined where it appears.
- Seed today: 37 items (5 + 9 + 6 + 8 + 9), 9 parts on D.1.1, asks for Luke = D.1.5 and E.7. Blocked from the digest: D.2.1 (Jordan's approval; E.2), D.2.8 (master access), D.3.1 (Jordan), D.3.4 (Yeo), D.4.1 (Jordan), D.4.7 (Jordan).

---

## 4. The six zones — the panel budget is six

Zones are fixed positions held across sessions; a reading changes, an instrument never moves. Widget: 680 px wide, 16 px padding, content 648 px, about 548 px tall at rest.

| # | Zone | Widget position | What it holds |
|---|---|---|---|
| 1 | **Clock** — the hero | Row 1 left · x 16–376 · y 16–116 | The day count (56 px) · one sentence · the since-line |
| 2 | **Ask card** | Row 1 right · x 392–664 · y 16–116 | The decision waiting on Luke; `+N more`; `No decisions waiting` when empty, same footprint |
| 3 | **Flight deck** | Row 2 · y 128–156 | AT BAT · ON DECK · IN THE HOLE, left to right |
| 4 | **Next 14 days** — the ruler | Row 3 · y 172–252 | A time strip with today drawn on it, one tick per date carrying undone work, a late band, a *then* tail |
| 5 | **Lanes** | Row 4 · five rows of 44 px · y 268–488 | Number · name · timing word · one mark per item · done / total · state word · nearest date |
| 6 | **Provenance** | Footer · y 500–516 | `Snapshot · todo.json rev 7 · written 14:12 · rendered 14:15 · Refresh` |

Reading order is the frame's asymmetry by placement: the clock (departure, lower-left of row 1) reads into the decision (resolution, upper-right), then time runs left to right, then the cockpit. On the phone the six zones stack in the same order; the ruler becomes a dated list with one bar per date on a shared scale (today at 40 % of the row width, bars grow right for future dates and left for late ones). On the laptop the clock and ask card share row 1, the ruler widens to 21 days, the lanes sit left with the flight deck as a vertical stack on the right, and the plain table view of all 37 rows sits below the fold as the accessibility relief.

### Zone 1 — the Clock

*What:* the number of whole days from today to the soonest date carried by an undone item or part. Today: **3** (Sep 9, Short Shorts Tokyo, discount email not sent). *Why this number:* it is the one value on the list that changes overnight without anyone touching the file; it is precomputed (the verdict, not the raw list); and the discount-before-paying rule makes the real deadline earlier than the festival's, so the surface does that subtraction for him.

Sentence beneath, 14 px: `Sep 9 · Short Shorts Tokyo closes · email not sent · ask before paying`. Since-line, 12 px: `0 of 9 emails sent · unchanged since the Sep 6 call`. The at-bat item rides in the flight deck directly beneath, so the number and the current piece sit within one glance without competing as two dominants.

Late flips to `N days late` with *late* as a reversed chip (ink on text). No dated work flips to `No dated work open` in the secondary ink. The column reserves 360 px so nothing reflows.

**A rule both judges asked for, kept:** when the digest's date and `data.json` disagree, the hero prints the disagreement. (Today's case — Short Shorts Sep 9 versus the board's Jan 15, 2027 — is already settled: FilmFreeway's own listing says *Next Deadline: September 9, 2026*; the board lacks that tier. The fix is D.5.1, importing FilmFreeway's deadlines. The rule stays because the next disagreement will not be settled yet.)

### Zone 2 — the Ask card

Cards only for decisions that belong to Luke. Today: D.1.5 (the no-reply rule, due Sep 9) and E.7 (the colouring window). Anatomy: kind line in 11 px caps (`YOUR CALL · DUE SEP 9`), the question in 14 px (two lines max), a typed answer field and Send. Where the digest names the options, two pre-shaped buttons sit above the field; where it does not, the field alone — the surface never authors his choices. Sort: soonest due, then oldest. The board's 3 px gold left rule appears in the developing state. In the critical state an overdue ask takes the hero slot with its field, so the thing the frame is about and the control that resolves it are one object.

### Zone 3 — the Flight deck

Three cells, Luke's vocabulary, one short title each in 13 px with the owner word. Promotion is explicit and in his words — a button on the item, never a drag. `order conflict: 2 at bat` if the file breaks the one-at-bat rule.

### Zone 4 — the Ruler

The picture that tells the story by position and length — the one drawn structure on the surface. Title states the count: `Next 14 days · 4 deadlines with work open`. Track 8 px across 544 px = 38.9 px per day, today at the left, gold 2 px today line. One tick per date carrying undone work (Sep 9, 12, 14, 18 today); labels alternate above and below when two ticks fall within 60 px; a hollow tick head means *not on board*. Late shows as a muted band from the late date to the today line — length, not colour. A *then* tail at the right lists dates past the window (`then Sep 25 Aspen · Sep 30 ×3 · Nov 1`). Tap a tick: the items and parts due that day, with Sent / Replied on email parts. The 14-day crop is declared by the title and the word *then*.

### Zone 5 — the Lanes

Five rows, Luke's order, never re-sorted. Per row: `1 Discount emails · today · ○○○○○ · 0 / 5 · not started · Sep 9 · 3 d`.

- **One mark per item**, in digest order, so a note can name a part ("lane 2, mark 4"): hollow ring = not started, half-filled ring = working, filled = complete, ring with a slash = blocked. Shape carries status; tone second; hue third and decided by the contact sheet (§7).
- **Count** in tabular figures. **State word** precomputed in this order: `complete` if all are; `waiting on <name>` if the first open item is blocked; `working` if any is; else `not started`. The lane holding the at-bat item shows its name in the brighter text token — no marker, no hue.
- **Date cell**: the nearest hard date among undone items with its runway, or `no date`. This is what keeps the seven dates visible at rest.
- Tap a row: the lane's items beneath it, one lane open at a time. Per item: the status word as the button (`○ not started` → working; `◐ working` → complete; complete has no action), the short title, owner or `waiting on <who>`, the date, `to bat`.

### Zone 6 — Provenance

Always present. Widget: `Snapshot · todo.json rev 7 · written Sep 6 14:12 · rendered 14:15 · Refresh`. Page: `checked 8 s ago · every 30 s · todo.json rev 7 (Sep 6 14:12)`. A widget older than 60 minutes at render time says so.

---

## 5. Escalation — three states, spent in tone

State is computed from the file and the clock, never stored. The steady state must not sit at maximum intensity; each step spends one more unit of tone and nothing of hue, so the climax has headroom.

| State | Trigger | What changes — and only this |
|---|---|---|
| **Calm** | Nothing undone due within 3 days; nothing late; no block older than 3 days | Hero figure in the secondary ink. Ticks 1 px. Ask card hairline border. No band |
| **Developing** | An undone item or part due within 3 days; or a block 3+ days old; or a lane whose timing is *today* with nothing complete | Hero figure steps to the primary ink. That one tick thickens to 2 px and its label brightens. Ask card gains the 3 px gold left rule |
| **Critical** | An undone dated item or part past its date; or a block past the date of what it gates | Hero reads `N days late`, *late* as a reversed chip — the single maximum-contrast element, the one rule-break on a held grid. The late band appears on the ruler. The lane row prints `late` in the same chip. The offending ask sorts first and takes the hero slot |

Today (Sep 6, three days to Sep 9, nothing sent) renders as **developing**. Sep 10 with Short Shorts unsent and D.1.5 undecided renders as **critical**. No red in any work state. Red is reserved for a fault of the surface itself — a stale page or an invalid file — which keeps red meaning *bad news* on both the board and the Docket.

---

## 6. Colour — measured, not reasoned

One contrast channel: **tone**, on the board's own greys — ink `#171310`, panel `#201a14`, panel-2 `#262019`, hairline `#362b1e`, muted `#7a705d`, text-2 `#a79b85`, text `#ede4d3`. The grayscale test passes by construction. **One hue at rest: gold `#e5a44c`**, meaning *today* and *needs you* — the two things the board already uses it for — on the today line, the ask rule and the AT BAT label. Gold never marks a lane, an owner or a status. The board's tier hues (blue, orange, green for dream, strong, worthy) appear nowhere: a festival name beside a tick is text-2.

Validator runs, 2026-09-06, dark mode against the board's panel `#201a14`:

| Set | Result | Consequence |
|---|---|---|
| Luke's trio — gold (yellow) `#e5a44c` · red `#e06a5e` · green `#5fc287` | **FAIL** — red↔gold ΔE 14.7 normal vision (floor 15); green↔gold 7.0 protan (warn band); gold and green above the dark lightness band | Colour cannot carry status alone. Shape and word first; colour third |
| The board's own status pair — open `#6fae86` · closing `#d96a55` | **FAIL** — green reads grey (chroma 0.088); 6.6 deutan | Not reused |
| The dataviz reserved status set on this panel | **FAIL** — red↔green 4.1 deutan | No four-colour status set passes on this surface |
| Strip ramp — muted track `#7a705d` · text-2 fill `#a79b85` | **PASS** on `#201a14` and `#171310` as a two-step ordinal ramp | The only validated fill on the surface |
| Contrast — gold 7.99 · text 13.65 · text-2 6.29 · muted 3.53 · red 5.24 · green 7.84 (all on panel) | All ≥ 3:1 | Muted is never text under 14 px |

Also on record from the panel: red already means *rejected / spent / danger* on the festival board, and green means *tier worthy* — so painting red for *working* would give red two meanings across surfaces the same person reads.

**Status colour at rest is decided by a contact sheet, not by argument.** Three renders of the same frame, varying only the lane marks: **(a)** tone only; **(b)** Luke's words — red half-disc for working, green disc for complete; **(c)** green glyph on complete only. He points. The measurements above print beside the sheet.

Before ship: re-run the validator on the final tokens against both surfaces and record the output in `data-visualisation.md` §7 (the filing rule).

---

## 7. Typography

| Where | Face | Rule |
|---|---|---|
| Widget | The host sans (Anthropic Sans) — web fonts are not loadable in a widget | Widths reserved identically to the page so nothing reflows between them |
| Page — numbers, body, the hero | Archivo (the board's body face) | Hero 56 px / 600 / proportional figures (64 on laptop, 48 on phone); counts and dates in tabular figures; 11 px floor, and only in text or text-2 |
| Page — section titles only | Fraunces (the board's display face) | `Next 14 days`, the five lane names. Never on a number |

No uppercase transforms except the 11 px kind lines; no italics; no letterspacing.

---

## 8. Interaction — each control answers one question the widget cannot precompute

Reads are in-widget and need no round trip: tap a lane (which items, who holds them), tap a tick (what is due that day), `+N more` (what else is waiting on me). Writes go through `sendPrompt` as complete sentences Claude acts on with `todo.py`, then re-renders. Hover carries nothing.

| Control | Where | Sends |
|---|---|---|
| Status word | expanded item | `Advance "<short>" (<id>) to working in todo.json` / `… to complete in todo.json` |
| to bat | expanded item · on-deck cell | `Move "<short>" (<id>) to at bat in todo.json; move the current at-bat item to on deck` |
| to on deck | in-the-hole cell | `Move "<short>" (<id>) from in the hole to on deck in todo.json` |
| Sent / Replied | an email part | `Log the discount email to <festival> as sent today in todo.json (part of D.1.1)` / `<festival> replied to the discount email — ask me what they said, then log it (part of D.1.1)` |
| Pre-shaped decision | ask card, only where the digest names the options | `Decision on <id>: <option>. Record it in todo.json and close the ask` |
| Send (typed) | ask card | `Answer for <id>, <short>: <typed text>` |
| Nudge sent / Unblocked | a waiting-on line | `Log that Luke chased <who> today about <short> (<id>)` / `<who> came back on <short> (<id>): clear the block` |
| Refresh | footer | `Re-render the Docket from todo.json` |

Not on the product: Publish (the writer pushes under the standing rule), Reset (a sentence), filters, search, sort, drag.

---

## 9. Freshness and trend

Three layers on every render. **State:** the hero, the ticks, the marks, the cards. **Trend, baseline always named:** the hero's since-line (`0 of 9 emails sent · unchanged since the Sep 6 call`, or `+2 complete since Sep 5 14:12`); a waiting-on line prints its age (`Jordan · 2 days · nudged Sep 6`); the done delta reads `+N since the Sep 6 call` until Luke names a new baseline (the file records it). No sparklines and no per-lane deltas until three days of history exist — a flat line would claim nothing happened. **Provenance:** two times on the widget (file written, widget rendered) because they are different facts, and the word *snapshot*; on the page, seconds since the last good poll and the interval.

Every number is computed from `todo.json` or `data.json`; nothing is typed in; a date the two files disagree on is shown as a disagreement.

---

## 10. The ugly states — designed before the happy path

| State | Treatment |
|---|---|
| Empty lane (all not started — how the file is born) | Hollow rings, `0 / 5`, no hue |
| Lane with no items | `no items` in text-2; row height kept |
| All blocked (EPK, drives not arrived) | Every ring slashed; `0 / 8 · waiting on Jordan`; no red — waiting is not overdue |
| Nothing at bat | `Nothing at bat` in text-2; one control, *Set at bat* |
| No dated work | Hero prints those words; ruler shows the today line alone; the tail still lists later dates |
| All 37 complete | Hero `All 37 complete · as of <time>`; every mark filled; `No decisions waiting`; calm — quiet, not celebratory |
| Three deadlines on one day (Sep 30) | One tick `Sep 30 ×3`; the three listed on tap |
| A date the board disagrees with | Hollow tick head; label suffix *not on board*; on tap: `board says …; digest says …; fix data.json` |
| Two items at bat | `order conflict: 2 at bat`; the file shown as untrusted until fixed |
| Longest titles (D.2.1 at 190 characters) | The 60-character short title, always; the sentence one tap away; no ellipsis anywhere |
| Stale page | Previous render held at 60 % opacity; `stale 2 m · last good 14:12`; values desaturated to text-2 |
| Invalid file | Title line names the defect; the page holds the last valid render; the writer refuses such writes, so this follows only a hand edit |
| Widget without web fonts | System sans, the same widths reserved |
| Reduced motion | Length changes swap instead of easing |

---

## 11. Build sequence — tiny first

| Step | What | Gate |
|---|---|---|
| 0 | `BRAND.md` for this project, written from the tokens `index.html` already uses (ink, panel, text, gold, Fraunces, Archivo) | Doctrine rule 13: no surface ships without one. Luke ratifies |
| 1 | Seed `todo.json` from the digest: 37 items, 9 parts, 2 asks, the ladder | Luke's yes on authored short titles and the ladder seed |
| 2 | `tools/todo.py` with validation, temp-then-rename, `rev`, commit; the two `PreToolUse` deny handlers | `todo.py check` clean on the seed |
| 3 | **Static proof** — the widget rendered from a fake file carrying the ugly cases (longest title, all blocked, empty lane, no dates, late). The **contact sheet**: three colour variants (a/b/c) of the lane row, plus the three escalation states. Luke points | His pick, by eye |
| 4 | The widget for real: `todo.py render` from `todo.json` each turn, every button wired to its sentence | Zero collisions at rest and expanded |
| 5 | `docket.html` on Pages, read-only, polling; then phase 2 — the edit path reusing the board's publish loop | Live on the phone; a publish round-trips |
| 6 | Motion, page only: 200 ms ease-out on value change; hold-at-60 %-opacity on refetch; reduced-motion swap | One moving thing per region |
| 7 | Validator record into `data-visualisation.md` §7 | The filing rule |

Never build the live surface live.

---

## 12. Deliberately left out

The $5,000 spend meter and fee ledger (the festival board's job; D.5.2 is the to-do to build it there). Festival dates with no to-do on them (the board draws those). Owner colours (five owners; the all-pairs cap is three; a word is exact). A 37-row Gantt (740 px, and 28 rows have no date). A percent ring (angle decodes worse than a unit strip). A month calendar (Sep 9, 12 and 14 collide at widget width). Per-lane trend ticks until there is history. Fraunces on the widget. A light theme (the board is dark by design). Push notifications (the page's stale state is the alarm). Emoji, taglines, empty-state copy with character.

---

## 13. Questions for Luke — only the ones that are his

1. **Predict before the contact sheet:** which status-mark treatment do you think you will pick — (a) tone only, (b) your red/green, (c) green on complete only? Name one now; the sheet will show the gap.
2. **The name.** "The Docket," or your word? And "flight deck" for the at-bat row — keep or rename?
3. **Short titles.** May Claude author 37 titles of 60 characters or fewer, with the digest sentence one tap away? And does the section number (`D.1.5`) print beside each title at rest, or only inside an expanded lane with a one-line legend?
4. **D.1.5's options** if a festival has not replied by its deadline: *pay the full fee* / *skip it this round* / a third? Name them, or say it stays free text.
5. **E.7** — the colouring-window favour: a card on the Docket, or not a KOM task at all?
6. **The ladder seed:** at bat D.1.1 (the emails). On deck: D.1.5 (the no-reply rule) or D.2.1 (Jordan's draft)? In the hole: the other, or D.3.1 (YouTube access)? Name the three.
7. **The done delta's baseline:** `since the Sep 6 call`, or a rolling `last 7 days`?
8. **Pushing.** May `todo.py` push `todo.json` to this repo without a per-action OK, as the doctrine repo does — a standing exception — or do you want to be asked each time?

---

## Plain-words glossary

| Term | Meaning here |
|---|---|
| Bullet strip / unit marks | A thin bar, or one small mark per item, showing done-over-total by length or count — not by a dial or a ring |
| Ordinal ramp | Two or more shades of one colour that read as an order (track → fill) |
| ΔE | The validator's colour-distance score; below 15 two colours are hard to tell apart even with full colour vision; 8 is the target under colour-blindness simulation |
| Tone / hue | Tone is light-versus-dark; hue is which colour. The plan spends tone first because the eye goes to brightness before colour |
| Escalation curve | The three designed states — calm, developing, critical — each one step louder, so the resting state leaves headroom for the alarm |
| `sendPrompt` | The widget's one way to act: it sends a sentence into chat as if Luke typed it; Claude does the work |
| `rev` | A counter in the file that goes up on every write; a writer that reads rev 6 and finds rev 7 must re-read before writing |
| `PreToolUse` hook | A rule the harness enforces before Claude uses a tool — here, "never hand-edit `todo.json`" |
| GitHub Pages | The free static hosting the board already lives on; a commit goes live in about a minute |
| Tabular / proportional figures | Digits of equal width (so columns align) versus natural width (so a big lone number does not look loose) |
| Hairline | A 1 px line in the board's faintest ink |

---

## Sources

Designs and verdicts: three design specs and two judge reports, 2026-09-06 (session scratchpad; the panel's method is in the handoff). Playbooks: `composition-for-data.md`, `living-infographics.md`, `widget-mastery.md`, `data-visualisation.md`, `the-beautiful-canon.md`, `claude-surfaces-2026-09.md`; `CONTROL_SURFACES.md`, `SHOWING_THE_WORK.md`, `WORKING_WITH_LUKE.md`. The dataviz skill's `choosing-a-form.md` and `palette.md`; its validator, run against the board's tokens. The board's own `index.html` for tokens and the publish loop. The press-lane tracker (`notes.json`) as the precedent for labeled parts.
