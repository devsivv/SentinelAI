# Architecture

## System Diagram

```text
Citizen / Police / Bank / Telecom
                │
                ▼
        Orchestrator Agent (FastAPI, async fan-out)
                │
 ┌──────────────┼───────────────┬────────────────┐
 ▼              ▼                ▼                ▼
Scam Comm.   Fraud (txn)   Currency [stretch]  Voice [stretch]
 Agent         Agent          Agent               Agent
   │              │                │                │
   └──────────────┴────────┬───────┴────────────────┘
                            ▼
                Intelligence Fusion Agent
                            │
             ┌──────────────┴──────────────┐
             ▼                              ▼
     Graph Agent [stretch]           Geo Agent [stretch]
                            │
                            ▼
                 Alert & Report Agent
                            │
                            ▼
          Police Dashboard / Citizen App (React)
```
All agents communicate only through the Orchestrator.

Agents never call each other directly.

The Fusion Agent consumes only the Standard Agent Contract.

The Orchestrator and Fusion Agent perform **no AI inference themselves**. All intelligence lives in the specialized agents; the Orchestrator routes, the Fusion Agent reasons over already-produced verdicts.

## Standard Agent Contract

Every specialized agent — regardless of what it analyzes — exposes one FastAPI endpoint and returns one JSON shape. This is what makes the system genuinely agentic instead of a fixed pipeline: the Fusion Agent only ever needs to understand *this* schema, never each agent's internals, and any agent can be mocked with a static JSON file while its real model is still being built.

**Endpoint:** `POST /analyze` (full request/response spec: `api.md`)

Enforcing this from day one means:
- Orchestrator calls agents in parallel (`asyncio.gather`) instead of sequentially
- Fusion Agent logic is a simple aggregator over a list of contract objects, not custom per-agent parsing
- Agents can be added, removed, or swapped as a config change

## Communication

Plain REST between agents. No message broker (Celery/Redis) — real setup cost for little demo value at this scale; noted as a production scaling path in `deployment.md`, not built.

## Track Legend

- **MVP** — Orchestrator, Fraud Agent, Scam Comm. Agent, Fusion Agent, minimal Dashboard
- **Stretch** — Currency Agent, Voice Agent, Graph Agent, Geo Agent (pick at most one or two)
- **Future** — full Police Portal, production deployment, live dispatch/FIR/account-freeze automation

See `MASTER_PLAN.md` for the full phase-by-phase detail behind each box in this diagram.
