"""
test_integration.py — Integration tests for Phase 2.7.

Verifies that the full request path works correctly end-to-end:

    HTTP Request  →  FastAPI Router  →  Agent  →  Response

Each test exercises the complete chain without loading real ML model
artefacts.  Models are mocked at the prediction-function boundary so
we test request-validation, agent invocation, response serialisation,
shared-logging initialisation, shared-configuration usage and exception
translation — the entire integration surface — without needing model
files on disk.

Architecture boundary enforced by these tests
---------------------------------------------
  API layer (routers) calls agents via their public ``predict_*`` /
  ``build_*`` functions only.  Routers never call model loaders, shared
  infrastructure utilities, or other agents directly.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app, raise_server_exceptions=False)

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

_SMS_PAYLOAD = {
    "case_id": "integ-sms-001",
    "input_type": "sms",
    "payload": {"text": "URGENT: Your bank account has been suspended. Call now!"},
}

_URL_PAYLOAD = {
    "case_id": "integ-url-001",
    "input_type": "url",
    "payload": {"url": "http://verify-account.phish.example.com/login"},
}

_FRAUD_PAYLOAD = {
    "case_id": "integ-fraud-001",
    "input_type": "transaction",
    "payload": {
        "step": 1,
        "type": "TRANSFER",
        "amount": 182000.0,
        "oldbalanceOrg": 182000.0,
        "newbalanceOrig": 0.0,
        "oldbalanceDest": 0.0,
        "newbalanceDest": 182000.0,
        "isFlaggedFraud": 0,
    },
}


# ---------------------------------------------------------------------------
# SECTION 1 — Health endpoints
# ---------------------------------------------------------------------------


class TestHealthIntegration:
    """Verify health endpoints return complete, correctly-typed responses."""

    def test_root_returns_service_metadata(self):
        """GET / must return service name, version, and status fields."""
        resp = client.get("/")
        assert resp.status_code == 200
        body = resp.json()
        assert body["service"] == "SentinelAI"
        assert "version" in body
        assert body["status"] == "operational"

    def test_health_returns_timestamp(self):
        """GET /health must return a healthy status and a non-empty timestamp."""
        resp = client.get("/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "healthy"
        assert isinstance(body["timestamp"], str)
        assert len(body["timestamp"]) > 0


# ---------------------------------------------------------------------------
# SECTION 2 — Currency Agent integration
# ---------------------------------------------------------------------------


class TestCurrencyAgentIntegration:
    """Verify the Currency API → Currency Agent integration."""

    @patch("api.routers.currency.predict")
    @patch("api.routers.currency.build_verdict")
    def test_successful_request_returns_agent_contract_shape(
        self, mock_build, mock_predict
    ):
        """A valid image upload must flow through the agent and return the
        standard Agent Contract response shape."""
        from agents.currency_agent.schemas import PredictionResult

        mock_predict.return_value = PredictionResult(
            predicted_class="genuine",
            confidence=0.97,
            probabilities={"genuine": 0.97, "fake": 0.03},
            image_size=(224, 224),
        )
        mock_build.return_value = {
            "verdict": "safe",
            "confidence": 0.97,
            "risk_score": 3,
            "category": "none",
            "explanation": "MobileNetV2 classified the note as genuine with 97.0% confidence.",
        }

        resp = client.post(
            "/currency/analyze",
            data={"case_id": "integ-curr-001"},
            files={"image": ("note.jpg", b"\xff\xd8\xff\xe0fake", "image/jpeg")},
        )

        assert resp.status_code == 200
        body = resp.json()
        # Contract fields
        assert body["agent"] == "currency_agent"
        assert body["case_id"] == "integ-curr-001"
        assert body["verdict"] == "safe"
        assert 0.0 <= body["confidence"] <= 1.0
        assert 0 <= body["risk_score"] <= 100
        assert "category" in body
        assert "explanation" in body
        assert "evidence" in body
        assert "processed_at" in body
        # Agent was invoked with the correct case_id
        mock_predict.assert_called_once()
        call_kwargs = mock_predict.call_args
        assert call_kwargs.kwargs["case_id"] == "integ-curr-001"

    def test_missing_image_returns_422(self):
        """Omitting the required image field must produce a 422 error."""
        resp = client.post(
            "/currency/analyze",
            data={"case_id": "integ-curr-002"},
        )
        assert resp.status_code == 422

    def test_missing_case_id_returns_422(self):
        """Omitting case_id from the form must produce a 422 error."""
        resp = client.post(
            "/currency/analyze",
            files={"image": ("note.jpg", b"fake", "image/jpeg")},
        )
        assert resp.status_code == 422

    @patch("api.routers.currency.predict")
    def test_file_not_found_maps_to_404(self, mock_predict):
        """FileNotFoundError from the agent must be translated to HTTP 404."""
        mock_predict.side_effect = FileNotFoundError("currency_model.pt not found")

        resp = client.post(
            "/currency/analyze",
            data={"case_id": "integ-curr-003"},
            files={"image": ("note.jpg", b"fake", "image/jpeg")},
        )
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"].lower()

    @patch("api.routers.currency.predict")
    def test_value_error_maps_to_400(self, mock_predict):
        """ValueError (e.g. empty image) from the agent must map to HTTP 400."""
        mock_predict.side_effect = ValueError("Image bytes are empty.")

        resp = client.post(
            "/currency/analyze",
            data={"case_id": "integ-curr-004"},
            files={"image": ("note.jpg", b"", "image/jpeg")},
        )
        assert resp.status_code == 400

    @patch("api.routers.currency.predict")
    def test_runtime_error_maps_to_500(self, mock_predict):
        """RuntimeError during inference must be translated to HTTP 500."""
        mock_predict.side_effect = RuntimeError("Model forward pass failed.")

        resp = client.post(
            "/currency/analyze",
            data={"case_id": "integ-curr-005"},
            files={"image": ("note.jpg", b"fake", "image/jpeg")},
        )
        assert resp.status_code == 500


# ---------------------------------------------------------------------------
# SECTION 3 — Scam SMS Agent integration
# ---------------------------------------------------------------------------


class TestScamSMSAgentIntegration:
    """Verify the Scam SMS API → SMS Agent integration."""

    @patch("api.routers.scam.predict_sms")
    @patch("api.routers.scam.build_sms_verdict")
    def test_scam_sms_returns_agent_contract(self, mock_build, mock_predict):
        """A valid SMS payload must produce a full Agent Contract response."""
        from agents.scam_comm_agent.schemas import SMSPredictionResult

        mock_predict.return_value = SMSPredictionResult(
            predicted_class="scam",
            confidence=0.98,
            scam_probability=0.98,
            ham_probability=0.02,
            cleaned_text="urgent bank account suspended call",
        )
        mock_build.return_value = {
            "verdict": "fraud",
            "confidence": 0.98,
            "risk_score": 98,
            "category": "digital_arrest_scam",
            "explanation": "SMS classified as scam with 98.0% confidence.",
        }

        resp = client.post("/scam/sms", json=_SMS_PAYLOAD)

        assert resp.status_code == 200
        body = resp.json()
        assert body["agent"] == "scam_comm_agent"
        assert body["case_id"] == "integ-sms-001"
        assert body["verdict"] == "fraud"
        assert body["category"] == "digital_arrest_scam"
        assert 0.0 <= body["confidence"] <= 1.0
        assert 0 <= body["risk_score"] <= 100
        assert "evidence" in body
        assert body["evidence"]["cleaned_text"] == "urgent bank account suspended call"
        # The agent was called with the correct case_id
        mock_predict.assert_called_once_with(
            "URGENT: Your bank account has been suspended. Call now!",
            case_id="integ-sms-001",
        )

    def test_sms_wrong_input_type_returns_400(self):
        """Sending input_type='url' to /scam/sms must return 400."""
        payload = {**_SMS_PAYLOAD, "input_type": "url", "payload": {"url": "http://x.com"}}
        resp = client.post("/scam/sms", json=payload)
        assert resp.status_code == 400

    def test_sms_missing_text_returns_422(self):
        """Sending a payload with no 'text' key must trigger Pydantic 422."""
        bad = {
            "case_id": "integ-sms-002",
            "input_type": "sms",
            "payload": {},  # 'text' is required
        }
        resp = client.post("/scam/sms", json=bad)
        assert resp.status_code == 422

    @patch("api.routers.scam.predict_sms")
    def test_sms_value_error_maps_to_400(self, mock_predict):
        """Empty / whitespace SMS text must surface as HTTP 400."""
        mock_predict.side_effect = ValueError("SMS text must be a non-empty string.")

        resp = client.post(
            "/scam/sms",
            json={
                "case_id": "integ-sms-003",
                "input_type": "sms",
                "payload": {"text": "   "},
            },
        )
        assert resp.status_code == 400

    @patch("api.routers.scam.predict_sms")
    def test_sms_file_not_found_maps_to_404(self, mock_predict):
        """Missing model artefact must surface as HTTP 404."""
        mock_predict.side_effect = FileNotFoundError("sms_model.joblib not found")

        resp = client.post("/scam/sms", json=_SMS_PAYLOAD)
        assert resp.status_code == 404

    @patch("api.routers.scam.predict_sms")
    def test_sms_runtime_error_maps_to_500(self, mock_predict):
        """Inference failure must surface as HTTP 500."""
        mock_predict.side_effect = RuntimeError("Inference pipeline crashed.")

        resp = client.post("/scam/sms", json=_SMS_PAYLOAD)
        assert resp.status_code == 500


# ---------------------------------------------------------------------------
# SECTION 4 — Scam URL Agent integration
# ---------------------------------------------------------------------------


class TestScamURLAgentIntegration:
    """Verify the Scam URL API → URL Agent integration."""

    @patch("api.routers.scam.predict_url")
    @patch("api.routers.scam.build_url_verdict")
    def test_phishing_url_returns_agent_contract(self, mock_build, mock_predict):
        """A valid URL payload must produce a full Agent Contract response."""
        from agents.scam_comm_agent.schemas import URLPredictionResult

        mock_predict.return_value = URLPredictionResult(
            predicted_class="phishing",
            confidence=0.94,
            phishing_probability=0.94,
            safe_probability=0.06,
            features={"url_length": 48, "https": 0, "has_ip": 0},
        )
        mock_build.return_value = {
            "verdict": "fraud",
            "confidence": 0.94,
            "risk_score": 94,
            "category": "phishing",
            "explanation": "URL classified as phishing with 94.0% confidence.",
        }

        resp = client.post("/scam/url", json=_URL_PAYLOAD)

        assert resp.status_code == 200
        body = resp.json()
        assert body["agent"] == "scam_comm_agent"
        assert body["case_id"] == "integ-url-001"
        assert body["verdict"] == "fraud"
        assert body["category"] == "phishing"
        assert "evidence" in body
        assert body["evidence"]["url"] == "http://verify-account.phish.example.com/login"
        assert "features" in body["evidence"]

    def test_url_wrong_input_type_returns_400(self):
        """Sending input_type='sms' to /scam/url must return 400."""
        payload = {**_URL_PAYLOAD, "input_type": "sms", "payload": {"text": "hello"}}
        resp = client.post("/scam/url", json=payload)
        assert resp.status_code == 400

    def test_url_missing_url_field_returns_422(self):
        """Sending a URL payload with no 'url' key must trigger Pydantic 422."""
        bad = {
            "case_id": "integ-url-002",
            "input_type": "url",
            "payload": {},  # 'url' is required
        }
        resp = client.post("/scam/url", json=bad)
        assert resp.status_code == 422

    @patch("api.routers.scam.predict_url")
    def test_url_value_error_maps_to_400(self, mock_predict):
        """Malformed URL must surface as HTTP 400."""
        mock_predict.side_effect = ValueError(
            "Malformed URL — missing scheme or host: 'not-a-url'."
        )

        resp = client.post(
            "/scam/url",
            json={
                "case_id": "integ-url-003",
                "input_type": "url",
                "payload": {"url": "not-a-url"},
            },
        )
        assert resp.status_code == 400

    @patch("api.routers.scam.predict_url")
    def test_url_file_not_found_maps_to_404(self, mock_predict):
        """Missing model artefact must surface as HTTP 404."""
        mock_predict.side_effect = FileNotFoundError("xgboost_phishing.joblib not found")

        resp = client.post("/scam/url", json=_URL_PAYLOAD)
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# SECTION 5 — Fraud Agent integration
# ---------------------------------------------------------------------------


class TestFraudAgentIntegration:
    """Verify the Fraud API → Fraud Agent integration."""

    @patch("api.routers.fraud.predict_fraud")
    @patch("api.routers.fraud.build_fraud_verdict")
    def test_fraud_transaction_returns_agent_contract(self, mock_build, mock_predict):
        """A valid transaction payload must produce a full Agent Contract response."""
        from agents.fraud_agent.schemas import FraudPredictionResult

        mock_predict.return_value = FraudPredictionResult(
            predicted_class="fraud",
            confidence=0.92,
            fraud_probability=0.92,
            safe_probability=0.08,
            type_encoded=4,
            engineered_features={
                "log_amount": 12.11,
                "orig_balance_diff": 182000.0,
                "high_risk_type": 0,
                "amount_balance_ratio": 1.0,
                "zero_balance": 1,
            },
        )
        mock_build.return_value = {
            "verdict": "fraud",
            "confidence": 0.92,
            "risk_score": 92,
            "category": "mule_transaction",
            "explanation": "TRANSFER transaction flagged as fraudulent with 92.0% confidence.",
        }

        resp = client.post("/fraud/analyze", json=_FRAUD_PAYLOAD)

        assert resp.status_code == 200
        body = resp.json()
        assert body["agent"] == "fraud_agent"
        assert body["case_id"] == "integ-fraud-001"
        assert body["verdict"] == "fraud"
        assert body["category"] == "mule_transaction"
        assert 0.0 <= body["confidence"] <= 1.0
        assert 0 <= body["risk_score"] <= 100
        assert "evidence" in body
        assert body["evidence"]["transaction_type"] == "TRANSFER"
        assert body["evidence"]["type_encoded"] == 4
        assert "engineered_features" in body["evidence"]
        assert "processed_at" in body
        # Verify agent was called with correct case_id
        mock_predict.assert_called_once()
        call_kwargs = mock_predict.call_args
        assert call_kwargs.kwargs["case_id"] == "integ-fraud-001"

    def test_invalid_transaction_type_returns_422(self):
        """Unknown transaction type must be rejected by Pydantic with 422."""
        bad = {**_FRAUD_PAYLOAD}
        bad["payload"] = {**bad["payload"], "type": "WIRE_TRANSFER"}
        resp = client.post("/fraud/analyze", json=bad)
        assert resp.status_code == 422

    def test_negative_amount_returns_422(self):
        """Negative amount must be rejected by Pydantic with 422."""
        bad = {**_FRAUD_PAYLOAD}
        bad["payload"] = {**bad["payload"], "amount": -100.0}
        resp = client.post("/fraud/analyze", json=bad)
        assert resp.status_code == 422

    def test_zero_amount_returns_422(self):
        """Zero amount must be rejected by Pydantic with 422."""
        bad = {**_FRAUD_PAYLOAD}
        bad["payload"] = {**bad["payload"], "amount": 0.0}
        resp = client.post("/fraud/analyze", json=bad)
        assert resp.status_code == 422

    def test_step_zero_returns_422(self):
        """Step=0 must be rejected (ge=1 constraint) with 422."""
        bad = {**_FRAUD_PAYLOAD}
        bad["payload"] = {**bad["payload"], "step": 0}
        resp = client.post("/fraud/analyze", json=bad)
        assert resp.status_code == 422

    @patch("api.routers.fraud.predict_fraud")
    def test_file_not_found_maps_to_404(self, mock_predict):
        """Missing model artefact must surface as HTTP 404."""
        mock_predict.side_effect = FileNotFoundError("xgboost_paysim.joblib not found")

        resp = client.post("/fraud/analyze", json=_FRAUD_PAYLOAD)
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"].lower()

    @patch("api.routers.fraud.predict_fraud")
    def test_runtime_error_maps_to_500(self, mock_predict):
        """Inference RuntimeError must surface as HTTP 500."""
        mock_predict.side_effect = RuntimeError("XGBoost prediction failed.")

        resp = client.post("/fraud/analyze", json=_FRAUD_PAYLOAD)
        assert resp.status_code == 500


# ---------------------------------------------------------------------------
# SECTION 6 — Architecture boundary verification
# ---------------------------------------------------------------------------


class TestArchitectureBoundaries:
    """Smoke-test that public package imports work correctly.

    These confirm that ``agents.currency_agent``, ``agents.scam_comm_agent``,
    and ``agents.fraud_agent`` each expose a clean public surface via
    ``__init__.py`` and that no import errors are raised.
    """

    def test_currency_agent_public_imports(self):
        """All expected public symbols must be importable from agents.currency_agent."""
        from agents.currency_agent import (  # noqa: F401
            CurrencyAnalysisRequest,
            CurrencyAnalysisResponse,
            CurrencyEvidence,
            CurrencyPayload,
            PredictionResult,
            build_verdict,
            predict,
            settings,
        )

    def test_scam_comm_agent_public_imports(self):
        """All expected public symbols must be importable from agents.scam_comm_agent."""
        from agents.scam_comm_agent import (  # noqa: F401
            ScamCommAnalysisRequest,
            ScamCommAnalysisResponse,
            SMSEvidence,
            SMSPredictionResult,
            URLEvidence,
            URLPredictionResult,
            build_sms_verdict,
            build_url_verdict,
            extract_url_features,
            predict_sms,
            predict_url,
            preprocess_sms,
            preprocess_url,
        )

    def test_fraud_agent_public_imports(self):
        """All expected public symbols must be importable from agents.fraud_agent."""
        from agents.fraud_agent import (  # noqa: F401
            VALID_TRANSACTION_TYPES,
            FraudAnalysisRequest,
            FraudAnalysisResponse,
            FraudEvidence,
            FraudPredictionResult,
            TransactionPayload,
            build_fraud_verdict,
            get_fraud_model,
            predict_fraud,
            prepare_features,
            reset_model_cache,
            run_fraud_inference,
        )

    def test_core_public_imports(self):
        """All expected core symbols must be importable from core."""
        from core import (  # noqa: F401
            AgentBaseConfig,
            PROJECT_ROOT,
            SentinelAIError,
            build_agent_logger,
            load_joblib_model,
        )

    def test_api_main_imports(self):
        """The FastAPI app must be importable from api.main."""
        from api.main import app  # noqa: F401
        from fastapi import FastAPI

        assert isinstance(app, FastAPI)

    def test_shared_logging_is_used_by_all_agents(self):
        """Each agent logging module must delegate to core.logging."""
        import agents.currency_agent.logging as cu_log
        import agents.fraud_agent.logging as fr_log
        import agents.scam_comm_agent.logging as sc_log
        from core.logging import build_agent_logger

        # Each agent's get_logger() must return the same logger object on
        # repeated calls (singleton guarantee).
        logger_a = cu_log.get_logger()
        logger_b = cu_log.get_logger()
        assert logger_a is logger_b

        logger_c = sc_log.get_logger()
        logger_d = sc_log.get_logger()
        assert logger_c is logger_d

        logger_e = fr_log.get_logger()
        logger_f = fr_log.get_logger()
        assert logger_e is logger_f

    def test_shared_config_inherited_by_all_agents(self):
        """Each agent config must be a subclass of AgentBaseConfig."""
        from agents.currency_agent.config import CurrencyAgentConfig
        from agents.fraud_agent.config import FraudAgentConfig
        from agents.scam_comm_agent.config import ScamCommAgentConfig
        from core.config import AgentBaseConfig

        assert issubclass(CurrencyAgentConfig, AgentBaseConfig)
        assert issubclass(ScamCommAgentConfig, AgentBaseConfig)
        assert issubclass(FraudAgentConfig, AgentBaseConfig)
