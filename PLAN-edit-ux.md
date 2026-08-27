# PLAN — Edit UX v2 (merged: Claude + Codex, 2026-08-26)

*Inputs: PLAN-edit-ux-claude.md (written blind) and the Codex independent plan
(archived in ../codex-design-2026-08-26.txt). Convergent spine adopted;
disagreements flagged for Luke, not smoothed over. Mockup: /mockup.html.*

## The spine (both plans agree — build this)

1. **Edit entry, unmissable.** Desktop: a gold **✎ Edit campaign** pill in the
   header top-right, sticky. Phone: a fixed bottom-right labeled button (52px,
   text not icon). Active state reads **Editing** and the draft bar rises. The
   footer link stays as a secondary door.
2. **What's editable vs locked.**
   *Editable (campaign):* status events (submitted/selected/not selected/
   withdrawn/screened/nominee/winner + date, fee, award, confirmation), add
   festival (quick-capture → Needs research; full form → target), promote /
   rule out / restore, tier, notes (public-safe), key dates, premiere states.
   *Locked (research):* names, locations, categories, festival dates,
   submission windows, published fee schedules, qualifying paths, links,
   why-prose, sources. Locked fields show a 🔒 + "Verified Aug 25" stamp.
   *Escape hatch:* **Suggest research correction** — requires a source URL,
   updates lastChecked, never a casual inline edit. (Codex's version adopted
   over Claude's bare overflow-editor.)
3. **Status-first row (desktop).** Summary row: **status rail (6px, status
   color)** · big status pill + event date · festival (name 18px, loc/cat
   under, tier mark) · deadline countdown (large, tabular) · **[Official site ↗]
   [FilmFreeway ↗] buttons (44px, always visible)** · chevron. The why-prose
   and locked research move into an **expandable detail row** — the 9-column
   sprawl dies. In edit mode the status pill becomes the control and offers
   the CONTEXT-AWARE next step (Claude): not-submitted → [Mark submitted];
   submitted → [Selected]/[Not selected]; selected → [Won…]/[Screened];
   "More…" for the rest.
4. **Mobile card.** Status banner across the top (status color, tappable in
   edit mode = "Change status") · name 20px · deadline hero ("6 days left",
   28px) with exact date + fee under · two 48px link buttons side by side ·
   "View details" row → bottom sheet. Tap targets ≥44px everywhere.
5. **Status color law.** Muted = not submitted · gold = submitted/awaiting ·
   green = selected/screened · red = not selected · purple = needs research ·
   withdrawn = muted+strike · **winner = green + gold ★** (never a new color).
   Every color paired with a label. Deadline urgency is TYPE SIZE, not a second
   red system (red only when overdue-but-actionable).
6. **Timeline gains campaign state.** Event markers on bars: gold dot at the
   submission date · green diamond at selection · small red tick at
   not-selected. Decided/closed bars recede (opacity + desaturation, existing
   pattern). Windows stay tier-colored.
7. **Flows at 4 phone taps.** Mark submitted: Edit → row status → Submitted
   (today prefilled) → Publish. Decision: same shape; selection reveals award/
   screening/premiere fields IN THE SAME SHEET (no modal cascade). Add
   recommendation: Edit → + Add → name/link/why → lands purple in Needs
   research, never auto-target.
8. **Tiles become controls** (Claude): tapping applied/accepted/rejected/
   pending filters the list and scrolls; maybes opens the not-vetted fold.
   Plus a **thin progress meter** under the tiles: open targets submitted vs
   total (the funnel, in one line).
9. **Refuse list (union of both):** no kanban · no editable research mega-form
   · no tiny text links or links behind "details" · no 9-column table on
   phones · no color-only status · no raw system words in UI (no "stage",
   "disposition") · no mandatory review screen · no modal chains · no
   auto-promotion of recommendations.

## Flagged disagreements (Luke decides; current build keeps his ratified calls)

- **Tier row tints.** Codex: drop tints, tier as a small dot only — status
  should own row color. Luke ratified the tints (Aug 25). KEEPING TINTS; the
  status rail rides the left edge alongside. Say the word to go Codex's way.
- **The 8 tiles.** Codex: replace with a Targets → Submitted → Pending →
  Selected → Wins pipeline. Luke specified the 8-tile grid. KEEPING TILES;
  the pipeline ships as the thin progress meter instead.

## Deferred (plan, not this build)

Per-festival "next action" + reminder-date fields (schema addition — worth it
at first selection) · toast-with-undo after quick actions (draft bar already
covers undo) · pending-corrections queue UI beyond the source-URL requirement.

## Build order

1. Mockup (/mockup.html) — Luke reviews the markup. ← THIS TURN
2. On his notes: implement rows/cards/edit entry/locked-fields (1 session).
3. Timeline markers + tile-filters + meter (half session).
4. Codex verification pass, fix, ship.

## Addendum — the festival sheet, v2 (2026-08-26 evening)

Luke graded the first detail view 10–20%: "the important screen — think macOS."
Redesigned as a state-adaptive sheet, marked up at /mockup-detail.html:
header wears the status (wash + pill), hero states the one current fact
(countdown / awaiting / screening date / award), ONE primary action or a
segmented next-step pair, two link buttons, then grouped panes — Campaign
(timeline of events + notes, designed empty state) and Research record
(locked, Verified stamp, correction-with-source). Six header states specced;
motion: bottom-sheet spring on phone, 200ms scale-fade on desktop, single
250ms cross-fade on status change, reduced-motion fallbacks. This sheet
supersedes the expandable-row detail from section 3 of the spine.
