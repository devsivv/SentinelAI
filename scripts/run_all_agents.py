#!/usr/bin/env python3
"""
run_all_agents.py — starts the Orchestrator, Fusion Agent, and every agent
listed as active in configs/agents.yaml as background subprocesses.

Usage: python scripts/run_all_agents.py
Stop with Ctrl+C — all child processes are terminated on exit.
"""

import signal
import subprocess
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
processes = []


def start(module: str, port: int):
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", f"{module}:app", "--port", str(port)],
        cwd=ROOT,
    )
    processes.append(proc)


def main():
    with open(ROOT / "configs" / "agents.yaml") as f:
        cfg = yaml.safe_load(f)

    start("backend.orchestrator.main", 8000)
    start("backend.fusion_agent.main", 8010)
    for agent in cfg.get("active_agents", []):
        port = int(agent["url"].rsplit(":", 1)[-1])
        start(f"agents.{agent['name']}.main", port)

    def shutdown(*_):
        for p in processes:
            p.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    print(f"Running {len(processes)} services. Ctrl+C to stop.")
    for p in processes:
        p.wait()


if __name__ == "__main__":
    main()
