# CHANGELOG.md — Progress Log

Newest entries appear at the top.

---

## 2026-07-13 — Sprint 04: Front-End Application (Citizen Portal & Police Dashboard)

### Added

- Sprint 04 Phase 4.1–4.6 completion
- Citizen Portal frontend application initialized with React, Vite, and TailwindCSS
- Implementation of the `Investigation` page with dynamic `EvidenceForm`
- Implementation of the `Results` page with `FusionVerdictCard`, `RiskScoreCard`, and `AgentResultCard`
- Strong TypeScript typing aligned to the backend schemas
- Unified Axios service layer for `POST /investigate`
- Resilient states handling (Loading, Error, and Empty fallbacks)
- App-wide routing via React Router DOM

### Verified

- Frontend adheres strictly to presentation responsibilities without duplicating backend logic
- `npm run build` succeeds with zero errors (1847 modules transformed)
- 180 backend tests continue to pass (100% success rate)

---

## 2026-07-13 — Sprint 03: Intelligence Fusion & Orchestration

### Added

- Sprint 03 completion
- Fusion Agent
- Orchestrator Agent
- `POST /investigate` endpoint
- Canonical `AgentResult` response model
- Async parallel execution and fan-out orchestration
- Case lifecycle tracking (`case_id`)
- Cross-agent communication logic
- Weighted rule-based risk aggregation

### Improved

- Strong typing across orchestration boundaries
- Public service interfaces for Agents, decoupling inference logic from orchestration
- Strict architecture boundaries enforced
- Consistent logging with `case_id`

### Verified

- 180 passing tests (100% success rate)
- Backward compatibility maintained for agent-specific endpoints
- No ML inference logic inside Fusion (purely rule-based)
- Existing APIs unchanged

---

## 2026-07-13 — Sprint 02: AI Agent Implementation

### Added

- Sprint 02 completion
- Currency Agent implementation
- Scam Communication Agent implementation
- Fraud Agent implementation
- Shared Infrastructure (Logging, Configuration, Loaders, Exceptions)
- FastAPI API layer (`/currency/analyze`, `/scam/sms`, `/scam/url`, `/fraud/analyze`)
- Extensive repository-wide QA (formatting, linting, type-checking)
- Integration tests ensuring architectural boundaries

### Verified

- 170 passing tests (100% success rate)
- 94% test coverage
- Strict layering architecture (API → Agents → Infrastructure → Models)
- Consistent singleton logic and API response schemas

---

## 2026-07-13 — Sprint 01: Dataset Engineering & Machine Learning

### Added

- Sprint 01 completion
- Currency model completed
- SMS model completed
- Phishing model completed
- Fraud model completed

### Verified

- Repository ready for AI Agent implementation

---

## 2026-07-11 — Sprint 00: Project Planning & Repository Foundation

### Added

- Initialized Git repository
- Connected GitHub remote
- Established Engineering Operating System (EOS)
- Added complete repository structure
- Added PROJECT_STRUCTURE.md
- Added dependency management
- Added configuration management
- Added module README files
- Added architecture documentation
- Added API documentation
- Added database documentation
- Added deployment documentation
- Added presentation documentation

### Verified

- Repository structure
- Folder hierarchy
- Agent architecture
- API contract
- Database schema
- Documentation consistency

### Not Implemented (By Design)

- AI Agents
- Backend services
- FastAPI endpoints
- Machine learning models
- Database migrations

### Next

Sprint 01 — Dataset Engineering