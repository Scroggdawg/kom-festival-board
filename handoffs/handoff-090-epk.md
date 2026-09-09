# handoff-090-epk

## Where we left off

**This turn (Sep 9, 2026, Opus 5):** Luke sent nineteen notes on the EPK INFO document and asked for them catalogued, executed, and double-checked. Done, and audited against the deployed files rather than against intent. **`press/epk.json` rev 18 · 37 of 47 = 79%.**

### Why the document said "17 of 49"

**He was reading a different file.** There are two documents with almost the same name in `00 PRESS`:

- `EPK INFO — all the text.gdoc` — a native Google Doc another lane made on Sep 8 at 22:08. It is frozen at roughly rev 4, which is where "17 of 49" comes from, and it **cannot be updated from the filesystem** — the `.gdoc` is a 175-byte pointer whose own contents say the changes will be lost.
- `EPK INFO (Claude).docx` — this lane's, rebuilt from `epk.json` on every change. It already said 47 items, rev 17, and already showed all three loglines.

Everything he reported missing — one logline instead of three, no synopsis, the "17 of 49" — was true of the stale doc and already false of the live one. **The naming is the fault**, and it is worth resolving: either the Google Doc gets retired to `z_Old_EPKs/`, which is Luke's call since it is his document, or this lane's file gets a name nobody can mistake.

### The nineteen notes

Catalogued to a file first, executed, then asserted one by one at the end against the **deployed** docx and PDF — parsed back out of the files on the Drive, not out of intent.

| | |
|---|---|
| Confirmed already correct | `3.3` California · `3.4` 2025 · `3.5` 2026 · `3.9` 2.39:1 · `3.10` 24 fps · `3.18` Instagram · `5.2`–`5.5` bios from the website · `9.2` full cast · `11.1` thanks |
| Changed | `3.11` **Alexa 35 RE RAW** in his wording, and the "ARRIRAW?" query dropped from the PDF — he has now confirmed it twice · `3.13` **Stereo 5.1** · `7.2` points at the Drive BTS folder · `A.2` trailer joins `3.12` waiting on You Wu |
| Corrected everywhere | **Yeo → You Wu** |
| Rebuilt | EPK INFO, for reading |
| Already gone | the "ONE UNLOCK / no hard drives needed" block |

**Joan's kit does have a press contact.** `press/epk-spec.md`, which is derived from her Night Feeds EPK, gives page 3 as "RIGHTS: AFI Conservatory + named contact" — that is where `3.17` came from. Ours is still empty and needs a name and an email.

### Yeo, and what was deliberately not rewritten

Fixed in every working document: `tools/build-epk-pdf.py`, `press/epk-inventory.md`, `press/epk-one-sheet.md`, `press/messages-to-send.md` — including the draft message, which was addressed "To Yeo" and now reads "To You Wu".

**The handoffs and the Joan-call notes were left alone on purpose.** They record what was believed at the time. Rewriting a ledger to match later knowledge destroys the ability to audit how a conclusion was reached — and this particular conclusion took three turns and an inference to arrive at. `todo.json` and `PLAN-docket.md` still say Yeo in three places; those belong to the docket lane.

### The audit caught itself

Eighteen of nineteen checks passed and one failed: "no Yeo left in press/ or tools/". The failure was **the check, not the work** — `grep -rl` had matched **binary JPEGs** in `press/assets/` whose bytes happen to contain the letters "Yeo". Re-run with `-I` to skip binaries: clean. Worth recording because a naive text sweep over a repo that now holds 145 photographs will keep doing this.

### The document now

Leads with **Still needed** — ten lines, each with its number and whoever owns it — then the contents, one item per block with room around it, all three loglines and both synopses in full. On the Drive as `EPK INFO (Claude).docx`, and the breakdown PDF beside it in `EPK BUILDS/`.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-089-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Retire or rename one of the two EPK INFO documents** — until then this will happen again, and it cost a whole round trip. Then Jordan picks `2.1` and `2.2`, and `3.17` needs a press contact name and email, which Joan's kit has and ours does not. Unanswered since handoff-062: decimal `3.15` or Roman `III.15`.

## Files

- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/EPK-breakdown.pdf
- On the Drive: `05 MARKETING/00 PRESS/EPK INFO (Claude).docx` · `EPK BUILDS/EPK-breakdown.pdf`
- The spec, and Joan's page 3: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk-spec.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-089-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-090-epk.md
