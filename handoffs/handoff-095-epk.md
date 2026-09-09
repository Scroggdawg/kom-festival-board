# handoff-095-epk

## Correcting handoff-094-epk: that is not how this session did it

094 says the route was an installed-app OAuth client called `bmf-agent`, found in `~/Downloads`, with a script and token in a scratch directory that has since been cleaned — and concludes *"the capability existed, was never written down, and died with the session."*

**None of that is true of this session.** The correction matters because a live capability is being written off as dead.

Checked on this machine this turn, not recalled:

| Claim in 094 | Actual |
|---|---|
| An OAuth client in `~/Downloads` | No `client_secret`, `credentials` or `oauth` file exists there |
| A script and token in scratch | The scratch directory holds images, text dumps and a venv. No Drive script, no token |
| `googleapiclient` | Not installed in this session's venv either |
| The capability died with the session | **It is live right now.** It created both Docs and it still works |

### What was actually used

A **Google Drive MCP connector**, authorised to **camerawrap@gmail.com** — every file it created is owned by that address. No OAuth dance, no credential on disk, no library.

**Why 094's registry search found nothing.** Its tools are **deferred**, so no schema loads until `ToolSearch` fetches one, and **the names are opaque UUIDs**:

```
mcp__25eba522-0b5f-4d60-9c42-1ad13a406e65__create_file
mcp__25eba522-0b5f-4d60-9c42-1ad13a406e65__search_files
mcp__25eba522-0b5f-4d60-9c42-1ad13a406e65__read_file_content
```

No "drive", no "google", no "docs" anywhere in those strings. **A name search cannot find them.** They are found by searching descriptions:

```
ToolSearch: "google drive upload create document folder"
```

`create_file` comes back first. Re-run this turn to be sure.

### The recipe

1. `search_files` for the parent: `title = '00 PRESS' and owner = 'me' and mimeType = 'application/vnd.google-apps.folder'`. It is `1utGEFQb5gDuUOC9JU7zvuslwRlwbRorx`. A folder just made through the Drive mount needs a moment to sync before the API sees it.
2. `create_file` with `title`, `parentId`, `contentMimeType: "text/plain"` and the whole body in `textContent`. Drive converts plain text into a real Google Doc by default; `disableConversionToGoogleType` is what would stop it.
3. The result returns `fileSize: "1"`. That looks like failure and is not — verify with `read_file_content` on the returned id.
4. Use `textContent`, never the deprecated `content`. Plain text is parsed as light Markdown on conversion, so underscores and brackets come back escaped. Cosmetic only.

### Where 094 is right, and should not be undone

**`tools/gdoc.py` does something this connector cannot: replace an existing Doc's body in place.** `create_file` only makes new documents; there is no update-body call in the connector. Since Luke wants *that* Doc updated rather than a second one appearing beside it, keeping its id, URL and sharing, **gdoc.py is the better instrument and the reasoning behind `files.update` over `batchUpdate` is sound.** Do not abandon it on the strength of this correction.

**Two things to weigh before Luke clicks consent.** The scope requested is full `drive`, not `drive.file` — 094 says why, and the reason is real, but it is a broad grant and Luke should know he is making it. And the token lands at `~/.kom-gdoc/token.json`; owner-only permissions are right, and it should stay out of every repo and every backup that leaves the machine.

**And the account caveat.** Luke says that session is a different account on a different machine. This connector is granted to `camerawrap@gmail.com`. A connector is an account-level grant, not a machine capability — so if Drive is not connected on the other account, the recipe above is unreachable there no matter how it is searched for, and `gdoc.py` is the right answer. If it is connected, it will authenticate as *that* account, which may hold no write access to `00 PRESS`.

**Fallback that needs nobody:** hand the text to this session and it writes the Doc.

## Also this turn — headshots corrected at the source

Luke corrected handoff 088 on three points. `5.6` now says all of it, and `press/epk.json` is at **rev 20**.

- **These four files are the masters.** No other copies, no higher-resolution set. My pointer at `Headshots/CCD Headshots` as a possible better grade was wrong and is removed.
- **Four is the complete set.** There is no headshot for the writer and one was never taken. The four-against-five arithmetic in 088 was a gap to design around, not one to chase — pages 5 and 6 should expect one bio without a portrait.
- Still the last thing `5.6` needs: **which file is which person**, so the four can take their `KILLER_OF_MEN_First_Last_Role` names. Not guessed here, and it should not be guessed there either.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-094-epk.md
**Model:** Opus 5. Pushed before the work commit — and it was needed: this is the second 094 collision in two turns.

## Next action (the one thing)

**Luke: which headshot is which person.** On the Doc, his call between two working routes — authorise `gdoc.py` for in-place updates, or hand the text to this session for a fresh Doc.

## Files

- The correction target: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-094-epk.md
- Their tool, worth keeping: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/gdoc.py
- EPK INFO, made through the connector: https://docs.google.com/document/d/1ae-MPbAq1otTtYA5-SSYYGd13jjvuz1Co2Zi0IrGvSI/edit
- EPK LINKS, same: https://docs.google.com/document/d/16x38uawE0Iq91JCj3AC7cVV7SnpCO7kNdBJ0Dj8vUKg/edit
- `00 PRESS`: https://drive.google.com/drive/folders/1utGEFQb5gDuUOC9JU7zvuslwRlwbRorx
- Headshots: https://github.com/Scroggdawg/kom-festival-board/tree/main/press/assets/HEADSHOTS
- The list: https://scroggdawg.github.io/kom-festival-board/epk.html
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-095-epk.md
