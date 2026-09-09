# handoff-087-epk

## Where we left off

**This turn (Sep 9, 2026, Opus 5):** Luke sent the Instagram and IMDb links, said the image selection is settled so three slots can go, and asked what the 60-second introduction is. **`press/epk.json` rev 14 · 36 of 47 = 77%.** Four sections are now complete.

### Three slots retired, and why the numbers were not freed with them

`2.3` hero still, `4.2` photo behind the text and `9.3` still behind the credits are dropped — Luke has the images he is using, so leaving them showing as missing would be false.

**Their numbers are retired, not released.** `drop_field()` records the number in the section's `retired` list and `add_field()` counts past it. Without that, dropping `2.3` and later adding a field to section 2 would hand the new one the number `2.3` — and a number Luke had already used in conversation would quietly mean something else. That is the same class of failure as the docket lane's prefix match writing one festival's data onto another.

Asserted, not assumed: after `2.3` was retired, a probe field added to section 2 came back **`2.4`**; hand-editing it to `2.3` is refused by the validator; and `drop_field` refuses a field that still holds a value or candidates. Every prior revision is in git regardless, so no drop is unrecoverable.

**The denominator moved from 49 to 47**, which is why the percentage jumped from 69% to 77% with only two fields added. Worth saying plainly: about half of that rise is arithmetic, not work.

### The two links

`3.18` Instagram — `https://www.instagram.com/killerofmenmovie/`.

`3.19` **IMDb** — `https://www.imdb.com/title/tt37523933/` — is a **new field**. The film's IMDb title page had no home: `5.7` is Instagram and IMDb links *per filmmaker*, not the film. Section 3 is the links footer, so it appends there as `3.19`. Flagged rather than done quietly, since the standing rule is to ask when something does not fit a slot; this one fits so obviously that filing it and saying so beat blocking on the question. Easy to drop if Luke disagrees.

### What the 60-second introduction is

From Joan on the September 6 call, in her words: *"sometimes some of the festivals want to like put it like a brief filmmaker presentation before they screen the film."*

So: **Jordan, to camera, about a minute, introducing the film** — played by the festival before the screening. It is not a trailer and not a press piece. It ships in the **per-festival package** alongside the laureled poster, the laureled trailer, the localised subtitled screener and the SRT (`press/epk-spec.md`, the delivery folder). It is **D.4.7** on the docket, owned by and waiting on Jordan, and it is one of only two things in the kit that still need him.

### What is actually left

Nine items, and only two are writing:

- **`7.1` cast bios** — the last real writing. Ten billed roles now exist in `3.15`; the bios do not.
- **`3.17` press contact** and **`3.12` exhibition formats** — facts, not work.
- The other six are files someone must produce or collect: headshots, per-person IG/IMDb links, partner logos, the trailer, the laurels, the 60-second intro.

Plus `2.1` and `2.2`, both written and waiting on a pick.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-086-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Pick the logline and the synopsis** — `2.1` and `2.2` are the only section still at 0%, both are already written, and each is one click on the page. That takes 77% to 81% and puts text on page 2. Then `3.17` press contact, which needs nobody but Luke. Unanswered since handoff-062: decimal `3.15` or Roman `III.15`.

## Files

- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- Data: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/epk.py
- PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/EPK-breakdown.pdf
- The Joan call: https://github.com/Scroggdawg/kom-festival-board/blob/main/meetings/2026-09-06-joan-call.md
- On the Drive: `05 MARKETING/00 PRESS/EPK INFO (Claude).docx`
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-086-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-087-epk.md
