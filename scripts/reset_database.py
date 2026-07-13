#!/usr/bin/env python3
"""
reset_database.py — drops and re-applies backend/db/schema.sql against the
local dev database. Destructive; local/dev use only, never point this at
a production config.
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    confirm = input("This will WIPE the local dev database. Type 'yes' to continue: ")
    if confirm.strip().lower() != "yes":
        print("Aborted.")
        return
    subprocess.run(
        [
            "psql",
            "-h",
            "localhost",
            "-U",
            "sentinelai",
            "-d",
            "sentinelai_dev",
            "-f",
            str(ROOT / "backend" / "db" / "schema.sql"),
        ],
        check=True,
    )
    print("Schema re-applied.")


if __name__ == "__main__":
    main()
