# ContainerLab Network Automation — A Hands-On Course

From zero to agentic NetOps, built on real emulated devices. You declare what the network *should* be, you verify what it *actually* is, and you climb from deterministic automation all the way to AI-driven, self-governing operations.

## Who this is for
Network engineers (CCNA-level) comfortable in a terminal who want to become automation engineers. No prior automation experience required.

## How each day works
Every day follows the same four beats:

1. **Lecture** — a short audio + written intro: what we're doing and *why* it matters (concept only, no commands).
2. **Demonstration** — the instructor builds it live; you watch the moving parts before touching them.
3. **Lab** — you do it yourself, then break it on purpose and fix it.
4. **Verify** — you check the result on the real device, never the tool's own report.

**Golden rule of the course:** the emulator is the source of truth. A tool that says "success" is making a *claim*; the device is the *proof*. The gap between the two is where the skill lives.

## One-time setup
See [`../00-phase0-validation/SETUP.md`](../00-phase0-validation/SETUP.md): Docker + ContainerLab + Ansible in WSL, and the run-labs-from-Linux-disk rule. Verify the toolchain before Day 1.

## Syllabus (the six rungs)
| Day | Topic | Artifact |
| --- | --- | --- |
| **1** | **Idempotency & deterministic automation** ← start here | A topology + idempotent playbook |
| 2 | Config-as-code + CI/CD (the pipeline as a gate) | A pipeline that rejects bad config |
| 3 | Telemetry & observability (seeing the network live) | A live dashboard off the lab |
| 4 | Closed-loop automation (self-healing + guardrails) | A self-healing demo |
| 5 | Intent-based networking (declare outcomes, reconcile reality) | An intent engine |
| 6 | Agentic NetOps (AI proposes, human approves, system verifies) | An agentic NetOps demo |

By the end you can build, operate, and *reason about* a lab-scale agentic network — and teach it.
