# Claude's plan — the status-first cockpit (written before reading Codex's)

*2026-08-26. Luke's brief: edit must be obvious; enumerate what's editable; lock
research facts; make links prominent; better rows/cards; deliver information
visually, really sexy.*

## 1. Edit model

**Editable (the campaign):** status events — submitted / selected / not selected
/ withdrawn / screened / nominee / winner (+date, fee, award name) · add
festival (quick-capture → not-vetted; full form → target) · promote / rule out
· notes · key dates · premiere states.

**Locked (the research):** deadlines, submission windows, festival dates, fees
text, category, tier, the why-prose. These are verified facts, not campaign
state — casual edits corrupt them. One escape hatch, deliberately out of the
main path: a per-row ⋯ overflow → "Correct festival facts", carrying a warning
("research facts — edit only when the festival itself announces a change").

**Entry:** a persistent **✎ Edit** pill in the top-right of the header — always
visible, accent-bordered, sticky on mobile scroll. In edit mode it turns solid
gold **Done**, and the draft bar rises. The footer link stays as a secondary
door. Never again a footer-only entry.

## 2. The row and the card — status-first objects

- **Column order:** Festival · **Status** · Final deadline · **Links** · Where ·
  Festival dates · Fees · Path · Why. Status moves up to slot 2 and grows.
- **Chip states at rest:** "Not submitted" (muted outline — never a bare "—") ·
  "Submitted Sep 1" (gold) · "Official Selection" (green) · "Winner — Best
  Drama" (gold-filled) · "Not selected" (red) · "Withdrawn" (muted).
- **Context-aware next action (edit mode):** the row offers exactly the next
  lifecycle step as a real button — open+unsubmitted rows get **[Mark
  submitted]**; submitted rows get **[Selected] [Not selected]**; selected rows
  get **[Won award…] [Screened]**. One tap opens the prefilled sheet. The
  generic 7-button sheet remains only behind search.
- **Links as buttons:** two pills per row — **[Site ↗] [FilmFreeway ↗]** —
  visible at rest. Cards get a full-width button row. A missing link shows a
  muted [+ add link] in edit mode only.
- **Mobile card:** row 1 name + status chip · row 2 deadline countdown (big,
  tabular) + fee · row 3 link buttons · edit mode appends the context action
  full-width. Why-prose stays behind the existing details tap. All tap targets
  ≥44px.

## 3. Visual information delivery

- **Channel routing:** tier keeps hue on the row tint + mark; status owns the
  chip AND one new element — a thin **status underline on each timeline bar**
  (gold = submitted, green = selected, red = not selected). The Gantt then
  shows the windows AND the campaign's progress in one glance.
- **Tiles become controls:** tapping applied/accepted/rejected/pending applies
  that filter and scrolls to the list; the maybes tile opens the not-vetted
  fold. Pressed states so they read as buttons.
- **Wins get a ★** before the festival name in list and timeline — recognition
  at a glance, one glyph, no new color. The awards strip stays the celebration
  surface.
- **One trend line:** a thin progress meter under the dashboard — open targets
  submitted vs total, track drawn, count labeled. The campaign's single
  heartbeat (state → trend → provenance).
- Recent activity dates go relative ("3d ago").

## 4. The three flows, on a phone

1. **Mark submitted:** ✎ Edit → row's [Mark submitted] → sheet (today + fee
   prefilled) → Stage → Publish. **4 taps + optional fee tweak.**
2. **Record a decision:** ✎ Edit → row's [Selected] → date confirm → premiere
   nudge → Stage → Publish.
3. **Add a recommendation:** ✎ Edit → [+ Add] → name + link → Stage → Publish.

## 5. What not to do

No kanban/drag. No inline editing of research prose. No second status color
system. No value reachable only by hover or modal. No auto-scraped deadlines.
Not every cell tappable — only status, links, and ⋯.
