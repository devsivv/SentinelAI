#!/usr/bin/env python3
"""
start_project.py — one-command local bring-up for SentinelAI.

Reads configs/development.yaml, starts Postgres via docker compose,
applies backend/db/schema.sql, then prints the uvicorn commands needed
to bring up the Orchestrator, Fusion Agent, and any active agents from
configs/agents.yaml.

This is a convenience wrapper, not a process manager — it does not
daemonize agents. For that, use run_all_agents.py.
"""
import subprocess
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    print("[1/3] Starting database (docker compose up -d db)...")
    subprocess.run(["docker", "compose", "up", "-d", "db"], cwd=ROOT, check=True)

    print("[2/3] Applying schema (backend/db/schema.sql)...")
    # NOTE: fill in real connection details once configs/development.yaml
    # env vars are wired up; left as a manual step placeholder intentionally.
    print("      -> run: psql -h localhost -U sentinelai -d sentinelai_dev -f backend/db/schema.sql")

    print("[3/3] Active agents (from configs/agents.yaml):")
    with open(ROOT / "configs" / "agents.yaml") as f:
        cfg = yaml.safe_load(f)
    for agent in cfg.get("active_agents", []):
        print(f"      -> uvicorn agents.{agent['name']}.main:app --reload --port "
              f"{agent['url'].rsplit(':', 1)[-1]}")
    print(f"      -> uvicorn backend.orchestrator.main:app --reload --port 8000")
    print(f"      -> uvicorn backend.fusion_agent.main:app --reload --port 8010")


if __name__ == "__main__":
    sys.exit(main())
