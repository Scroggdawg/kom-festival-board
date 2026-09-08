# handoff-048-docket

## Where we left off

**This turn (Sep 8, 2026, Opus 5, goose):** the Sundance eligibility question is answered rather than escalated, and recording why found the fourth instance of my own recurring bug.

### The contradiction was a misreading, and it is withdrawn

The festival lane read the 2027 Rules PDF. The clause *"Only projects retaining world premiere status are eligible"* appears four times and **every instance attaches to a FEATURE category**. Shorts are not named and carry a far looser rule — public exhibition before Jan 1 2026 excludes, and numbered rule 11 exempts shorts screened *"at any number of festivals anywhere in the world."*

So a spent world premiere **does not** exclude this film from Sundance shorts. Moot for 2027, live for 2028.

**The generalisation is withdrawn explicitly** — that lane named it as speculation stacked on the misreading rather than quietly narrowing it, which is what let me delete it cleanly. **There is no new workstream, D.5.9 needs nothing, and last turn's "shape-of-the-campaign question" should be read as retracted.** The premiere ledger is unaffected: the world premiere is still spent, it simply matters less than was claimed.

What survives is a festival-domain checking habit — *"world premiere required" is frequently a feature-category rule, so check category specificity before writing a festival off* — and it belongs in their validator, not my file. Same reasoning as declining to re-derive the tier flag.

### The fourth instance

Extending `dateNote` with their process note, `push()` said **"nothing to push"** and the edit was gone. The earlier fix carried local-*only* top-level keys but treated every **shared** key as remote-wins, so editing one that already existed was unpublishable — and the overrule only printed on a successful push, so it was invisible too.

The rev ordering already said who was later and the code was not reading it. **Fixed:** a higher local rev means this machine's value is the newer edit and it wins; where revs have diverged the remote still wins and the key is named, now reported whether or not anything is published. Three cases tested.

**Four times today a local change vanished without a word** — title-only edits, the reset over an unpushed commit, top-level keys, and edits to existing ones. Every one the same shape: *the code modelled the common case and treated everything else as nothing rather than as something it did not understand.* That is worth more than any of the individual fixes.

### Recorded

`dateNote` now carries the summariser lesson as the same rule as the prose one rather than a new one: **a confident sentence standing in for a check, whether a person or a tool wrote it.** WebFetch's summariser reported Sundance's 2027 rules as a 2009 document containing no premiere or completion clauses; it is the 2027 document and contains every one of them. *"The document does not say" is not evidence the document does not say it.*

Rev 65, valid, published.

---

**Timestamp:** 2026-09-08
**Lane:** `docket`
**Continues:** handoff-047-docket.md
**Model:** Opus 5. **Goose turn** — a question answered and withdrawn, a fourth silent-loss path closed.

## Next action (the one thing)

Two questions, both still only Luke's: **is Jordan's YouTube link downloadable (D.3.1)**, which decides whether the campaign Vimeo must exist by Sep 15, and **does he have a file to upload at all (D.3.3)**.

## Files

- Dashboard: https://scroggdawg.github.io/kom-festival-board/
- Docket: https://scroggdawg.github.io/kom-festival-board/docket.html
- Truth, with both notes: https://github.com/Scroggdawg/kom-festival-board/blob/main/todo.json
- Writer: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/todo.py
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-047-docket.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-048-docket.md
- Mirror: file:///Users/scroggdawg/openclaw-handoffs/handoff-492-docket.md
