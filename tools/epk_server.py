#!/usr/bin/env python3
"""Serves the EPK worksheet and accepts edits from epk.html.

  epk_server.py [port]      default 8643, binds 127.0.0.1

GET  /...      static files from the clone (json and html sent with no-store)
GET  /status   the last push result and whether one is pending
POST /set      {"id","value","prev"} → compare-and-set through epk.py, returns the document
POST /push     publish now (an edit otherwise publishes a few seconds later)

Every write goes through tools/epk.py. A background loop pulls origin every 20 s, so a
value saved from the published page shows up here without anyone asking.
"""
import json, os, sys, threading, time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import epk

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8643
LOCK = threading.RLock()
PUSH_AT = [0.0]
STATE = {"push": "", "pushAt": "", "pull": "", "pullAt": ""}
OK_HOSTS = {f"localhost:{PORT}", f"127.0.0.1:{PORT}"}
OK_ORIGINS = {f"http://localhost:{PORT}", f"http://127.0.0.1:{PORT}"}
PUSH_DELAY = 4      # seconds of quiet before publishing, so a burst of edits is one commit
PULL_EVERY = 20     # seconds between checks for someone else's writes


def worker():
    last_pull = 0.0
    while True:
        time.sleep(1)
        now = time.time()
        if PUSH_AT[0] and now >= PUSH_AT[0]:
            PUSH_AT[0] = 0.0
            try:
                with LOCK:
                    STATE["push"] = epk.push()
            except Exception as e:
                STATE["push"] = f"push failed: {e}"
            STATE["pushAt"] = epk.now()
            print(STATE["pushAt"], "push:", STATE["push"], flush=True)
            last_pull = now
        elif not PUSH_AT[0] and now - last_pull >= PULL_EVERY:
            last_pull = now
            try:
                with LOCK:
                    r = epk.pull()
            except Exception as e:
                r = f"pull failed: {e}"
            STATE["pull"] = r
            STATE["pullAt"] = epk.now()
            if r not in ("current", "local change pending"):
                print(STATE["pullAt"], "pull:", r, flush=True)


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=epk.ROOT, **k)

    def end_headers(self):
        if self.path.split("?")[0].endswith((".json", ".html")):
            self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def reply(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def local_only(self):
        """This server takes no credentials, so refuse anything not from its own page:
        blocks a rebound hostname and a form post from another site."""
        if (self.headers.get("Host") or "").lower() not in OK_HOSTS:
            return False
        origin = self.headers.get("Origin")
        return origin is None or origin in OK_ORIGINS

    def do_GET(self):
        if self.path.split("?")[0] == "/status":
            return self.reply(200, dict(STATE, pending=bool(PUSH_AT[0])))
        super().do_GET()

    def do_POST(self):
        path = self.path.split("?")[0]
        if not self.local_only():
            return self.reply(403, {"error": "this server only answers its own page"})
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        except ValueError:
            return self.reply(400, {"error": "bad json"})
        if path == "/set":
            try:
                with LOCK:
                    d = epk.load()
                    changed = epk.set_value(d, str(body.get("id")), body.get("value") or "",
                                            by="epk.html", expect=body.get("prev"))
                    if changed:
                        epk.save(d, "epk.html")
                if changed:
                    PUSH_AT[0] = time.time() + PUSH_DELAY
                return self.reply(200, {"rev": d["rev"], "changed": changed, "data": d})
            except epk.Conflict as e:
                with LOCK:
                    d = epk.load()
                return self.reply(409, {"error": str(e), "data": d})
            except (KeyError, ValueError) as e:
                return self.reply(400, {"error": str(e)})
        if path == "/push":
            PUSH_AT[0] = time.time()
            return self.reply(200, {"queued": True})
        self.reply(404, {"error": "no such route"})

    def log_message(self, fmt, *a):
        if self.command == "POST":
            super().log_message(fmt, *a)


if __name__ == "__main__":
    if not epk.DEDICATED:
        print(f"refusing: {epk.ROOT} is not the epk clone (no .epk-clone marker)", file=sys.stderr)
        sys.exit(1)
    threading.Thread(target=worker, daemon=True).start()
    print(f"epk server on http://127.0.0.1:{PORT}/epk.html serving {epk.ROOT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
