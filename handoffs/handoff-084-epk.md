# handoff-084-epk

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** Luke sent the credits spreadsheet. **The end-credit roll is in** — the unlock every handoff since 062 has been waiting on. **`press/epk.json` rev 13 · 34 of 49 filled.**

Numbered **084**, and the number is a story. I wrote this as 083 under the shared-counter rule and the push was rejected: **the other session had just pushed its own `handoff-083-epk.md`.** Same lane, same number, same minute. Theirs went first, so theirs keeps 083 and this is 084.

**The convention has a gap.** A shared counter fixes lanes colliding; it does not fix two sessions reading the counter at the same moment, because reading and claiming are separate steps. Cheapest fix, and I am not changing the README unilaterally: **push the handoff first, before the work commit** — the push either succeeds and claims the number, or is rejected and you take the next one. That is what happened here by accident, and it worked. Alternative if that is too fussy: add a short lane-instance suffix, `handoff-083-epk-a.md`.

Their 083 was preparation for exactly this file — they installed `openpyxl`, wrote a dump script, and set a watcher polling Drive and Downloads for the workbook. **The watcher may still be running and may still announce it.** It has already landed and is parsed; nothing more is needed from it.

Source: `2513 KOM Credits 11-5-SDnotes.xlsx`, third tab, **End Titles**. Archived at `press/credits/` so the fields stay traceable.

### Filled from the crawl

| | |
|---|---|
| `3.15` | Nine billed cast, in crawl order |
| `9.1` | Executive producers, UPM, both ADs, colorist, stunt coordinator, still photographer |
| `9.2` | Full cast plus fifteen extras |
| `10.1` | Full crew, about seventy names, grouped by department |
| `11.1` | Thirty thank-yous |
| `11.3` | AFI fellows and all four boilerplate paragraphs, verbatim |

**Two long-standing questions closed.** **Kenner's actor is Eric Pargac** — the slot has been empty since Sep 8. And the **still photographer is Jedidiah Woods**, which is the page 8 credit line handoff-070 flagged as missing; recorded in `8.1`.

**Two name corrections, made on the sheet's own instructions**, not my judgement: "DANILE KASSAR" carries the note *Daniel*, and "NIKITA MAKSIMCHIK" carries *Nikita Korshunov per contract*. Both appear again in the extras list marked *delete*, consistent with being billed as Spectators instead. Roles marked *combine and make plural* were combined; Thesis Mentor and Editing Advisor, both marked *Delete*, were left out — AFI's own instructions tab forbids faculty credits on a second-year thesis.

### What the credits did NOT settle — read this before quoting anything

1. **No sound designer exists anywhere in the document.** The whole post-sound block reads TBD: sound effects editor, sound editor, recordist, foley artist, foley mixer, ADR mixer. Set sound was Jacob Eliett with Day Wren on boom. `9.1` says UNKNOWN rather than guessing. The one-sheet has promised for weeks that the crawl would answer this. It does not.
2. **The director's name does not match itself.** The fellows list reads **Jordan Uwhubetine**; the poster, the billing block and every other credit read **Jordan Betine**. Legal name against professional name is the obvious explanation, but it is a guess. Nothing printed until Jordan says.
3. **The crawl is dated © MMXXV — 2025 — while `3.5` records completion as 2026.** Festivals read both. One is wrong, or the copyright is dated to creation rather than completion.
4. **Twelve crew positions are blank**, including location manager and property master, and the colour house is a placeholder reading "Picture Shop 1" through "Picture Shop 7".
5. **This is a working document, dated 11-5, with someone's notes in a side column.** It is not a locked crawl. Treat every name as needing one confirmation pass.

Smaller: the thanks list is not alphabetical, which AFI requires; Padma Chitrapu appears twice; "Tracey B" has no surname to sort on. The animal-welfare line carries the question *"Did you work with the Humane Society?"* and the crawl bills a **snake wrangler**, so an animal was on set and the American Humane wording needs checking.

### Answering handoff-083's open questions

That session listed things the credits should settle. They do:

- **Rajarajeshwari, not Rajeshwari.** The fellows list reads "Rajarajeshwari Ragampudi", agreeing with the poster and her own bio text against the website heading. Three to one; treat it as settled.
- **The plantation owner is credited as "Master Kenner"**, played by Eric Pargac. Both halves of that question are answered.
- **The final opponent is billed.** Kojo, played by Jamal Dennis, third in cast order, with Kojo's Master right after him. Whether he is a *principal* is a layout decision — the crawl does not separate principals from supporting, so `3.15` carries the whole billed list and says so.
- **Yeo is still not identified.** No one named Yeo appears anywhere in the crawl. You Wu is credited as editor and AFI Editing Fellow, so the guess is reasonable, but a name that never appears in the document is not evidence. Left unwritten, as they left it.

### The breakdown PDF was lying

Its two footer blocks still said "Transcribe the end credits" and "Build the Drive folders", both done. Rewritten: the left block now says what the credits answered and what they did not, the right block lists what is actually next. Stale per-field notes from the other session's spec fills were refreshed at the same time — display only, no data touched.

---

**Timestamp:** 2026-09-08
**Lane:** `epk`
**Continues:** handoff-083-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Ask Jordan two questions in one message: Betine or Uwhubetine, and who designed the sound.** Both block a page. Then pick the pictures — hero, page 8 mosaic, cast in character, credits still — and the synopsis. Still open from 082: Kenner is answered, but `3.17` press contact, `3.18` Instagram and whether "RE-RAW" is ARRIRAW are not.

## Files

- The credits source: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/credits/2513%20KOM%20Credits%2011-5-SDnotes.xlsx
- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/EPK-breakdown.pdf
- Handoff convention: `KILLER OF MEN/HANDOFFS/README.txt` on the Drive
- Drive press folder: https://drive.google.com/drive/folders/1utGEFQb5gDuUOC9JU7zvuslwRlwbRorx
- Prior handoff (the other session's, written the same minute): https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-083-epk.md
- The one before that: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-082-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-084-epk.md
