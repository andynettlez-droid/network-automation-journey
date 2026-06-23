# PLAN.md — ContainerLab Automation → Agentic NetOps

The live source of truth across sessions and both models. Agents read and update it; I review it. Full rationale lives in `north-star-build-plan.md`.

**Scope:** ContainerLab network automation (the six rungs). CCNA study is separate, on my own time — not tracked here.

## Status: Phase 0 — Foundation (in progress)

## Locked decisions (do not relitigate)

- Roles: me = architect/verifier, Opus = designer/reviewer, Codex = implementer (Opus covers implementer on Codex fallback). See `CONVENTIONS.md`.
- Emulator = ground truth; human-in-the-loop for any state change.
- Climb the six rungs in order; don't start rung N+1 until N's artifact exists and I can retrieve its concept cold.

## Phase 0 checklist

- [ ] Validate the toolchain: Docker + ContainerLab + Ansible installed; a throwaway 2-node topology deploys, is reachable, and tears down cleanly
- [x] Repo structure scaffolded (README, PLAN, CONVENTIONS, AI-ACCELERATION, .gitignore, folders)
- [ ] Push repo to GitHub as `network-automation-journey` (public)
- [ ] Weekly review reminder active

## The six rungs

- [ ] **Rung 1 — Deterministic automation** (Wks 1–3) → `/projects/rung1-deterministic/`. Gate: write a fresh idempotent playbook unaided + concept cold.
- [ ] **Rung 2 — Config-as-code + CI/CD** (Wks 3–6) → `/projects/rung2-cicd/`. Gate: a bad change is provably blocked pre-deploy.
- [ ] **Rung 3 — Telemetry + observability** (Wks 6–10, THE HINGE) → `/projects/rung3-telemetry/`. Gate: telemetry reflects ground truth live.
- [ ] **Rung 4 — Closed-loop automation** (Wks 10–16) → `/projects/rung4-closed-loop/`. Gate: heals a defined fault + I can name every failure mode + guardrail.
- [ ] **Rung 5 — Intent-based networking** (Months 4–5) → `/projects/rung5-intent/`. Gate: intent holds under induced failure.
- [ ] **Rung 6 — Agentic NetOps** (Months 5+, NORTH STAR) → `/projects/rung6-agentic-netops/`. Gate: agent proposes → I approve → pipeline executes → verifies, with a documented autonomy model. Then package + go to market.

## Verification log

_(append one line per verified increment: `[date] built X, ran it, result: ___, what I had to fix: ___`)_

- [2026-06-23] Phase 0 repo scaffold created via Cowork. Verify: open files, confirm structure, push to GitHub.

## Next session starts here

→ Stand up the toolchain: install Docker + ContainerLab + Ansible, deploy a throwaway 2-node SR Linux topology, confirm both nodes are up and reachable, then `destroy` it. Once the environment is proven, push the repo to GitHub and write the first `/specs/` increment for Rung 1.
