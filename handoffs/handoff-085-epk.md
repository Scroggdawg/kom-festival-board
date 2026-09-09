# handoff-085-epk

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** the end-credit workbook has **not** arrived. `press/epk.json` unchanged at rev 11 · 30 of 49 filled.

### The watcher I set up last turn was blind, and I said it was working

`find -newermt "-90 minutes"` **silently matches nothing on macOS.** BSD `find` does not accept a relative time string there — it does not error, it just returns an empty set. Proved rather than guessed: a file touched one second earlier is not matched by `-newermt "-120 minutes"`, on the local disk and on the Drive mount alike, while `-mmin -120` matches it correctly.

```
local file, just touched     -newermt '-120 minutes' -> 0
                             -newermt '-2H'          -> 0
                             -mmin -120              -> 1
drive file, mtime 45m ago    -newermt '-120 minutes' -> 0
                             -mmin -120              -> 1
```

So last turn's watcher could never have reported the workbook even if it had landed, and its "NOT FOUND after ~47 minutes" carried no information. Two other checks in that turn used the same flag and were also meaningless — "newest 8 files anywhere under it" and "anything modified in the last 2 hours in My Drive". The tell was that the second one claimed nothing had changed in My Drive during the two hours in which this lane wrote 113 files into it. That contradiction is what exposed the bug.

**The conclusion still holds, on separate evidence.** An unfiltered name-based sweep — no time predicate — listed every spreadsheet in My Drive, the whole `KILLER OF MEN` tree, `Other computers/My MacBook Pro`, and `~/Downloads`: **29 workbooks, none of them the credits.** Shotlists, expense reports, gear lists, and the festival list. Nothing new.

### The watcher now

Snapshot-diff, no time predicate at all: 29 spreadsheet paths recorded as a baseline, rescanned every 25 seconds for about 42 minutes, reporting anything that appears in the set and was not there before. It cannot be fooled by a timestamp that does not behave.

### Still true from last turn

`openpyxl 3.1.5` is installed in `$SCRATCH/venv` and `$SCRATCH/readxl.py` dumps every sheet as aligned text — both proven against a real 258-row workbook, so the parse is not the risk.

**The `.gsheet` risk is unchanged and worth restating**, because it is now visibly common: of the 29 spreadsheets found, most are `.gsheet` pointers rather than real files. If Drive converts the upload, it lands as one — 175 bytes of JSON, unreadable from disk. The fix is Luke's: in Drive, **File → Download → Microsoft Excel (.xlsx)** into the folder. The watcher looks for `.gsheet` too, so this will be named rather than missed.

---

**Timestamp:** 2026-09-08
**Lane:** `epk`
**Continues:** handoff-083-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**The workbook.** When it lands: parse it section by section into `7.1` cast bios, `9.2` full cast, `10.1` full crew, `11.1` thanks and `11.3` AFI boilerplate — not as one blob — and use it to settle the three open spellings: **Rajarajeshwari vs Rajeshwari**, whether the plantation owner is credited **Kenner**, and whether **Yeo is You Wu**. Independent of it: Kenner's actor, `3.17` press contact, `3.18` Instagram, whether "RE-RAW" is ARRIRAW, and decimal `3.15` versus Roman `III.15`.

## Files

- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Handoff convention: `KILLER OF MEN/HANDOFFS/README.txt`
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-083-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-085-epk.md
