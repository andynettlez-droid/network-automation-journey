# Day 1 — Idempotency & Deterministic Automation

**Time:** ~60–90 min · **Prerequisite:** Day 0 (you know what an interface and an IP address are) and the Phase 0 setup.

> **Idempotency** (the word this whole day is about): you describe the state you want, and re-running the automation changes nothing once reality already matches. So it's safe to run a thousand times.

## What you're doing today, in plain English
You'll give one **port** (`ethernet-1/1`) on a virtual router an **IP address** (`10.0.0.1/30`), using **Ansible** instead of typing commands by hand. Then you'll run the exact same automation again — and watch it correctly do *nothing*, because the device already matches. See the picture: [`lecture/topology.svg`](lecture/topology.svg).

## Learning objectives
By the end you can:
- Say what idempotency is and why it makes automation safe.
- Boot a small network from a file with ContainerLab.
- Write an Ansible task that *declares* an interface's address on SR Linux.
- Prove idempotency: run twice, second run reports **no change**.
- Verify the result on the real device — not the tool's summary.

## The one idea under the hood: declarative vs. the old way
- **The old way (imperative):** you send commands — "add this address." Re-run it and it adds again, or errors.
- **The declarative way (what we use):** you state "this port *should have* this address." The tool checks what's there and only acts if something differs. *That* is what makes re-running safe — and it's why declarative equals idempotent.

## 1. Lecture — listen first
Play [`lecture/lecture.mp3`](lecture/lecture.mp3) (or read [`lecture/lecture.txt`](lecture/lecture.txt)) and look at the diagram. Ideas and *why* only.

## 2. Demonstration — watch
The instructor will: boot the two routers → apply the address with one Ansible task (**changed**) → run it again (**no change**) → verify on the device → change the device by hand to cause **drift**, re-run, and watch only the drift get fixed.

## 3. Lab — your turn
Open [`lab/README.md`](lab/README.md). The config task is left as a `TODO` — **you** write it. Try before peeking at `lab/solution/`.

## 4. Verify — ground truth
Always check the device itself (`sr_cli` only exists *inside* the container, so go in via `docker exec`):
```
docker exec -it clab-day1-idempotency-srl1 sr_cli "show interface ethernet-1/1"
```

## Recap
- **Declarative state + a state-comparing tool = idempotency.**
- `changed` on run 1, `ok` / no change on run 2 is the signature of correct automation.
- The device is the truth. Always look.

## Homework / portfolio artifact
Commit your working lab with a short note showing the "ran twice → second did nothing" output and the device check. That's your Day 1 piece.

## Next
**Day 2 — Config-as-code + CI/CD:** put your now-safe automation behind an automatic checker that rejects bad changes before they reach a device.
