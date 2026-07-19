# PROJECT_STRUCTURE.md

This document serves as the authoritative repository map for the SentinelAI project. It provides a complete audit of the repository, including a hierarchical tree of all folders and files, their purposes, owners, and sprints, as well as an audit report verifying alignment with the `MASTER_PLAN.md`, `SYSTEM_RULES.md`, and other core documentation.

## 1. Repository Hierarchical Tree

```text
SentinelAI/
│   ├── .env.example
│   ├── .gitignore
│   ├── AI_GUIDELINES.md
│   ├── CHANGELOG.md
│   ├── docker-compose.yml
│   ├── MASTER_PLAN.md
│   ├── PROJECT_CONTEXT.md
│   ├── README.md
│   ├── SYSTEM_RULES.md
│   ├── TODO.md
│   ├── agents/
│   │   ├── currency_agent/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   ├── model.py
│   │   │   ├── predict.py
│   │   │   ├── preprocess.py
│   │   │   ├── schemas.py
│   │   │   ├── README.md
│   │   │   ├── .gitkeep
│   │   ├── fraud_agent/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   ├── model.py
│   │   │   ├── predict.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   ├── README.md
│   │   │   ├── .gitkeep
│   │   ├── geo_agent/
│   │   │   ├── .gitkeep
│   │   ├── graph_agent/
│   │   │   ├── .gitkeep
│   │   ├── scam_comm_agent/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   │   │   ├── sms_model.py
│   │   │   ├── sms_predict.py
│   │   │   ├── url_model.py
│   │   │   ├── url_predict.py
│   │   │   ├── README.md
│   │   ├── voice_agent/
│   │   │   ├── .gitkeep
│   ├── api/
│   │   ├── __init__.py
│   │   ├── errors.py
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── currency.py
│   │   │   ├── fraud.py
│   │   │   ├── health.py
│   │   │   ├── investigate.py
│   │   │   ├── scam.py
│   ├── assets/
│   │   ├── README.md
│   │   ├── architecture/
│   │   │   ├── .gitkeep
│   │   ├── demo/
│   │   │   ├── .gitkeep
│   │   ├── icons/
│   │   │   ├── .gitkeep
│   │   ├── logos/
│   │   │   ├── .gitkeep
│   │   ├── posters/
│   │   │   ├── .gitkeep
│   │   ├── screenshots/
│   │   │   ├── .gitkeep
│   │   ├── videos/
│   │   │   ├── .gitkeep
│   ├── backend/
│   │   ├── db/
│   │   │   ├── .gitkeep
│   │   │   ├── schema.sql
│   │   ├── fusion_agent/
│   │   │   ├── __init__.py
│   │   │   ├── logic.py
│   │   │   ├── schemas.py
│   │   ├── orchestrator/
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py
│   │   │   ├── service.py
│   ├── configs/
│   │   ├── .gitkeep
│   │   ├── agents.yaml
│   │   ├── datasets.yaml
│   │   ├── development.yaml
│   │   ├── models.yaml
│   │   ├── production.yaml
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── loader.py
│   │   ├── logging.py
│   ├── datasets/
│   │   ├── currency/
│   │   ├── phishing/
│   │   ├── sms/
│   │   ├── transactions/
│   ├── docker/
│   │   ├── .gitkeep
│   │   ├── README.md
│   ├── docs/
│   │   ├── api.md
│   │   ├── architecture.md
│   │   ├── database.md
│   │   ├── deployment.md
│   │   ├── presentation.md
│   ├── experiments/
│   │   ├── README.md
│   │   ├── currency/
│   │   │   ├── .gitkeep
│   │   ├── fraud/
│   │   │   ├── .gitkeep
│   │   ├── scam/
│   │   │   ├── .gitkeep
│   ├── frontend/
│   │   ├── citizen-portal/
│   │   │   ├── .gitkeep
│   │   ├── police-dashboard/
│   │   │   ├── components/
│   │   │   ├── data/
│   │   │   ├── pages/
│   │   │   ├── services/
│   │   │   ├── types/
│   ├── logs/
│   │   ├── README.md
│   │   ├── agents/
│   │   │   ├── .gitkeep
│   │   ├── api/
│   │   │   ├── .gitkeep
│   │   ├── orchestrator/
│   │   │   ├── .gitkeep
│   │   ├── training/
│   │   │   ├── .gitkeep
│   ├── models/
│   │   ├── README.md
│   │   ├── currency/
│   │   │   ├── class_names.json
│   │   │   ├── efficientnet_b0_best.pth
│   │   │   ├── mobilenetv2_best.pth
│   │   │   ├── resnet18_best.pth
│   │   │   ├── mobilenetv2_metrics.json
│   │   ├── phishing/
│   │   │   ├── phishing_model.joblib
│   │   ├── sms/
│   │   │   ├── metrics.json
│   │   │   ├── sms_model.pkl
│   │   │   ├── tfidf_vectorizer.pkl
│   │   ├── transactions/
│   │   │   ├── paysim_model.joblib
│   │   │   ├── xgb_model.pkl
│   ├── prompts/
│   │   ├── Sprint-00.md
│   │   ├── Sprint-01.md
│   │   ├── Sprint-02.md
│   │   ├── Sprint-03.md
│   │   ├── Sprint-04.md
│   │   ├── Sprint-05.md
│   │   ├── Sprint-06.md
│   │   ├── Sprint-07.md
│   │   ├── Sprint-08.md
│   │   ├── Sprint-09.md
│   │   ├── Sprint-10.md
│   │   ├── Sprint-11.md
│   │   ├── Sprint-12.md
│   │   ├── _TEMPLATE.md
│   ├── reports/
│   │   ├── README.md
│   │   ├── currency/
│   │   │   ├── .gitkeep
│   │   ├── fraud/
│   │   │   ├── .gitkeep
│   │   ├── fusion/
│   │   │   ├── .gitkeep
│   │   ├── scam/
│   │   │   ├── .gitkeep
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── dev.txt
│   │   ├── ml.txt
│   │   ├── README.md
│   ├── scripts/
│   │   ├── .gitkeep
│   │   ├── download_models.py
│   │   ├── prepare_data.py
│   │   ├── reset_database.py
│   │   ├── run_all_agents.py
│   │   ├── start_project.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_api.py
│   │   ├── test_currency.py
│   │   ├── test_fraud.py
│   │   ├── test_fusion.py
│   │   ├── test_integration.py
│   │   ├── test_integration_sprint3.py
│   │   ├── test_orchestrator.py
│   │   ├── test_scam_comm.py
```

## 2. Directory Details

| Folder | Purpose | Owner | Sprint | Scope | Status |
|---|---|---|---|---|---|
| `agents/` | Contains all individual AI agents | AI | 0-8 | MVP | - |
| `agents/currency_agent/` | Detect counterfeit Indian currency | AI | 2 | Stretch | Implemented |
| `agents/fraud_agent/` | Detect fraudulent financial transactions | AI | 3 | MVP | Implemented |
| `agents/geo_agent/` | Geospatial intelligence, crime heatmaps | AI | 8 | Stretch | Deferred |
| `agents/graph_agent/` | Identify fraud rings, mule accounts | AI | 7 | Stretch | Deferred |
| `agents/scam_comm_agent/` | Detect scam SMS + phishing URLs | AI | 4 | MVP | Implemented |
| `agents/voice_agent/` | Analyze voice recordings for spoofing | AI | 5 | Stretch | Deferred |
| `api/` | FastAPI API layer (main application, exceptions, router endpoints) | Backend | 2 | MVP | Implemented |
| `assets/` | Static assets (icons, diagrams, demos) | Frontend/DevOps | 0 | MVP | - |
| `assets/architecture/` | Architecture diagrams | Frontend/DevOps | 0 | MVP | - |
| `assets/demo/` | Demo materials and recordings | Frontend/DevOps | 0 | MVP | - |
| `assets/icons/` | UI Icons | Frontend/DevOps | 0 | MVP | - |
| `assets/logos/` | Brand logos | Frontend/DevOps | 0 | MVP | - |
| `assets/posters/` | Promotional posters | Frontend/DevOps | 0 | MVP | - |
| `assets/screenshots/` | App screenshots | Frontend/DevOps | 0 | MVP | - |
| `assets/videos/` | Demo videos | Frontend/DevOps | 0 | MVP | - |
| `backend/` | Core backend logic | Backend | 1-9 | MVP | - |
| `backend/db/` | Database schemas and migrations | Backend | 0 | MVP | Implemented |
| `backend/fusion_agent/` | Central reasoning engine | Backend | 6 | MVP | Implemented |
| `backend/orchestrator/` | Coordinates all active agents | Backend | 1, 9 | MVP | Implemented |
| `configs/` | Configuration files (models, datasets) | DevOps/Backend | 0 | MVP | Implemented |
| `core/` | Shared infrastructure (configuration, logging, loaders, exceptions) | DevOps/Backend | 2 | MVP | Implemented |
| `datasets/` | Standardized datasets for training | AI | 1 | MVP/Stretch | - |
| `datasets/currency/` | Indian currency dataset | AI | 2 | Stretch | Implemented |
| `datasets/phishing/` | Phishing Website Dataset | AI | 4 | MVP | Implemented |
| `datasets/sms/` | SMS Spam Collection | AI | 4 | MVP | Implemented |
| `datasets/transactions/` | Financial transactions dataset | AI | 3 | MVP | Implemented |
| `docker/` | Dockerfiles and container configurations | DevOps | 11 | Future | - |
| `docs/` | Technical documentation and specs | All | 0 | MVP | - |
| `experiments/` | Placeholders. Tracking begins on future iterations | AI | 2-5 | MVP/Stretch | Placeholder |
| `experiments/currency/` | Placeholder | AI | 2 | Stretch | Placeholder |
| `experiments/fraud/` | Placeholder | AI | 3 | MVP | Placeholder |
| `experiments/scam/` | Placeholder | AI | 4 | MVP | Placeholder |
| `experiments/voice/` | Placeholder | AI | 5 | Stretch | Placeholder |
| `frontend/` | Web and mobile UIs | Frontend | 10 | MVP/Stretch | - |
| `frontend/citizen-portal/` | Citizen facing app | Frontend | 10 | Stretch | Implemented |
| `frontend/police-dashboard/` | Dashboard for police personnel | Frontend | 10 | MVP | Implemented |
| `logs/` | Application and system logs | DevOps | 1-9 | MVP | - |
| `logs/agents/` | Agent specific logs | DevOps | 1-9 | MVP | - |
| `logs/api/` | API access logs | DevOps | 1-9 | MVP | - |
| `agents/currency_agent/config.py` | Configuration constants for currency agent | 2 | YAML, config | Configuration |
| `agents/currency_agent/logging.py` | Logger instantiation for currency agent | 2 | Logging | Utility |
| `agents/currency_agent/model.py` | MobileNetV2 architecture & model loading | 2 | PyTorch | Implementation |
| `agents/currency_agent/predict.py` | Inference pipeline for counterfeit detection | 2 | PyTorch, PIL | Implementation |
| `agents/currency_agent/preprocess.py` | Preprocessing utilities for currency images | 2 | PIL, Albumentations | Implementation |
| `agents/currency_agent/schemas.py` | Request/response Pydantic models for currency agent | 2 | Pydantic | Schema |
| `agents/currency_agent/README.md` | Usage guide for currency agent | 2 | None | Documentation |
| `agents/fraud_agent/config.py` | Configuration constants for fraud agent | 3 | YAML, config | Configuration |
| `agents/fraud_agent/logging.py` | Logger instantiation for fraud agent | 3 | Logging | Utility |
| `agents/fraud_agent/model.py` | Model architecture & loading (XGBoost/RF) | 3 | XGBoost, joblib | Implementation |
| `agents/fraud_agent/predict.py` | Inference pipeline for transaction anomalies | 3 | Pandas, NumPy | Implementation |
| `agents/fraud_agent/schemas.py` | Request/response Pydantic models for fraud agent | 3 | Pydantic | Schema |
| `agents/fraud_agent/service.py` | Business logic service layer for fraud agent | 3 | None | Implementation |
| `agents/fraud_agent/README.md` | Usage guide for fraud agent | 3 | None | Documentation |
| `agents/scam_comm_agent/config.py` | Configuration constants for scam communication agent | 4 | YAML, config | Configuration |
| `agents/scam_comm_agent/logging.py` | Logger instantiation for scam agent | 4 | Logging | Utility |
| `agents/scam_comm_agent/schemas.py` | Request/response Pydantic models for scam agent | 4 | Pydantic | Schema |
| `agents/scam_comm_agent/service.py` | Main service layer coordinating SMS and URL predictions | 4 | None | Implementation |
| `agents/scam_comm_agent/sms_model.py` | TF-IDF and SVM classifier setup for SMS spam | 4 | scikit-learn, joblib | Implementation |
| `agents/scam_comm_agent/sms_predict.py` | SMS scam inference logic | 4 | pandas, sms_model | Implementation |
| `agents/scam_comm_agent/url_model.py` | URL feature extractor and random forest setup | 4 | joblib | Implementation |
| `agents/scam_comm_agent/url_predict.py` | URL phishing inference logic | 4 | pandas, url_model | Implementation |
| `agents/scam_comm_agent/README.md` | Usage guide for scam communication agent | 4 | None | Documentation |
| `api/main.py` | FastAPI application entrypoint and router wiring | 2 | FastAPI, config | Implementation |
| `api/errors.py` | Global exception handler registration | 2 | FastAPI | Implementation |
| `api/routers/__init__.py` | Router module init | 2 | None | Stub |
| `api/routers/currency.py` | Router endpoint for currency analysis | 2 | FastAPI | Implementation |
| `api/routers/fraud.py` | Router endpoint for transaction fraud analysis | 3 | FastAPI | Implementation |
| `api/routers/health.py` | Health check router endpoint | 2 | FastAPI | Implementation |
| `api/routers/investigate.py` | Router endpoint for Orchestrator investigatory cases | 3 | FastAPI | Implementation |
| `api/routers/scam.py` | Router endpoint for SMS and URL verification | 4 | FastAPI | Implementation |
| `assets/README.md` | Assets docs | 0 | None | Documentation |
| `assets/*/.gitkeep` | Preserve directories | 0 | None | Stub |
| `backend/db/schema.sql` | DB Schema | 0 | PostgreSQL | Implementation |
| `backend/*/.gitkeep` | Preserve directories | 0 | None | Stub |
| `configs/agents.yaml` | Agent configurations | 0 | None | Configuration |
| `configs/datasets.yaml` | Dataset configurations | 0 | None | Configuration |
| `configs/development.yaml` | Dev config | 0 | None | Configuration |
| `configs/models.yaml` | Model configurations | 0 | None | Configuration |
| `configs/production.yaml` | Prod config | 0 | None | Configuration |
| `core/__init__.py` | Core library package initializer | 2 | None | Stub |
| `core/config.py` | Config loading, schema definition, and CORS centralization | 2 | Pydantic, YAML | Configuration |
| `core/exceptions.py` | Base exceptions and error mappings | 2 | None | Implementation |
| `core/loader.py` | Centralized model loading helper | 2 | joblib, torch | Implementation |
| `core/logging.py` | Custom logging configuration and file handler setup | 2 | Logging | Implementation |
| `datasets/README.md` | Datasets documentation | 0 | None | Documentation |
| `datasets/*/.gitkeep` | Preserve directories | 0 | None | Stub |
| `docker/README.md` | Docker instructions | 0 | None | Documentation |
| `docs/api.md` | API contracts and sources | 0 | None | Documentation |
| `docs/architecture.md` | Architecture design | 0 | None | Documentation |
| `docs/database.md` | DB design | 0 | None | Documentation |
| `docs/deployment.md` | Deployment guide | 0 | None | Documentation |
| `docs/presentation.md` | Demo presentation slides | 0 | None | Documentation |
| `experiments/README.md` | Experiment tracking docs | 0 | None | Documentation |
| `experiments/*/.gitkeep` | Preserve directories | 0 | None | Stub |
| `frontend/*/.gitkeep` | Preserve directories | 0 | None | Stub |
| `logs/README.md` | Logs docs | 0 | None | Documentation |
| `logs/*/.gitkeep` | Preserve directories | 0 | None | Stub |
| `models/README.md` | Models docs | 0 | None | Documentation |
| `models/*/.gitkeep` | Preserve directories | 0 | None | Stub |
| `prompts/Sprint-*.md` | AI Sprint Prompts | 0 | None | Planning only |
| `prompts/_TEMPLATE.md` | AI Sprint Template | 0 | None | Planning only |
| `reports/README.md` | Reports docs | 0 | None | Documentation |
| `reports/*/.gitkeep` | Preserve directories | 0 | None | Stub |
| `requirements/base.txt` | Core deps | 0 | None | Configuration |
| `requirements/dev.txt` | Dev deps | 0 | None | Configuration |
| `requirements/ml.txt` | ML deps | 0 | None | Configuration |
| `requirements/README.md` | Requirements docs | 0 | None | Documentation |
| `scripts/download_models.py` | Model downloader | 1 | Python | Implementation |
| `scripts/prepare_data.py` | Dataset preparer | 1 | Python | Implementation |
| `scripts/reset_database.py` | DB reset script | 1 | Python, DB | Implementation |
| `scripts/run_all_agents.py` | Run agent servers | 1 | Python | Implementation |
| `scripts/start_project.py` | Start project script | 1 | Python | Implementation |
| `tests/conftest.py` | Test fixtures | 1 | pytest | Test |
| `tests/test_api.py` | API smoke tests | 1 | pytest | Test |
| `tests/test_currency.py` | Currency agent tests | 2 | pytest | Test |
| `tests/test_fraud.py` | Fraud agent tests | 3 | pytest | Test |
| `tests/test_fusion.py` | Fusion agent tests | 3 | pytest | Test |
| `tests/test_integration.py` | Orchestrator and agent integration tests | 2 | pytest | Test |
| `tests/test_integration_sprint3.py` | Sprint 03 Orchestrator tests | 3 | pytest | Test |
| `tests/test_orchestrator.py` | Orchestrator logic tests | 3 | pytest | Test |
| `tests/test_scam_comm.py` | Scam agent tests | 2 | pytest | Test |

## 4. Audit Report

### A. Missing Folders
- **None**. All MVP components and Orchestrator/Fusion tests are present.

### B. Missing Files
- **None**. Agent-specific READMEs and core components have all been implemented.

### C. Architecture & Compliance Violations
- **None detected.** Data folders are correctly organized. `docker-compose.yml` is at the root which is perfectly valid as per `MASTER_PLAN.md` (Phase 11 demo notes).

### D. Duplicate Folders
- None found.

### E. Future-scope / Deferred items
- **Voice Agent**: Voice Agent is intentionally deferred as a Stretch feature according to MASTER_PLAN.md.
- `configs/production.yaml` is present, which is marked as aspirational/future-scope in `SYSTEM_RULES.md`. This is acceptable as long as it remains a stub, but its usage should be restricted until Phase 11.

### F. Hardcoded paths
- Audit incomplete on internal script logic (`scripts/*.py`), but directory structure relies heavily on relative references (e.g. `configs/`). `SYSTEM_RULES.md` warns against inline paths.

## 5. Suggested Improvements
1. Implement full backend CRUD APIs for cases and persistent case database.
2. Build advanced visualization features for the police dashboard.
