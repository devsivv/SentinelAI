# Sprint 06 — Intelligence Fusion Agent `[MVP]`

Paste `PROJECT_CONTEXT.md` here first.

We are working on **Phase 6 — Intelligence Fusion Agent (MVP)** of SentinelAI. **This phase must not slip past Day 3 of the build — it's what judges care about most.**

**Objective:** Central reasoning engine. Consumes standard-contract outputs from all active agents for a `case_id` from the `agent_results` table — does not analyze raw data itself.

**Scope for this sprint:** Weighted aggregation of `risk_score` across agents + a small rules layer (e.g. "if 2+ agents report fraud with risk_score > 80, escalate to organized-scam verdict"). No ML model required — this is a legitimate reasoning engine for the demo as specified.

**Constraints:** Follow `SYSTEM_RULES.md` / `AI_GUIDELINES.md`. Fusion/aggregation logic lives only here, per `SYSTEM_RULES.md` §2 — not duplicated in the Orchestrator.

**Deliverables:** `backend/fusion_agent/main.py` (`POST /fuse`, per `docs/api.md`), writing to `fusion_reports`.

**Done when:** Produces a final verdict, overall risk score, narrative, and recommended actions for a multi-agent case.

At the end, list what should change in `PROJECT_CONTEXT.md`, `CHANGELOG.md`, and `TODO.md`.
