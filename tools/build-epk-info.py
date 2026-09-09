#!/usr/bin/env python3
"""Render press/epk.json as the text of the Drive doc "EPK INFO".

    python3 tools/build-epk-info.py > /tmp/epk-info.txt

epk.json is the truth; this is a view of it. Every field appears, filled or not,
so the doc shows the gaps instead of hiding them. A field with candidates and no
choice made prints every candidate. Regenerate and repaste after any epk.py set.
"""
import json, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "press", "epk.json"), encoding="utf-8"))

out = []
w = out.append
w("KILLER OF MEN — EPK INFO")
w("All the text of the press kit, in one place.")
w("")
w(f"Generated from press/epk.json rev {D['rev']} on {datetime.date.today().isoformat()}.")
w("epk.json is the source of truth. Edit there (or on the worksheet page), then regenerate")
w("this doc with tools/build-epk-info.py — do not treat this document as the master.")
w("Worksheet: https://scroggdawg.github.io/kom-festival-board/epk.html")
w("")
filled = sum(1 for s in D["sections"] for f in s["fields"] if f["value"].strip())
total = sum(len(s["fields"]) for s in D["sections"])
w(f"{filled} of {total} fields filled. Everything marked NEEDED is still missing.")
w("")

for s in D["sections"]:
    w("")
    w("")
    w(f"PAGE {s['num']} — {s['name'].upper()}")
    for f in s["fields"]:
        w("")
        w(f"{f['n']}  {f['label']}")
        v = f["value"].strip()
        if v:
            for line in v.split("\n"):
                w("    " + line)
        elif f.get("options"):
            w("    UNDECIDED — the text is written, the choice is not made:")
            for c in f["options"]:
                w("")
                note = f" ({c['note']})" if c.get("note") else ""
                w(f"    Version {c['key']}{note}:")
                for line in c["value"].split("\n"):
                    w("      " + line)
        else:
            w("    NEEDED")

w("")
w("")
w("HOW TO USE THIS DOCUMENT")
w("")
w("Fill a gap by editing the worksheet page, not this doc, then regenerate.")
w("The numbers (1.1 … A.6) are permanent — quote them when you send material.")
sys.stdout.write("\n".join(out) + "\n")
