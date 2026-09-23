# LEDGER — one ledger for KILLER OF MEN, and where every handoff came from

*2026-09-23. The repo's `handoffs/` (this directory) is the canonical ledger. The Drive folder `My Drive/KILLER OF MEN/HANDOFFS/` was a second one, kept by hand since September 8; this file records how the two were reconciled and what the Drive folder is from now on.*

## The rule

1. **Canonical: `handoffs/` in git.** A handoff exists when it is committed and pushed. Nothing else counts.
2. **One counter for everyone.** `handoffs/handoff-NNN-<lane>.md`; NNN = the highest number anywhere + 1, whatever the lane. "Anywhere" is measured, not remembered: every local and remote branch, the `handoffs/` of every other checkout on this Mac (an uncommitted handoff already holds its number), and the Drive folder. `bin/hooks/kom-session-start.sh` prints the next number when a session opens; `bin/hooks/kom-stop.sh` prints it when a turn ends and names a collision when it sees one; `bin/kom-check.sh` prints it on demand; `bin/githooks/pre-commit` refuses a commit that reuses a number already on `origin/main`.
3. **The test must stop the write.** Before writing: `[ -e handoffs/handoff-NNN-lane.md ] && exit 1` (or `set -o noclobber`). A warning that does not stop the write is decoration (the September 10 double 107, README.txt on the Drive).
4. **The Drive `HANDOFFS/` folder is a mirror, not a ledger.** Copying a handoff there is optional and harmless; nothing reads it except the number check above. Nothing is ever deleted from it.
5. **Never `git add -A`, never `git stash`, never `git reset`:** other sessions share these checkouts. Add by path.

## The reconciliation of 2026-09-23

Measured by md5 over every file in both places, before anything was copied. Two lanes did the fold-in on the same day from the same base commit (785ddf0): this lane (setup) and the EPK lane (its handoff-128-epk, branch `claude/vigorous-mayer-7773b9`). The copies are byte-identical in both branches, so they merge without conflict.

| File | Where it was | What was done | Now |
|---|---|---|---|
| `handoff-104-festival.md` | Drive only | copied verbatim into `handoffs/` | both, identical |
| `handoff-105-festival.md` | Drive only | copied verbatim into `handoffs/` | both, identical |
| `handoff-082-festival.md` | untracked in the `main` checkout on this Mac (`$HOME/Code/kom-festival-board`), never committed, not on the Drive | copied verbatim into `handoffs/`; the EPK lane copied it onto the Drive | both, identical |
| `handoff-083-connectors.md` | same | same | both, identical |
| `handoff-084-bio.md` | same (Sep 21, the cinematographer-bio interview, round 1 of 3) | same | both, identical |
| `handoff-100-epk.md`, `102-epk`, `106-epk`, `109-epk`, `109-festival` | repo only | the EPK lane copied them onto the Drive | both, identical |
| `handoff-128-epk.md` | the EPK lane's branch and the Drive | not on this branch; arrives with that branch's merge | Drive and its branch |
| every other `handoff-001` to `handoff-127` and `HARNESS-epk.md` | both | nothing: byte-identical already | both, identical |
| `handoff-067-epk.md` | both | the copy in the `main` checkout (at 9ba0bca, behind origin) differs from the Drive's and this branch's; the branch's is the newer text | both, identical on this branch |

After the fold-in: numbers 001 to 128 are all present; the repo holds 163 handoff files on this branch plus `HARNESS-epk.md`, the Drive 164 (it has 128-epk). The Drive's `README.txt` (the rule as the EPK lane wrote it on September 8, with the September 10 amendment) stays there unchanged.

## Numbers that exist twice (history, not to be repaired)

Before the shared counter, lanes counted separately. These numbers carry two files with different lane suffixes; the files do not collide and none was renamed:

| Numbers | Lanes |
|---|---|
| 030 to 048 | docket, festival |
| 062 to 072 | epk, festival |
| 082, 083, 084 | epk; festival, connectors, bio |
| 105, 109 | epk, festival |
| 110 | cast, epk |

From 111 on, every number is unique. The pre-commit guard keeps it that way for new numbers on `origin/main`.
