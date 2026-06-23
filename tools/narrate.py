#!/usr/bin/env python3
"""
narrate.py — turn a lesson's "what & why" script into narrated audio via ElevenLabs.

Audio carries CONCEPT and WHY only — never CLI/commands (those stay visual on screen).
Uses only the Python standard library (no pip installs needed).

Usage:
  python3 narrate.py --list                    # list available voices (id | name | labels)
  python3 narrate.py SCRIPT.txt [OUT.mp3]      # generate narration from a text script
  python3 narrate.py SCRIPT.txt --voice <id>   # override the voice for this run

Reads from the environment:
  ELEVENLABS_API_KEY  (required) — your API key (never hardcode it)
  ELEVEN_VOICE_ID     (optional) — default voice id; or pass --voice <id>

Audio is written under ../lessons-audio/ (gitignored).
"""
import os
import sys
import json
import urllib.request
import urllib.error

API = "https://api.elevenlabs.io/v1"
MODEL_ID = "eleven_multilingual_v2"


def _load_dotenv():
    """Load KEY=VALUE lines from a gitignored .env (repo root or tools/) into the env.
    Existing real env vars win; .env only fills what's missing."""
    here = os.path.dirname(os.path.abspath(__file__))
    for path in (os.path.join(here, "..", ".env"), os.path.join(here, ".env")):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _key():
    _load_dotenv()
    k = os.environ.get("ELEVENLABS_API_KEY")
    if not k:
        sys.exit("ERROR: ELEVENLABS_API_KEY not found. Put it in a .env file at the "
                 "repo root (ELEVENLABS_API_KEY=...) — it's gitignored.")
    return k


def list_voices():
    req = urllib.request.Request(f"{API}/voices", headers={"xi-api-key": _key()})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    for v in data.get("voices", []):
        labels = v.get("labels", {}) or {}
        desc = ", ".join(f"{k}={val}" for k, val in labels.items())
        print(f"{v['voice_id']}  |  {v['name']}  |  {desc}")


def synth(script_path, out_path, voice_id, speed=1.0):
    if not voice_id:
        sys.exit("ERROR: no voice id. Pass --voice <id> or set ELEVEN_VOICE_ID.")
    with open(script_path, encoding="utf-8") as f:
        text = f.read().strip()
    if not text:
        sys.exit("ERROR: script is empty.")
    # speed: 0.7 (slowest) .. 1.2 (fastest); 1.0 = default. Lower = calmer pacing.
    speed = max(0.7, min(1.2, float(speed)))
    body = json.dumps({
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "speed": speed},
    }).encode()
    req = urllib.request.Request(
        f"{API}/text-to-speech/{voice_id}",
        data=body,
        headers={"xi-api-key": _key(), "Content-Type": "application/json"},
        method="POST",
    )
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    try:
        with urllib.request.urlopen(req, timeout=120) as r, open(out_path, "wb") as out:
            out.write(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"ERROR {e.code}: {e.read().decode()[:300]}")
    print(f"Saved: {out_path}")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    if args[0] == "--check":
        _load_dotenv()
        k = os.environ.get("ELEVENLABS_API_KEY", "")
        print(f"key_present={bool(k)}  len={len(k)}  prefix={k[:3]!r}  "
              f"has_space={' ' in k}  has_quotes={(chr(34) in k) or (chr(39) in k)}")
        return
    if args[0] == "--list":
        list_voices()
        return
    _load_dotenv()
    voice = os.environ.get("ELEVEN_VOICE_ID")
    speed = float(os.environ.get("ELEVEN_SPEED", "1.0"))
    if "--voice" in args:
        i = args.index("--voice")
        voice = args[i + 1]
        del args[i:i + 2]
    if "--speed" in args:
        i = args.index("--speed")
        speed = float(args[i + 1])
        del args[i:i + 2]
    script = args[0]
    here = os.path.dirname(os.path.abspath(__file__))
    default_out = os.path.join(
        here, "..", "lessons-audio",
        os.path.splitext(os.path.basename(script))[0] + ".mp3",
    )
    out = args[1] if len(args) > 1 else os.path.normpath(default_out)
    synth(script, out, voice, speed)


if __name__ == "__main__":
    main()
