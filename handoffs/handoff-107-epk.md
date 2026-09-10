# handoff-107-epk

## Where we left off

**This turn (Sep 10, 2026, Fable 5.1):** Luke sent the per-filmmaker Instagram handles and IMDb links and said *"add these to the doc and update the widget."* **`5.7` written, rev 22, 39 of 47 = 83 %; section 5 is complete; the widget is regenerated.** The Doc is with the other session.

### 5.7, as stored

Five lines, `Role | Name | @handle | IMDb URL`, handles exactly as Luke typed them, IMDb links without the `?ref_=` tracking suffix his copies carried (the name ids are unchanged), and a provenance line. Written through `epk.py`, pushed as `499ccca`.

### The Doc: asked, not done, and why

"Add these to the doc" means the existing *EPK INFO* Google Doc. The pipeline that writes into it in place — `build-epk-doc.py` → `gdoc.py push` — is the other session's, and its consent token lives at `~/.kom-gdoc/token.json`, which **does not exist on this machine**. My own Drive connector can only create a new Doc beside the old one. So the peer has been asked to regenerate from rev 22 and push, and to say whether the consent click ever completed; if it never did, the honest fallback is Luke's own File → Import → Replace from the `.docx`, and I will say so.

### The widget: the established one, and now a committed tool

Two turns ago I rebuilt the readout without its section hues because the dataviz validator failed them as a chart palette. Luke: *"When I say make the widget that means make the widget, not reinvent it. Now they're ALL grey."* He was right — same failure class as the resize, a rule of mine over a preference of his. The established readout is back and is now **`tools/epk-widget.py`** (`f8d9b76`): section hues from `BANDS`, three states, the computed hatching rule from handoff-091, owner chips, "What is left." Its docstring records the validator's verdict and does not act on it. Next time it is one command. Lesson saved to memory.

---

**Timestamp:** 2026-09-10
**Lane:** `epk`
**Continues:** handoff-106-epk.md
**Model:** Fable 5.1.

## Next action (the one thing)

**The Doc push, from the session that holds the token.** Then, unchanged: Luke on one kit or two; Jordan on the logline, the synopsis, the sound designer and his name.

## Files

- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- The widget tool: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/epk-widget.py
- The Doc pipeline (theirs): https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/gdoc.py
- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-106-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-107-epk.md
