"""
main.py — FastAPI Application entry point for SentinelAI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.errors import register_exception_handlers
from api.routers import currency, fraud, health, scam, investigate

app = FastAPI(
    title="SentinelAI API",
    description="Unified API gateway for SentinelAI Agents.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom exception handlers (ValueError -> 400, etc.)
register_exception_handlers(app)

# Include routers
app.include_router(health.router)
app.include_router(currency.router)
app.include_router(scam.router)
app.include_router(fraud.router)
app.include_router(investigate.router)
