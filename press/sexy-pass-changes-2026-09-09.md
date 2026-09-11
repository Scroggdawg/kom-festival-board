# KILLER OF MEN EPK kit — change list for re-layout

Page 1296 x 1728 pt, margin M = 74 pt. Files: `site/tools/build-epk-kit.py` (pages 1–8, wrapper) and `site/tools/build-credit-card.py` (pages 9–11, imported by the kit). Palette unchanged: CREAM #efe6d6, DIM #b9a88c, RULE #6b5942 on GROUND #0b0806. Tone carries every emphasis change below; no new hue, no new face, no copy, no captions.

Findings F13 and F19 were refuted and are not applied: page 7's ROLE | NAME lockup stays at SUB + 3 = 24 pt, pages 5–6 at SUB = 21 pt; the page 3 footer stays at M + 24.

## Page 1

No change.

## Page 2 — logline / synopsis

| id | change | why |
|---|---|---|
| F09 | In `page_logline()`: `x, w = M, 900.0` (text edge 74, right edge 974). Label offset `y = H - hero_h - 90` (was 104; matches `page_cast`). Logline-to-SYNOPSIS gap 62 -> 48. Both label-to-body gaps 52 (were 54 / 52). hero_h 860, still 5 crop, sizes 26/40 and 22/34.5 unchanged; `fit()` still guards the last notch. Estimated: block ends ~1514 pt from top, ~136 pt above the margin. | 95–115 characters per line from a 114 pt edge no other page uses; 210–290 pt of bare ground under the synopsis. |
| F18 | `label()` in build-epk-kit.py: size = BODY (15.6), track = Z.track_r + 1.0 (2.35), DIM, no inserted spaces. Callers pass plain "LOGLINE" / "SYNOPSIS" and drop the size= overrides. Same class serves page 7 (BILLED CAST) and page 11 (THANK line). | Label tier was set at 18.2 / 15.2 / 14.2 pt with two spacing methods across pages 2, 7, 11. |
| F16 | `proof_slug()` (line 269): `tracked(c, W/2, M*0.45, text, "Bask", 9.5, 1.4, DIM, "center")` — RULE -> DIM, tracking 1.2 -> 1.4, size 9.5 and the 33 pt baseline unchanged. Both proof marks (page 2, page 5) inherit through the helper. Slug stays until fields 2.1 / 2.2 are filled. | RULE on GROUND is ~3:1; the mark cannot do its job at that contrast. |

## Page 3 — programmer page

Apply in this order; each later item depends on the sizes fixed by F04.

| id | change | why |
|---|---|---|
| F12 | Replace the hand-drawn 30 pt / 4.0 title with `title(c, 'KILLER OF MEN', H - M - 30, align='right', x=W - M)`: 40 pt, track 6.0, 0.7 pt RULE hairline 236 pt long drawn from xr − 236 to xr, 22 pt under the baseline. First kv line at the y `title()` returns (62 pt below). Pass the unspaced string; `title()` inserts the spaces. Right edge xr = 1222 kept. | Only titled page off the title law shared by pages 4, 5, 9, 10, 11. |
| F04 | kv, CAST, LINKS and footer lines 15.6 / 16.6 -> 19 pt on one 28 pt step (was 24 / 22 / 26), tracking Z.track_n. `head()` 21 -> 24 pt Bask-SB, 34 / 34 pt padding kept. Budget: title block + 33 lines x 28 = 924 + 4 heads x 68 = 272 -> column ends ~1355 pt from top, ~225 pt above the footer top; footer stays at M + 24. If `condense()` must step any line below 18 pt, set the whole column to 18 / 27 rather than let one line differ. Re-base the three link hit rectangles (mailto at xr − 520, the LINKS rects, the footer rects) on the 28 pt step and 19 pt size. | Smallest type in the kit (8 px at laptop fit-to-height) on the page a programmer reads first; column stops at 68 % of the page. |
| F05 | In `kv()`: keep building the full `f"{k}: {v}".upper()` line and running `card.condense()` on it so size and tracking are unchanged; then draw two passes on one baseline: `wv = tracked(c, xr, y, v.upper(), "Bask", size, tr, CREAM, "right")` then `tracked(c, xr - wv, y, f"{k}: ".upper(), "Bask", size, tr, DIM, "right")`. Same pattern in the CAST loop: role + "  |  " in DIM, actor in CREAM. Apply to every kv() caller (spec block, THE TEAM, RIGHTS). Section heads, title and LINKS untouched. Sizes are F04's. | Key and value were one face, size and colour; right alignment put the keys at 12 different x positions. Pages 7, 9, 10 already zone role DIM / name CREAM. |
| F06 | LINKS loop: `setStrokeColor(RULE)` -> `setStrokeColor(DIM)`, `setLineWidth(0.5)` kept, underline at y − 6 (was y − 5). Footer loop: after each `tracked()` add `c.setStrokeColor(DIM); c.setLineWidth(0.5); c.line(xr - wtxt, yy - 6, xr, yy - 6)` under WWW.KILLEROFMEN.COM, INSTAGRAM @KILLEROFMENMOVIE, IMDB. Hit rectangles unchanged. Do not underline the EMAIL value; head rules stay RULE at 0.7 pt. | Underlines at ~3:1 vanish at laptop scale; three live footer links carried no affordance. |

## Page 4 — director's statement

| id | change | why |
|---|---|---|
| F03 | In `page_statement()`: `x, w = (W - 720) / 2, 720` (x = 288). Size 23 / lead 36.5 and centred setting kept; `fit()` holds 23 pt at this width (34 lines, ~1285 pt body, max 84 chars/line). `room = top - (M + 76) - 56` so the signature is inside the guarded box. `y_end = para(...)`; draw the signature with `tracked()` at W/2, `y_end - 56`, same "Bask", Z.role + 1, Z.track_r + 1.0, DIM, "center" treatment. Result: body 195–1495 pt from top, signature baseline 177 pt from the foot. `title()` untouched. | Body ran ~100–119 chars per line and stopped at 63 % of the page; signature pinned 528 pt below it read as a footer. |
| F20 | Add `focus=(0.5, 0.5)` parameter to `ground()` and pass it through to `cover()`. Call `ground(c, 10, alpha=0.20, scrim=0.50, focus=(0.62, 0.5))` (was alpha 0.26, focus 0.5). 0.18 is the floor; do not brighten. | Hottest ghost in the kit (text-free mean L 19.1 / p95 35 vs page 3's 16.5 / 24); at focus 0.5 the 3:4 cover cut the second silhouette at the page edge. At 0.62 the crop keeps 41.9–74.3 % of the frame and both figures stand whole. |

## Page 5 — filmmakers 1

| id | change | why |
|---|---|---|
| F01 | Primary: fill `PORTRAITS['5.1']` with a behind-the-scenes frame of the director, cover-cropped to the same 333 x 396 pt box, focus (0.5, 0.40), no frame line, graded to match the headshots (value only). Candidates: `KOM_Day3_TheFarm-43`, `-45`, `-46` (director at the monitor) or the centre figure of `KOM_Day4_Soundstage-93`. Luke confirms the frame shows Jordan Betine before it ships; never a film still for a filmmaker. text_w then equals the other blocks' (W − 2M − 333 − 48 = 767). Fallback if no frame is approved: in `bio_block()`, when `has_img` is False set `text_w = W - 2*M - 333 - 48` and return `y - para_height(text, text_w, 19, 30) - 40` instead of `y - img_h` (block ~200 pt); the two portrait blocks stay at 436. Either way `page_bios()` distributes spare as `between = spare / (len(items) + 1)`, subtracted once before the loop (see F08): primary spare = 1438 − 1308 = 130 -> ~32 pt; fallback spare = 1438 − 200 − 872 = 366 -> ~91 pt. | The director's block reserved a 436 pt slot with no portrait: 120-character lines over a ~300 pt hole, while the three blocks sat 43 pt apart. |

## Page 6 — filmmakers 2

| id | change | why |
|---|---|---|
| F08 | In `page_bios()`: `block = 436.0` on every page (delete the 560 branch) so all portraits render 333 x 396 pt, focus (0.5, 0.40), 0.84 aspect. Replace `between = min(90, spare/len)` with `between = spare / (len(items) + 1)` and subtract `between` once before the loop, so the two-item page splits its spare equally above, between and below the blocks (≈200–216 pt each from the code's avail) instead of stacking at the top with ~340 pt dead at the foot. First-item page handled by F01. Do not bundle a PORTRAIT_ZOOM for Ruoxiao Li — see open questions. | Page 6 portraits were 31 % larger than page 5's, started 82 pt higher, and ended 343 pt above the foot; facing bio pages read as two documents. |

## Page 7 — cast

| id | change | why |
|---|---|---|
| F02 | In `page_cast()`: `hero_h` 900 -> 1230 (image bottom 498 pt from the foot); still 40 and focus (0.5, 0.35) unchanged. Heading baseline `H - hero_h - 90` (408 pt from the foot) at SUB + 3 = 24 pt as now. BILLED CAST label per F18 (15.6 DIM, track 2.35, no spaces). Cast rows: role 14.2 -> 15.6 (DIM), name 15.6 -> 17 (CREAM), step 25 -> 28; name offset col_x + 210 kept. Five rows then run 318 -> 206 pt from the foot, ~130 pt above M. Restore hero_h toward 1000 only when field 7.1 (bio) is filled. | 548 pt (32 %) of bare ground under a list whose names rendered at 8 px at laptop scale. |

## Page 8 — behind the scenes

Land F07, F10 and F14 together: the row heights are hard-coded and must sum with the gaps and strip to exactly 1728.

| id | change | why |
|---|---|---|
| F07 | In `page_bts`: `scale = (W - GAP*(len(cells)-1)) / sum(w for _, w in cells)`; draw each cell at `w*scale` and advance x by `w*scale + GAP`. Last cell's right edge lands at 1296.0. GAP = 6.0 untouched. | Every row stopped 11 pt short of the right edge while the left edge bled; read as mis-registration. |
| F10 | Rebuild MOSAIC as four rows, GAP 6, strip 74 (F14), rows summing 1636: row 1 h = 399 `KOM_Day3_TheFarm-18` (432) / `-59` (432) / `-149` (432); row 2 h = 399 `KOM_Day3_TheFarm-152` (432) / `KOM_Day4_Soundstage-81` (432) / `KOM_Day3_TheFarm-185` (432); row 3 h = 399 `KOM_Day3_TheFarm-220` (432) / `KOM_Day4_Soundstage-32` (432) / `KOM_Day4_Soundstage-93` (432); row 4 h = 439 `KOM_Day3_TheFarm-237` alone at 1296. 399·3 + 439 = 1636; + 3·6 + 74 = 1728. Ten photographs: drop `KOM_Day3_TheFarm-99` and `IMG_4467`. Verify the centre crop of Day3-237 at 1296 x 439 keeps every head; if `cover()` clips any, set rows 1–3 to 385 and row 4 to 481 (1155 + 481 = 1636). | Twelve cells within 5 % of each other with no dominant; the 45-face crew frame at 428 pt wide rendered ~9 pt faces. One size break (the crew row) on a held thirds grid; the two tonal breaks (daylight top-left, blue fog centre of row 2) carry sub-dominance by value, not size. |
| F14 | `strip = M` (74.0). Caption: `tracked(c, W/2, M*0.45, "BEHIND THE SCENES   ·   PHOTOGRAPHS JEDIDIAH WOODS", "Bask", Z.role, Z.track_r, DIM, "center")` — 14.2 pt, track 1.35, the kit's existing role-label class; baseline 33 pt from the foot (the same mark line as the proof slug). Bleed to top, left and right kept; no captions added. The permanent credit deliberately sits one class above the 9.5 pt temporary proof slug (F16). | 9.5 pt caption 10.6 pt from the trim in a 28 pt strip; every other page keeps a 74 pt foot. |

## Page 9 — cast credits

| id | change | why |
|---|---|---|
| F15 | Keep `ground()` at 0.16 / 0.55. In `credit_pages()` change the call lists to: cast `stills_for([14, 16])`; crew `stills_for([13, 17])`; thanks `stills_for([15])`. Primary picks 14 (mourners around the shrouded body, centre-crop mean L 83), 13 (oaks and field, L 70), 15 (burial under the oaks, L 97); 16 and 17 are spill fallbacks only so no two consecutive pages repeat a frame. Rule for this film: a ghost at 0.16 / 0.55 needs centre-crop mean L >= 70. | Stills 31 and 35 land at effective L ~9 on a L ~7 ground (invisible); page 11 repeated page 3's still 41. |

No other change on page 9; its title rule and group dividers are already the two correct classes (F21 lands on page 11).

## Page 10 — crew credits

| id | change | why |
|---|---|---|
| F22 | In `balance()` (build-credit-card.py): choose the column split only at department-heading boundaries (entries with role None), picking the boundary that minimises \|left_h − right_h\| subject to both columns fitting col_h (1472 pt at 1x). For the current list that is the boundary before ART: left = CAMERA, PRODUCTION, ELECTRIC, GRIP, SOUND (ends ~1167 pt from top); right = ART, COSTUME HAIR AND MAKEUP, POST, SAFETY AND SPECIAL EFFECTS, SUPPORT (ends ~1565 pt from top, ~89 pt above the foot). `flow()`, gutter, 21 pt lead and 15 pt gap unchanged. | Right column opened on SET DRESSERS / ART PAS / SCENIC PAINTER with no heading; ART's head sat at the foot of the left column. |
| F17 | In `draw_col()` (build-credit-card.py ~line 283): when `stringWidth(lab) + track_r*(len(lab)-1) > x_role - left_bound` at z.role, wrap with `simpleSplit(lab, "Bask", z.role, room - z.track_r*(len(lab)-1))` and draw each line right-aligned at x_role, `y - i*z.lead`, at z.role / track_r unchanged; drop the `condense()` call on labels. In `item_h(e, z)` compute label_lines the same way (via `pdfmetrics.stringWidth`) and return `z.lead * max(len(names), label_lines) + z.gap` so `flow()` and `balance()` see the true height. `condense()` and its 6 pt floor untouched for names and department headings. Sizes 14.2 / 15.6, lead 21, gap 15, gutter kept. | 'DEPARTMENT HEAD MAKEUP AND SFX MAKEUP' and '2ND SECOND ASSISTANT DIRECTOR' were condensed to ~9–13 pt inside a 14.2 pt list. |

## Page 11 — thanks / end card

| id | change | why |
|---|---|---|
| F11 | In `page_thanks()` (build-credit-card.py): boilerplate simpleSplit measure `W - 2*M - 180` (968) -> 540 (W/2 ± 270), scaled by the same factor the boiler size uses (`max(z.s*0.8, 1.0)`) so the --medium / --large card builds hold the ratio. Z.boiler 11.4 / 17 unchanged. Each paragraph sets in two lines with 10–12 words on the last; keep a '>= 3 words on the last line, else 520' guard. Anchor the legal block from the foot on the last thanks page: (c) MMXXV baseline at M + 18 = 92 pt (the kit's page-4 footer baseline), the three paragraphs stacked above it on z.boiler_lead (17) with 12 pt between paragraphs and the existing 10 + lead gap above the (c) line. Compute the `foot` height estimate (lines 371–372) from the actual simpleSplit line counts, not a hard-coded 2 per paragraph. Title, names and fellows keep flowing from the top; ghost occupies the seam. Re-render and confirm the seam reads as a zone, not a hole. | 143–170-character lines in 11.4 pt caps, single-word orphans, and ~560 pt (32 %) of empty ground after the (c) line. |
| F21 | build-credit-card.py line 396: `c.line(W/2 - 118*z.s, y + 14, W/2 + 118*z.s, y + 14)` -> `c.line(W/2 - 90*z.s, y + 14, W/2 + 90*z.s, y + 14)` so the fellows divider is 180 pt / 0.5 pt like the page 9–10 group dividers. `heading()` (236 pt / 0.7 pt), the one_col divider and page 3 link underlines unchanged. | Divider borrowed the title rule's length at the divider's weight: two identical-looking rules doing two jobs. |
| F18 | THE FILMMAKERS WISH TO THANK line: `z.role` -> `z.role * 1.1` (15.6), tracking 2.35 as now, DIM — the label class shared with pages 2 and 7. Row role labels in the columns stay at Z.role 14.2. | One label tier at one size across the kit. |
| F15 | Ghost: still 41 -> still 15 (see page 9 row). | Still 41 already grounds page 3; the kit's last image was a repeat. |

## Do not change

- Palette and its value-only hierarchy: CREAM #efe6d6, DIM #b9a88c, RULE #6b5942 on #0b0806; Baskerville throughout; no second face, no accent colour; every page passes the grayscale test.
- Page 1: poster fitted whole at min(W/iw, H/ih) with 54 pt bands of kit ground above and below; nothing cropped, billing block intact; never fit-to-height or cover-crop the key art.
- Page order 1-2-3 (poster, hero + logline/synopsis, specs/contact/links).
- Title law on pages 4, 5, 9, 10, 11: Baskerville 40 pt, spaces + 6.0 tracking, 236 pt / 0.7 pt RULE hairline 22 pt below; only extended to page 3, never altered.
- Page 2: still 5 as hero at hero_h 860 and the centred crop; the 26/40 -> 22/34.5 step from logline to synopsis; mixed-case running text; the PROOF slug until 2.1 / 2.2 are filled.
- Page 3: single right-hand alignment edge at xr = 1222 for title, specs, team, cast, rights, links, footer; RIGHTS directly above LINKS; footer at M + 24; live mailto / URL annotations; ghost of still 41 at alpha 0.22 / scrim 0.50 (the kit's reference ground intensity, text-free mean L ~17).
- Page 4: the signature's DIM 15.2 pt tracked treatment (only its position moves); `title()` as is.
- Pages 5–6: portraits at 0.84 aspect, focus (0.5, 0.40), no frame lines, low-key sepia on black merging into the ground, left/right alternation, 48 pt portrait-to-text gutter, ROLE | NAME lockup in Bask-SB 21 pt tracked 2.2 (F13 refuted). Do not alter any delivered headshot master.
- Page 7: still 40 as hero, focus (0.5, 0.35); heading at 24 pt; DIM role / CREAM name two-tone with the 210 pt name offset.
- Page 8: 6 pt gutters, full bleed to top, left and right, no captions; `KOM_Day3_TheFarm-220` and `-185` stay.
- Pages 9–10: the credit-card rhythm — role right-aligned DIM 14.2, name left CREAM 15.6, centred axis at W/2 ± 26, 52/56 pt gutter, 21 pt lead, 15 pt gap, department heads in small DIM caps with the 6 pt lift, two-column `balance()`; do not enlarge or restyle.
- Page 11: fellows listed by discipline, the (c) line, the thanks list centred; only measure, anchor, divider length, label size and ghost pick move.
- Ghost grounds on pages 3, 9, 10, 11 at their current alpha / scrim (0.22/0.50 and 0.16/0.55); only page 4's alpha changes.
- `para()` with setCharSpace(0) so heading tracking never leaks into body wraps.
- Selectable text on every page and real PDF link annotations.

## Open questions for Luke

1. F01 — Which BTS frame stands in for the director's portrait: `KOM_Day3_TheFarm-43`, `-45`, `-46`, or the centre figure of `KOM_Day4_Soundstage-93`? Confirm the chosen frame shows Jordan Betine. If none is approved, the page ships on the code fallback (narrow measure, ~200 pt block, 91 pt gaps).
2. F08 — Ruoxiao Li's head fills ~28 % of her box against ~40 % for the other three. A crop-only `PORTRAIT_ZOOM = {2: 1.25}` with focus (0.5, 0.42) would match her; it changes how a delivered headshot is cropped, so it is a separate yes/no and ships only after a render check.
3. F14 — Keep the 74 pt credit strip on page 8, or delete the strip and bleed row 4 to the foot as the model kit does? Jedidiah Woods is already billed Still Photographer on page 10, so the strip line is a duplicate. The list above assumes the strip stays.
4. F10 — Confirm the two cuts (`KOM_Day3_TheFarm-99`, `IMG_4467`) and that the 1296 x 439 centre crop of `KOM_Day3_TheFarm-237` keeps every head; fallback row heights are given.
5. Card module — F11, F15, F17, F18, F21 and F22 edit `build-credit-card.py`, which also builds the standalone credit card at --medium / --large. Edit in place (changes flow to the card) or fork the kit's copy?
6. F12 — BRAND.md's type table row (line 96) documents the page 3 title at 30 / 4.0; update it in the same commit so the table stops contradicting the build?
7. F02 — hero_h 1230 is provisional on field 7.1 (cast bio) staying empty; who supplies that copy, and when?
8. F03 — With the 720 pt measure the signature lands 177 pt from the foot (measured). Accept that foot margin, or accept a wider measure (760–860 pt, fewer lines, signature higher on the page)? The list assumes 720, the narrowest width at which `fit()` still holds 23 pt.
