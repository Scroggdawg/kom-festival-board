#!/usr/bin/env python3
"""The Docket's only writer. todo.json is the truth; never hand-edit it.

  todo.py list                      print every item with its status
  todo.py set <id> <status> [...]   set one or more items: not_started | started | awaiting | complete
  todo.py note <id> "<text>"        append a note to an item
  todo.py title <id> "<text>"       correct an item's wording
  todo.py due <id> <YYYY-MM-DD|->   set or clear an item's date
  todo.py waiting <id> <who|->      set or clear who an item is waiting on
  todo.py check                     validate the file
  todo.py push                      merge with origin and publish
  todo.py pull                      take origin's todo.json when nothing local is pending

docket_server.py imports from here, so the browser and the command line share one writer.

Two machines write this file: this one, and whoever opens the published page with a
token. So push() never overwrites the remote wholesale — it merges item by item, the
newer history entry wins, and both histories are kept.

push() rebases by resetting to origin, which throws away uncommitted work. It therefore
runs only in a checkout marked `.docket-clone` — a clone kept for the Docket alone — and
only when todo.json is the sole modified file. Anywhere else it commits todo.json alone
and, if the push is rejected, stops and says so rather than rewriting anything.
"""
import json, os, re, sys, datetime, subprocess, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "todo.json")
DEDICATED = os.path.exists(os.path.join(ROOT, ".docket-clone"))
STATUSES = ["not_started", "started", "awaiting", "complete"]
ALIASES = {"not started": "not_started", "awaiting response": "awaiting", "done": "complete", "waiting": "awaiting"}
class Conflict(Exception): pass

def load(path=None):
    with open(path or PATH, encoding="utf-8") as f: return json.load(f)
def now(): return datetime.datetime.now().astimezone().isoformat(timespec="seconds")
def dumps(d): return json.dumps(d, ensure_ascii=False, indent=1)
def items(d):
    for s in d["sections"]:
        for it in s["items"]: yield s, it
def find(d, iid):
    for s, it in items(d):
        if it["id"] == iid: return s, it
    raise KeyError(f"no item {iid}")
def _iso_date(v):
    try: datetime.date.fromisoformat(v); return True
    except (ValueError, TypeError): return False
def _iso_stamp(v):
    try: datetime.datetime.fromisoformat(v); return True
    except (ValueError, TypeError): return False
def _hex(v): return isinstance(v, str) and re.fullmatch(r"#[0-9a-fA-F]{3,8}", v) is not None
def _filled(v): return isinstance(v, str) and v.strip() != ""
def check(d):
    """Every rule here was true of the file when it was written. They are stated so the
    file cannot drift out of them — an absent value is null, never an empty string, and a
    date either parses or is refused."""
    errs = []
    if d.get("schema") != 1: errs.append("schema must be 1")
    if not isinstance(d.get("rev"), int): errs.append("rev must be a whole number")
    if not _iso_stamp(d.get("updated")): errs.append(f"updated is not a timestamp: {d.get('updated')!r}")
    if not _filled(d.get("updatedBy")): errs.append("updatedBy must say who wrote the file")
    if list(d.get("statuses") or []) != STATUSES: errs.append(f"statuses must be {STATUSES}")
    for key in ("statusLabels", "statusColors"):
        missing = [k for k in STATUSES if k not in (d.get(key) or {})]
        if missing: errs.append(f"{key} has no entry for {', '.join(missing)}")
    for k, v in (d.get("statusColors") or {}).items():
        if not _hex(v): errs.append(f"statusColors[{k}] is not a colour: {v!r}")
    seen_s, seen_i = set(), set()
    for s in d.get("sections") or []:
        if not _filled(s.get("id")): errs.append("a section has no id")
        elif s["id"] in seen_s: errs.append(f"duplicate section id {s['id']}")
        else: seen_s.add(s["id"])
        if not _filled(s.get("name")): errs.append(f"section {s.get('id')} has no name")
        if not _hex(s.get("color")): errs.append(f"section {s.get('id')} colour is not a colour: {s.get('color')!r}")
    for s, it in items(d):
        i = it.get("id")
        if not _filled(i): errs.append(f"an item in {s.get('id')} has no id"); continue
        if i in seen_i: errs.append(f"duplicate id {i}")
        seen_i.add(i)
        if it.get("status") not in STATUSES: errs.append(f"{i}: bad status {it.get('status')!r}")
        if not _filled(it.get("title")): errs.append(f"{i}: no title")
        if not _filled(it.get("owner")): errs.append(f"{i}: no owner")
        if it.get("waitingOn") is not None and not _filled(it["waitingOn"]):
            errs.append(f"{i}: waitingOn is empty; it should be null")
        if it.get("due") is not None and not _iso_date(it["due"]):
            errs.append(f"{i}: due is not a date: {it['due']!r}")
        h = it.get("history")
        if not isinstance(h, list) or not h: errs.append(f"{i}: no history")
        else:
            for e in h:
                if not isinstance(e, dict) or not _iso_stamp(e.get("at")): errs.append(f"{i}: history entry has no timestamp")
                elif e.get("status") not in STATUSES: errs.append(f"{i}: history entry has bad status {e.get('status')!r}")
                elif not _filled(e.get("by")): errs.append(f"{i}: history entry does not say who wrote it")
    return errs
def normalise(st):
    st = ALIASES.get(st, st).replace("-", "_")
    if st not in STATUSES: raise ValueError(f"bad status {st}; one of {STATUSES}")
    return st
def set_status(d, iid, st, by="todo.py", expect=None):
    """Change one item in memory. `expect` is a compare-and-set against the current status."""
    st = normalise(st); s, it = find(d, iid)
    if expect is not None and it["status"] != normalise(expect):
        raise Conflict(f"{iid} is now {it['status']}, not {normalise(expect)} — someone else changed it")
    if it["status"] == st: return False
    it["status"] = st; it.setdefault("history", []).append({"at": now(), "status": st, "by": by}); return True
def set_field(d, iid, field, value, by="todo.py"):
    """Edit an item's wording. Stamps history so the change survives a merge."""
    if field not in ("title", "owner", "waitingOn", "due"): raise ValueError(f"cannot set {field}")
    if field == "due" and value is not None and not _iso_date(value):
        raise ValueError(f"due must be YYYY-MM-DD, not {value!r}")
    if field == "waitingOn" and value is not None and not _filled(value):
        raise ValueError("waitingOn must name someone, or be cleared with -")
    s, it = find(d, iid)
    if it.get(field) == value: return False
    it[field] = value
    it.setdefault("history", []).append({"at": now(), "status": it["status"], "by": by, "field": field})
    return True
def save(d, by, path=None):
    errs = check(d)
    if errs: raise ValueError("refused: " + "; ".join(errs))
    d["rev"] = int(d.get("rev", 0)) + 1; d["updated"] = now(); d["updatedBy"] = by
    target = path or PATH
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(target), prefix=".todo.", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f: f.write(dumps(d))
    os.replace(tmp, target)
    return d["rev"]

# ---------- merge: two writers, newest entry per item wins ----------
def _last_at(it):
    return max((e.get("at", "") for e in (it.get("history") or [])), default="")
def _union_history(a, b):
    seen, out = set(), []
    for e in (a.get("history") or []) + (b.get("history") or []):
        k = (e.get("at"), e.get("status"), e.get("by"), e.get("field"))
        if k not in seen: seen.add(k); out.append(e)
    return sorted(out, key=lambda e: e.get("at", ""))
def merge(local, remote):
    """Remote is the base — it carries any structural change. Per item the side with the
    newer history entry wins. Returns (merged, differs_from_remote)."""
    lmap = {it["id"]: it for _, it in items(local)}
    merged = json.loads(dumps(remote)); changed = False
    for _, rit in items(merged):
        lit = lmap.pop(rit["id"], None)
        if not lit: continue
        hist = _union_history(rit, lit)
        local_newer = _last_at(lit) > _last_at(rit)
        winner = lit if local_newer else rit
        if winner["status"] != rit["status"]: changed = True
        if hist != (rit.get("history") or []): changed = True
        rit["status"] = winner["status"]; rit["history"] = hist
        if local_newer:
            for k in ("notes", "waitingOn", "due", "owner", "title"):
                if k in lit and lit.get(k) != rit.get(k): rit[k] = lit[k]; changed = True
    if lmap:                                   # items this machine has that the remote lacks
        by_section = {s["id"]: s for s in merged["sections"]}
        for s, it in items(local):
            if it["id"] in lmap and s["id"] in by_section:
                by_section[s["id"]]["items"].append(it); changed = True
    # Top-level keys the merge does not model. Anything this machine added that the
    # remote has never seen is carried over rather than dropped; anything both sides
    # changed keeps the remote's value and is named in the return, never dropped in
    # silence. A palette note added here was destroyed twice before this existed.
    MANAGED = {"rev", "updated", "updatedBy", "sections"}
    overruled = []
    for k, v in local.items():
        if k in MANAGED: continue
        if k not in merged: merged[k] = v; changed = True
        elif merged[k] != v: overruled.append(k)
    if changed:
        merged["rev"] = max(int(local.get("rev", 0)), int(remote.get("rev", 0))) + 1
        merged["updated"] = now(); merged["updatedBy"] = "merge"
    return merged, changed, overruled

# ---------- git ----------
def _git(*a, check=True):
    return subprocess.run(["git", "-C", ROOT, *a], check=check, capture_output=True, text=True)
def _branch(): return _git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
def _dirty_besides_todo():
    out = _git("status", "--porcelain", "--untracked-files=no").stdout.splitlines()
    return [l[3:] for l in out if l[3:].strip() != "todo.json"]
def _remote_todo(branch):
    r = _git("show", f"origin/{branch}:todo.json", check=False)
    return json.loads(r.stdout) if r.returncode == 0 else None
def _publish_pending(branch):
    """Commits made in this clone but not yet on origin — a handoff, say — must be
    published before any reset, never destroyed by one. Returns True when nothing is
    left unpushed."""
    ahead = lambda: _git("rev-list", f"origin/{branch}..HEAD").stdout.split()
    if not ahead(): return True
    if _git("push", "-q", "origin", f"HEAD:{branch}", check=False).returncode == 0: return True
    if _dirty_besides_todo(): return False
    _git("pull", "-q", "--rebase", check=False)          # clean tree, and this clone is ours alone
    if not ahead(): return True
    return _git("push", "-q", "origin", f"HEAD:{branch}", check=False).returncode == 0

def pull():
    """Fast-forward this clone to origin, when nothing local is pending."""
    if not DEDICATED: return "not the docket clone"
    branch = _branch(); _git("fetch", "-q", "origin", branch)
    if _git("diff", "--quiet", "HEAD", "--", "todo.json", check=False).returncode != 0: return "local change pending"
    if _dirty_besides_todo(): return "clone has other edits; not resetting"
    if not _publish_pending(branch): return "unpushed commits here; not resetting"
    if _git("rev-parse", "HEAD").stdout.strip() == _git("rev-parse", f"origin/{branch}").stdout.strip(): return "current"
    _git("reset", "-q", "--hard", f"origin/{branch}"); return "updated"
def push(message=None):
    """Merge with origin and publish. Returns a one-line result."""
    branch = _branch()
    if not DEDICATED:
        if _git("diff", "--quiet", "HEAD", "--", "todo.json", check=False).returncode == 0: return "nothing to commit"
        _git("commit", "--only", "todo.json", "-q", "-m", message or f"docket: todo.json rev {load().get('rev')}")
        p = _git("push", "-q", "origin", f"HEAD:{branch}", check=False)
        return "pushed" if p.returncode == 0 else "push rejected; not the docket clone, so nothing was rewritten — run todo.py push in ~/.kom-docket"
    other = _dirty_besides_todo()
    if other: return "refused: " + ", ".join(other[:3]) + " modified in the docket clone; commit or discard them first"
    _git("fetch", "-q", "origin", branch)
    if not _publish_pending(branch):
        return "refused: this clone has unpushed commits and publishing them failed; a reset here would destroy them"
    for _ in range(4):
        _git("fetch", "-q", "origin", branch)
        local = load(); remote = _remote_todo(branch)
        if remote is None: return "origin has no todo.json"
        merged, changed, overruled = merge(local, remote)
        if not changed: 
            _git("reset", "-q", "--hard", f"origin/{branch}")   # take origin's copy; nothing of ours is pending
            return "nothing to push"
        errs = check(merged)
        if errs: return "refused: the merge produced an invalid document (" + errs[0] + "); nothing written"
        _git("reset", "-q", "--hard", f"origin/{branch}")
        with open(PATH, "w", encoding="utf-8") as f: f.write(dumps(merged))
        try: written = load()                              # read back what actually landed
        except (ValueError, OSError) as e:
            _git("checkout", "-q", "--", "todo.json"); return f"refused: todo.json did not read back ({e}); reverted"
        if dumps(written) != dumps(merged):
            _git("checkout", "-q", "--", "todo.json"); return "refused: todo.json on disk does not match what was written; reverted"
        _git("commit", "--only", "todo.json", "-q", "-m", message or f"docket: todo.json rev {merged['rev']}")
        if _git("push", "-q", "origin", f"HEAD:{branch}", check=False).returncode == 0:
            return "pushed" + (f" (origin's {', '.join(overruled)} kept over this machine's)" if overruled else "")
    return "push kept colliding; will retry on the next change"

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
        elif cmd == "title":
            if set_field(d, a[1], "title", " ".join(a[2:]), by="todo.py title"):
                print(f"{a[1]} retitled\ntodo.json rev {save(d, 'todo.py title')} written")
            else: print("unchanged")
        elif cmd == "due":
            v = None if a[2] == "-" else a[2]
            if set_field(d, a[1], "due", v, by="todo.py due"):
                print(f"{a[1]} due {v or 'cleared'}\ntodo.json rev {save(d, 'todo.py due')} written")
            else: print("unchanged")
        elif cmd == "waiting":
            v = None if a[2] == "-" else " ".join(a[2:])
            if set_field(d, a[1], "waitingOn", v, by="todo.py waiting"):
                print(f"{a[1]} waiting on {v or 'nobody'}\ntodo.json rev {save(d, 'todo.py waiting')} written")
            else: print("unchanged")
        elif cmd == "note":
            s, it = find(d, a[1]); it.setdefault("notes", []).append({"at": now(), "text": " ".join(a[2:])})
            print(f"todo.json rev {save(d, 'todo.py note')} written")
        elif cmd == "push": print(push())
        elif cmd == "pull": print(pull())
        else: sys.exit(f"unknown command {cmd}")
    except (KeyError, ValueError, Conflict) as e: sys.exit(str(e))
if __name__ == "__main__": main(sys.argv[1:])
