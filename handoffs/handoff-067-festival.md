# handoff-067-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** the docket session refused a phrase I had been repeating — *"the real clock starts Sep 15"* — and asked what it referred to. It was right to. I had never said, and the answer turned out to matter.

### IFFR is real, verified, and seven days out

Checked against **IFFR's own film-entry page**, not a list scrape:

| Shorts tier (<64 min) | Date | Fee |
|---|---|---|
| Early | 15 Jun 2026 | €40 ex VAT |
| Standard | 31 Aug 2026 | €55 ex VAT |
| **Late / final** | **15 Sep 2026, 17:00 CEST** (08:00 PT) | **€70 ex VAT** |

- **Premiere:** world, international **or European**. ABFF and MVAAFF are both US, so European status survives — submitting does not spend it.
- **Students:** excluded **except** post-graduate (master) year. An AFI MFA thesis qualifies.
- **Portal:** direct to IFFR, not FilmFreeway.
- Not Academy-qualifying — prestige, not an Oscar path. Consistent with Luke's stated preference for a good run over Oscar-max.
- IFFR 2027 runs Jan 28 – Feb 7, colliding with Sundance.

Source: https://iffr.com/en/iffr-pro-submissions/film-entry

### Two corrections to my own record

1. **I have been incoherent about the doors.** I wrote "the clock starts Sep 15" and "the two live doors are SBIFF Sep 18 and Aspen Sep 25" in the same handoffs. If Sep 15 is a door it is the *first* door. Never reconciled; now reconciled.
2. **`feesText` on the IFFR record read "€85"**, a figure that appears nowhere on IFFR's page. Most likely €70 + 21% VAT = €84.70 — an **inference recorded as a quote**, the same failure mode as the Short Shorts Sep 9 error. Record now carries the real tiers, a `sourceUrl`, and `provenance: official`. One of the 73 cleared.

**Carthage JCC 37th also closes Sep 15 and is NOT verified** — its source is a Malian news site, not the festival, and its fee is "unpublished". Nothing should be dated against it.

### Walked back the dependency claim

I had said "four items queue behind D.2.1" repeatedly. Reading `todo.json` rev 43, the honest split is: **D.2.6** (completion date, triggers a DCP regen) and **D.2.7** (first-time flag) are genuinely Jordan's; **D.2.4** and **D.2.5** are bundled into the one ask but not actually gated — someone could do them today; **D.2.2** is a courtesy ask; **D.2.3** is gated on the end-credit roll, a different blocker. Told the docket its file-order strip is defensible and that a `due` date on D.2.1 does the work I was trying to get a dependency field to do.

Also told it D.5.1 still carries "Short Shorts Sep 9" in its item text — my error, inherited, never relayed when I fixed data.json.

### Held

`press/filmfreeway-page-v5.md` carries the superseded logline. Luke locked it this morning and reopened it hours later; nothing is settled. **Do not send Jordan v5.** The docket has been told.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-066-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**Luke: does IFFR get a submission by Sep 15?** ~€85 with VAT, direct portal, European premiere intact, thesis eligible. The practical blocker is a **screener link**, not the logline — the campaign Vimeo (D.3.3) does not exist and D.3.1 is "get YouTube access from Jordan." Note: I verified IFFR's deadlines and eligibility, **not** its form fields.

Then the logline, then v6, then D.2.1.

## Files

- IFFR record: https://github.com/Scroggdawg/kom-festival-board/blob/main/data.json
- Idea box, Gen 20: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/logline-idea-box.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-066-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-067-festival.md
