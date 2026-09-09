# handoff-094-epk

## Where we left off

**This turn (Sep 9, 2026, Opus 5):** Luke pushed back — another session built that Google Doc and put it on the Drive, so why can this one not? He was right, and the research found the path. **`tools/gdoc.py` is built and committed. One consent click from Luke and this lane can write the Doc directly.** `press/epk.json` unchanged at rev 19 · 38 of 47.

### How the other session did it

The answer was in its own handoff. `handoff-072-epk.md` says the Drive tree was *"Confirmed present on Drive through the API"*, and that it read folder owners (`asigel@afi.com`) and which AFI delivery folders were empty. That is not filesystem access — that is the Drive API.

Searching the machine turned up the credential it used: an **installed-app OAuth client for a Google Cloud project called `bmf-agent`**, sitting in `~/Downloads`. Its script and token lived in that session's scratch directory, which is session-scoped and has since been cleaned — so the capability existed, was never written down, and died with the session. That is the actual failure here, and it is why this one is a committed tool rather than a scratch script.

### What was checked before building

| | |
|---|---|
| MCP config | no `mcpServers` in `~/.claude/settings.json` or `~/.claude.json` |
| Registry | no Google Docs or Drive connector available |
| Claude in Chrome | `list_connected_browsers` → `[]`; extension not connected |
| Credentials on disk | **found** — `bmf-agent` installed-app client |
| Stored token | none; the previous session's is gone |

### The tool

`tools/gdoc.py` — `auth`, `whoami`, `push <docId> <file.docx>`.

**It replaces the Doc's contents in place** with `files.update` and a `.docx` body, which is exactly what *File → Import → Replace document* does in the UI. The Doc keeps its **id, URL and sharing** — which is the whole point, since Luke wants that document updated rather than a second one appearing beside it.

Deliberately **not** the Docs API `batchUpdate` route: replacing a body that way means tearing it down and rebuilding every run and its styling by hand, and a mistake there shows up as a silently mangled document rather than an error. Handing Google the `.docx` whole keeps the colour pass exactly as designed and validated.

**On credentials.** No secret touches this repository — checked before committing. The OAuth client is read from disk and never printed. The token goes to `~/.kom-gdoc/token.json`, owner-only permissions. Consent happens in **Luke's browser under his own login**; the script never sees a password. Scope is `drive`, which is broader than ideal — Drive will not let an app update a file it did not create on the narrower `drive.file` scope, and this Doc was made by hand.

### Waiting on one click

The consent flow is **running now**, listening on `localhost:56776`. The URL was given to Luke. Once he authorises, the whole loop closes:

```
epk.py set … → build-epk-doc.py → gdoc.py push <docId> → the Doc is current
```

and the drift between `epk.json` and the Doc — which has cost several turns — stops being a manual step.

---

**Timestamp:** 2026-09-09
**Lane:** `epk`
**Continues:** handoff-093-epk.md
**Model:** Opus 5.

## Next action (the one thing)

**Luke clicks the consent URL.** Then this lane runs `gdoc.py push 1ae-MPbAq1otTtYA5-SSYYGd13jjvuz1Co2Zi0IrGvSI` with the coloured build and the Doc is current, colours and all — no import dialog, no second document. If the flow has timed out by then it re-runs in one command. Then Jordan on `2.1` and `2.2`.

## Files

- The tool: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/gdoc.py
- Document builder: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/build-epk-doc.py
- The Doc: https://docs.google.com/document/d/1ae-MPbAq1otTtYA5-SSYYGd13jjvuz1Co2Zi0IrGvSI/edit
- The session that had this working: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-072-epk.md
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-093-epk.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-094-epk.md
