# handoff-065-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5) — THE LOGLINE IS LOCKED.** Luke: *"i think lock this for now."* Nineteen generations, closed.

> In 1834 South Carolina, an enslaved man is forced to fight for spectacle. But with every victory, he must take the life of one of his own. He stumbles upon the burial ceremony of his fallen opponent, and finds it being held in the ancient Faith of their shared ancestors, who he must now face to decide whether he will kill again.

**62 words, 330 characters.** His wording, verbatim.

### What he changed from the version I recommended

| | B (offered) | Locked |
|---|---|---|
| Sentence 3 opening | "When he stumbles upon…" | "He stumbles upon…" — its own sentence, no subordinate clause |
| Word order | "his fallen opponent's burial ceremony" | "the burial ceremony of his fallen opponent," — ends on *opponent* right before the turn |
| Participle | "finds it held" | "finds it being held" — the ceremony is in progress; he interrupts it |

Two things must not be normalised by any downstream lane: **capital F on "Faith"** (dictated, flagged once, kept) and **"being" in "being held"** (deliberate — it buys present tense inside a past-tense sentence).

### Shipped

- `press/filmfreeway-page-v5.md` and `.docx` — v4 with the locked logline swapped in. The **whole logline is red**, because a word-level diff against v4 found no shared run of three or more words: it is a replacement, not a revision, and marking a stray "burial ceremony" black would have been false precision. The v4 logline is quoted beneath it so Jordan sees what it replaced.
- `press/logline-idea-box.md` — LOCKED banner at the top, Generation 19 at the bottom.
- Messaged **Electronic Press Kit** (`local_d9850ab4`) to fill EPK field 2.1, and **KOM FEST TASK LIST** (`local_583cd801`) that D.2.1 is unblocked. Neither file is written from this lane.

### Notes for whoever builds the next docx

Neither the `docx` npm module nor `python-docx` is installed on this machine, and there is no LibreOffice, so **there is no docx→PDF path here**. The v4/v5 docx were built by unzip → edit `word/document.xml` → rezip. Red is `C01E1E`; body ink is `171310`. XML well-formedness and zip integrity were checked; **the file has not been opened in Word by anyone yet.**

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-064-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**Send Jordan `filmfreeway-page-v5.docx`** — that is D.2.1, and four items queue behind his approval. Real clock starts **Sep 15**; the two live doors are SBIFF **Sep 18** and Aspen **Sep 25**.

Still open behind it: the synopsis is unpicked (three drafts, 96–101 words, recommendation C); the end-credit roll is untranscribed (unblocks six EPK pages); the messages to Yeo and the HoDs are drafted and unsent; and **the board still records 0 submissions against a real 30** — the FilmFreeway export has never been imported.

## Files

- Page draft v5 (docx, for Jordan): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/filmfreeway-page-v5.docx
- Page draft v5 (md): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/filmfreeway-page-v5.md
- Idea box, now locked: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/logline-idea-box.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-064-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-065-festival.md
