# Sprint 01 — Dataset Engineering `[MVP, scoped down]`

Paste `PROJECT_CONTEXT.md` here first.

We are working on **Phase 1 — Dataset Engineering (MVP, scoped down)** of SentinelAI.

**Objective:** Clean, standardized datasets — build per-agent, just before that agent's phase, not all five upfront.

**Scope for this sprint:** Only the datasets needed for the current MVP agent (Fraud or Scam Comm. — check `PROJECT_CONTEXT.md` for which is next). Do not preprocess stretch-agent (Currency/Voice) datasets yet.

**Constraints:**
- Follow `SYSTEM_RULES.md` and `AI_GUIDELINES.md`.
- Use the exact datasets listed in `docs/api.md` §Data Sources.
- Apply class balancing (SMOTE / class-weighting) for imbalanced sets — note this explicitly in the script, don't silently skip it.
- Save cleaned data under `datasets/<domain>/`, scripts under `scripts/` or the agent's own folder — not scattered.

**Deliverables:** `prepare_data.py` (or per-domain cleaning scripts), dataset documentation noting source, size, class balance, and any label decisions.

**Done when:** The dataset for the current MVP agent is ready and documented.

At the end, list what should change in `PROJECT_CONTEXT.md`, `CHANGELOG.md`, and `TODO.md`.
