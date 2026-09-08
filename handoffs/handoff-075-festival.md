# handoff-075-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** while waiting on Luke, verified the two September dates this lane has asserted all day. **One is wrong.**

### SBIFF Sep 18 is a fee tier, not a door

Verified on **sbiff.org's own submit page**:

> earlybird Aug 7 $50 (passed) · **regular Sep 18 $60** · late Oct 30 $70 · **FINAL Dec 2 $80**

**Missing Sep 18 costs $10 and loses nothing. SBIFF's real door is December 2.** This lane called Sep 18 a "live door" repeatedly today — the identical tier-vs-deadline error as Short Shorts Sep 9, made *after* adopting the rule against it. `provenance: official` set; feesText names every tier; the mistake is written onto the record rather than quietly fixed.

### Aspen Sep 25 could not be verified — recorded as a failed verification

Aspen Film's own site publishes **no deadlines**: `/our-festivals/shortsfest/` and `/submit-your-film/` both defer to FilmFreeway, and `filmfreeway.com/AspenShortsfest` returns **403** to automated fetch. Sep 25 has no first-party confirmation. The record's own feesText already reads *"$80 by Sep 25 · **$95 final**"*, implying a later tier — so Sep 25 may be a price step too. **`provenance` deliberately NOT set.** To resolve: a human with a FilmFreeway account reads the tier names off the Deadlines & Fees table. Luke has one.

### The near-term picture, corrected

| | Sep date | What it actually is |
|---|---|---|
| **IFFR** | **Sep 15, 17:00 CEST** | **a real final deadline** — verified first-party |
| SBIFF | Sep 18 | a $10 price step; real door **Dec 2** |
| Aspen | Sep 25 | **unknown** — unverifiable without a human |

**There is one hard door in September, not three.** Materially calmer than what this lane has been telling Luke, and it means the pressure on the screener (D.3.1 / D.3.3) is IFFR's alone.

Verified count **1 → 2 of 97**.

### The lesson, which is narrower than the rule I adopted

1. **SBIFF and Aspen both already carried "VERIFIED 2026-09-08" in their `why` prose**, written by this lane earlier today. The prose asserted a verification the structured data did not carry — and re-fetching showed the SBIFF claim was flatly wrong. **A verification that lives only in prose is not one.**
2. Three instances of one error shape in a day, and the rule adopted after the first ("cite deadlines only from a festival's own panel") did not prevent the second or third. The version that actually catches it: **a date is not a deadline until something names its tier.**

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-074-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**Does Luke have a file he can upload?** It decides whether IFFR — now the *only* verified September door — is reachable at all. Then the D.3.1 screenshot, which may make the Vimeo build unnecessary.

Also for Luke, and cheap: **open the Aspen FilmFreeway listing and read the tier names.** Automated fetch is blocked; he has an account.

## Files

- Board data: https://github.com/Scroggdawg/kom-festival-board/blob/main/data.json
- Page draft v6 (for Jordan): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/filmfreeway-page-v6.docx
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-074-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-075-festival.md
