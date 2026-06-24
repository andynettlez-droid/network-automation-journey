#!/usr/bin/env python3
"""
tutor.py — an AI tutor for the lab. It reads YOUR playbook and what you're stuck on,
and gives a TARGETED NUDGE toward your next step. It never pastes the solution.

Run from your lab folder:
  python3 tutor.py                       # it asks what you're stuck on
  python3 tutor.py "I get a 401 error"   # or tell it directly

Needs ANTHROPIC_API_KEY (in the repo .env, gitignored). Stdlib only.
"""
import os
import sys
import json
import urllib.request
import urllib.error

API = "https://api.anthropic.com/v1/messages"
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
REPO_ENV = "/mnt/c/Users/andyn/Claude/Projects/ccna automation/.env"

SYSTEM = (
    "You are a kind, Socratic tutor for an absolute-beginner network-automation course. "
    "The student is on Day 1: writing an IDEMPOTENT Ansible task (module nokia.srlinux.config "
    "with an 'update:' list) that sets the IPv4 address 10.0.0.1/30 on interface ethernet-1/1 "
    "of a Nokia SR Linux device, so running it twice changes nothing the second time.\n"
    "RULES: Give ONE short, targeted nudge toward the student's next step (2-4 sentences). "
    "Point at the specific concept, line, or error; ask a guiding question when useful. "
    "NEVER paste the full solution or a complete working task, and never write more than a "
    "tiny one-line snippet even if asked. Be warm and encouraging; do not lecture."
)


def _load_env():
    for p in (os.path.join(os.getcwd(), ".env"), REPO_ENV):
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _read(path):
    try:
        return open(path, encoding="utf-8").read()
    except Exception:
        return "(no configure-interface.yml found in this folder)"


def main():
    _load_env()
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("ERROR: ANTHROPIC_API_KEY not found. Add it to the repo .env (gitignored).")
    stuck = " ".join(sys.argv[1:]).strip()
    if not stuck:
        try:
            stuck = input("What are you stuck on? (paste any error too)\n> ").strip()
        except EOFError:
            stuck = ""
    playbook = _read(os.path.join(os.getcwd(), "configure-interface.yml"))
    user = (f"My current configure-interface.yml:\n```\n{playbook}\n```\n\n"
            f"What I'm stuck on: {stuck or '(not sure - a general nudge, please)'}")
    body = json.dumps({
        "model": MODEL, "max_tokens": 300, "system": SYSTEM,
        "messages": [{"role": "user", "content": user}],
    }).encode()
    req = urllib.request.Request(API, data=body, method="POST", headers={
        "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
        text = "".join(b.get("text", "") for b in data.get("content", []))
        print("\n\033[36m== Tutor ==\033[0m\n" + text.strip() + "\n")
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR {e.code}: {e.read().decode()[:300]}")


if __name__ == "__main__":
    main()
