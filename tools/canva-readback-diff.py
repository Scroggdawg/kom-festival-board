#!/usr/bin/env python3
"""Diff a Canva read-back (canva/readback/latest.json, from the app + tools/canva-readback-server.py)
against the contract (canva/ops/epk-canva.json): per page, text the design carries that the
contract does not (Luke's edits and additions) and contract text the design no longer has
(his deletions). Whitespace-normalised; case as written.

    <venv>/bin/python tools/canva-readback-diff.py [readback.json]
"""
import json, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPS = os.path.join(ROOT, "canva", "ops", "epk-canva.json")
RB = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "canva", "readback", "latest.json")
S = 1.333333


def norm(t):
    return re.sub(r"\s+", " ", t.replace(" ", " ")).strip()


def main():
    ops = json.load(open(OPS)); rb = json.load(open(RB))
    print(f"read-back {os.path.relpath(RB, ROOT)} ({rb.get('at')}, {rb.get('scope')}) vs contract generated {ops['generated']}")
    total_added = total_removed = 0
    for op_page, rb_page in zip(ops["pages"], rb["pages"]):
        want = Counter(norm(e["text"]) for e in op_page["elements"] if e["type"] == "text")
        have = Counter(norm(e.get("text", "")) for e in rb_page["elements"] if e["type"] == "text")
        added = have - want; removed = want - have
        n_img_want = sum(1 for e in op_page["elements"] if e["type"] == "image")
        n_img_have = sum(1 for e in rb_page["elements"] if e["type"] == "image")
        flag = "" if not added and not removed and n_img_want == n_img_have else "  <-- differs"
        print(f"p{op_page['n']:02d} {op_page['name']:20} design {rb_page['count']:3} elements / contract {op_page['count']:3}; "
              f"images {n_img_have}/{n_img_want}{flag}")
        for t, k in removed.items():
            print(f"     - not in design{' x' + str(k) if k > 1 else ''}: {t!r}")
        for t, k in added.items():
            els = [e for e in rb_page["elements"] if e["type"] == "text" and norm(e.get("text", "")) == t]
            pos = ", ".join(f"({e['left']/S:.0f},{e['top']/S:.0f})pt" for e in els[:3])
            print(f"     + in design only{' x' + str(k) if k > 1 else ''}: {t!r} at {pos}")
        total_added += sum(added.values()); total_removed += sum(removed.values())
    print(f"{total_added} text element(s) only in the design, {total_removed} only in the contract")


if __name__ == "__main__":
    main()
