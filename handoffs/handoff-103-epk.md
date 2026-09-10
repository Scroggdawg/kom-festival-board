# handoff-103-epk

## Where we left off

**This turn (Sep 9, 2026, Fable 5.1, ultracode on at Luke's word):** Luke asked for a much better cinematographer bio for himself, EPK field 5.3, and said to study what makes a DP bio stand out and to ask him about himself where needed. **Delivered: four candidate bios staged as options on 5.3, a readout with the claims-to-sources table and eight questions for him, and the field's value left untouched until he picks.** `press/epk.json` is at rev 21.

**Before this turn (handoff-102, the sibling session):** the EPK as an Illustrator project on the Drive, the sexy pass applied to kit and card, BRAND.md v0.1 draft awaiting Luke's ratification. That session is still working in this clone; its uncommitted files were left alone and this commit names its paths explicitly.

**Direction:** Luke picks a version (or swaps a sentence), answers the eight questions in the readout, then `epk.py set 5.3` takes the chosen text and the EPK rebuilds. The same package serves FilmFreeway, lukescroggins.com/about and a replacement for the 2015 actor bio still on his IMDb page.

### What was done

1. **A fact sheet from his own files, not from the old bio.** The two AFI application statements, the 2022 CVs, the four AFI cycle books, the KOM DP statement, his Google Sheet "DP Website Content Tracker" (his own curated credit list with directors and producers), lukescroggins.com/about, and his public IMDb credits. Every line tagged verified, website, or unconfirmed. The unconfirmed items were barred from the drafts.
2. **A 64-agent workflow** (`dp-bio-raid`, run `wf_953c35c1-a6e`): seven research sweeps read 217 real bios and guidance pages; one agent wrote a brief with a seven-criterion rubric and a 40-phrase banned list; eight drafters wrote from eight angles; each draft was split into claims and checked against the fact sheet, then scored by three judges (festival programmer, hiring producer and agent, Clean Bank copy editor); a synthesizer built the package; three refuters checked it through three repair rounds. All eight drafts beat both existing bios on every judge. The last refuter objections were to note text, not to the bios.
3. **Hand pass after the workflow.** Three items the refuters had held out for reconciliation were put back because Luke himself asserts them, and are flagged as questions: DAYS OF OUR LIVES (in both of his bios, not on his IMDb credit list), LE'DIRECTOR (four spellings across his files; the tracker's spelling used), and Ford Bronco and the U.S. Air Force as commercial credits (on his tracker, not on his site's client list). Every text then re-passed the mechanical checks: word bands, no banned phrase, no semicolon, dash or parenthesis.
4. **Staged, not set.** `epk.set_options` put the four candidates on 5.3 with keys `recommended`, `credits-first`, `craft-first`, `chronology`, each with a note on where it is for. The field's value is still the killerofmen.com text. `epk.py check` is clean.

### The recommended text (157 words)

Cinematographer Luke Scroggins shot KILLER OF MEN, his thesis film at the AFI Conservatory, for director Jordan Betine. The 1830s South Carolina drama was shot on the ARRI Alexa 35, on a farm, in a barn and on a soundstage. For director John Lavelle he shot the short KEEPING WARM, one continuous scene inside a minivan. His AFI cycle films are PLACENTA for director Japhet Velazquez, PROSPECT, a motorcycle-club crime drama, for Piper De Palma, and DEEP TISSUE, an action thriller, for Matthew Genecov. With director Ze'ev Waismann he shot LE'DIRECTOR, his AFI application film, and commercials for Ford Bronco, the U.S. Air Force and Banner Health. Before AFI he was camera utility and data manager on the feature FRESH KILLS under cinematographer Ben Hardwicke. He holds a BFA in Acting from Otterbein University and appeared on SWITCHED AT BIRTH, GENERAL HOSPITAL and DAYS OF OUR LIVES. He is from San Antonio and based in Los Angeles.

### What the research settled

| Finding | Evidence |
|---|---|
| Every credit is a unit: title, director, year | Format lists ("narrative, commercial, music video") stood in for credits in 19 of 45 DP bios read and in no director bio |
| Open on the current film, past tense, not on birthplace or school | Agents and programmers quoted saying they stop reading a stale or origin-led opener |
| Counts beat adjectives; repeat collaborators beat awards for an early career | Morrison's "eight Sundance premieres"; Prieto's "fourth film together" |
| One process fact per headline credit | Fraser, Prieto and emerging DPs all do it; it replaces every craft adjective |
| Acting as one clause after the credits, as fact | Every acting-to-DP bio read does this; one DP who claimed transferred skill later deleted the sentence. Bio B's last sentence was that error |
| Most festival surfaces print no DP bio at all | Sundance, Tribeca, Aspen, Clermont, HollyShorts carry a credit line only; the EPK bio is a post-selection asset a catalogue editor trims |

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-102-epk.md (the sibling session's) and handoff-101-epk.md
**Model:** Fable 5.1, ultracode. Goose turn: briefed by Luke's ask, executed with a workflow. Two rooms worked this repo tonight; explicit paths on every commit.

## Next action (the one thing)

**Luke picks the version for 5.3 and answers the eight questions** in `press/bio-luke-scroggins.md`. The FRESH KILLS credit string and the LE'DIRECTOR spelling are the two that change printed text.

## Decisions Luke owns

1. Which of the four goes into 5.3 (recommended, credits-first, craft-first, chronology), or a sentence swap.
2. Whether DAYS OF OUR LIVES stays, and whether to add it to IMDb.
3. Whether the KOM lighting line (hard side key, deep falloff, near-black shadows) describes the film's grade; a yes adds one sentence.
4. Whether to replace the 2015 actor bio on his IMDb page with the chronology text.

## Files

- Readout with all four versions, the questions and the sources: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/bio-luke-scroggins.md
- Local: file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20%28THESIS%29/FESTIVAL%20CAMPAIGN/site/press/bio-luke-scroggins.md
- The worksheet (5.3 now carries four options): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Fact sheet (session scratchpad; personal detail from the AFI statements stays out of the public repo): file:///private/tmp/claude-501/-Users-scrogdawg-BMF-Headquarters-Previous-Years-2025---SEW-TO-GROW-25-01-KILLER-OF-MEN--THESIS-/4458f851-4022-4f16-b1ff-ea435a23657d/scratchpad/luke-facts.md
- Full workflow result, 217 research examples with URLs, eight drafts, 24 judge reports: file:///private/tmp/claude-501/-Users-scrogdawg-BMF-Headquarters-Previous-Years-2025---SEW-TO-GROW-25-01-KILLER-OF-MEN--THESIS-/4458f851-4022-4f16-b1ff-ea435a23657d/scratchpad/bio-raid-result.json
- His credit list, the source of truth for DP work: https://docs.google.com/spreadsheets/d/197lIEfxVatKTlRBZL2QqOy2hWlav8WePVy2o-o31K7c/edit
- Drive HANDOFFS folder: https://drive.google.com/drive/folders/1PgS0k2_7m6W7GYdnXag-LXdfx6M21XkS
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-102-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-103-epk.md
