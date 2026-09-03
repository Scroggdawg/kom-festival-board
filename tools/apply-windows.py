#!/usr/bin/env python3
"""Apply researched submission windows + portal links to data.json.

Reads JSONL from the file given as argv[1] — one object per line:
  {"id","site","filmfreeway","open","open_est","close","close_est","note"}
`open`/`close` optional (link-only records omit them). Empty strings are
ignored, never written. Sets `estimated` true when either date is a
pattern-estimate. Appends the note to the record's `why` provenance only when
it flags something material (a passed deadline, a portal that isn't
FilmFreeway). Run from site/.
"""
import json, sys, re, uuid

if len(sys.argv) < 2: sys.exit("usage: apply-windows.py <jsonl-file> [more...]")

recs = {}
for path in sys.argv[1:]:
    for line in open(path):
        line = line.strip()
        if not line or not line.startswith("{"): continue
        try: o = json.loads(line)
        except json.JSONDecodeError:
            print(f"  ! unparseable line skipped: {line[:70]}"); continue
        if o.get("id"): recs[o["id"]] = o

D = json.load(open("data.json"))
by_id = {f["id"]: f for f in D["festivals"]}

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
stats = dict(open_set=0, close_set=0, site=0, ff=0, portal_note=0, missing=[])

for fid, o in recs.items():
    f = by_id.get(fid)
    if not f:
        stats["missing"].append(fid); continue
    links = f.setdefault("links", {})
    if o.get("site", "").startswith("https://") and not links.get("site"):
        links["site"] = o["site"]; stats["site"] += 1
    if o.get("filmfreeway", "").startswith("https://filmfreeway.com/") and not links.get("filmfreeway"):
        links["filmfreeway"] = o["filmfreeway"]; stats["ff"] += 1

    est = False
    if DATE.match(o.get("open", "") or ""):
        f["open"] = o["open"]; stats["open_set"] += 1
        est = est or bool(o.get("open_est"))
    if DATE.match(o.get("close", "") or ""):
        f["close"] = o["close"]; stats["close_set"] += 1
        est = est or bool(o.get("close_est"))
    if est: f["estimated"] = True
    elif o.get("open") and o.get("close") and not o.get("open_est") and not o.get("close_est"):
        f["estimated"] = False

    note = (o.get("note") or "").strip()
    if note:
        low = note.lower()
        material = any(k in low for k in ("portal", "passed", "closed", "not on filmfreeway",
                                          "no filmfreeway", "email", "inactive", "dormant", "defunct"))
        if material and note not in (f.get("why") or ""):
            f["why"] = ((f.get("why") or "").rstrip() + " Submission note: " + note).strip()
            stats["portal_note"] += 1
    f["lastChecked"] = "2026-09-03"

ids = [f["id"] for f in D["festivals"]]
if len(ids) != len(set(ids)): sys.exit("DUPLICATE IDS — aborting")

D["rev"] = str(uuid.uuid4()); D["updated"] = "2026-09-03"
json.dump(D, open("data.json", "w"), ensure_ascii=False, indent=1)

t = [f for f in D["festivals"] if f["disposition"] == "target"]
print(f"applied {len(recs)} records: opens {stats['open_set']}, closes {stats['close_set']}, "
      f"sites {stats['site']}, filmfreeway {stats['ff']}, portal notes {stats['portal_note']}")
if stats["missing"]: print("  ! unknown ids:", stats["missing"])
print(f"targets {len(t)} | still no open: {sum(1 for f in t if not f.get('open'))}"
      f" | no site: {sum(1 for f in t if not (f.get('links') or {}).get('site'))}"
      f" | no filmfreeway: {sum(1 for f in t if not (f.get('links') or {}).get('filmfreeway'))}")
print("rev:", D["rev"])
