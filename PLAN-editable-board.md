# PLAN — The editable board ("the ledger pattern")

*Written 2026-08-26, lane `festival`. A duck plan: the plan is the interface — any model
should be able to build this cold. Status: awaiting Luke's go.*

## Goal

Luke can update the board from any browser — mark a festival applied / accepted /
rejected, fix a deadline, add a festival or a key date — and everyone holding the
public link sees the change within a minute. Zero design regression: at rest the
page looks exactly like today's board. The editor is invisible until summoned
(widget-mastery law 5: design for the resting state).

## Recommendation

**A self-editing static page.** Same repo (`Scroggdawg/kom-festival-board`), same
URL, no backend, no service to babysit. Three pieces:

### 1. `data.json` — one source of truth
Move every fact out of `index.html` into `data.json` in the repo: the festival
records, key dates, asks, researched/ruled-out constants. Two model upgrades while
extracting:
- Each festival gains `status: "none" | "applied" | "accepted" | "rejected"` and
  `statusDate`. The dashboard's bottom row and "pending" DERIVE from these — the
  parallel `CAMPAIGN` arrays die. One record, one truth.
- Key dates become an array (Luke said more are coming), each `{label, date,
  showDate: bool}` — the Sundance card shows its date, the Oscar-window card
  doesn't, per his spec.

`index.html` fetches `data.json` at load. Pages/Vercel serve both files; a data
edit redeploys nothing but bytes.

### 2. Edit mode — in the page, invisible at rest
Summoned by `?edit` on the URL (plus a triple-click on the H1 as the phone-friendly
door). Reveals:
- A status control on every dream-list row (applied / accepted / rejected + date).
- Click-to-edit on deadline, fees, window fields.
- "Add festival" and "add key date" forms matching the schema.
- Unsaved edits held in localStorage as a draft — closing the tab loses nothing.

Sexy constraints carried in from the playbooks: edit affordances take the already-
budgeted status colors (no new hues); entering edit mode raises visual intensity
ONE step, not to max (the intensity curve — headroom stays for the save-pending
state); a saved change animates once, 150–300ms ease-out, no pulses.

### 3. Save = commit
A "Publish" bar commits `data.json` back to the repo via the GitHub Contents API.
Auth: a fine-grained PAT scoped to this ONE repo, contents read/write only, which
Luke pastes once per device; it lives in his browser's localStorage and nowhere
else — never in the repo. The flow fetches the current file SHA before writing
(conflict guard), commits with a message like `board: Sundance → applied`, and
GitHub Pages rebuilds in ~30–60s (Vercel, once imported, auto-deploys the same
push). Everyone else's link updates itself.

**The free prize:** every status change is a git commit — the campaign's history
becomes a journal for free, renderable later as a timeline strip on the board.

## Security, stated plainly

- Worst-case token leak = someone can edit this one public repo; revoke in one
  click at github.com/settings/tokens. Nothing else is reachable.
- The data is already public by design (it IS the shared page). Nothing secret
  ever enters `data.json`.
- Anyone without a token sees a read-only page; `?edit` without a token shows the
  paste-token prompt and nothing else.

## Phases

| Phase | What ships | Size |
|---|---|---|
| 1 | Extract `data.json`; per-festival `status` model; counters derive; zero visual change; deploy | ~1 hour |
| 2 | Edit mode UI: status controls, field edits, add-forms, localStorage drafts | ~1 session |
| 3 | Publish via GitHub API: token onboarding, SHA conflict guard, commit messages | ~half session |
| 4 (later) | Campaign journal strip from git history; FilmFreeway deep links; per-festival notes | optional |

## Alternatives considered (and why not)

- **Claude artifact with runtime capabilities** (a page that saves new versions of
  itself): real, but it lives on claude.ai — not the one canonical sendable URL,
  and edits wouldn't flow to the GitHub/Vercel copy.
- **Decap CMS**: an OAuth app plus an /admin subsite to edit one JSON file — more
  machinery than the job.
- **Next.js + database on Vercel**: a standing service with real auth to babysit,
  for what is a single-editor ledger. Right answer only if/when several people
  must edit simultaneously.

## Decision needed

None blocking — "go" starts Phase 1. One optional call: if teammates should also
edit, each becomes a repo collaborator with their own PAT (two minutes each);
otherwise it stays Luke-only.
