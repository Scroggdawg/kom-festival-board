#!/usr/bin/env python3
"""Validate data.json before it is committed.

Written 2026-09-08 after a prefix match ("curta") wrote Curta Cinema Rio's dates
onto Curtas Vila do Conde, a different festival. Caught by luck on a read-back.
This makes the read-back mandatory instead of lucky.

  validate-data.py              structural checks; exit 1 on any error
  validate-data.py --provenance also report deadline provenance (advisory)
  validate-data.py --strict     make provenance an error, not a warning

Structural checks (always errors):
  schema is 2 · rev and updated present · ids unique and non-empty
  disposition in target|bench|out · dates are ISO yyyy-mm-dd and parse
  close is not before open · premiere ledger ids unique, states valid
  events reference known types · no festival is missing a name

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
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def d(s):
    try: return datetime.date.fromisoformat(s)
    except Exception: return None

def main(argv):
    prov = "--provenance" in argv or "--strict" in argv
    strict = "--strict" in argv
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
        if prov and f.get("disposition") == "target" and f.get("close"):
            if not f.get("source"):
                (errs if strict else warns).append(f"{fid}: close date with no source URL")
            if not TIER.search((f.get("feesText") or "") + " " + (f.get("why") or "")):
                (errs if strict else warns).append(f"{fid}: close date with no tier or category named")

    pids = set()
    for p in data.get("premieres", []):
        if p.get("id") in pids: errs.append(f"duplicate premiere id: {p.get('id')}")
        pids.add(p.get("id"))
        if p.get("state") not in PREMIERE_STATES:
            errs.append(f"premiere {p.get('id')}: bad state {p.get('state')!r}")

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
