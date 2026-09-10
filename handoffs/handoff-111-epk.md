# handoff-111-epk

2026-09-10 · lane: epk (continues handoff-110-cast) · model: started on Fable 5.1, finished on Opus 5 · goose turn (fact-check, write, edit the Doc, verify)

## Where we left off, newest first

1. **The cast bios are in field 7.1 and in the EPK INFO Doc.** Luke: "add these to the epk text doc on gdrive." `press/epk.json` rev 23 (commit f00ba4d) holds four bios in crawl order, a Prior credits line for each, and three caps notes: drafts not yet approved; Sandra McDaniels has no bio of her own; what to confirm with the actors. `press/cast-bios.md` carries the sources, the credit tables and the fact-check. **The Doc was edited in place, not regenerated.** 7.1 is filled in section 7's colour (#6a4400, the Doc's sign for Claude's text), section 7 now reads (2 of 2), and 7.1 is off the Still Needed list. A Drive read-back shows 7.1 matching epk.json line for line and nothing else in the Doc changed.
2. **Fact-check before writing.** Eight checkers, two per actor with different angles, plus a critic that merged their verdicts. They corrected eight wording points: Erik's sketch-team line and "short film" for Al Davis; Eric's "performed in ten", the shared 2006-2007 StageSceneLA award, "co-produced", "HBO's" attached to Succession only, and IRT Theater; Jamal's RADA line as technique and scene study. All of Sandra's claims held. The full table is in `press/cast-bios.md`.
3. handoff-110-cast: the four actors found and confirmed against the IMDb title page tt37523933.
4. handoff-109-epk (peer session): the Canva build plan.

## Direction

- Each actor should approve their bio before print. Get Sandra's own bio from her or from NTA Talent Agency.
- The kit (.ai and PDF) reads epk.json but has **not** been rebuilt. Page 7 picks up 7.1 on the epk lane's next build.
- The Doc's lead line still says "38 of 47 supplied · rebuilt from rev 20". It was already stale before this turn, and I left it alone because the Doc is no longer a pure rebuild.
- 5.7 has been filled in epk.json since rev 22 but still reads "not supplied" in the Doc (the gap from handoff-108). It was not touched this turn.

## Why the Doc was edited in place

The Doc holds text people typed into it that is **not** in epk.json: second versions of the director's statement and of every filmmaker bio, and a rewritten producer bio. Regenerating would erase all of it, because `gdoc.py push` replaces the whole Doc. Its token is not on this Mac anyway. The method is in memory: Claude in Chrome signed in as camerawrap, a synthetic paste event on the Doc's text-event iframe, a plain-text paste so the block inherits the value style, then colour and italic set over the block.

## Incidents, reported plainly

- **A stale element ref typed into the Doc.** After Find & Replace was reopened, refs from the earlier find resolved to points in the document. The two typed search strings replaced Jamal Dennis's bio paragraph and one blank line. Both were reverted with two undos, one at a time, and the Drive read-back confirmed the repair.
- **A styled HTML paste came in at 11.5pt against the Doc's 15pt body.** It was undone and replaced with the plain-text paste.
- **A scratch Doc was created and trashed.** "zz scratch paste test (Claude, delete me)" was made for a paste test, then moved to Drive trash, not permanently deleted.
- The Doc's version history shows all of these edits under Luke's account.

## What was verified

| Check | Result |
|---|---|
| epk.py check after the set | clean, rev 23 |
| Commit f00ba4d | press/epk.json and press/cast-bios.md only; the peer's two commits had been pushed by the peer at 14:51 |
| Doc 7.1 vs epk.json 7.1 | identical, 20 lines |
| Doc outside 7.1 | unchanged except the section 7 count and the Still Needed line |
| Section 7 heading | (2 of 2) |
| Colour | #6a4400 (106, 68, 0), upright, Georgia 15, the Doc's value indent |

## Files

- The Doc: https://docs.google.com/document/d/1ae-MPbAq1otTtYA5-SSYYGd13jjvuz1Co2Zi0IrGvSI/edit
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Bios, sources and fact-check: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/cast-bios.md
- Commit: https://github.com/Scroggdawg/kom-festival-board/commit/f00ba4d
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-110-cast.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-111-epk.md
