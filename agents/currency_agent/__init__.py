"""
agents/currency_agent — MobileNetV2-based counterfeit currency detector.

Public surface
--------------
    from agents.currency_agent import predict, build_verdict, settings

Modules
-------
config      Runtime settings (paths, thresholds, log level).
logging     Shared rotating-file + stdout logger.
preprocess  Image loading, resizing, normalisation, tensor conversion.
model       Singleton model loader and raw inference (logits only).
predict     High-level pipeline: preprocess → infer → softmax → labels.
schemas     Pydantic request / response models (Agent Contract).
"""

from .config import settings
from .predict import build_verdict, predict
from .schemas import (CurrencyAnalysisRequest, CurrencyAnalysisResponse,
                      CurrencyEvidence, CurrencyPayload, PredictionResult)

__all__ = [
    "settings",
    "predict",
    "build_verdict",
    "PredictionResult",
    "CurrencyPayload",
    "CurrencyAnalysisRequest",
    "CurrencyAnalysisResponse",
    "CurrencyEvidence",
]
