#!/usr/bin/env python3
"""The Docket's only writer. todo.json is the truth; never hand-edit it.

  todo.py list                      print every item with its status
  todo.py set <id> <status> [...]   set one or more items: not_started | started | awaiting | complete
  todo.py note <id> "<text>"        append a note to an item
  todo.py check                     validate the file
  todo.py push                      commit todo.json and push (after set/note; separate so batches are one commit)
"""
import json, os, sys, datetime, subprocess, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "todo.json")
STATUSES = ["not_started", "started", "awaiting", "complete"]
ALIASES = {"not started": "not_started", "awaiting response": "awaiting", "done": "complete", "waiting": "awaiting"}

def load():
    with open(PATH, encoding="utf-8") as f: return json.load(f)
def now(): return datetime.datetime.now().astimezone().isoformat(timespec="seconds")
def items(d):
    for s in d["sections"]:
        for it in s["items"]: yield s, it
def find(d, iid):
    for s, it in items(d):
        if it["id"] == iid: return s, it
    sys.exit(f"no item {iid}")
def check(d):
    errs = []; seen = set()
    if d.get("schema") != 1: errs.append("schema must be 1")
    for s, it in items(d):
        if it["id"] in seen: errs.append(f"duplicate id {it['id']}")
        seen.add(it["id"])
        if it["status"] not in STATUSES: errs.append(f"{it['id']}: bad status {it['status']}")
        if not it.get("title"): errs.append(f"{it['id']}: no title")
    return errs
def save(d, by):
    errs = check(d)
    if errs: sys.exit("refused: " + "; ".join(errs))
    d["rev"] = int(d.get("rev", 0)) + 1; d["updated"] = now(); d["updatedBy"] = by
    fd, tmp = tempfile.mkstemp(dir=ROOT, prefix=".todo.", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, PATH)
    print(f"todo.json rev {d['rev']} written")

def main(a):
    if not a or a[0] in ("-h", "--help"): print(__doc__); return
    cmd = a[0]; d = load()
    if cmd == "list":
        for s in d["sections"]:
            done = sum(it["status"] == "complete" for it in s["items"])
            print(f"\n{s['name']}  {done}/{len(s['items'])} complete")
            for it in s["items"]:
                w = f"  ⌀ {it['waitingOn']}" if it.get("waitingOn") else ""
                print(f"  {it['id']:6} {d['statusLabels'][it['status']]:18} {it['title'][:70]}{w}")
    elif cmd == "check":
        errs = check(d); print("clean" if not errs else "\n".join(errs)); sys.exit(1 if errs else 0)
    elif cmd == "set":
        pairs = a[1:]
        if len(pairs) % 2: sys.exit("usage: set <id> <status> [<id> <status> ...]")
        for iid, st in zip(pairs[::2], pairs[1::2]):
            st = ALIASES.get(st, st).replace("-", "_")
            if st not in STATUSES: sys.exit(f"bad status {st}; one of {STATUSES}")
            s, it = find(d, iid)
            if it["status"] != st:
                it["status"] = st; it["history"].append({"at": now(), "status": st, "by": "todo.py"})
                print(f"{iid} → {d['statusLabels'][st]}")
        save(d, "todo.py set")
    elif cmd == "note":
        s, it = find(d, a[1]); it.setdefault("notes", []).append({"at": now(), "text": " ".join(a[2:])}); save(d, "todo.py note")
    elif cmd == "push":
        subprocess.run(["git", "-C", ROOT, "add", "todo.json"], check=True)
        r = subprocess.run(["git", "-C", ROOT, "diff", "--cached", "--quiet"])
        if r.returncode == 0: print("nothing to commit"); return
        subprocess.run(["git", "-C", ROOT, "commit", "-q", "-m", f"docket: todo.json rev {d['rev']}"], check=True)
        subprocess.run(["git", "-C", ROOT, "pull", "-q", "--rebase"], check=True)
        subprocess.run(["git", "-C", ROOT, "push", "-q"], check=True); print("pushed")
    else: sys.exit(f"unknown command {cmd}")
if __name__ == "__main__": main(sys.argv[1:])
