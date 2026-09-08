#!/usr/bin/env python3
"""Validate data.json before it is committed.

Written 2026-09-08 after a prefix match ("curta") wrote Curta Cinema Rio's dates
onto Curtas Vila do Conde, a different festival. Caught by luck on a read-back.
This makes the read-back mandatory instead of lucky.

  validate-data.py              structural checks; exit 1 on any error
  validate-data.py --provenance also report deadline provenance (advisory)
  validate-data.py --strict     make provenance an error, not a warning
  validate-data.py --write-flags recompute and write the derived closeUnverifiedTier flag
                                (also stamps flagsComputedAt, so readers can spot staleness)

The flag exists because the campaign dashboard (index.html, another lane's surface)
wanted the suspect count on the front page. Re-implementing the rule there would
give two implementations of one rule, which drift -- we paid for that once already
with `source` and `sourceUrl` holding the same fact and two validators disagreeing
about which was authoritative. So the rule lives HERE, once, and its result is
written into the data for anyone to read.

Derived data rots silently -- an embedded snapshot in board.html did exactly that
this week. So a plain run RECOMPUTES every flag and errors if a stored one
disagrees. The flag cannot go stale without the gate saying so. Editing feesText
or provenance from the board's browser publish will make it stale; the next
validator run catches it, and --write-flags fixes it.

Structural checks (always errors):
  schema is 2 · rev and updated present · ids unique and non-empty
  disposition in target|bench|out · dates are ISO yyyy-mm-dd and parse
  close is not before open · premiere ledger ids unique, states valid
  events reference known types · no festival is missing a name
  close is not earlier than a dated tier the record's own feesText names

The last one was added Sep 8, 2026, after the same error appeared three times in
one day: Short Shorts "Sep 9" was a pitch-competition deadline, then Sep 30 (its
early tier) while its own feesText said the final was Jan 15 2027; and SBIFF's
close held Sep 18, the regular fee tier, while the final was Dec 2. `close` means
the FINAL door -- board.html says so in its own words: "Sorted by final deadline:
read top to bottom as the order the doors close." A tier date in that field makes
every consumer downstream call a price step a deadline.

The rule, narrowed each time it failed: a date is not a deadline until something
names its tier -- and a verification that lives only in prose is not one.

Provenance checks (advisory unless --strict), the rule learned the hard way:
  a close date is only trustworthy with the festival's own page behind it
  (source URL) and the tier or category named beside it (feesText/why).
"""
import json, sys, re, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data.json")
DISPOSITIONS = {"target", "bench", "out"}
EVENT_TYPES = {"submitted", "withdrawn", "selected", "not_selected", "screened", "nominated", "won"}
PREMIERE_STATES = {"available", "reserved", "spent"}
TIER = re.compile(r"early|earlybird|early bird|regular|late|final|official|extended|deadline|tier|rolling", re.I)
LATER_TIER = re.compile(r"\b([A-Za-z]{3})[a-z]*\.?\s+(\d{1,2}),?\s*(\d{4})\b")
MONTHS = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}

def dated_tiers(text):
    """Explicitly-dated tiers named in free text. Year must be written out --
    an inferred year would guess, and guessing is the bug this catches."""
    out = []
    for m in LATER_TIER.finditer(text or ""):
        mo = MONTHS.get(m.group(1).lower())
        if not mo: continue
        try: out.append((datetime.date(int(m.group(3)), mo, int(m.group(2))), m.group(0)))
        except ValueError: pass
    return out
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def d(s):
    try: return datetime.date.fromisoformat(s)
    except Exception: return None

FLAG = "closeUnverifiedTier"
STAMP = "flagsComputedAt"

def suspect(f):
    """True when an unverified target's own feesText names a later tier, so its
    close may be a fee tier rather than the final door -- as SBIFF's was.

    KNOWN FALSE-POSITIVE MODE, found Sep 8 2026 on Sundance: "late" is very often
    the NAME of a festival's final tier, not evidence that a later one exists.
    Sundance's ladder is early / official / LATE, and its close was correct. So a
    flag means WORTH CHECKING, never DEFECT -- the only way to clear one is a
    first-party read. That read is still worth doing: checking Sundance turned up
    an unresolved premiere-eligibility contradiction that mattered more than
    the date did.
    """
    return bool(
        f.get("disposition") == "target"
        and f.get("close")
        and f.get("provenance") != "official"
        and re.search(r"\b(final|late|extended)\b", f.get("feesText") or "", re.I)
    )

def main(argv):
    prov = "--provenance" in argv or "--strict" in argv
    strict = "--strict" in argv
    write_flags = "--write-flags" in argv
    data = json.load(open(PATH, encoding="utf-8"))
    errs, warns = [], []

    if data.get("schema") != 2: errs.append("schema must be 2")
    for k in ("rev", "updated", "festivals", "premieres"):
        if k not in data: errs.append(f"missing top-level key: {k}")

    seen = set()
    for f in data.get("festivals", []):
        fid = f.get("id")
        if not fid: errs.append(f"festival with no id: {f.get('name','?')}"); continue
        if fid in seen: errs.append(f"duplicate id: {fid}")
        seen.add(fid)
        if not f.get("name"): errs.append(f"{fid}: no name")
        if f.get("disposition") not in DISPOSITIONS:
            errs.append(f"{fid}: bad disposition {f.get('disposition')!r}")
        for k in ("open", "close", "festDate"):
            v = f.get(k)
            if v is None: continue
            if not DATE.match(str(v)) or d(v) is None:
                errs.append(f"{fid}: {k} is not a valid ISO date: {v!r}")
        o, c = d(f.get("open") or ""), d(f.get("close") or "")
        if o and c and c < o: errs.append(f"{fid}: close {c} is before open {o}")
        for e in f.get("events") or []:
            if e.get("type") not in EVENT_TYPES:
                errs.append(f"{fid}: unknown event type {e.get('type')!r}")
        if c:
            for dt, txt in dated_tiers(f.get("feesText")):
                if dt > c:
                    errs.append(f"{fid}: close {c} is EARLIER than a tier its own feesText dates "
                                f"({txt!r}) — close must be the final door, not a fee tier")
        if prov and f.get("disposition") == "target" and f.get("close"):
            if not f.get("source"):
                (errs if strict else warns).append(f"{fid}: close date with no source URL")
            if not TIER.search((f.get("feesText") or "") + " " + (f.get("why") or "")):
                (errs if strict else warns).append(f"{fid}: close date with no tier or category named")
            if suspect(f):
                warns.append(f"{fid}: feesText names a later tier but the record is unverified — "
                             f"close {f.get('close')} may be a fee tier, as SBIFF's was")

    pids = set()
    for p in data.get("premieres", []):
        if p.get("id") in pids: errs.append(f"duplicate premiere id: {p.get('id')}")
        pids.add(p.get("id"))
        if p.get("state") not in PREMIERE_STATES:
            errs.append(f"premiere {p.get('id')}: bad state {p.get('state')!r}")

    # derived flag: recompute always, write only on request, error on disagreement
    stale, flagged = [], 0
    for f in data.get("festivals", []):
        want, have = suspect(f), bool(f.get(FLAG))
        if want: flagged += 1
        if want != have:
            if write_flags:
                if want: f[FLAG] = True
                else: f.pop(FLAG, None)
            else:
                stale.append(f"{f.get('id')}: stored {FLAG}={have} but computed {want} — "
                             f"run --write-flags")
    if write_flags and not errs:
        # Stamp what the flags were computed against. The dashboard cannot otherwise
        # tell a fresh flag from a stale one: a board publish bumps `rev` without
        # recomputing, so rev != stamped rev means "these flags predate the data".
        data[STAMP] = {"rev": data.get("rev"), "at": datetime.date.today().isoformat(),
                       "flagged": flagged, "by": "tools/validate-data.py --write-flags"}
        json.dump(data, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        open(PATH, "a", encoding="utf-8").write("\n")
        print(f"  wrote {FLAG} — {flagged} record(s) flagged")
    errs.extend(stale)

    n = len(data.get("festivals", []))
    tgt = sum(1 for f in data["festivals"] if f.get("disposition") == "target")
    print(f"data.json — {n} festivals, {tgt} targets, schema {data.get('schema')}, rev {str(data.get('rev'))[:8]}")
    for w in warns: print(f"  WARN  {w}")
    for e in errs: print(f"  ERROR {e}")
    if warns and not strict:
        print(f"\n  {len(warns)} provenance warnings — advisory. Run with --strict to make them errors.")
    print("\n" + ("REFUSED — fix the errors above" if errs else "clean"))
    return 1 if errs else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
