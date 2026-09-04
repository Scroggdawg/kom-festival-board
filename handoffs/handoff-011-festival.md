# handoff-011-festival

## Where we left off

**This session (Aug 26, 2026, 20:58):** Edit UX v2 EXECUTED and LIVE on Luke's approval — the festival sheet, status-first rows/cards, front-door edit button, timeline campaign markers — then Codex-verified (SHIP-WITH-FIXES, zero security findings) and every fix applied and re-verified.

- **Aug 26 20:58** — Final build live: fix bundle applied (4-tap flows restored via direct row actions + close-on-save; "Stage"→"Save"/"unpublished changes"; screened advances reserved premieres; premiere concurrency carries dates; screened-event hero; state-gated More actions; applied/pending tiles distinct; default-aware dirty guards on every close path; links open new tabs; withdrawn strike; Unresearched stamp for bench; desktop scale-in). Verification transcript archived.
- **Aug 26 ~20:30** — Edit UX v2 built and shipped: festivalSheet (state-adaptive header wash/hero/primary-or-seg/campaign timeline/locked research/provenance), renderRows/renderCards status-first, edit pill (header + fixed phone), tiles-as-filters + meter, gantt event markers. My own testing caught and fixed a render-time javascript:-URL hole before Codex ran.
- **Aug 26 daytime** — Sheet markup approved by Luke (handoffs 009–010).

**Direction we were going:** The board is feature-complete for the campaign's start. What remains is the real world: Sundance (deadline Aug 31 — 4 days), the AFI email, Luke's PAT for in-page publishing, wave-1 September fees, the next-ring raid toward ~150.

---

**Timestamp:** 2026-08-26 20:58 PDT
**Lane:** `festival`
**Continues:** handoff-010-festival.md
**Model:** Fable 5. **This turn was a goose with a Codex jury** — build, adversarial verify, fix, ship.

## What shipped (all live at scroggdawg.github.io/kom-festival-board)

- **Tap any festival → the sheet.** State-adaptive: countdown hero + one gold [Mark submitted] on untouched festivals; gold wash + [Official Selection|Not selected] pair when submitted; green wash + screening date + [★ Record an award|Mark screened] when selected; ★ award hero for wins. Campaign timeline with designed empty state; locked research pane (🔒 Verified stamp / Unresearched for bench) with correction-needs-source; provenance footer.
- **Rows and cards are status-first**: rail + pill + countdown + two always-visible link buttons (render-time protocol-filtered) + chevron. Nine-column table is gone. Phone gets banner cards + a fixed gold ✎ Edit campaign button.
- **The board tells the campaign visually**: gantt bars carry submission dots / selection diamonds / rejection ✕s and recede when decided; tiles filter on tap; a thin submitted-vs-reachable meter under the dashboard.
- Flows: Edit → row button → prefilled form → Save (closes, draft bar counts) → Publish. Four taps.

## Verification trail

Codex build audit: SHIP-WITH-FIXES, "no new HTML-injection path found" — all interaction-semantics issues, all fixed same session, syntax + live behavior re-verified in-browser. Archived: `FESTIVAL CAMPAIGN/codex-uxverify-2026-08-26.txt`. Deliberate deviations recorded in PLAN-edit-ux.md's outcome section (meter union math, pre-existing ≤30d red chip, non-sticky desktop pill, award fields one tap after selection, restore-from-ruled-out backlog).

## Open uncertainty

Standing: Luke's PAT (edit mode stages but cannot publish until pasted); Vercel import; PAFF ladder; AFI email; premiere assumption; College TV Awards window.

## Next action (the one thing)

**Sundance — deadline Aug 31, 4 days.** Submit, then record it: Edit campaign → Sundance's [Mark submitted] → Save → Publish.

## Files

- Live board: https://scroggdawg.github.io/kom-festival-board/
- Artifact mirror: https://claude.ai/code/artifact/5dadab1f-b512-47eb-a2b4-e04cc9d18ff5
- Verification: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/FESTIVAL%20CAMPAIGN/codex-uxverify-2026-08-26.txt
- Prior handoff: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-010-festival.md

file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-011-festival.md
