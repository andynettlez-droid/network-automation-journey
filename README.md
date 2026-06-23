# network-automation-journey

Field service technician → Network Automation Engineer, built in the open. **Focus: ContainerLab network automation** — a six-rung climb from deterministic automation to agentic NetOps.

**The thesis:** AI makes *producing* automation cheap; it makes *verifying and directing* it valuable. This repo is the record of climbing the network-automation ladder the verification-first way — using AI (Opus 4.8 + Codex 5.5) as an accelerator on top of fundamentals I understand well enough to be accountable for. Every rung is a buildable ContainerLab lab; every lab is a portfolio artifact; the running journal proves I'm the person who catches the AI's confident-wrong output, not just the person who prompts it.

## Project boundary

This is a standalone project for **ContainerLab network automation**. It is separate from the CCNA study / lesson-player tool at `OneDrive\Documents\ccna study` (its own git repo). Any agent or session working here must confine all work to this folder and must never read from, write to, or modify the study repo.

## How to read this repo

- **`north-star-build-plan.md`** — how the build runs: roles (me = architect/verifier, Opus = designer/reviewer, Codex = implementer), safety rails, per-rung plan.
- **`PLAN.md`** — live status, locked decisions, the per-rung checklist, and "next session starts here."
- **`CONVENTIONS.md`** — the handoff protocol, coding standards, and the non-negotiable safety rails.
- **`/projects/`** — the six rung artifacts (deterministic → CI/CD → telemetry → closed-loop → intent → agentic NetOps).
- **`/learning-journal/`** — per-session entries. The `What I had to verify/correct` field is the point.
- **`/specs/`** — the increment specs that Opus writes and Codex builds against.
- **`AI-ACCELERATION.md`** — the meta-log: where AI compressed time, and what it got wrong that I caught.

## The compass

Climb in order. Opus designs and checks, Codex builds, I verify against ground truth and own the push. Aim at the layer above the AI — verification + governance — not in competition with it.
