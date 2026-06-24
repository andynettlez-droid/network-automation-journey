#!/usr/bin/env python3
"""
serve-lesson.py — local server for the lesson player's AI features.

It serves the Day 1 lesson page AND proxies AI calls to Claude so the API key
stays here (server-side), never in the browser. Stdlib only.

Run:   python3 tools/serve-lesson.py
Then open:  http://localhost:8000/lesson.html

Endpoints (POST, JSON):
  /api/explain  {svg}             -> a beginner explanation of the diagram
  /api/tutor    {q, playbook}     -> a Socratic nudge (never the full answer)
Key comes from the repo .env (ANTHROPIC_API_KEY).
"""
import os
import json
import http.server
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
LECTURE = os.path.join(REPO, "course", "day-01-idempotency", "lecture")
ENV = os.path.join(REPO, ".env")
PORT = 8000
API = "https://api.anthropic.com/v1/messages"
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")


def _key():
    if os.path.exists(ENV):
        for line in open(ENV, encoding="utf-8"):
            if line.startswith("ANTHROPIC_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("ANTHROPIC_API_KEY", "")


KEY = _key()


def claude(system, user, max_tokens=400):
    body = json.dumps({"model": MODEL, "max_tokens": max_tokens, "system": system,
                       "messages": [{"role": "user", "content": user}]}).encode()
    req = urllib.request.Request(API, data=body, method="POST", headers={
        "x-api-key": KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    return "".join(b.get("text", "") for b in data.get("content", [])).strip()


EXPLAIN_SYS = (
    "You explain network diagrams to ABSOLUTE BEGINNERS. The diagram is given as SVG markup; "
    "read its text labels and shapes. Explain what it shows in 3-5 short, friendly sentences. "
    "Gloss any jargon in a word or two. No markdown, no preamble."
)
TUTOR_SYS = (
    "You are a kind, Socratic tutor for an absolute-beginner network-automation course, Day 1: "
    "writing an IDEMPOTENT Ansible task (nokia.srlinux.config with an 'update:' list) that sets "
    "10.0.0.1/30 on ethernet-1/1 of a Nokia SR Linux device, so running it twice changes nothing. "
    "Give ONE short nudge (2-4 sentences); never paste the full solution or more than a tiny snippet."
)


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=LECTURE, **k)

    def log_message(self, *a):
        pass

    def do_POST(self):
        n = int(self.headers.get("content-length", 0))
        try:
            p = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            p = {}
        try:
            if not KEY:
                out = "No ANTHROPIC_API_KEY found in .env — the AI features can't run."
            elif self.path == "/api/explain":
                out = claude(EXPLAIN_SYS, "Explain this diagram to a beginner:\n" + p.get("svg", ""))
            elif self.path == "/api/tutor":
                out = claude(TUTOR_SYS, f"I'm stuck on: {p.get('q', '(general nudge)')}\n\n"
                                        f"My configure-interface.yml:\n{p.get('playbook', '(none)')}")
            else:
                self.send_error(404)
                return
        except urllib.error.HTTPError as e:
            out = f"AI error {e.code}: {e.read().decode()[:200]}"
        except Exception as e:
            out = f"AI error: {e}"
        self._json({"text": out})

    def _json(self, obj):
        b = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)


if __name__ == "__main__":
    print(f"Lesson server running -> http://localhost:{PORT}/lesson.html   (Ctrl+C to stop)")
    print(f"  AI key: {'loaded' if KEY else 'MISSING (add ANTHROPIC_API_KEY to .env)'}")
    http.server.HTTPServer(("127.0.0.1", PORT), H).serve_forever()
