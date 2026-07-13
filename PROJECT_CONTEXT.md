# PROJECT_CONTEXT.md — Live Snapshot

Paste this file at the start of every new build session/chat so it starts with full context. **Update it at the end of every sprint** — this file, not `MASTER_PLAN.md`, is what changes day to day.

---

```md
Project: SentinelAI – Agentic Digital Public Safety Intelligence Platform

Track:
MVP

Current Phase:
Sprint 03 — Intelligence Fusion & Orchestration

Completed:

### Repository
- Repository initialized
- Engineering Operating System completed
- Project folder structure finalized
- Documentation completed
- Configuration management completed
- Dependency management completed

### Machine Learning

**Currency Agent**
- Dataset engineering completed
- EDA completed
- Data cleaning completed
- Data augmentation completed
- Train/Validation/Test split completed
- Transfer learning completed
- Compared MobileNetV2, EfficientNet-B0 and ResNet18
- Selected MobileNetV2
- Implemented Grad-CAM
- Exported production model

**SMS Scam Detection**
- Dataset engineering completed
- Comprehensive EDA completed
- Text preprocessing completed
- TF-IDF feature engineering completed
- Compared multiple classifiers
- Hyperparameter tuning completed
- Selected Linear SVM
- Exported model
- Exported TF-IDF vectorizer

**Phishing URL Detection**
- Dataset engineering completed
- Feature engineering completed
- Model comparison completed
- Exported production model

**Fraud Detection**
- PaySim dataset prepared
- Feature engineering completed
- Model comparison completed
- Exported production model

Current Status:

- **Sprint 00**: Completed
- **Sprint 01**: Completed
- **Sprint 02**: Completed
- **Sprint 03**: Ready to Begin

**Repository now contains:**
- `datasets/` (currency, sms, phishing, transactions)
- `models/` (currency, sms, phishing, transactions)
- `agents/` (Currency, Scam Communication, Fraud)
- `core/` (Shared configuration, logging, exceptions, loaders)
- `api/` (FastAPI layer with endpoints for each agent)
- `tests/` (170 tests passing, including unit and integration tests)

**Testing & Coverage:**
- 170 passing tests (100% success rate)
- 94% overall repository coverage
- Strict architectural boundaries verified

**Machine Learning:** Completed.
**AI Agents & API Layer:** Completed.

Overall Progress: ~65%

Next Objective:

Sprint 03 — Intelligence Fusion & Orchestration

Immediate goals:
1. Build Intelligence Fusion Agent (Risk aggregation).
2. Build Orchestrator Agent (Task routing and fan-out).
3. Establish robust cross-agent communication logic.
4. Implement tracking by `case_id`.
5. Integrate Fusion & Orchestrator with FastAPI layer.

Blockers:

- None

Technology Stack:

- Python 3.13 (Development)
- FastAPI
- React
- PostgreSQL
- NetworkX (Neo4j deferred until Phase 7)
- Docker

Reference:

- MASTER_PLAN.md
- PROJECT_STRUCTURE.md
- docs/architecture.md
- docs/api.md
- docs/database.md
```

---

## How to use this file

1. Paste this file at the beginning of every new AI session.
2. Update it after every sprint.
3. Update CHANGELOG.md and TODO.md together.
4. If project scope changes, update MASTER_PLAN.md as well.