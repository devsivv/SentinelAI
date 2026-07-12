#!/usr/bin/env python3
"""
download_models.py — fetches pretrained model checkpoints referenced in
configs/models.yaml (e.g. Whisper-small, ASVspoof checkpoint) so they don't
get committed to git (see SYSTEM_RULES.md §3 — model artifacts are git-ignored).

Fill in real download logic per model as each stretch agent is built.
"""


def download_whisper_small():
    # faster-whisper pulls this automatically on first use; documented here
    # for visibility, not because a manual download step is required.
    print("Whisper-small is fetched automatically by faster-whisper on first run.")


def download_asvspoof_checkpoint():
    raise NotImplementedError(
        "Add the actual ASVspoof pretrained checkpoint URL here when Phase 5 is attempted."
    )


if __name__ == "__main__":
    download_whisper_small()
