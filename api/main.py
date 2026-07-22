"""
main.py — FastAPI Application entry point for SentinelAI.

Startup:
    uvicorn api.main:app --reload --port 8000

All configuration (CORS origins, API version, host/port) is read from
``core.config.AppConfig`` so nothing is hardcoded here.  Override any value
via environment variable or ``.env`` (see ``.env.example``).
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.errors import register_exception_handlers
from api.routers import cases, currency, fraud, geo, graph, health, investigate, scam
from core.config import API_VERSION, app_config
from core.logging import log_memory


@asynccontextmanager
async def lifespan(app: FastAPI):
    log_memory("FastAPI startup complete")
    yield


app = FastAPI(
    title="SentinelAI API",
    description="Unified API gateway for SentinelAI Agents.",
    version=API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom exception handlers (ValueError → 400, FileNotFoundError → 404, RuntimeError → 500)
register_exception_handlers(app)

# Include routers
app.include_router(health.router)
app.include_router(currency.router)
app.include_router(scam.router)
app.include_router(fraud.router)
app.include_router(graph.router)
app.include_router(geo.router)
app.include_router(investigate.router)
app.include_router(cases.router)

