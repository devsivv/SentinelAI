# PROJECT_STRUCTURE.md

This document serves as the authoritative repository map for the SentinelAI project. It provides a complete audit of the repository, including a hierarchical tree of all folders and files, their purposes, owners, and sprints, as well as an audit report verifying alignment with the `MASTER_PLAN.md`, `SYSTEM_RULES.md`, and other core documentation.

## 1. Repository Hierarchical Tree

```text
SentinelAI/
│
│   ├── .env.example
│   ├── .gitignore
│   ├── AI_GUIDELINES.md
│   ├── CHANGELOG.md
│   ├── docker-compose.yml
│   ├── generate_structure.py
│   ├── MASTER_PLAN.md
│   ├── PROJECT_CONTEXT.md
│   ├── README.md
│   ├── SYSTEM_RULES.md
│   ├── TODO.md
│   ├── agents/
│   │   ├── currency_agent/
│   │   │   ├── .gitkeep
│   │   ├── fraud_agent/
│   │   │   ├── .gitkeep
│   │   ├── geo_agent/
│   │   │   ├── .gitkeep
│   │   ├── graph_agent/
│   │   │   ├── .gitkeep
│   │   ├── scam_comm_agent/
│   │   │   ├── .gitkeep
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
│   │   │   ├── .gitkeep
│   │   ├── orchestrator/
│   │   │   ├── .gitkeep
│   ├── configs/
│   │   ├── .gitkeep
│   │   ├── agents.yaml
│   │   ├── datasets.yaml
│   │   ├── development.yaml
│   │   ├── models.yaml
│   │   ├── production.yaml
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
│   │   │   ├── .gitkeep
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
│   │   ├── .gitkeep
│   │   ├── conftest.py
│   │   ├── test_api.py
│   │   ├── test_currency.py
│   │   ├── test_fraud.py
│   │   ├── test_sms.py
```

## 2. Directory Details

| Folder | Purpose | Owner | Sprint | Scope | Status |
|---|---|---|---|---|---|
| `agents/` | Contains all individual AI agents | AI | 0-8 | MVP | - |
| `agents/currency_agent/` | Detect counterfeit Indian currency | AI | 2 | Stretch | - |
| `agents/fraud_agent/` | Detect fraudulent financial transactions | AI | 3 | MVP | - |
| `agents/geo_agent/` | Geospatial intelligence, crime heatmaps | AI | 8 | Stretch | - |
| `agents/graph_agent/` | Identify fraud rings, mule accounts | AI | 7 | Stretch | - |
| `agents/scam_comm_agent/` | Detect scam SMS + phishing URLs | AI | 4 | MVP | - |
| `agents/voice_agent/` | Analyze voice recordings for spoofing | AI | 5 | Stretch | - |
| `assets/` | Static assets (icons, diagrams, demos) | Frontend/DevOps | 0 | MVP | - |
| `assets/architecture/` | Architecture diagrams | Frontend/DevOps | 0 | MVP | - |
| `assets/demo/` | Demo materials and recordings | Frontend/DevOps | 0 | MVP | - |
| `assets/icons/` | UI Icons | Frontend/DevOps | 0 | MVP | - |
| `assets/logos/` | Brand logos | Frontend/DevOps | 0 | MVP | - |
| `assets/posters/` | Promotional posters | Frontend/DevOps | 0 | MVP | - |
| `assets/screenshots/` | App screenshots | Frontend/DevOps | 0 | MVP | - |
| `assets/videos/` | Demo videos | Frontend/DevOps | 0 | MVP | - |
| `backend/` | Core backend logic | Backend | 1-9 | MVP | - |
| `backend/db/` | Database schemas and migrations | Backend | 0 | MVP | - |
| `backend/fusion_agent/` | Central reasoning engine | Backend | 6 | MVP | - |
| `backend/orchestrator/` | Coordinates all active agents | Backend | 1, 9 | MVP | - |
| `configs/` | Configuration files (models, datasets) | DevOps/Backend | 0 | MVP | - |
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
| `frontend/citizen-portal/` | Citizen facing app | Frontend | 10 | Stretch | - |
| `frontend/police-dashboard/` | Dashboard for police personnel | Frontend | 10 | MVP | - |
| `logs/` | Application and system logs | DevOps | 1-9 | MVP | - |
| `logs/agents/` | Agent specific logs | DevOps | 1-9 | MVP | - |
| `logs/api/` | API access logs | DevOps | 1-9 | MVP | - |
| `logs/orchestrator/` | Orchestrator coordination logs | DevOps | 1-9 | MVP | - |
| `logs/training/` | Model training logs | DevOps | 2-5 | MVP/Stretch | - |
| `models/` | Trained model artifacts | AI | 2-5 | MVP/Stretch | - |
| `models/currency/` | Currency models | AI | 2 | Stretch | Implemented |
| `models/phishing/` | Phishing models | AI | 4 | MVP | Implemented |
| `models/sms/` | SMS Scam models | AI | 4 | MVP | Implemented |
| `models/transactions/` | Transactions (Fraud) models | AI | 3 | MVP | Implemented |
| `prompts/` | Prompt templates for AI assistant | AI/DevOps | 0 | MVP | - |
| `reports/` | Generated analytical reports | Backend | 10 | MVP/Stretch | - |
| `reports/currency/` | Currency reports | Backend | 10 | Stretch | - |
| `reports/fraud/` | Fraud reports | Backend | 10 | MVP | - |
| `reports/fusion/` | Fusion summary reports | Backend | 10 | MVP | - |
| `reports/scam/` | Scam communication reports | Backend | 10 | MVP | - |
| `reports/voice/` | Voice threat reports | Backend | 10 | Stretch | - |
| `requirements/` | Python dependency listings | Backend/AI | 0 | MVP | - |
| `scripts/` | Utility scripts (downloads, data prep) | Backend/AI | 1 | MVP | - |
| `tests/` | Smoke and integration tests | Backend/AI | 1-9 | MVP | - |

## 3. File Details

| File | Purpose | Sprint | Dependencies | Type |
|---|---|---|---|---|
| `.env.example` | Environment variables template | 0 | None | Configuration |
| `.gitignore` | Git ignore rules | 0 | None | Configuration |
| `AI_GUIDELINES.md` | Rules for AI coding assistants | 0 | None | Documentation |
| `CHANGELOG.md` | Project changelog | 0 | None | Documentation |
| `docker-compose.yml` | Local service orchestration | 0 | Docker | Configuration |
| `MASTER_PLAN.md` | Overall roadmap and scope | 0 | None | Planning only |
| `PROJECT_CONTEXT.md` | Live snapshot of project state | 0 | None | Planning only |
| `README.md` | Main repo documentation | 0 | None | Documentation |
| `SYSTEM_RULES.md` | Engineering rules | 0 | None | Documentation |
| `TODO.md` | Current sprint tasks | 0 | None | Planning only |
| `agents/*/.gitkeep` | Preserve directories | 0 | None | Stub |
| `assets/README.md` | Assets docs | 0 | None | Documentation |
| `assets/*/.gitkeep` | Preserve directories | 0 | None | Stub |
| `backend/db/schema.sql` | DB Schema | 0 | PostgreSQL | Implementation |
| `backend/*/.gitkeep` | Preserve directories | 0 | None | Stub |
| `configs/agents.yaml` | Agent configurations | 0 | None | Configuration |
| `configs/datasets.yaml` | Dataset configurations | 0 | None | Configuration |
| `configs/development.yaml` | Dev config | 0 | None | Configuration |
| `configs/models.yaml` | Model configurations | 0 | None | Configuration |
| `configs/production.yaml` | Prod config | 0 | None | Configuration |
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
| `tests/test_sms.py` | Scam agent tests | 4 | pytest | Test |

## 4. Audit Report

### A. Missing Folders
- **`tests/` Missing specific folders/files**: Missing upcoming tests for MVP orchestration (`tests/test_orchestrator.py`, `tests/test_fusion.py`). Note: Stretch agents (Geo, Graph) intentionally do not require tests at this stage.

### B. Missing Files
- **Missing `README.md` files**: Agent-specific READMEs will be created during Sprint 02 when each agent is implemented. This is expected and not an implementation mistake.

### C. Architecture & Compliance Violations
- **Agent specific inference endpoints**: Current agent directories only contain `.gitkeep`. They need a `model.py` and standard `POST /analyze` API route to comply with `SYSTEM_RULES.md`.
- **Misplaced Files / Naming inconsistencies**: None detected. Data folders are correctly organized. `docker-compose.yml` is at the root which is perfectly valid as per `MASTER_PLAN.md` (Phase 11 demo notes).

### D. Duplicate Folders
- None found.

### E. Future-scope / Deferred items
- **Voice Agent**: Voice Agent is intentionally deferred as a Stretch feature according to MASTER_PLAN.md. Repository folders for Voice will be created only when Sprint 05 begins.
- `configs/production.yaml` is present, which is marked as aspirational/future-scope in `SYSTEM_RULES.md`. This is acceptable as long as it remains a stub, but its usage should be restricted until Phase 11.

### F. Hardcoded paths
- Audit incomplete on internal script logic (`scripts/*.py`), but directory structure relies heavily on relative references (e.g. `configs/`). `SYSTEM_RULES.md` warns against inline paths.

## 5. Suggested Improvements
1. Implement Currency Agent.
2. Implement Scam Communication Agent.
3. Implement Fraud Agent.
4. Build shared model loading utilities.
5. Implement inference services.
6. Create FastAPI endpoints.
7. Add smoke tests.
8. Add README.md for each implemented agent.
