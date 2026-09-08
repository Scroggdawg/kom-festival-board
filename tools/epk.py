#!/usr/bin/env python3
"""The EPK worksheet's only writer. press/epk.json is the truth; never hand-edit it.

  epk.py list [--all]               every field: number, label, and what is in it
  epk.py get <ref>                  print one field's value in full
  epk.py set <ref> "<text>"         set a field ("-" reads the value from stdin)
  epk.py clear <ref>
  epk.py check                      validate the file
  epk.py push                       merge with origin and publish
  epk.py pull                       take origin's copy when nothing local is pending

`ref` is a field's number (3.9) or its id (p3-aspect-ratio). Both are matched in
full — never by prefix. A prefix match on an id once wrote one festival's data onto
another in data.json, and the ids here ("p3-website", "p3-website-url") are just as
easy to confuse.

epk_server.py imports from here, so the browser and the command line share one writer.

Two machines write this file: this one, and whoever opens epk.html with a token. So
push() never overwrites the remote wholesale — it merges field by field, the newer
history entry wins, and both histories are kept.

Numbers are permanent. A field's number is how Luke refers to it when he sends
material, so save() refuses any change that moves an existing id to a different
number or a different section. New fields are appended to the end of their section.

push() rebases by resetting to origin, which throws away uncommitted work. It
therefore runs only in a checkout marked `.epk-clone` — a clone kept for the EPK
alone — and only when epk.json is the sole modified file. Anywhere else it commits
epk.json alone and, if the push is rejected, stops and says so rather than
rewriting anything.
"""
import json, os, re, sys, datetime, subprocess, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = "press/epk.json"
PATH = os.path.join(ROOT, "press", "epk.json")
DEDICATED = os.path.exists(os.path.join(ROOT, ".epk-clone"))
NUMBERINGS = ("decimal", "roman")
HISTORY_KEEP = 6            # prior values kept per field, so nothing typed is lost in a merge


class Conflict(Exception):
    pass


def load(path=None):
    with open(path or PATH, encoding="utf-8") as f:
        return json.load(f)


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def dumps(d):
    return json.dumps(d, ensure_ascii=False, indent=1)


def fields(d):
    for s in d["sections"]:
        for f in s["fields"]:
            yield s, f


def find(d, ref):
    """Full match on the number or the id. Never a prefix, never a substring."""
    ref = str(ref).strip()
    for s, f in fields(d):
        if f["id"] == ref or f["n"] == ref:
            return s, f
    raise KeyError(f"no field {ref!r}; give a number like 3.9 or an id like p3-aspect-ratio")


def _iso_stamp(v):
    try:
        datetime.datetime.fromisoformat(v)
        return True
    except (ValueError, TypeError):
        return False


def _filled(v):
    return isinstance(v, str) and v.strip() != ""


def current(f):
    """The value the history says this field holds. `value` is a cache of this."""
    h = f.get("history") or []
    return h[-1].get("value", "") if h else ""


def check(d):
    """Every rule here was true of the file when it was written, stated so the file
    cannot drift out of them. The one that matters most: a value and its history
    cannot disagree, because the history is what a merge reads."""
    errs = []
    if d.get("schema") != 2:
        errs.append("schema must be 2")
    if not isinstance(d.get("rev"), int):
        errs.append("rev must be a whole number")
    if not _iso_stamp(d.get("updated")):
        errs.append(f"updated is not a timestamp: {d.get('updated')!r}")
    if not _filled(d.get("updatedBy")):
        errs.append("updatedBy must say who wrote the file")
    if d.get("numbering") not in NUMBERINGS:
        errs.append(f"numbering must be one of {NUMBERINGS}")
    seen_s, seen_num, seen_id, seen_n = set(), set(), set(), set()
    for s in d.get("sections") or []:
        sid, num = s.get("id"), s.get("num")
        if not _filled(sid):
            errs.append("a section has no id")
        elif sid in seen_s:
            errs.append(f"duplicate section id {sid}")
        else:
            seen_s.add(sid)
        if not _filled(num):
            errs.append(f"section {sid} has no number")
        elif num in seen_num:
            errs.append(f"duplicate section number {num}")
        else:
            seen_num.add(num)
        if not _filled(s.get("name")):
            errs.append(f"section {sid} has no name")
        if not isinstance(s.get("fields"), list) or not s["fields"]:
            errs.append(f"section {sid} has no fields")
            continue
        seq = []
        for f in s["fields"]:
            fid, n = f.get("id"), f.get("n")
            if not _filled(fid):
                errs.append(f"a field in {sid} has no id")
                continue
            if fid in seen_id:
                errs.append(f"duplicate field id {fid}")
            seen_id.add(fid)
            if not _filled(n):
                errs.append(f"{fid}: no number")
                continue
            if n in seen_n:
                errs.append(f"duplicate field number {n}")
            seen_n.add(n)
            if not re.fullmatch(re.escape(str(num)) + r"\.\d+", str(n)):
                errs.append(f"{fid}: number {n} does not belong to section {num}")
                continue
            seq.append(int(str(n).rsplit(".", 1)[1]))
            if not _filled(f.get("label")):
                errs.append(f"{n}: no label")
            v = f.get("value")
            if not isinstance(v, str):
                errs.append(f"{n}: value must be text, not {type(v).__name__}")
            h = f.get("history")
            if not isinstance(h, list):
                errs.append(f"{n}: history must be a list")
                continue
            for e in h:
                if not isinstance(e, dict) or not _iso_stamp(e.get("at")):
                    errs.append(f"{n}: a history entry has no timestamp")
                elif not _filled(e.get("by")):
                    errs.append(f"{n}: a history entry does not say who wrote it")
                elif not isinstance(e.get("value"), str):
                    errs.append(f"{n}: a history entry has no value")
            if isinstance(v, str) and current(f) != v:
                errs.append(f"{n}: value and history disagree; the merge would read the history")
        if seq != sorted(seq):
            errs.append(f"section {num}: numbers are out of order — new fields go at the end")
    return errs


def check_stable(new, base):
    """Numbers are how Luke refers to fields. An id that already exists must keep the
    number and the section it was given. Returns a list of violations. A baseline from
    before schema 2 carries no numbers, so there is nothing it can pin."""
    if not isinstance(base, dict) or base.get("schema") != 2:
        return []
    was = {f["id"]: (s["id"], f["n"]) for s, f in fields(base)}
    errs = []
    for s, f in fields(new):
        old = was.get(f["id"])
        if old and old != (s["id"], f["n"]):
            errs.append(f"{f['id']} was {old[1]} in {old[0]} and is now {f['n']} in {s['id']}; numbers are permanent")
    return errs


def committed(rel=REL, rev="HEAD"):
    """The copy of the file in git, or None. Used as the baseline for check_stable."""
    r = _git("show", f"{rev}:{rel}", check=False)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except ValueError:
        return None


def set_value(d, ref, value, by="epk.py", expect=None):
    """Set one field in memory. Every change stamps history — that is the only record
    a merge can read, so a change that skipped it would be silently discarded."""
    if not isinstance(value, str):
        raise ValueError("a value must be text")
    s, f = find(d, ref)
    if expect is not None and f["value"] != expect:
        raise Conflict(f"{f['n']} has changed since you read it — nothing written")
    if f["value"] == value:
        return False
    f["value"] = value
    h = f.setdefault("history", [])
    h.append({"at": now(), "by": by, "value": value})
    del h[:-HISTORY_KEEP]
    return True


def save(d, by, path=None):
    errs = check(d)
    if errs:
        raise ValueError("refused: " + "; ".join(errs))
    base = committed()
    if base:
        errs = check_stable(d, base)
        if errs:
            raise ValueError("refused: " + "; ".join(errs))
    d["rev"] = int(d.get("rev", 0)) + 1
    d["updated"] = now()
    d["updatedBy"] = by
    target = path or PATH
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(target), prefix=".epk.", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(dumps(d))
    os.replace(tmp, target)
    written = load(target)                       # read back what actually landed
    if dumps(written) != dumps(d):
        raise ValueError("refused: epk.json on disk does not match what was written")
    return d["rev"]


# ---------- merge: two writers, newest entry per field wins ----------
def _last_at(f):
    return max((e.get("at", "") for e in (f.get("history") or [])), default="")


def _union_history(a, b):
    seen, out = set(), []
    for e in (a.get("history") or []) + (b.get("history") or []):
        k = (e.get("at"), e.get("by"), e.get("value"))
        if k not in seen:
            seen.add(k)
            out.append(e)
    out.sort(key=lambda e: e.get("at", ""))
    return out[-HISTORY_KEEP:]


def merge(local, remote):
    """Remote is the base — it carries any structural change. Per field the side with
    the newer history entry wins, and both histories are kept, so a value typed on one
    machine is still recoverable after the other machine wins. Returns
    (merged, differs_from_remote)."""
    lmap = {f["id"]: f for _, f in fields(local)}
    merged = json.loads(dumps(remote))
    changed = False
    for _, rf in fields(merged):
        lf = lmap.pop(rf["id"], None)          # full id match, never a prefix
        if not lf:
            continue
        hist = _union_history(rf, lf)
        winner = lf if _last_at(lf) > _last_at(rf) else rf
        if winner["value"] != rf["value"] or hist != (rf.get("history") or []):
            changed = True
        rf["history"] = hist
        rf["value"] = hist[-1]["value"] if hist else winner["value"]
    if lmap:                                   # fields this machine has that the remote lacks
        by_section = {s["id"]: s for s in merged["sections"]}
        for s, f in fields(local):
            if f["id"] in lmap and s["id"] in by_section:
                by_section[s["id"]]["fields"].append(f)
                changed = True
    if changed:
        merged["rev"] = max(int(local.get("rev", 0)), int(remote.get("rev", 0))) + 1
        merged["updated"] = now()
        merged["updatedBy"] = "merge"
    return merged, changed


# ---------- git ----------
def _git(*a, check=True):
    return subprocess.run(["git", "-C", ROOT, *a], check=check, capture_output=True, text=True)


def _branch():
    return _git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()


def _fetch(branch):
    """False when origin cannot be reached. Every caller must stop rather than reset:
    a reset against a stale origin is how unpushed work disappears."""
    return _git("fetch", "-q", "origin", branch, check=False).returncode == 0


def _dirty_besides_epk():
    out = _git("status", "--porcelain", "--untracked-files=no").stdout.splitlines()
    return [l[3:] for l in out if l[3:].strip() != REL]


def _remote_epk(branch):
    r = _git("show", f"origin/{branch}:{REL}", check=False)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except ValueError:
        return None


def _publish_pending(branch):
    """Commits made in this clone but not yet on origin — a handoff, say — must be
    published before any reset, never destroyed by one. Without this check a
    `reset --hard` in the background loop silently deletes work; it has happened."""
    def ahead():
        return _git("rev-list", f"origin/{branch}..HEAD").stdout.split()
    if not ahead():
        return True
    if _git("push", "-q", "origin", f"HEAD:{branch}", check=False).returncode == 0:
        return True
    if _dirty_besides_epk():
        return False
    _git("pull", "-q", "--rebase", check=False)      # clean tree, and this clone is ours alone
    if not ahead():
        return True
    return _git("push", "-q", "origin", f"HEAD:{branch}", check=False).returncode == 0


def pull():
    """Fast-forward this clone to origin, when nothing local is pending."""
    if not DEDICATED:
        return "not the epk clone"
    branch = _branch()
    if not _fetch(branch):
        return "cannot reach origin; not resetting"
    if _git("diff", "--quiet", "HEAD", "--", REL, check=False).returncode != 0:
        return "local change pending"
    if _dirty_besides_epk():
        return "clone has other edits; not resetting"
    if not _publish_pending(branch):
        return "unpushed commits here; not resetting"
    if _git("rev-parse", "HEAD").stdout.strip() == _git("rev-parse", f"origin/{branch}").stdout.strip():
        return "current"
    _git("reset", "-q", "--hard", f"origin/{branch}")
    return "updated"


def push(message=None):
    """Merge with origin and publish. Returns a one-line result."""
    branch = _branch()
    if not DEDICATED:
        if _git("diff", "--quiet", "HEAD", "--", REL, check=False).returncode == 0:
            return "nothing to commit"
        _git("commit", "--only", REL, "-q", "-m", message or f"epk: rev {load().get('rev')}")
        p = _git("push", "-q", "origin", f"HEAD:{branch}", check=False)
        return "pushed" if p.returncode == 0 else "push rejected; not the epk clone, so nothing was rewritten — run epk.py push in ~/.kom-epk"
    other = _dirty_besides_epk()
    if other:
        return "refused: " + ", ".join(other[:3]) + " modified in the epk clone; commit or discard them first"
    if not _fetch(branch):
        return "refused: cannot reach origin; nothing written"
    if not _publish_pending(branch):
        return "refused: this clone has unpushed commits and publishing them failed; a reset here would destroy them"
    for _ in range(4):
        if not _fetch(branch):
            return "refused: cannot reach origin; nothing written"
        local, remote = load(), _remote_epk(branch)
        if remote is None:
            return f"origin has no {REL}"
        merged, changed = merge(local, remote)
        if not changed:
            _git("reset", "-q", "--hard", f"origin/{branch}")   # nothing of ours is pending
            return "nothing to push"
        errs = check(merged) + check_stable(merged, remote)
        if errs:
            return "refused: the merge produced an invalid document (" + errs[0] + "); nothing written"
        _git("reset", "-q", "--hard", f"origin/{branch}")
        with open(PATH, "w", encoding="utf-8") as f:
            f.write(dumps(merged))
        try:
            written = load()                                    # read back what actually landed
        except (ValueError, OSError) as e:
            _git("checkout", "-q", "--", REL)
            return f"refused: epk.json did not read back ({e}); reverted"
        if dumps(written) != dumps(merged) or check(written):
            _git("checkout", "-q", "--", REL)
            return "refused: epk.json on disk does not match what was written; reverted"
        _git("commit", "--only", REL, "-q", "-m", message or f"epk: rev {merged['rev']}")
        if _git("push", "-q", "origin", f"HEAD:{branch}", check=False).returncode == 0:
            return "pushed"
    return "push kept colliding; will retry on the next change"


# ---------- command line ----------
ROMAN = {"1": "I", "2": "II", "3": "III", "4": "IV", "5": "V", "6": "VI", "7": "VII",
         "8": "VIII", "9": "IX", "10": "X", "11": "XI"}


def label_of(n, numbering="decimal"):
    head, tail = str(n).rsplit(".", 1)
    return (ROMAN.get(head, head) if numbering == "roman" else head) + "." + tail


def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = a[0]
    d = load()
    try:
        if cmd == "list":
            show_all = "--all" in a
            for s in d["sections"]:
                got = sum(bool(f["value"].strip()) for f in s["fields"])
                print(f"\n{s['num']}  {s['name']}  {got}/{len(s['fields'])}")
                for f in s["fields"]:
                    v = " ".join(f["value"].split())
                    if not show_all and len(v) > 60:
                        v = v[:59] + "…"
                    print(f"  {label_of(f['n'], d['numbering']):>6}  {f['label'][:34]:34} {v}")
            n = sum(1 for _, f in fields(d) if f["value"].strip())
            print(f"\n{n} of {sum(1 for _ in fields(d))} filled · rev {d['rev']}")
        elif cmd == "get":
            print(find(d, a[1])[1]["value"])
        elif cmd == "check":
            errs = check(d)
            base = committed()
            if base:
                errs += check_stable(d, base)
            print("clean" if not errs else "\n".join(errs))
            sys.exit(1 if errs else 0)
        elif cmd == "set":
            value = sys.stdin.read() if a[2:3] == ["-"] else " ".join(a[2:])
            if set_value(d, a[1], value.strip("\n"), by="epk.py"):
                s, f = find(d, a[1])
                print(f"{f['n']} {f['label']} ← {len(f['value'])} characters\nepk.json rev {save(d, 'epk.py set')} written")
            else:
                print("unchanged")
        elif cmd == "clear":
            if set_value(d, a[1], "", by="epk.py"):
                print(f"{find(d, a[1])[1]['n']} cleared\nepk.json rev {save(d, 'epk.py clear')} written")
            else:
                print("already empty")
        elif cmd == "push":
            print(push())
        elif cmd == "pull":
            print(pull())
        else:
            sys.exit(f"unknown command {cmd}")
    except (KeyError, ValueError, IndexError, Conflict) as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main(sys.argv[1:])
