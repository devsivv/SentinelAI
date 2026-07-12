# SYSTEM_RULES.md

Non-negotiable rules for this codebase. Every human sprint and every AI coding session (ChatGPT, Claude, Cursor, Claude Code, etc.) must follow these without being reminded each time. If a rule and a shortcut conflict, the rule wins — these exist specifically to survive the "just this once" pressure of a hackathon timeline.

For *how to prompt/instruct an AI assistant*, see `AI_GUIDELINES.md`. This file is about the code and repo, not the AI interaction style.

---

## 1. API & Data Contracts

- Every API is built with **FastAPI + Pydantic** models — no raw dicts as request/response bodies.
- Every AI agent exposes exactly one inference endpoint: **`POST /analyze`**.
- Every agent response follows the **Agent Contract** defined in `docs/api.md` — no exceptions, no agent-specific response shapes. If an agent needs extra fields, they go inside `evidence`, not as new top-level keys.
- Breaking the contract to "make one agent work faster" breaks the Orchestrator and Fusion Agent for everyone — don't.

## 2. No Duplicate Business Logic

- Verdict/risk-scoring logic lives in exactly one place per agent (`agents/<agent>/model.py` or equivalent) — not copy-pasted into the API layer, the Orchestrator, and the Fusion Agent.
- Fusion/aggregation logic lives only in `backend/fusion_agent/` — agents do not pre-aggregate or guess at final verdicts.
- Shared code (the Pydantic contract models, config loading, logging setup) lives in a shared module, not copied into every agent folder.

## 3. Models & Experiments

- All trained model artifacts are saved under `models/<agent>/` — never inside `agents/<agent>/` or committed loose in the repo root.
- Model files are **git-ignored** (see `.gitignore`) — commit code and configs, not weights. Large files go via `scripts/download_models.py` or a release asset, not `git add`.
- Every experiment (a training run, a model variant) gets its own folder under `experiments/<domain>/exp_NN_<description>/` (e.g. `experiments/fraud/exp_02_lightgbm/`) with at minimum: the training script/notebook used, the resulting metrics, and a one-line note on what changed from the previous experiment.
- Promoting an experiment to production means copying its output into `models/<domain>/` and recording which `exp_NN` it came from in that model's README.

## 4. Configuration

- No hardcoded paths, hostnames, ports, dataset paths, or model paths in agent/backend code — read them from `configs/*.yaml` (see `docs/deployment.md` for how config is loaded).
- `development.yaml` is the default; `production.yaml` is aspirational/future-scope (see `MASTER_PLAN.md` Phase 11) but should still exist as a stub so the switch is a one-line change, not a rewrite.

## 5. Every Sprint Must Update

At the end of every sprint (see `MASTER_PLAN.md` for phase boundaries):
- [ ] `PROJECT_CONTEXT.md` — current phase, status, next objective, blockers
- [ ] `CHANGELOG.md` — one dated entry, short
- [ ] `TODO.md` — completed items removed, next batch added

## 6. Every Sprint Should Include

- [ ] At minimum a smoke test in `tests/` for any new endpoint (does it respond with contract-shaped JSON on a trivial input?)
- [ ] A short doc update in `docs/` if the sprint changed an API shape, schema, or architecture decision
- [ ] An updated `README.md` in the relevant subfolder if a new agent/service was added

Tests are lightweight by design (see `tests/README` pattern) — the goal is catching integration breakage before a demo, not full coverage.

## 7. Logging

- Agents and the Orchestrator log to `logs/<component>/` (git-ignored, see `.gitignore`), not stdout-only, so a failed demo run can be debugged afterward.
- Log at minimum: request received, verdict returned, and errors with the `case_id` — `case_id` is the join key across every log and report, always include it.

## 8. Scope Discipline

- Anything in `MASTER_PLAN.md`'s "Future scope" column does not get built, no matter how small it seems in the moment. If it feels necessary, it belongs on a slide in `docs/presentation.md`, not in the codebase.
- A stretch phase is not started until the MVP phases are demo-safe end-to-end (see `MASTER_PLAN.md` §Timeline).
