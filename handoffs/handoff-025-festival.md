# handoff-025-festival

## Where we left off

**This turn (Sep 6, 2026, Fable 5.1, duck):** Luke accepted the list shape and asked for (1) a far more interesting Nigerian colour scheme, (2) a per-task four-way status toggle — not started · started · awaiting response · complete — and (3) "make it visually interesting." Rendered in chat as an interactive mockup.

### What was built (mockup only, not in the repo)

- **Palette — adire indigo:** ground `#14213d`, panel `#1b2c4f`, hairline `#2a3d66`, cream text `#f3ecd8`, muted `#b7bdcc`. A faint cream dot-grid (adire resist pattern) at 7 % over the ground. Status four: not started = outline `#9aa3b8` · started = Oshun gold `#e6a92a` · awaiting response = sky `#5fb3e0` · complete = Nigerian green `#2bb673`. Glyphs ○ ◐ ◔ ● plus the word on every state.
- **Validator, dark on `#14213d`, all-pairs:** normal-vision floor PASS (worst 17.0); CVD WARN 7.6 protan (gold↔green) — legal with the glyph + word carried; tritan 4.5 gold↔sky, covered the same way. Contrasts: cream 13.5 · muted 8.5 · gold 7.7 · sky 6.9 · green 6.1 · outline 6.3. Lightness-band FAIL noted — that band governs series marks; these are status marks with secondary encoding.
- **Interaction:** each item has a four-segment toggle; the group header carries a three-segment bar (started / awaiting / complete) that animates as toggles change; the top carries the whole-board bar, a legend with live counts, and a `send N changes to Claude` button that fires `sendPrompt("Update todo.json: D.1.1 → started; …. Then re-render the list.")`. State lives in the widget until sent — the footer says so.
- **Status vocabulary changed by Luke:** four states now (adds *awaiting response*). `PLAN-docket.md` §3 and `tools/todo.py` must carry `not_started | started | awaiting | complete`.

### Still mockup

No `todo.json`, no writer, no page. The list is hand-carried from the digest §D; the toggles do nothing outside the widget until the send button is pressed and Claude writes the file.

---

**Timestamp:** 2026-09-06
**Lane:** `festival`
**Continues:** handoff-024-festival.md
**Model:** Fable 5.1. **Duck turn** — one interactive mockup.

## Next action (the one thing)

**Luke: is this it?** If yes, the goose (one turn): rewrite `PLAN-docket.md` to the list shape with four statuses and the adire palette; seed `todo.json`; build `tools/todo.py`; render the widget from the file; then `docket.html` on Pages. Still his: the name; whether D.n.n prints; the push exception.

## Files

- Plan (to rewrite): https://github.com/Scroggdawg/kom-festival-board/blob/main/PLAN-docket.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-024-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-025-festival.md
