# Killer of Men — Festivals 2026–2027

The festival campaign for **Killer of Men**, a 13-minute AFI Conservatory thesis
short: 1834 South Carolina, an enslaved prize-fighter who reconnects with the
Yoruba faith of his ancestors. Picture locked January 2026.

**The live board: <https://scroggdawg.github.io/kom-festival-board/>**

Everything the campaign runs on lives in this repository — the board itself, the
research it was built from, the adversarial reviews it survived, and the running
log of decisions.

---

## The board

`index.html` is the whole application: a single self-contained page, no build
step, no dependencies. `data.json` is the single source of truth — 151
researched festivals, of which 97 are live targets.

It is **editable in the browser**. Click *Edit campaign*, record a submission or
a decision, then Publish; changes commit straight back to `data.json` through
the GitHub API using a fine-grained personal access token that the editor pastes
once and that never leaves their browser. No token is stored in this repository.

Campaign state is an **event ledger**, not a status field: every festival's
current standing is derived from the submissions, selections, rejections and
wins recorded against it, so the history stays intact and the counters can never
drift from the record.

| File | What it is |
|---|---|
| `index.html` | The board — UI, logic, publishing, all of it |
| `data.json` | Schema 2. Festivals, key dates, the premiere ledger |
| `mockup.html`, `mockup-detail.html` | Design markups the build was approved from |
| `PLAN-v2.md`, `PLAN-edit-ux.md` | Build specs, including the disagreements |
| `tools/` | Python utilities that regenerate and enrich `data.json` |

## `research/`

The August 2026 sweep that started the campaign: 117 festivals with per-record
sources, a long-form digest, and a strategy paper covering premiere law, the
Oscar qualifying window, and publicist timing.

## `readouts/`

- **`jm-75-decoded.html`** — a festival strategist's 256-festival list, her 75
  recommendations for this film decoded one by one: what each festival is, why
  she picked it, our verdict, and what it corrected in our own thinking.
  ([live](https://scroggdawg.github.io/kom-festival-board/readouts/jm-75-decoded.html))
- **`kom-dp-sheet.html`** — the cinematography lane, kept deliberately separate
  from the main board.
  ([live](https://scroggdawg.github.io/kom-festival-board/readouts/kom-dp-sheet.html))

## `reviews/`

Cross-family adversarial reviews. Every significant build was audited by a model
from a different family before shipping; these are the unedited transcripts,
including the verdicts that sent work back.

## `handoffs/`

The project log, oldest to newest. Each entry records what changed, what was
verified, what stayed uncertain, and the single next action. Read the highest
number first.

---

## Working on it

The board needs no toolchain — open `index.html`, or serve the folder:

```bash
python3 -m http.server 8642
```

The utilities in `tools/` expect to run from the repository root and rewrite
`data.json` in place. `embed-snapshot.py` refreshes the copy of the data
embedded in `index.html` as an offline fallback, and should be run after any
change to `data.json` that is committed by hand.

## Conventions worth knowing

- **Research facts are locked in the UI.** Dates, windows, fees and qualifying
  paths can only be changed through a correction that requires a source URL,
  which also re-stamps the record's `lastChecked`. Campaign facts — what was
  submitted, what came back — are freely editable.
- **`~` means estimated.** A date carrying it is a pattern-estimate from the
  previous cycle, not a confirmed deadline, because many 2027 editions are not
  yet announced.
- **Oscar-path scoring is cycle-specific.** In the fit heat map, a festival that
  qualifies for the Academy Awards but whose reachable edition falls outside the
  100th window (October 1, 2026 – September 30, 2027) scores low, because it
  cannot help this campaign even though it is a real qualifier.
- **Fit scores are assessed, not measured.** They are judgments from the
  research record, and the rubric is documented at the top of
  `tools/heat-expand.py`.
