# Rung 1 — Deterministic automation (idempotency)

**Concept:** declare desired state, run automation, run it **again** and watch it do nothing. The truth lives in code; the device reflects it. This is the base of the whole ladder — everything above "decides"; this just "executes."

## Status: scaffolded (config task is yours to write)

## Files
- `topology.clab.yml` — 2-node SR Linux. Deploy from `~/netlab` (not `/mnt/c` — see repo `CONVENTIONS.md`).
- `inventory.yml` — Ansible inventory for `srl1` (nokia.srlinux collection, JSON-RPC; password from `$SRL_PASSWORD`).
- `configure-interface.yml` — the playbook. **The interface-config task is intentionally a TODO — write it by hand, not with an agent.**

## The exercise (by hand)
1. Deploy: `mkdir -p ~/netlab/rung1 && cp topology.clab.yml ~/netlab/rung1/ && cd ~/netlab/rung1 && sudo containerlab deploy -t topology.clab.yml`
2. `ansible-galaxy collection install nokia.srlinux` and `export SRL_PASSWORD='NokiaSrl1!'`
3. Write the config task in `configure-interface.yml` (declare an IP on `ethernet-1/1`).
4. Run the playbook → expect **changed**.
5. Run it **again** unchanged → expect **no change**. ← idempotency proven.
6. Induce drift by hand on the device, re-run → only the drift is corrected.
7. Verify on the device each time (`show interface ethernet-1/1`), not the playbook's summary.

## Gate to Rung 2
You can write a fresh idempotent playbook unaided **and** explain *why* it's idempotent (what makes the module declare state vs. push commands) cold.

## Result
_(fill in: paste the "ran twice → second run no change" output + the device verification, and the journal link.)_
