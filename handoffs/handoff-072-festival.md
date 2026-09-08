# handoff-072-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5) — THE LOGLINE IS LOCKED IN TWO VERSIONS.** Luke: *"These are the two im going to present. Lock them. A and B."* Twenty-four generations.

**A — title first, ends on the act. 65 words, 356 characters.**

> KILLER OF MEN -- In 1834 South Carolina, an enslaved man is forced to fight to the death for spectacle, and survival. But every victory means killing one of his own. When he stumbles upon his opponent's burial rites, he finds the ceremony being held in the ancient faith of their shared ancestors, who he must now face to decide whether he will kill again.

**B — title last, ends on what he becomes. 64 words, 354 characters.**

> In 1834 South Carolina, an enslaved man is forced to fight to the death for spectacle, and survival. But every victory means killing one of his own. When he stumbles upon his opponent's burial rites, he finds the ceremony being held in the ancient faith of their shared ancestors, who he must now face to decide whether he will remain... a KILLER OF MEN.

**The 56 words between "In 1834" and "…to decide" are identical in both.** They differ only in where the title sits and how the sentence ends. **Neither is a draft of the other** — both go to Jordan and one comes back chosen.

**Open seam, his words:** *"May eventually update 'who he must now face to decide' but the rest im good on."* That clause is identical in both, so a later edit hits both at once.

Both versions absorbed findings from the two generations before them: **A** uses the Gen 23 corpus measurement (18 of 23 title-bearing loglines put the title in the first quarter — the press-kit convention). **B** uses the "remain" fix and swaps the banned em dash for an **ellipsis**, which keeps the theatrical pause without breaking his own Sep 7 rule.

### Shipped

`press/filmfreeway-page-v6.md` and `.docx` — both versions, both in red, labelled A and B with counts, v5 quoted beneath. Idea box carries a two-version LOCKED banner; the morning single lock is retained beneath it as superseded.

Messaged the docket (pin v6; its item text implies one logline) and the EPK session (field 2.1 is one string and now needs to hold two values — told it the schema choice is its own but that **neither version may be modelled as primary**).

### A defect I introduced, found by auditing the docket's bug against my own lane

The docket reported that its merge silently dropped unmodelled top-level keys and rolled `rev` backwards with a success-shaped result. **Audited the board's publish loop for the same shape: it is clean.** `applyOps` deep-clones the whole fetched remote (`JSON.parse(JSON.stringify(base))`) and mutates it rather than rebuilding from a field list; the PUT sends that whole object with the sha; `rev` is a fresh uuid so it cannot go backwards; the client validator has no unknown-key rejection. Hand-added keys survive a browser publish.

**But the audit found this instead:** yesterday I added `sourceUrl` to the IFFR record. **`source` already existed for that purpose — 124 of 151 records — and it is what `tools/validate-data.py --provenance` checks.** The docket's dashboard tests `provenance==='official' && sourceUrl`. So two fields now hold one fact and the two validators disagree about which is authoritative.

**Proposed convergence: `source` is the URL, `provenance` is the flag, `sourceUrl` dies.** Sequencing matters — both fields hold the identical URL today, so the docket changes its test first and I delete `sourceUrl` after; the reverse order would make the front page read "none verified yet" in the gap. I am not editing `index.html`.

Also invented a scalar `note` on that record where the schema's structure is `notes[]` (array of `{text}`), which the board renders and searches. Will fold it in.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-071-festival.md
**Model:** Opus 5.

## Next action (the one thing)

**IFFR closes Sep 15, 17:00 CEST — seven days**, verified in 067, still unanswered across six turns. Its blocker is a **screener link**, not the logline: the campaign Vimeo does not exist (D.3.3) and D.3.1 is "get YouTube access from Jordan."

Then: send Jordan v6 (D.2.1), and delete `sourceUrl` once the docket's test has moved.

## Files

- Page draft v6 (docx, for Jordan): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/filmfreeway-page-v6.docx
- Page draft v6 (md): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/filmfreeway-page-v6.md
- Idea box, locked A and B: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/logline-idea-box.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-071-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-072-festival.md
