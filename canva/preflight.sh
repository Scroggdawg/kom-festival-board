#!/usr/bin/env bash
# Pre-flight for the Canva build. Run from the repo root BEFORE any Canva step.
# Checks what a machine can check, then lists what only Luke can provide.
# Exit 0 = machine checks pass; the Luke items are printed regardless and must be
# confirmed with him in conversation before step 3 of canva/README.md.
set -u
ok()   { printf '  ok       %s\n' "$1"; }
fail() { printf '  MISSING  %s\n' "$1"; FAILED=1; }
FAILED=0
echo "== Machine checks"
[ -f canva/README.md ] && ok "repo root (canva/README.md present)" || fail "run this from the repo root: cd .../kom-festival-board"
command -v node >/dev/null && [[ "$(node -v)" == v24* ]] && ok "node $(node -v)" || fail "Node 24 (have: $(node -v 2>/dev/null || echo none)); install from https://nodejs.org"
command -v npm  >/dev/null && ok "npm $(npm -v)" || fail "npm"
[ -x venv/bin/python ] && venv/bin/python -c "import reportlab, PIL, pypdf, pymupdf, fontTools" 2>/dev/null && ok "venv with reportlab, pillow, pypdf, pymupdf, fonttools" || fail "venv: python3 -m venv venv && venv/bin/pip install -r tools/requirements.txt"
[ -f /System/Library/Fonts/Supplemental/Baskerville.ttc ] && ok "Baskerville.ttc (the kit measures text with it)" || fail "Baskerville.ttc not found; the emitter's measurements will differ on this machine"
[ -d canva/kom-epk-builder/node_modules ] && ok "app dependencies installed" || fail "app deps: (cd canva/kom-epk-builder && npm ci)"
[ -f canva/ops/epk-canva.json ] && ok "ops contract present ($(python3 -c "import json;d=json.load(open('canva/ops/epk-canva.json'));print(len(d['pages']),'pages, epk rev',d['source']['epk_rev'])" 2>/dev/null))" || fail "ops contract: venv/bin/python tools/build-epk-canva.py"
code=$(curl -s -o /dev/null -w '%{http_code}' https://scroggdawg.github.io/kom-festival-board/canva/ops/epk-canva.json); [ "$code" = "200" ] && ok "GitHub Pages serves the ops contract (200)" || fail "GitHub Pages returned $code for the ops contract; push and wait a minute"
code=$(curl -s -o /dev/null -w '%{http_code}' https://scroggdawg.github.io/kom-festival-board/press/assets/derived/canva/p03-e01.jpg); [ "$code" = "200" ] && ok "GitHub Pages serves the derivatives (200)" || fail "GitHub Pages returned $code for a derivative image"
git remote get-url origin >/dev/null 2>&1 && ok "git remote: $(git remote get-url origin)" || fail "git remote origin"
if command -v gh >/dev/null && gh auth status >/dev/null 2>&1; then ok "GitHub auth present (can push progress)"; else printf '  NOTE     no GitHub auth on this machine: progress can be recorded locally but not pushed until Luke signs in (gh auth login)\n'; fi
[ -f canva/STATE.json ] && ok "STATE.json present; next_step: $(python3 -c "import json;print(json.load(open('canva/STATE.json'))['next_step'][:110])" 2>/dev/null)" || fail "canva/STATE.json"
echo
echo "== Ask Luke, and wait for each answer, before step 3 (nothing inside Canva can start without them)"
echo "  1. Is the Claude in Chrome extension signed in to THIS Claude account? (It pairs with one account. If not, sign it in first.)"
echo "  2. Which Chrome is logged in to Canva Pro? (The session must ask, then Luke clicks Connect in that Chrome when prompted.)"
echo "  3. Is Luke at the keyboard for the Developer Portal's Developer Terms click? (His click, not the agent's.)"
echo "  4. Confirm the standing decisions in canva/STATE.json still hold (tier Pro, Libre Baskerville at build, Canva master after acceptance, editor-driving OK)."
echo
[ "$FAILED" = 0 ] && echo "Machine checks: PASS. Now ask the four questions above." || echo "Machine checks: FAIL. Fix the MISSING lines, re-run, then ask the four questions."
exit $FAILED
