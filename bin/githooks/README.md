# githooks — the tracked git hooks for this repo

Install once per clone (the config is not tracked; `bin/kom-check.sh` reports whether it is set):

```bash
git config core.hooksPath bin/githooks
```

`pre-commit` REJECTS, printing `REJECT <path>: <rule>` and exiting 1: a staged blob over 50 MB (SIZE); an `.env`-named or CLAUDE-PRIVATE-CONTEXT file, only `.env.example` allowed (SECRET); a NEW `handoffs/handoff-NNN-<lane>.md` whose NNN already exists in that ledger directory on `origin/main` or in the index, any lane (HANDOFF); a NEW line in a staged `.py`/`.sh`/`.ts`/`.json` carrying a `/Users/` literal outside a comment or docstring (HOMEPATH). Everything else passes in well under a second.

HOMEPATH is a documented heuristic, not a parser: only added lines are read; a line is skipped when its stripped form starts with `#`, `//`, `*` or `/*`, when the literal sits after a trailing `#` (.py/.sh) or `//` (.ts), and, for `.py` only, when the line is inside a `"""`/`'''` string of the STAGED file or itself contains a triple quote. HANDOFF never fetches, so `origin/main` is as fresh as your last pull; with no `origin/main` ref that half is skipped and says so.

Files already in history are not re-judged: twelve behind-the-scenes JPEGs between 18 and 53 MB were committed under `press/assets/BTS/` before this hook existed (RUNBOOK.md §8 lists them). The hook stops the next one.

The Claude hooks in `.claude/settings.json` (session start, prompt, stop) are separate: they remind; this one refuses. Codex and any other tool that commits gets this one only.

Proven 2026-09-23 in a scratch repo (transcript in `bin/hooks/FALSIFY-kom-stop.md`, its last section): a 60 MB blob, a colliding handoff number against a fake `origin/main`, two handoffs staged with one number, `/Users/` in code vs a comment vs a docstring, `.env` vs `.env.example`, and a timed normal commit.
