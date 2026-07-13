# Sprint 10 — Dashboard `[MVP: minimal version; full version is Stretch/Future]`

Paste `PROJECT_CONTEXT.md` here first.

We are working on **Phase 10 — Dashboard** of SentinelAI.

**Scope for this sprint (MVP first):** One flow — submit input (SMS text / transaction / URL) → see per-agent verdicts → see fused verdict → see recommended action. This alone is a complete, demoable product; stop here unless MVP phases are done with days to spare.

**Stretch additions (only after MVP dashboard works):** Citizen Portal features (scan currency, upload voice, report fraud). Do not build the full Police Portal (live alerts, analytics, heatmaps, investigation reports) — that's Future scope per `MASTER_PLAN.md`.

**Constraints:** Follow `SYSTEM_RULES.md` / `AI_GUIDELINES.md`. Calls the Orchestrator's `/investigate`, not individual agents directly.

**Deliverables:** `frontend/citizen-portal/` MVP flow.

**Done when:** A user can submit evidence and see the full agent → fusion → recommendation chain in the UI.

At the end, list what should change in `PROJECT_CONTEXT.md`, `CHANGELOG.md`, and `TODO.md`.
