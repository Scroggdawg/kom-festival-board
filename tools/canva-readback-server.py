#!/usr/bin/env python3
"""Receive the Canva app's read-back as JSON on disk.

    python3 tools/canva-readback-server.py [DIR]      (default canva/readback/)

The app's "Read design (openDesign)" posts {scope, at, pages[{index, count, elements[{type,
top, left, width, height, text?}]}]} to http://localhost:8787/readback after every read; this
writes it to DIR/<UTC>.json and DIR/latest.json. The panel is a cross-origin iframe, so the
JSON it shows cannot be read from outside; this is how the design's wording (Luke edits it in
the editor, and his edits win) is mirrored back into press/epk.json with tools/epk.py set.
Localhost only; no auth; run it while reading, stop it after.
"""
import datetime, os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "canva", "readback")


class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0)); body = self.rfile.read(n)
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        os.makedirs(OUT, exist_ok=True)
        for name in (f"{stamp}.json", "latest.json"):
            open(os.path.join(OUT, name), "wb").write(body)
        print(f"received {n} bytes -> {os.path.relpath(os.path.join(OUT, stamp + '.json'), ROOT)}", flush=True)
        self.send_response(200); self._cors(); self.send_header("Content-Type", "application/json"); self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"listening on http://localhost:8787/readback -> {OUT}", flush=True)
    HTTPServer(("127.0.0.1", 8787), H).serve_forever()
