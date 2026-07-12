# Deployment

## Local (build this — Phase 0/9)

`docker-compose.yml` at the repo root runs Postgres (and Neo4j, if Phase 7 is attempted) for local development. Agents and the Orchestrator run directly via `uvicorn` during the build, not containerized — containerizing each agent is extra setup time with no demo value.

```bash
docker compose up -d db
uvicorn backend.orchestrator.main:app --reload --port 8000
uvicorn agents.fraud_agent.main:app --reload --port 8001
uvicorn agents.scam_comm_agent.main:app --reload --port 8002
uvicorn backend.fusion_agent.main:app --reload --port 8010
```

Or simply: `python scripts/run_all_agents.py`, which reads `configs/agents.yaml` and starts everything active in one command.

## Production — `[Future scope, not built]`

The following belong on a roadmap slide (`presentation.md`), not in this build:

- Dockerfiles per agent + full `docker-compose.yml` (all services containerized)
- Nginx reverse proxy / TLS termination
- Redis + Celery for async job queues at scale
- GitHub Actions CI/CD
- Cloud deployment (managed Postgres/Neo4j, container orchestration)
- Multi-tenant auth, live police dispatch integration, automated FIR filing, automated account-freeze

Treat Phase 11 as the most common way hackathon teams run out of time — a local Compose file covering the DB is enough. Spend the time this would take on hardening the MVP instead (see `MASTER_PLAN.md` §Timeline, Day 5).
