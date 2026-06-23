# North Star Build Plan — Climbing to Agentic NetOps with Opus 4.8 + Codex 5.5

**Scope:** this project is **ContainerLab network automation** — the six-rung climb from deterministic automation to agentic NetOps. (CCNA study is pursued separately, on your own time; it is not part of this build.)

**What this is:** the execution layer beneath `north-star-roadmap.md`. The roadmap says *what* to climb (six rungs to agentic NetOps). This says *how* to build it — the division of labor between you (architect/verifier), **Opus 4.8** (designer/teacher/reviewer), and **Codex 5.5** (implementer) — plus the skills, safety rails, shared artifacts, and per-rung gates that keep the climb efficient, safe, and clean.

**One sentence:** Opus designs and verifies, Codex implements, you own ground-truth verification and the production push. That triangle *is* your career thesis made operational — AI produces, the human governs accountability.

---

## 1. The three roles (lock these)

**You — Architect & Verifier (accountable).**
- Own structure decisions, the go/no-go on every increment, and ground-truth verification against the emulator.
- Build the hard parts by hand — the struggle is the learning. Never accept a blob you can't read.
- The only one who pushes to "production" (merges to main, applies config to the lab).

**Opus 4.8 — Designer, Teacher, Reviewer (the judgment-side AI).**
- System/architecture design, trade-off reasoning, schema and contract design.
- Explains the concept and the "why" behind each lab; diagnoses your exact stuck-point; quizzes you cold.
- Code review of Codex's output — idempotency, security, readability, "will this survive production" judgment.
- Writes the specs/tickets Codex implements against.

**Codex 5.5 — Implementer (the production-side AI).**
- Raw code grinding under an Opus-written spec: topology files, Ansible playbooks, Python tooling, IaC, test scaffolds, config generation, helper scripts.
- Works in tight, runnable increments. Never an 800-line dump across 10 files before anything is checked.

**Caveat — Codex fallback.** When Codex usage limits are up, **Opus 4.8 (in Cowork) takes the implementer role too** — same spec, same review step, same human ground-truth verification. Nothing about the safety model changes; just separate the "build" pass from the "review" pass deliberately (review with fresh eyes in a separate turn/session), since the two-different-models cross-check is temporarily unavailable.

**The handoff loop — every unit of work:**
1. You + Opus define the increment + acceptance criteria → write it into `PLAN.md` / a spec file.
2. Implementer (Codex, or Opus on fallback) builds only that increment.
3. Opus reviews the diff (correctness, idempotency, security, readability).
4. You verify behavior against the emulator (ground truth) and commit.
5. Log the "what I had to verify/correct" line in the journal.

Never skip steps 3 or 4. The review + verify steps are the entire point — they're where the durable, hireable skill lives.

---

## 2. Why this split (efficiency + safety rationale)

- **Efficiency:** Opus is stronger at architecture, reasoning, teaching, and catching subtle wrongness; Codex is faster at high-volume code production. Each runs on its edge.
- **Safety (defense in depth):** two AIs that both produce *and* check each other (Opus reviews Codex; you verify both against the emulator) gives layered protection against confident-wrong output.
- **Cleanliness/governance:** the human as sole production-pusher + emulator-as-ground-truth means no change reaches a real target unreviewed. This is literally the Rung 6 governance model, practiced from day one.

---

## 3. Safety rails (non-negotiable, apply to every rung)

1. **Emulator = ground truth.** AI output is the "should"; the device is the "is." Verify every claim against real device output.
2. **Human-in-the-loop for any state change.** No agent applies config to the lab without your explicit approval. This rule scales unchanged into the Rung 6 autonomy model.
3. **Secrets discipline.** API/cloud keys only from env vars / a secrets manager — never hardcoded, printed, or committed. `.gitignore` covers `.env`, `*.key`, Terraform state, and any inventory holding credentials.
4. **Small, reversible increments + git.** Commit after each working unit so a bad agent edit rolls back cleanly.
5. **Opus reviews Codex before you run it** — especially Ansible idempotency and anything touching device state.
6. **AI does not auto-solve the hard parts.** You attempt first; AI unsticks the exact point only after you've struggled. Diagnosis is the skill.
7. **Blast-radius isolation.** Everything lives in a lab (ContainerLab/CML) you can `destroy` and rebuild. No experiments against anything you can't tear down.
8. **Cost guard.** Cloud (Rung 4+): free tier, billing alerts, `terraform destroy` after each session. Cache anything metered.

---

## 4. Shared artifacts (the spine across sessions and both models)

These keep a fresh Opus session and a fresh Codex session coherent:

- **`PLAN.md`** (repo root) — status, locked decisions, per-rung checklist, verification log, "next session starts here." Both agents read and update it; you review it.
- **`/specs/`** — one Opus-authored spec per increment; the interface between designer and implementer.
- **`SCHEMA` / contracts** — frozen data shapes (inventory, intent model, telemetry schema) so components never drift out of sync.
- **`/learning-journal/`** — per-session entries; the "what I had to verify/correct" field is the portfolio core.
- **`AI-ACCELERATION.md`** — running meta-log: where AI compressed time, what it got wrong that you caught.
- **`CONVENTIONS.md`** — coding standards, naming, commit format, the handoff protocol, and the safety rails — so Codex output is consistent and reviewable.

---

## 5. Phase 0 — Foundation (Week 0, ~half a day, before any rung)

Stand up the operating system so the climb is documented and coherent from the first commit.

- **Validate the toolchain first:** install Docker + ContainerLab + Ansible and deploy a throwaway 2-node topology; confirm both nodes come up and you can reach them. Prove the environment before building anything on it.
- Create the public GitHub repo `network-automation-journey`. Folders: `/learning-journal/`, `/projects/`, `/specs/`. Add README (one-paragraph thesis), `PLAN.md`, `CONVENTIONS.md`, `AI-ACCELERATION.md`, `.gitignore`.
- Write the handoff protocol (§1) and safety rails (§3) into `CONVENTIONS.md`.
- **Model split:** Opus sets up structure/README/PLAN.md and the conventions; Codex generates `.gitignore`, templates, and repo scaffolding; you commit.
- **Skills:** `schedule` → weekly journal/PLAN review reminder. Optionally `skill-creator` → a small "journal-entry" skill.
- **Gate to Rung 1:** repo live, `PLAN.md` populated, toolchain verified (a topology deploys + tears down cleanly), schedule set.

---

## 6. The climb — per rung

Format per rung: **Build · Opus does · Codex does · You verify · Skills · Artifact · Gate.**

### Rung 1 — Deterministic automation (Weeks 1–3)
- **Build:** ContainerLab topology from code; Ansible/Python pushes config to virtual devices; prove idempotency (run twice → second run does nothing).
- **Opus:** explains idempotency / declarative-vs-imperative; designs the lab task; **reviews your playbook for true idempotency before you re-run**; diagnoses stuck points.
- **Codex:** generates the `.clab.yml` topology; scaffolds (does **not** solve) the playbook skeleton with TODOs; writes helper scripts.
- **You (by hand):** deploy the topology, write the playbook yourself, *see* the second run no-op, induce drift, watch it correct. Verify on the device (e.g. SR Linux) directly.
- **Skills:** `pdf`/`docx` (Rung 1 writeup), `canvas-design` (topology diagram for the README).
- **Artifact:** `/projects/rung1-deterministic/` — topology + playbook + README showing "ran twice, second did nothing."
- **Gate:** you can write a fresh idempotent playbook unaided *and* retrieve the concept cold.

### Rung 2 — Config-as-code + CI/CD (Weeks 3–6)
- **Build:** configs in Git; a pipeline lints/tests/deploys; bad config rejected pre-deploy.
- **Opus:** designs the pipeline stages + verification gates (this rung mechanizes your verification discipline); reviews pipeline logic; teaches the GitOps "why."
- **Codex:** writes the GitHub Actions / GitLab CI YAML, Batfish/pyATS test scaffolds, lint config.
- **You:** submit a deliberately bad config, watch the gate reject it; verify what passed actually applied.
- **Skills:** `pdf`/`docx` (writeup).
- **Artifact:** `/projects/rung2-cicd/` — a pipeline that gates network changes.
- **Gate:** a bad change is provably blocked pre-deploy; you can explain every stage.

### Rung 3 — Telemetry + observability (Weeks 6–10) — THE HINGE
- **Build:** stream live state (gNMI / model-driven telemetry) → time-series store → Grafana dashboard; NetBox/Nautobot as source of truth.
- **Opus:** designs the telemetry pipeline architecture; explains streaming-telemetry "why"; reviews data flow; helps define what "normal" looks like.
- **Codex:** wires Telegraf/Prometheus, Grafana provisioning, gNMI subscriptions, NetBox integration scripts.
- **You:** confirm the dashboard reflects real induced changes (pull a link, watch the metric move) — dashboard vs device = claim vs truth.
- **Skills:** `canvas-design` (architecture diagram), `docx` (the hinge-rung writeup).
- **Artifact:** `/projects/rung3-telemetry/` — live dashboard off your lab.
- **Gate:** telemetry reflects ground truth in real time. (CCNA, pursued separately on your own time, naturally lands around here — but it neither gates nor is gated by this build.)

### Rung 4 — Closed-loop automation (Weeks 10–16) — first taste of the edge
- **Build:** connect Rung 3 telemetry → Rung 1 automation. Detect a condition → auto-remediate with guardrails. The network self-heals a defined fault.
- **Opus:** designs the OODA loop + the **guardrails** (the dangerous part — wrong remediation worsens the incident); reviews the decision logic adversarially ("how does this misfire?"); designs the human-approval checkpoint.
- **Codex:** implements the detector, the remediation trigger, the guardrail checks, the logging.
- **You:** break the network, watch it heal, then try to make the remediation misfire and confirm guardrails hold. This is governance practice.
- **Skills:** `canvas-design` (loop diagram), `docx` (the standout break/heal/guardrail writeup).
- **Artifact:** `/projects/rung4-closed-loop/` — self-heal demo with documented guardrails. Your strongest portfolio piece so far.
- **Gate:** it heals the defined fault *and* you can articulate every failure mode + guardrail.

### Rung 5 — Intent-based networking (Months 4–5)
- **Build:** move from "if X do Y" to "maintain this OUTCOME." Declare intent; the system continuously reconciles reality to intent.
- **Opus:** designs the reconciliation loop + intent model (the Kubernetes-for-networks leap); reasons about convergence and conflicts; reviews.
- **Codex:** implements the intent engine, the diff-and-reconcile logic, state comparison.
- **You:** declare an outcome, induce failures, watch reconciliation hold the intent; verify against devices.
- **Skills:** `canvas-design` (intent-engine diagram), `docx`.
- **Artifact:** `/projects/rung5-intent/` — an intent engine holding declared state against induced failures.
- **Gate:** intent holds under failure; you understand declarative reconciliation deeply.

### Rung 6 — Agentic NetOps (Months 5+) — THE NORTH STAR
- **Build:** an LLM agent ingests telemetry (R3), reasons about an anomaly, **proposes** a remediation, executes via the tested pipeline (R2) *with human-in-the-loop approval*, then verifies. Autonomy as an advisory→autonomous trust gradient.
- **Opus:** home turf — designs the agent orchestration, the approval/governance boundary, the autonomy gradient, the MCP servers exposing network tooling; reasons about the trust model; can be (or design) the reasoning agent itself.
- **Codex:** implements the agent scaffolding, the MCP server(s), the approval-gate plumbing, the verify-after-action step.
- **You:** operate the approval boundary — the agent proposes, *you* approve, the pipeline executes, the system verifies. You **are** the governance layer the whole thesis is about.
- **Skills:** `skill-creator` (package the network tooling as a reusable skill/MCP), `canvas-design` (architecture + autonomy-model diagram), `docx`/`pptx` (capstone writeup + portfolio deck).
- **Artifact:** `/projects/rung6-agentic-netops/` — an agentic demo with a documented autonomy/approval model. The defensible summit.
- **Gate:** the summit. Then **package + go to market** (the old roadmap's Phase 5): clean repo story, 2–3 writeups, the reflective "how I used AI to compress this" piece, targeted applications to Network Automation / NetDevOps / NRE roles.

---

## 7. Cadence & rhythm

- **Per build session:** run the LOOP — attempt → struggle → targeted unstick (Opus) → apply → verify against the emulator → document. One journal entry every time.
- **Weekly:** review the journal, update `PLAN.md` "next," update `AI-ACCELERATION.md`.
- **Per rung:** don't start N+1 until N's artifact exists and you can retrieve its concept cold.

---

## 8. Definition of done (the whole climb)

Six rung artifacts on a public repo; a documented AI-acceleration + verification track record; and a capstone agentic-NetOps demo with a governance model you can defend in an interview. Built from a position of employment, conflict-free, ~6 months overlapping. (CCNA is pursued separately on your own time as a résumé keyword gate — it complements this work but isn't part of this build.)

---

## 9. The compass

Climb in order. Opus designs and checks, Codex builds, you verify against ground truth and own the push. Aim at the layer above the AI — verification + governance — and arrive at the agentic edge having understood every rung, governing the autonomy rather than just invoking it.
