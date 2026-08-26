# PLAN v2 — The editable board (reconciled after cross-family review)

*2026-08-26. Supersedes PLAN-editable-board.md. Reconciles Claude's draft with the
Codex adversarial review (verdict on v1: UNSOUND — event ledger, phone-first,
token security, publish semantics, auditability). This is the build spec.*

## Verdict handling

All five of Codex's required changes are adopted. Deviations from Codex noted
inline with reasons. Scope for BUILD 1 is marked; everything else is backlog.

## 1. Data model — `data.json`, schema v2 (BUILD 1)

- `schema: 2`, `updated` stamp. Validation function runs before render AND before
  publish; a failed validation never renders empty sections or commits.
- **Stable ids** (slugs: `sundance-2027`). Festival + year = edition; next year's
  edition is a NEW record (Codex's edition point).
- **Event ledger per festival** replaces any status field:
  `events: [{type, date, note?, fee?, currency?, tierUsed?, award?, link?, confirmation?}]`
  with `type ∈ submitted | withdrawn | selected | not_selected | screened | nominated | won`.
  Lifecycle state and every counter DERIVE from events. Submission date and
  decision date coexist. `won`/`nominated` carry `award` (name required).
- **Vocabulary** (Codex's filmmaker-native set, adopted): chips read
  "Submitted", "Official Selection", "Not selected", "Withdrawn",
  "Screened", "Winner — <award>". Dashboard tile labels stay as Luke set them
  ("applied/accepted/rejected/pending") — flagged to Luke for optional rename,
  not silently changed.
- **The whole funnel materializes**: all 117 researched festivals live in the
  file — `disposition: target | bench | out` (46 / 57 / 14, from the research
  JSON). Counters become auditable; the bench becomes visible.
- **Provenance on every deadline**: `estimated`, `lastChecked`, `source` (URL).
- **Fees**: researched `feesText` (display) stays separate from actual paid
  amounts, which live on `submitted` events (`fee`, `currency`, waiver as fee 0 +
  note). Total-spent derives from events only.
- **Premiere ledger**: `premieres: [{id, label, state: available|reserved|spent,
  byFestivalId?, date?, note?}]` seeded with world / international / North America
  / US / LA / NY / Atlanta / France-screening flag. Manual state changes in edit
  mode; selecting or screening prompts "does this reserve/spend a premiere?".
- Authority rule: structured fields are authoritative for anything counted,
  plotted, or dated; prose (`why`) is commentary and may not carry unique facts
  about dates or money. (Codex's one-source-of-truth objection, resolved by rule
  rather than by normalizing all prose.)

## 2. Read path — resilience (BUILD 1)

- `index.html` fetches `data.json?ts=<now>` (cache-bust). Fallback chain:
  fetch → localStorage last-known-good (rendered with a visible STALE banner +
  its date) → embedded snapshot in the HTML (same banner) → explicit error state
  with Retry button. No path renders blank sections.
- Old-HTML/new-schema mismatch: `schema` checked; too-new data → stale-snapshot
  render + "reload for the new version" notice.
- Viewport meta tag added (missing today — Codex catch).
- **Mobile cards**: below 720px the dream list renders as cards (deadline,
  status chip, fee, next tier) instead of the wide table; research detail behind
  a tap. Timeline/heat map stay horizontal-scroll panels.

## 3. Read-path features (BUILD 1)

- **Search** across name, city, country, category, path, notes — filters table,
  cards, and bench together.
- **Filter chips**: All · Submit next (open + not submitted, deadline-sorted) ·
  Closing ≤30d · Submitted (awaiting) · Selections · Not selected · Bench ·
  Ruled out. Sort toggle: tier (default, Luke's spec) ⇄ deadline.
- **Selections & Awards strip** under Key Dates, hidden until the first
  selection: festival · result · award name. Text + tier color only — never
  imitation laurel graphics (Codex rule, adopted).
- **Recent activity**: last 5 events, derived, with dates.
- **Wins surface in the dashboard**: "accepted" tile's detail line shows
  "· N wins" when nonzero (grid stays 8 — Luke's even-grid law).
- **Bench section**: searchable one-liners (name, place, fit note, likely
  deadline) + per-row "Promote to target" / "Rule out" (edit mode only).
- **Links**: official site + FilmFreeway on every record that has them.

## 4. Edit mode (BUILD 1)

- Entry: `?edit` URL (bookmarkable) + a discreet "Edit board" footer link.
  No triple-tap (gesture conflicts — Codex).
- **Quick-update sheet, phone-first**: search → pick festival → one-tap action
  (Submitted / Selected / Not selected / Withdrawn / Screened / Won…) → date
  defaults to today, fee prefilled from the record's cheapest current tier where
  parseable → optional note → stage. Three taps + typing for the common case.
- **Quick-capture inbox** (Codex adopt): name + link + who recommended + one
  line → lands on the bench as `disposition: bench`, `lastChecked: null`.
  Full add-festival form exists for research-grade entries.
- Field edits: deadline, window, fees text, tier, festival dates — tap-to-edit
  with per-field validation; invalid or empty required fields block staging with
  an inline message.
- **Draft model**: staged changes live in localStorage keyed with `schema`,
  `baseSha`, and timestamp; a visible draft bar lists staged changes with
  per-change discard (undo before publish). Storage wrapped in try/catch;
  the bar carries "drafts live in this browser only and Safari may clear them
  after ~7 days of no visits — publish, don't hoard" (Codex honesty, adopted).
  Drafts do not roam between devices; the UI says so.
- Editing raises visual intensity ONE step (edit affordances in existing status
  colors); publish-pending is the next step; calm returns on success.

## 5. Publish path (BUILD 1)

- GitHub Contents API PUT of `data.json` only.
- **Token**: fine-grained PAT, this repo only, Contents RW. Default storage:
  sessionStorage (gone on tab close). Explicit "remember on this device"
  checkbox → localStorage, with the shared-`*.github.io`-origin warning stated.
  "Forget token" button always visible in edit mode. Prompt text states: the
  token is only ever sent to api.github.com; never paste it anywhere else; and
  carries the revoke URL. 401 → clear token, re-prompt. (Deviation from Codex's
  "remove persistent storage": persistence stays as an OPT-IN with the warning —
  the user is one non-technical person and re-pasting is the abandon-risk;
  compensating controls below.)
- **XSS defense, the real one**: every data-derived string renders through an
  `esc()` helper (or textContent); zero raw interpolation of editable fields.
  CSP meta tag with `connect-src 'self' https://api.github.com` and
  `object-src 'none'` blocks exfil targets even though inline script stays.
- **Concurrency (Codex's 6-step protocol, adopted)**: baseSha captured at draft
  start; at publish, fetch current SHA; mismatch → conflict screen (draft kept):
  offer "reload latest + auto-reapply my staged event-adds" (safe: events are
  appends keyed by festival id) or manual review for field edits; PUT with
  agreed SHA; a further 409 re-enters the loop.
- **UTF-8-safe base64** (TextEncoder → bytes → btoa). (Codex catch — the data
  is full of € and em dashes.)
- **Honest publish status**: after commit — "Committed ✓ — going live (usually
  ~1 min in our measurements; GitHub says up to 10)". The page polls the
  cache-busted `data.json` until the live copy matches, then shows "Live ✓".
  Editor sees changes instantly (optimistic local render). Already-open
  readers see updates on their next load — no self-refresh promise.

## 6. Explicitly deferred (backlog, not BUILD 1)

`.ics` calendar export · CSV/PDF export · unified upcoming-work view ·
deliverables/task tracking beyond event notes · edition-rollover tooling ·
programmer-contact anything (Codex SKIP list adopted wholesale).

## 7. Build order & verification

1. Schema v2 + data extraction (incl. bench/out from research JSON) + validation
   + resilient read path + derived counters. Visual parity check against current
   board (screenshot/DOM diff).
2. Read features: search, filters, cards, bench, awards strip, links, activity.
3. Edit mode + drafts + quick sheet + inbox.
4. Publish path + token flow + conflict protocol (tested against the real repo
   with gh-authenticated API calls simulating a second device's conflicting
   commit; in-page flow tested with a mock transport, then live once with a
   throwaway commit).
5. Adversarial audit round (Codex, read-only, against the built code) + fixes.
6. Deploy; artifact snapshot (embedded data) republished as the private mirror.

Success = the director's month-1..10 scenarios from the Codex review each
executable on a 390px viewport without touching the wide table.

---

## Addendum — Codex round-2 conditions, accepted (2026-08-26)

Verdict: AGREE-WITH-CONDITIONS. All five adopted; resolutions frozen here:

1. **Schema & reducer frozen.** Events carry unique `eid`s. Lifecycle reducer
   (one function, used by chips AND counters): `withdrawn` if the latest
   lifecycle event is withdrawn; else `selected` if any selected; else
   `not_selected` if any not_selected; else `submitted` if any submitted; else
   none. `screened` is a flag on selected; `won`/`nominated` are recognition,
   listed with award names. Deadline tiers get structure:
   `tiers: [{label, date, amount, currency}]` (optional; feesText remains the
   display fallback). Key dates: `{id, label, date, endDate?, showDate, detail}`,
   editable. Bench leads may be incomplete: only `name` + `disposition` required.
   Fee totals reported PER CURRENCY, never converted. A quick action that sets a
   premiere stages its event-op and premiere-op together; one commit = atomic.
2. **Real records.** Bench/out materialize from `../research-2026-08-25.json`
   (117 sweep records with per-record sources — outside this repo, which is why
   the reviewer couldn't see it). Name-variant duplicates in the sweep are
   deduped during generation; the researched tile then DERIVES from actual
   record count. If dedupe lands under 117, the tile tells the truth and the
   delta is reported, not hidden.
3. **Operation-based drafts.** A draft is a list of ops `{opid, kind, target,
   payload, prev}`. Rebase replays ops onto latest: addEvent idempotent by eid;
   setField auto-applies only if the upstream value still equals `prev`,
   otherwise it becomes a manual-review item (keep mine / keep theirs); premiere
   ops conflict on upstream state change. 409 loops re-enter the same protocol.
4. **Publish poll.** `data.json` carries a `rev` uuid regenerated each publish.
   PUT targets branch `main` explicitly. Poll: 10s→15s→30s backoff, 5-minute
   cap, matching `rev` ⇒ "Live ✓"; timeout ⇒ terminal "Committed — still
   propagating (GitHub says up to 10 min)" with a link to the commit. No
   deploy-failure detection is claimed.
5. **CSP strengthened + honest copy.** `default-src 'none'` base with explicit
   script/style/font/img/connect/form-action/base-uri/object-src directives;
   UI copy states escaping is the primary defense and CSP narrows, not
   eliminates, exfiltration paths. Shared-github.io-origin risk stated in the
   remember-token opt-in.

Also resolved: asks / playbook cards / next-actions prose stay in `index.html`
as non-editable chrome (Codex's own SKIP: inline-editing every paragraph);
`data.json` owns everything counted, dated, or plotted — festivals (all
dispositions), events, key dates, premieres, rev. The ruled-out table derives
from `disposition: out`. The embedded HTML snapshot ages between index.html
touches; the localStorage last-known-good covers repeat visitors, and the
banner always shows the snapshot's date.
