# BUILD-REPORT — kom-epk-builder

Built 2026-09-10 from the official starter (`canva-sdks/canva-apps-sdk-starter-kit`, cloned at depth 1;
scaffold files copied, examples/templates/tests dropped). Installed SDK versions:
`@canva/design` 2.13.x, `@canva/asset` 2.3.x, `@canva/platform` 2.2.x, `@canva/error` 2.2.x,
`@canva/app-ui-kit` 5.14.3, `@canva/app-scripts` 1.1.1, `@canva/cli` 2.12.0 (pinned devDependency since the review fixes), TypeScript 5.9.2,
React 19.2. Node v24.13.1, npm 11.8.0.

App directory: `/Users/scrogdawg/BMF Headquarters/Previous Years/2025 - SEW TO GROW/25_01 KILLER OF MEN (THESIS)/FESTIVAL CAMPAIGN/site/canva/kom-epk-builder`

## SDK calls used and the docs read for each

| Call | Package | Doc URL read (2026-09-10) | Where used |
|---|---|---|---|
| `addPage({ title, dimensions, background, elements })` | `@canva/design` | https://www.canva.dev/docs/apps/api/design-add-page/ | `src/ops/build.ts` buildPage |
| `addElementAtPoint(element)` | `@canva/design` | https://www.canva.dev/docs/apps/api/design-add-element-at-point/ | `src/ops/build.ts` fallback path |
| `createRichtextRange()` → `appendText`, `formatParagraph`, `formatText` | `@canva/design` | https://www.canva.dev/docs/apps/api/design-create-richtext-range/ | `src/ops/build.ts` richtextElement |
| Shape rectangle (`type:'shape'`, `paths[{d, fill:{color}}]`, `viewBox`) | `@canva/design` | https://www.canva.dev/docs/apps/creating-shapes/ | `src/ops/build.ts` ruleElement |
| `upload({ type:'image', mimeType, url, thumbnailUrl, aiDisclosure:'none', width, height })` | `@canva/asset` | https://www.canva.dev/docs/apps/api/asset-upload/ | `src/ops/build.ts` uploadImage |
| `findFonts()` | `@canva/asset` | https://www.canva.dev/docs/apps/api/asset-find-fonts/ | `app.tsx` onFindLibre |
| `requestFontSelection({ selectedFontRef? })` | `@canva/asset` | https://www.canva.dev/docs/apps/api/asset-request-font-selection/ | `app.tsx` onPickFont |
| `getDesignMetadata()` | `@canva/design` | https://www.canva.dev/docs/apps/api/design-get-design-metadata/ | `app.tsx` onProbePage |
| `getCurrentPageContext()` | `@canva/design` | https://www.canva.dev/docs/apps/api/design-get-current-page-context/ | `app.tsx` onProbePage |
| `openDesign({type:'all_pages'|'current_page'}, cb)`, `session.pageRefs`, `helpers.openPage`, `page.elements.toArray()` | `@canva/design` | https://www.canva.dev/docs/apps/api/design-open-design/ and https://www.canva.dev/docs/apps/design-editing/ | `src/ops/readback.ts` |
| `CanvaError` / `ErrorCode` (`rate_limited`) | `@canva/error` | public errors page not found at any guessed URL (see below); used `node_modules/@canva/error/index.d.ts` | `src/ops/retry.ts` |
| `useFeatureSupport()` → `isSupported(addPage)`, `isSupported(addElementAtPoint)` | `@canva/app-hooks` | starter kit `src/intents/design_editor/app.tsx` pattern; typings in `node_modules/@canva/app-hooks/lib/index.d.ts` | `app.tsx` |

Names in the brief that do not exist as given:

- `platform-get-design-metadata`: `getDesignMetadata` is exported by `@canva/design`, not `@canva/platform`;
  the doc lives at `.../api/design-get-design-metadata/` (the `platform-...` URL is a 404). Return shape is
  `{ title?, defaultPageDimensions?: {width,height}, pageMetadata, durationInSeconds }`.
- `design-editing (openDesign)`: the API page is `.../api/design-open-design/`; the guide is `.../design-editing/`.
  `all_pages` is documented as preview on the guide page but GA in the `@canva/design` 2.10.0 changelog (2026-06-12); the app tries it and falls back to `current_page`.
- Errors doc: `.../api/error-canva-error/`, `.../errors/`, `.../rate-limits/` all returned 404. The `ErrorCode`
  union in the installed `@canva/error` typings is: bad_external_service_response, bad_request,
  failed_precondition, internal_error, not_found, not_allowed, permission_denied, missing_permission,
  quota_exceeded, rate_limited, timeout, unsupported_surface, unsupported_page_type, user_offline.
- The addPage doc does not state a max element count per page or any rate limit; the batch → per-element
  fallback is triggered by any rejection of the batch call, not by a documented threshold.

All element/option shapes were cross-checked against the installed `.d.ts` files, which are what `tsc` enforces:
`ImageElementAtPoint = ImageElement & Point & (WidthAndHeight|Width|Height)`, `RichtextElementAtPoint = {type,range} & {top,left,rotation?,width?}` (no height),
`ShapeElementAtPoint` needs `viewBox` + `paths` + box, `ImageUploadOptions` requires width and height together,
`FontSelectionResponse` is `{type:'completed', font} | {type:'aborted'}`.

## Mapping decisions

- `s = pagePx.width / page.width_pt`; every x, y, w, h, size_pt is multiplied by `s`; the new page is
  `width_pt*s × height_pt*s`. If both probes return undefined the panel says so and Build is disabled.
- Paragraph text is appended verbatim (`\n` = paragraph end per the richtext doc; `\n\n` becomes an empty paragraph,
  preserving the blank-line spacing of the source).
- `fontSize = clamp(size_pt*s, 1, 1000)`, `lineHeightEm = clamp(leading/size, 0.5, 2.5)`,
  `letterSpacingEm = clamp(tracking/size, -0.2, 0.8)`; a clamp on tracking is logged.
- Font: chosen ref for the key; if the chosen font lacks the weight, the table's `fallback_weight` is used; if no
  ref was chosen, the Libre Baskerville ref (from `findFonts`) with `fallback_weight`; if neither, no `fontRef`
  (Canva default) and a log line.
- Links: `formatText({index:start, length:end-start}, {link})` per entry, clamped to the text length.
- Rules: rectangle path `M 0 0 H w V h H 0 L 0 0` with `viewBox {0,0,w,h}`, fill colour, no stroke. Height is the
  exact `h*s`; only if Canva rejects the page is the batch retried with sub-pixel rules floored to 1 px (logged).
- Images: `mimeType` by extension (`.png`, `.webp`, `.svg`, else `image/jpeg`), `thumbnailUrl = url`,
  `aiDisclosure:'none'`, alt text from `alt` (decorative when absent). Uploads run sequentially before `addPage`.
- Retry: `rate_limited` → 500 ms, 1 s, 2 s, 4 s, max 5 tries; anything else propagates to the page log.
- Progress: `localStorage["kom-epk-builder:progress:v2"]` = `{key: "<generated>|<epk_rev>", done{}, failed{}}`, each page
  `{n, name, elements_attempted, elements_placed, failures, at, mode, page_id, page_is_current}`;
  fonts in `kom-epk-builder:fonts`; ops URL in `kom-epk-builder:ops_url`.

## Typecheck / lint / build output

`npx tsc --noEmit -p tsconfig.json` → no output, exit 0 (zero errors).

`npx eslint .` → no output, exit 0 (after pinning `settings.jest.version` because the Canva plugin loads jest rules and this app has no jest).

`npm run build`:
```
Canva │ @canva/app-scripts 1.1.1 · build
info    build started...
ready   built in 0.48s
Warn: BACKEND_HOST is set to localhost; a production build needs your deployed backend URL. (no backend is used)
       App bundle (app.js)   Build: completed in 1959ms   File size: 1.26 MB (max 5MB)   Output: .../dist/app.js
       Translations (messages_en.json)   Messages: 0 extracted   File size: 2 B
```
exit 0.

Smoke test `npm start`:
```
Canva │ @canva/app-scripts 1.1.1 · dev
  →  Frontend:  http://localhost:8080
  →  Preview your Design Editor app in Canva:  unavailable: CANVA_APP_ID not found in .env file.
ready   built in 0.28s
```
`curl http://localhost:8080/app.js` → HTTP 200, 6,413,862 bytes (dev bundle). Server then stopped; `lsof` shows nothing listening on 8080.

## Not verified (needs a Canva session)

1. Nothing was run inside Canva: no Developer Portal app exists yet, so `addPage`, richtext, upload, font picker and
   `openDesign` were exercised only by the type checker.
2. `canva/ops/epk-canva.json` does not exist yet (GitHub Pages URL returns 404 as of build time); the parser was
   written to the contract in the brief and rejects `count` mismatches, but has not seen a real file.
3. Whether `addPage()` leaves the new page current is now checked at runtime (`getCurrentPageMetadata().id` vs
   the returned `PageMetadata.id`) and the per-element fallback refuses to place when it is not; whether the
   check ever reports "is NOT" in practice is still unobserved.
4. Whether Canva accepts a 0.667 px-high shape (0.5 pt at s = 1.333) or forces the floored retry, and whether
   `line` kind text with `w` slack never wraps at the scaled `fontSize` (Read back now flags WRAPPED lines
   against `leading_pt*s*1.3`), are checks for the page-3 pilot.
5. `openDesign all_pages` is documented as preview; if it throws in production the app falls back to `current_page`
   (one page per read).
6. `getDesignMetadata().defaultPageDimensions` may be undefined for docs/whiteboards; the second probe covers it,
   and the panel reports undefined plainly.
7. `.env` (gitignored) was created by the starter's postinstall from `.env.template`; it holds no secrets. HMR
   needs `CANVA_APP_ID`/`CANVA_APP_ORIGIN` from the Portal.


## Review fixes (2026-09-10, second pass)

Seventeen review findings were applied or rejected as below. Each accepted fix cites the doc it was checked against
in a code comment. Nothing outside `canva/kom-epk-builder/` was touched.

| # | Finding (file:line) | Decision | What changed / why not |
|---|---|---|---|
| 1, 6 | `build.ts` fallback assumes new page is current | **Applied** | `addPage()` is documented only as "Adds a new page immediately after the currently selected page" and returns `PageMetadata` whose `id` is a "Stable identifier for this page within the design" (https://www.canva.dev/docs/apps/api/design-add-page/). `getCurrentPageMetadata()` returns the same shape (https://www.canva.dev/docs/apps/api/design-get-current-page-metadata/). `buildPage` now keeps the returned metadata, calls `getCurrentPageMetadata()` after every `addPage`, logs `page id X is / is NOT the current page`, and in the per-element fallback returns `placed 0` with a failure when the ids differ. When either id is unavailable (`type: "unsupported"` or `id` absent — `id?` is optional in the 2.13.0 typings) it logs "cannot verify" and, in the fallback only, proceeds with a warning. |
| 7 | Page order unverified; `addPage` id discarded | **Applied in part** | `page_id` and `page_is_current` are now in `BuildResult`, `PageProgress`, the panel and the STATE export. The "position N of N via `getDesignMetadata().pageMetadata`" part is **rejected**: that field is documented "The order of pages is not guaranteed" (https://www.canva.dev/docs/apps/api/design-get-design-metadata/ and the installed d.ts), so an index into it would be noise. README-APP.md step 4 now says build page 1 first, confirm its position and the "is the current page" log line before Build all, delete the default blank page, and check Read back counts. |
| 2 | `mailto:` links passed to `formatText({link})` | **Applied** | The `link` field is documented only as "An external URL that the text links to" (https://www.canva.dev/docs/apps/api/design-create-richtext-range/). `richtextElement` now applies links only when `/^https?:\/\//i` matches; the two `mailto:` links (sdretzka@afi.com, killerofmenmovie@gmail.com) keep their text and log `link ... skipped: non-http(s) scheme not documented for richtext links`. Consistent with STATE.json's standing decision to show the address as plain text if Canva drops mailto. Emitter not changed (outside scope). |
| 3 | `BACKEND_HOST` warning | **No code change** (as recommended) | Documented in README-APP.md "Run": the app calls no backend; the warning matters only if the bundle is submitted. |
| 4 | App directory untracked in git | **Not done here — operator action** | Committing/pushing writes outside `kom-epk-builder/` (the repo's `.git`) and is an outward action needing Luke's per-action OK. README-APP.md gained a "Git" section with the exact explicit-path list. Command for the operator, from the repo root: `git add canva/kom-epk-builder/{package.json,package-lock.json,tsconfig.json,eslint.config.mjs,.nvmrc,.npmrc,.prettierrc,.gitattributes,.gitignore,.env.template,README-APP.md,BUILD-REPORT.md,LICENSE.md,declarations,styles,scripts,src} && git commit -m "canva: add kom-epk-builder app" && git push`, then `git ls-files canva/kom-epk-builder | wc -l` on a fresh clone (expect 21). |
| 5 | Scopes never mentioned | **Applied** | https://www.canva.dev/docs/apps/configuring-scopes/ lists `addPage`/`addElementAtPoint` under `canva:design:content:write`, `upload` under `canva:asset:private:write`, `getCurrentPageContext` under `canva:design:content:read`; `getDesignMetadata`, `getCurrentPageMetadata`, `openDesign`, `findFonts`, `requestFontSelection` appear under no scope. README-APP.md has a new Portal step 3 (Scopes). `retry.ts errorMessage()` appends a hint naming the three scopes whenever the code is `missing_permission`. |
| 8 | Progress records failures as done; not tied to ops file; no per-page reset | **Applied** | `storage.ts`: record = `{key: generated|epk_rev, done, failed}`; `recordPage` files a page under `done` only when `placed === attempted && failures.length === 0`; Build all skips `done` only and announces the `failed` retries; loading an ops file with a different key logs `progress record is for ops "...", loaded "..." — not used`; per-page **Forget page N** button; Reset also removes the pre-review key. Design-id namespacing **rejected**: `DesignMetadata` in the installed typings has no id (`title, defaultPageDimensions, pageMetadata, durationInSeconds`), so README tells the operator to Reset when switching designs. |
| 9 | STATE export shape mismatch | **Applied** | `onExportState` now emits `probes.page_size{done,width_px,height_px,source}`, `probes.fonts{done,Bask,Bask-SB,Bask-B,"Libre Baskerville"}` (each `{ref,name,weights}`), `design{page_px:[w,h],scale_px_per_pt}`, `ops{epk_rev_built_from,generated,kit_commit}`, `pages_built[{n,name,status,elements_attempted,elements_placed,mode,failures,page_id,page_is_current,at}]`, `last_error`. README step 5 lists the keys to merge. |
| 10 | `upload()` given placement box as image size | **Applied** | The upload doc defines `width`/`height` only as "A width, in pixels" / "A height, in pixels" (https://www.canva.dev/docs/apps/api/asset-upload/), i.e. the asset's own size. `OpsImage` gained `px?: [number, number]` and `file?: string` (both written by the emitter for all 22 images); `uploadImage` sends `px` and falls back to the scaled box only when `px` is absent. |
| 11 | Rule height floored at 1 px | **Applied (variant)** | The shape doc (https://www.canva.dev/docs/apps/creating-shapes/) states no minimum height. `ruleElement(ctx, el, floor)` builds the exact height by default; `buildPage` tries the batch with exact rules, and only if that is rejected and the page has sub-pixel rules retries the batch with rules floored (logging `rule #i height floored 0.667 -> 1 px`) before the per-element fallback (which uses the floored variant). Chosen over the reviewer's per-element catch so the batch path stays atomic. Runtime acceptance still to be observed on the page-3 pilot. |
| 12 | Explicit `fontRef: undefined` / `fontWeight: undefined` keys | **Applied** | Both are optional in the typings (`fontWeight` "@defaultValue normal", https://www.canva.dev/docs/apps/api/design-create-richtext-range/); keys are now spread in only when a value exists. |
| 13 | Read back does not detect wrapped `line`s | **Applied** | `readback.ts`: `matchOpsPage` pairs a read page with the ops page of identical element count (else the panel's *Page n*), `flagWrapped` flags `line` elements whose read height > `leading_pt*s*1.3`; the panel shows a WRAPPED alert with page, index, text, read px vs expected px. |
| 14 | README step 4: how to open the app in the poster; default page; rebuild appends | **Applied in part** | README now states the untested path (open the poster, Apps -> Your apps) with the fallback (build in the fresh Preview design, pages get ops dimensions anyway, delete its default page), and that Build page N appends — delete the old page first. Cannot be tested without a Canva session; marked as such. |
| 15 | `@canva/cli` not pinned | **Applied** | `devDependencies["@canva/cli"] = "2.12.0"` (bin name `canva`, confirmed via `npm view @canva/cli@2.12.0 bin`); scripts are `canva apps start` / `canva apps start --preview` / `canva apps build`. `npm install` added 92 packages; `npx canva --version` prints 2.12.0. |
| 16 | `parseOps` skips `height_pt`; contract text omits `file`/`px` | **Applied** | `height_pt` is now required (`ops JSON missing page.height_pt`); the contract comment in `types.ts` lists the emitter extras `file` and `px`. |
| 17 | Out-of-brief scan clean; note `all_pages` is preview | **Applied (doc only)** | README step 6 says to expect one page per read on the stable SDK. |

Doc facts that could not be confirmed and are therefore labelled inferences in code comments: whether `addPage` makes
the new page current (now measured at runtime instead), whether richtext `link` accepts `mailto:` (avoided), whether a
sub-pixel shape height is accepted (exact first, floored retry), what runtime error a missing scope raises (the scopes
page says only "If the scope isn't enabled, the app can't be approved for release"; the `missing_permission` hint is
keyed on the `ErrorCode` name in `@canva/error`).

### Typecheck / lint / build after the fixes

`npx tsc` -> no output, exit 0. `npx eslint .` -> no output, exit 0 (four `@typescript-eslint/no-dynamic-delete`
errors during the pass were fixed by rest-destructuring instead of `delete`). `npx prettier --write` applied to `src/`.

`npm run build` (now `canva apps build`, @canva/cli 2.12.0 pinned):
```
Canva │ @canva/app-scripts 1.1.1 · build
info    build started...
ready   built in 0.42s
Warn: BACKEND_HOST is set to localhost; a production build needs your deployed backend URL. Set "backend.host" or CANVA_BACKEND_HOST before publishing.
  →  Config:    None (Using defaults)
  →  Outputs:
       App bundle (app.js)
         →  Build:      completed in 493ms
         →  File size:  1.26 MB (max 5MB)
         →  Output:     .../canva/kom-epk-builder/dist/app.js
       Translations (messages_en.json)
         →  Messages:   0 extracted
         →  File size:  2 B (max 1MB)
```
exit 0. The BACKEND_HOST line is the only diagnostic (see finding 3).

Files changed in this pass: `src/ops/build.ts`, `src/ops/readback.ts`, `src/ops/storage.ts`, `src/ops/retry.ts`,
`src/ops/types.ts`, `src/intents/design_editor/app.tsx`, `package.json`, `package-lock.json`, `README-APP.md`,
`BUILD-REPORT.md`.

## Codex audit, 2026-09-11 (cross-family, read-only; verdict UNSOUND)

Eight findings against the runbook, STATE, the plan and this source; no invented or type-invalid SDK call was found
(`addPage`, `addElementAtPoint`, richtext formatting, `upload`, font selection, metadata calls and `openDesign` all
exist in the current GA references). What changed in response, the same day:

| # | Finding | Response |
|---|---|---|
| 1 | Link acceptance tests asked for 20 links (10 on page 3); the app drops the two `mailto:` rows as text, so 18 / 8 is the most it can produce | README expectations corrected to 18 live links, 8 on page 3, the two email rows as plain text (the recorded decision in STATE) |
| 2 | Fonts loaded from localStorage; a resumed session could build in Canva's default font and be recorded complete | `resolveFont` throws when no ref was resolved; the panel passes only refs picked in the current session (`fresh`), shows stored refs as stale, and keeps Build disabled until every key is fresh |
| 3 | The "build with explicit dimensions" fallback did not exist in the app | Manual page-width control in section 2 (`Use this width`), unverified against Canva; README says so |
| 4 | Scopes absent from the runbook's step 3; the hint keyed on `missing_permission` only, while the errors guide documents `permission_denied` | Scopes named in step 3; hint fires on both codes |
| 5 | `press/canva-plan.md` stale (Free, `canva apps create`, transparency post-pass, worksheet as master) | Superseded banner with the four corrections |
| 6 | Pilot check read `d[0]`, the default blank page | Delete the blank page first; the check reads `d[-1]` |
| 7 | Export STATE was said to supply `design.url` | `url: null` in the export with a note; README says copy it from the address bar |
| 8 | `whenUploaded()` never awaited | Awaited per image; a failed upload fails the element and the page is recorded failed |

Typecheck, lint and build after these fixes (2026-09-11): `npx prettier --write src`, `npx tsc --noEmit` exit 0, `npx eslint .` exit 0, `npm run build` completed (`dist/app.js` 1.26 MB).

## First runs inside Canva, 2026-09-11

What only the live editor could show, in the order it showed it:

| Finding | Response |
|---|---|
| The Preview button opens a fresh 800 x 600 px design; the app is opened inside another design by appending the Preview tab's `ui=` query parameter to that design's edit URL | Runbook step 4 and STATE record the trick; an 18 x 24 in design measures 1728 x 2304 px (96 px/in exactly) |
| Libre Baskerville runs wider than the Baskerville the line boxes were measured with: 63 of page 3's 70 lines wrapped | Emitter: every line's box is `width * 1.35 + 24`, anchored on its own alignment edge (right-aligned lines keep their spine and grow leftward); the recorder passes `align` and the anchor x |
| With two separate runs, a key anchored at its value's Baskerville edge overlapped the wider value | Emitter merges abutting same-baseline runs into one line with colour `runs`; the app applies each run's colour after the whole-range colour |
| Each `addPage` lands after the previously added page, although `getCurrentPageMetadata()` never reports the new page as current | Build all runs 1 to 11 into a design holding one blank page; a reverse run came out backwards and was deleted in the grid view |
| `addPage` rejects more than 100 elements (`bad_request: Please specify up to a maximum of 100 elements`), undocumented; page 10 has 126 | `placeOnCurrentPage()`: the operator selects the background-only page the fallback created and the elements go on with `addElementAtPoint`; `ADD_PAGE_MAX_ELEMENTS` logs the warning up front |
| `addElementAtPoint` has its own rate limit (`rate_limited: Add native element rate limit exceeded`); 126 calls in a row lost 3 elements at four retries topping out at 4 s | Backoff to 16 s over 7 tries and a 150 ms pace between placements (`PACE_MS`) |
| Canva names the exported file after the page title (`03 Programmer.pdf`) | Runbook's pilot check looks for it by name |
| The pilot export: 1296 x 1728 pt, live text, Libre Baskerville Regular and Bold embedded, 10 link annotations over 4 URLs, the two mailto rows as text | As designed |
