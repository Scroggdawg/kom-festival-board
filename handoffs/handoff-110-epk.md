# handoff-110-epk

## Where we left off

**This turn (Sep 10, 2026, Fable 5.1, ultracode):** Luke answered the six Canva decisions (Pro; fonts my call, right for the film not the reference; Canva becomes the master after the build; email killerofmenmovie@gmail.com; line breaks and editor-driving my call) and asked for infrastructure any account can execute or resume. **Built and pushed:**

| Piece | Where | State |
|---|---|---|
| Runbook, cold-start to share, with resume rules | `canva/README.md` (mirrored to Drive `00 PRESS/CANVA`) | done |
| Progress file any account resumes from | `canva/STATE.json` | current |
| Emitter: kit layout → Canva contract + flattened images | `tools/build-epk-canva.py` | runs: 11 pages, 405 elements, 22 images, 20 links attached |
| The contract | `canva/ops/epk-canva.json`, served by GitHub Pages (200) | current, epk rev 24 |
| Flattened images (ghosts and scrims baked, crops applied) | `press/assets/derived/canva/` 5.9 MB, served (200) | done; masters untouched |
| The Canva app (Apps SDK, React/TS) | `canva/kom-epk-builder/` | built from the official starter, typecheck and lint clean, reviewed by two skeptics against canva.dev, 17 findings applied or rejected with citations (`BUILD-REPORT.md`); never yet run inside Canva |
| Production email on page 3 | worksheet field **3.20** (rev 24), kit footer, kit and .ai rebuilt (`KillerOfMen_EPK_1544_10092026`) | done |
| Dev server entry | `.claude/launch.json` → `canva-app` on 8080 | running this session |

**Decisions recorded in STATE.json:** build in Libre Baskerville (apps cannot use uploaded fonts; a real-Baskerville swap on Pro is optional and Luke's licence call); editable reflowing paragraphs, tracked lines one element each; mailto shown as plain text if Canva drops it (the app already treats mailto as text, since richtext links document http(s) only); Luke's blanket OK to drive his editor at human pace.

**Blocked at the door of Canva itself.** Two Chromes are connected to the account; Luke chose the in-Chrome confirmation route and the Connect prompt timed out twice with no click. Nothing has run inside Canva: no Developer Portal app, no probes, no pilot.

---

**Timestamp:** 2026-09-10
**Lane:** `epk`
**Continues:** handoff-109-epk.md
**Model:** Fable 5.1, ultracode. Handoff number chosen by a gating existence test.

## Next action (the one thing)

**Luke clicks Connect in the Claude-in-Chrome prompt on the Chrome that is logged in to Canva.** Then runbook steps 3 and 4: create the app in the Developer Portal (Development URL http://localhost:8080, Preview; the Developer Terms click is his), and the three probes. Any account can do this from `canva/README.md` and `canva/STATE.json`.

## Files

- Runbook: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/README.md
- STATE: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/STATE.json
- The app: https://github.com/Scroggdawg/kom-festival-board/tree/main/canva/kom-epk-builder
- Build report: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/kom-epk-builder/BUILD-REPORT.md
- Emitter: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-canva.py
- Contract (served): https://scroggdawg.github.io/kom-festival-board/canva/ops/epk-canva.json
- Plan: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/canva-plan.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-109-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-110-epk.md
