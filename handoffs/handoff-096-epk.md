# handoff-096-epk

## Where we left off

**This turn (Sep 9, 2026, Opus 5):** Luke authorised, and **the Google Doc is now written directly from this lane.** The colour pass is in it — no import dialog, no second document, same URL and sharing. `press/epk.json` rev 20 · 38 of 47.

### It works

```
gdoc.py whoami   → camerawrap@gmail.com · Luke Scroggins
gdoc.py push …   → replaced "EPK INFO — all the text"
                     was modified 08:20:29Z
                     now modified 09:08:17Z
```

**Verified by reading it back out of Google rather than trusting the write.** All eleven section hues survived the round trip — 5 runs of section 1's indigo, 26 of section 3's teal, 11 of Assets' violet, every band present. The text checks passed too: `STILL NEEDED` leads the document, `Alexa 35 ARRIRAW`, `Susan Dretzka`, `sdretzka@afi.com`, `Instagram and IMDb, per filmmaker`, `Workshop`.

### The verification caught a stale assumption of mine

One probe failed: the document did not contain "rev 19". It was not the document — **another lane pushed rev 20 during the `git fetch` immediately before the build**, so the build correctly used rev 20 and my check was carrying a number from before the pull. The changed field was `5.6` headshots, *"confirmed these are the masters"*.

Worth recording because the failure mode is the pleasant one: the check was wrong in the direction of being *behind* the truth, and it surfaced rather than passing quietly. A probe written against a hardcoded expectation will do this every time the file moves underneath.

### A backup command, added after the fact

The first push happened after exporting the Doc's prior contents by hand, as `.docx` and `.txt`. That is now **`gdoc.py backup <docId> <dir>`** rather than a thing someone has to remember. **A replace is not reversible from this side** and the Doc is somewhere people type — Luke had pasted into it himself an hour earlier. Run backup before any push.

### The loop, closed

```
epk.py set …  →  build-epk-doc.py  →  gdoc.py push  →  the Doc is current
```

`epk.json` stays the truth. The Doc, the breakdown PDF and the published page are all views of it, and none of them needs a human to carry text between them any more.

### The standing caveat

The token holds the **full `drive` scope** — Drive refuses to let an app update a file it did not create on the narrower `drive.file`, and this Doc was made by hand. It sits at `~/.kom-gdoc/token.json`, owner-only, outside the repository. No credential is in git; that was checked before the commit. Revoking is one click at myaccount.google.com → Security → Third-party access.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-094-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Jordan on `2.1` and `2.2`.** Section 2 is the only one at zero, both items are written, and settling `2.2` also settles section 4, since the statement is one of its candidates. Everything else outstanding is a file to collect: `3.12` and `A.2` are You Wu, `A.5` is Jordan, and `7.1` cast bios is the last real writing. Unanswered since handoff-062: decimal `3.15` or Roman `III.15`.

## Files

- The Doc, now written directly: https://docs.google.com/document/d/1ae-MPbAq1otTtYA5-SSYYGd13jjvuz1Co2Zi0IrGvSI/edit
- The tool: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/gdoc.py
- Document builder: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-doc.py
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- The live page: https://scroggdawg.github.io/kom-festival-board/epk.html
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-094-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-096-epk.md
