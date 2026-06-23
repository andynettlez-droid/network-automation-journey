# Spec 0001: Rung 1 — topology + idempotent interface config

The interface between designer (Opus) and implementer (Codex, or Opus on fallback). One small, runnable increment. Build and verify in a single sitting.

**Rung / project:** Rung 1 — deterministic automation
**Branch:** `rung1/idempotent-interface`
**Prereq:** Phase 0 toolchain validated (see `00-phase0-validation/SETUP.md`).

## Goal
Stand up the Rung 1 lab topology from code and configure one interface on `srl1` **idempotently** with Ansible — so a second run of the same playbook reports no change. This is the concrete demonstration of idempotency, the base of the whole ladder.

## Scope
- In scope: the `.clab.yml` topology, an Ansible inventory, and one playbook that sets an IP on `srl1` interface `ethernet-1/1`.
- Out of scope (do NOT build): multi-node config, routing protocols, CI, any abstraction/roles. Keep it one flat playbook. _(prevents over-reach)_

## Acceptance criteria
- [ ] `containerlab deploy` brings up the topology; both nodes `running`.
- [ ] Playbook run #1 configures the interface and reports `changed`.
- [ ] Playbook run #2 (no edits) reports `ok` / **no change** — idempotency proven.
- [ ] Inducing drift by hand (change the IP on the device), then re-running, corrects **only** the drift.
- [ ] Verified against the device, not the playbook's own report (see below).

## Files to touch
- `projects/rung1-deterministic/topology.clab.yml` — 2-node SR Linux (start from the Phase 0 topology).
- `projects/rung1-deterministic/inventory.yml` — Ansible inventory for `srl1` (gNMI/NETCONF or the SR Linux Ansible collection).
- `projects/rung1-deterministic/configure-interface.yml` — the playbook.
- `projects/rung1-deterministic/README.md` — the "ran twice, second did nothing" writeup.

## Model split
- **Codex (or Opus on fallback):** generate the topology, inventory skeleton, and a playbook **skeleton with TODOs** — do NOT write the working config task; leave it for the human.
- **You (by hand):** write the actual interface-config task yourself; this is the rep that teaches idempotency.
- **Opus:** review the finished playbook specifically for *true* idempotency (does the module declare desired state, or blindly push?) before run #2.

## Constraints / guardrails
- Secrets (device credentials) from env vars or an Ansible vault — never hardcoded or committed.
- Idempotent by construction: use a state-declaring module, not raw command pushes.
- Human-in-the-loop: you run the playbook against the lab, not an agent.

## How I'll verify (ground truth)
After each run, enter the device and read real state — this is the truth, not Ansible's `changed/ok`:
```
docker exec -it clab-rung1-deterministic-srl1 sr_cli
show interface ethernet-1/1
```
The interface IP on the device must match the declared state; run #2 must show the device unchanged.

## Notes for the reviewer
Scrutinize hardest: is the playbook genuinely idempotent, or does it just *look* unchanged because the module always reports `ok`? Prove it by checking the device state and the module's change semantics, not the summary line.
