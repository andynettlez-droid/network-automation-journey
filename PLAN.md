# PLAN.md — ContainerLab Automation → Agentic NetOps

The live source of truth across sessions and both models. Agents read and update it; I review it. Full rationale lives in `north-star-build-plan.md`.

**Scope:** ContainerLab network automation (the six rungs). CCNA study is separate, on my own time — not tracked here.

## Status: Phase 0 — Foundation (gate cleared; GitHub push pending)

### Toolchain state (validated 2026-06-23)
WSL2 ✓ (v2.7.8) · default distro **Ubuntu 26.04 LTS** ✓ · **Docker 29.6.0, ContainerLab 0.76.1, Ansible 13.1.0 installed & validated**. Labs run from `~/netlab` (Linux-native) — **not** `/mnt/c` (drvfs breaks SR Linux's config commit). The `ccna-ubuntu` distro is off-limits (separate study project).

## Locked decisions (do not relitigate)

- Roles: me = architect/verifier, Opus = designer/reviewer, Codex = implementer (Opus covers implementer on Codex fallback). See `CONVENTIONS.md`.
- Emulator = ground truth; human-in-the-loop for any state change.
- Climb the six rungs in order; don't start rung N+1 until N's artifact exists and I can retrieve its concept cold.

## Phase 0 checklist

- [x] Repo structure scaffolded (README, PLAN, CONVENTIONS, AI-ACCELERATION, .gitignore, folders)
- [x] Phase 0 validation pack authored — `00-phase0-validation/` (topology + SETUP.md) and first Rung 1 spec (`specs/0001`)
- [x] Local git initialized + first commit (`main`, f7fbee1)
- [x] Weekly review reminder active
- [x] Install Docker + ContainerLab + Ansible inside Ubuntu
- [x] Deploy validation topology from `~/netlab` — both nodes `running`, clean config commit — **Phase 0 gate cleared** (final `sr_cli` look + `destroy` to confirm)
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
- [2026-06-23] Toolchain detected; validation pack + spec 0001 authored; git initialized (commit f7fbee1).
- [2026-06-23] Toolchain installed + validated (Docker/ContainerLab/Ansible). Catch: `/mnt/c` drvfs breaks SR Linux config commit → labs now run from `~/netlab`. Logged in AI-ACCELERATION.md + journal.

## Next session starts here

→ Phase 0 gate cleared. Create the GitHub repo and `git push -u origin main`, then start Rung 1 from `specs/0001` (idempotent interface config). Reminder: deploy Rung 1 labs from `~/netlab`, never `/mnt/c`.
