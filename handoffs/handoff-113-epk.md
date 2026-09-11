# handoff-113-epk

## Where we left off, newest first

1. **The taste-pass draft of the EPK is built and in the repo, for Luke's review.** `press/drafts/2026-09-11/`: the eleven-page draft PDF (`KillerOfMen_EPK_draft_2026-09-11.pdf`, 11 pages, 20 live links, 4.2 MB, not released and not on the Drive), a before/after review sheet with every changed region boxed (`index.html`, served by GitHub Pages once pushed; also published privately as a Claude artifact), `review.md`, `notes.json` (the changes and the CONFIRM list per page), the page-9 comparison variant in page 3's idiom (`p09-variant-kit-idiom.pdf`), `evidence/` (the critics' measured mocks) and `research/taste-pass-2026-09-11.json` (four reference lanes, seven critics, the synthesis, three refuters). Page 3, the page Luke named as the north star, is untouched. The layout that produced it is `tools/build-epk-kit.py`; the shipped release `press/KillerOfMen_EPK_1544_10092026_compressed.pdf` is unchanged.

   | Page | Verdict | What changed |
   |---|---|---|
   | 1 | unchanged | spec row 1 and the Bible's note amended so no builder crops the poster to "full bleed" |
   | 2 | adjusted | hero 860 → 720 pt cropped from the frame's left edge (the owner in the doorway stays in; 76 % of the DP's frame instead of 63); measure 900 → 820; the block placed by a 3:5 split of its spare |
   | 3 | unchanged | the north star |
   | 4 | redesigned | page 3's armature: still 1.1.10 at focus 0.83 (Mace's back whole in the left third), title right-aligned to xr, a 686 pt flush-left column at 536–1222, the director's own seven paragraph turns restored (they were folded into one 17-line block); lands at 21.5 / 33.8 |
   | 5 | adjusted | the director has a portrait: set photograph Day3-43, crop-only zoom 1.15, value-graded at draw time to sit beside the studio headshots (masters untouched), behind a PROOF slug until Luke confirms the man is Jordan Betine; blocks anchored title-to-foot with 66 pt gaps; handles and IMDB in the label class with page 3's underline; one text edge at M on every block, only the portrait alternates |
   | 6 | adjusted | alternation continues across the turn (RJ right, You Wu left); the two blocks as one group a little above centre; prose flush-left |
   | 7 | redesigned | the broken page (provenance notes printed as copy, the list off the foot, Kojo's face over the lead's name) rebuilt in page 3's form mirrored: CAST under the title law at the left edge, four ROLE \| NAME lockups over their bios flush-left on a 600 pt measure, the five other billed names under ALSO BILLED, still 1.1.17 ghosted in the right third with Mace's face looking into the column; field 7.1 is parsed so the notes never print and a PROOF slug marks the bios as drafts |
   | 8 | adjusted | rows read as the shoot: the farm by day (84, 59, 152), the barn and the fight (194, 185, 220), the soundstage and the burial (76, 81, 93), the unit; two illegible cells replaced (149 → 194, Soundstage-32 → 76); the barn-yard wide (84) opens the page |
   | 9 | adjusted | within the Night Feeds form: still 1.1.29 (the spirit blur) → 1.1.2, the cupped hands with the shells, anchor 0.35, alpha 0.75 (gated: 1.0 fails at p95 72, 0.85 at 63, 0.80 scrapes 59.9, 0.75 passes at 56 against 60) |
   | 10 | adjusted | still 1.1.27 alpha 0.60 → 0.45 (gate p95 32 against 65); SOUND DESIGNER \| STILL UNKNOWN no longer printed as a credit (press mode) and the page carries PROOF — SOUND DESIGNER NOT YET NAMED; the two exact duplicates (Still photographer, Colorist) printed once on both the kit's and the card's path; CREDITS and CREW titles one size (56) |
   | 11 | adjusted | still 1.1.25 at 0.35 anchored 0.50, the lantern as fog behind the middle column (gate p95 40 against 75); the PARTNER LOGOS band drawn only when field 11.2 holds logos (the legal block stays anchored 90 pt above the AFI box, so the air lands between the thanks and the Avid line) |

   The stills are the DP's frames cropped at draw time; every fact on every page still comes from `press/epk.json` rev 24; nothing was retyped.

2. **How the draft was made, so the next session can trust or distrust it.** A 15-agent workflow: four reference lanes (Cannes 2025 short kits VULTURES and ALI, the ShortsTV Oscar-shorts kit, Janus press notes for Godland and Four Nights, AFI's Blue Hour and peer theses, Szarkowski and Tschichold on the asymmetric page; the renders are in the session scratchpad only, third-party PDFs were not committed), seven critics over the current pages against page 3, a synthesis (12 changes kept, 15 rejected), then three adversarial refuters: taste refuted 0 of 12 with five amendments taken (no prior-credits line in DIM, one text edge per bio block, keep the barn-yard opener on the evidence of the render, never print STILL UNKNOWN, gate page 11), law refuted 1 (never pre-fill the exhibition formats; that is You Wu's fact, to be written through `tools/epk.py`), implementability refuted 3 (the cupped hands fail the gate at 1.0; the Illustrator replay lacked `zoom` and dropped the grade, and its page 6 lacked `offset=3`; the duplicate filter had to sit on both card paths). All of it is applied. My own prototypes ran ahead of the list: a four-frame grid for page 7 was built, rejected by the synthesis as a fourth image treatment, and kept in `evidence/` only. **Fable 5.1, ultracode; a goose turn on a brief Luke gave and then widened ("continue to refine and develop this EPK … execute a draft fully").**

3. **The replays hold.** The Illustrator recorder and the Canva emitter replay the new layout: 11 pages, 410 elements, 23 images, 20 links attached, 0 unattached; the crop-only zoom is encoded as a tighter region; the director's grade is baked into the Canva derivative (`grade_mono_pixels`), while the `.ai` links the ungraded master by that tool's contract and now prints a NOTE saying so. **The Canva contract on GitHub Pages is still rev 24 of the old layout**; regenerate with `tools/build-epk-canva.py` and push only after Luke accepts the draft, or the app builds the superseded kit. **The six standalone credit-card PDFs in `press/` are stale against the card module** (title 56, duplicates once, band gated); the card lane rebuilds them with the gate.

4. **Codex audit of the Canva lane: UNSOUND, eight findings, no invented SDK call, all eight answered the same day** (commit `49717db`): link expectations corrected to 18 live links (the two mailto rows are plain text by design); the app refuses to build until every font key is resolved in the current panel session and fails an element rather than fall back to Canva's default font; a manual page-width control for the fresh-design case (unverified in Canva); scopes in the runbook's step 3 and the hint on both `missing_permission` and `permission_denied`; `press/canva-plan.md` carries a superseded banner with its four corrections; the pilot check reads the last page; `design.url` is copied by hand; every image upload awaited. Typecheck, lint and build clean. The table is in `canva/kom-epk-builder/BUILD-REPORT.md`.

5. **Pre-flight (runbook step 0): machine checks PASS, zero MISSING lines.** The four questions were asked and are unanswered (Luke stepped away): the Claude in Chrome extension signed in to this account; which Chrome is logged in to Canva Pro (two Chromes are connected, Browser 1 and Browser 2, and a pick or a Connect click is his); whether he is at the keyboard for the Developer Terms click; whether the decisions in `STATE.json` still hold. **Nothing inside Canva was started**, by the runbook's own gate.

## Next action (the one thing)

**Luke reads the review sheet and rules**, page by page, on the CONFIRM list; the ruling that settles the most is one object or two (page 9 beside its variant). Then the four pre-flight answers, and the Canva lane resumes at runbook step 3.

## What blocks a shippable kit (data, not design)

| Gap | Where it shows | Owner |
|---|---|---|
| Logline and synopsis chosen (fields 2.1, 2.2) | page 2 PROOF slug | Jordan |
| The director's portrait is Jordan Betine (Day3-43) | page 5 PROOF slug | Luke |
| Cast bios approved by the actors; Sandra McDaniels' own bio | page 7 PROOF slug | Jordan, the actors |
| Sound designer named | page 10 PROOF slug | Jordan |
| Exhibition formats (3.12), written through `tools/epk.py` | page 3 row absent | You Wu |
| Partner logos (11.2) and the AFI Conservatory logo file | page 11 slots | Luke, AFI |
| BETINE or UWHUBETINE in the fellows; MMXXV or MMXXVI | page 11 | Jordan, Luke |
| Instagram and IMDb per cast member (spec row 7; no field holds them) | page 7 | Luke |

## Open questions for Luke

1. One object or two: pages 9–11 in page 3's recipe (the variant) or the Night Feeds form with today's three still fixes. Settles BRAND.md rows a–h.
2. Page 7's ghost: still 1.1.17 (Mace's face into the column, as drafted) or 1.1.15 (his figure at the oak, which loses the crown in the crop). Is the man Mace?
3. Page 4: accept the focus-0.83 crop with the owner's hand entering from the edge, keep both figures with a flush-left column, or name another single-figure still. Pages 3 and 4 now share one arrangement (figure left, column right); mirror page 4 or keep the pair?
4. Page 2: is the man in the waistcoat Master Kenner (inference), and is the wide crop of your frame accepted?
5. Page 5: the Ruoxiao Li crop-only zoom (two dict entries, `PORTRAIT_FOCUS["5.2"]`, `PORTRAIT_ZOOM["5.2"]`), yes or no.
6. Page 7: the label word ALSO BILLED; the bios cut toward 90 words each (owner Jordan, then the actors).
7. Page 10: keep the 9.1 tail on CREW (minus exact duplicates) or let 10.1 carry those names alone.
8. Page 11: a black end card rather than the faint lantern (the taste reviewer's preference); the legal block at Regular 15.6 on a narrower measure (deferred behind question 1).
9. The card module was edited in place (sexy-pass question 5): title 56, duplicate filter, band gating, a `proof_slug` option. Keep in place or fork.
10. Page 8: keep the 74 pt credit strip (the draft keeps it).

## Record hygiene done this turn

`BRAND.md` Amendments carry the pass as PROPOSED (crop-at-draw-time practice; the statement at 21.5 / 33.8; page 7's lockup class; flush-left prose; the two-position title rule); `press/epk-spec.md` rows 1 and 2 and the 2026-09-09 build note amended; `press/sexy-pass-changes-2026-09-09.md` marked superseded in part; `tools/requirements.txt` gains numpy (the card's gate needs it); `tools/epk-review-sheet.py` is new (before/after sheet with change boxes, reusable for any draft). The shipped PDF's page 4 was not built from the code on disk (right-aligned in the PDF, centred in the code); the review sheet's "before" is the shipped PDF and says so.

## Playbook material, offered

The taste-pass shape (measured critics against a named north star → one synthesis → three refuters with different lenses → the gate as the acceptance test) and the review-sheet tool are reusable for any visual draft. Not filed to DOCTRINE without Luke's word.

---

**Timestamp:** 2026-09-11 · **Lane:** `epk` · **Continues:** handoff-112-epk.md · **Model:** Fable 5.1, ultracode. Handoff number chosen by a gating existence test.

## Files

- The draft PDF: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/drafts/2026-09-11/KillerOfMen_EPK_draft_2026-09-11.pdf
- The review sheet (after push): https://scroggdawg.github.io/kom-festival-board/press/drafts/2026-09-11/index.html · as a private artifact: https://claude.ai/code/artifact/f173bf5a-02ca-4fe5-8442-4963afa412e2
- The notes and CONFIRM list: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/drafts/2026-09-11/review.md · https://github.com/Scroggdawg/kom-festival-board/blob/main/press/drafts/2026-09-11/notes.json
- The page-9 variant: https://github.com/Scroggdawg/kom-festival-board/blob/main/press/drafts/2026-09-11/p09-variant-kit-idiom.pdf
- Evidence and research: https://github.com/Scroggdawg/kom-festival-board/tree/main/press/drafts/2026-09-11/evidence · https://github.com/Scroggdawg/kom-festival-board/blob/main/press/drafts/2026-09-11/research/taste-pass-2026-09-11.json
- The layout: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-kit.py · the review tool: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/epk-review-sheet.py
- Bible and spec: https://github.com/Scroggdawg/kom-festival-board/blob/main/BRAND.md · https://github.com/Scroggdawg/kom-festival-board/blob/main/press/epk-spec.md
- Canva lane: https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/README.md · https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/STATE.json · https://github.com/Scroggdawg/kom-festival-board/blob/main/canva/kom-epk-builder/BUILD-REPORT.md · the Codex commit: https://github.com/Scroggdawg/kom-festival-board/commit/49717db
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-112-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-113-epk.md
