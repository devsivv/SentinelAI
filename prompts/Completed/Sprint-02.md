# Sprint 02 — Currency Agent `[Stretch]`

Paste `PROJECT_CONTEXT.md` here first.

**Only start this sprint if the MVP phases (0,1,3,4,6,9,10) are already demo-safe end-to-end — confirm in `PROJECT_CONTEXT.md` before proceeding.**

We are working on **Phase 2 — Currency Agent (Stretch)** of SentinelAI.

**Objective:** Detect counterfeit Indian currency from an image.

**Scope for this sprint:** CNN/YOLO model OR the rule-based watermark-region fallback (`docs/api.md`) if data quality/time is short — pick one, don't attempt both. FastAPI service matching the Agent Contract. Grad-CAM explainability, budgeted as real work, not assumed free.

**Constraints:** Follow `SYSTEM_RULES.md` / `AI_GUIDELINES.md`. Save the trained model under `models/currency/`. Log the experiment under `experiments/currency/exp_NN_<description>/`.

**Deliverables:** `agents/currency_agent/{train.py, predict.py, main.py}`, evaluation results (precision/recall, not just accuracy).

**Done when:** Model evaluated on real images, returns contract-shaped JSON via `/analyze`.

At the end, list what should change in `PROJECT_CONTEXT.md`, `CHANGELOG.md`, and `TODO.md`.
