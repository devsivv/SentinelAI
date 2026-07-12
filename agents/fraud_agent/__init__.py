"""
__init__.py — Public surface of the Fraud Agent package.

Exposes the primary prediction functions and result schemas so callers
(FastAPI routes, CLI scripts, tests) need only import from the package root.
"""

from .model import get_fraud_model, reset_model_cache, run_fraud_inference
from .predict import build_fraud_verdict, predict_fraud, prepare_features
from .schemas import (
    FraudAnalysisRequest,
    FraudAnalysisResponse,
    FraudEvidence,
    FraudPredictionResult,
    TransactionPayload,
    VALID_TRANSACTION_TYPES,
)

__all__ = [
    # Schemas
    "FraudAnalysisRequest",
    "FraudAnalysisResponse",
    "FraudEvidence",
    "FraudPredictionResult",
    "TransactionPayload",
    "VALID_TRANSACTION_TYPES",
    # Model
    "get_fraud_model",
    "reset_model_cache",
    "run_fraud_inference",
    # Prediction pipeline
    "prepare_features",
    "predict_fraud",
    "build_fraud_verdict",
]
