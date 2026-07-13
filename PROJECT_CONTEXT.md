# PROJECT_CONTEXT.md — Live Snapshot

Paste this file at the start of every new build session/chat so it starts with full context. **Update it at the end of every sprint** — this file, not `MASTER_PLAN.md`, is what changes day to day.

---

```md
Project: SentinelAI – Agentic Digital Public Safety Intelligence Platform

Track:
MVP

Current Phase:
Sprint 05 — Advanced Features & Optimization (Ready to Begin)

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

### Intelligence Fusion & Orchestration (Sprint 03)
- Fusion Agent
- Orchestrator Agent
- Unified investigation endpoint (`/investigate`)
- Canonical AgentResult
- Strongly typed communication
- Async parallel execution
- Case lifecycle (`case_id`)
- Rule-based weighted aggregation
- Cross-agent communication

### Front-End Application (Sprint 04)
- React Vite application initialized
- TailwindCSS styling implemented
- React Router DOM integrated
- Frontend `Investigation` workflow
- Frontend `Results` visualization cards
- End-to-end API integration with the `/investigate` endpoint
- Graceful error states, loading spinners, and empty fallbacks
- Strict TypeScript schemas aligned with Pydantic models

Current Status:

- **Sprint 00**: Completed
- **Sprint 01**: Completed
- **Sprint 02**: Completed
- **Sprint 03**: Completed
- **Sprint 04**: Completed
- **Sprint 05**: Ready to Begin

**Repository now contains:**
- `datasets/` (currency, sms, phishing, transactions)
- `models/` (currency, sms, phishing, transactions)
- `agents/` (Currency, Scam Communication, Fraud)
- `core/` (Shared configuration, logging, exceptions, loaders)
- `api/` (FastAPI layer with endpoints for each agent, plus Orchestrator `/investigate`)
- `backend/` (Orchestrator and Fusion Agent)
- `frontend/citizen-portal/` (React application)
- `tests/` (180 tests passing, including unit and integration tests)

**Testing & Coverage:**
- 180 passing tests (100% success rate)
- 94% overall repository coverage
- Strict architectural boundaries verified

**Machine Learning:** Completed.
**AI Agents & API Layer:** Completed.
**Intelligence Fusion & Orchestration:** Completed.
**Frontend Integration:** Completed.

Overall Progress: ~85%

Next Objective:

Sprint 05 — Advanced Features & Optimization

Immediate goals:
1. Connect existing agents to new frontend dashboards.
2. Begin working on Police Dashboard interface.
3. Plan data visualizations for dashboard.

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