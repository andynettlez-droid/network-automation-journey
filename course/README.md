# ContainerLab Network Automation — A Hands-On Course (from absolute zero)

Learn to automate computer networks even if you've **never touched networking before**. You'll practice on *virtual* routers running safely on your own computer — nothing to buy, nothing you can break. By the end you'll go from "what's an IP address?" to building AI-assisted, self-governing networks.

## Who this is for
**Total beginners.** If you can use a computer and follow steps in a terminal window, you can take this course. No networking, no programming, no automation experience needed. Day 0 teaches the vocabulary; every lesson defines its terms in plain English.

## How each day works
Every day follows the same four beats:

1. **Lecture** — a short audio + a picture: what we're doing and *why* it matters (ideas only, no typing).
2. **Demonstration** — the instructor does it live while you watch.
3. **Lab** — you do it yourself, then break it on purpose and fix it.
4. **Verify** — you check the result on the real (virtual) device, never just trusting the tool's "success" message.

**Golden rule of the course:** the device is the source of truth. A tool that says "done" is making a *claim*; looking at the device is the *proof*. The gap between the two is where the real skill lives.

## One-time setup
See [`../00-phase0-validation/SETUP.md`](../00-phase0-validation/SETUP.md) — it installs the three tools you need and checks they work. Day 0 explains what each tool *is*.

## Syllabus
| Day | Topic | What you'll be able to do |
| --- | --- | --- |
| **0** | **Networking & tools, from scratch** ← start here | Understand devices, interfaces, IP addresses, and the tools — in plain English |
| 1 | Idempotency & deterministic automation | Configure a device safely, so re-running changes nothing |
| 2 | Config-as-code + CI/CD | Catch bad changes automatically before they reach a device |
| 3 | Telemetry & observability | See the network's live state on a dashboard |
| 4 | Closed-loop automation | Make the network heal itself, with guardrails |
| 5 | Intent-based networking | Declare an outcome; the system keeps reality matching it |
| 6 | Agentic NetOps | An AI proposes fixes; a human approves; the system verifies |

Each day produces something real you can show off. By the end you can build, run, and *explain* an AI-assisted network — and teach it to someone else.
