# HARNESS: picking up the EPK lane cold

Read this first after a compaction or in a fresh session. It is the standing pickup for the `epk` lane; the numbered handoffs carry the day-by-day record (latest: highest `handoff-NNN-epk.md`). Updated 2026-09-21 (Erik Orjiako's bio). Before that: 2026-09-20 (cast bios; the connector route). Before that: 2026-09-16 (after the 2.2 mirror).

## Standing rules (Luke's, verbatim where quoted)

- "Never git add -A, git stash, or git reset: another session shares this tree." Commit by explicit path only.
- "Never commit: tokens, secrets, credential maps, cap-table/deal terms." "Never without Luke's per-action OK: deploy, OTA, EAS, migrate, anything outward."
- Masters in `press/assets` are never modified. Every fact in `press/epk.json` is written with `venv/bin/python tools/epk.py set N.N "…"` (or `set N.N -` from stdin), never by hand; `tools/epk.py check` after.
- **Luke's Canva edits win.** When he changes the design, the worksheet is updated to match, never reverted. Pointing out a change is fine. Do not rebuild Canva pages from the contract without his word; the design is ahead of the kit.
- Clean Bank for anything he reads as a product (readouts, reports, kit text): no flourish, no codas.
- Every turn ends with a handoff `handoffs/handoff-NNN-epk.md` (test that NNN does not exist first), committed by path, pushed, copied to `$HOME/Google Drive/My Drive/KILLER OF MEN/HANDOFFS/`. Say whether the turn was duck (plan) or goose (execute).
- The Canva Download click is Luke's, not mine (browser download rule).

## Where things are

- Repo: this directory, branch `main`, remote `Scroggdawg/kom-festival-board`. Two machines commit here (this Mac as `Scroggdawg`, the other as `C`); pull before assuming.
- Worksheet: `press/epk.json`. Field 2.1 logline (Jordan's FilmFreeway text, rev 25); 2.2 synopsis; 7.1 cast bios (rev 35: Erik Orjiako's as Luke supplied it on 21 Sep with three slips corrected; Eric Pargac's and Jamal Dennis's exactly as he supplied them on 20 Sep, three paragraphs each, one paragraph per line in the field; Sandra McDaniels's still the 10 Sep draft); 11.1 thanks (rev 32, 58 lines mirrored from the design).
- Kit: `tools/build-epk-kit.py` (pages 1 to 8) and `tools/build-credit-card.py` (9 to 11); contract emitter `tools/build-epk-canva.py` → `canva/ops/epk-canva.json`; checkers `tools/check-canva-contract.py`, `tools/check-canva-export.py`, `tools/canva-readback-diff.py`.
- Canva design: "EPK _ KoM 2026", id `DAHU6a7HKPs`, 18×24 in, 11 pages. Page ids in `canva/STATE.json`. Edit URL with the app open: `https://www.canva.com/design/DAHU6a7HKPs/edit?ui=eyJFIjp7IkE_IjoiTiIsIlMiOiJBQUhPR0JDTUM0QSIsIlQiOjF9fQ`. The app is `canva/kom-epk-builder` (React, @canva/design), served by the dev server `preview_start` name `canva-app` (it stops between sessions).
- Drive mirror: `$HOME/Google Drive/My Drive/KILLER OF MEN/05 MARKETING/00 PRESS/` (kit PDFs under `EPK BUILDS`, Canva exports under `EPK BUILDS/CANVA`).
- Provenance reports (done): `press/cast-bios-evidence.md`, `press/cast-bios-bibliography.md`, `press/cast-bios-proposed-2026-09-15.md` (conservative bios, not applied), `press/synopsis-evidence.md`.

## Procedure: mirror a Canva edit into the worksheet

1. Start the read-back receiver in the background: `venv/bin/python tools/canva-readback-server.py` (listens on localhost:8787, writes `canva/readback/<UTC>.json` and `latest.json`). `pkill -f canva-readback-server` when done.
2. `preview_start` with name `canva-app` so the app's bundle is served.
3. In Luke's Chrome (the `mcp__claude-in-chrome__*` tools; load them with one ToolSearch `select:` call): find the design tab. The app panel (KOM EPK Builder) must be open in the editor's side panel. If it says it couldn't load the app's JavaScript bundle, navigate the tab to the edit URL above again. **The app iframe only takes input when its tab is the front tab**; a stray keystroke into a frozen panel reaches the editor (a Backspace once deleted a page; Undo restored it).
4. Click the app's read-back control. `app.tsx` POSTs every page's elements with text to the receiver.
5. `venv/bin/python tools/canva-readback-diff.py` prints, per page, the design text against the contract. Take the changed field's text exactly as the design has it (typos included; flag them to Luke, do not fix them).
6. Write it: `venv/bin/python tools/epk.py set 2.2 -` with the text on stdin (keep paragraph breaks as blank lines). `tools/epk.py check`. Commit `press/epk.json` by path with a message naming the field and the source ("mirrored from the design").
7. **Shortcut that worked on 16 Sep:** the editor renders the displayed page's text in the DOM, so `get_page_text` on the design tab (with the page selected in the editor) returns the exact text without the app. Steps 1 to 5 are only needed for a full-design read with positions. Fallback if Chrome cannot be driven at all: ask Luke to paste the text.

## Procedure: change words on a built Canva page without a rebuild (found 2026-09-20)

The claude.ai Canva connector reaches the design from a session with no browser, no app and no dev server (tools `read-design`, `edit-design`, `export-design`; load them with one ToolSearch `select:` call).

1. `read-design` with `design_id: DAHU6a7HKPs`, `filter.page_indices: [N]`, `open_transaction: true`, fields `design_content` and `thumbnails`. It returns every element with its `locator_id`, geometry in px (page 1728 × 2304, 1.3333 px per pt) and formatting, plus a `transaction_id`.
2. `edit-design` with `replace_text` on the existing text element. **The element keeps its face, size, leading and colour.** `add_text` does not: it arrives in Canva's default face (16 px, black) and `format_text` has no font-family setting, so new copy goes into an existing element, never a new one. A bio of several paragraphs is one box with a blank line between paragraphs (a blank line is a full 32 px line at the body's pitch).
3. Read the new box heights from the returned document (a body box of n lines is 32 × (n − 1) + 24.29 px tall), then `position_element` everything below. Page 7's rhythm: lockup to bio 58.37 px; bio box to next lockup one uniform gap, fitted so the last row keeps its place (54.67 px on 20 Sep, 62.67 px on 21 Sep; never more than the original 67 px); ALSO BILLED 14.84 px further; rows at +45.33, +82.67, +120 with the names column 1.77 px higher; the last row's baseline on the 74 pt foot margin means its label box top at 2185.6 px.
4. Look at the render the call returns, check the numbers in the returned document, then `edit-design` again with `finalize: "commit"` and no operations (permanent) or `"cancel"`.
5. Proof: `export-design` PNG of the page at 1296 × 1728. Record the edit in `canva/STATE.json` under the page's `edited_in_place`.

Page rebuilds from the contract still go through the app in a front tab (below). The design tab opened by a session starts hidden, and the app's panel takes no input there.

## Open items (as of 2026-09-20)

- Field 2.2: done 16 Sep, Luke's Canva synopsis mirrored (rev 33 in the worksheet). The seven-inference analysis in `press/synopsis-evidence.md` applies to the old draft C, not to his text.
- Cast bios: **Erik Orjiako's is in as Luke supplied it on 21 Sep** (worksheet rev 35, kit PDF `1250_21092026`, Canva page 7 edited in place; three slips corrected and listed in the field's note: "performaces", "Malcom X", a stray semicolon; East West Players' own page lists him among three actors alternating as Malcolm X in the 2026-27 Theatre for Youth Tour, so "currently touring" will date). **Eric Pargac's and Jamal Dennis's are in, as Luke supplied them on 20 Sep** (worksheet rev 34, kit PDF `0958_20092026`, contract on Pages, Canva page 7 edited in place and committed; the wording matches each actor's self-written IMDb mini biography where the 10 Sep captures quote it). Sandra McDaniels's is the last 10 Sep draft; the conservative proposal for hers awaits Luke's go, and she still has no bio of her own. Hers is now the only one that ends with the "In Killer of Men she plays" sentence; Luke's call whether it stays. The EPK INFO Doc still shows the 10 Sep drafts for all four (it is also behind on 2.2, 3.1, 5.7 and 11.1).
- Page 11: "Devaraonda" spelling is Luke's to fix in Canva.
- Export: Luke downloads (Share › Download › PDF Print · RGB · all pages · crop marks off · flatten off), then `venv/bin/python tools/check-canva-export.py "$HOME/Downloads/EPK _ KoM 2026.pdf"`, copy to the Drive `EPK BUILDS/CANVA`.
