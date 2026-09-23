#!/usr/bin/env python3
"""sync_shelf — the KILLER OF MEN shelf (a Google Drive folder) indexed in git, safely.

KOM build 1, 2026-09-23. This file is Petrol's blender/scripts/harness/bin/sync_assets.py
v4 (sha256 1eccff3f3cbe2a728ea8223a63413cdb81b4d51626f699ba843817022f0367aa) with its constants, paths, bases and
words changed for this project and one mode added. The v4 contract and every audited fix
(quarantine, never replace; per-key locks; hash gates; exit 2 = refused before touching
anything) carry over unchanged; the audit history is in that file's docstring and in
petrol-brand-bible's FALSIFY-sync_assets-v4.md. The falsification run of THIS file is
shelf/FALSIFY-sync_shelf.md (re-run: bash shelf/test-sync_shelf.sh).

  git   = words, code, records, handoffs, and THIS registry (shelf/registry.json)
  shelf = the big files: "My Drive/KILLER OF MEN" in camerawrap@gmail.com's Google Drive

SHELF: $KOM_SHELF, else the one Google Drive mount's "My Drive/KILLER OF MEN". It must
carry .store_id matching the registry's store_id; register/push refuse an unstamped shelf
unless --init-store, which stamps it exclusively (O_CREAT|O_EXCL under .locks/store_id.lock).

LOCAL: shelf/local/<key> in this checkout (gitignored) is the local mirror; a key is the
shelf-relative path, e.g. "05 MARKETING/00 PRESS/POSTER/KillerOfMen_Poster_2160x2700.jpg".
Nothing needs to be pulled to work: the Drive mount serves the bytes on this Mac; pull is
for a Mac without the mount, or for a build that wants a checked copy.

  shelf/sync_shelf.py register [--only P] [--deep] [--force] [--init-store]
      adopt what is already ON THE SHELF: walk <shelf>/<base>, hash every file the
      registry does not know, write its line. A registered key is counted ok when the
      shelf copy has the registered size (--deep hashes it too); a shelf copy that
      differs from its line is "STORE DIFFERS FROM REGISTRY", a problem, re-registered
      only with --force. Reads the shelf, writes only the registry (and .store_id with
      --init-store). Never copies bytes, never touches shelf/local.
  shelf/sync_shelf.py push     [--only P] [--update] [--force] [--init-store] [--prune [--yes]]
      local -> shelf, then registers (the v4 gates: STORE CONFLICT, LOCAL CHANGED, ...).
  shelf/sync_shelf.py pull     [--only P] [--force]          shelf -> local, per key, quarantining what it displaces
  shelf/sync_shelf.py verify   [--only P] [--deep] [--strict]  both sides against the registry
  shelf/sync_shelf.py status   [--only P]                    local only; never opens a shelf file
  shelf/sync_shelf.py merge-registry <other.json>            union by key; exit 2 on any conflict
  shelf/sync_shelf.py verify-store <copy> --manifest <frozen.json> [--index <INDEX.tsv> | --no-quarantine]
  shelf/sync_shelf.py --version                              prints "sync_shelf 4 (KOM build 1)"

NEVER A BARE PULL: --only <path> always. The shelf is 2.6 GB today and grows.

BASES (shelf-relative, every file, ungated: a fresh checkout has none locally, so a
registered file absent from shelf/local is NOT PULLED, never a problem):
  05 MARKETING/00 PRESS · 05 MARKETING/07 FESTIVALS · DELIVERY · HANDOFFS
Never covered: .DS_Store, .store_id, .locks/, .quarantine/, and the VOLATILE suffixes
(.log .part .tmp .crdownload, and Drive's document shortcuts .gdoc .gsheet .gslides
.gdraw .gform .gmap .gsite .gjam, which hold a URL, not the document).

EXIT CODES (the v4 contract, every mode): 0 = ran clean; 1 = ran and found problems;
2 = refused before touching anything (no shelf, several Drive mounts, wrong .store_id,
a registry that does not parse or names no store, an unstamped shelf on register/push
without --init-store, --only matching nothing, --prune without --yes, a flag on a mode
it means nothing in, a merge-registry conflict, ...). Read every exit code unpiped, on
its own line.

SUMMARY LINE, always last:
  SYNC|<mode>|ok= copied= skipped= unregistered= not_pulled= problems=|registry= store=
In register, copied= counts the registry lines written this run. A `verify` that exits
0 is an inventory result; a CERTIFICATE is `verify --deep --strict` whose ok= equals an
independently counted number with unregistered=0 not_pulled=0 problems=0.

QUARANTINE: nothing this tool displaces is deleted. A shelf copy push replaces goes to
<shelf>/.quarantine/<key>.<UTC>.<sha256 first 12>; a local file pull replaces goes to
shelf/local/.quarantine/...; each move is one line in that root's .quarantine/INDEX.tsv.
"""
import argparse
import errno
import glob
import hashlib
import json
import os
import re
import shutil
import socket
import stat
import sys
import time
import uuid

VERSION = 4  # the Petrol sync_assets contract this file carries
KOM_BUILD = 1

HERE = os.path.dirname(os.path.abspath(__file__))  # <checkout>/shelf
REPO = os.path.abspath(os.path.join(HERE, ".."))
REPO_REAL = os.path.realpath(REPO)
LOCAL = os.path.join(REPO, "shelf", "local")  # the gitignored local mirror; <LOCAL>/<key>
REG = os.path.join(HERE, "registry.json")
SHELF_ENV = "KOM_SHELF"
SHELF_GLOB = "~/Library/CloudStorage/GoogleDrive-*/My Drive/KILLER OF MEN"
PROBE = 1 << 20  # 1 MiB head+tail readability probe
VOLATILE = (".log", ".part", ".tmp", ".crdownload",
            ".gdoc", ".gsheet", ".gslides", ".gdraw", ".gform", ".gmap", ".gsite", ".gjam")
QDIR = ".quarantine"
INDEX = "INDEX.tsv"
LOCKS = ".locks"  # <store>/.locks/<sha256 of the key>.lock (fix L, KeyLock), store_id.lock (F2)
STORE_ID_LOCK = "store_id.lock"  # --init-store's lock, <store>/.locks/store_id.lock (F2)
# The checkout's locks, under the gitignored .petrol/ (a stale lock beside
# the tracked registry could be committed): the registry's (R), and pull's,
# one per key (F1).
LOCAL_LOCKS = os.path.join(REPO, ".kom", "locks")
REG_LOCK = os.path.join(LOCAL_LOCKS, "registry.json.lock")
REG_LOCK_WAIT = 30.0  # seconds a registry save waits for that lock; a save holds it well under 1 s
LOCK_POLL = 0.05  # seconds between tries of a lock that is waited for
HASH_TRIES = 3  # F5: reads of a file, in all, when its signature moves while it is read
# FLAG / MODE CONTRACT (v4 (4)): the modes each flag means something in.
# Any other mode given the flag is a refusal (exit 2), never a silent
# no-op; a flag argparse knows but this table lacks is refused too.
FLAG_MODES = {
    "only": ("push", "pull", "verify", "status", "register"),
    "deep": ("verify", "register"),
    "strict": ("verify",),
    "force": ("push", "pull", "register"),
    "update": ("push",),
    "init_store": ("push", "register"),
    "prune": ("push",),
    "yes": ("push",),
    "manifest": ("verify-store",),
    "index": ("verify-store",),
    "no_quarantine": ("verify-store",),
}


# (prefix, include(basename) -> bool or None for everything, gated). The four Drive
# subfolders of "KILLER OF MEN", every file, all ungated (a checkout legitimately holds
# none of them locally; the registry, not shelf/local, is the inventory).
FIXED_BASES = (
    ("05 MARKETING/00 PRESS", None, False),
    ("05 MARKETING/07 FESTIVALS", None, False),
    ("DELIVERY", None, False),
    ("HANDOFFS", None, False),
)
BASES = list(FIXED_BASES)


def discover_bases(files):
    """The fixed four; nothing is discovered (Petrol added blender/units/<unit>/tex here)."""
    return list(FIXED_BASES)


def base_prefixes():
    return [b for b, _inc, _g in BASES]


def gated(base):
    """Non-base groups (the big top-level blends) behave as gated."""
    for b, _inc, g in BASES:
        if b == base:
            return g
    return True


def refuse(msg):
    """Every refusal: message on stderr, exit 2, nothing touched (v4 (4)).
    stdout is flushed first so a transcript shows the cause before the
    refusal when both streams land in one file."""
    sys.stdout.flush()
    print(f"sync_shelf: {msg}", file=sys.stderr)
    sys.exit(2)


def oserr(e):
    """The short reason an OSError carries (its strerror), else its text."""
    return getattr(e, "strerror", None) or str(e)


def id_problem(doc):
    """F4 (Codex round 3): how a registry, or a manifest, names no store (a
    phrase for a refusal), or None when its store_id is a non-empty
    string."""
    if not isinstance(doc, dict) or "store_id" not in doc:
        return "carries no store_id"
    sid = doc["store_id"]
    if isinstance(sid, str) and sid.strip():
        return None
    return f"has store_id {json.dumps(sid)}"


def registry_id(reg):
    """F4 (Codex round 3): the registry's store_id, which must be a
    non-empty string, else a refusal (exit 2): REGISTRY HAS NO STORE ID.
    store_root() can check a store's .store_id only against an id; run 8
    compared the two only when both were non-empty, so a registry holding
    null or "" accepted a store stamped with any id. A registry this run
    creates (no file yet) carries the new id load_reg() gave it."""
    how = id_problem(reg)
    if how is None:
        return reg["store_id"]
    refuse(f"REGISTRY HAS NO STORE ID. {REG} {how}, so no store's .store_id can be checked "
           f"against it. Nothing touched. Write into its \"store_id\" the id in the .store_id "
           f"of the store it indexes; --init-store stamps a new store only with an id the "
           f"registry names.")


def store_root(reg):
    p = os.environ.get(SHELF_ENV)
    if not p:
        hits = sorted(glob.glob(os.path.expanduser(SHELF_GLOB)))
        if not hits:
            refuse(f"no shelf. Set ${SHELF_ENV}, or sign Drive for desktop in as "
                   f"camerawrap@gmail.com so that '{SHELF_GLOB}' exists.")
        if len(hits) > 1:
            refuse(f"multiple Drive shelves found; set ${SHELF_ENV} "
                   "explicitly:\n  " + "\n  ".join(hits))
        p = hits[0]
    want = registry_id(reg)  # F4: main() has refused a registry that names no store
    idf = os.path.join(p, ".store_id")
    have = None
    if os.path.lexists(idf):
        try:
            with open(idf) as f:
                have = f.read().strip()
        except OSError as e:
            refuse(f"cannot read {idf}: {e.strerror or e}")
    if have and want != have:
        refuse(f"WRONG STORE. registry expects {want}, {p} carries {have}. "
               f"Refusing to touch it.")
    return p, have


def covered():
    """Everything heavy and gitignored. Recursive; nothing top-level-only.
    Hidden directories are walked (three registered keys live under a
    .vrayThumbs/); only .DS_Store and VOLATILE suffixes are skipped."""
    out = set()
    for base, include, _g in BASES:
        for dp, dns, fns in os.walk(os.path.join(LOCAL, base)):
            dns[:] = [d for d in dns if d not in (QDIR, LOCKS)]
            for fn in fns:
                if fn in (".DS_Store", ".store_id") or fn.endswith(VOLATILE):
                    continue
                if include is not None and not include(fn):
                    continue
                out.add(os.path.relpath(os.path.join(dp, fn), LOCAL).replace(os.sep, "/"))
    return sorted(out)


def shelf_walk(store):
    """register: every file under every base ON THE SHELF, as keys (the same
    exclusions as covered(), plus the shelf's own .quarantine/ and .locks/)."""
    out = set()
    for base, include, _g in BASES:
        for dp, dns, fns in os.walk(os.path.join(store, base)):
            dns[:] = [d for d in dns if d not in (QDIR, LOCKS)]
            for fn in fns:
                if fn in (".DS_Store", ".store_id") or fn.endswith(VOLATILE):
                    continue
                if include is not None and not include(fn):
                    continue
                out.add(os.path.relpath(os.path.join(dp, fn), store).replace(os.sep, "/"))
    return sorted(out)


def shelf_hash(p):
    """register: (sha256, stat_sig) of a shelf file. hash_still() first (F5: a read
    across which the full signature held still). A Drive placeholder hydrates during
    its first read and may move its ctime or inode as it does, which F5 rightly calls
    a change; when every read moved, two further reads that agree are accepted, so
    the digest still names bytes read twice the same. None when nothing agrees."""
    got = hash_still(p)
    if got is not None:
        return got
    a, b = sha256(p), sha256(p)
    if a == b:
        return a, stat_sig(p)
    return None


def sha256(p, bufsize=4 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while True:
            b = f.read(bufsize)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def readable(p, size):
    """Head+tail probe. Forces Drive to hydrate a placeholder and
    catches truncation/IO errors without hashing 41 GiB."""
    try:
        with open(p, "rb") as f:
            if not f.read(min(PROBE, size)) and size:
                return False
            if size > PROBE:
                f.seek(-min(PROBE, size), os.SEEK_END)
                if not f.read():
                    return False
        return True
    except OSError:
        return False


def safe_rel(rel):
    full = os.path.abspath(os.path.join(LOCAL, rel))
    return full.startswith(LOCAL + os.sep) and not os.path.isabs(rel)


def load_reg():
    if os.path.exists(REG):
        try:
            with open(REG) as f:
                reg = json.load(f)
        except (OSError, ValueError) as e:
            refuse(f"cannot read the registry {REG}: {e}")
        if not isinstance(reg, dict) or not isinstance(reg.get("files", {}), dict):
            refuse(f"registry {REG} holds no 'files' mapping")
        return reg
    return {"_doctrine": "Committed index of the KILLER OF MEN shelf: one sha256 per "
            "shelf-relative path. Bytes live on the shelf (My Drive/KILLER OF MEN, "
            "$KOM_SHELF), mirrored at shelf/local/<key> when pulled. "
            "shelf/sync_shelf.py register/push/pull/verify/status/merge-registry/"
            "verify-store; never a bare pull.",
            "store_id": str(uuid.uuid4()), "files": {}}


def snapshot(reg):
    """The registry as this run loaded it: its store_id and every line in
    canonical form, so save_reg() can tell this run's changes from lines
    another run wrote meanwhile (R)."""
    return {"store_id": reg.get("store_id"),
            "files": {k: json.dumps(v, sort_keys=True) for k, v in reg.get("files", {}).items()}}


def brief(e):
    """A registry line in a few words, for REGISTRY CONFLICT."""
    if e is None:
        return "no line"
    if not isinstance(e, dict):
        return "a line that is not a mapping"
    if e.get("type") == "symlink":
        return f"a link -> {e.get('target')}"
    return f"sha256 {str(e.get('sha256'))[:12]}"


def contract(e):
    """What two registry lines must share to be the same line (norm_entry);
    None for no line."""
    if e is None:
        return None
    if not isinstance(e, dict):
        return ("not a mapping", json.dumps(e, sort_keys=True))
    return norm_entry(e)


def save_reg(reg, base, strict=False):
    """Record this run's registry changes, merged into the registry as it is
    on disk NOW (R, ruled 2026-09-23). Two pushes in one checkout used to
    save their whole in-memory copies, so the last save dropped the other's
    new lines while both exited 0 (10 of 10 rounds, measured). Now, holding
    REG_LOCK (FileLock, waited for up to REG_LOCK_WAIT s): re-read the
    registry on disk, apply only the lines this run changed since it
    loaded (`base`, a snapshot(); None when no registry existed then), and
    replace the file atomically. A line another run changed meanwhile to a
    different contract is a conflict: the line on disk is kept, and the
    conflict is returned as (key, on disk, this run's); with strict
    (merge-registry) any conflict means nothing is written. A run that
    changed nothing takes no lock and writes nothing. Raises OSError (push
    prints REGISTRY NOT WRITTEN) when the lock cannot be had, or when the
    registry on disk cannot be read, has gone since this run loaded it, or
    names another store or none (F4: run 8 kept a null or "" id there)."""
    ours = reg.setdefault("files", {})
    start = (base or {}).get("files", {})
    changed = [k for k in sorted(set(start) | set(ours))
               if (json.dumps(ours[k], sort_keys=True) if k in ours else None) != start.get(k)]
    if base is not None and not changed and base.get("store_id") == reg.get("store_id"):
        return []
    name = os.path.relpath(REG, REPO).replace(os.sep, "/")
    try:
        lock = FileLock(REG_LOCK, name, "registry save", wait=REG_LOCK_WAIT)
    except Locked as e:
        raise OSError(f"the registry lock is held: {e}")
    with lock:
        try:
            with open(REG) as f:
                disk = json.load(f)
        except FileNotFoundError:
            if base is not None:
                raise OSError(f"{name} was removed after this run read it; this run's "
                              f"{len(changed)} changed line(s) are not recorded")
            disk = {k: v for k, v in reg.items() if k != "files"}
        except (OSError, ValueError) as e:
            raise OSError(f"the registry on disk cannot be read now ({oserr(e)}); this run's "
                          f"{len(changed)} changed line(s) are not recorded")
        if not isinstance(disk, dict) or not isinstance(disk.get("files", {}), dict):
            raise OSError(f"the registry on disk holds no 'files' mapping now; this run's "
                          f"{len(changed)} changed line(s) are not recorded")
        now_id = disk.get("store_id")
        if reg.get("store_id") and now_id != reg["store_id"]:
            what = (f"names store {now_id}" if isinstance(now_id, str) and now_id.strip()
                    else "carries no store_id" if "store_id" not in disk
                    else f"has store_id {json.dumps(now_id)}")
            raise OSError(f"the registry on disk now {what}; this run used {reg['store_id']}; "
                          f"its {len(changed)} changed line(s) are not recorded")
        dfiles = disk.setdefault("files", {})
        conflicts = []
        for k in changed:
            now, mine = dfiles.get(k), ours.get(k)
            now_c = None if now is None else json.dumps(now, sort_keys=True)
            if now_c != start.get(k) and contract(now) != contract(mine):
                conflicts.append((k, now, mine))  # another run changed this line meanwhile
                continue
            if mine is None:
                dfiles.pop(k, None)
            else:
                dfiles[k] = mine
        if strict and conflicts:
            return conflicts
        tmp = f"{REG}.{os.getpid()}.part"
        try:
            with open(tmp, "w") as f:
                json.dump(disk, f, indent=1, sort_keys=True)
            os.replace(tmp, REG)
        finally:
            if os.path.lexists(tmp):  # a failed write leaves no .part behind
                os.remove(tmp)
        for k, v in disk.items():  # this run now holds what it wrote
            if k != "files":
                reg[k] = v
        ours.clear()
        ours.update(dfiles)
    return conflicts


def utc_stamp():
    """(compact for file names, ISO for INDEX.tsv) of the same instant."""
    t = time.gmtime()
    return time.strftime("%Y%m%dT%H%M%SZ", t), time.strftime("%Y-%m-%dT%H:%M:%SZ", t)


def private_name(path, tag):
    """A fresh name beside `path` that no other process uses,
    <path>.<pid>.<8 hex>.<tag>: renaming onto it replaces nothing."""
    return f"{path}.{os.getpid()}.{uuid.uuid4().hex[:8]}.{tag}"


def sig_of(st):
    """(inode, size, mtime_ns) of an os.stat_result, as stat_sig() gives."""
    return (st.st_ino, st.st_size, st.st_mtime_ns)


def install(part, dst):
    """Round 2, F1 (Codex, 2026-09-23): put `part`, a staged copy only this
    process writes, at dst with os.link(), which creates dst or fails with
    EEXIST when ANY path is there (a file, a dangling link, a directory):
    it never replaces one. Then unlink `part`. FileExistsError: nothing at
    dst was touched and `part` is still there for the caller to remove.
    (Fix L's claim() left an empty file at dst and renamed onto it, so a
    writer that wrote into the claim, or quarantined it and installed its
    own bytes, lost them to that rename.)"""
    os.link(part, dst)
    os.remove(part)


def place(src, dst, digest=None):
    """Step 1 of a move (round 2, F1): put the object at src (a regular
    file, or a symlink) at dst with a call that fails with EEXIST when any
    path is there, never replacing one: os.link() for a file (a second
    name of the same inode), os.symlink() with the same text for a link.
    Across devices (EXDEV) the file is copied to a private .part beside
    dst, checked against `digest` (else against src hashed again), and
    linked there the same way. FileExistsError: nothing moved. Returns
    (src's lstat as it was read, True when dst is a hard link of it)."""
    before = os.lstat(src)
    if stat.S_ISLNK(before.st_mode):
        os.symlink(os.readlink(src), dst)
        return before, False
    try:
        os.link(src, dst, follow_symlinks=False)
        return before, True
    except OSError as e:
        if e.errno != errno.EXDEV:
            raise
    part = private_name(dst, "part")
    try:
        shutil.copy2(src, part)
        if sha256(part) != (digest or sha256(src)):
            raise OSError(f"cross-device move of {src} did not verify; source kept")
        os.link(part, dst)
    finally:
        if os.path.lexists(part):
            os.remove(part)
    return before, False


def put_back(held, path):
    """Return the object at the private name `held` to `path` without
    replacing anything there (link(), or symlink() for a link), then drop
    `held`. When that fails `held` is kept, and the OSError names it."""
    try:
        if os.path.islink(held):
            os.symlink(os.readlink(held), path)
        else:
            os.link(held, path, follow_symlinks=False)
    except OSError as e:
        raise OSError(e.errno, f"{path} changed while it was being moved and what was there "
                               f"cannot be put back ({oserr(e)}); it is kept at {held}")
    os.remove(held)


def unplace(src, dst, hard):
    """Undo place() when src keeps its object: dst goes only while it is a
    second name of the object at src (a hard link) or this process's own
    copy or link. Best effort; the caller raises its own error."""
    try:
        if not hard or os.path.samestat(os.lstat(src), os.lstat(dst)):
            os.remove(dst)
    except OSError:
        pass


def release(src, dst, before, hard):
    """Steps 2 and 3 of a move (round 2, F1): take the name src away from
    the object place() put at dst, and from nothing else. src is detached
    onto a fresh private name beside it (a rename onto a name nothing
    holds, so nothing is replaced; whatever sits at src at that instant is
    what moves), and that name is unlinked only when it holds the object
    now at dst: the same inode (a hard link), or for a copy or a link the
    same (inode, size, mtime) src had when place() read it. Anything else
    is an object a writer that takes no lock put at src meanwhile:
    put_back() returns it to src, and it is never unlinked. When src
    cannot be detached (or the check cannot be made), the object stays at
    (or goes back to) src and unplace() removes dst, so a quarantine name
    never stays a second name of a live file; the error is raised."""
    held = private_name(src, "moving")
    try:
        os.rename(src, held)
    except OSError:
        unplace(src, dst, hard)
        raise
    try:
        now = os.lstat(held)
        mine = os.path.samestat(now, os.lstat(dst)) if hard else sig_of(now) == sig_of(before)
    except OSError:
        put_back(held, src)
        unplace(src, dst, hard)
        raise
    if mine:
        os.remove(held)
    else:
        put_back(held, src)


def move_no_clobber(src, dst, digest=None):
    """Move src to dst, never replacing anything at dst and never unlinking
    anything at src but the object moved: place(), then release().
    FileExistsError, src untouched, when a path is at dst. (Run 5's build
    tested lexists(dst) and then renamed; run 7's claimed dst with an
    empty file and renamed onto the claim, which a second writer could
    fill or quarantine first: Codex round 2, F1.)"""
    before, hard = place(src, dst, digest)
    release(src, dst, before, hard)


def quarantine(path, root, mode, sha=None, sig=None, strict=False):
    """v4 (6)(7): THE one displacement helper for both sides. Moves `path`
    (a regular file, or a symlink recorded by its link text) to
    <root>/.quarantine/<rel>.<UTC stamp>.<sha256 first 12>, appending
    -1, -2, ... when that name is taken. The move is place() then
    release() (round 2, F1): the file reaches the name through link(), a
    symlink through symlink(), each failing when the name is taken, so no
    quarantine path is ever replaced. Appends one line to
    <root>/.quarantine/INDEX.tsv, whose header only the process that
    creates the file writes:
      utc  mode  rel  sha256  bytes  quarantine-path
    The line names what the quarantine path holds (F5, Codex round 4): a
    file's sha256 and size are read from its quarantine name after the
    link, while its full signature held still (hash_still()), and read
    there again if it moved before the line is written; a link is listed
    by its text. No digest read before the move is ever listed (run 9
    listed the caller's, which a rewrite during the caller's read had
    made stale). Returns the quarantine path relative to root. `sha`, the
    digest a caller already read (the push gate, pull's pre-check), names
    the file without another read here on a strict move, which checks it
    after the link; a move that is not strict reads the file for its name,
    so a digest nothing checked never names a quarantined file.
    strict (F3, F5; every move push and pull make): `path` must still
    carry `sig` when it is read here, the object linked to the quarantine
    name must be the one that carried it (the same inode, size and mtime
    once linked), and its bytes, read from the quarantine name under a
    signature that held still and is still `sig`, must hash to `sha` (to
    what this helper read before the move when no `sha` is given);
    otherwise the link is undone and Changed is raised, nothing moved."""
    rel = os.path.relpath(path, root).replace(os.sep, "/")
    if rel.startswith("../") or os.path.isabs(rel):
        raise ValueError(f"quarantine: {path} is outside {root}")
    st0 = stat_sig(path)
    if st0 is None:
        raise FileNotFoundError(errno.ENOENT, "nothing to quarantine", path)
    if strict and st0 != sig:
        raise Changed(path)  # F3: not the object the caller checked; nothing moved
    text = None
    if os.path.islink(path):
        text = os.readlink(path)
        digest, nbytes = sha256_text(text), len(text.encode("utf-8"))
    else:
        # the NAME's digest (F5): the caller's only on a strict move, which
        # checks it after the link (strict has already required st0 == sig);
        # the INDEX line's is read from the quarantine name after the link
        digest = sha if (strict and sha is not None) else sha256(path)
        nbytes = st0[1]
    compact, iso = utc_stamp()
    qdir = os.path.join(root, QDIR)
    first = os.path.join(qdir, f"{rel}.{compact}.{digest[:12]}")
    os.makedirs(os.path.dirname(first), exist_ok=True)
    dst, n = first, 0
    while True:  # the first free name: place() never replaces a taken one
        try:
            before, hard = place(path, dst, None if text is not None else digest)
            break
        except FileExistsError:
            n += 1
            dst = f"{first}-{n}"
    qrel = os.path.relpath(dst, root).replace(os.sep, "/")
    held = None  # F5: (sha256, stat_sig) of the bytes at dst, read after the link
    try:
        if strict and (sig_of(before) != sig or (hard and stat_sig(dst) != sig)):
            # F3: what was linked is not the object checked (it was replaced
            # or rewritten between the check and the link): undo the link
            unplace(path, dst, hard)
            raise Changed(path)
        if strict and text is None:
            # F5: the bytes linked must be the ones the caller hashed, read from
            # the quarantine name while the signature held still and was still
            # the caller's (a rewrite that put the old mtime back passes the
            # check above): else undo the link. A read that the signature moved
            # under is made again (metadata alone can move the ctime); the
            # digest decides.
            try:
                held = hash_still(dst)
            except OSError:
                unplace(path, dst, hard)
                raise
            if held is None or held[0] != digest or (hard and held[1] != sig):
                unplace(path, dst, hard)
                raise Changed(path)
        release(path, dst, before, hard)
    finally:  # a version still at dst is listed, whatever release() met
        if os.path.lexists(dst):
            if os.path.islink(dst):
                now = os.readlink(dst)
                if now != text:
                    digest, nbytes = sha256_text(now), len(now.encode("utf-8"))
                mode += "-link"
            else:
                # F5: the bytes the quarantine name holds, read from it after the
                # link; read (again) when not read yet or moved since
                if held is None or stat_sig(dst) != held[1]:
                    held = hash_still(dst) or (sha256(dst), stat_sig(dst))
                digest, nbytes = held[0], held[1][1]
            line = f"{iso}\t{mode}\t{rel}\t{digest}\t{nbytes}\t{qrel}\n"
            index = os.path.join(qdir, INDEX)
            try:
                fd = os.open(index, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_APPEND, 0o644)
                line = "# utc\tmode\trel\tsha256\tbytes\tquarantine-path\n" + line
            except FileExistsError:
                fd = os.open(index, os.O_WRONLY | os.O_APPEND)
            with os.fdopen(fd, "a") as f:
                f.write(line)
    return qrel


class Locked(Exception):
    """Another writer holds the lock: push and pull print LOCKED, a problem
    (a key's lock is never waited for); a lock that is waited for (the
    registry's, --init-store's) raises it once the wait is over."""


class DestinationExists(Exception):
    """Round 2, F1: install() found a path at the key (link() refused it).
    Only a writer that takes no lock can put one there while the key's
    lock is held. Nothing was replaced and nothing more is quarantined;
    `quarantined` names the prior copy this run displaced first, if any."""

    def __init__(self, quarantined):
        super().__init__(quarantined)
        self.quarantined = quarantined


class Changed(Exception):
    """F3 (Codex round 3): the object at a path is not the one its caller
    checked. `stage` "copy": copy_atomic() (push) had made its staged copy
    and the path no longer carried the (inode, size, mtime) the caller read,
    nor the bytes it hashed (pull makes the same check inline). `stage`
    "move": quarantine(strict=True) found another (inode, size, mtime) when
    it read the path or once it had linked it to its quarantine name, or
    (F5) read bytes there that are not the ones the caller hashed. `stage`
    "source" (F6): copy_atomic()'s staged copy of the path (push's local
    file) does not hold the bytes the caller hashed: the file was written
    while it was copied. Nothing is moved: the path keeps what the writer
    put there, and a quarantine name made for it is removed again (it is
    kept, and listed in INDEX.tsv, only when the path was replaced as well,
    so that the name is all that still holds what was linked)."""

    def __init__(self, path, stage="move"):
        super().__init__(path)
        self.stage = stage


def pid_running(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def read_lock(path):
    """(raw bytes, holder) of a lock file; (None, None) when there is none.
    holder is None when the content is not a lock this tool wrote; such a
    lock is held, never judged stale."""
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except FileNotFoundError:
        return None, None
    except OSError:
        return b"", None
    try:
        who = json.loads(raw.decode("utf-8"))
    except ValueError:
        return raw, None
    if (isinstance(who, dict) and type(who.get("pid")) is int and 0 < who["pid"] < 2 ** 31
            and isinstance(who.get("host"), str)):
        return raw, who
    return raw, None


def break_stale(path, raw):
    """Remove the stale lock `path`, whose bytes were `raw`, while holding
    <lock>.break (created O_CREAT|O_EXCL), and only if it re-reads
    byte-identical: two processes that judged the same lock stale can never
    remove the fresh lock one of them made afterwards. True when the lock
    is gone."""
    brk = path + ".break"
    try:
        os.close(os.open(brk, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600))
    except FileExistsError:
        return False
    try:
        now, _who = read_lock(path)
        if now is None:
            return True
        if now != raw:
            return False
        os.remove(path)
        return True
    finally:
        os.remove(brk)


class FileLock:
    """v4 fix L (Codex code audit, 2026-09-23), R (ruled after run 6) and
    round 2 (F1, F2): the exclusive lock every store write of push runs
    under (KeyLock in <store>/.locks/, one per key), every install of pull
    (KeyLock in <checkout>/.kom/locks/, one per key), every registry
    save (REG_LOCK, one per checkout) and --init-store's stamp
    (<store>/.locks/store_id.lock). The lock file is created with O_CREAT|O_EXCL and holds one
    JSON line (key, host, pid, utc, mode, token). Stale-lock rule: a lock
    naming THIS host and a pid that is not running is removed
    (break_stale) and the acquire retried, printed as "stale lock
    removed". Every other lock is held: a running pid, another host (its
    process cannot be checked from here), content this tool did not
    write, or a stale lock whose <lock>.break is already present. A held
    lock raises Locked at once when `wait` is 0 (a store key: push prints
    LOCKED and copies nothing), or after polling for `wait` seconds (the
    registry). Released on every exit, removing only its own lock."""

    def __init__(self, path, key, mode, wait=0.0):
        self.path = path
        host = socket.gethostname()
        self.body = (json.dumps({"key": key, "host": host, "pid": os.getpid(),
                                 "utc": utc_stamp()[1], "mode": mode,
                                 "token": uuid.uuid4().hex}, sort_keys=True)
                     + "\n").encode("utf-8")
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        deadline, churn = time.time() + wait, 0
        while True:
            try:
                fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except FileExistsError:
                raw, who = read_lock(self.path)
                if raw is None:
                    why = None  # released in between: try again
                elif who is None:
                    why = (f"{self.path} cannot be read or is not a lock this tool wrote; "
                           f"remove it if no sync_assets run is using it")
                else:
                    since = f"pid {who['pid']} on {who['host']} since {who.get('utc', '?')}"
                    if who["host"] != host:
                        why = (f"held by {since}; a process on another host cannot be "
                               f"checked from here; lock {self.path}")
                    elif pid_running(who["pid"]):
                        why = f"held by {since}, running; lock {self.path}"
                    elif break_stale(self.path, raw):
                        print(f"stale lock removed  {key}  ({since}: not running)")
                        why = None
                    else:
                        why = (f"the stale lock of {since} (not running) is being removed "
                               f"by another process, or {self.path}.break was left behind; "
                               f"remove both if no sync_assets run is using them")
                if why is None:
                    churn += 1
                    if churn < 3 or time.time() < deadline:
                        continue
                    why = (f"{self.path} changed hands {churn} times while this {mode} tried "
                           f"to take it")
                if time.time() >= deadline:
                    raise Locked(why + (f"; waited {wait:g} s" if wait else ""))
                time.sleep(LOCK_POLL)
                continue
            try:
                os.write(fd, self.body)
            except BaseException:
                os.close(fd)
                os.remove(self.path)
                raise
            os.close(fd)
            return

    def __enter__(self):
        return self

    def __exit__(self, kind, _value, _tb):
        raw, _who = read_lock(self.path)
        if raw == self.body:
            os.remove(self.path)
        elif kind is None:
            raise OSError(f"the lock {self.path} was removed or replaced while it was held")
        return False


class KeyLock(FileLock):
    """A per-key lock, <sha256 of the key>.lock in `lockdir`, never waited
    for: push's in <store>/.locks/ (fix L), pull's in LOCAL_LOCKS, the
    checkout's .kom/locks/ (round 2, F1)."""

    def __init__(self, lockdir, rel, mode):
        super().__init__(os.path.join(lockdir, sha256_text(rel) + ".lock"), rel, mode)


def stat_sig(p):
    """(inode, size, mtime_ns) of p itself, or None when nothing is there.
    Every copy this tool installs is a freshly staged file linked into
    place, so a new inode; a signature that changed between push's read of
    the store copy (or pull's of the local file) and its locked write means
    another writer got there first."""
    try:
        st = os.lstat(p)
    except (FileNotFoundError, NotADirectoryError):  # a file where a directory of p should be
        return None
    return (st.st_ino, st.st_size, st.st_mtime_ns)


def full_sig(p):
    """F5 (Codex round 4): stat_sig() and the ctime, (inode, size,
    mtime_ns, ctime_ns) of p itself, or None when nothing is there. Every
    write, truncate, utime or chmod moves the ctime, so a rewrite that puts
    the old mtime back moves it too. It brackets a READ (hash_still()):
    link() and rename() move a file's ctime as well, so an identity check
    across this tool's own moves compares stat_sig()."""
    try:
        st = os.lstat(p)
    except (FileNotFoundError, NotADirectoryError):
        return None
    return (st.st_ino, st.st_size, st.st_mtime_ns, getattr(st, "st_ctime_ns", None))


def hash_still(p, tries=HASH_TRIES):
    """F5 (Codex round 4): (sha256, stat_sig) of p from a read across which
    its full_sig() held still, so the digest names the bytes that signature
    describes. A read that p moved under is made again, `tries` reads in
    all; None when p moved across every one; FileNotFoundError when p is
    gone. (Run 9's push took the store copy's signature again AFTER its
    read and compared inode and size only, so a same-size rewrite in place
    during the read became the baseline of every later check.)"""
    for _ in range(tries):
        before = full_sig(p)
        if before is None:
            raise FileNotFoundError(errno.ENOENT, "gone before it was read", p)
        digest = sha256(p)
        if full_sig(p) == before:
            return digest, before[:3]
    return None


def same_bytes(p, sha, sig):
    """F3 (Codex round 3): True when p, whose (inode, size, mtime) is now
    `sig`, is a regular file whose bytes hash to `sha` and whose signature
    held still while they were read (F5: its full signature, ctime
    included): only its signature moved since it was hashed (a touch, or
    the same bytes saved again). False for anything else, and when there
    is no digest to compare (no file was there)."""
    if sha is None or sig is None:
        return False
    try:
        if not stat.S_ISREG(os.lstat(p).st_mode):
            return False
        got = hash_still(p)
        return got is not None and got[0] == sha and got[1] == sig
    except OSError:
        return False


def copy_atomic(src, dst, root, mode, dst_sha=None, dst_sig=None, src_sha=None, src_bytes=None):
    """Stage src in a private .part beside dst, check that the staged copy
    holds the bytes the caller hashed and that dst is still the copy the
    caller read, displace an existing dst through quarantine() (v4 (6):
    never replaced in place), then install() the staged copy (round 2, F1:
    link(), never over a path). push calls it holding the key's lock.
    Returns the quarantine path or None. F6 (round 4): a src written while
    it is copied leaves a staged copy that is not the bytes push hashed and
    registers, so the staged copy must hash to `src_sha` and hold
    `src_bytes` bytes, checked before anything is quarantined or installed;
    else Changed (stage "source"). F3b (Codex round 3, ruled 2026-09-23):
    the copy can take minutes, and a writer that takes no lock (another
    Mac's Drive sync) may replace dst meanwhile, so once the staged copy is
    made and checked dst must still carry `dst_sig` (nothing there when
    that is None), or hold the bytes `dst_sha` names when only its
    signature moved, and the move is quarantine(strict=True). Raises
    Changed (stage "source", "copy" or "move") when the staged copy or dst
    is not what the caller read: nothing replaced or quarantined, the
    staged copy removed. Raises DestinationExists when a path is at dst by
    the time the staged copy is linked there: nothing is replaced, the
    staged copy is removed, and the displaced copy stays in the
    quarantine."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    tmp = private_name(dst, "part")
    try:
        shutil.copy2(src, tmp)
        if src_sha is not None and ((src_bytes is not None and os.path.getsize(tmp) != src_bytes)
                                    or sha256(tmp) != src_sha):
            raise Changed(src, "source")  # F6: src was written while it was copied
        now = stat_sig(dst)
        if now != dst_sig and not same_bytes(dst, dst_sha, now):
            raise Changed(dst, "copy")
        q = None
        if os.path.lexists(dst):
            q = quarantine(dst, root, mode, sha=dst_sha, sig=now, strict=True)
        try:
            install(tmp, dst)
        except FileExistsError:
            raise DestinationExists(q)
        return q
    finally:
        if os.path.lexists(tmp):  # every exit short of the install
            os.remove(tmp)


def stamp_store(store, sid):
    """F2 (Codex code audit, round 2): stamp an unstamped store for
    --init-store. <store>/.store_id is created with O_CREAT|O_EXCL, so an
    id that is there is never truncated, while holding
    <store>/.locks/store_id.lock (a FileLock, waited for up to
    REG_LOCK_WAIT), then read back and compared. An id there that is not
    `sid` (another initializer stamped first) is STORE ID CONFLICT: exit 2,
    no payload copied, the registry not written. The same id already there
    is not a conflict. Returns True when this run wrote the id. (Run 7's
    build wrote it with open("w"): two initializers each stamped, the
    later id replacing the earlier, and both exited 0.)"""
    idf = os.path.join(store, ".store_id")
    try:
        os.makedirs(store, exist_ok=True)
        lock = FileLock(os.path.join(store, LOCKS, STORE_ID_LOCK), ".store_id", "init-store",
                        wait=REG_LOCK_WAIT)
    except Locked as e:
        refuse(f"cannot stamp {store}: {e}. Nothing written.")
    except OSError as e:
        refuse(f"cannot stamp {store} as a new store: {oserr(e)}")
    wrote = False
    with lock:
        try:
            fd = os.open(idf, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            fd = None  # stamped meanwhile: read below
        except OSError as e:
            refuse(f"cannot stamp {store} as a new store: {oserr(e)}")
        if fd is not None:
            try:
                os.write(fd, sid.encode("utf-8"))
                os.fsync(fd)
                wrote = True
            except OSError as e:
                refuse(f"cannot write {idf}: {oserr(e)}. It may be left empty; remove it before "
                       f"--init-store again. No payload copied, registry not written.")
            finally:
                os.close(fd)
        try:
            with open(idf) as f:
                have = f.read().strip()
        except OSError as e:
            refuse(f"cannot read back {idf}: {oserr(e)}. No payload copied, registry not written.")
    if have != sid:
        if not have:
            how = ("the file is empty (a stamp that never finished, or one made by hand); remove "
                   "it only if nothing uses this store")
        elif wrote:
            how = "it replaced the id this run had just created"
        else:
            how = "another initializer stamped this store first"
        refuse(f"STORE ID CONFLICT. {idf} holds {have or '(nothing: an empty file)'}, not this "
               f"registry's {sid}: {how}. No payload copied, registry not written. Point "
               f"${SHELF_ENV} at the shelf this registry names, or merge-registry into "
               f"the registry that names this one.")
    return wrote


def entry_for(local, rel):
    if os.path.islink(local):
        return {"type": "symlink", "target": os.readlink(local)}
    return {"type": "file", "bytes": os.path.getsize(local),
            "mtime": int(os.path.getmtime(local)),
            "sha256": sha256(local)}


SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def entry_problem(ent):
    """The reason a registry line cannot be acted on, or None. pull and
    verify never stage, hash or link from a line that lacks what the step
    needs (a sha256 to check the staged copy against, the bytes to size
    the probe, a link target), so nothing half-done is left behind (a
    v4.0 pull staged first and died on ent["sha256"], leaving the .part)."""
    if not isinstance(ent, dict):
        return "not a mapping"
    kind = ent.get("type", "file")
    if kind == "symlink":
        if not isinstance(ent.get("target"), str) or not ent["target"]:
            return "symlink without a target"
        return None
    if kind != "file":
        return f"unknown type {kind!r}"
    sha = ent.get("sha256")
    if not isinstance(sha, str) or not SHA_RE.match(sha):
        return "no sha256" if sha is None else "malformed sha256"
    nbytes = ent.get("bytes")
    if isinstance(nbytes, bool) or not isinstance(nbytes, int) or nbytes < 0:
        return "no bytes" if nbytes is None else "malformed bytes"
    if ent.get("mtime") is not None and not isinstance(ent["mtime"], (int, float)):
        return "malformed mtime"
    return None


def base_of(rel):
    """The directory whose local walk is the evidence for `rel`: one of
    BASES when rel sits under it, else the blend's parent directory."""
    for b in base_prefixes():
        if rel.startswith(b + "/"):
            return b
    return os.path.dirname(rel)


def in_scope(base, only):
    """A base is inside --only's scope when the scope is empty, names the
    base, sits under it, or is a prefix of it."""
    return (not only) or base.startswith(only) or only == base or only.startswith(base + "/")


def symlink_loop(base):
    """(is_loop, target). A base that is a symlink resolving to itself or
    to a path inside itself: os.walk yields nothing, silently, and every
    registered file under it looks "gone"."""
    p = os.path.join(LOCAL, base)
    if not os.path.islink(p):
        return False, None
    target = os.readlink(p)
    canon = os.path.join(os.path.realpath(os.path.dirname(p)),
                         os.path.basename(p))
    resolved = os.path.realpath(os.path.join(os.path.dirname(p), target))
    return (resolved == canon or resolved.startswith(canon + os.sep)), target


def link_component(base):
    """The first component of `base`, walking down from the repo root,
    that is a symlink: (repo-relative path, link text), else (None, None)."""
    parts = base.split("/")
    for i in range(1, len(parts) + 1):
        rel = "/".join(parts[:i])
        p = os.path.join(LOCAL, rel)
        if os.path.islink(p):
            return rel, os.readlink(p)
    return None, None


def inside_checkout(real):
    """True when the real path `real` lies in THIS checkout: under the real
    repo root and not inside a nested checkout (a directory below the root
    carrying its own .git, as the lane worktrees under .claude/worktrees/
    do)."""
    if real != REPO_REAL and not real.startswith(REPO_REAL + os.sep):
        return False
    d = real
    while d != REPO_REAL:
        if os.path.lexists(os.path.join(d, ".git")):
            return False
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return True


def symlinked_outside(base):
    """C2(d). (link, target, checkout) when `base` resolves outside this
    checkout — through a symlink at the base itself or at any directory
    above it (blender/units -> <other>/blender/units), or into a nested
    checkout — the checkout being the one that really holds the base;
    else (None, None, None). realpath resolves what exists and keeps the
    rest, so a base that does not exist yet under a linked parent is
    judged by where a write would land."""
    real = os.path.realpath(os.path.join(LOCAL, base))
    if inside_checkout(real):
        return None, None, None
    link, target = link_component(base)
    if link is None:  # outside with no visible link (a mount): name the base
        link, target = base, real
    suffix = os.sep + os.path.join("shelf", "local", base.replace("/", os.sep))
    checkout = real[:-len(suffix)] if real.endswith(suffix) else os.path.dirname(real)
    return link, target, checkout


def base_status(base, cov):
    """(sound, label). sound only when the base is present locally, is a
    real directory (not a symlink), and yields files in covered(). Used
    by --prune for every base, gated or not."""
    p = os.path.join(LOCAL, base)
    n = sum(1 for k in cov if k.startswith(base + "/"))
    loop, target = symlink_loop(base)
    if loop:
        return False, f"SYMLINK LOOP -> {target}"
    if os.path.islink(p):
        return False, f"symlink -> {os.readlink(p)}"
    link, target, _checkout = symlinked_outside(base)
    if link is not None:
        return False, f"resolves outside this checkout via {link} -> {target}"
    if not os.path.isdir(p):
        return False, "missing locally"
    if n == 0:
        return False, "present but yields 0 covered files"
    return True, f"ok, {n} covered files"


def base_integrity(files, cov, only):
    """v3 gate, gated bases only (v4 C2(a)). For each gated base covered()
    walks: the registry holds N>0 entries under it but the local walk
    found 0 files -> BASE EMPTY. A symlink loop is named explicitly and
    treated as empty. Returns the number of empty bases inside the --only
    scope; bases outside it are printed as notices and not counted."""
    bad = 0
    for base, _inc, g in BASES:
        if not g:
            continue
        n_reg = sum(1 for k in files if k.startswith(base + "/"))
        if not n_reg:
            continue
        n_loc = sum(1 for k in cov if k.startswith(base + "/"))
        loop, target = symlink_loop(base)
        if loop:
            print(f"SYMLINK LOOP  {base} -> {target}")
        elif n_loc:
            continue
        scoped = in_scope(base, only)
        note = "" if scoped else f"  (outside --only '{only}'; not counted)"
        print(f"BASE EMPTY  {base}: registry={n_reg} local={n_loc}{note}")
        if scoped:
            bad += 1
    return bad


def only_filter(todo, only, extra=(), what="entries"):
    """A FILTER THAT MATCHES NOTHING MUST NOT REPORT A PASS.
    (2026-09-03, HERO-03 room: `--only hero03` — a name, not a path
    prefix — selected zero entries and printed "ok=0 ... problems=0",
    exit 0. That is precisely the class the Codex audit convicted this
    tool of: a green check that never touched the thing it certifies.
    It had survived inside the filter.) `extra` is the already-scoped
    list of prune candidates: a prune aimed at a folder that is gone
    locally selects nothing from the walk by definition (v3 refused it)."""
    if not only:
        return todo
    universe = len(todo)
    todo = [p for p in todo if p.startswith(only)]
    if not todo and not extra:
        refuse(f"--only '{only}' matched 0 of {universe} {what}. It is a "
               f"shelf-relative PATH PREFIX (e.g. '05 MARKETING/00 PRESS/POSTER'), "
               f"not a name. Refusing to report a pass on an empty selection.")
    return todo


def do_status(files, cov, only):
    """C2(b). Local only: registry keys against the local walk and
    lexists(). Never resolves the store, never opens a store file, never
    hashes (a present file is counted present, not verified)."""
    universe = sorted(set(files) | set(cov))
    todo = only_filter(universe, only)
    rows = {}

    def row(b):
        return rows.setdefault(b, [0, 0, 0, 0])  # registered present not_pulled unregistered

    bad = 0
    for rel in todo:
        if not safe_rel(rel):
            print(f"UNSAFE PATH (refused)  {rel}")
            bad += 1
            continue
        r = row(base_of(rel))
        if rel in files:
            r[0] += 1
            if os.path.lexists(os.path.join(LOCAL, rel)):
                r[1] += 1
            else:
                r[2] += 1
        else:
            r[3] += 1
    order = base_prefixes() + sorted(b for b in rows if b not in base_prefixes())
    tot = [0, 0, 0, 0]
    for b in order:
        if b not in rows and only:
            continue
        r = rows.get(b, [0, 0, 0, 0])
        if b in base_prefixes():
            cls = "gated" if gated(b) else "ungated"
            p = os.path.join(LOCAL, b)
            link, target, _checkout = symlinked_outside(b)
            if os.path.islink(p):
                cls += f", symlink -> {os.readlink(p)}"
            elif link is not None:
                cls += f", via symlink {link} -> {target} (outside this checkout)"
            elif not os.path.isdir(p):
                cls += ", absent locally"
        else:
            cls = "outside every base"
        print(f"STATUS  {b:<34} registered={r[0]:<6} present={r[1]:<6} "
              f"not_pulled={r[2]:<6} unregistered={r[3]:<6} {cls}")
        tot = [x + y for x, y in zip(tot, r)]
    store = os.environ.get(SHELF_ENV) or "(unresolved; status never touches the shelf)"
    print(f"SYNC|status|ok={tot[1]} copied=0 skipped=0 unregistered={tot[3]} "
          f"not_pulled={tot[2]} problems={bad}|registry={len(files)} store={store}")
    sys.exit(1 if bad else 0)


def norm_entry(e):
    """The fields of the registry contract; mtime is machine-local noise."""
    return (e.get("type", "file"), e.get("sha256"), e.get("bytes"), e.get("target"))


def merge_registry(other_path):
    """C2(c). Union by key into this checkout's registry. Any conflict
    (same key, different contract fields; an unsafe key; a different
    store_id) prints the diff and exits 2 with nothing written. The write
    is save_reg(strict): a key another run changed on disk while this one
    merged is a conflict too, and then nothing is written (R). F4 (round
    3, ruled 2026-09-23): a registry on either side that names no store
    (id_problem(); a bare 'files' mapping names none) is refused, exit 2,
    nothing written; run 8 compared the two ids only when both were
    non-empty, so such a registry merged into any other."""
    existed = os.path.exists(REG)
    reg = load_reg()
    base = snapshot(reg) if existed else None
    files = reg.setdefault("files", {})
    try:
        other = json.load(open(other_path))
    except (OSError, ValueError) as e:
        refuse(f"merge-registry: cannot read {other_path}: {e}")
    ofiles = other.get("files", other) if isinstance(other, dict) else None
    if not isinstance(ofiles, dict):
        refuse(f"merge-registry: {other_path} holds no 'files' mapping")
    for where, doc in ((REG, reg), (other_path, other)):
        how = id_problem(doc)
        if how:
            refuse(f"merge-registry: REGISTRY HAS NO STORE ID. {where} {how}: a merge is checked "
                   f"store id against store id, and a registry that names no store cannot be. "
                   f"Nothing written.")
    conflicts = []
    if other["store_id"] != reg["store_id"]:
        conflicts.append(("store_id", reg["store_id"], other["store_id"]))
    added = same = 0
    for k in sorted(ofiles):
        oe = ofiles[k]
        if not isinstance(oe, dict):
            refuse(f"merge-registry: {other_path} holds no usable 'files' mapping "
                   f"(entry {k!r} is a {type(oe).__name__}, not a mapping); nothing written.")
        if not safe_rel(k):
            conflicts.append((k, files.get(k), oe))
            print(f"UNSAFE PATH (refused)  {k}")
            continue
        me = files.get(k)
        if me is None:
            files[k] = oe
            added += 1
        elif isinstance(me, dict) and norm_entry(me) == norm_entry(oe):
            same += 1
        else:
            conflicts.append((k, me, oe))
    for k, me, oe in conflicts:
        print(f"MERGE CONFLICT  {k}\n  ours:   {json.dumps(me, sort_keys=True)}"
              f"\n  theirs: {json.dumps(oe, sort_keys=True)}")
    if conflicts:
        print(f"merge-registry REFUSED: {len(conflicts)} conflict(s) between "
              f"{REG} and {other_path}; nothing written.")
        sys.exit(2)
    try:
        late = save_reg(reg, base, strict=True)
    except OSError as e:
        refuse(f"merge-registry: {REG} not written: {oserr(e)}")
    for k, now, mine in late:
        print(f"MERGE CONFLICT  {k}  (changed on disk while merging)\n  on disk: "
              f"{json.dumps(now, sort_keys=True)}\n  theirs:  {json.dumps(mine, sort_keys=True)}")
    if late:
        print(f"merge-registry REFUSED: {len(late)} key(s) changed in {REG} while merging; "
              f"nothing written.")
        sys.exit(2)
    print(f"SYNC|merge-registry|added={added} same={same} conflicts=0"
          f"|registry={len(files)} other={other_path}")
    sys.exit(0)


def verify_store(copy, manifest_path, index_path, no_quarantine=False):
    """C2(e). The backup certificate: hash every file-typed manifest key
    at <copy>/<key>, then every INDEX.tsv line at <copy>/<quarantine
    path>. Reads nothing from the checkout. Refused (exit 2) before any
    hashing: a copy that is not a directory; a manifest or an explicit
    --index that cannot be read; a manifest whose 'files' mapping holds a
    value that is not a mapping, or no file-typed key (v4.0 died on
    e.get() with an AttributeError). Fix C (Codex code audit, 2026-09-23)
    adds three, because run 5's build certified what it never read: a
    manifest key, or a quarantine path on an INDEX line, that does not
    resolve (realpath) INSIDE the copy root, each named (copy=bin/hooks
    with the key ../../.gitignore hashed the checkout's own .gitignore and
    exited 0); a quarantine index that is missing or cannot be read (it
    used to count as quarantined_expected=0, exit 0), unless
    --no-quarantine says the copy carries none; and --no-quarantine given
    beside --index or beside an index the copy does carry. A copy file
    that cannot be read is a problem (UNREADABLE), never a traceback. F4
    (round 3, ruled 2026-09-23): a manifest that carries a store_id beside
    its 'files' mapping must name a store with it (id_problem(): null, ""
    and the like are refused); one that carries none, a bare 'files'
    excerpt, is still accepted, since the certificate is by hash."""
    if not os.path.isdir(copy):
        refuse(f"verify-store: {copy} is not a directory")
    try:
        with open(manifest_path) as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        refuse(f"verify-store: cannot read manifest {manifest_path}: {e}")
    if isinstance(data, dict) and "files" in data and "store_id" in data and id_problem(data):
        refuse(f"verify-store: REGISTRY HAS NO STORE ID. {manifest_path} {id_problem(data)}: a "
               f"frozen registry that names no store certifies no store's copy (a manifest that "
               f"carries no store_id at all, a bare 'files' excerpt, is accepted). Nothing read "
               f"from the copy.")
    man = data.get("files", data) if isinstance(data, dict) else None
    if not isinstance(man, dict):
        refuse(f"verify-store: {manifest_path} holds no 'files' mapping")
    odd = sorted(k for k, e in man.items() if not isinstance(e, dict))
    if odd:
        refuse(f"verify-store: {manifest_path} holds no usable 'files' mapping: "
               f"{len(odd)} entr{'y is' if len(odd) == 1 else 'ies are'} not a mapping "
               f"(first {odd[0]!r}, a {type(man[odd[0]]).__name__}). Nothing read from the copy.")
    keys = sorted(k for k, e in man.items() if e.get("type", "file") == "file")
    if not keys:
        refuse(f"verify-store: {manifest_path} names no file-typed key; refusing to "
               f"certify a copy against nothing.")
    root = os.path.realpath(copy)

    def outside(rel):
        """The real path `rel` reaches from the copy root when that is NOT
        inside the root (through '..', an absolute key, or a link in the
        copy that leads out), else None."""
        try:
            real = os.path.realpath(os.path.join(copy, rel))
        except ValueError:  # an embedded NUL byte
            return "(not a path)"
        return None if real.startswith(root + os.sep) else real

    out = [(k, outside(k)) for k in sorted(man)]
    out = [(k, real) for k, real in out if real is not None]
    for k, real in out:
        print(f"OUTSIDE THE COPY  {k} -> {real}")
    if out:
        refuse(f"verify-store: {len(out)} manifest key(s) do not resolve inside the copy "
               f"{root} (first {out[0][0]!r}); nothing read from the copy.")
    explicit = index_path is not None
    default = os.path.join(copy, QDIR, INDEX)
    lines = []
    if no_quarantine:
        if explicit:
            refuse("verify-store: --no-quarantine says the copy carries no quarantine index, "
                   "and --index names one; give one or the other.")
        if os.path.lexists(default):
            refuse(f"verify-store: --no-quarantine given, but the copy carries {default}; "
                   f"drop the flag to certify the versions it lists.")
    else:
        index_path = index_path or default
        if not explicit:
            real = outside(f"{QDIR}/{INDEX}")
            if real is not None:
                print(f"OUTSIDE THE COPY  {QDIR}/{INDEX} -> {real}")
                refuse(f"verify-store: the copy's quarantine index resolves outside the copy "
                       f"{root}; nothing read from the copy.")
        try:
            with open(index_path) as f:
                lines = [raw.rstrip("\n") for raw in f]
        except (OSError, ValueError) as e:
            refuse(f"verify-store: cannot read the quarantine index {index_path}: {oserr(e)}. "
                   f"A copy that carries no quarantine is certified only with --no-quarantine.")
    rows = [(line, line.split("\t")) for line in lines if line and not line.startswith("#")]
    qout = [(p[5], outside(p[5])) for _line, p in rows if len(p) == 6]
    qout = [(q, real) for q, real in qout if real is not None]
    for q, real in qout:
        print(f"QUARANTINE PATH OUTSIDE THE COPY  {q} -> {real}")
    if qout:
        refuse(f"verify-store: {len(qout)} quarantine path(s) in {index_path} do not resolve "
               f"inside the copy {root} (first {qout[0][0]!r}); nothing read from the copy.")
    expected, ok, missing, bad = len(keys), 0, 0, 0
    for k in keys:
        e = man[k]
        why = entry_problem(e)
        if why:
            print(f"BAD MANIFEST ENTRY ({why})  {k}")
            bad += 1
            continue
        p = os.path.join(copy, k)
        if not os.path.isfile(p):
            print(f"MISSING  {k}")
            missing += 1
            continue
        try:
            if os.path.getsize(p) != e["bytes"]:
                print(f"BAD (size)  {k}")
                bad += 1
                continue
            if sha256(p) != e["sha256"]:
                print(f"BAD (hash)  {k}")
                bad += 1
                continue
        except OSError as err:
            print(f"UNREADABLE ({oserr(err)})  {k}")
            bad += 1
            continue
        ok += 1
    qexp = qok = 0
    if no_quarantine:
        print("no quarantine index (--no-quarantine): no displaced version is certified")
    for line, parts in rows:
        qexp += 1
        if len(parts) != 6:
            print(f"BAD (index line)  {line}")
            bad += 1
            continue
        _utc, _mode, _rel, digest, _nbytes, qrel = parts
        p = os.path.join(copy, qrel)
        if not os.path.lexists(p):
            print(f"QUARANTINED MISSING  {qrel}")
            missing += 1
            continue
        try:
            got = sha256_text(os.readlink(p)) if os.path.islink(p) else sha256(p)
        except OSError as err:
            print(f"QUARANTINED UNREADABLE ({oserr(err)})  {qrel}")
            bad += 1
            continue
        if got != digest:
            print(f"QUARANTINED BAD (hash)  {qrel}")
            bad += 1
            continue
        qok += 1
    shown = "none (--no-quarantine)" if no_quarantine else index_path
    print(f"SYNC|verify-store|expected={expected} ok={ok} missing={missing} bad={bad} "
          f"quarantined_expected={qexp} quarantined_ok={qok}|copy={copy} manifest={manifest_path} "
          f"index={shown}")
    sys.exit(0 if (ok == expected and qok == qexp and missing == 0 and bad == 0) else 1)


def main():
    global BASES
    ap = argparse.ArgumentParser(
        description="the KILLER OF MEN shelf (a Drive folder), indexed in git, safely "
                    "(see the module docstring for the contract)")
    ap.add_argument("--version", action="version", version=f"sync_shelf {VERSION} (KOM build {KOM_BUILD})")
    ap.add_argument("mode", choices=["register", "push", "pull", "verify", "status",
                                     "merge-registry", "verify-store"])
    ap.add_argument("arg", nargs="?", metavar="PATH",
                    help="merge-registry: the other registry JSON. verify-store: "
                         "the root directory of the copy.")
    ap.add_argument("--only", metavar="PATH_PREFIX",
                    help="shelf-relative PATH PREFIX, e.g. '05 MARKETING/00 PRESS/POSTER'. A "
                         "prefix matching nothing is a refusal (exit 2), never a pass.")
    ap.add_argument("--deep", action="store_true",
                    help="verify: hash SHELF bytes in full, not just probe. register: hash "
                         "already-registered shelf copies too, not only their size")
    ap.add_argument("--strict", action="store_true",
                    help="verify: unregistered local files are problems too")
    ap.add_argument("--force", action="store_true",
                    help="push: replace a store copy that differs from the registry "
                         "or that this registry does not know (STORE CONFLICT); the "
                         "prior bytes go to the store's .quarantine/. Implies "
                         "--update. pull: overwrite a local file that is newer or "
                         "being written right now. register: re-register a shelf copy "
                         "that differs from its registry line (STORE DIFFERS FROM REGISTRY).")
    ap.add_argument("--update", action="store_true",
                    help="push: re-register a registered file whose local bytes "
                         "changed (LOCAL CHANGED); the store's prior bytes go to "
                         "its .quarantine/.")
    ap.add_argument("--init-store", action="store_true",
                    help="push, register: stamp a shelf directory that has no .store_id "
                         "(creating it if needed) with the id the registry names "
                         "(a registry naming none is refused, exit 2). Without it "
                         "an unstamped store is refused (exit 2).")
    ap.add_argument("--prune", action="store_true",
                    help="push: list registered entries absent from the local "
                         "walk (key, base directory, store presence) and "
                         "refuse (exit 2). With --yes, deregister those whose "
                         "base directory is present, a real directory, and "
                         "non-empty; the rest are skipped and printed. "
                         "Deregistration is never implied by local absence.")
    ap.add_argument("--yes", action="store_true",
                    help="push --prune: actually deregister the eligible "
                         "candidates.")
    ap.add_argument("--manifest", metavar="JSON",
                    help="verify-store: the frozen registry to certify the copy against")
    ap.add_argument("--index", metavar="TSV",
                    help="verify-store: a frozen .quarantine/INDEX.tsv (default: the "
                         "copy's own; a copy without one is refused unless --no-quarantine)")
    ap.add_argument("--no-quarantine", action="store_true",
                    help="verify-store: the copy carries no quarantine index; certify the "
                         "manifest keys only (refused beside --index, or when the copy "
                         "does carry an index)")
    a = ap.parse_args()

    # FLAG / MODE CONTRACT (v4 (4)): a flag on a mode it means nothing in
    # is a refusal, never a silent no-op. FLAG_MODES names the modes of
    # every flag (v4.0 checked five of the ten by hand; --deep, --strict
    # and --force passed silently on every other mode).
    unlisted = sorted(set(vars(a)) - set(FLAG_MODES) - {"mode", "arg"})
    if unlisted:
        refuse(f"internal: flag(s) {', '.join(unlisted)} missing from FLAG_MODES; "
               f"refusing rather than letting a flag go unchecked.")
    for dest, modes in FLAG_MODES.items():
        if getattr(a, dest) and a.mode not in modes:
            refuse(f"--{dest.replace('_', '-')} applies to {'/'.join(modes)} only, "
                   f"not {a.mode}. Nothing touched.")
    if a.yes and not a.prune:
        refuse("--yes means nothing without --prune.")
    if a.mode == "pull" and not a.only:
        # KOM build 1: the rule "never a bare pull" is enforced here, not by habit
        refuse("a bare pull is refused: name what a build needs, pull --only <shelf path>. "
               "The shelf is several GB and grows; nothing is pulled by default.")
    if a.mode in ("merge-registry", "verify-store"):
        if not a.arg:
            refuse(f"{a.mode} needs a path argument.")
    elif a.arg:
        refuse(f"{a.mode} takes no path argument (use --only PATH_PREFIX).")
    if a.mode == "verify-store":
        if not a.manifest:
            refuse("verify-store needs --manifest <frozen-registry.json>.")
        verify_store(a.arg, a.manifest, a.index, a.no_quarantine)  # exits; touches no checkout file
    if a.mode == "merge-registry":
        merge_registry(a.arg)  # exits; never resolves the store

    existed = os.path.exists(REG)
    reg = load_reg()
    # F4 (Codex round 3): a registry that names no store is refused before
    # the store is resolved or anything is read or written (run 8's
    # setdefault() here kept a null or "" id, and store_root() then
    # accepted a store stamped with any id). load_reg() gives a registry it
    # creates a new id.
    registry_id(reg)
    # save_reg()'s merge base (R): the registry as this push loaded it
    reg_base = snapshot(reg) if (existed and a.mode in ("push", "register")) else None
    files = reg.setdefault("files", {})
    BASES = discover_bases(files)
    cov = covered()
    covset = set(cov)
    if a.mode == "status":
        do_status(files, cov, a.only)  # exits; never resolves the store

    store, have_id = store_root(reg)  # refuses: no store, several, wrong id
    # UNSTAMPED STORE (v4 (2)): push never adopts a directory by accident.
    if a.mode in ("push", "register") and not have_id and not a.init_store:
        refuse(f"no .store_id at {store}; pass --init-store to stamp it as this registry's shelf")

    # SYMLINKED-BASE GUARD (v4 C2(d)): never write through a link into
    # another checkout. The REAL path of each in-scope base is judged, so
    # the link may sit at any component of it (blender/units ->
    # <other>/blender/units; v4.0 looked at the base alone and wrote
    # through). verify and status read through it.
    if a.mode in ("push", "pull"):
        linked = []
        for base in base_prefixes():
            if not in_scope(base, a.only):
                continue
            link, target, checkout = symlinked_outside(base)
            if link is not None:
                linked.append(base)
                via = "" if link == base else f" via {link}"
                print(f"SYMLINKED BASE  {base}{via} -> {target} resolves outside this "
                      f"checkout; run this command in {checkout}")
        if linked:
            refuse(f"{a.mode} REFUSED: {len(linked)} in-scope base(s) resolve through a "
                   f"symlink into another checkout. Nothing copied, registry untouched.")

    # BASE INTEGRITY GATE (v3, 2026-09-16 audit; gated bases only since
    # v4). Runs before anything is stamped, copied, or saved. A base that
    # walks to nothing while the registry holds entries under it is a
    # broken base, not a deletion.
    base_bad = 0
    if a.mode in ("push", "verify"):
        base_bad = base_integrity(files, covset, a.only)
        if a.mode == "push" and base_bad:
            print(f"push REFUSED: {base_bad} base(s) hold registered entries "
                  f"but yield 0 local files. Nothing copied, registry "
                  f"untouched. Repair the base, or --only a different base.")
            sys.exit(2)

    todo = cov if a.mode == "push" else sorted(files)
    if a.mode == "verify":
        todo = sorted(set(files) | covset)
    if a.mode == "register":
        todo = shelf_walk(store)
    cands = []
    if a.mode == "push" and a.prune:
        cands = [k for k in sorted(files) if k not in covset
                 and (not a.only or k.startswith(a.only))]
    todo = only_filter(todo, a.only, extra=cands,
                       what="shelf files" if a.mode == "register" else "entries")

    # The same guard key by key (push, pull): the directory of every
    # in-scope key this run would write is judged too, so a link BELOW a
    # base, or above a big blend that sits in no base, cannot carry a
    # write out of this checkout either. Unsafe keys keep their own
    # per-key refusal below.
    if a.mode in ("push", "pull"):
        outside = {}
        for d in sorted({os.path.dirname(k) for k in todo if safe_rel(k)}):
            link, target, checkout = symlinked_outside(d)
            if link is not None:
                outside.setdefault((link, target, checkout), []).append(d)
        for (link, target, checkout), dirs in sorted(outside.items()):
            print(f"SYMLINKED PATH  {link} -> {target} resolves outside this checkout "
                  f"({len(dirs)} key director{'y' if len(dirs) == 1 else 'ies'}, first "
                  f"{dirs[0]}); run this command in {checkout}")
        if outside:
            refuse(f"{a.mode} REFUSED: in-scope keys resolve through a symlink outside "
                   f"this checkout. Nothing copied, registry untouched.")

    # PRUNE (v3). Deregistration is an explicit, listed, confirmed act,
    # and only for candidates whose base directory is sound.
    prune_now, prune_skip = [], []
    if a.mode == "push" and a.prune:
        scope = f" under --only '{a.only}'" if a.only else ""
        print(f"prune: {len(cands)} registered entries absent from the "
              f"local walk{scope}")
        for k in cands:
            b = base_of(k)
            sound, label = base_status(b, covset)
            if not safe_rel(k):
                present = "unsafe path"
            elif os.path.lexists(os.path.join(store, k)):
                present = "present"
            else:
                present = "MISSING"
            print(f"  candidate  {k}\n             base={b} [{label}]  "
                  f"store={present}")
            (prune_now if sound else prune_skip).append((k, label))
        if cands and not a.yes:
            print(f"prune REFUSED: --prune only lists. Add --yes to "
                  f"deregister the {len(prune_now)} eligible candidate(s); "
                  f"{len(prune_skip)} would be skipped. Nothing copied, "
                  f"registry untouched.")
            sys.exit(2)

    # --init-store stamps only here, after every refusal above. v4.0
    # stamped before the --only and --prune refusals, so a refused run
    # could leave a store carrying an id that no registry holds.
    # F2: the id is created exclusively under the store's store_id lock and
    # read back (stamp_store); another id there is STORE ID CONFLICT, 2.
    if a.mode in ("push", "register") and not have_id:  # --init-store was given
        if stamp_store(store, reg["store_id"]):
            print(f"stamped new store {store} -> {reg['store_id']}")
        else:
            print(f"store {store} was stamped meanwhile with this registry's id "
                  f"{reg['store_id']}; nothing to stamp")

    ok = copied = unreg = skipped = not_pulled = 0
    bad = base_bad
    update = a.update or a.force

    def pull_lock(rel):
        """F1 (round 2): pull's per-key lock in this checkout
        (LOCAL_LOCKS), never waited for. None, with LOCKED printed and
        counted, when another run holds it."""
        nonlocal bad
        try:
            return KeyLock(LOCAL_LOCKS, rel, "pull")
        except Locked as e:
            print(f"LOCKED  {rel}  ({e}; nothing staged, local left as is)")
            bad += 1
            return None

    def dest_exists(rel, q):
        """The pull side's DESTINATION EXISTS line (F1)."""
        kept = f"; the displaced local is at {q}" if q else ""
        return (f"DESTINATION EXISTS  {rel}  (local: a file appeared at the key while this "
                f"pull held its lock; nothing replaced, nothing more quarantined{kept})")

    def one(rel):
        """The per-key work of push / pull / verify. Malformed state gets a
        labelled problem line here (v4 contract); an OSError nothing here
        foresaw propagates to the loop below, which labels it IO ERROR."""
        nonlocal ok, copied, unreg, skipped, not_pulled, bad
        if not safe_rel(rel):
            print(f"UNSAFE PATH (refused)  {rel}")
            bad += 1
            return
        local = os.path.join(LOCAL, rel)
        remote = os.path.join(store, rel)
        ent = files.get(rel)
        why = None if ent is None else entry_problem(ent)

        if a.mode == "register":
            # KOM build 1: adopt the shelf copy into the registry. Reads the shelf,
            # writes only the registry line; never copies, never touches shelf/local.
            if os.path.isdir(remote):
                print(f"STORE DIRECTORY at file key (refused)  {rel}")
                bad += 1
                return
            if ent is not None and why:
                if not a.force:
                    print(f"BAD REGISTRY ENTRY ({why})  {rel}  (nothing re-registered; "
                          f"--force replaces the line)")
                    bad += 1
                    return
                print(f"BAD REGISTRY ENTRY ({why})  {rel}  (--force: the line is replaced)")
                ent = None
            try:
                size = os.path.getsize(remote)
            except OSError as e:
                print(f"STORE UNREADABLE ({oserr(e)})  {rel}  (nothing registered)")
                bad += 1
                return
            if ent is not None and not a.deep:
                if size == ent["bytes"]:
                    ok += 1  # registered, and the shelf copy has the registered size
                    return
                print(f"STORE SIZE WRONG  {rel}  (registry {ent['bytes']} bytes, shelf {size}; "
                      f"nothing re-registered; --deep hashes it, --force re-registers)")
                bad += 1
                return
            try:
                got = shelf_hash(remote)
            except FileNotFoundError:
                print(f"STORE CHANGED DURING REGISTER  {rel}  (the shelf copy was moved while "
                      f"this run read it; nothing registered; run register again)")
                bad += 1
                return
            except OSError as e:
                print(f"STORE UNREADABLE ({oserr(e)})  {rel}  (nothing registered)")
                bad += 1
                return
            if got is None:
                print(f"STORE CHANGED DURING REGISTER  {rel}  (the shelf copy kept changing while "
                      f"this run read it; nothing registered; run register again)")
                bad += 1
                return
            digest, sig = got
            new = {"type": "file", "bytes": sig[1], "mtime": int(os.path.getmtime(remote)),
                   "sha256": digest}
            if ent is not None:
                if ent["sha256"] == digest and ent["bytes"] == new["bytes"]:
                    ok += 1
                    return
                if not a.force:
                    print(f"STORE DIFFERS FROM REGISTRY (hash)  {rel}  (registry "
                          f"{ent['sha256'][:12]}, shelf {digest[:12]}; nothing re-registered; "
                          f"--force re-registers the shelf's bytes)")
                    bad += 1
                    return
                files[rel] = new
                copied += 1
                print(f"re-registered (--force)  {rel}  (was {ent['sha256'][:12]}, now {digest[:12]})")
                return
            files[rel] = new
            copied += 1
            print(f"registered  {rel}  ({new['bytes']} bytes, {digest[:12]})")
            return

        if a.mode == "push":
            if why:
                # replacing a registry line is an explicit act, even a broken one
                if not a.force:
                    print(f"BAD REGISTRY ENTRY ({why})  {rel}  (nothing copied; "
                          f"--force replaces the line)")
                    bad += 1
                    return
                print(f"BAD REGISTRY ENTRY ({why})  {rel}  (--force: the line is replaced)")
                ent = None
            if os.path.islink(local):
                link = entry_for(local, rel)
                if ent is not None and (ent.get("type") != "symlink"
                                        or ent.get("target") != link["target"]):
                    # a retargeted link, or a registered file that has become
                    # a link: the registry line is replaced only by an explicit
                    # act, as in fix 2 (v4.0 re-recorded the link silently)
                    was = (f"registry -> {ent.get('target')}" if ent.get("type") == "symlink"
                           else "registry holds a file")
                    if not update:
                        print(f"LINK CONFLICT  {rel}  (local -> {link['target']}; {was}; "
                              f"registry unchanged; --update re-registers)")
                        bad += 1
                        return
                    print(f"re-registered link ({'--force' if a.force else '--update'})  "
                          f"{rel} -> {link['target']}  (was: {was})")
                files[rel] = link
                ok += 1
                return
            try:
                new = entry_for(local, rel)
            except OSError as e:
                print(f"LOCAL UNREADABLE ({oserr(e)})  {rel}  (nothing copied)")
                bad += 1
                return
            # One lstat gives presence and identity together: the locked
            # write below proceeds only while <store>/<rel> is still what
            # was read here (fix L).
            sig = stat_sig(remote)
            has_store = sig is not None and os.path.exists(remote)
            if has_store and os.path.isdir(remote):
                print(f"STORE DIRECTORY at file key (refused)  {rel}")
                bad += 1
                return
            # Fix S (Codex code audit; C1(5) as the plan wrote it): the store
            # copy is hashed whenever one exists, an unchanged local file
            # included. Run 5's build skipped this when the local matched the
            # registry and the store copy had the registered size, so a
            # same-sized corrupt store copy passed with exit 0. F5 (Codex
            # round 4): the read counts only when the copy's full signature
            # (inode, size, mtime, ctime) held still across it, and every
            # later check compares with that signature; a copy that moved is
            # read again, three reads in all (hash_still). Run 9 took the
            # signature again after the read and compared inode and size
            # only, so a same-size rewrite in place during the read passed
            # every later check and was quarantined under the digest read
            # before it. One read per push while nothing moves.
            store_sha = None
            if has_store:
                try:
                    got = hash_still(remote)
                except FileNotFoundError:
                    print(f"STORE CHANGED DURING PUSH  {rel}  (the store copy was moved while "
                          f"this push read it; nothing copied; run push again)")
                    bad += 1
                    return
                except OSError as e:
                    print(f"STORE UNREADABLE ({oserr(e)})  {rel}  (nothing copied)")
                    bad += 1
                    return
                if got is None:
                    print(f"STORE CHANGED DURING PUSH  {rel}  (the store copy kept changing while "
                          f"this push read it: its inode, size, mtime or ctime moved during each of "
                          f"{HASH_TRIES} reads; nothing copied, nothing displaced; run push again)")
                    bad += 1
                    return
                store_sha, sig = got
            if has_store and store_sha == new["sha256"]:
                if ent is None:
                    # a key this registry does not know whose store bytes
                    # already ARE the local bytes: nothing would be
                    # replaced, so the line is adopted without a copy
                    files[rel] = new
                    print(f"registered (store already holds these bytes)  {rel}")
                elif ent.get("sha256") != new["sha256"]:
                    # registry X, local Y, store Y: the line is the only
                    # pointer to X, and replacing it is an explicit act
                    # (v4 (5)/(8); v4.0 re-registered X -> Y here silently)
                    if not a.force:
                        print(f"STORE CONFLICT (hash)  {rel}  (store copy differs from the "
                              f"registry and equals the local file; nothing done; "
                              f"--force re-registers)")
                        bad += 1
                        return
                    files[rel] = new
                    print(f"re-registered (--force; the store already holds these "
                          f"bytes, nothing displaced)  {rel}")
                ok += 1
                return
            if has_store and (ent is None or store_sha != ent.get("sha256")):
                # v4 (5) STORE CONFLICT (hash): bytes this registry does not know.
                if not a.force:
                    reason = ("not in this registry" if ent is None
                              else "differs from the registry")
                    print(f"STORE CONFLICT (hash)  {rel}  (store copy {reason}; "
                          f"nothing copied; --force replaces it after quarantine)")
                    bad += 1
                    return
                mode = "push-force"
            elif ent is not None and ent.get("sha256") != new["sha256"]:
                # v4 (8) LOCAL CHANGED: the registry line is the only pointer
                # to the prior bytes; replacing it is an explicit act.
                if not update:
                    where = ("store copy matches the registry" if has_store
                             else "store holds no copy")
                    print(f"LOCAL CHANGED since registration  {rel}  ({where}; "
                          f"nothing copied; --update re-registers after quarantine)")
                    bad += 1
                    return
                mode = "push-update"
            else:
                mode = "push"  # a new key, or a registered file the store lacks
            # Fix L: the write runs under the key's lock, and only while the
            # store copy is the one hashed above (none, if there was none).
            try:
                lock = KeyLock(os.path.join(store, LOCKS), rel, mode)
            except Locked as e:
                print(f"LOCKED  {rel}  ({e}; nothing copied)")
                bad += 1
                return
            with lock:
                if stat_sig(remote) != sig:
                    print(f"STORE CHANGED DURING PUSH  {rel}  (another writer changed the "
                          f"store copy after this push read it; nothing copied; run push again)")
                    bad += 1
                    return
                try:
                    q = copy_atomic(local, remote, store, mode, dst_sha=store_sha, dst_sig=sig,
                                    src_sha=new["sha256"], src_bytes=new["bytes"])
                except Changed as e:
                    if e.stage == "source":
                        # F6: the local file was written while push copied it
                        print(f"LOCAL CHANGED DURING PUSH  {rel}  (the local file changed while "
                              f"this push copied it: the staged copy is not the bytes this push "
                              f"hashed; the staged copy discarded, the store copy untouched, nothing "
                              f"quarantined; run push again)")
                        bad += 1
                        return
                    # F3b: the store copy changed while this push copied the local
                    # file into its staged .part, or at the move itself
                    when = ("while this push staged its copy" if e.stage == "copy"
                            else "as this push moved it to the quarantine")
                    print(f"STORE CHANGED DURING PUSH  {rel}  (another writer changed the store "
                          f"copy {when}; the staged copy discarded, nothing replaced; run push "
                          f"again)")
                    bad += 1
                    return
                except DestinationExists as r:
                    kept = f"; the prior copy is at {r.quarantined}" if r.quarantined else ""
                    print(f"DESTINATION EXISTS  {rel}  (store: a file appeared at the key while "
                          f"this push held its lock; nothing replaced, nothing more "
                          f"quarantined{kept})")
                    bad += 1
                    return
                if sha256(remote) != new["sha256"]:
                    print(f"POST-COPY HASH MISMATCH  {rel}")
                    bad += 1
                    return
            files[rel] = new
            copied += 1
            print(f"push  {rel}" + (f"  (prior store bytes -> {q})" if q else ""))
            return

        if a.mode == "pull":
            if why:
                print(f"BAD REGISTRY ENTRY ({why})  {rel}  (nothing staged; local left as is)")
                bad += 1
                return
            if ent.get("type") == "symlink":
                sig = stat_sig(local)  # re-checked under the key's lock (F1)
                if os.path.islink(local) and os.readlink(local) == ent["target"]:
                    ok += 1
                    return
                if os.path.isdir(local) and not os.path.islink(local):
                    print(f"DIRECTORY at symlink-typed key (refused)  {rel}")
                    bad += 1
                    return
                os.makedirs(os.path.dirname(local), exist_ok=True)
                lock = pull_lock(rel)
                if lock is None:
                    return
                with lock:
                    if stat_sig(local) != sig:
                        if os.path.islink(local) and os.readlink(local) == ent["target"]:
                            ok += 1  # another pull linked it meanwhile
                            return
                        print(f"LOCAL CHANGED DURING PULL  {rel}  (the local path changed after "
                              f"this pull read it; nothing replaced; run pull again)")
                        bad += 1
                        return
                    q = None
                    if os.path.lexists(local):
                        # v4 (7): never os.remove a regular file (round-1 finding 17);
                        # F3: strict, so only the object just checked is moved
                        try:
                            q = quarantine(local, LOCAL, "pull-symlink-key", sig=sig, strict=True)
                        except Changed:
                            print(f"LOCAL CHANGED DURING PULL  {rel}  (the local path changed as "
                                  f"this pull moved it to the quarantine; nothing replaced; run "
                                  f"pull again)")
                            bad += 1
                            return
                    try:
                        os.symlink(ent["target"], local)  # EEXIST, never over a path (F1)
                    except FileExistsError:
                        print(dest_exists(rel, q))
                        bad += 1
                        return
                copied += 1
                print(f"pull  {rel} -> {ent['target']}"
                      + (f"  (displaced local -> {q})" if q else ""))
                return
            if os.path.isdir(local):
                what = "SYMLINK TO DIRECTORY" if os.path.islink(local) else "DIRECTORY"
                print(f"{what} at file key (refused)  {rel}")
                bad += 1
                return
            sig = stat_sig(local)  # re-checked under the key's lock (F1) and after staging (F3)
            have = None  # the local bytes' sha256, when there is a file to read
            if os.path.exists(local):
                try:
                    have = sha256(local)
                except OSError as e:
                    print(f"LOCAL UNREADABLE ({oserr(e)})  {rel}  (left as is)")
                    bad += 1
                    return
                if have == ent["sha256"]:
                    ok += 1
                    return
            if not os.path.exists(remote):
                print(f"MISSING IN STORE  {rel}")
                bad += 1
                return
            if os.path.isdir(remote):
                print(f"STORE DIRECTORY at file key (refused)  {rel}")
                bad += 1
                return
            # LIVE-WRITE GUARD (2026-09-03, from the HERO/shelving room):
            # a working scene changes several times an hour, so the store
            # is stale between saves BY DESIGN. Never hand a builder an
            # older file over their newer one, and never touch a file
            # being written this minute. Announcements are not a guard.
            if os.path.exists(local) and not a.force:
                lm = os.path.getmtime(local)
                if time.time() - lm < 120:
                    print(f"BEING WRITTEN (skipped; --force overrides)  {rel}")
                    skipped += 1
                    return
                if ent.get("mtime") and lm > ent["mtime"] + 1:
                    print(f"LOCAL IS NEWER than the store (skipped; push it "
                          f"or --force to overwrite)  {rel}")
                    skipped += 1
                    return
            os.makedirs(os.path.dirname(local), exist_ok=True)
            # F1 (round 2): stage, displace and install only while holding
            # the key's lock in this checkout, and only while the local file
            # is still the one examined above.
            lock = pull_lock(rel)
            if lock is None:
                return
            with lock:
                if stat_sig(local) != sig:
                    if (os.path.isfile(local) and not os.path.islink(local)
                            and sha256(local) == ent["sha256"]):
                        ok += 1  # another pull installed it meanwhile
                        return
                    print(f"LOCAL CHANGED DURING PULL  {rel}  (the local file changed after "
                          f"this pull read it; nothing staged, nothing replaced; run pull again)")
                    bad += 1
                    return
                tmp = private_name(local, "part")
                try:
                    try:
                        shutil.copy2(remote, tmp)
                    except OSError as e:
                        if e.filename != remote:
                            raise
                        print(f"STORE UNREADABLE ({oserr(e)})  {rel}  (local left intact)")
                        bad += 1
                        return
                    if sha256(tmp) != ent["sha256"]:
                        print(f"STORE BYTES BAD, local left intact  {rel}")
                        bad += 1
                        return
                    # F3 (Codex round 3): the copy above can take minutes, and a
                    # writer that takes no lock (an editor saving) may have changed
                    # the local file meanwhile. Only the bytes examined above are
                    # displaced: the signature again, then the sha256 when only the
                    # signature moved (a touch).
                    now = stat_sig(local)
                    if now != sig and not same_bytes(local, have, now):
                        print(f"LOCAL CHANGED DURING PULL  {rel}  (the local file changed while "
                              f"this pull staged the store copy; the staged copy discarded, "
                              f"nothing replaced; run pull again)")
                        bad += 1
                        return
                    q = None
                    if os.path.lexists(local):
                        # v4 (7): a versioned name, never the fixed .quarantine/<rel>
                        # (round-2 finding 1: the second pull erased the first).
                        # F3: the digest just checked goes with it, so nothing reads
                        # the file between the check and the move, and the move is
                        # strict: only the file checked is moved
                        try:
                            q = quarantine(local, LOCAL, "pull", sha=have, sig=now, strict=True)
                        except Changed:
                            print(f"LOCAL CHANGED DURING PULL  {rel}  (the local file changed as "
                                  f"this pull moved it to the quarantine; the staged copy "
                                  f"discarded, nothing replaced; run pull again)")
                            bad += 1
                            return
                        print(f"quarantined differing local -> {q}")
                    try:
                        install(tmp, local)  # F1: link(), never over a path
                    except FileExistsError:
                        print(dest_exists(rel, q))
                        bad += 1
                        return
                finally:
                    if os.path.lexists(tmp):  # every exit short of the install
                        os.remove(tmp)
            copied += 1
            print(f"pull  {rel}")
            return

        # verify — checks BOTH sides
        if ent is None:
            print(f"UNREGISTERED  {rel}")
            unreg += 1
            if a.strict:
                bad += 1
            return
        if why:
            print(f"BAD REGISTRY ENTRY ({why})  {rel}")
            bad += 1
            return
        if ent.get("type") == "symlink":
            if os.path.islink(local) and os.readlink(local) == ent["target"]:
                ok += 1
            elif not os.path.lexists(local) and not gated(base_of(rel)):
                # v4 C2(a): a registered link absent from an ungated base is
                # not pulled yet, like a file (v4.0 counted it a problem)
                print(f"NOT PULLED  {rel}")
                not_pulled += 1
            else:
                print(f"SYMLINK DIFFERS/MISSING  {rel}")
                bad += 1
            return
        if not os.path.exists(local):
            if not gated(base_of(rel)):
                # v4 C2(a): legitimately absent from a sparse checkout
                print(f"NOT PULLED  {rel}")
                not_pulled += 1
                return
            print(f"LOCAL MISSING  {rel}")
            bad += 1
            return
        if os.path.isdir(local):
            what = "SYMLINK TO DIRECTORY" if os.path.islink(local) else "DIRECTORY"
            print(f"{what} at file key  {rel}")
            bad += 1
            return
        try:
            have = sha256(local)
        except OSError as e:
            print(f"LOCAL UNREADABLE ({oserr(e)})  {rel}")
            bad += 1
            return
        if have != ent["sha256"]:
            print(f"LOCAL DIFFERS  {rel}")
            bad += 1
            return
        if not os.path.exists(remote):
            print(f"STORE MISSING  {rel}")
            bad += 1
            return
        if os.path.isdir(remote):
            print(f"STORE DIRECTORY at file key  {rel}")
            bad += 1
            return
        if os.path.getsize(remote) != ent["bytes"]:
            print(f"STORE SIZE WRONG  {rel}")
            bad += 1
            return
        if a.deep:
            try:
                got = sha256(remote)
            except OSError as e:
                print(f"STORE UNREADABLE ({oserr(e)})  {rel}")
                bad += 1
                return
            if got != ent["sha256"]:
                print(f"STORE BYTES BAD  {rel}")
                bad += 1
                return
        elif not readable(remote, ent["bytes"]):
            print(f"STORE UNREADABLE (placeholder?)  {rel}")
            bad += 1
            return
        ok += 1

    for rel in todo:
        try:
            one(rel)
        except OSError as e:
            # the backstop (v4 contract): an OSError no check in one()
            # foresaw is one labelled problem on one key, never a traceback;
            # a staged .part was already removed where it was made
            print(f"IO ERROR ({oserr(e)})  {rel}")
            bad += 1

    if a.mode in ("push", "register"):
        # v3: NO implicit prune. Local absence is never evidence. Only
        # --prune --yes deregisters, and only candidates whose base
        # directory is sound (see base_status); the rest are printed.
        if a.mode == "push" and a.prune and a.yes:
            for k, label in prune_skip:
                print(f"prune SKIPPED ({label})  {k}")
            for k, _label in prune_now:
                del files[k]
                print(f"deregistered (--prune --yes)  {k}")
        try:
            late = save_reg(reg, reg_base)
        except OSError as e:
            print(f"REGISTRY NOT WRITTEN ({oserr(e)})  {REG}")
            bad += 1
        else:
            for k, now, mine in late:
                print(f"REGISTRY CONFLICT  {k}  (another run in this checkout recorded "
                      f"{brief(now)} after this {a.mode} read the registry; this {a.mode}'s "
                      f"{brief(mine)} is not recorded; the line on disk is kept; run {a.mode} again)")
                bad += 1
    depth = "deep" if a.deep else "probe"
    print(f"SYNC|{a.mode}{'/' + depth if a.mode == 'verify' else ''}|"
          f"ok={ok} copied={copied} skipped={skipped} unregistered={unreg} "
          f"not_pulled={not_pulled} problems={bad}"
          f"|registry={len(files)} store={store}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
