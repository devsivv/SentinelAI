# CHANGELOG.md — Progress Log

Newest entries appear at the top.

---

## 2026-07-14 — Sprint 06: Production Readiness & Handoff

### Improved

- Centralized CORS origins and API version into `core/config.py` (`AppConfig`, `API_VERSION`) — removed hardcoded values from `api/main.py` and `api/routers/health.py`
- Added `FastAPI` type annotation to `api/errors.py` `register_exception_handlers`
- Fixed PEP 8 import ordering in `backend/orchestrator/service.py` (stdlib → third-party → local)
- Added `from __future__ import annotations` to `api/routers/investigate.py` and `backend/orchestrator/service.py`
- Replaced `Optional[Path]` with `Path | None` in `agents/scam_comm_agent/sms_predict.py` (Python 3.10+ union syntax)
- Added `BackendAgentEvidence` TypeScript interface to `frontend/police-dashboard/src/types/api.ts` — eliminated `any` types in `CaseDetails.tsx` evidence mapping
- Expanded `.env.example` to document all overridable environment variables (CORS, log levels, model paths per agent)
- Rewrote `docs/deployment.md` — corrected stale per-agent uvicorn startup commands; added frontend dev server instructions

### Verified

- `python -m pytest tests/ -q` → 180 passed (100% success rate)
- `npm run lint && npm run build` (citizen-portal) → 0 errors
- `npm run lint && npm run build` (police-dashboard) → 0 errors

---

## 2026-07-13 — Sprint 05: Police Dashboard MVP


### Added

- Police Dashboard MVP foundation using React, Vite, and TailwindCSS
- Case Management page with mock case data
- Case Details workspace including Investigation Review and Fusion Summary
- Agent Result Cards, Evidence Panel, and Investigation Timeline
- Live backend integration using the existing `POST /investigate` endpoint
- Graceful Loading and Error state components
- Placeholders for Alerts and Profile features

### Improved

- Responsive design enabling flawless mobile, tablet, and desktop views
- Card sizing, flex wrapping, and grid layouts
- Accessibility through focus-visible rings and interactive states
- Search, filter, and default sorting logic (newest first)

### Verified

- Zero backend architecture violations; no unauthorized CRUD APIs created
- `npm run lint` reported 0 errors via oxlint
- `npm run build` completed cleanly without TypeScript errors

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