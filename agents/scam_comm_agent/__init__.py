"""
__init__.py — Public surface of the Scam Communication Agent package.

Exposes the primary prediction functions and result schemas so callers
(FastAPI routes, CLI scripts, tests) need only import from the package root.
"""

from .schemas import (
    ScamCommAnalysisRequest,
    ScamCommAnalysisResponse,
    SMSEvidence,
    SMSPredictionResult,
    URLEvidence,
    URLPredictionResult,
)
from .sms_model import get_sms_model, reset_sms_model_cache, run_sms_inference
from .sms_predict import build_sms_verdict, predict_sms, preprocess_sms
from .url_model import get_url_model, reset_url_model_cache, run_url_inference
from .url_predict import build_url_verdict, predict_url, preprocess_url, extract_url_features
from .service import analyze_sms, analyze_url

__all__ = [
    # Schemas
    "ScamCommAnalysisRequest",
    "ScamCommAnalysisResponse",
    "SMSEvidence",
    "SMSPredictionResult",
    "URLEvidence",
    "URLPredictionResult",
    # SMS pipeline
    "get_url_model",
    "reset_url_model_cache",
    "run_url_inference",
    # Prediction Pipelines
    "preprocess_sms",
    "predict_sms",
    "build_sms_verdict",
    "preprocess_url",
    "predict_url",
    "build_url_verdict",
    "extract_url_features",
    # Public service
    "analyze_sms",
    "analyze_url",
]
