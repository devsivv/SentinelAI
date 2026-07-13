# Sprint 04 — Scam Communication Agent `[MVP]`

Paste `PROJECT_CONTEXT.md` here first.

We are working on **Phase 4 — Scam Communication Agent (MVP)** of SentinelAI.

**Objective:** Detect scam SMS and phishing URLs (email is optional/stretch — do not build it this sprint).

**Scope for this sprint:**
- SMS: classifier fine-tuned on the Phase 1 dataset (TF-IDF + XGBoost is an acceptable baseline if BERT/IndicBERT is too slow to get working).
- URL: feature-based XGBoost (URL length, HTTPS, special chars) — no transformer needed here.
- Both return verdict + category + risk score + explanation on the standard contract.

**Constraints:** Follow `SYSTEM_RULES.md` / `AI_GUIDELINES.md`. This agent must be real, not mocked, by the end of the MVP window (`MASTER_PLAN.md` §Timeline, Day 2).

**Deliverables:** `agents/scam_comm_agent/{train.py, predict.py, main.py}`, smoke tests `tests/test_sms.py`.

**Done when:** Returns accurate, contract-shaped verdicts for both SMS and URL inputs.

At the end, list what should change in `PROJECT_CONTEXT.md`, `CHANGELOG.md`, and `TODO.md`.
