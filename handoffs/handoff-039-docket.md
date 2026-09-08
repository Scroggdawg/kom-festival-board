# handoff-039-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** Luke asked for a dashboard homepage covering the campaign's surfaces. Built, and it is the homepage now. Four data corrections landed alongside it.

### The dashboard

`index.html` is a campaign dashboard reading all three files live — `data.json`, `todo.json`, `press/epk.json`. One tile each, with a headline number, a progress bar and three rows. Polls every 15 s published, 3 s locally, dims when a read goes stale, and reports per-source rev and write time in the footer. Stacks to one column on a phone.

| Tile | Reads |
|---|---|
| Festival board → `board.html` | 97 targets of 151 · next **verified** deadline · verified at the festival 1 of 97 · 8 premiere routes available |
| The Docket → `docket.html` | 0 of 37 · next unblocked D.1.1 · waiting on Jordan 3, master access 1, Yeo 1 · 3 items dated Sep 15 |
| Electronic press kit → `epk.html` | 11 of 49 fields · 11 sections · emptiest section · 38 left |

**The board moved to `board.html`, byte-identical** — verified with `cmp` against the previous commit before committing. Nothing 404s; the root URL now lands on the dashboard with the board one click away. One commit to revert. The festival lane was told at once, and told to edit `board.html` from now on.

**Two decisions worth keeping.**

The tile for the board shows the next deadline **verified against the festival's own page**, not the next date in the file, with "1 of 97" beside it. Showing the next raw date would have put Carthage JCC Sep 15 — sourced from a Malian news site, fee unpublished — at the top of the campaign's front page, which is the exact failure the other lane spent the day correcting.

**No colour encodes identity.** I tried the five section colours as tile accents and ran the validator instead of trusting my eye: they fail as a categorical set — violet against periwinkle is ΔE 3.2 deutan and 10.4 normal, well under the floor of 15. Tiles are told apart by their titles; the palette stays monochrome and the status colours stay reserved. That also settles the note carried since handoff-026 that the five section colours were never validated as a set. **They do not pass. Nothing should ever be colour-coded by them.**

### Corrections applied from the festival lane

That lane verified Sep 15 properly this time — IFFR's own film-entry page, late/final tier €70 ex VAT, 15 September 2026 17:00 CEST, which is 08:00 Pacific. It is a real door and the *first* one, ahead of SBIFF Sep 18.

- **D.1.1, D.1.5, D.2.1** → due **2026-09-15**.
- **D.1.5** retitled: "…the first doors are IFFR Sep 15, SBIFF Sep 18, Aspen Sep 25".
- **D.2.1** retitled off the stale `press/filmfreeway-page-v5.md` pointer — Luke reopened the logline after locking it, so v5 is superseded and v6 is not written. It now names the current draft generically; the version gets pinned when v6 lands.
- **D.5.1** — "deadlines incl. Short Shorts Sep 9" removed; Sep 9 was the pitch-competition deadline, inherited from the error corrected days ago.
- **Nothing dated against Carthage JCC**, which also closes Sep 15 but is unverified.

Data at rev 50, valid. The Docket page carries a back-link to the dashboard.

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-038-docket.md
**Model:** Opus 5. **Goose turn** — a homepage that reads all three surfaces, and the section palette finally tested.

## Next action (the one thing)

**D.1.1 — the discount emails.** Seven days to the first verified door. The homepage now says so without anyone opening a file.

## Files

- Dashboard: https://scroggdawg.github.io/kom-festival-board/
- Board: https://scroggdawg.github.io/kom-festival-board/board.html
- Docket: https://scroggdawg.github.io/kom-festival-board/docket.html
- EPK: https://scroggdawg.github.io/kom-festival-board/epk.html
- Dashboard source: https://github.com/Scroggdawg/kom-festival-board/blob/main/index.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-038-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-039-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-483-docket.md
