#!/usr/bin/env python3
"""
prepare_data.py — runs the per-domain dataset cleaning scripts referenced
in configs/datasets.yaml. Each agent's Phase 1 sprint (see prompts/Sprint-01.md)
should add its own cleaning step here rather than a separate ad-hoc script.

Usage: python scripts/prepare_data.py --domain fraud
"""

import argparse


def prepare_fraud():
    raise NotImplementedError(
        "Add transaction dataset cleaning here (Phase 1 / Phase 3 sprint)."
    )


def prepare_sms():
    raise NotImplementedError(
        "Add SMS + hand-labeled scam dataset cleaning here (Phase 1 / Phase 4 sprint)."
    )


def prepare_phishing():
    raise NotImplementedError(
        "Add phishing URL dataset cleaning here (Phase 1 / Phase 4 sprint)."
    )


DOMAINS = {
    "fraud": prepare_fraud,
    "sms": prepare_sms,
    "phishing": prepare_phishing,
    # "currency": prepare_currency,   # add when Phase 2 is attempted
    # "voice": prepare_voice,          # add when Phase 5 is attempted
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", required=True, choices=DOMAINS.keys())
    args = parser.parse_args()
    DOMAINS[args.domain]()


if __name__ == "__main__":
    main()
