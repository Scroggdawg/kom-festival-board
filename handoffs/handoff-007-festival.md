# handoff-007-festival

## Where we left off

**This session (Aug 26, 2026, 14:38):** The board became an editable campaign ledger — planned WITH Codex, built, adversarially audited BY Codex, fixed, re-verified, and shipped to the live site.

- **Aug 26 14:38** — Final build live at https://scroggdawg.github.io/kom-festival-board/ after the full cross-family loop: plan v1 → Codex UNSOUND → PLAN-v2 → Codex AGREE-WITH-CONDITIONS (all 5 adopted) → build → Codex audit DO-NOT-SHIP (3 criticals) → all fixed → Codex verification SHIP-WITH-FIXES → residuals (integer-cent fees, stricter validation) fixed and pushed.
- **Aug 26 AM** — Sexy pass + editable plan (handoff-006).
- **Aug 25** — Research raid, board revisions, public launch (handoffs 001–005).

**Direction we were going:** The campaign now has its operating tool. Real-world work resumes: Sundance submission (4 days), the AFI email, wave-1 September deadlines — and the queued next-ring raid toward ~150.

---

**Timestamp:** 2026-08-26 14:38 PDT
**Lane:** `festival`
**Continues:** handoff-006-festival.md
**Model:** Fable 5. **This turn was a goose with a Codex jury** — Luke's explicit process: co-plan, build, adversarial audit, fix, present.

## What shipped

- **The editable ledger.** `data.json` (schema 2) holds the whole funnel — 113 festivals: 47 targets (S16 restored), 52 bench (now VISIBLE and searchable, promote/rule-out in edit mode), 14 ruled out (table derives from data). Per-festival event ledger with filmmaker vocabulary: Submitted / Official Selection / Not selected / Withdrawn / Screened / Nominee / Winner + award names, fees (cent-exact, per-currency totals on the applied tile), confirmation numbers, notes. Premiere ledger chips (world→city, available/reserved/spent) with nudges when a selection/screening is recorded. Selections & Awards strip appears at the first yes. Search + filter chips (Submit next / Closing ≤30d / status views) + deadline sort. Mobile: card view + phone-first quick sheet (search → tap action → today prefilled → stage). Quick-capture inbox for recommendations; full add-festival form.
- **Publishing** (the director's save button): stage changes → Publish → GitHub Contents API commit with a fine-grained single-repo token (pasted once; sessionStorage default, opt-in remember with honest shared-origin copy; Forget button). Single rebase loop: per-op prev checks, conflict sheet where "keep mine" rebinds to the reviewed value (no blind force), sha-race retries, commit link + live-poll with honest timing. Resilient read path: fetch → last-known-good → embedded snapshot → error+retry, never blank; stale banners; schema-too-new notice.
- **Cross-family record:** review transcripts archived in `FESTIVAL CAMPAIGN/` (director role-play, audit, verification). Verdict trail: UNSOUND → AGREE-WITH-CONDITIONS → DO-NOT-SHIP → SHIP-WITH-FIXES → residuals closed.
- Contents API mechanics verified end-to-end against the real repo from the CLI before the in-page flow shipped.

## Decisions + assumptions

- Counters now derive from records: researched shows **113** (the sweep's 117 included 4 name-variant duplicates — ABFF ×3, AFI FEST ×2 etc., now consolidated). The tile tells the truth.
- Tile labels still read applied/accepted/rejected/pending per Luke's spec; row chips use filmmaker vocabulary (Codex's point) — Luke may rename tiles anytime.
- Token model: opt-in persistence kept over Codex's removal preference (accepted by Codex round 2 given the threat model), with strict escaping + URL guards + honest copy as the real defenses.

## Open uncertainty

- **Luke's one-time setup:** create the fine-grained PAT (repo `kom-festival-board`, Contents RW, short expiry) and paste it on first Publish. Until then the edit mode stages but cannot publish.
- Vercel import still pending (two clicks at vercel.com/new); PAFF ladder, AFI email, premiere assumption, College TV Awards window all still open from earlier handoffs.
- Structured fee-tier arrays (`tiers`) exist in the schema but are unpopulated — feesText carries display; backlog.
- In-page publish has been tested with mocked transport + real-API mechanics from CLI; the first real in-page publish (with Luke's token) is the last unexercised step.

## Next action (the one thing)

**Sundance — 4 days.** Submit, then record it on the board: Edit board → Update → Sundance → Submitted → Publish.

## Files

- Live board: https://scroggdawg.github.io/kom-festival-board/ (edit: append `?edit` or use the footer link)
- Repo: https://github.com/Scroggdawg/kom-festival-board
- Artifact mirror: https://claude.ai/code/artifact/5dadab1f-b512-47eb-a2b4-e04cc9d18ff5
- Plan + reviews: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/FESTIVAL%20CAMPAIGN/site/PLAN-v2.md · codex-director-review / codex-audit / codex-verify (same folder, dated Aug 26)
- Prior handoff: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-006-festival.md

file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/HANDOFFS/handoff-007-festival.md
