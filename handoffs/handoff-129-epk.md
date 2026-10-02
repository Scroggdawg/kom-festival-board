# handoff-129-epk

## Where we left off, newest first

1. **Mock-ups of BTS photos as the background on the last two pages (crew, page 11; thanks, page 12), 2026-10-02.** Luke asked to try the KOM Stage shots and Day 4 Soundstage 58 in place of the current grounds. They are in a separate Canva design, "MOCKUP Credits backgrounds (BTS) _ KoM EPK" (`DAHW0-KVvy8`, https://www.canva.com/d/thm-4Lj1Gvgdzh_), saved. It has 8 pages in crew/thanks pairs: Stage 1 (pp 1–2), Stage 5 (3–4), Stage 9 (5–6), Soundstage 58 (7–8). The master `DAHU6a7HKPs` is not touched.

2. **How the grounds were made.** Each photo is cover-cropped to 1800 × 2400 and blended into `#0b0806`. The blend strength was chosen so the brightest areas (p95) are no brighter than the grounds on the master today, so the credits stay as readable as now. The files are in `press/assets/derived/credits-bts/`:

   | Photo | Crop anchor | Crew alpha | Thanks alpha |
   |---|---|---|---|
   | Stage 1 | 0.5 | 0.14 | 0.11 |
   | Stage 5 | 0.40 | 0.26 | 0.21 |
   | Stage 9 | 0.5 | 0.23 | 0.18 |
   | Soundstage 58 | 0.60 | 0.21 | 0.16 |

   Stage 1 is a bright photo, so it comes out very faint. Stronger versions are easy to make if Luke wants the photo to read more.

3. **The 12 BTS photos Luke listed are already in the repo** at `press/assets/BTS/`:
   - KOM_Stage-1, 5, 9
   - KOM_Day4_Soundstage-58, 32, 13, 76, 10
   - KOM_Day3_TheFarm-119, 45, 46, 18

   These are camera originals, 4672–7008 px.

4. **Bypass permissions.** Luke asked why he can't select it. Per the Claude Code docs (permission-modes), cloud sessions offer only Accept edits, Plan and Auto, and bypass is not available there. The bypass setting applies to local sessions (desktop app on a local folder, or the CLI).

5. **Not done / for Luke:**
   - Pick a background, or none. When he does, swap the fill of the full-page rect on master pages 11 and 12, and update `canva/ops/epk-canva.json` p10-e01/p11-e01, which are now off by one page.
   - The open items from handoff-128 still stand: the B.E.S.T. laurel square, the kit, contract, STATE and worksheet page numbering, Drive laurel sharing, the Sep 27 edits, and the leftover mock-up designs.

---

**Timestamp:** 2026-10-02 · **Lane:** `epk` · **Continues:** handoff-128-epk.md · cloud session, branch `claude/admiring-keller-38qjll`.

## Files

- Mock-ups: https://www.canva.com/d/thm-4Lj1Gvgdzh_ (`DAHW0-KVvy8`)
- Grounds: `press/assets/derived/credits-bts/`
- BTS originals: `press/assets/BTS/`
- Prior handoff: `handoffs/handoff-128-epk.md`
