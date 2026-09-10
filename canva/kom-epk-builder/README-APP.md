# kom-epk-builder (Canva app)

Builds the Killer of Men EPK pages inside a Canva design from the operations file
`canva/ops/epk-canva.json` (schema 1), emitted by `tools/build-epk-canva.py`.

Panel sections: 1 Load operations · 2 Probe page size · 3 Probe fonts · 4 Build page N / all ·
5 Export STATE · 6 Read back · Log.

## Requirements

- Node 24 (`.nvmrc` = `lts/krypton`), npm 11. Engines: `^22 || ^24`.
- A Canva account with the Developer Portal enabled.

## Run

```bash
cd canva/kom-epk-builder   # if this folder is missing, the app has not been committed yet — see "Git" below
npm install                # also copies .env.template -> .env (no secrets in it); installs @canva/cli 2.12.0 (pinned)
npm start                  # dev server on http://localhost:8080 (canva apps start)
```

Type-check and production bundle:

```bash
npm run lint:types     # tsc, zero errors expected
npm run lint           # eslint (Canva app plugin)
npm run build          # dist/app.js via @canva/app-scripts
```

`npm run build` prints `Warn: BACKEND_HOST is set to localhost ...`. The app calls no backend (its only
fetch is the ops JSON), so the warning is harmless for local/preview use; it only matters if the bundle is
ever submitted for review, when `CANVA_BACKEND_HOST` in `.env` would need a real HTTPS host.

## Developer Portal steps (one time)

1. Open <https://www.canva.com/developers/apps> and click **Create an app**. Name it
   `KOM EPK Builder`; choose the *Design editor* intent (public / team is fine, it is never submitted).
2. **App source** -> **Development URL** = `http://localhost:8080`.
3. **Scopes** -> enable `canva:design:content:write` (addPage, addElementAtPoint),
   `canva:asset:private:write` (upload) and `canva:design:content:read` (getCurrentPageContext), per
   <https://www.canva.dev/docs/apps/configuring-scopes/>. A `missing_permission` line in the Log means one of
   these is off; the panel appends that hint to the error.
4. Optional HMR: **Security** -> **Credentials** -> copy the `.env` block (`CANVA_APP_ID`,
   `CANVA_APP_ORIGIN`) into this folder's `.env`, set `CANVA_HMR_ENABLED=TRUE`, restart `npm start`.
   `.env` is gitignored.
5. With `npm start` running, click **Preview**. The Canva editor opens with the app in the side panel
   (click **Open** the first time). Preview opens a fresh design of the app's default type; to build into the
   18 x 24 in poster instead, open that design and find the app under **Apps** -> *Your apps* (untested as of
   2026-09-10; if the dev app is not listed there, build in the fresh design, which gets its pages at the
   ops dimensions anyway, and delete its default blank page afterwards). The page size the app reads is
   the open design's default page size, so probe it in the design you will build in.

Safari needs `npm start -- --use-https` and the Development URL set to `https://localhost:8080`.

## Operator sequence

1. **Load** — the URL field is prefilled with the GitHub Pages ops JSON; or paste the JSON. The panel
   shows schema, generated, epk_rev, page count, element count and refuses a `count` mismatch.
2. **Read page size** — tries `getDesignMetadata().defaultPageDimensions`, then
   `getCurrentPageContext().dimensions`. Shows px and `s = widthPx / page.width_pt`. If both are
   undefined the panel says so and building is disabled.
3. **Fonts** — one *Pick font* button per font key (opens Canva's font picker; the chosen ref, name and
   weights are kept in `localStorage`), plus *Find Libre Baskerville* (`findFonts()` filtered by name;
   first match becomes the fallback ref).
4. **Build page 1 first**, then check the editor: it must sit right after the page that was selected
   (normally position 2, after the default blank page) and the Log line `page 1: page id ... is the current
   page` must say *is*, not *is NOT*. Only then **Build all pages**. Each page is one `addPage()` with all
   elements (rules at exact height; if a sub-pixel rule makes Canva reject the page, the batch is retried
   with rules floored to 1 px and the floor is logged); if both are rejected the app adds a background-only
   page, confirms via `getCurrentPageMetadata()` that it is the current page, and only then runs
   `addElementAtPoint()` per element — otherwise it stops with `placed 0` and tells you to delete that page
   and retry. `rate_limited` errors retry with 500 ms, 1 s, 2 s, 4 s backoff (5 tries).
   `addPage` is documented as inserting after the currently selected page, so if the new page does not
   become current the pages come out in reverse order; the check above catches that on page 1.
   **Building a page appends a new page; it never replaces one.** To rebuild page N, delete the old page N
   in the editor first. Delete the design's default blank page when the build is done.
   Progress is stored in `localStorage` under the ops file's `generated|epk_rev`: a page counts as *done*
   only when every element was placed with no failure; anything else is recorded as *FAILED* and
   *Build all* retries it (delete its partial page first). Loading a different ops file reports the old
   record and ignores it; *Forget page N* drops one record; *Reset progress record* clears all. The
   record is not tied to the design (the SDK exposes no design id), so Reset when switching designs.
5. **Render STATE JSON** — the block mirrors `canva/STATE.json`: merge `probes.page_size`,
   `probes.fonts` (`done`, `Bask`, `Bask-SB`, `Bask-B`, `Libre Baskerville`), `design.page_px`,
   `design.scale_px_per_pt`, `ops.epk_rev_built_from`, `pages_built[]` (with `status`, `page_id`,
   `page_is_current`, `mode`, `failures`) and `last_error` over the matching keys.
6. **Read design** — `openDesign` (`all_pages`, falling back to `current_page`) lists element type and
   box per page for a diff against the ops file. On the stable SDK (`@canva/design` 2.13.0) `all_pages` is
   preview-only, so expect one page per read (the current page). With ops loaded and the page size
   probed, the panel also pairs each read page with an ops page (unique element-count match, else the
   *Page n* field) and flags any `line` element read back taller than `leading_pt * s * 1.3` as
   **WRAPPED**; widen that element's `w` in the emitter. After Build all, Read back on each page should
   list counts matching each ops page's `count`.

Every SDK call is wrapped in try/catch and its message appears in the Log. The only network request
the app itself makes is the ops JSON fetch; images are uploaded by Canva from their public URLs.

## Git

The app lives in the `kom-festival-board` repo at `canva/kom-epk-builder`. If `git ls-files
canva/kom-epk-builder` prints nothing, commit it by explicit path (`package.json`, `package-lock.json`,
`tsconfig.json`, `eslint.config.mjs`, `.nvmrc`, `.npmrc`, `.prettierrc`, `.gitattributes`, `.gitignore`,
`.env.template`, `README-APP.md`, `BUILD-REPORT.md`, `LICENSE.md`, `declarations/`, `styles/`, `scripts/`,
`src/`) and push; `.env`, `node_modules/` and `dist/` stay ignored.

## Layout

```
src/index.tsx                       intent registration (starter)
src/intents/design_editor/index.tsx React root with AppUiProvider (starter)
src/intents/design_editor/app.tsx   the panel
src/ops/types.ts                    data contract + parser
src/ops/build.ts                    element builders + page builder (addPage / fallback)
src/ops/readback.ts                 openDesign read-back
src/ops/retry.ts                    CanvaError handling + backoff
src/ops/storage.ts                  localStorage keys
```

`LICENSE.md` is Canva's starter-kit licence, retained because the scaffold files come from
`canva-sdks/canva-apps-sdk-starter-kit`.
