# Sprint 03 — Fraud Agent `[MVP]`

Paste `PROJECT_CONTEXT.md` here first.

We are working on **Phase 3 — Fraud Agent (MVP)** of SentinelAI.

**Objective:** Detect fraudulent financial transactions.

**Scope for this sprint:** Train and compare XGBoost / Random Forest / LightGBM on the Phase 1 dataset. Add SHAP explainability. Build the FastAPI service on `/analyze` matching the Agent Contract exactly.

**Constraints:** Follow `SYSTEM_RULES.md` / `AI_GUIDELINES.md`. Report PR-AUC/recall, not accuracy (imbalanced data). Save each model variant under `experiments/fraud/exp_NN_<model>/`; promote the winner to `models/fraud/`.

**Deliverables:** `agents/fraud_agent/{train.py, predict.py, main.py}`, a smoke test in `tests/test_fraud.py`.

**Done when:** Best model selected and deployed locally behind `/analyze`, returning contract-shaped JSON.

At the end, list what should change in `PROJECT_CONTEXT.md`, `CHANGELOG.md`, and `TODO.md`.
