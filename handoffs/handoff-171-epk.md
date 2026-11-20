# handoff-171-epk — College Television Awards nominee posts, Instagram

## Recap (newest first)
- Luke sent 6 film frames, then 5 of Jedidiah Woods' stage portraits (found at full res in `press/assets/BTS/KOM_Stage-{1,4,5,9,12}.jpg`). Instagram only.
- Built 11 laurel candidates + a laurel-alone card (`press/social/cta-2027/candidates/`, renderer `tools/cta-laurel-posts.py`). Every one is printed against the rules: supplied white laurel, ratio kept, height 17–19% of image (max 20%), inside the picture, no text or logos in frame. Recropped A to landscape (the portrait crop cut her face), and moved D's laurel off his head.
- Wrote 5 caption candidates with pairings and hashtags: `press/social/cta-2027/posts.md`.
- Earlier this session: read the 46th CTA toolkit, saved the rules (`press/social/cta-2027-rules.md`) and the two laurels (`press/laurels/cta-2027/`, byte-identical to the toolkit's).

## Open
- `[CATEGORY]` unknown. No public 46th nominee list found on 2026-11-19; confirm it's announced before posting.
- The stage portraits are filed as BTS. They fit "production stills" in spirit, but it's a judgement call against the toolkit's "no other images".
- Jedidiah's handle and AFI's handle aren't confirmed.

## Next
1. Luke picks the images and captions and fills in the category.

---
**Timestamp:** 2026-11-19 · **Lane:** `epk` · **Continues:** handoff-170-epk.md · **Model:** Opus 5.5 (duck turn, no subagents).

## Files
- Posts: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/social/cta-2027/posts.md
- Rules: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/social/cta-2027-rules.md
- Prior: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-170-epk.md · This: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-171-epk.md

## Addendum, same day
- Luke pasted the Foundation's email: **Scripted Series** (graduate). Public list: https://www.televisionacademy.com/features/news/awards-news/46th-cta-nominees. Also nominated in the category: AFTERLIFE and Fly Again (both USC). Captions filled in; the announcement is public.
- Luke: the posts come from @killerofmenmovie, not him; captions stay generic, naming no crew and no cinematography; never name the co-writer anywhere (memory filed). All five captions rewritten; the only tag is @televisionacademyfoundation.
- Luke picked his caption ("Honored that KILLER OF MEN has been nominated for the 46th College Television Awards in the Scripted Series category. Thank you, @televisionacademyfoundation.") and wants the laurel movable in Canva. Built `tools/build-cta-canva.py` → `canva/ops/cta-2027-canva.json`: 12 pages at 1080×1350; on each, the frame is one element larger than the page (so it can slide) and the laurel is its own element, 352×230 (max 270 tall). Hosted images are in `press/assets/derived/canva-cta-2027/`. Preview: `press/social/cta-2027/canva-preview.jpg`. **Not pushed, not built in Canva:** the app fetches from GitHub Pages, so it needs Luke's OK to push.
- Luke gave the push OK. Removed the co-writer's name from the three files across the 11 unpushed commits (git filter-branch index-filter; the final tree is unchanged; backup branch `backup/pre-scrub-2026-11-19`, local only), then pushed (07e069b..1b3acdf). Added a landscape design, `canva/ops/cta-2027-landscape-canva.json`: film frames A–F at 1080×566 (1.91:1, full sharpness), laurel 108 tall (max 113). Pages serves both ops files.
- Canva build **blocked:** Chrome (Claude in Chrome) isn't signed in to Canva. The design tab is open at 1080×1350. Next: Luke signs in, then open the app in the design with the Preview tab's ui= parameter (canva/STATE.json), set the ops URL, and Build all; then do the same for landscape.
