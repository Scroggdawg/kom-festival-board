#!/usr/bin/env python3
"""Render press/epk-one-sheet.md from press/epk.json: every field, its state, who supplies it.

    python3 tools/build-epk-one-sheet.py > press/epk-one-sheet.md

epk.json is the truth; this is a view of it, regenerated after any epk.py set. It replaces
the hand-written Sep 8 sheet, which described 47 fields and predates the permanent numbering.

A field's state is read, not judged:
    HAVE      value present, no `waiting`
    PARTIAL   value present and `waiting` set, or the value's first word is PARTIAL
    CHOOSE    no value, two or more `options` recorded
    WAITING   no value, `waiting` names someone
    EMPTY     nothing yet, nobody named
"""
import json, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "press", "epk.json"), encoding="utf-8"))

MARK = {"HAVE": "●", "PARTIAL": "◐", "CHOOSE": "◑", "WAITING": "⌀", "EMPTY": "○"}


def state(f):
    v = f.get("value", "").strip()
    if v:
        if f.get("waiting") or v.split(" ", 1)[0].rstrip(",:") == "PARTIAL":
            return "PARTIAL"
        return "HAVE"
    if f.get("options"):
        return "CHOOSE"
    if f.get("waiting"):
        return "WAITING"
    return "EMPTY"


def who(f, st):
    if st == "HAVE":
        return "—"
    if f.get("waiting"):
        return f["waiting"]
    if st == "CHOOSE":
        return "Luke or Jordan to pick"
    return "unassigned"


def first_line(f):
    v = " ".join(f.get("value", "").split())
    if not v and f.get("options"):
        return f"{len(f['options'])} versions: " + ", ".join(o["key"] for o in f["options"])
    return (v[:88] + "…") if len(v) > 89 else v


out = []
w = out.append
counts = {k: 0 for k in MARK}
rows = []
for s in D["sections"]:
    for f in s["fields"]:
        st = state(f)
        counts[st] += 1
        rows.append((s, f, st))

total = len(rows)
w("# Killer of Men — EPK, all the pieces")
w("")
w(f"*Generated from `press/epk.json` rev {D['rev']} on {datetime.date.today().isoformat()} by "
  "`tools/build-epk-one-sheet.py`. The live list is `press/epk.json`, rendered at "
  "[epk.html](https://scroggdawg.github.io/kom-festival-board/epk.html). Regenerate this sheet "
  "after any change; do not edit it by hand.*")
w("")
w("● have it · ◐ partly, the rest named · ◑ written, a choice pending · ⌀ waiting on someone · ○ nothing yet")
w("")
w(f"**{counts['HAVE']} of {total} fields complete**, {counts['PARTIAL']} partial, "
  f"{counts['CHOOSE']} awaiting a choice, {counts['WAITING']} waiting on a person, "
  f"{counts['EMPTY']} empty.")
w("")
w("| | Field | State | Who | What is there |")
w("|---|---|---|---|---|")
for s, f, st in rows:
    w(f"| {MARK[st]} | **{f['n']}** {f['label']} | {st} | {who(f, st)} | {first_line(f)} |")
w("")

open_rows = [(s, f, st) for s, f, st in rows if st != "HAVE"]
if open_rows:
    w("## Still open, by person")
    w("")
    by = {}
    for s, f, st in open_rows:
        by.setdefault(who(f, st), []).append((f, st))
    for person, items in by.items():
        w(f"**{person}**")
        w("")
        for f, st in items:
            w(f"- {f['n']} {f['label']} ({st.lower()})")
        w("")

print("\n".join(out))
