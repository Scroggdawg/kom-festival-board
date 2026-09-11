# handoff-112-epk

## Where we left off

**This turn (Sep 10, 2026, Fable 5.1):** Luke asked whether a new Claude account can open this and finish the Canva EPK to the same ability as this session. Answer given plainly: **not 100 percent, and here is exactly what closes the gap.** Work done to close as much as can be closed from here:

1. **Research committed.** The five lane reports, the 175 verification verdicts and the workflow's synthesis, which lived only in this session's scratchpad, are now `canva/research/`. The sexy-pass change list is `press/sexy-pass-changes-2026-09-09.md`.
2. **Runbook hardened for a cold account.** `canva/README.md` gained: push access and the Claude-in-Chrome extension pairing as prerequisites (the extension is signed in to one Claude account; a new account must sign it in before it can drive Chrome); `tools/requirements.txt` for the venv (`venv/` now gitignored); `npm ci`; and a section "What the first session knew that is written nowhere else" (nothing has run inside Canva yet, mailto handled as text, page order not guaranteed, the CANVA_APP_ID warning is harmless, fidelity accepted, Canva's Terms, the two-rooms rules).
3. **Fresh-clone test, passed.** A depth-1 clone of 8fe4d38 into an empty folder: sixteen required files present; venv from requirements; emitter reproduces 405 elements and 20 links; `npm ci`, `tsc --noEmit` and `npm run build` clean. Recorded in the runbook and `STATE.json`.

**What a new account cannot get from disk:** the eleven hours of live context in this session's head, which now matters only for debugging the first Canva run. Everything decided is in `STATE.json`; everything researched is in `canva/research/`; every SDK call and the doc it was checked against is in the app's `BUILD-REPORT.md`.

**What no account has done yet:** anything inside Canva. The Developer Portal app, the three probes, the page-3 pilot, the build, the export and the share are steps 3 to 9 of the runbook and will surface the things a type checker cannot.

---

**Timestamp:** 2026-09-10
**Lane:** `epk`
**Continues:** handoff-110-epk.md
**Model:** Fable 5.1. Handoff number chosen by a gating existence test.

## Next action (the one thing)

**Whichever account runs Canva: read `canva/STATE.json`, then runbook step 3.** Before that, Luke signs the Claude in Chrome extension in to that account and is logged in to Canva Pro in that Chrome.

## Files

- Runbook: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/README.md
- STATE: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/STATE.json
- Research: https://github.com/Scroggdawg/kom-festival-board/tree/main/canva/research
- The app and its build report: https://github.com/Scroggdawg/kom-festival-board/tree/main/canva/kom-epk-builder
- Requirements: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/requirements.txt
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-110-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-112-epk.md
