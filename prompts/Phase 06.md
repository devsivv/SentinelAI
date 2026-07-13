# Sprint 07 — Graph Intelligence Agent `[Stretch]`

Paste `PROJECT_CONTEXT.md` here first.

**Only attempt if MVP + at most one other stretch phase are already solid — confirm in `PROJECT_CONTEXT.md`.**

We are working on **Phase 7 — Graph Intelligence Agent (Stretch)** of SentinelAI.

**Objective:** Identify fraud rings, mule accounts, shared devices, repeat offenders.

**Scope for this sprint:** Neo4j graph model from `docs/database.md`, OR the NetworkX in-memory fallback if Neo4j setup is eating time — decide up front, don't discover this mid-sprint.

**Constraints:** Follow `SYSTEM_RULES.md` / `AI_GUIDELINES.md`.

**Deliverables:** `agents/graph_agent/main.py`, a visualization (pyvis/matplotlib if using the NetworkX fallback).

**Done when:** Given a case's linked entities, returns identified fraud rings/mule patterns in contract-shaped JSON plus a visual.

At the end, list what should change in `PROJECT_CONTEXT.md`, `CHANGELOG.md`, and `TODO.md`.
