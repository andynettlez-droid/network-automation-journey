# Spec: [increment name]

The interface between designer (Opus) and implementer (Codex, or Opus on fallback). One spec = one small, runnable increment. Keep it tight enough to build and verify in a single sitting.

**Rung / project:** e.g. Rung 1 — deterministic automation
**Branch:** `rungN/<short-topic>`

## Goal
One sentence: what this increment produces and why.

## Scope
- In scope: …
- Out of scope (do NOT build): … _(prevents the 800-line over-reach)_

## Acceptance criteria
- [ ] …
- [ ] …
- [ ] Verifiable against the emulator how: ___

## Files to touch
- `path/to/file` — what changes

## Constraints / guardrails
- Secrets from env vars only.
- Idempotent if it pushes config (re-run = no change).
- Reviewer (Opus) checks: correctness, idempotency, security, readability.

## How I'll verify (ground truth)
The exact device command / observation that proves it works — not the tool's own success report.

## Notes for the reviewer
Anything to scrutinize especially hard.
