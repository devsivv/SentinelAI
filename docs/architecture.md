# Architecture

## System Diagram

```text
Citizen / Police / Bank / Telecom
                │
                ▼
        Orchestrator Agent (FastAPI, async fan-out)
                │
  ┌─────────────┼─────────────┬─────────────┬─────────────┐
  ▼             ▼             ▼             ▼             ▼
Scam Comm.  Fraud (txn)   Currency     Graph Agent    Geo Agent
  Agent        Agent         Agent     (NetworkX)    (Haversine)
  │             │             │             │             │
  └─────────────┴──────┬──────┴─────────────┴─────────────┘
                       ▼
           Intelligence Fusion Agent
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

## Graph Intelligence Agent & NetworkX Architecture

The **Graph Intelligence Agent** is implemented as a specialized agent that sits alongside the other analytical agents (Fraud, Scam Communication, Currency, Geo). 

### Why It Exists
Single-point indicators (like a single suspicious transaction or phishing SMS) are often insufficient to flag complex fraud rings. The Graph Intelligence Agent acts as a correlation engine across multiple cases, victims, suspects, and technical identifiers, allowing SentinelAI to detect coordinated cyber-financial fraud operations.

### Multi-Agent Integration
1. **Parallel Execution**: The Orchestrator fans out raw evidence (SMS, URL, Transaction, etc.) to the Fraud, Scam Communication, Currency, and Geo agents. Concurrently, it sends all raw evidence to the Graph Agent.
2. **Dynamic Ingest**: The Graph Agent extracts and normalizes entities/relationships from the raw evidence and populates a shared, global in-memory multi-graph.
3. **Verdict Production**: The Graph Agent computes network risk scores and returns a canonical `AgentResult` response, which is fed to the Fusion Agent.
4. **Weighted Reasoning**: The Fusion Agent counts Graph Agent findings as fraud indicators, facilitating aggregate escalation (e.g., triggering digital arrest warnings or freezing mule account networks).

## Geo Intelligence Agent & Spatial Heuristics Architecture

The **Geo Intelligence Agent** evaluates spatial incident datasets to compute relative crime density, identify local hotspots, cluster incidents geographically, and plan patrol routes.

### Multi-Agent Integration & Contextual Fusion
1. **Parallel Execution**: When an investigation request contains location evidence (`input_type: "location"`), the Orchestrator fans out the payload to the Geo Agent concurrently via `asyncio.gather`.
2. **Spatial Risk & Density**: The Geo Agent calculates the Haversine great-circle distance relative to seeded historical incidents, evaluates local crime density per km², and detects hotspot boundaries.
3. **Contextual Risk Modifier**: In `backend/fusion_agent/logic.py`, Geo findings act as a contextual risk modifier ($\pm 5$ risk score adjustment). Core verdicts (Fraud, Scam, Currency, Graph) remain primary, ensuring spatial history alone cannot falsely create a high-risk fraud verdict without supporting primary evidence.

## Communication

Plain REST between agents. No message broker (Celery/Redis) — real setup cost for little demo value at this scale; noted as a production scaling path in `deployment.md`, not built.

## Track Legend

- **MVP** — Orchestrator, Fraud Agent, Scam Comm. Agent, Fusion Agent, minimal Dashboard
- **Stretch** — Currency Agent, Graph Agent, Geo Agent (Completed)
- **Future** — full Police Portal, production database persistence, live dispatch/FIR/account-freeze automation

See `MASTER_PLAN.md` for the full phase-by-phase detail behind each box in this diagram.
