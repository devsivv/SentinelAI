# PROJECT_CONTEXT.md — Live Snapshot

Paste this file at the start of every new build session/chat so it starts with full context. **Update it at the end of every sprint** — this file, not `MASTER_PLAN.md`, is what changes day to day.

---

```md
Project: SentinelAI – Agentic Digital Public Safety Intelligence Platform

Track:
MVP

Current Phase:
Sprint 02 — AI Agent Implementation

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
- **Sprint 02**: Ready to Begin

**Repository now contains:**
- `datasets/` (currency, sms, phishing, transactions)
- `models/` (currency, sms, phishing, transactions)

**Machine Learning:** Completed.

Overall Progress: ~50%

Next Objective:

Sprint 02 — AI Agent Implementation

Immediate goals:
1. Build Currency Agent.
2. Implement shared model loading utilities.
3. Build Currency inference service.
4. Create Currency FastAPI endpoint.
5. Add smoke tests.

After Currency Agent is complete, continue with:
- Scam Communication Agent
- Fraud Agent

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