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
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
LECTURE = os.path.join(REPO, "course", "day-01-idempotency", "lecture")
ENV = os.path.join(REPO, ".env")
PORT = 8000
API = "https://api.anthropic.com/v1/messages"
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")


def env(k):
    if os.path.exists(ENV):
        for line in open(ENV, encoding="utf-8"):
            if line.startswith(k + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get(k, "")


KEY = env("ANTHROPIC_API_KEY")


def elevenlabs_tts(text):
    """Speak text in the course voice (Daniel) via ElevenLabs. Returns mp3 bytes or None."""
    k = env("ELEVENLABS_API_KEY"); vid = env("ELEVEN_VOICE_ID")
    if not k or not vid or not text:
        return None
    try:
        speed = float(env("ELEVEN_SPEED") or "1.0")
    except Exception:
        speed = 1.0
    body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2",
                       "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "speed": speed}}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}",
                                 data=body, method="POST",
                                 headers={"xi-api-key": k, "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    except Exception:
        return None


def claude(system, user, max_tokens=400):
    body = json.dumps({"model": MODEL, "max_tokens": max_tokens, "system": system,
                       "messages": [{"role": "user", "content": user}]}).encode()
    req = urllib.request.Request(API, data=body, method="POST", headers={
        "x-api-key": KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    return "".join(b.get("text", "") for b in data.get("content", [])).strip()


# --- Agentic (tool-using) tutor -------------------------------------------------
LAB = "/home/andyn/netlab/day1-mine"

TUTOR_AGENT_SYS = (
    "You are a kind, Socratic tutor for an absolute-beginner network-automation course, Day 1: the student "
    "must write an IDEMPOTENT Ansible task (nokia.srlinux.config with an 'update:' list) that sets 10.0.0.1/30 "
    "on ethernet-1/1 of a Nokia SR Linux device. You have tools to read their playbook, run the grader, and "
    "inspect the device. USE the tools to find the REAL problem before answering. Then give ONE short, specific "
    "nudge based on what you actually found (name the real issue, e.g. 'your task has no ipv4 block'), ask a "
    "guiding question, and encourage. NEVER paste the full solution or more than a tiny one-line snippet."
)

TOOLS = [
    {"name": "read_playbook", "description": "Read the student's current configure-interface.yml.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "run_grader", "description": "Run the lab grader (check.sh) and return its output.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "inspect_interface", "description": "Show the live state of ethernet-1/1 on device srl1.",
     "input_schema": {"type": "object", "properties": {}}},
]


def _run_tool(name):
    try:
        if name == "read_playbook":
            return open(os.path.join(LAB, "configure-interface.yml"), encoding="utf-8").read()[:4000]
        if name == "run_grader":
            r = subprocess.run(["bash", "check.sh"], cwd=LAB, capture_output=True, text=True, timeout=120)
            return (r.stdout + r.stderr)[-3000:]
        if name == "inspect_interface":
            cmd = ("docker exec clab-day1-idempotency-srl1 sr_cli 'show interface ethernet-1/1' 2>/dev/null "
                   "|| sudo docker exec clab-day1-idempotency-srl1 sr_cli 'show interface ethernet-1/1'")
            r = subprocess.run(["bash", "-lc", cmd], capture_output=True, text=True, timeout=45)
            return (r.stdout or r.stderr)[-3000:]
    except Exception as e:
        return f"(tool error: {e})"
    return "(unknown tool)"


def _messages(system, messages, tools=None, max_tokens=600):
    payload = {"model": MODEL, "max_tokens": max_tokens, "system": system, "messages": messages}
    if tools:
        payload["tools"] = tools
    req = urllib.request.Request(API, data=json.dumps(payload).encode(), method="POST", headers={
        "x-api-key": KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def claude_agent(question, max_turns=5):
    messages = [{"role": "user", "content": question}]
    for _ in range(max_turns):
        resp = _messages(TUTOR_AGENT_SYS, messages, tools=TOOLS)
        if resp.get("stop_reason") == "tool_use":
            messages.append({"role": "assistant", "content": resp["content"]})
            results = []
            for block in resp.get("content", []):
                if block.get("type") == "tool_use":
                    results.append({"type": "tool_result", "tool_use_id": block["id"],
                                    "content": _run_tool(block["name"])})
            messages.append({"role": "user", "content": results})
        else:
            return "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text").strip()
    return "(tutor hit its step limit - try asking again)"


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
        if self.path == "/api/speak":
            audio = elevenlabs_tts(p.get("text", ""))
            if audio:
                self.send_response(200)
                self.send_header("content-type", "audio/mpeg")
                self.send_header("content-length", str(len(audio)))
                self.end_headers()
                self.wfile.write(audio)
            else:
                self._json({"text": "(voice unavailable - check ELEVENLABS_API_KEY / ELEVEN_VOICE_ID in .env)"})
            return
        try:
            if not KEY:
                out = "No ANTHROPIC_API_KEY found in .env — the AI features can't run."
            elif self.path == "/api/explain":
                out = claude(EXPLAIN_SYS, "Explain this diagram to a beginner:\n" + p.get("svg", ""))
            elif self.path == "/api/tutor":
                out = claude_agent(f"I'm stuck on: {p.get('q', '(general nudge - look at my work)')}")
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
