# handoff-009-festival

## Where we left off

**This session (Aug 26, 2026, 17:51):** Edit-UX redesign round — Claude and Codex wrote independent design plans, merged them, and shipped a review markup of the new features at **https://scroggdawg.github.io/kom-festival-board/mockup.html**. The live board is unchanged; the markup awaits Luke's notes.

- **Aug 26 17:51** — Markup live: front-door Edit button (desktop pill + phone fixed button), tappable tiles + progress meter, status-first rows (rail + pill + context action + link buttons + expandable locked research record with Verified stamp), phone cards with status banners and deadline heroes, timeline event markers (dot/diamond/✕). Merged plan in PLAN-edit-ux.md; both source plans archived.
- **Aug 26 14:46** — Widgets-first declutter (handoff-008).
- **Aug 26 earlier** — Editable ledger built + Codex-audited (handoff-007).

**Direction we were going:** Luke reviews the markup → on his notes, the build (est. 1.5 sessions) → Codex verification → ship. Meanwhile Sundance in 4 days.

---

**Timestamp:** 2026-08-26 17:51 PDT
**Lane:** `festival`
**Continues:** handoff-008-festival.md
**Model:** Fable 5. **This turn was ducks** — two independent plans, a merge, and a markup; nothing built into the live board.

## What the plans agreed on (the spine, in PLAN-edit-ux.md)

Unmissable labeled Edit button (never footer-only) · campaign facts editable, research facts LOCKED with 🔒 + Verified date + "suggest correction (needs source URL)" · status-first row: rail + big pill + context-aware next-step button ([Mark submitted] on open rows) · links as always-visible 44px buttons · expandable detail row replaces the 9-column table · phone card: status banner + deadline hero + thumb-width links · status colors (muted/gold/green/red/purple, winner = green + gold ★) with labels always · timeline event markers with decided bars receding · 4-tap phone flows · refuse list (no kanban, no color-only status, no modal chains, no raw system words).

## Flagged disagreements (kept Luke's ratified calls)

1. Codex would drop tier row-tints (status owns row color); Luke ratified tints Aug 25 — KEPT, flip on his word.
2. Codex would replace the 8 tiles with a funnel pipeline; Luke specced the tiles — KEPT, funnel ships as the thin progress meter.

## Open uncertainty

- Luke's markup notes gate the build. Everything else unchanged (PAT setup, Vercel, PAFF, AFI email, premiere assumption).
- Mockup verified: top-section screenshot + DOM checks (5 rows, 3 cards, 4 timeline rows, 13 annotations, no horizontal scroll); Browser pane died mid-scroll again, so the lower sections got DOM-only verification.

## Next action (the one thing)

**Luke: open the markup, mark it up.** (And Sundance — 4 days.)

## Files

- Markup: https://scroggdawg.github.io/kom-festival-board/mockup.html
- Merged plan: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/FESTIVAL%20CAMPAIGN/site/PLAN-edit-ux.md
- Claude plan: …/site/PLAN-edit-ux-claude.md · Codex plan: …/codex-design-2026-08-26.txt
- Prior handoff: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-008-festival.md

file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-009-festival.md
