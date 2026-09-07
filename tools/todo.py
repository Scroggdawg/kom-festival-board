#!/usr/bin/env python3
"""The Docket's only writer. todo.json is the truth; never hand-edit it.

  todo.py list                      print every item with its status
  todo.py set <id> <status> [...]   set one or more items: not_started | started | awaiting | complete
  todo.py note <id> "<text>"        append a note to an item
  todo.py check                     validate the file
  todo.py push                      commit todo.json and push (after set/note; separate so batches are one commit)

docket_server.py imports set_status / save / push from here, so the browser writes the same way.
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
    raise KeyError(f"no item {iid}")
def check(d):
    errs = []; seen = set()
    if d.get("schema") != 1: errs.append("schema must be 1")
    for s, it in items(d):
        if it["id"] in seen: errs.append(f"duplicate id {it['id']}")
        seen.add(it["id"])
        if it["status"] not in STATUSES: errs.append(f"{it['id']}: bad status {it['status']}")
        if not it.get("title"): errs.append(f"{it['id']}: no title")
    return errs
def normalise(st):
    st = ALIASES.get(st, st).replace("-", "_")
    if st not in STATUSES: raise ValueError(f"bad status {st}; one of {STATUSES}")
    return st
def set_status(d, iid, st, by="todo.py"):
    """Change one item in memory. Returns True if it changed."""
    st = normalise(st); s, it = find(d, iid)
    if it["status"] == st: return False
    it["status"] = st; it["history"].append({"at": now(), "status": st, "by": by}); return True
def save(d, by):
    errs = check(d)
    if errs: raise ValueError("refused: " + "; ".join(errs))
    d["rev"] = int(d.get("rev", 0)) + 1; d["updated"] = now(); d["updatedBy"] = by
    fd, tmp = tempfile.mkstemp(dir=ROOT, prefix=".todo.", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, PATH)
    return d["rev"]
def _git(*a, check=True, env=None):
    return subprocess.run(["git", "-C", ROOT, *a], check=check, capture_output=True, text=True, env=env)
def _branch():
    return _git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
def _rebuild_onto(base, branch):
    """Put HEAD's todo.json on top of `base` without touching the working tree.

    The repo is shared with other sessions, so it is often dirty: `pull --rebase`
    would refuse, and stashing could collide with another session's stash. This
    writes the new commit through a temporary index instead — no checkout, no stash.
    Refuses if main carries unpushed commits other than ours."""
    ahead = _git("rev-list", f"{base}..HEAD").stdout.split()
    if len(ahead) != 1: raise RuntimeError(f"{len(ahead)} unpushed commits on {branch}; not rewriting them")
    blob = _git("rev-parse", "HEAD:todo.json").stdout.strip()
    msg = _git("log", "-1", "--format=%B").stdout.strip()
    fd, idx = tempfile.mkstemp(prefix=".docket-index."); os.close(fd); os.unlink(idx)
    env = dict(os.environ, GIT_INDEX_FILE=idx)
    try:
        _git("read-tree", base, env=env)
        _git("update-index", "--cacheinfo", f"100644,{blob},todo.json", env=env)
        tree = _git("write-tree", env=env).stdout.strip()
    finally:
        if os.path.exists(idx): os.unlink(idx)
    new = _git("commit-tree", tree, "-p", base, "-m", msg).stdout.strip()
    _git("update-ref", f"refs/heads/{branch}", new, "HEAD")
def push(message=None):
    """Commit todo.json alone (if changed) and push it. Never touches other files."""
    branch = _branch()
    if _git("diff", "--quiet", "HEAD", "--", "todo.json", check=False).returncode != 0:
        _git("commit", "--only", "todo.json", "-q", "-m", message or f"docket: todo.json rev {load().get('rev')}")
    _git("fetch", "-q", "origin", branch)
    if not _git("rev-list", f"origin/{branch}..HEAD").stdout.split():
        return "nothing to push"
    err = ""
    for _ in range(4):
        p = _git("push", "-q", "origin", f"HEAD:{branch}", check=False)
        if p.returncode == 0: return "pushed"
        err = (p.stderr or p.stdout).strip().splitlines()[-1] if (p.stderr or p.stdout).strip() else "rejected"
        _git("fetch", "-q", "origin", branch)
        _rebuild_onto(f"origin/{branch}", branch)
    return "push failed: " + err

def main(a):
    if not a or a[0] in ("-h", "--help"): print(__doc__); return
    cmd = a[0]; d = load()
    try:
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
                if set_status(d, iid, st): print(f"{iid} → {d['statusLabels'][normalise(st)]}")
            print(f"todo.json rev {save(d, 'todo.py set')} written")
        elif cmd == "note":
            s, it = find(d, a[1]); it.setdefault("notes", []).append({"at": now(), "text": " ".join(a[2:])})
            print(f"todo.json rev {save(d, 'todo.py note')} written")
        elif cmd == "push": print(push())
        else: sys.exit(f"unknown command {cmd}")
    except (KeyError, ValueError) as e: sys.exit(str(e))
if __name__ == "__main__": main(sys.argv[1:])
