# SentinelAI – Agentic Digital Public Safety Intelligence Platform

SentinelAI acts as an intelligent digital police officer. Instead of a single model answering queries, multiple specialized AI agents investigate incoming evidence, share intelligence with each other, correlate evidence across sources, and generate a unified threat assessment with recommended actions — for law enforcement, banks, telecom providers, and citizens.

This repo is organized as a living blueprint, not a one-off spec. Start here, then go to the file that matches what you're doing right now:

| I want to... | Go to |
|---|---|
| See the full roadmap and what's MVP vs. Stretch vs. Future | [`MASTER_PLAN.md`](./MASTER_PLAN.md) |
| Start a new build session / hand off context to a new chat | [`PROJECT_CONTEXT.md`](./PROJECT_CONTEXT.md) + the matching [`prompts/Sprint-NN.md`](./prompts) |
| See what's done so far | [`CHANGELOG.md`](./CHANGELOG.md) |
| See what's being worked on right now | [`TODO.md`](./TODO.md) |
| Know the non-negotiable engineering rules | [`SYSTEM_RULES.md`](./SYSTEM_RULES.md) |
| Brief an AI coding assistant (Claude Code, Cursor, ChatGPT...) | [`AI_GUIDELINES.md`](./AI_GUIDELINES.md) |
| Understand the system architecture and agent contract | [`docs/architecture.md`](./docs/architecture.md) |
| See API endpoints / request-response shapes | [`docs/api.md`](./docs/api.md) |
| See the database schema | [`docs/database.md`](./docs/database.md) |
| Set up or deploy the system | [`docs/deployment.md`](./docs/deployment.md) |
| Prep slides / demo script / judge Q&A | [`docs/presentation.md`](./docs/presentation.md) |
| Reuse a per-phase prompt instead of rewriting it | [`prompts/`](./prompts) |

## Quick Start

```bash
git clone <repo-url> && cd SentinelAI
cp .env.example .env
python scripts/start_project.py   # brings up db, prints next steps
# or, once agents exist:
python scripts/run_all_agents.py  # starts orchestrator + fusion + all active agents
```

See [`docs/deployment.md`](./docs/deployment.md) for the full local setup and what's in/out of scope for a hackathon build.

## Current Status

Check [`PROJECT_CONTEXT.md`](./PROJECT_CONTEXT.md) for the live "where are we right now" snapshot — that file, not this README, is the source of truth for current phase and next objective.

## Tech Stack

Python 3.12 · FastAPI · React · PostgreSQL · Neo4j (or NetworkX fallback) · Docker

## Development Workflow

This repository follows an Engineering Operating System (EOS).

Development proceeds sprint-by-sprint.

Before every implementation:

1. Read PROJECT_CONTEXT.md
2. Read MASTER_PLAN.md
3. Read SYSTEM_RULES.md
4. Read PROJECT_STRUCTURE.md
5. Implement only the active sprint
6. Update CHANGELOG.md, PROJECT_CONTEXT.md and TODO.md

## Repo Structure

```
SentinelAI/
│
├── README.md                 ← You are here
├── MASTER_PLAN.md             ← Complete roadmap (MVP/Stretch/Future, timeline, risks)
├── PROJECT_CONTEXT.md         ← Live snapshot, updated after every sprint
├── CHANGELOG.md               ← Dated progress log
├── TODO.md                    ← Current sprint tasks only
├── SYSTEM_RULES.md            ← Non-negotiable engineering rules
├── AI_GUIDELINES.md           ← How to brief any AI coding assistant
├── docker-compose.yml         ← Local dev DB only
├── .env.example
│
├── docs/
│   ├── architecture.md        ← System design + agent contract
│   ├── api.md                  ← Endpoint specs + data sources
│   ├── database.md             ← Postgres + Neo4j/NetworkX schema
│   ├── deployment.md           ← Local setup + future scope
│   └── presentation.md         ← Demo script + slide outline
│
├── prompts/                    ← Reusable Sprint-00.md ... Sprint-12.md, one per phase
│
├── backend/
│   ├── orchestrator/            ← MVP — routes requests, no AI inference itself
│   ├── fusion_agent/            ← MVP — central reasoning engine
│   └── db/schema.sql
│
├── agents/
│   ├── scam_comm_agent/         ← MVP
│   ├── fraud_agent/             ← MVP
│   ├── currency_agent/          ← Stretch
│   ├── voice_agent/             ← Stretch
│   ├── graph_agent/             ← Stretch
│   └── geo_agent/               ← Stretch
│
├── frontend/
│   ├── citizen-portal/
│   └── police-dashboard/
│
├── configs/                     ← development.yaml, production.yaml, datasets/agents/models.yaml
├── datasets/                    ← git-ignored raw/clean data, per domain
├── models/                      ← git-ignored trained artifacts, per domain
├── experiments/                 ← exp_NN_<description> per domain, per SYSTEM_RULES.md §3
├── scripts/                     ← start_project.py, run_all_agents.py, prepare_data.py, etc.
├── tests/                       ← smoke tests, one per agent + orchestrator
├── reports/                     ← generated investigation outputs, per domain
├── logs/                        ← git-ignored runtime logs, per component
├── assets/                      ← diagrams, screenshots, demo recordings for Phase 12
├── docker/                      ← Future scope: per-agent Dockerfiles (not built yet)
└── .github/workflows/           ← minimal smoke-test CI
```
