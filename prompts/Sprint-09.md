# Sprint 09 — Orchestrator Agent `[MVP]`

Paste `PROJECT_CONTEXT.md` here first.

We are working on **Phase 9 — Orchestrator Agent (MVP)** of SentinelAI.

**Objective:** Coordinate all active agents. No AI inference itself.

**Scope for this sprint:** `POST /investigate` (per `docs/api.md`) fans out to active agents in parallel (`asyncio.gather`), writes each result to `agent_results`, calls the Fusion Agent, returns the final report. Must degrade gracefully if an agent times out or errors — partial fusion over whichever agents responded, not a hard failure.

**Constraints:** Follow `SYSTEM_RULES.md` / `AI_GUIDELINES.md`. Adding/removing a stretch agent should be a config change (`configs/agents.yaml`), not a code rewrite.

**Deliverables:** `backend/orchestrator/main.py`, smoke test `tests/test_api.py`.

**Done when:** A single request produces per-agent results plus a fused final report, and survives one agent being down.

At the end, list what should change in `PROJECT_CONTEXT.md`, `CHANGELOG.md`, and `TODO.md`.
