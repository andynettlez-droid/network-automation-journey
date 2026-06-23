# PLAN.md — ContainerLab Automation → Agentic NetOps

The live source of truth across sessions and both models. Agents read and update it; I review it. Full rationale lives in `north-star-build-plan.md`.

**Scope:** ContainerLab network automation (the six rungs). CCNA study is separate, on my own time — not tracked here.

## Status: Phase 0 — Foundation (in progress)

### Toolchain state (detected 2026-06-23)
WSL2 ✓ (v2.7.8) · default distro **Ubuntu 26.04 LTS** ✓ (python3, git present) · **Docker / ContainerLab / Ansible: not yet installed** in Ubuntu. The `ccna-ubuntu` distro belongs to the separate study project — off-limits.

## Locked decisions (do not relitigate)

- Roles: me = architect/verifier, Opus = designer/reviewer, Codex = implementer (Opus covers implementer on Codex fallback). See `CONVENTIONS.md`.
- Emulator = ground truth; human-in-the-loop for any state change.
- Climb the six rungs in order; don't start rung N+1 until N's artifact exists and I can retrieve its concept cold.

## Phase 0 checklist

- [x] Repo structure scaffolded (README, PLAN, CONVENTIONS, AI-ACCELERATION, .gitignore, folders)
- [x] Phase 0 validation pack authored — `00-phase0-validation/` (topology + SETUP.md) and first Rung 1 spec (`specs/0001`)
- [x] Local git initialized + first commit (`main`, f7fbee1)
- [x] Weekly review reminder active
- [ ] Install Docker + ContainerLab + Ansible inside Ubuntu (see `00-phase0-validation/SETUP.md`) — *your hands*
- [ ] Deploy `topology.clab.yml`, confirm both nodes reachable via `sr_cli`, then `destroy` — **the Phase 0 gate**
- [ ] Push repo to GitHub as `network-automation-journey` (public) — *needs your GitHub auth*

## The six rungs

- [ ] **Rung 1 — Deterministic automation** (Wks 1–3) → `/projects/rung1-deterministic/`. Gate: write a fresh idempotent playbook unaided + concept cold.
- [ ] **Rung 2 — Config-as-code + CI/CD** (Wks 3–6) → `/projects/rung2-cicd/`. Gate: a bad change is provably blocked pre-deploy.
- [ ] **Rung 3 — Telemetry + observability** (Wks 6–10, THE HINGE) → `/projects/rung3-telemetry/`. Gate: telemetry reflects ground truth live.
- [ ] **Rung 4 — Closed-loop automation** (Wks 10–16) → `/projects/rung4-closed-loop/`. Gate: heals a defined fault + I can name every failure mode + guardrail.
- [ ] **Rung 5 — Intent-based networking** (Months 4–5) → `/projects/rung5-intent/`. Gate: intent holds under induced failure.
- [ ] **Rung 6 — Agentic NetOps** (Months 5+, NORTH STAR) → `/projects/rung6-agentic-netops/`. Gate: agent proposes → I approve → pipeline executes → verifies, with a documented autonomy model. Then package + go to market.

## Verification log

_(append one line per verified increment: `[date] built X, ran it, result: ___, what I had to fix: ___`)_

- [2026-06-23] Phase 0 repo scaffold created via Cowork.
- [2026-06-23] Toolchain detected; validation pack + spec 0001 authored; git initialized (commit f7fbee1). Verify next: run SETUP.md, deploy the validation topology, reach a node's CLI, destroy.

## Next session starts here

→ Install Docker + ContainerLab + Ansible inside the default Ubuntu distro (`00-phase0-validation/SETUP.md`), then deploy `topology.clab.yml`, reach `srl1` via `sr_cli`, and `destroy`. That clears the Phase 0 gate. Then create the GitHub repo and `git push -u origin main`. After that, Rung 1 begins from `specs/0001`.
