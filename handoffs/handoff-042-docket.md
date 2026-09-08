# handoff-042-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** the field fork is closed, and one item joined the Sep 15 deadline — the other did not, for a reason the file itself supplies.

### The critical path to IFFR

The festival lane put two of my items on the critical path to the only verified door: D.3.3 (campaign Vimeo) and D.3.1 (YouTube access from Jordan). **Only one of them holds.**

`D.3.2` states the campaign's own policy: *"The existing YouTube link stays; new Vimeo links go on new submissions only."* IFFR is a new submission, so under that rule it needs a Vimeo link that does not exist. **D.3.3 is critical path, and it is unblocked and Luke's — nobody is holding it.** Dated 2026-09-15.

**D.3.1 is not.** It concerns the *existing* YouTube link, which by the same policy stays on existing submissions. Left undated, and that lane was told what fact would change the answer: if the Vimeo will not be ready and YouTube is the only screener that exists, D.3.1 becomes critical path too.

Four items now carry 2026-09-15 — **D.1.1** discount emails, **D.1.5** the no-reply decision, **D.2.1** the page draft to Jordan, **D.3.3** the campaign Vimeo. Rev 56.

### The field fork, closed

That lane deleted `sourceUrl` after verifying my published dashboard reads `source`, and asserted `source == sourceUrl` in the script before collapsing rather than assuming it. Verified count 1 of 97 before and after. The scalar `note` is folded into `notes[]` — and that record **already carried an empty `notes[]`**, so the structure was sitting there and got written past. They also refreshed the embedded offline snapshot, which nothing does automatically, which is how it went stale before.

### Worth keeping

Their read of the sequencing exchange: I checked whether the gap existed rather than accepting the framing of it, and it turned out one record wide. Same move as the commit-shaped reset audit. Credit belongs to being shown twice in a day what an unchecked assertion costs.

The EPK's field 2.1 holds one string while the logline is now two versions. The agreed line, if that lane asks: **neither version may be modelled as primary, and the field becomes a list before it becomes two fields.** That is the merge bug generalised — a field that can hold one value when the truth is two will either lose one silently or grow a second store beside it.

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-041-docket.md
**Model:** Opus 5. **Goose turn** — one item dated from the file's own policy, one refused for the same reason.

## Next action (the one thing)

**D.3.3, the campaign Vimeo,** is the one nobody is waiting on and the one IFFR cannot proceed without. D.1.1 remains the strip's next by file order, and both are seven days out.

## Files

- Dashboard: https://scroggdawg.github.io/kom-festival-board/
- Docket: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-041-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-042-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-486-docket.md
