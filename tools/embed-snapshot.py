#!/usr/bin/env python3
"""Embed data.json into index.html's snapshot block. Run from site/ before committing index.html."""
import json, re
data = open("data.json").read()
json.loads(data)  # sanity
html = open("index.html").read()
new = re.sub(r'(<script id="snapshot" type="application/json">).*?(</script>)',
             lambda m: m.group(1) + data.replace("</", "<\\/") + m.group(2),
             html, count=1, flags=re.S)
assert new != html or data in html, "snapshot block not found"
open("index.html", "w").write(new)
print("embedded", len(data), "bytes")
