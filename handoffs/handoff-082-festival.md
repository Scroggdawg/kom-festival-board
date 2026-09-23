# handoff-082-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5 — a duck, no build):** Luke asked how valuable
SCAD Savannah is, given `Killer of Men` is in the 2026 edition. Answered as a
readout widget; nothing in the repo was changed.

**Previous turn (handoff-081):** `press/joan-writing-notes.pdf` shipped — the
Joan call's writing notes isolated to one page, and two silences turned into
named unknowns.

## The finding that resolves an open field

`data.json` carries SCAD with `path: "unclear — festival markets itself as an
Oscar-season stop but does not appear on"` (the string is truncated in the file).
**It is resolved: SCAD Savannah is not Oscar-qualifying.** Checked against the
99th Academy Awards shorts qualifying list — 172 festivals, 57 of them US, and
Georgia is represented only by Atlanta Film Festival and BronzeLens. SCAD is
absent.

Caveat on the evidence: `oscars.org` serves the primary PDF behind an Akamai
403, so the check ran against the Indie Shorts Mag mirror of the 172-festival
list, not the Academy's own file. Mirror, not primary — worth one re-check
against the PDF from a machine that can reach it.

The festival's own "road to the Oscars" language is about the films it *screens*
(26 Oscar-nominated titles, 89 nominations in 2025) and the honorees it fetes.
That is not a qualifying award a short can win.

## Two discrepancies in the repo, both unfixed

1. **The ledger does not know we are in.** `data.json` has SCAD as
   `disposition: bench`, `events: []`. But `press/epk.json`, `press/epk-one-sheet.md`
   and `press/filmfreeway-page-v6.md` all list `SCAD Savannah 2026` as a laurel
   beside ABFF and MVAAFF, and `todo.json` D.2.5 treats it as a screening to
   fill in. The event ledger is meant to be the truth and it is missing a
   selection.
2. **The Aug 25 research says we missed the 2026 window.** `research/research-2026-08-25.json`
   records the 2026 cycle as closed and the film as not submitted. That
   contradicts the EPK laurel. One of the two is wrong and nobody has reconciled
   them.

## Numbers as verified Sep 8, 2026

FilmFreeway key stats: 65,000 attendance (SCAD's own 2026 release says 74,000+),
~2,800 submissions, 100 projects selected (3.6%), 20 awards. 29th edition,
Oct 24–31, 2026, Trustees and Lucas theatres. Notification was set for Sept 14,
2026. **DCP is the only accepted exhibition format and the filmmaker supplies
it** — an unbudgeted deliverable if it is not already cut.

Category structure matters for the DP thesis: `Student Shorts` is a separate
competition from `Narrative Shorts`. The 2025 Best Cinematography award went to
`The Singers` in the **professional** competition; the student sections took
Best Student Short and Best Student Animated Short. **Which section KOM sits in
determines whether the cinematography prize is reachable at all** — unknown, and
answerable with one email to Sheila Bolda, competition programmer.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-081-festival.md
**Model:** Opus 5.

## Next action (the one thing)

Ask SCAD which section `Killer of Men` is programmed in, and reconcile the
ledger — either record the selection event against `scad-savannah-film-festival`
and flip it off the bench, or strike SCAD from the EPK laurels.
