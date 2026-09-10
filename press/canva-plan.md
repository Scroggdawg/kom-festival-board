# Building the KILLER OF MEN press kit in Canva — plan

*2026-09-10. Research: five lanes over canva.dev and canva.com/help, read in a real browser the same day (canva.com returns 403 to non-browser fetchers), 175 verification passes on the load-bearing claims. Nothing below was tested against Luke's account yet; the first hour of execution is tests.*

## Recommendation

**Build a small Canva app that replays the kit's own operation list into an 18 × 24 in design, page by page.** It is the same architecture the Illustrator project uses (one layout in `tools/build-epk-kit.py`, replayed through a recording canvas), pointed at a third target. It is the only route that is repeatable when the worksheet changes, keeps every text run live, places at exact coordinates, and carries all nineteen links, because every link in this kit sits on text and Canva's richtext API sets links on text.

Three short probes come first and fix the fidelity budget before any build: import the current PDF and see what Canva makes of it; open the font picker inside the app to see which Baskerville is reachable; read the pixel size Canva gives an 18 × 24 in page. Then a one-page pilot (page 3, the text-dense one with nine links) goes to Luke for a go or no-go before the other ten pages are built.

**Account note.** A Canva help page rendered in Luke's own browser session on 2026-09-10 read "you're using Canva Free". On Free the app, the preview, the build and PDF export all work; font upload, Resize and Compress PDF do not until Pro.

## The routes

| Route | What it is | Fidelity to the PDF | Effort | Gate | Repeatable | Verdict |
|---|---|---|---|---|---|---|
| A. Import the PDF | Drag the 9.8 MB PDF onto Canva; text and images become elements | Layout survives; fonts substituted; links lost (undocumented, expect to re-add 19); page size survival unverified; paragraphs likely arrive as one text box per line, because the kit draws each line separately, which is hostile to editing | Minutes to import, 2–4 h to fix up | none (Pro for font upload and Resize) | No: every worksheet change means re-import and re-fix | Run as the baseline test; fall back to it if C fails the font test badly |
| B. Drive the editor by browser automation | Agent clicks, types, uploads in Luke's Chrome | Medium: positions exact via Position › Advanced; tracking and leading are sliders, so approximate | 17–33 agent hours, fragile | none; Canva's Terms forbid scraping, so human pace only | No | Touch-ups only (image links, one-off fixes) |
| **C. Canva app replaying the kit's operations** | Apps SDK: `addPage` with dimensions, richtext runs with font, size, tracking, leading, alignment and links; images by public URL at x, y, w, h | Good, not pixel-identical: Canva reflows paragraphs with its own composer; fonts exact only if uploaded Baskerville is reachable, else Libre Baskerville | 2–3 agent days; 30–60 min of Luke | Developer Portal is free; the owner runs the app in Preview with no review | **Yes**: re-run the emitter and the loop | **Recommended** |
| D. Connect REST API | Server-side API | Cannot place content at all: assets, blank designs, import, export only | half a day | private integrations are Enterprise-only; public-in-draft works | n/a | Use only its export and asset upload, if at all |
| E. Canva MCP server | Remote MCP at mcp.canva.com | Edit operations are text replacement only | | custom clients need a waitlist | n/a | Not for this |

## Facts that shape the plan (verified 2026-09-10)

- **The Connect API cannot place or edit elements.** Its only content-changing calls are Enterprise autofill (`update_design`, GA 2026-08-25) and page merges; element-level editing exists only in the Apps SDK. The "Design Editing API" belongs to the Apps SDK.
- **Apps SDK, current:** `addPage` takes dimensions (each side 40–8000 px, area ≤ 25 M px²), a background colour, and elements. Richtext ranges take `fontRef`, `fontSize`, `textAlign`, `letterSpacingEm` (−0.2 to 0.8 em), `lineHeightEm` (0.5 to 2.5 em) and inline `link`. The kit's tracking and leading values fit those ranges. Images are placed at top, left, width, height from `upload()`, which takes a **public HTTPS URL that does not redirect** or a data URL under 10 MB. No crop or opacity at creation, so crops and the ghosted grounds are baked into derivative images. Design Editing (`openDesign`) can adjust transparency afterwards; its all-pages mode is preview only.
- **Our assets are already public over HTTPS with no redirect:** the repo publishes to GitHub Pages, and `https://scroggdawg.github.io/kom-festival-board/press/assets/...` answers 200 with `image/jpeg` or `image/png`. Derivatives committed beside them are served the same way.
- **The toolchain is present:** Node 24.13.1 and npm 11.8 are installed (the SDK requires Node 24 / npm 11). The Canva CLI is one `npm i -g @canva/cli` away.
- **Fonts.** Canva ships Libre Baskerville. Upstream it has been a variable 400–700 family since 2025, so a SemiBold may exist; whether Canva exposes that weight is unverified and the font probe records it. Real Baskerville needs Canva Pro and a Brand Kit upload of one `.ttf` per face; the Mac `Baskerville.ttc` holds six faces (Regular, Bold, Italic, Bold Italic, SemiBold, SemiBold Italic), all with embedding flag 0 (installable), and splits cleanly with fontTools. **Apps are documented as unable to use Pro or custom fonts, so expect the app to build in Libre Baskerville regardless; an uploaded Baskerville matters only for a swap in the editor afterwards, on Pro.** Whether Apple's licence permits uploading a bundled font to a cloud service is unverified; that is Luke's call.
- **Page size.** 18 × 24 in is Canva's Medium poster preset. The pixel size Canva assigns to it is unpublished (probably 1728 × 2304 at 96 px/in). A 300 dpi page (5400 × 7200) cannot exist in Canva at all: the area cap is 25 M px². So the design lives at screen pixels and PDF Print's 300 dpi governs the export. The app reads the page size at runtime and scales every coordinate from the kit's 1296 × 1728 pt.
- **Design Editing across all pages** is marked preview on its guide page but GA in the `@canva/design` changelog (2.10.0, 2026-06-12); the app falls back to one page at a time if the all-pages mode is refused.
- **Export.** PDF Print is 300 dpi; **Flatten must stay OFF** or links, tags and live text die. Cropped images embed their full originals, so pre-cropped derivatives keep the file small. `mailto:` links are undocumented; one test export decides page 3's email link.
- **Sharing on Pro:** an "Anyone with the link, can edit" link lets the director and producer edit without accounts (they need free accounts to comment or download). Teams and Brand Templates need the Business plan.
- **Canva's Terms of Use (19 Aug 2026)** forbid scraping and bypassing access controls; nothing found on automated UI input. Route B, if used, runs at human pace and only through documented UI.

## Steps

| # | Who | Step | Check |
|---|---|---|---|
| 0 | Luke | Confirm the plan tier in Settings › Billing. Decide the font: split and upload the Mac Baskerville (Regular, SemiBold, Bold) to Brand › Fonts, or accept Libre Baskerville. Accept the Developer Terms once at canva.dev. Stay logged in to Canva in Chrome. | Billing page shows the tier; Brand › Fonts lists the uploads, or the decision is "Libre" |
| 1 | Agent | **Import test (20 min):** drop the current PDF on the Canva home page; open the result. | Page count 11; page size in Resize › Custom; which pages have editable text; which font Canva substituted; how many links survived (expect 0) |
| 2 | Agent | Emit the Canva operation list: a `--canva-json` mode on the recording canvas that writes every page's runs (text, font key, size, tracking, leading, colour, x, y, width, alignment, link), rules, and images as public URLs of pre-cropped derivatives committed under `press/assets/derived/canva/`. | The JSON has 11 pages, 19 links, and the same run count as the PDF (the recorder prints both) |
| 3 | Agent | `npm i -g @canva/cli`, `canva apps create kom-epk-builder`, `canva apps start` on port 8080. In the Developer Portal set the Development URL to `http://localhost:8080` and click Preview. | The app panel opens inside the Canva editor |
| 4 | Agent + Luke | **Font test (10 min):** in the app, open the font picker. | The uploaded Baskerville appears with its weights, or it does not; the refs are recorded either way |
| 5 | Agent | **Page-size test:** open a new design from the 18 × 24 in poster preset with the app; read the design's pixel dimensions. | The px-per-pt factor is recorded; a 1296 pt page maps to that width |
| 6 | Agent | **Pilot, page 3 only:** `addPage` (background `#0b0806`, the measured dimensions), images by URL, richtext runs with font, size, tracking, leading, alignment, colour and the nine links, rules as thin shapes; sequential with backoff. Export PDF Standard, Flatten OFF. | Element count equals the JSON's for page 3; pypdf finds 9 links whose URLs match; text selectable; the mailto link opens; render diffed against the master with position deltas listed |
| 7 | Luke | **Go or no-go on the pilot:** typeface, line-break drift, the mailto behaviour. Any tweak goes into the emitter, never hand-edited in Canva. | Decision recorded |
| 8 | Agent | **Full build**, pages 1–11 in order. Post-pass with Design Editing (all pages, else page by page): set transparency on the six ghost stills if they were not baked, read back every element's position. | Eleven pages in order; read-back positions within 1 px of the scaled JSON; transparency confirmed on six elements |
| 9 | Agent | Export: Share › Download › PDF Print, RGB, Flatten OFF, crop marks OFF, all pages. | pypdf: 11 pages at 1296 × 1728 pt, 19 link annotations, text extracts, fonts embedded; page renders diffed against the master; file size recorded against 9.8 MB |
| 10 | Luke (Pro only) | If real Baskerville was chosen: the agent splits the `.ttc` into per-face `.ttf`; Luke uploads Regular, SemiBold, Bold in Brand › Fonts and swaps the faces in the editor. | Font menu shows the uploaded family with three styles; the export's embedded fonts read Baskerville |
| 11 | Luke | Share: "Anyone with the link, can edit" to the director and producer (ask them to sign in so they can comment and download); a view link for press. | Both open the design; one of them changes a word and it shows |
| 12 | Agent | Repeatability: on a worksheet change, re-run steps 2 and 8 for the changed pages. A rebuilt page is a new page; the superseded one is deleted, and any collaborator edits on it are lost unless folded back into the worksheet first. | Same checks as 8 and 9 |

## What Luke decides before step 1

1. **Plan tier.** Pro is enough for fonts, Brand Kit, PDF Print and edit links. Business adds a team and Brand Templates; not needed for this.
2. **The font.** Real Baskerville by upload (his licence call) or Libre Baskerville (no SemiBold; the credit-card headings and the bio lockups re-fit).
3. **Which copy is the master.** The worksheet stays the source of truth and the Canva design is a mirror rebuilt from it. Edits collaborators make in Canva do not flow back to `press/epk.json`. If they should, the working rule is: collaborators edit words in Canva, someone copies the words into the worksheet with `epk.py set`, and the kit regenerates. Say which way round.
4. **Page 3's email link** if `mailto:` fails the export test: a Drive-folder link on the row, or the address as plain text.
5. **Line-break tolerance.** Accept Canva's reflow (editable paragraphs; line breaks drift on pages 2, 3, 4, 5, 6, 9, 10, 11) or emit one element per line (exact breaks, poor editability, three times the elements).
6. **Per-action OK** for the agent to drive his logged-in Canva editor for the manual steps (the import probe, image-borne links if any, the font swap), at human pace, through the documented UI only.

## Risks, plainly

- Uploaded fonts may be invisible to apps. Then Libre Baskerville: letterforms visibly different, SemiBold gone, line breaks drift; half a day to re-fit.
- Canva reflows paragraphs with its own composer, so line breaks on pages 2, 4, 5 and 6 will not match the PDF exactly. Tracked caps can be emitted one line per element to hold their breaks.
- The Preview button may open a fresh design rather than an existing one; if so the poster preset is created first and the app opened from it, or the page is resized (Pro).
- The 18 × 24 in pixel mapping is unpublished; read it, never assume it.
- A reported ceiling of about 1,000 elements per design comes from secondary sources; this kit is about 415 operations.
- A rebuild adds pages rather than updating in place. Refreshing text in place through the Design Editing API is plausible and unverified.
- Canva's own help pages disagree with each other on PDF import (editable elements versus flattened A4 images: the second reads as the scanned-PDF case), on the page-size cap (8000 px per side versus 8000 × 3125), and on Pro storage. Where they disagree, the probe decides.
- Research claims that did not survive verification and were dropped: that Canva carries no Monotype Baskerville (no public font list exists to check); that Libre Baskerville has no SemiBold (stale upstream); that the Connect API has no editing at all (Enterprise autofill exists). A font "Change all" swap appears in a May 2026 Canva newsroom post but not in the Help Center.
- No live test has run against the account. Every "expect" above is documented or inferred, not observed.

## Sources (read 2026-09-10)

canva.dev/docs/connect (endpoint index, changelog, integrations, scopes, create-design, imports, exports, autofills) · canva.dev/docs/apps (prerequisites, previewing-apps, releasing-apps, design-add-page, design-add-element-at-point, design-create-richtext-range, asset-upload, asset-find-fonts, asset-request-font-selection, design-editing, fonts) · canva.dev/docs/mcp · canva.com/help (import-and-edit-pdfs-canva, upload-formats-requirements, upload-fonts, brand-kit, brand-fonts, color-palettes, download-file-types, download-flattened-pdf, hyperlinks, moving-elements, resize-and-crop, format-text, canva-keyboard-shortcuts, screen-reader-editor, design-from-scratch, resize, collaborate-with-anyone, share-via-link-or-email, publish-team-template, about-canva-business) · canva.com/sizes/poster · canva.com/policies/terms-of-use (effective 19 Aug 2026) · canva.com/pricing.
