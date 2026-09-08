#!/usr/bin/env python3
"""Embed data.json into board.html's snapshot block. Run from the repo root before committing board.html.

The board moved from index.html to board.html on Sep 8, 2026, when index.html became the
campaign dashboard. This script targets board.html; pointed at index.html it fails the
assert rather than writing, but it would not do its job."""
import json, re
data = open("data.json").read()
json.loads(data)  # sanity
html = open("board.html").read()
new = re.sub(r'(<script id="snapshot" type="application/json">).*?(</script>)',
             lambda m: m.group(1) + data.replace("</", "<\\/") + m.group(2),
             html, count=1, flags=re.S)
assert new != html or data in html, "snapshot block not found"
open("board.html", "w").write(new)
print("embedded", len(data), "bytes")
