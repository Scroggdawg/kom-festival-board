# handoff-080-festival

## Where we left off

**This turn (Sep 8, 2026, Opus 5):** the docket declined to record the category-specific premiere habit, correctly — this lane had said it belongs where the tier rule lives. So it went into `tools/validate-data.py`. Then its diagnosis of its own fourth bug found one of the same shape here.

### The shape, and where it was hiding in this lane

The docket's words on the four local-change-vanishing bugs it fixed today:

> "the code modelled the common case and treated everything else as nothing rather than as something it did not understand"

**The dated-tier check had exactly that shape.** It only matches tiers written with an explicit year — a deliberate choice, to avoid guessing — and **skipped 18 records in silence**, so they read as passing when they were merely unexamined. Silence was being mistaken for cleanliness.

### Two advisories, both saying "unchecked" where the tool used to say nothing

- **UNDATED TIER** — feesText names a tier but no year appears, so the dated-tier check could not run. **18 records**, including Tampere, Atlanta, Flickerfest, SXSW.
- **PROSE PREMIERE** — a premiere rule asserted only in `why` while the structured `premiere` field is null. **That field was null on all 97 targets.** Premiere requirements are frequently FEATURE-category rules, and reading one as a shorts rule cost this lane a retracted claim about Sundance today. Four records: Tribeca, Curtas Vila do Conde, TIFF Short Cuts, IFFR.

### IFFR's premiere rule is now structured rather than prose

Its shorts rule was verified first-party this morning — *"world, international or European"* — so `premiere` now carries it and the warning clears. **Three left, all genuinely unchecked.** And `premiere` set without a `source` is now an error under `--strict`, so the field cannot become another place to assert something with no check behind it — which is what `sourceUrl` was.

---

**Timestamp:** 2026-09-08
**Lane:** `festival`
**Continues:** handoff-079-festival.md
**Model:** Opus 5.

## Next action (the one thing)

Two questions with Luke, unchanged, both gating the only real deadline:

1. **Does he have a file he can upload?** Decides whether IFFR Sep 15 is reachable at all.
2. **IFFR — yes or no?**

And the cheap one: **Aspen's tier names off FilmFreeway** (403 to automated fetch; he has an account).

Three unchecked premiere claims sit behind those — Tribeca, Curtas Vila do Conde, TIFF Short Cuts — each a festival this campaign may be wrongly counting in or out.

## Files

- Board data: https://github.com/Scroggdawg/kom-festival-board/blob/main/data.json
- The gate: https://github.com/Scroggdawg/kom-festival-board/blob/main/tools/validate-data.py
- Page draft v6 (for Jordan): https://github.com/Scroggdawg/kom-festival-board/blob/main/press/filmfreeway-page-v6.docx
- Prior handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-079-festival.md
- This handoff: https://github.com/Scroggdawg/kom-festival-board/blob/main/handoffs/handoff-080-festival.md
