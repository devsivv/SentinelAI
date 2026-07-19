# Deployment

## Local Development Setup

### Prerequisites

- Python 3.12+
- Node.js 20+ and npm
- Model artifacts present under `models/` (see `scripts/download_models.py` or release assets)

### 1. Clone and configure

```bash
git clone <repo-url> && cd SentinelAI
cp .env.example .env
# Edit .env if you need to override ports, model paths, or CORS origins
```

### 2. Install Python dependencies

```bash
pip install -r requirements/base.txt -r requirements/ml.txt -r requirements/dev.txt
```

### 3. Start the backend API

All agents are unified under a single FastAPI application. Run it from the
**repository root** (so Python can resolve package imports correctly):

```bash
uvicorn api.main:app --reload --port 8000
```

The API is now available at `http://127.0.0.1:8000`.
Interactive docs: `http://127.0.0.1:8000/docs`

### 4. Start the Citizen Portal frontend

```bash
cd frontend/citizen-portal
npm install
npm run dev
# Runs on http://localhost:5173
```

### 5. Start the Police Dashboard frontend

```bash
cd frontend/police-dashboard
npm install
npm run dev
# Runs on http://localhost:5174 (or the next available port)
```

### 6. Run all tests

```bash
python -m pytest tests/ -v
```

### CORS

The API allows `http://localhost:5173` and `http://127.0.0.1:5173` by default.
If your frontend runs on a different port, set `CORS_ORIGINS` in your `.env`:

```env
CORS_ORIGINS=http://localhost:5173,http://localhost:5174
```

---

## Production — `[Future scope, not built]`

The following belong on a roadmap slide (`presentation.md`), not in this build:

- Dockerfiles per agent + full `docker-compose.yml` (all services containerised)
- Nginx reverse proxy / TLS termination
- Redis + Celery for async job queues at scale
- GitHub Actions CI/CD
- Cloud deployment (managed Postgres/Neo4j, container orchestration)
- Multi-tenant auth, live police dispatch integration, automated FIR filing, automated account-freeze

Treat Phase 11 as the most common way hackathon teams run out of time — a local
Compose file covering the DB is enough. Spend the time this would take on
hardening the MVP instead (see `MASTER_PLAN.md` §Timeline, Day 5).
