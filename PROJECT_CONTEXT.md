# PROJECT_CONTEXT.md — Live Snapshot

Paste this file at the start of every new build session/chat so it starts with full context. **Update it at the end of every sprint** — this file, not `MASTER_PLAN.md`, is what changes day to day.

---

```md
Project: SentinelAI – Agentic Digital Public Safety Intelligence Platform

Track:
MVP

Current Phase:
Sprint 08 — Geo Intelligence Agent & Police Dashboard Integration (Completed)

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

### Police Dashboard (Sprint 05)
- Police Dashboard MVP Foundation
- Case Management (Search, Filters, Sorting)
- Case Details & Investigation Review
- Fusion Summary & Agent Result Cards
- Evidence Panel & Timeline
- Recommended Actions & Responsive UI
- Live backend integration using the `POST /investigate` endpoint
- Loading & Error state handling
- *Limitation*: No persistent case database; lists remain mock-driven due to backend design.

### Production Readiness & Handoff (Sprint 06)
- Centralized CORS origins and API version into `core/config.py` (`AppConfig`, `API_VERSION`)
- Fixed type annotations and PEP 8 import ordering across backend and frontend
- Expanded `.env.example` with CORS origins, log levels, and per-agent model paths
- Standardized local startup commands and updated deployment guide

### Graph Intelligence Agent (Sprint 07)
- Implemented in-memory multi-graph using NetworkX
- Created entity extraction and normalization pipeline
- Added connected component, degree centrality, repeated identity, and suspicious cluster (fraud ring) detection
- Integrated with Orchestrator (fans out in parallel) and Fusion Agent
- Added standard `POST /graph/analyze` API route
- Tested with thread-safe graph insertion and API mock fixtures

### Geo Intelligence Agent & Police Dashboard Integration (Sprint 08)
- Created `agents/geo_agent/` module with coordinate validation, Haversine formula, crime density calculations, hotspot detection, and leader clustering heuristics
- Exposed standard `POST /geo/analyze` API endpoint
- Integrated Geo Agent into Orchestrator (fans out in parallel) and Fusion Agent (contextual risk modifier)
- Integrated Leaflet, React Leaflet, and OpenStreetMap interactive mapping into the Police Dashboard (`GeoIntelligencePanel.tsx`)
- Added density overlay toggle, cluster layer toggle, district overview, distance-sorted nearby incidents panel, and patrol recommendations card
- Comprehensive test coverage with 206 backend tests passing and 0 frontend lint/build warnings

Current Status:

- **Sprint 00**: Completed
- **Sprint 01**: Completed
- **Sprint 02**: Completed
- **Sprint 03**: Completed
- **Sprint 04**: Completed
- **Sprint 05**: Completed
- **Sprint 06**: Completed
- **Sprint 07**: Completed
- **Sprint 08**: Completed

**Repository now contains:**
- `datasets/` (currency, sms, phishing, transactions)
- `models/` (currency, sms, phishing, transactions)
- `agents/` (Currency, Scam Communication, Fraud, Graph, Geo)
- `core/` (Shared configuration, logging, exceptions, loaders)
- `api/` (FastAPI layer with endpoints for each agent, plus Orchestrator `/investigate`, Graph `/graph/analyze`, and Geo `/geo/analyze`)
- `backend/` (Orchestrator and Fusion Agent)
- `frontend/citizen-portal/` (React application)
- `frontend/police-dashboard/` (React application with Geo Intelligence interactive mapping)
- `tests/` (206 tests passing, including unit and integration tests)

**Testing & Coverage:**
- 206 passing tests (100% success rate)
- 96% overall repository coverage
- Strict architectural boundaries verified

**Machine Learning:** Completed.
**AI Agents & API Layer:** Completed.
**Intelligence Fusion & Orchestration:** Completed.
**Frontend Integration:** Completed.
**Graph Intelligence:** Completed.
**Geo Intelligence & Interactive Mapping:** Completed.

Overall Progress: 100% (Sprint 08 Completed)

Next Objective:

Hackathon Pitch & Final System Demonstration

Immediate goals:
1. Conduct final repository dry-run
2. Present SentinelAI full multi-agent intelligence platform to hackathon judges

Blockers:

- None

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