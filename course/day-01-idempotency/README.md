# Day 1 — Idempotency & Deterministic Automation

**Time:** ~60–90 min · **Prerequisite:** Phase 0 toolchain validated.

## Learning objectives
By the end you can:
- Explain idempotency and why it's the foundation of safe automation.
- Deploy a network topology from code with ContainerLab.
- Write an idempotent Ansible task that declares interface state on Nokia SR Linux.
- Prove idempotency: run twice, second run reports **no change**.
- Verify configuration on the real device — not the tool's summary.

## 1. Lecture — listen first
Play [`lecture/lecture.mp3`](lecture/lecture.mp3) (or read [`lecture/lecture.txt`](lecture/lecture.txt)). Concept and *why* only.

## 2. Demonstration — watch
The instructor will:
1. Deploy the 2-node topology from code.
2. Apply a declared interface state with one Ansible task → **changed**.
3. Run the same task again → **no change** (idempotency).
4. Verify the IP on the device with `sr_cli`.
5. Change the device by hand to cause drift, re-run, and watch only the drift get corrected.

## 3. Lab — your turn
Open [`lab/README.md`](lab/README.md) and do it yourself. The playbook's config task is left as a `TODO` — **you** write it. The instructor solution is in `lab/solution/`; try before you peek.

## 4. Verify — ground truth
Every claim is checked on the device:
```
sr_cli "show interface ethernet-1/1"
```

## Recap
- Declarative state + a state-comparing module = idempotency.
- `changed` on run 1, `ok` / no change on run 2 is the signature of correct automation.
- The device is the truth. Always look.

## Homework / portfolio artifact
Commit your working lab with a short note showing the "ran twice → second did nothing" output plus the device verification. That's your Day 1 portfolio piece.

## Next
**Day 2 — Config-as-code + CI/CD:** put your now-idempotent automation behind a pipeline that tests changes before they ever reach a device.
