# KILLER OF MEN — Branding Bible

**v0.1 DRAFT, unratified, 2026-09-09.**
Luke ratifies; until then chapters marked DEFINED bind per the playbook's defined-is-binding law, chapters marked MISSING do not.
Machine layer: `tokens.css` beside this file. Playbook: `$HOME/BMF Headquarters/DOCTRINE/PLAYBOOKS/branding-bibles.md`.

**Method.** Every hex is a median of masked pixels from the artifact named beside it (Pillow 11.3, numpy 2.0, `/usr/bin/python3`, 2026-09-09), never eyeballed. Constants come from `tools/build-credit-card.py`, confirmed against rendered EPK pages. Contrast is WCAG 2.x, computed. The dataviz validator (`scripts/validate_palette.js`, bundled skill 2.1.260) was run; verdicts in chapter 3. Sampler scripts are uncommitted — PROPOSED: `tools/sample-brand.py` at ratification.

---

## 1. ID and idea — DEFINED (facts), PROPOSED (principles)

| Field | Value | Source |
|---|---|---|
| Name | KILLER OF MEN, always capitals on surfaces | poster, EPK p03, credit card |
| What it is | 13-minute AFI Conservatory thesis short. Historical drama, Southern gothic. 2.39:1, 24 fps, ALEXA 35 ARRIRAW, 5.1 and stereo. Shot California 2025, completed 2026 | EPK p03 |
| Writer-director | Jordan Betine | poster billing, EPK p03 |
| Rights holder | AFI Conservatory | EPK p03 |
| Version, place | v0.1 DRAFT, `FESTIVAL CAMPAIGN/site/BRAND.md` | this file |

Principles, PROPOSED. Each is observed in the artifacts, not invented:

1. Two palettes, never mixed. The poster paints; every document prints.
2. Assets are placed, never re-set: no re-lettering, re-colouring, or cropping a still's letterbox.
3. One type family. Letterspaced capitals for titles and labels; sentence case for reading.
4. Value before hue. Documents are tonal, cream on warm near-black; the single hue is the reserved emphasis, currently unspent everywhere.
5. Clean Bank. Documents about the film carry zero personality.

## 2. Logo suite — MISSING, owner Jordan

The only mark is the hand-lettered title on the poster (`press/assets/POSTER/KillerOfMen_Poster_2160x2700.jpg`, bottom band; lettering `#efeca1`, drop shadow `#df0001`). No separate file exists. Until one does, the title on documents is set in type per chapter 4, never traced from the poster.

| File needed | Purpose | Owner |
|---|---|---|
| Title lettering, transparent PNG, 4000 px wide or more | stills, laurel posters, social tiles | Jordan (source: the poster artist) |
| Title lettering, vector (AI or SVG) | print at any size | Jordan |
| Variant for cream ground, if ever approved | light-ground use | Jordan |
| Lockup: "AFI CONSERVATORY PRESENTS" over the title | EPK p01, trailer card | Jordan |
| AFI Conservatory logo, official file | required on the end card by `press/epk-spec.md` p11; absent from `press/assets` and from rendered p11 | Luke (source: AFI) |

## 3. Colour — DEFINED (print), DEFINED (paint, as reference), PROPOSED (emphasis)

Two palettes and one material. **PRINT** is every document surface: EPK pages 2–11, credit cards, one-sheets, cover letters, readouts. **PAINT** is the poster and only things that are the poster: laurelled variants, social tiles cut from it, EPK page 1 where the poster is a placed image on the print ground (p01 corners sample `#0a0805`; the spec says full-bleed, the render is not — for Luke). **FILM** is the stills: placed whole, never a source of type or fill colour.

Law: PAINT hues never appear as type, rule, or fill on a document. PRINT tokens never overpaint the poster. They share no hex; the grounds are neighbours (`#100100` poster darkest 5%, `#0b0806` print).

| Token | Hex | Role | Law | How sampled |
|---|---|---|---|---|
| GROUND | `#0b0806` | page ground | never pure `#000000` on a page; the only document ground | constant in `tools/build-credit-card.py`; EPK p02 render median `#0a0805` |
| CREAM | `#efe6d6` | primary type: names, running text, page titles | the reading colour; never tinted or at reduced opacity | constant; EPK p02 body and p03 title mode `#efe6d6` |
| DIM | `#b9a88c` | secondary type: role labels, section labels, captions, footers a reader needs | labels only; never running text | constant; EPK p02 section label brightest `#b8a88c` |
| RULE | `#6b5942` | hairline rules 0.5–0.7 pt; department headings in the credit columns | 2.98:1, just under the 3:1 large-text line: structure only, where the grouping already tells the reader what the heading says; never labels, footers or running text (the proof slug moved to DIM on 2026-09-09) | constant; p02 footer at 9.5 pt samples `#584936` (antialiased) |
| LETTERBOX | `#000000` | the stills' own bars | travels with the still; never a page ground | median of bar rows across all 41 stills |
| GHOST | `#0e0e0a` | measured result of a still at 22% under a 50% GROUND scrim (page 3). The family in use on pages 3 and 4: 0.22/0.50 and 0.20/0.50. **Pages 9–11 CONTESTED**: the redesigned card draws the still at 1.0 / 0.60 / 0.45 with no scrim (`GROUND_RECIPE` in `tools/build-credit-card.py`) | a recipe family, not a paint colour; a ghost needs a centre-crop mean luminance of about 70 or more to read at all | EPK p03 right-column median |
| EMPHASIS (PROPOSED) | `#df0001` | the one reserved hue | at most one instance per surface; type 18 pt and up, rules, markers only; never body text, never fill; unused on every current surface | median of red drop-shadow pixels behind the poster title (8,652 px) |
| PAINT red | `#be2e13` | poster glow, title shadow | poster only | median of pixels hue 345–12°, S>0.55, V>0.35 (3.6% of frame) |
| PAINT orange | `#a7682c` | sunset band, skin, wood | poster only | hue 15–42° band (28% of frame); pure sunset region `#fe5907` |
| PAINT yellow | `#f6e62c` | sky | poster only | hue 45–68° band (5.8%); sun core `#fbd012` |
| PAINT green | `#688d2b` | moss | poster only | hue 80–165° band (1.5%) |
| PAINT blue | `#006b97` | the ragged frame | poster only | hue 185–235° band (6.5%); border strips `#006a97` |
| PAINT cream | `#efeca1` | title lettering, billing block | image only; documents use CREAM | median of pale low-saturation pixels in the bottom band (76,116 px) |

Emphasis alternative for Luke: red-band median `#be2e13` (3.41:1). The drop-shadow red is the one red the poster artist placed deliberately and clears 3:1 with more margin. The film's own red, the elder's headwrap (`#5f1c14`, still 1.1.18), fails at 1.58:1: material, not a token.

Contrast of every text-capable token against every ground (WCAG, computed):

| Token | on GROUND `#0b0806` | on LETTERBOX `#000000` | on GHOST `#0e0e0a` | Verdict |
|---|---|---|---|---|
| CREAM `#efe6d6` | 16.13:1 | 16.96:1 | 15.62:1 | AAA any size |
| DIM `#b9a88c` | 8.60:1 | 9.04:1 | 8.33:1 | AAA any size |
| RULE `#6b5942` | 2.98:1 | 3.13:1 | 2.89:1 | fails 3:1 on GROUND — lines and provenance only |
| EMPHASIS `#df0001` | 3.94:1 | 4.14:1 | 3.81:1 | large text and graphics only (3:1); fails body (4.5:1) |
| PAINT red `#be2e13` | 3.41:1 | 3.59:1 | 3.31:1 | reference only |
| PAINT yellow `#f6e62c` | 15.48:1 | 16.27:1 | 14.99:1 | reference only |
| PAINT blue `#006b97` | 3.38:1 | 3.55:1 | 3.27:1 | reference only |
| PAINT cream `#efeca1` | 16.34:1 | 17.18:1 | 15.82:1 | reference only |

EMPHASIS on CREAM 4.10:1. CREAM on RULE 5.41:1. DIM on RULE 2.89:1 — never DIM type on a RULE fill.

Validator (`--mode dark --surface #0b0806`): print text tokens FAIL lightness band and chroma floor, WARN on RULE at 2.98:1; CVD separation PASS (ΔE 18.8), normal-vision PASS (19.0). Poster hues FAIL: orange–red ΔE 4.3 deutan, 11.3 normal; yellow out of band. Neither set is a chart palette. Because the band and chroma checks are built for chart series, neither their FAIL nor their PASS results bear on a text palette; only the CVD-separation figure is informative here, and it is recorded as such. Law, PROPOSED: charts about the film use the dataviz reference palette's dark-mode steps on GROUND until a brand categorical set is validated.

The contrast table measures against a median ghost. Behind actual text on page 4 the ground varies; local DIM contrast falls to about 6.5:1 at the brightest points (still AA), CREAM stays above 12:1.

## 4. Type — DEFINED

One family. `/System/Library/Fonts/Supplemental/Baskerville.ttc`: index 0 Baskerville Regular, index 4 Baskerville SemiBold (names read from the file). Fallback stack in `tokens.css`; if Baskerville is missing, stop and say so rather than substitute.

| Face | Job | Restraint |
|---|---|---|
| Baskerville Regular | page titles, labels, names, running text, boilerplate, footers | everything except headings that lead a block |
| Baskerville SemiBold | section and person headings (SUB), department headings, the billed lead line | headings only; never running text |

Sizes and tracking at scale 1.0, in points, from `tools/build-credit-card.py` and `tools/build-epk-kit.py`:

| Element | Face | Size / lead | Tracking | Case | Colour |
|---|---|---|---|---|---|
| Page title (CAST, CREW, THANKS, DIRECTOR'S STATEMENT) | Regular | 40 | 6.0 | caps | CREAM |
| Page-3 title | Regular | 40 | 6.0 | caps | CREAM — the title law, right-aligned, since 2026-09-09 |
| Section label (LOGLINE, SYNOPSIS, BILLED CAST, the THANK line) | Regular | 15.6 | 2.35 | caps | DIM |
| Programmer-page column (specs, team, cast, rights, links, footer) | Regular | 19 / 28 | 0.95 | caps | key DIM, value CREAM; links underlined 0.5 pt DIM |
| Programmer-page section head | SemiBold | 24 | 2.2 | caps | CREAM |
| Section / person heading | SemiBold | 21 | 2.2 | caps | CREAM |
| Billed lead line | SemiBold | 24 | 2.2 | caps | CREAM |
| Department heading | SemiBold | 14.2 | 2.05 | caps | RULE |
| Role label | Regular | 14.2 | 1.35 | caps | DIM |
| Name | Regular | 15.6 / 21 | 0.95 | caps | CREAM |
| Running text | Regular | 15.6 / 24.5 | 0 | sentence | CREAM |
| Logline | Regular | 26 / 40 | 0 | sentence | CREAM |
| Synopsis | Regular | 22 / 34.5, fit-down | 0 | sentence | CREAM |
| Director's statement | Regular | 23 / 36.5, fit-down to 9 minimum | 0 | sentence | CREAM |
| Small text | Regular | 12.4 / 18 | 0 | sentence | CREAM |
| AFI boilerplate | Regular | 11.4 / 17 | 0.95 | caps | CREAM |
| Provenance footer (proof slug) | Regular | 9.5 | 1.4 | caps | DIM |
| Behind-the-scenes credit strip | Regular | 14.2 | 1.35 | caps | DIM |

Never-rules: the poster title is an image, never re-set in any face. Tracking scales with size (`Sz`); no hand-tuned lines. Enlarged cards (1.30x, 1.75x) stack role over name, centred. Names are never clipped: condense tracking, then size (`condense()`). No second family or italic. **Bold (index 1): CONTESTED** since 2026-09-10; the redesigned credit card sets every credit in Baskerville Bold (see the redesign table below).

The rows above that describe the credit pages (page titles CAST / CREW / THANKS, department heading, role label, name, AFI boilerplate) are **CONTESTED** for pages 9–11 as of handoff-105-epk; the card's own values are in the redesign table. They stand for pages 1–8.

## 5. Mark geometry — MISSING, owner Jordan

Clear space and minimum size follow the logo files (chapter 2). Page geometry in use is DEFINED for pages 1–8: 1296 × 1728 pt pages, 74 pt margins, heading rule 236 pt wide, 0.7 pt, 22 pt below the title baseline; list dividers 0.5 pt. **CONTESTED for pages 9–11**: the redesigned CREW page runs 48 pt side margins and the card titles carry no rule (handoff-105-epk).

## 6. Voice

**Document voice — DEFINED.** Clean Bank on every surface an agent makes: EPK, credit cards, readouts, one-sheets, cover-letter templates. Zero personality, taglines, or codas. Idiom in use: `ROLE  |  NAME`, two spaces around the pipe; ` · ` between co-credited names; capitals throughout; "WRITTEN & DIRECTED BY". Plausible and wrong: a tag line under the title on a document page.

**The film's own voice — MISSING, owner Jordan.** Not defined here. Unratified raw material: loglines A and B in `press/filmfreeway-page-v6.md`, `press/synopsis-draft.md`, the director's statement on EPK p04. EPK p02 still carries a proof footer marking logline and synopsis as drafts.

## 7. Icons — MISSING, owner Luke

None in use. `press/epk-spec.md` calls for Instagram and IMDb glyphs on bio pages; none drawn. Until then, links are DIM capitals as on EPK p03.

## 8. Texture and material — DEFINED (measured)

- Stills: 41 PNG frames, 1920 × 1080, picture rows 137–943 (2.38:1 inside 16:9), letterbox `#000000`. Placed whole, bars intact. The credit card un-letterboxes only its own 16% backdrop copy; delivered stills are never altered.
- Grade: low-key, warm. Mean luminance 42/255 (median 34); 25 of 41 stills below 40, one above 100; warm midtone `#69401d`, hue 28°.
- Ghosting, the approved family: a still at 16–22% on GROUND under a 50–55% GROUND scrim. In use: 0.16/0.55 (pages 9–11), 0.22/0.50 (page 3), 0.20/0.50 with focus 0.62 (page 4). Measured result on page 3 `#0e0e0a`. Only stills whose centre crop averages about L 70 or more are used as ghosts; darker frames disappear.
- Grain is in the ALEXA 35 material, unmeasured here. No synthetic grain, paper, or vignette on any surface.

## 9. Motion — MISSING, owner Luke

No moving surface exists beyond the film and a trailer not in the repo. When one does: ease for system, spring for user, one moving thing, `prefers-reduced-motion` honoured (`widget-mastery.md` §4).

## 10. Applications — DEFINED (inventory)

| Surface | Palette | File(s) | State |
|---|---|---|---|
| Poster, key art | PAINT | `press/assets/POSTER/KillerOfMen_Poster_2160x2700.jpg` (2160 × 2700) | delivered, never altered |
| EPK, 11 pages | PRINT; PAINT on p01 as a placed image | `press/KillerOfMen_EPK_<HHMM>_<DDMMYYYY>_compressed.pdf`, latest wins (1922 and 1954 of 09092026 present); builder `tools/build-epk-kit.py`; spec `press/epk-spec.md` | proof; logline and synopsis unlocked |
| Credit cards, three sizes plus transparent | PRINT | `press/KillerOfMen_Credits*.pdf`; PNGs `press/assets/CREDITS/` (20); Illustrator `press/illustrator/*.ai` (3); builder `tools/build-credit-card.py` | built |
| FilmFreeway page | none — platform chrome, text only | `press/filmfreeway-page-v6.md`, `.docx` | draft v6 |
| Website | not sampled | https://www.killerofmen.com/ — Wix landing page with GoFundMe link; dark ground, white type per fetch; hexes and fonts MISSING | live, off-Bible |
| Stills, contact sheet | FILM | `press/assets/STILLS/` (41 PNG + `contact-sheet.jpg`) | delivered |
| BTS, headshots | FILM / photography | `press/assets/BTS/` (103), `press/assets/HEADSHOTS/` (4) | delivered |
| Social tiles, laurel posters | PAINT | none exist | MISSING, owner Luke |
| Internal readouts (`index.html`, `board.html`, `docket.html`, `epk.html`) | campaign board palette (`#0f1930` ink, Archivo) | site root | not governed by this Bible; Clean Bank applies |

---

## Counter-evidence and open risks

Recorded from a cross-family audit (Codex, read-only, 2026-09-09; verdict UNSOUND as a binding standard, arithmetic mostly accurate). Each is a question for Luke at ratification, not a settled law.

| Risk | Evidence | What it would take to settle |
|---|---|---|
| The print laws ratify what the credit-card tool happened to do | The card was designed first, the EPK inherited it, the Bible came third (handoff-100) | Luke decides whether cream on warm near-black is the look, or a default that stuck |
| Effective type size when the 18 × 24 in page is printed at Letter | 15.6 pt body becomes 7.4 pt; 9.5 pt footer becomes 4.5 pt. The programmer page was raised to 19 pt on 2026-09-09 for this reason | Declare the kit screen-first, and set a print rule (print at 18 × 24, or scale type) |
| The print palette is untested with its audience | No programmer has read the kit; no light-ground alternative exists | One read-through by a programmer, or a light-ground page for comparison |
| PAINT is quarantined | The poster is the film's only distinctive brand asset; documents carry none of it | Luke's call: one PAINT accent on documents, or none |
| RULE at 2.98:1 carries department headings | Just under the 3:1 large-text line | Accept as structure-only, or step department headings to DIM |
| The sampler is not committed | One re-run of the red mask gives `#bd2f13` against `#be2e13` here | Commit `tools/sample-brand.py` and re-run every hex from it |
| Validator results are not evidence either way | The dataviz checks are built for chart series | Keep only the CVD-separation figure; find a text-palette check |

## Contested by the credit-card redesign — PROPOSED, for Luke

On 2026-09-09 Luke redirected the credit cards to the Night Feeds EPK as the guide ("using this as the guide, edit and improve upon the full credit cards"). The rebuilt card (handoff-105-epk, `tools/build-credit-card.py`) deviates from the DEFINED entries above on purpose. Per the playbook's law, a deviation is proposed here, not silently made. Each row is a PROPOSED amendment; the affected DEFINED rows are marked CONTESTED until Luke rules.

| | What the card now does | What the Bible defined | Scope |
|---|---|---|---|
| a | Every credit in Baskerville **Bold** (index 1, `Bask-B`); SemiBold no longer drawn on the card | no Bold; SemiBold for headings only | type |
| b | Role labels in **CREAM**; DIM survives only on the two logo-slot labels, the CONTINUED tag and, under `--label-gold`, three wayfinding labels | role labels DIM | colour |
| c | Department headings **off** by default; under `--headings` they are CREAM 17 pt tracked 3.0 | department headings RULE, SemiBold 14.2 | type, colour |
| d | The still is the page: drawn once at **1.0 / 0.60 / 0.45** (CREDITS / CREW / THANKS) with **no scrim**, horizontal anchor 0.20 / 0.50 / 0.70; enlarged sets use still 1.1.27 at 0.45 | ghost family 0.16–0.22 under a 0.50–0.55 scrim | texture |
| e | Titles are single words **CREDITS / CREW** at 60 / 56 pt tracked 2.0, no rule | spaced "C A S T" at 40 pt tracked 6.0 with the 236 pt rule | type |
| f | Poster-block names 26 / lead 30; cast rows 20; crew 17; page-3 body 20; boilerplate **Bold 20 pt CREAM on a 1160 pt measure** | name 15.6 / 21; boilerplate Regular 11.4 / 17 | type |
| g | CREW side margins **48 pt** | 74 pt page geometry | geometry |
| h | A tracking table of 1.0–4.0 by element | Sz-scaled 6.0 / 1.35 / 0.95 | type |

The question these rows raise is larger than any row: pages 1–8 of the EPK are cream Baskerville Regular on warm near-black with ghosted stills, pages 9–11 are now the Night Feeds form. **Either the whole kit follows the redirect or the credit pages stand apart as a second object.** That is Luke's ruling, and it settles every row above at once. `tokens.css` is untouched until he rules.

## Amendments

- 2026-09-09 — v0.1 DRAFT written from the artifacts. Awaiting Luke's ratification.
- 2026-09-10 — Credit-card redesign contradictions appended as PROPOSED (rows a–h, from the builder's deviations report via the card session, handoff-105-epk); the DEFINED rows they touch marked CONTESTED for pages 9–11.
- 2026-09-09 — Codex audit folded in: GHOST corrected from a single recipe to the family actually in use; RULE law narrowed to structure only; type table updated for the page-3 title law, the label class, the 19/28 programmer column and the DIM proof slug; counter-evidence table added.
