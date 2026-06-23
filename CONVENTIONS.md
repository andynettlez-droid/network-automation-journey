# CONVENTIONS

The operating rules every session (human or AI) follows. Read this first.

## Roles

- **Me — Architect & Verifier (accountable).** Structure decisions, go/no-go on every increment, ground-truth verification against the emulator, and the only one who merges to `main` or applies config to the lab. I do the learning by hand.
- **Opus 4.8 — Designer / Teacher / Reviewer.** Architecture, trade-offs, schema/contract design, explaining the "why" behind each lab, and **review of Codex's diffs** (idempotency, security, readability). Writes the specs in `/specs/`.
- **Codex 5.5 — Implementer.** Code grinding against an Opus-written spec, in tight runnable increments.

### Caveat — Codex fallback
When Codex usage limits are up, **Opus 4.8 (in Cowork) takes the implementer role too.** Nothing about the safety model changes: the same increment spec, the same review step, and the same human ground-truth verification still apply. The only difference is one model is now wearing two hats — so be extra deliberate about separating the "build" pass from the "review" pass (review with fresh eyes, ideally in a separate session/turn), since the built-in cross-check of two different models is temporarily gone.

## The handoff loop (every unit of work)

1. Opus + me define the increment + acceptance criteria → written into a `/specs/` file and the `PLAN.md` checklist.
2. Implementer (Codex, or Opus on fallback) builds **only** that increment.
3. Opus reviews the diff — correctness, idempotency, security, readability.
4. I verify behavior against the emulator (ground truth), then commit.
5. I log the `What I had to verify/correct` line in the journal.

Steps 3 and 4 are never skipped. They are the skill.

## Safety rails (non-negotiable)

1. **Emulator = ground truth.** AI output is the "should"; the device is the "is." Verify every claim against real device output.
2. **Human-in-the-loop for any state change.** No agent applies config to the lab without my explicit approval.
3. **Secrets discipline.** Keys only from env vars / a secrets manager — never hardcoded, printed, or committed. See `.gitignore`.
4. **Small, reversible increments + git.** Commit after each working unit.
5. **Opus reviews Codex before I run it** — especially Ansible idempotency and anything touching device state.
6. **AI does not auto-solve the learning.** I attempt first; AI unsticks the exact point only after I've struggled.
7. **Blast-radius isolation.** Everything in a lab I can `destroy` and rebuild. No experiments against anything I can't tear down.
8. **Cost guard.** ElevenLabs: generate-once-and-cache. Cloud: free tier, billing alerts, `terraform destroy` after each session.

## Coding standards

- **Language:** Python (network tooling), YAML (Ansible/CI/ContainerLab topologies), HCL (Terraform).
- **Style:** Python — PEP 8, type hints on function signatures, `ruff`/`black` clean. YAML — 2-space indent, no tabs.
- **No secrets in code.** Read from `os.environ`; fail loudly if a required env var is missing.
- **Idempotency is a review gate** for any config-pushing code. A playbook that isn't truly idempotent does not pass.
- **Readability over cleverness.** If I can't read it, it doesn't merge.

## Git

- **Branches:** `rungN/<short-topic>` (e.g. `rung1/idempotent-interface`).
- **Commits (Conventional Commits):** `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`. Imperative, present tense.
- **One increment per commit** where practical. Commit only what was verified.

## Environment (WSL / ContainerLab)

- **Source on Windows, labs on Linux.** The repo lives on the Windows filesystem (`C:\…\ccna automation`) for editing + git. ContainerLab labs must be deployed from Linux-native disk under `~` (e.g. `~/netlab/<lab>`), **never from `/mnt/c`** — drvfs can't set Linux file permissions and SR Linux's config commit fails there. Keep topology/playbook source in the repo; copy or sync to `~` at run time.
- **Docker** runs as a systemd service in the default `Ubuntu` distro. `docker` works without `sudo` in a shell that has the `docker` group (open a fresh session or run `newgrp docker`).
- **Tear down labs after every session** (`containerlab destroy`) — blast-radius rule.
- `ccna-ubuntu` distro is off-limits (separate study project).

## Definition of done (per increment)

Built to the spec · Opus-reviewed · verified against the emulator · committed · journal line written. Only then start the next increment.
