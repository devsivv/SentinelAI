"""
errors.py — Global exception handlers for the FastAPI application.

Maps domain-specific exceptions to standard HTTP error responses.
Registered centrally via ``register_exception_handlers`` so individual
routers stay free of error-handling boilerplate.

Error → HTTP mapping:
    ValueError          → 400 Bad Request
    FileNotFoundError   → 404 Not Found
    RuntimeError        → 500 Internal Server Error
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Handle ValueError as HTTP 400 Bad Request."""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


async def file_not_found_error_handler(
    request: Request, exc: FileNotFoundError
) -> JSONResponse:
    """Handle FileNotFoundError as HTTP 404 Not Found."""
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


async def runtime_error_handler(request: Request, exc: RuntimeError) -> JSONResponse:
    """Handle RuntimeError as HTTP 500 Internal Server Error."""
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all custom exception handlers on the FastAPI application instance."""
    app.add_exception_handler(ValueError, value_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(FileNotFoundError, file_not_found_error_handler)  # type: ignore[arg-type]
    app.add_exception_handler(RuntimeError, runtime_error_handler)  # type: ignore[arg-type]
