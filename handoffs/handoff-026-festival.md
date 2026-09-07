# handoff-026-festival

## Where we left off

**This turn (Sep 6, 2026, Fable 5.1, duck):** Luke rejected the segmented-toggle control and specified the list's look precisely. Rendered in chat as an interactive mockup:

- **Status dial:** one sprite per task, tap to cycle — ○ not started (outline `#9aa3b8`) → ◐ started (Oshun gold `#e6a92a`) → ⊘ awaiting response (sky `#5fb3e0`) → ● complete (green `#2bb673`) — word beside it in the same colour. These four colours are reserved for status only.
- **Blocks:** 12×8 blocks, one per task, in every section header; outline in the section's colour when not started, filled with the status colour otherwise.
- **Title top-left:** "Killer of Men Festival Campaign"; top-right: the five-row block map (5 · 9 · 6 · 8 · 9 blocks), one row per section, same fills.
- **Section colours** (not grey, gold, sky or green): terracotta `#e8703a` · magenta `#d64f9e` · violet `#a06ff0` · periwinkle `#6f93f0` · peach `#f2b8a0` — on the section name, the block outlines, the left rule of the open list, and the map-row key dot. Not validated as a categorical set: section identity is also carried by name and position; note for the build.
- Send button unchanged (`sendPrompt("Update todo.json: D.1.1 → started; …")`). Still a mockup — no `todo.json`, no writer.

---

**Timestamp:** 2026-09-06
**Lane:** `festival`
**Continues:** handoff-025-festival.md
**Model:** Fable 5.1. **Duck turn** — one interactive mockup.

## Next action (the one thing)

**Luke: is this it?** Then the goose builds: `todo.json` (four statuses), `tools/todo.py`, the widget rendered from the file, `docket.html` on Pages with this exact look; rewrite `PLAN-docket.md` to match.

## Files

- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-025-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-026-festival.md
