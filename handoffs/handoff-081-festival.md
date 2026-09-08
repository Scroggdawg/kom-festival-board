# handoff-081-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** Luke asked for the Joan call's writing notes — logline, statement, synopsis — isolated as a one-page PDF.

**Shipped: `press/joan-writing-notes.pdf`**, built by `tools/build-writing-notes-pdf.py` from `meetings/2026-09-06-joan-call.md`. Eight blocks: the governing sentence (§A), logline (§C.1), director bio (§C.2), director statement (§C.3), synopsis, wording rules elsewhere (§C.8, §C.12), how the writing gets approved (§D.2.1, §F.9), and why the notes are shaped as they are (§G.2, §G.3). Italics are verbatim; every block carries its section ref.

### Two things the extraction surfaced that were not in the brief

1. **The synopsis was never discussed on the call.** It appears **once** in the entire transcript — as one item in the §B.3 delivery-folder list, *"Synopsis, credits & director bio"*. Joan gave **no guidance on writing one**. Given it as its own block on the sheet so nobody attributes a synopsis rule to her. The three drafts in `press/synopsis-draft.md` came from somewhere else.
2. **The first-time-filmmaker box is ticked and contradicts the bio** (§C.10). That was filed under page settings; it is a writing note, and it now sits with the bio.

### A defect in the digest itself, fixed

**§D.4.5 read "Luke's producer bio."** Luke is the **cinematographer** — he corrected that on Sep 8 and it was fixed in `epk.json`, the one-sheet and the inventory, but **the meeting digest kept the error** and nobody had gone back to it. Corrected, with the correction noted inline.

### Layout, since the first two attempts were wrong

The subtitle ran off the right edge unwrapped, and the column split cut at the first block past half the total — four tall blocks left, four short right, a third of the page blank. **The split now minimises the TALLER column** (that is what caps the body size) and the size auto-fits to fill one page; it landed at **9.0pt**. Rendered at 150dpi and read before shipping, which is how both faults were caught.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-080-festival.md
**Model:** Opus 5.

## Next action (the one thing)

Two questions with Luke, both gating the only real deadline:

1. **Does he have a file he can upload?** Decides whether IFFR Sep 15 is reachable at all.
2. **IFFR — yes or no?**

And the cheap one: **Aspen's tier names off FilmFreeway** (403 to automated fetch; he has an account).

## Files

- The sheet: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/joan-writing-notes.pdf
- Its builder: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-writing-notes-pdf.py
- Source digest, corrected: https://github.com/Scroggdawg/kom-festival-board/blob/main/meetings/2026-09-06-joan-call.md
- Page draft v6 (for Jordan): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/filmfreeway-page-v6.docx
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-080-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-081-festival.md
