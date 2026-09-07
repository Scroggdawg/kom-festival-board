#!/usr/bin/env python3
"""Serves the repo root and accepts status clicks from docket.html.

  docket_server.py [port]      default 8642, binds 127.0.0.1

GET  /...      static files (json and html sent with no-store)
GET  /status   last push result
POST /set      {"id": "D.1.1", "status": "started"} → writes via todo.py, returns the new document
POST /push     push now (writes are otherwise pushed a few seconds after the last click)

Writes go through tools/todo.py, so the browser and the command line share one writer.
"""
import json, os, sys, threading, time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import todo

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8642
LOCK = threading.Lock(); PUSH_AT = [0.0]; PUSH_LOG = {"last": "", "at": ""}
OK_HOSTS = {f"localhost:{PORT}", f"127.0.0.1:{PORT}"}
OK_ORIGINS = {f"http://localhost:{PORT}", f"http://127.0.0.1:{PORT}"}
DELAY = 4  # seconds of quiet before pushing, so a burst of clicks is one commit

def pusher():
    while True:
        time.sleep(1)
        if PUSH_AT[0] and time.time() >= PUSH_AT[0]:
            PUSH_AT[0] = 0.0
            try:
                with LOCK: PUSH_LOG["last"] = todo.push()
            except Exception as e: PUSH_LOG["last"] = f"push failed: {e}"
            PUSH_LOG["at"] = todo.now()
            print(PUSH_LOG["at"], PUSH_LOG["last"], flush=True)

class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=todo.ROOT, **k)
    def end_headers(self):
        if self.path.split("?")[0].endswith((".json", ".html")): self.send_header("Cache-Control", "no-store")
        super().end_headers()
    def reply(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def local_only(self):
        """Refuse cross-origin and rebound-DNS posts: this server takes no credentials."""
        if (self.headers.get("Host") or "").lower() not in OK_HOSTS: return False
        origin = self.headers.get("Origin")
        return origin is None or origin in OK_ORIGINS
    def do_GET(self):
        if self.path.split("?")[0] == "/status": return self.reply(200, {"push": PUSH_LOG, "pending": bool(PUSH_AT[0])})
        super().do_GET()
    def do_POST(self):
        path = self.path.split("?")[0]
        if not self.local_only(): return self.reply(403, {"error": "this server only accepts posts from its own page"})
        try: body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        except ValueError: return self.reply(400, {"error": "bad json"})
        if path == "/set":
            try:
                with LOCK:
                    d = todo.load()
                    changed = todo.set_status(d, str(body.get("id")), str(body.get("status")), by="docket.html")
                    if changed: todo.save(d, "docket.html")
                if changed: PUSH_AT[0] = time.time() + DELAY
                return self.reply(200, {"rev": d["rev"], "changed": changed, "data": d})
            except (KeyError, ValueError) as e: return self.reply(400, {"error": str(e)})
        if path == "/push":
            PUSH_AT[0] = time.time(); return self.reply(200, {"queued": True})
        self.reply(404, {"error": "no such route"})
    def log_message(self, fmt, *a):
        if self.command == "POST": super().log_message(fmt, *a)

if __name__ == "__main__":
    threading.Thread(target=pusher, daemon=True).start()
    print(f"docket server on http://127.0.0.1:{PORT}/docket.html serving {todo.ROOT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
