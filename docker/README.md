# docker/

Per-agent Dockerfiles are **Future scope** (`MASTER_PLAN.md` Phase 11 / `docs/deployment.md`).
The local dev build only needs the root `docker-compose.yml` (Postgres, optionally Neo4j).

When Phase 11 is actually attempted, each Dockerfile goes here, named `Dockerfile.<agent>`,
and gets wired into a full `docker-compose.prod.yml` — not built during the hackathon window.
