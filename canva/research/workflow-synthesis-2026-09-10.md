# KILLER OF MEN press kit in Canva: build plan

Date: 2026-09-10. Planner output from verified research (all Canva pages read 2026-09-10; canva.com help pages were read in a rendered browser tab because they return HTTP 403 to fetchers).

## Recommendation

Build the kit with a **Canva Apps SDK replayer**: a small app (`kom-epk-builder`) that Luke runs in the Canva editor from the Developer Portal's Preview button, served from the agent's local dev server, which reads a JSON operation list dumped from the existing recording canvas in `build-epk-ai.py` and replays it with `addPage()` (page background #0b0806, custom dimensions), `createRichtextRange()` (one paragraph per text block, with `fontRef`, `letterSpacingEm`, `lineHeightEm`, and inline `link`), shape elements for rules, and image elements from pre-cropped data-URL uploads. Precede it with a one-hour probe day (PDF import test, font picker test, page-size read) whose results fix the fidelity budget before the two-to-three-day build.

## Why

- It is the only route that keeps **paragraph-level live text and live text links** and is **re-runnable from the worksheet**. Connect REST cannot place any element (verified: no element-level endpoint; only Enterprise autofill `update_design` and page merges exist). Browser automation is 17-33 agent hours for approximate tracking and widths and is not re-runnable. PDF import is fast but re-imports lose all 19 links, substitute fonts, and (inference from the reportlab per-line `textOut` path) will likely deliver body copy as one text box per line, which is hostile to the director and producer editing paragraphs.
- The replayer reuses the exact coordinate set the PDF and .ai already use (build-epk-ai.py's `install()` recorder emits one `area` op per paragraph and one `point` op per tracked heading), so PDF, .ai and Canva stay one layout.
- No review, no plan gate: a free Canva account can create an app, preview it in its own editor, add pages, upload assets by data URL and export PDF Standard. Pro is needed only for uploaded Baskerville, Resize, and Compress PDF.
- Honest fidelity ceiling: Libre Baskerville rather than Monotype Baskerville is the likely typeface at build time (apps cannot access Pro fonts or custom fonts; Brand Kit font exposure to apps is undocumented and expected negative); Canva reflows richtext with its own metrics so line breaks will drift on text-dense pages (3, 4, 9, 10, 11); the page is stored at Canva's screen-pixel size for 18 x 24 in (unpublished factor, probably 96 px/in = 1728 x 2304; a 300-dpi 5400 x 7200 page exceeds the 25,000,000 px² cap), so PDF Print export governs output resolution; ghost stills are set via `transparency = 0.84` in a post-pass; any link sitting on an image (not on words) is added by hand.

## Alternatives

| Path | What it is | Fidelity to PDF | Effort | Gates | Repeatable when worksheet changes | Verdict |
|---|---|---|---|---|---|---|
| Apps SDK replayer | Own app in Preview mode replays JSON ops via addPage / richtext / image / shape | Medium-high: positions, colours, rules, crops, text links exact; typeface Libre Baskerville unless swapped post-build; line breaks drift | 2-3 agent days + 1 h probes | None to build/preview (Free OK). Pro for uploaded Baskerville swap. Enterprise only to distribute the app (not needed) | Yes: re-run per page; in-place text refresh via Design Editing API is a plausible phase 2 (unverified) | Recommended |
| PDF import + fix-up | Drag the 9.8 MB PDF onto Canva; fix fonts, re-add links, swap images | Medium: layout and dark ground survive; fonts substituted; 19 links lost; text likely fragmented per line; 18 x 24 in survival unverified | 15 min import + 2-4 h fix-up | Import: no stated gate. Resize (if page size wrong): Pro+, uses AI credit. Font upload: Pro+ | Partly: re-import is one click but every fix-up (fonts, 19 links, images) repeats | Run as the 15-minute probe and as a stopgap only |
| Connect REST API | Public-in-draft integration: asset upload, design import, export, folders | n/a: cannot place text, images, rules or links; one image at create | 0.5 day | Public-in-draft any plan; Private = Enterprise; Autofill = Enterprise | Yes for upload/export automation only | Supporting role only (optional export automation) |
| Browser automation of editor | Claude-in-Chrome drives T / Position > Advanced / sliders / Cmd+K | Medium at best: tracking and line spacing via sliders and nudges of undocumented step; text-box widths approximate | 17-33 agent hours, 25-35 wall-clock | None; ToU forbids scraping and bypassing restrictions, silent on human-pace UI input | Poor | Fallback for the few manual steps only (image links, font swap) |
| Canva MCP (mcp.canva.com) | Remote MCP editing transactions | Text replacement on existing elements only; no insertion, no geometry write | n/a | Custom clients waitlisted; self-serve only via pre-approved assistants | Would suit text refresh later, not a build | Not viable now |
| PPTX / .ai / SVG import | Alternative import formats | SVG: no text, no links. PPTX: beta, approximate fonts. .ai: beta, may rasterise | n/a | None | No | Rejected |

## Steps

| # | Who | Step | Check |
|---|---|---|---|
| 0 | Luke | Decide the four items under "Luke must decide" below and record them. Confirm plan tier in Settings > Billing (a rendered Canva help page in Luke's session said "you're using Canva Free"). | Written answers exist; plan tier recorded. |
| 1 | Agent (Chrome) | Probe A, PDF import (15 min): drag `KillerOfMen_EPK_1234_10092026_compressed.pdf` onto canva.com home; open the design. | Page count = 11. Click into a paragraph on p3: count text boxes on p3 vs the JSON's p3 text ops; note substituted font name; count surviving links (expect 0); record the design's stated size (Resize > Custom size units px on Pro; otherwise the size shown in the download dialog). Keep the design as stopgap or delete. |
| 2 | Agent (Python) | Add `--canva-json` to `build-epk-ai.py`'s recorder: dump per page the `area` (paragraph) and `point` (tracked heading) text ops, rule ops, image ops (path, crop box, alpha, target box), link ops (url + rect), all in the 1296 x 1728 pt space; tracking as em (track_pt / size_pt), leading as em. | JSON validates; 11 pages; 24 image ops (18 full-opacity + 6 ghost); 19 link ops; every coordinate within 0..1296 / 0..1728; text op count logged. |
| 3 | Agent (Python/PIL) | Derive images: cover-crop each image op to its target aspect, downsample to <= 2x target px, re-encode until base64 < 10,485,760 chars (~7.5 MB binary). Ghost stills left at full opacity (transparency set later). Write next to the JSON. Never write to `press/assets`. | 24 derived files; each base64 length < 10,485,760; sha256 of every master in `press/assets` unchanged before vs after. |
| 4 | Agent (Node 24) + Luke | `npm i -g @canva/cli`; `canva apps create kom-epk-builder`; `canva apps start` on :8080. Luke: canva.dev Developer Portal > create app, accept Developer Terms, App source > Development URL = http://localhost:8080, click Preview (Chrome). | The preview editor opens with the app panel showing a log pane and buttons "Pick font", "Read page size", "Build page N", "Build all". |
| 5 | Agent + Luke | Probe B, fonts: in the app call `requestFontSelection()`; Luke searches "Baskerville" then "Libre Baskerville"; app logs ref, name, weights, styles. Also call `findFonts()` and log whether any Brand Kit uploaded font appears (expected: no). | Log lines show a ref for Libre Baskerville and its weight list (does 600/semibold appear?). Uploaded Baskerville present: yes/no recorded. |
| 6 | Agent + Luke | Probe C, page size: Luke creates an 18 x 24 in design (Create > Poster 18 x 24 in, or Custom size 18 in x 24 in). Test whether Preview attaches to it or whether the app must be opened from the Apps panel inside it; if neither, the app will `addPage({dimensions})` into the preview design and Luke deletes the default page. App logs `getDesignMetadata().defaultPageDimensions` and `getCurrentPageContext().dimensions`. | Width/height logged in px (expect 1728 x 2304; ratio 0.75 within 0.001). Scale factor = pagePx / 1296 recorded. If `dimensions` is undefined, stop and report. |
| 7 | Agent | Pilot: build page 3 only (text-dense, 9 links): addPage with background #0b0806 and dimensions; images via `upload()` data URL then `addElementAtPoint`; rules as shape rects; each paragraph as richtext with fontRef, fontSize, textAlign, letterSpacingEm, lineHeightEm, formatText colour #efe6d6 / weight / `link`. Sequential awaits with backoff on `rate_limited`. | Element count on the page equals the JSON op count for p3. Export PDF Standard (Flatten off): pypdf finds 9 /Link annots whose URLs set-equal the JSON; `pdffonts` shows embedded fonts and text is selectable; pdftoppm side-by-side vs master p3 with position deltas listed. |
| 8 | Luke | Review the pilot page in the editor: accept or reject the line-break drift, the typeface, and mailto behaviour (test the p3 mailto link in the exported PDF). | Luke's go/no-go recorded; any width or size tweaks written back to the JSON emitter, not hand-edited in Canva. |
| 9 | Agent | Full build, pages 1-11, one page per "Build page N" click, in order. Post-pass with `openDesign({type:"all_pages"})` (fall back to `current_page` per page if all_pages is unavailable): set `transparency = 0.84` on the 6 ghost stills, read back every element's top/left/width/height and dump to JSON. | 11 pages in order (ids returned by addPage). Read-back positions within 1 px of scaled JSON for every element; transparency 0.84 confirmed on 6 elements. |
| 10 | Agent (Chrome) + Luke | Any of the 19 links whose anchor is an image rather than words: select element, Cmd+K, paste URL, Enter. Luke gives the per-action OK for the agent driving his editor. | Export PDF Standard; pypdf link count = 19; URL set equals the JSON link list; each opens correctly, mailto included. |
| 11 | Luke (Pro only) | If Luke chose real Baskerville: split `Baskerville.ttc` into per-face .ttf with fontTools (agent does the split), upload Regular, SemiBold, Bold via Brand > Fonts > Upload a font; in the editor swap fonts (font picker "Change all" if present; otherwise select-all per page). | Font menu shows Uploaded fonts > Baskerville grouped with three styles; export and `pdffonts` shows Baskerville, Baskerville-SemiBold, Baskerville-Bold; visual check of tracked caps. |
| 12 | Agent | Final QA export: Share > Download > PDF Print, RGB, Flatten off, crop marks off, all pages. | `pdfinfo` page size 1296 x 1728 pt on all 11 pages; `pdfimages -list` effective dpi per image logged; per-page pdftoppm diff vs the master with deltas > 0.5% page width listed; file size recorded against 9.8 MB. |
| 13 | Luke | Share > Anyone with the link > Can edit to the director and producer (ask them to sign in so they can comment and download). Keep the edit link private; create a view link for press if wanted. | Each collaborator opens the design and edits one word; Luke sees the edit. |
| 14 | Agent | Handoff: write the re-run recipe (regenerate JSON from the worksheet, rebuild only changed pages, delete the superseded page) and note that a rebuild replaces the page, so collaborator edits on that page are lost unless folded back into the worksheet. | Handoff file exists with working links to the JSON emitter, the app repo, the derived-image folder and the QA reports. |

## Luke must decide before execution

1. **Plan tier.** Stay Free (Libre Baskerville, no Resize, edit-link sharing works, PDF Standard/Print export) or upgrade to Pro (upload Baskerville, Resize, Compress PDF; ~US$180/yr, figure disputed across sources, read canva.com/pricing in a browser). Business is only needed for a team workspace or Brand Templates; not required for collaborators to edit via link.
2. **Typeface.** (a) Split Apple's bundled Baskerville.ttc (fsType 0, technically embeddable; Apple SLA grants use "while running the Apple Software", so uploading to Canva's servers is legally unresolved; copyright Monotype); (b) licence Baskerville from Monotype; (c) Libre Baskerville from Canva's library (whether Canva exposes the 600/SemiBold weight is unverified; test in Probe B). Note: the app will almost certainly build in Libre Baskerville regardless; an uploaded font matters only for a post-build swap in the editor.
3. **Source of truth after handoff.** Worksheet regenerates pages (collaborator edits in Canva on rebuilt pages are lost) or Canva becomes the master after the first build (worksheet frozen).
4. **Line-break tolerance.** Accept Canva's reflow (editable paragraphs, drift on pages 3, 4, 9, 10, 11) or emit one element per line (exact breaks, poor editability, more elements).
5. **Per-action OK** for the agent to drive Luke's logged-in Canva editor for the manual steps (steps 1, 10, 11), at human pace, no undocumented endpoints.

## Risks

- Brand Kit uploaded fonts are expected NOT to be visible to apps (docs: apps cannot access Pro fonts or custom fonts; findFonts returns a subset). Fallback is Libre Baskerville at build time; swap in the editor afterwards on Pro.
- The px size Canva assigns to an 18 x 24 in design is unpublished; 96 px/in is inference. If `defaultPageDimensions` is undefined or the inch validator rejects 18 x 24, the fallback is addPage with 1728 x 2304 px. A 300-dpi page (5400 x 7200) cannot exist in Canva (25,000,000 px² cap).
- `all_pages` openDesign context: the guide page says preview-only while the @canva/design changelog says GA in 2.10.0 (2026-06-12). Plan for per-page `current_page` fallback.
- Whether Preview can open the app inside an existing design is undocumented; step 6 tests it.
- Canva reflows richtext; line breaks will not match reportlab on text-dense pages. Text elements have no height.
- Links via the API exist only on richtext; image-borne links need the editor UI. mailto acceptance is undocumented (third-party guides say it works; test in step 8).
- No published rate limits for addPage/upload; a `rate_limited` error code exists. A ~1,000 element per design ceiling is reported by secondary sources only.
- Exported PDFs embed the full original of any image cropped inside Canva; using pre-cropped derivatives avoids this. Compress PDF is Pro-only.
- Re-running the replayer adds pages; it does not update in place. In-place text refresh via the Design Editing API is plausible but unverified.
- Refuted or downgraded claims from the research: "Canva does not carry Monotype Baskerville" is unverifiable (no public font list); "Libre Baskerville has no SemiBold" is stale upstream (variable 400-700 since 2025) and unverified inside Canva; "imported PDF pages become A4 images" (upload-formats page) is contradicted by Canva's dedicated PDF-import article and reads as the flattened-scan case; "Connect has no editing" is too strong (Enterprise autofill `update_design` GA 2026-08-25 and page-level merges exist) but element-level editing is still Apps SDK only; a font "Change all" swap is in Canva's May 2026 newsroom post but absent from the Help Center.
- Canva Terms of Use (19 Aug 2026) forbid scraping and bypassing access restrictions; no clause on human-pace UI automation was found. Not legal advice.
- Luke's account rendered as Canva Free on 2026-09-10; font upload and Resize are unavailable until upgraded.
- Collaborators editing via link as guests cannot upload, download or copy; they should sign in.

## Sources (all read 2026-09-10)

- https://www.canva.com/help/import-and-edit-pdfs-canva/
- https://www.canva.com/help/upload-formats-requirements/
- https://www.canva.com/help/upload-fonts/
- https://www.canva.com/help/font-upload-error/
- https://www.canva.com/help/resize/
- https://www.canva.com/help/design-from-scratch/
- https://www.canva.com/help/hyperlinks/
- https://www.canva.com/help/download-file-types/
- https://www.canva.com/help/download-flattened-pdf/
- https://www.canva.com/help/pdf-accessibility-features/
- https://www.canva.com/help/collaborate-with-anyone/
- https://www.canva.com/help/moving-elements/
- https://www.canva.com/help/resize-and-crop/
- https://www.canva.com/help/format-text/
- https://www.canva.com/help/canva-keyboard-shortcuts/
- https://www.canva.com/help/screen-reader-editor/
- https://www.canva.com/help/brand-kit/
- https://www.canva.com/help/publish-team-template/
- https://www.canva.com/help/about-canva-business/
- https://www.canva.com/pricing/
- https://www.canva.com/newsroom/news/whats-new-may-2026/
- https://www.canva.com/policies/terms-of-use/
- https://www.canva.dev/docs/apps/prerequisites/
- https://www.canva.dev/docs/apps/previewing-apps/
- https://www.canva.dev/docs/apps/creating-apps/
- https://www.canva.dev/docs/apps/managing-team-apps/
- https://www.canva.dev/docs/apps/design-editing/
- https://www.canva.dev/docs/apps/fonts/
- https://www.canva.dev/docs/apps/elements/
- https://www.canva.dev/docs/apps/api/latest/design-add-page/
- https://www.canva.dev/docs/apps/api/latest/design-add-element-at-point/
- https://www.canva.dev/docs/apps/api/latest/design-create-richtext-range/
- https://www.canva.dev/docs/apps/api/latest/asset-upload/
- https://www.canva.dev/docs/apps/api/latest/asset-request-font-selection/
- https://www.canva.dev/docs/apps/api/latest/design-changelog/
- https://www.canva.dev/docs/connect/llms.txt
- https://www.canva.dev/docs/connect/changelog/
- https://www.canva.dev/docs/connect/authentication/
- https://www.canva.dev/docs/connect/api-reference/designs/create-design/
- https://www.canva.dev/docs/connect/api-reference/assets/create-asset-upload-job/
- https://www.canva.dev/docs/connect/api-reference/exports/create-design-export-job/
- https://www.canva.dev/docs/connect/api-reference/design-imports/create-design-import-job/
- https://www.canva.dev/docs/connect/api-reference/autofills/create-design-autofill-job/
- https://www.canva.dev/blog/developers/canva-and-coding-agents-platforms/
- https://www.canva.dev/blog/developers/launching-new-ways-to-build/
- https://www.canva.dev/docs/mcp/
- https://www.canva.dev/docs/mcp/tools.md
- https://www.canva.dev/docs/mcp/tools/perform-editing-operations.md
- https://www.apple.com/legal/sla/docs/macOSTahoe.pdf
- https://fonts.google.com/specimen/Libre+Baskerville
- https://raw.githubusercontent.com/google/fonts/main/ofl/librebaskerville/METADATA.pb
- file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20(THESIS)/FESTIVAL%20CAMPAIGN/site/tools/build-epk-ai.py
- file:///Users/scrogdawg/BMF%20Headquarters/Previous%20Years/2025%20-%20SEW%20TO%20GROW/25_01%20KILLER%20OF%20MEN%20(THESIS)/FESTIVAL%20CAMPAIGN/site/press/KillerOfMen_EPK_1234_10092026_compressed.pdf
