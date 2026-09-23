#!/usr/bin/env python3
"""kom-status.py — where every checkout of kom-festival-board stands, measured now.
KOM build 1 (2026-09-23), from petrol-brand-bible's bin/petrol-status.py (PLAN_SETUP_v1
C7) with the lane rule, the ledger directory and the shelf line changed for this project.

A LIVE rescan of every checkout in `git worktree list`, run NOW: `git status --porcelain`
(dirty), one `git fetch --prune origin` per repository then `git rev-list --count
@{u}..HEAD` (ahead), `git log -1 --format=%ct @{u}` for an upstream on origin (the newest
commit GitHub holds, labelled `commit time`: %ct is the committer timestamp — git records no
publication time), and the newest mtime under the checkout outside .git ("last file
change"). The Stop-hook snapshot under $HOME/.kom/status/<session_id>.json (kom-stop.sh,
kom-prompt.sh) is a hint that can only demote a checkout to `working`, never upgrade one.

States, tested in this order per checkout:
  unknown          checkout unreadable; no upstream, or an upstream whose remote-tracking
                   ref is gone (`upstream gone`: deleted on GitHub, pruned by the fetch); the
                   fetch was attempted and failed (`fetch failed`, every checkout); or a
                   checkout that would be `saved to GitHub` lacks a piece of that state's
                   evidence (the missing piece is the reason). No upstream still reports the
                   measured facts as a suffix: uncommitted files, and commits on no remote ref
  working          the newest snapshot for the checkout says working, or an untracked-or-
                   ignored file under the checkout is newer than that snapshot
  unsaved changes  git status --porcelain is not empty
  not on GitHub    the upstream is not a branch of origin (`upstream is local` for a local
                   branch, `upstream is on <remote>, not origin` for another remote), or
                   ahead > 0
  saved to GitHub  dirty 0 and ahead 0, and all of this evidence from this run: the
                   upstream is refs/remotes/origin/<x> of a branch whose remote is origin;
                   origin's URL is github.com/Scroggdawg/kom-festival-board;
                   `git fetch --prune origin` succeeded in this run; origin/<x> contains
                   HEAD (git merge-base --is-ancestor).
A snapshot older than the newest tracked-file change is shown as a suffix
`(snapshot HH:MM, files changed HH:MM)`. Remote branches with no local checkout are
listed from `git for-each-ref` with their commit time and newest handoff number.

The lane (KOM): git config kom.lane (worktree scope, then any), else main, else on a
claude/* branch the suffix of the checkout's newest handoffs/handoff-NNN-<lane>.md, marked
"guessed", else the branch's last path component. A checkout with no upstream stays
`unknown`; its suffix names the origin ref that already holds HEAD and the command that
sets the upstream, else `git push -u origin HEAD`.

Every value that can hold a URL (origin's URL, a branch's remote, git fetch's error text)
is printed and written to --json through redact_url, which prints credentials as ***.

Usage:
  kom-status.py [--plain | --json] [--no-fetch] [--fetch-timeout SECONDS]
                [--repo PATH] [--status-dir PATH]
Writes nothing itself: no file in any working tree, no snapshot (the hooks write those).
Every git call runs with GIT_OPTIONAL_LOCKS=0, so `git status` never refreshes or locks an
index; the shelf tool runs with PYTHONDONTWRITEBYTECODE=1. The one write is git's own:
`git fetch --prune --quiet --no-auto-gc --no-write-fetch-head origin` (skipped by
--no-fetch) updates origin's remote-tracking refs in the repository's shared .git.
Exit 0 when the scan ran, 2 on a usage or repository error.
"""

import argparse
import calendar
import datetime
import json
import os
import re
import subprocess
import sys
import time

os.environ["GIT_OPTIONAL_LOCKS"] = "0"          # git status must not rewrite any index
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"    # the shelf tool must not leave __pycache__

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
LEDGER = "handoffs"
HANDOFF_RE = re.compile(r"^handoff-(\d+)")
HANDOFF_LANE_RE = re.compile(r"^handoff-(\d+)-([A-Za-z0-9_-]+)\.md$")
STATES = ("unknown", "working", "unsaved changes", "not on GitHub", "saved to GitHub")
ORIGIN_PREFIX = "refs/remotes/origin/"
# "saved to GitHub" needs origin to be this GitHub repository itself: https, ssh or scp form,
# any user part; GitHub owner and repository names are case-insensitive
GITHUB_ORIGIN_RE = re.compile(
    r"^(?:https?://(?:[^@/]+@)?github\.com/|ssh://(?:[^@/]+@)?github\.com(?::\d+)?/"
    r"|(?:[^@/:]+@)?github\.com:)Scroggdawg/kom-festival-board(?:\.git)?/?$", re.IGNORECASE)
# --prune: a branch deleted on GitHub loses its remote-tracking ref in this run, so no
# stale ref can stand as evidence; origin named, never the current branch's remote
FETCH_CMD = ["fetch", "--prune", "--quiet", "--no-auto-gc", "--no-write-fetch-head", "origin"]


# ----------------------------------------------------------------- helpers
def display(path):
    """$HOME form for printing (the repo forbids home-folder literals in files)."""
    if path and (path == HOME or path.startswith(HOME + os.sep)):
        return "$HOME" + path[len(HOME):]
    return path


def git(args, cwd, timeout=30):
    """Returns (stdout, error). stdout is None and error non-empty on any failure."""
    try:
        p = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True,
                           text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, "%s: %s" % (type(e).__name__, e)
    if p.returncode != 0:
        return None, (p.stderr.strip() or "exit %d" % p.returncode)
    return p.stdout, ""


def git_int(args, cwd):
    out, err = git(args, cwd)
    if out is None:
        return None, err
    try:
        return int(out.strip()), ""
    except ValueError:
        return None, "not a number: %r" % out.strip()


def git_rc(args, cwd, timeout=30):
    """Returns (exit code, stderr); the code is None when git could not be run at all."""
    try:
        p = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True,
                           text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, "%s: %s" % (type(e).__name__, e)
    return p.returncode, p.stderr.strip()


# One rule for every URL this tool prints or emits as JSON. bin/hooks/kom-stop.sh,
# kom-session-start.sh and bin/kom-check.sh carry the whole rule (test-kom-stop.sh feeds one
# set of URLs to all four):
#  (a) scheme://authority: the authority ends at the first / ? # or blank, and all of it before
#      its LAST @ prints as *** (https://us@er:tok@en@host/... -> https://***@host/...);
#  (b) the scp form of ssh, [user@]host:path (a word with no ://): a user part holding a colon
#      (user:token@host:path) prints as ***; a bare user (git@host:path) stays. The user part is
#      the word before its last @ ahead of the word's first /.
# No credentials, no change; idempotent.
URL_AUTHORITY_CREDENTIALS = re.compile(r"://[^/?#\s]*@")


def _redact_scp(m):
    w = m.group(0)
    if "://" in w:
        return w
    user, at, host = w.split("/", 1)[0].rpartition("@")
    if at and ":" in user and ":" in host:
        return "***@" + w[len(user) + 1:]
    return w


def redact_url(s):
    """s with every URL's credentials as *** (the rule above); None and "" pass through."""
    if not s:
        return s
    return re.sub(r"\S+", _redact_scp, URL_AUTHORITY_CREDENTIALS.sub("://***@", s))


def hhmm(epoch):
    if epoch is None:
        return "?"
    return time.strftime("%H:%M", time.localtime(epoch))


def when(epoch):
    """HH:MM today, else YYYY-MM-DD HH:MM."""
    if epoch is None:
        return "?"
    if time.strftime("%Y-%m-%d", time.localtime(epoch)) == time.strftime("%Y-%m-%d"):
        return hhmm(epoch)
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(epoch))


def rel_time(epoch, now=None):
    if epoch is None:
        return "?"
    now = time.time() if now is None else now
    d = int(now - epoch)
    if d < 0:
        d = 0
    if d < 60:
        return "%d s ago" % d
    if d < 3600:
        return "%d min ago" % (d // 60)
    if d < 86400:
        return "%d h ago" % (d // 3600)
    return "%d d ago" % (d // 86400)


def iso_utc(epoch):
    return datetime.datetime.fromtimestamp(epoch, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_ts(s):
    try:
        return calendar.timegm(time.strptime(s, "%Y-%m-%dT%H:%M:%SZ"))
    except (TypeError, ValueError):
        return None


def newest_handoff_in(names):
    best = 0
    for n in names:
        m = HANDOFF_RE.match(n)
        if m:
            best = max(best, int(m.group(1)))
    return best


def newest_handoff_file(root):
    """(number, file name) of the newest handoffs/handoff-NNN-*.md in a checkout."""
    try:
        names = os.listdir(os.path.join(root, LEDGER))
    except OSError:
        return 0, None
    best, best_name = 0, None
    for n in names:
        m = HANDOFF_RE.match(n)
        if m and int(m.group(1)) >= best:
            best, best_name = int(m.group(1)), n
    return best, best_name


# ----------------------------------------------------------------- worktrees
def list_worktrees(repo):
    out, err = git(["worktree", "list", "--porcelain"], repo)
    if out is None:
        return None, err
    entries, cur = [], {}
    for line in out.splitlines():
        if not line.strip():
            if cur:
                entries.append(cur)
                cur = {}
            continue
        key, _, val = line.partition(" ")
        if key == "worktree":
            cur = {"path": val}
        elif key == "HEAD":
            cur["head"] = val
        elif key == "branch":
            cur["branch"] = val[len("refs/heads/"):] if val.startswith("refs/heads/") else val
        elif key == "detached":
            cur["detached"] = True
        elif key == "bare":
            cur["bare"] = True
        elif key == "prunable":
            cur["prunable"] = val or True
    if cur:
        entries.append(cur)
    return entries, ""


def lane_name(root, branch):
    """(lane, source): kom.lane (worktree, then any scope), else main, else, for a claude/*
    branch, the suffix of the checkout's newest handoff (guessed), else the branch."""
    out, _ = git(["config", "--worktree", "kom.lane"], root)
    if out and out.strip():
        return out.strip(), "kom.lane"
    out, _ = git(["config", "kom.lane"], root)
    if out and out.strip():
        return out.strip(), "kom.lane"
    if branch == "main":
        return "main", "branch"
    if branch and branch.startswith("claude/"):
        _n, name = newest_handoff_file(root)
        m = HANDOFF_LANE_RE.match(name or "")
        if m:
            return m.group(2), "guessed from %s/%s" % (LEDGER, name)
        return "<lane>", "unset"
    if branch and "/" in branch:
        return branch.rsplit("/", 1)[1], "branch"
    return branch or os.path.basename(root), "branch"


def publish_hint(rec, root, branch):
    """Suffix for a checkout with no upstream on origin: the origin ref that already holds
    HEAD and the command that sets it as the upstream, else the command that publishes."""
    holders = refs_holding_head(root)
    rec["head_on_remote_refs"] = holders
    if not branch or branch in ("main", "?", "(detached)"):
        return
    pick = None
    if "origin/" + branch in holders:
        pick = "origin/" + branch
    elif len(holders) == 1:
        pick = holders[0]
    if pick is None:
        probe, _ = git(["rev-parse", "--verify", "--quiet", "refs/remotes/origin/" + branch], root)
        if probe is not None:
            pick = "origin/" + branch
    if pick is not None:
        if pick in holders:
            rec["suffix"].append("HEAD is on %s" % pick)
        rec["suffix"].append("set it: git branch --set-upstream-to=%s" % pick)
    else:
        rec["suffix"].append("publish first: git push -u origin HEAD")


def saved_blocker(rec, fetch_state):
    """Why a clean checkout level with its upstream is NOT saved to GitHub (None: it is)."""
    if fetch_state == "skipped":
        return "not fetched this run (--no-fetch)"
    if fetch_state != "ok":
        return "fetch " + str(fetch_state)
    if rec["upstream_kind"] != "origin":
        return "upstream is not a branch of origin"
    if not rec["origin_is_github"]:
        return "origin is not the GitHub repo: %s" % (rec["origin_url"] or "no URL")
    if rec["origin_contains_head"] is not True:
        if rec["origin_contains_head"] is False:
            return "%s does not contain HEAD" % rec["upstream"]
        return "could not check that %s contains HEAD" % rec["upstream"]
    return None


def refs_holding_head(root):
    """Remote-tracking refs on origin whose history contains HEAD (short names)."""
    out, _ = git(["for-each-ref", "--contains", "HEAD", "--format=%(refname:short)",
                  "refs/remotes/origin"], root)
    return [l.strip() for l in (out or "").splitlines()
            if l.strip() and l.strip() not in ("origin/HEAD", "origin")]


# ----------------------------------------------------------------- snapshots
def load_snapshots(status_dir):
    snaps = []
    try:
        names = os.listdir(status_dir)
    except OSError:
        return snaps
    for n in names:
        if not n.endswith(".json"):
            continue
        p = os.path.join(status_dir, n)
        try:
            with open(p, encoding="utf-8") as fh:
                d = json.load(fh)
        except (OSError, ValueError):
            continue
        if not isinstance(d, dict):
            continue
        d["_file"] = n
        d["_ts"] = parse_ts(d.get("ts"))
        snaps.append(d)
    return snaps


def snapshot_for(root_real, snaps, real_roots):
    """The newest snapshot whose root/cwd lies in this checkout (and not in a nested one)."""
    best = None
    for s in snaps:
        p = s.get("root") or s.get("cwd")
        if not p:
            continue
        try:
            rp = os.path.realpath(p)
        except OSError:
            continue
        owner = None
        for r in real_roots:
            if rp == r or rp.startswith(r + os.sep):
                if owner is None or len(r) > len(owner):
                    owner = r
        if owner != root_real:
            continue
        if best is None or (s["_ts"] or 0) > (best["_ts"] or 0):
            best = s
    return best


# ----------------------------------------------------------------- one checkout
def newest_mtimes(root, rel_paths, nested_roots):
    """(newest mtime, path) over the given root-relative paths, pruning nested checkouts."""
    newest, newest_path = None, None
    for rel in rel_paths:
        if not rel:
            continue
        ap = os.path.join(root, rel)
        skip = False
        for nr in nested_roots:
            if ap == nr or ap.startswith(nr + os.sep):
                skip = True
                break
        if skip:
            continue
        try:
            st = os.lstat(ap)
        except OSError:
            continue
        if newest is None or st.st_mtime > newest:
            newest, newest_path = st.st_mtime, rel
    return newest, newest_path


def scan_checkout(wt, all_roots, snaps, fetch_state, now):
    root = wt["path"]
    branch = wt.get("branch") or ("(detached)" if wt.get("detached") else "?")
    rec = {
        "path": root, "path_display": display(root), "branch": branch,
        "lane": None, "lane_source": None, "state": None, "unknown_reason": None,
        "dirty": None, "ahead": None, "behind": None, "upstream": None,
        "upstream_ref": None, "upstream_kind": None, "origin_url": None,
        "origin_is_github": None, "origin_contains_head": None, "state_reason": None,
        "ahead_any_remote": None, "head_on_remote_refs": None,
        "commit_time": None, "commit_time_iso": None, "head_time": None,
        "last_file_change": None, "last_file_change_path": None,
        "newest_tracked_mtime": None, "newest_other_mtime": None, "newest_other_path": None,
        "last_handoff": None, "last_handoff_file": None,
        "snapshot": None, "suffix": [],
    }
    root_real = os.path.realpath(root)
    real_roots = [os.path.realpath(r) for r in all_roots]
    nested = [r for r in real_roots if r != root_real and r.startswith(root_real + os.sep)]

    if not os.path.isdir(root):
        rec["unknown_reason"] = "checkout missing"
    else:
        rec["lane"], rec["lane_source"] = lane_name(root, branch)
        if rec["lane_source"].startswith("guessed"):
            rec["suffix"].append("lane %s: kom.lane unset (git config --worktree kom.lane <lane>)" % rec["lane_source"])
        elif rec["lane_source"] == "unset":
            rec["suffix"].append("lane unset: git config --worktree kom.lane <lane>")
        out, err = git(["status", "--porcelain"], root)
        if out is None:
            rec["unknown_reason"] = "git status failed: " + err
        else:
            rec["dirty"] = len([l for l in out.splitlines() if l])
    if rec["unknown_reason"] is None:
        out, err = git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], root)
        if out is None:
            merge, _ = git(["config", "branch.%s.merge" % branch], root)
            merge = (merge or "").strip()
            if merge:
                # configured, but its remote-tracking ref is gone: the branch was deleted on
                # GitHub and the fetch pruned it (or it was never fetched). The remote may be
                # a URL (git push -u <url> writes one), so it prints redacted
                remote, _ = git(["config", "branch.%s.remote" % branch], root)
                remote = (remote or "").strip()
                name = merge[len("refs/heads/"):] if merge.startswith("refs/heads/") else merge
                rec["unknown_reason"] = ("upstream gone: no local branch %s" % name if remote == "."
                                         else "upstream gone: %s has no %s" % (redact_url(remote) or "?", name))
            else:
                rec["unknown_reason"] = "no upstream"
            # the facts the live scan can still measure without an upstream
            rec["ahead_any_remote"], _ = git_int(["rev-list", "--count", "HEAD", "--not", "--remotes"], root)
            if rec["dirty"]:
                rec["suffix"].append("%d uncommitted file(s)" % rec["dirty"])
            if rec["ahead_any_remote"]:
                rec["suffix"].append("%d commit(s) on no remote ref" % rec["ahead_any_remote"])
            publish_hint(rec, root, branch)
        else:
            rec["upstream"] = out.strip()
            full, _ = git(["rev-parse", "--symbolic-full-name", "@{u}"], root)
            full = (full or "").strip()
            remote, _ = git(["config", "branch.%s.remote" % branch], root)
            remote = (remote or "").strip()
            rec["upstream_ref"] = full
            if remote == "origin" and full.startswith(ORIGIN_PREFIX) and len(full) > len(ORIGIN_PREFIX):
                rec["upstream_kind"] = "origin"
            elif full.startswith("refs/heads/"):
                rec["upstream_kind"] = "local"
            else:
                rec["upstream_kind"] = "remote " + (redact_url(remote) or "?")   # a remote may be a URL
            rec["ahead"], _ = git_int(["rev-list", "--count", "@{u}..HEAD"], root)
            rec["behind"], _ = git_int(["rev-list", "--count", "HEAD..@{u}"], root)
            if rec["ahead"] is None:
                rec["unknown_reason"] = "rev-list failed"
            if rec["upstream_kind"] == "origin":
                # the evidence "saved to GitHub" needs, besides dirty 0 and ahead 0
                rec["commit_time"], _ = git_int(["log", "-1", "--format=%ct", "@{u}"], root)
                if rec["commit_time"] is not None:
                    rec["commit_time_iso"] = iso_utc(rec["commit_time"])
                url, _ = git(["remote", "get-url", "origin"], root)
                url = (url or "").strip()
                rec["origin_url"] = redact_url(url)
                rec["origin_is_github"] = bool(GITHUB_ORIGIN_RE.match(url))
                rc, _ = git_rc(["merge-base", "--is-ancestor", "HEAD", full], root)
                rec["origin_contains_head"] = {0: True, 1: False}.get(rc)
            else:
                # a local branch or another remote holds nothing on GitHub: no commit time
                publish_hint(rec, root, branch)
        if fetch_state == "failed":
            rec["unknown_reason"] = "fetch failed"
    if os.path.isdir(root):
        rec["head_time"], _ = git_int(["log", "-1", "--format=%ct", "HEAD"], root)
        out, _ = git(["ls-files", "-z"], root)
        tracked = out.split("\0") if out is not None else []
        rec["newest_tracked_mtime"], _tp = newest_mtimes(root, tracked, nested)
        out, _ = git(["ls-files", "--others", "-z"], root)
        others = out.split("\0") if out is not None else []
        rec["newest_other_mtime"], rec["newest_other_path"] = newest_mtimes(root, others, nested)
        cands = [(rec["newest_tracked_mtime"], _tp), (rec["newest_other_mtime"], rec["newest_other_path"])]
        cands = [c for c in cands if c[0] is not None]
        if cands:
            m, p = max(cands)
            rec["last_file_change"], rec["last_file_change_path"] = m, p
        rec["last_handoff"], rec["last_handoff_file"] = newest_handoff_file(root)

    snap = snapshot_for(root_real, snaps, real_roots)
    snap_ts = snap["_ts"] if snap else None
    if snap:
        rec["snapshot"] = {
            "file": snap["_file"], "state": snap.get("state"), "ts": snap.get("ts"),
            "session_id": snap.get("session_id"), "dirty": snap.get("dirty"),
            "ahead": snap.get("ahead"), "emitted": snap.get("emitted"),
        }

    # the state machine, in the ratified order
    kind = rec["upstream_kind"]
    note = None                           # an upstream that is not a branch of origin
    if kind == "local":
        note = "upstream is local"
    elif kind and kind != "origin":
        note = "upstream is on %s, not origin" % kind[len("remote "):]
    reason = None
    if rec["unknown_reason"]:
        state = "unknown"
    elif snap and snap.get("state") == "working":
        state = "working"
    elif (snap and snap_ts is not None and rec["newest_other_mtime"] is not None
          and int(rec["newest_other_mtime"]) > snap_ts):
        # whole seconds: the snapshot ts has 1 s resolution, so a file written in the
        # same second as the Stop is not "newer"
        state = "working"
    elif rec["dirty"]:
        state = "unsaved changes"
    elif note:
        state, reason = "not on GitHub", note
    elif rec["ahead"]:
        state = "not on GitHub"
    else:
        # saved to GitHub only on evidence measured in this run; any piece missing: unknown
        rec["unknown_reason"] = saved_blocker(rec, fetch_state)
        state = "unknown" if rec["unknown_reason"] else "saved to GitHub"
    if state == "unknown":
        reason = rec["unknown_reason"]
    if note and reason != note:
        rec["suffix"].insert(0, note)
    rec["state"], rec["state_reason"] = state, reason

    if snap is None:
        rec["suffix"].append("no snapshot")
    else:
        if (snap_ts is not None and rec["newest_tracked_mtime"] is not None
                and int(rec["newest_tracked_mtime"]) > snap_ts):
            rec["suffix"].append("snapshot %s, files changed %s"
                                 % (hhmm(snap_ts), hhmm(rec["newest_tracked_mtime"])))
        st = snap.get("state") or ""
        if st == "working":
            rec["suffix"].append("session %s marked working at %s, no Stop since"
                                 % ((snap.get("session_id") or "?")[:8], when(snap_ts)))
        if st.startswith("failed:"):
            rec["suffix"].append("session ended %s at %s" % (st, hhmm(snap_ts)))
        if state == "working" and st != "working" and rec["newest_other_path"]:
            rec["suffix"].append("untracked or ignored file newer than the snapshot: %s"
                                 % rec["newest_other_path"])
    return rec


# ----------------------------------------------------------------- remote-only branches
def remote_only(repo, local_branches):
    prefix = "refs/remotes/origin/"
    out, err = git(["for-each-ref", "--format=%(refname)\t%(committerdate:unix)\t%(objectname:short)",
                    prefix], repo)
    rows = []
    if out is None:
        return rows
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        ref, ct, sha = parts
        if not ref.startswith(prefix):
            continue
        branch = ref[len(prefix):]
        if branch == "HEAD" or branch in local_branches:
            continue
        names, _ = git(["ls-tree", "--name-only", ref + ":" + LEDGER], repo)
        rows.append({
            "branch": branch, "commit_time": int(ct) if ct.isdigit() else None,
            "commit_time_iso": iso_utc(int(ct)) if ct.isdigit() else None,
            "head": sha, "last_handoff": newest_handoff_in(names.splitlines() if names else []),
        })
    rows.sort(key=lambda r: -(r["commit_time"] or 0))
    return rows


# ----------------------------------------------------------------- the shelf line
def shelf_status(repo):
    tool = os.path.join(repo, "shelf", "sync_shelf.py")
    if not os.path.isfile(tool):
        return {"available": False, "reason": "no shelf/sync_shelf.py in this checkout"}
    try:
        with open(tool, encoding="utf-8", errors="replace") as fh:
            src = fh.read()
    except OSError as e:
        return {"available": False, "reason": "cannot read the tool: %s" % e}
    if not re.search(r"^VERSION = \d+\b", src, re.M):
        return {"available": False, "reason": "this checkout's sync_shelf.py carries no VERSION line"}
    try:
        p = subprocess.run([sys.executable, tool, "status"], cwd=repo, capture_output=True,
                           text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"available": False, "reason": "status did not run: %s" % e}
    line = ""
    for l in p.stdout.splitlines():
        if l.startswith("SYNC|status|"):
            line = l
    if not line:
        return {"available": False, "reason": "status printed no summary (exit %d)" % p.returncode}
    nums = {}
    for m in re.finditer(r"(ok|unregistered|not_pulled|problems|registry)=(\d+)", line):
        nums[m.group(1)] = int(m.group(2))
    ok = nums.get("ok", 0)
    reg = nums.get("registry", 0)
    text = ("This Mac: {ok:,} of {reg:,} shelf files pulled into shelf/local; {np:,} not pulled "
            "(normal: the Drive mount serves them); {un:,} files here not yet on the shelf; problems {pr}"
            .format(ok=ok, reg=reg, un=nums.get("unregistered", 0), np=nums.get("not_pulled", 0),
                    pr=nums.get("problems", 0)))
    return {"available": True, "exit": p.returncode, "text": text, "summary": line.split("|store=")[0]}


# ----------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description="live status of every kom-festival-board checkout")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--plain", action="store_true", help="one line per checkout (default)")
    g.add_argument("--json", action="store_true", help="the full scan as JSON")
    ap.add_argument("--no-fetch", action="store_true", help="skip git fetch (offline; tests)")
    ap.add_argument("--fetch-timeout", type=int, default=25, metavar="SECONDS")
    ap.add_argument("--repo", metavar="PATH", help="any checkout of the repository to scan "
                    "(default: the one holding this script)")
    ap.add_argument("--status-dir", metavar="PATH",
                    default=os.environ.get("KOM_STATUS_DIR") or os.path.join(HOME, ".kom", "status"),
                    help="snapshot directory (default $KOM_STATUS_DIR or $HOME/.kom/status)")
    a = ap.parse_args(argv)
    now = time.time()

    start = a.repo or HERE
    out, err = git(["rev-parse", "--show-toplevel"], start)
    if out is None:
        print("kom-status: not a git checkout: %s (%s)" % (display(start), err), file=sys.stderr)
        return 2
    repo = out.strip()

    wts, err = list_worktrees(repo)
    if wts is None:
        print("kom-status: git worktree list failed: %s" % err, file=sys.stderr)
        return 2

    fetch_state = "skipped"
    fetch_detail = ""
    if not a.no_fetch:
        out, err = git(FETCH_CMD, repo, timeout=a.fetch_timeout)
        if out is None:
            fetch_state, fetch_detail = "failed", redact_url(err)   # git's error can quote the URL
        else:
            fetch_state = "ok"

    snaps = load_snapshots(a.status_dir)
    roots = [w["path"] for w in wts]
    checkouts = [scan_checkout(w, roots, snaps, fetch_state, now) for w in wts]
    local_branches = set(w.get("branch") for w in wts if w.get("branch"))
    remotes = remote_only(repo, local_branches)
    shelf = shelf_status(repo)

    result = {
        "generated_at": iso_utc(now), "generated_local": time.strftime("%Y-%m-%d %H:%M", time.localtime(now)),
        "repo": repo, "repo_display": display(repo),
        "fetch": fetch_state, "fetch_detail": fetch_detail, "fetch_command": "git " + " ".join(FETCH_CMD),
        "status_dir": a.status_dir, "snapshots_read": len(snaps),
        "states": list(STATES), "checkouts": checkouts, "remote_only": remotes, "shelf": shelf,
    }
    if a.json:
        print(json.dumps(result, indent=2, sort_keys=False))
        return 0

    print("kom-status %s — %d checkouts — fetch --prune origin: %s%s — snapshots read: %d from %s"
          % (result["generated_local"], len(checkouts), fetch_state,
             (" (" + fetch_detail + ")") if fetch_detail else "", len(snaps), display(a.status_dir)))
    for r in checkouts:
        state = r["state"]
        if r["state_reason"]:
            state += " (%s)" % r["state_reason"]
        if r["suffix"]:
            state += " (" + "; ".join(r["suffix"]) + ")"
        print("%s — %s — commit time %s — handoff %s — %s dirty:%s ahead:%s behind:%s — last file change %s — %s"
              % (r["lane"] or "?", state, rel_time(r["commit_time"], now),
                 r["last_handoff"] if r["last_handoff"] else "none", r["branch"],
                 "?" if r["dirty"] is None else r["dirty"], "?" if r["ahead"] is None else r["ahead"],
                 "?" if r["behind"] is None else r["behind"],
                 hhmm(r["last_file_change"]), r["path_display"]))
    if remotes:
        print("on GitHub, no local view:")
        for r in remotes:
            print("  %s — commit time %s — handoff %s" % (r["branch"], rel_time(r["commit_time"], now),
                                                          r["last_handoff"] or "none"))
    if shelf.get("available"):
        print("shelf: %s (exit %d)" % (shelf["text"], shelf["exit"]))
    else:
        print("shelf: %s" % shelf.get("reason"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
