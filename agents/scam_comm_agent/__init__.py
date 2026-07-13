"""
__init__.py — Public surface of the Scam Communication Agent package.

Exposes the primary prediction functions and result schemas so callers
(FastAPI routes, CLI scripts, tests) need only import from the package root.
"""

from .schemas import (ScamCommAnalysisRequest, ScamCommAnalysisResponse,
                      SMSEvidence, SMSPredictionResult, URLEvidence,
                      URLPredictionResult)
from .sms_predict import build_sms_verdict, predict_sms, preprocess_sms
from .url_predict import (build_url_verdict, extract_url_features, predict_url,
                          preprocess_url)

__all__ = [
    # Schemas
    "ScamCommAnalysisRequest",
    "ScamCommAnalysisResponse",
    "SMSEvidence",
    "SMSPredictionResult",
    "URLEvidence",
    "URLPredictionResult",
    # SMS pipeline
    "preprocess_sms",
    "predict_sms",
    "build_sms_verdict",
    # URL pipeline
    "extract_url_features",
    "preprocess_url",
    "predict_url",
    "build_url_verdict",
]
