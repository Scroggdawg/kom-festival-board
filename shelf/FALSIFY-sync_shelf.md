# FALSIFY-sync_shelf — recorded run of shelf/test-sync_shelf.sh

Tool under test: shelf/sync_shelf.py, sha256 `61f461331d13dd4ee769b9877a58ba53f8ed63b793dd4aacbb6cd17e05eefbe7` (2247 lines), `--version` prints `sync_shelf 4 (KOM build 1)`. Harness sha256 `5796a21d999d41aa068356dec0f0ecdfa90589a4523d3241420948736e3caecc`. Run 2026-09-23T23:27:06Z on Darwin 25.4.0, Python 3.14.7.

Result: PASS 91  FAIL 0; harness exit 0 (0 = every check passed).

Sections, in transcript order:

- A: the scratch shelf, unstamped, holding four files (two covered, a .DS_Store, a .gdoc)
- 1: register on an unstamped shelf without --init-store — expect exit 2, no .store_id, no registry
- 2: register --init-store — expect the stamp, two lines registered with the independent hashes, the .DS_Store and .gdoc skipped
- 3: register again — expect ok=2 copied=0, registry unchanged
- 4: --only that matches nothing — expect exit 2, never a pass
- 5: the shelf copy of poster.jpg rewritten in place, same size, other bytes — register (size only) passes it, --deep catches it, --force re-registers
- 6: status never touches the shelf (KOM_SHELF pointed at a path that does not exist)
- 7: a bare pull is refused (KOM build 1 enforces the rule)
- 8: pull --only the poster — expect the local copy with the registered hash; a second pull is ok=1
- 9: the local poster edited, dated 5 minutes ago — pull skips it (LOCAL IS NEWER); --force displaces it to the quarantine, listed in INDEX.tsv, never deleted
- 10: verify --deep --strict over the press base — the certificate form: ok=1 (poster pulled), not_pulled=1 (frame), unregistered=0 problems=0
- 11: push a new local file into EPK BUILDS — registered and on the shelf; a shelf copy changed behind the registry is STORE CONFLICT until --force, which quarantines it on the shelf
- 12: a shelf stamped with another id — every mode that opens the shelf refuses (WRONG STORE), nothing touched
- 13: a flag on a mode it means nothing in — refused, exit 2
- 14: no shelf at all (KOM_SHELF unset, no Drive glob match under a scratch HOME) — exit 2 naming KOM_SHELF
- 15: a local base that is a symlink out of the checkout — pull refuses (SYMLINKED BASE), nothing written through it
- 16: merge-registry — a second checkout's registry (one new key) merges; a conflicting line refuses with nothing written
- 17: nothing this run deleted — every byte version that existed is still on disk (in place or in a quarantine)
- R: the real shelf, read-only — with no registry id to match, the tool must refuse before touching it; no .store_id is created there
- no Traceback in any output of this run

Method: a scratch checkout holds a copy of the tool (so its checkout, local mirror and registry resolve into the scratch directory) and $KOM_SHELF names a scratch shelf; every command runs unpiped, its exit code read on its own line; assertions are on printed state (sha256 of both sides, registry lines, quarantine names, INDEX.tsv, the SYNC line last), never on the exit code alone. The real shelf is read once (section R) and must be refused; nothing is written there. Re-run: `bash shelf/test-sync_shelf.sh --record shelf/FALSIFY-sync_shelf.md`.

```text
test-sync_shelf.sh — 2026-09-23T23:27:06Z — Python 3.14.7 — tool sha256 61f461331d13 — sync_shelf 4 (KOM build 1)
scratch: $SCRATCH (under $TMPDIR); KOM_SHELF=$SCRATCH/shelf; the checkout under test is $SCRATCH/co
== A: the scratch shelf, unstamped, holding four files (two covered, a .DS_Store, a .gdoc) ==
  independent sha256: poster f6f48e1d5356f242cc6cec0796728e292f35bd92e072e252cfe5cbcd49678aad
  independent sha256: frame  ee6458bfe0233501a732e79b9756893926856613976f8111d754f68f4f91a1a3
== 1: register on an unstamped shelf without --init-store — expect exit 2, no .store_id, no registry ==
$ python3 $SCRATCH/co/shelf/sync_shelf.py register --only 05 MARKETING/00 PRESS
  sync_shelf: no .store_id at $SCRATCH/shelf; pass --init-store to stamp it as this registry's shelf
$ echo $?
2
  PASS  exit 2 (refused)
  PASS  names --init-store
  PASS  no .store_id created
  PASS  no registry written
== 2: register --init-store — expect the stamp, two lines registered with the independent hashes, the .DS_Store and .gdoc skipped ==
$ python3 $SCRATCH/co/shelf/sync_shelf.py register --only 05 MARKETING/00 PRESS --init-store
  stamped new store $SCRATCH/shelf -> d1cfb3dd-be5d-4f05-898b-0ae2d463ad16
  registered  05 MARKETING/00 PRESS/BTS/day 3/frame (1).jpg  (30000 bytes, ee6458bfe023)
  registered  05 MARKETING/00 PRESS/POSTER/poster.jpg  (20000 bytes, f6f48e1d5356)
  SYNC|register|ok=0 copied=2 skipped=0 unregistered=0 not_pulled=0 problems=0|registry=2 store=$SCRATCH/shelf
$ echo $?
0
  PASS  exit 0
  PASS  SYNC line is last
  PASS  summary: copied=2 (two lines written) problems=0
  PASS  .store_id written and equals the registry's store_id
  PASS  registry holds exactly 2 keys
  PASS  poster.jpg registered with the independent sha256
  PASS  frame (1).jpg (a space, parentheses, a subfolder with a space) registered with the independent sha256
  PASS  bytes recorded (20000)
  PASS  .DS_Store not registered
  PASS  .gdoc not registered (a Drive shortcut, not bytes)
  PASS  shelf/local untouched (register never copies)
  PASS  the store_id lock released
== 3: register again — expect ok=2 copied=0, registry unchanged ==
$ python3 $SCRATCH/co/shelf/sync_shelf.py register --only 05 MARKETING/00 PRESS
  SYNC|register|ok=2 copied=0 skipped=0 unregistered=0 not_pulled=0 problems=0|registry=2 store=$SCRATCH/shelf
$ echo $?
0
  PASS  exit 0
  PASS  ok=2 copied=0
  PASS  registry file byte-identical
== 4: --only that matches nothing — expect exit 2, never a pass ==
$ python3 $SCRATCH/co/shelf/sync_shelf.py register --only 05 MARKETING/00 PRESS/NOPE
  sync_shelf: --only '05 MARKETING/00 PRESS/NOPE' matched 0 of 2 shelf files. It is a shelf-relative PATH PREFIX (e.g. '05 MARKETING/00 PRESS/POSTER'), not a name. Refusing to report a pass on an empty selection.
$ echo $?
2
  PASS  exit 2
  PASS  says it matched 0
== 5: the shelf copy of poster.jpg rewritten in place, same size, other bytes — register (size only) passes it, --deep catches it, --force re-registers ==
$ python3 $SCRATCH/co/shelf/sync_shelf.py register --only 05 MARKETING/00 PRESS/POSTER
  SYNC|register|ok=1 copied=0 skipped=0 unregistered=0 not_pulled=0 problems=0|registry=2 store=$SCRATCH/shelf
$ echo $?
0
  PASS  size-only register: exit 0 (a registered key counted ok by size)
$ python3 $SCRATCH/co/shelf/sync_shelf.py register --only 05 MARKETING/00 PRESS/POSTER --deep
  STORE DIFFERS FROM REGISTRY (hash)  05 MARKETING/00 PRESS/POSTER/poster.jpg  (registry f6f48e1d5356, shelf 26dd636aad38; nothing re-registered; --force re-registers the shelf's bytes)
  SYNC|register|ok=0 copied=0 skipped=0 unregistered=0 not_pulled=0 problems=1|registry=2 store=$SCRATCH/shelf
$ echo $?
1
  PASS  --deep: exit 1 (a problem)
  PASS  --deep: STORE DIFFERS FROM REGISTRY
  PASS  --deep: registry line unchanged
$ python3 $SCRATCH/co/shelf/sync_shelf.py register --only 05 MARKETING/00 PRESS/POSTER --deep --force
  re-registered (--force)  05 MARKETING/00 PRESS/POSTER/poster.jpg  (was f6f48e1d5356, now 26dd636aad38)
  SYNC|register|ok=0 copied=1 skipped=0 unregistered=0 not_pulled=0 problems=0|registry=2 store=$SCRATCH/shelf
$ echo $?
0
  PASS  --force: exit 0
  PASS  --force: re-registered line
  PASS  --force: registry now names the new bytes
== 6: status never touches the shelf (KOM_SHELF pointed at a path that does not exist) ==
$ env KOM_SHELF=$SCRATCH/does-not-exist python3 $SCRATCH/co/shelf/sync_shelf.py status
  STATUS  05 MARKETING/00 PRESS              registered=2      present=0      not_pulled=2      unregistered=0      ungated, absent locally
  STATUS  05 MARKETING/07 FESTIVALS          registered=0      present=0      not_pulled=0      unregistered=0      ungated, absent locally
  STATUS  DELIVERY                           registered=0      present=0      not_pulled=0      unregistered=0      ungated, absent locally
  STATUS  HANDOFFS                           registered=0      present=0      not_pulled=0      unregistered=0      ungated, absent locally
  SYNC|status|ok=0 copied=0 skipped=0 unregistered=0 not_pulled=2 problems=0|registry=2 store=$SCRATCH/does-not-exist
$ echo $?
0
  PASS  exit 0
  PASS  registered=2 not_pulled=2 for the press base
  PASS  SYNC line: not_pulled=2
== 7: a bare pull is refused (KOM build 1 enforces the rule) ==
$ python3 $SCRATCH/co/shelf/sync_shelf.py pull
  sync_shelf: a bare pull is refused: name what a build needs, pull --only <shelf path>. The shelf is several GB and grows; nothing is pulled by default.
$ echo $?
2
  PASS  exit 2
  PASS  says --only
  PASS  nothing pulled
== 8: pull --only the poster — expect the local copy with the registered hash; a second pull is ok=1 ==
$ python3 $SCRATCH/co/shelf/sync_shelf.py pull --only 05 MARKETING/00 PRESS/POSTER
  pull  05 MARKETING/00 PRESS/POSTER/poster.jpg
  SYNC|pull|ok=0 copied=1 skipped=0 unregistered=0 not_pulled=0 problems=0|registry=2 store=$SCRATCH/shelf
$ echo $?
0
  PASS  exit 0
  PASS  local copy hashes to the registry
  PASS  the frame (not asked for) is not pulled
$ python3 $SCRATCH/co/shelf/sync_shelf.py pull --only 05 MARKETING/00 PRESS/POSTER
  SYNC|pull|ok=1 copied=0 skipped=0 unregistered=0 not_pulled=0 problems=0|registry=2 store=$SCRATCH/shelf
$ echo $?
0
  PASS  second pull: ok=1 copied=0
== 9: the local poster edited, dated 5 minutes ago — pull skips it (LOCAL IS NEWER); --force displaces it to the quarantine, listed in INDEX.tsv, never deleted ==
$ python3 $SCRATCH/co/shelf/sync_shelf.py pull --only 05 MARKETING/00 PRESS/POSTER
  LOCAL IS NEWER than the store (skipped; push it or --force to overwrite)  05 MARKETING/00 PRESS/POSTER/poster.jpg
  SYNC|pull|ok=0 copied=0 skipped=1 unregistered=0 not_pulled=0 problems=0|registry=2 store=$SCRATCH/shelf
$ echo $?
0
  PASS  exit 0 with skipped=1
  PASS  says LOCAL IS NEWER
  PASS  the edited local file is untouched
$ python3 $SCRATCH/co/shelf/sync_shelf.py pull --only 05 MARKETING/00 PRESS/POSTER --force
  quarantined differing local -> .quarantine/05 MARKETING/00 PRESS/POSTER/poster.jpg.20260923T232707Z.a23a346a52be
  pull  05 MARKETING/00 PRESS/POSTER/poster.jpg
  SYNC|pull|ok=0 copied=1 skipped=0 unregistered=0 not_pulled=0 problems=0|registry=2 store=$SCRATCH/shelf
$ echo $?
0
  PASS  --force: exit 0
  PASS  --force: the local copy is the registry's bytes again
  quarantine path: .quarantine/05 MARKETING/00 PRESS/POSTER/poster.jpg.20260923T232707Z.a23a346a52be
  PASS  the edited bytes are in shelf/local/.quarantine under a versioned name
  PASS  INDEX.tsv lists it with its sha256
== 10: verify --deep --strict over the press base — the certificate form: ok=1 (poster pulled), not_pulled=1 (frame), unregistered=0 problems=0 ==
$ python3 $SCRATCH/co/shelf/sync_shelf.py verify --only 05 MARKETING/00 PRESS --deep --strict
  NOT PULLED  05 MARKETING/00 PRESS/BTS/day 3/frame (1).jpg
  SYNC|verify/deep|ok=1 copied=0 skipped=0 unregistered=0 not_pulled=1 problems=0|registry=2 store=$SCRATCH/shelf
$ echo $?
0
  PASS  exit 0
  PASS  summary reads ok=1 ... not_pulled=1 problems=0
  PASS  the frame is NOT PULLED, not a problem
== 11: push a new local file into EPK BUILDS — registered and on the shelf; a shelf copy changed behind the registry is STORE CONFLICT until --force, which quarantines it on the shelf ==
$ python3 $SCRATCH/co/shelf/sync_shelf.py push --only 05 MARKETING/00 PRESS/EPK BUILDS
  push  05 MARKETING/00 PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf
  SYNC|push|ok=0 copied=1 skipped=0 unregistered=0 not_pulled=0 problems=0|registry=3 store=$SCRATCH/shelf
$ echo $?
0
  PASS  exit 0
  PASS  copied=1
  PASS  shelf copy hashes to the local file
  PASS  registered
  PASS  registry holds 3 keys
$ python3 $SCRATCH/co/shelf/sync_shelf.py push --only 05 MARKETING/00 PRESS/EPK BUILDS
  STORE CONFLICT (hash)  05 MARKETING/00 PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf  (store copy differs from the registry; nothing copied; --force replaces it after quarantine)
  SYNC|push|ok=0 copied=0 skipped=0 unregistered=0 not_pulled=0 problems=1|registry=3 store=$SCRATCH/shelf
$ echo $?
1
  PASS  shelf copy changed by another writer: exit 1
  PASS  STORE CONFLICT (hash), nothing copied
  PASS  the foreign shelf bytes untouched
$ python3 $SCRATCH/co/shelf/sync_shelf.py push --only 05 MARKETING/00 PRESS/EPK BUILDS --force
  push  05 MARKETING/00 PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf  (prior store bytes -> .quarantine/05 MARKETING/00 PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf.20260923T232707Z.b620951e4cfd)
  SYNC|push|ok=0 copied=1 skipped=0 unregistered=0 not_pulled=0 problems=0|registry=3 store=$SCRATCH/shelf
$ echo $?
0
  PASS  --force: exit 0
  PASS  --force: the shelf holds the local bytes again
  shelf quarantine path: .quarantine/05 MARKETING/00 PRESS/EPK BUILDS/KillerOfMen_EPK_test.pdf.20260923T232707Z.b620951e4cfd
  PASS  the foreign bytes are in the shelf's .quarantine, never deleted
  PASS  the shelf's INDEX.tsv lists them
== 12: a shelf stamped with another id — every mode that opens the shelf refuses (WRONG STORE), nothing touched ==
$ env KOM_SHELF=$SCRATCH/other-shelf python3 $SCRATCH/co/shelf/sync_shelf.py verify --only 05 MARKETING/00 PRESS
  sync_shelf: WRONG STORE. registry expects d1cfb3dd-be5d-4f05-898b-0ae2d463ad16, $SCRATCH/other-shelf carries ffffffff-0000-0000-0000-000000000000. Refusing to touch it.
$ echo $?
2
  PASS  verify --only '05 MARKETING/00 PRESS': exit 2
  PASS  verify: says WRONG STORE
$ env KOM_SHELF=$SCRATCH/other-shelf python3 $SCRATCH/co/shelf/sync_shelf.py register --only 05 MARKETING/00 PRESS
  sync_shelf: WRONG STORE. registry expects d1cfb3dd-be5d-4f05-898b-0ae2d463ad16, $SCRATCH/other-shelf carries ffffffff-0000-0000-0000-000000000000. Refusing to touch it.
$ echo $?
2
  PASS  register --only '05 MARKETING/00 PRESS': exit 2
  PASS  register: says WRONG STORE
$ env KOM_SHELF=$SCRATCH/other-shelf python3 $SCRATCH/co/shelf/sync_shelf.py pull --only 05 MARKETING/00 PRESS/POSTER
  sync_shelf: WRONG STORE. registry expects d1cfb3dd-be5d-4f05-898b-0ae2d463ad16, $SCRATCH/other-shelf carries ffffffff-0000-0000-0000-000000000000. Refusing to touch it.
$ echo $?
2
  PASS  pull --only '05 MARKETING/00 PRESS/POSTER': exit 2
  PASS  pull: says WRONG STORE
$ env KOM_SHELF=$SCRATCH/other-shelf python3 $SCRATCH/co/shelf/sync_shelf.py push --only 05 MARKETING/00 PRESS/POSTER
  sync_shelf: WRONG STORE. registry expects d1cfb3dd-be5d-4f05-898b-0ae2d463ad16, $SCRATCH/other-shelf carries ffffffff-0000-0000-0000-000000000000. Refusing to touch it.
$ echo $?
2
  PASS  push --only '05 MARKETING/00 PRESS/POSTER': exit 2
  PASS  push: says WRONG STORE
  PASS  the other shelf's id untouched
== 13: a flag on a mode it means nothing in — refused, exit 2 ==
$ python3 $SCRATCH/co/shelf/sync_shelf.py status --deep
  sync_shelf: --deep applies to verify/register only, not status. Nothing touched.
$ echo $?
2
  PASS  status --deep: exit 2
$ python3 $SCRATCH/co/shelf/sync_shelf.py register --only 05 MARKETING/00 PRESS --update
  sync_shelf: --update applies to push only, not register. Nothing touched.
$ echo $?
2
  PASS  register --update: exit 2
$ python3 $SCRATCH/co/shelf/sync_shelf.py verify --only 05 MARKETING/00 PRESS --init-store
  sync_shelf: --init-store applies to push/register only, not verify. Nothing touched.
$ echo $?
2
  PASS  verify --init-store: exit 2
== 14: no shelf at all (KOM_SHELF unset, no Drive glob match under a scratch HOME) — exit 2 naming KOM_SHELF ==
$ env -u KOM_SHELF HOME=$SCRATCH/home python3 $SCRATCH/co/shelf/sync_shelf.py verify --only 05 MARKETING/00 PRESS
  sync_shelf: no shelf. Set $KOM_SHELF, or sign Drive for desktop in as camerawrap@gmail.com so that '~/Library/CloudStorage/GoogleDrive-*/My Drive/KILLER OF MEN' exists.
$ echo $?
2
  PASS  exit 2
  PASS  names $KOM_SHELF
== 15: a local base that is a symlink out of the checkout — pull refuses (SYMLINKED BASE), nothing written through it ==
$ python3 $SCRATCH/co/shelf/sync_shelf.py register --only DELIVERY
  registered  DELIVERY/master.mov  (5000 bytes, 770beb781db8)
  SYNC|register|ok=0 copied=1 skipped=0 unregistered=0 not_pulled=0 problems=0|registry=4 store=$SCRATCH/shelf
$ echo $?
0
  PASS  DELIVERY registered
$ python3 $SCRATCH/co/shelf/sync_shelf.py pull --only DELIVERY
  SYMLINKED BASE  DELIVERY -> $SCRATCH/elsewhere resolves outside this checkout; run this command in $SCRATCH
  sync_shelf: pull REFUSED: 1 in-scope base(s) resolve through a symlink into another checkout. Nothing copied, registry untouched.
$ echo $?
2
  PASS  exit 2
  PASS  SYMLINKED BASE named
  PASS  nothing written into the link's target
== 16: merge-registry — a second checkout's registry (one new key) merges; a conflicting line refuses with nothing written ==
$ python3 $SCRATCH/co/shelf/sync_shelf.py merge-registry $SCRATCH/other.json
  SYNC|merge-registry|added=1 same=0 conflicts=0|registry=5 other=$SCRATCH/other.json
$ echo $?
0
  PASS  exit 0, added=1
  PASS  registry holds 5 keys
$ python3 $SCRATCH/co/shelf/sync_shelf.py merge-registry $SCRATCH/conflict.json
  MERGE CONFLICT  HANDOFFS/handoff-999-test.md
    ours:   {"bytes": 3, "mtime": 0, "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "type": "file"}
    theirs: {"bytes": 3, "mtime": 0, "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb", "type": "file"}
  merge-registry REFUSED: 1 conflict(s) between $SCRATCH/co/shelf/registry.json and $SCRATCH/conflict.json; nothing written.
$ echo $?
2
  PASS  conflict: exit 2
  PASS  MERGE CONFLICT printed
  PASS  registry byte-identical (nothing written)
== 17: nothing this run deleted — every byte version that existed is still on disk (in place or in a quarantine) ==
  PASS  the original poster bytes (v1) were replaced in place by this harness, not by the tool; the tool's displaced versions: edited local -> quarantine
  PASS  foreign shelf pdf -> shelf quarantine
  PASS  no .part left anywhere
  PASS  no lock left anywhere
== R: the real shelf, read-only — with no registry id to match, the tool must refuse before touching it; no .store_id is created there ==
$ env -u KOM_SHELF HOME=$HOME python3 $SCRATCH/fresh/shelf/sync_shelf.py register --only 05 MARKETING/00 PRESS
  sync_shelf: no .store_id at $HOME/Library/CloudStorage/GoogleDrive-camerawrap@gmail.com/My Drive/KILLER OF MEN; pass --init-store to stamp it as this registry's shelf
$ echo $?
2
  PASS  a fresh registry against the real shelf without --init-store: exit 2
  PASS  the real shelf is unstamped: the refusal names --init-store, and no .store_id appeared
  PASS  no registry written in the fresh checkout
== no Traceback in any output of this run ==
  PASS  0 tracebacks
== summary: PASS 91  FAIL 0 ==
harness exit:
0
```
