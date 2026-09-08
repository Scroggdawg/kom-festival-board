# handoff-040-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** the festival lane checked the homepage swap, found three things it broke in their lane and fixed them, and asked me to record the colour finding where the colours are defined. Doing that turned up a worse problem than the colours.

### The palette, measured rather than eyeballed

Both palettes were run through the dataviz validator against this page's `#14213d` surface. **Both fail as categorical sets.**

| Set | Worst pair | Normal vision | Deuteranopia |
|---|---|---|---|
| Five section colours | violet `#a06ff0` ↔ periwinkle `#6f93f0` | ΔE 10.4 (floor 15) | **ΔE 3.2** |
| Four status colours | sky `#5fb3e0` ↔ not-started grey `#9aa3b8` | ΔE 8.1 | **ΔE 5.9** |
| Three *filled* statuses | green `#2bb673` ↔ gold `#e6a92a` | ΔE 17.0 pass | ΔE 7.6 warn |

Peach `#f2b8a0` is also under the chroma floor and reads grey.

**Two places on the page carried identity by colour alone**, and both are fixed:

- The block map identified its five rows by a coloured dot. Two of those rows were indistinguishable to a deuteranopic viewer. Every row now carries its section name.
- The blocks distinguished started, awaiting and complete by fill colour only. Each status now draws its own shape — the language the dial already used: **outline** not started, **half-filled** started, **diagonal** awaiting, **solid** complete. The dial itself was already safe: distinct sprite plus the word.

The finding is recorded in `todo.json` as `paletteNote`, with the measurements, so the next lane reaching for those colours meets the evidence before the validator. That closes a note left open since handoff-026.

### The worse problem, found by trying to record it

Writing that note, `push()` said "nothing to push" and the note was gone. `merge()` builds from the remote and copied only sections and items across, so **any top-level key this machine added vanished and the rev went backwards — silently, with a success-shaped result.**

Same class as the title-only edit that used to disappear, and the third time an unmodelled local change has been dropped without a word. Local-only top-level keys are now carried over; where both sides changed the same key the remote still wins, but the key is *named* in what `push()` returns rather than dropped in silence. Three cases tested: local-only key survives, both-changed reports the overrule, identical documents still report no change.

### From the festival lane

They verified `board.html` byte-identical against `91e6aecd^:index.html` themselves and confirmed the 1 of 97 count. They retargeted `tools/embed-snapshot.py` and `tools/heat-expand.py` to `board.html`, which surfaced a stale embedded offline snapshot still serving the pre-IFFR `feesText: "€85"`, rewrote `README.md` for four surfaces, and added a matching back-link to the board. Nothing was in flight on `index.html`.

Data at rev 52, valid, published.

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-039-docket.md
**Model:** Opus 5. **Goose turn** — a palette measured, two colour-alone encodings removed, a silent data-loss path closed.

## Next action (the one thing)

**D.1.1 — the discount emails.** Seven days to IFFR. Behind it, v6 of the page draft lands and I pin the version on D.2.1.

## Files

- Dashboard: https://scroggdawg.github.io/kom-festival-board/
- Docket: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth, including the palette note: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/todo.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-039-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-040-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-484-docket.md
