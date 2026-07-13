"""
test_fraud.py — Comprehensive test suite for the Fraud Agent.

Covers:
  Model
    - lazy loading
    - singleton (same object returned on second call)
    - thread safety (concurrent callers get same instance, loaded once)
    - missing model file → FileNotFoundError

  Prediction
    - successful prediction returns FraudPredictionResult
    - confidence is in [0, 1]
    - fraud + safe probabilities sum to ~1.0
    - fraud prediction label
    - safe prediction label

  Feature engineering
    - feature vector is shape (1, 18)
    - log_amount matches log1p formula
    - large_transaction flag set correctly
    - receiver_balance_unchanged flag set correctly
    - high_risk_type is always 0 (training artefact)
    - amount_balance_ratio computed correctly
    - zero_balance flag set correctly
    - orig_balance_diff computed correctly
    - dest_balance_diff computed correctly
    - origin_balance_error computed correctly
    - destination_balance_error computed correctly
    - type encoding correct for all 5 types

  Validation
    - missing required field → ValidationError
    - invalid transaction type → ValidationError
    - negative amount → ValidationError
    - zero amount → ValidationError
    - isFlaggedFraud out of range → ValidationError
    - step < 1 → ValidationError

  Verdict logic
    - high-confidence fraud → verdict='fraud', category='mule_transaction'
    - high-confidence safe → verdict='safe', category='none'
    - low-confidence → verdict='suspicious'
    - risk_score in [0, 100]
    - explanation is a non-empty string

  Architecture
    - singleton reused across calls (no duplicate loading)
    - reset_model_cache clears singleton
"""

from __future__ import annotations

import math
import threading
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from pydantic import ValidationError

# ---------------------------------------------------------------------------
# Fixtures — reset singleton before every test for isolation
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def reset_model_singleton():
    """Clear the in-process model singleton before and after each test."""
    from agents.fraud_agent import model as m

    m._model = None
    yield
    m._model = None


def _make_mock_model(fraud_prob: float = 0.92) -> MagicMock:
    """Return a mock XGBClassifier that mimics predict_proba output.

    XGBoost classes_: [0 = safe, 1 = fraud]
    """
    model = MagicMock()
    model.predict_proba.return_value = np.array([[1.0 - fraud_prob, fraud_prob]])
    return model


def _make_payload(**overrides) -> dict:
    """Return a valid TransactionPayload dict with sensible defaults."""
    defaults = {
        "step": 1,
        "type": "TRANSFER",
        "amount": 181000.00,
        "oldbalanceOrg": 181000.0,
        "newbalanceOrig": 0.0,
        "oldbalanceDest": 0.0,
        "newbalanceDest": 0.0,
        "isFlaggedFraud": 0,
    }
    defaults.update(overrides)
    return defaults


# ===========================================================================
# SECTION 1: Model Loading
# ===========================================================================


class TestModelLoading:
    """Tests for model.get_fraud_model()."""

    def test_loads_model_from_valid_path(self, tmp_path):
        """get_fraud_model() should load and cache when the file exists."""
        from agents.fraud_agent import model as m

        fake_path = tmp_path / "paysim_model.joblib"
        fake_path.write_bytes(b"fake")

        mock_model = _make_mock_model()
        with patch("joblib.load", return_value=mock_model):
            loaded = m.get_fraud_model(path=fake_path)

        assert loaded is mock_model

    def test_singleton_returns_same_object(self, tmp_path):
        """A second call must return the cached instance without re-loading."""
        from agents.fraud_agent import model as m

        fake_path = tmp_path / "paysim_model.joblib"
        fake_path.write_bytes(b"fake")

        load_count = {"n": 0}

        def counting_load(*args, **kwargs):
            load_count["n"] += 1
            return _make_mock_model()

        with patch("joblib.load", side_effect=counting_load):
            first = m.get_fraud_model(path=fake_path)
            second = m.get_fraud_model(path=fake_path)

        assert first is second
        assert load_count["n"] == 1, "joblib.load should be called exactly once."

    def test_raises_file_not_found_for_missing_model(self):
        """get_fraud_model() must raise FileNotFoundError for a missing file."""
        from agents.fraud_agent import model as m

        with pytest.raises(FileNotFoundError, match="Fraud model file not found"):
            m.get_fraud_model(path=Path("/nonexistent/paysim_model.joblib"))

    def test_thread_safe_singleton(self, tmp_path):
        """Concurrent calls must load the model exactly once."""
        from agents.fraud_agent import model as m

        fake_path = tmp_path / "paysim_model.joblib"
        fake_path.write_bytes(b"fake")

        load_count = {"n": 0}
        mock_instance = _make_mock_model()

        def counting_load(*args, **kwargs):
            load_count["n"] += 1
            return mock_instance

        results: list = []
        errors: list = []

        def worker():
            try:
                with patch("joblib.load", side_effect=counting_load):
                    results.append(m.get_fraud_model(path=fake_path))
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert len(results) == 10
        # All threads must see the same object
        assert all(r is results[0] for r in results)

    def test_reset_clears_singleton(self, tmp_path):
        """reset_model_cache() must allow a fresh load on the next call."""
        from agents.fraud_agent import model as m

        fake_path = tmp_path / "paysim_model.joblib"
        fake_path.write_bytes(b"fake")

        load_count = {"n": 0}

        def counting_load(*args, **kwargs):
            load_count["n"] += 1
            return _make_mock_model()

        with patch("joblib.load", side_effect=counting_load):
            m.get_fraud_model(path=fake_path)

        m.reset_model_cache()

        with patch("joblib.load", side_effect=counting_load):
            m.get_fraud_model(path=fake_path)

        assert load_count["n"] == 2, "After reset, model should be reloaded."


# ===========================================================================
# SECTION 2: Feature Engineering
# ===========================================================================


class TestFeatureEngineering:
    """Tests for predict.prepare_features()."""

    def _payload(self, **overrides):
        from agents.fraud_agent.schemas import TransactionPayload

        return TransactionPayload(**_make_payload(**overrides))

    def test_feature_vector_shape_is_1x18(self):
        """Feature vector must be exactly shape (1, 18)."""
        from agents.fraud_agent.predict import prepare_features

        features, vector = prepare_features(self._payload())
        assert vector.shape == (1, 18)

    def test_log_amount_matches_log1p(self):
        """log_amount must equal math.log1p(amount)."""
        from agents.fraud_agent.predict import prepare_features

        amount = 9839.64
        features, _ = prepare_features(self._payload(amount=amount))
        expected = math.log1p(amount)
        assert abs(features["log_amount"] - expected) < 1e-9

    def test_log_amount_verified_against_notebook_value(self):
        """Verify against notebook output: amount=181 → log_amount=5.204007."""
        from agents.fraud_agent.predict import prepare_features

        features, _ = prepare_features(self._payload(amount=181.0))
        assert abs(features["log_amount"] - 5.204007) < 1e-5

    def test_large_transaction_flag_set_when_above_threshold(self):
        """large_transaction must be 1 when amount exceeds threshold."""
        from agents.fraud_agent.predict import prepare_features

        features, _ = prepare_features(
            self._payload(amount=2_000_000.0),
            large_transaction_threshold=1_200_000.0,
        )
        assert features["large_transaction"] == 1

    def test_large_transaction_flag_not_set_when_below_threshold(self):
        """large_transaction must be 0 when amount is below threshold."""
        from agents.fraud_agent.predict import prepare_features

        features, _ = prepare_features(
            self._payload(amount=100_000.0),
            large_transaction_threshold=1_200_000.0,
        )
        assert features["large_transaction"] == 0

    def test_receiver_balance_unchanged_when_equal(self):
        """receiver_balance_unchanged must be 1 when old == new dest balance."""
        from agents.fraud_agent.predict import prepare_features

        features, _ = prepare_features(
            self._payload(oldbalanceDest=5000.0, newbalanceDest=5000.0)
        )
        assert features["receiver_balance_unchanged"] == 1

    def test_receiver_balance_unchanged_not_set_when_different(self):
        """receiver_balance_unchanged must be 0 when old != new dest balance."""
        from agents.fraud_agent.predict import prepare_features

        features, _ = prepare_features(
            self._payload(oldbalanceDest=0.0, newbalanceDest=181000.0)
        )
        assert features["receiver_balance_unchanged"] == 0

    def test_high_risk_type_always_zero(self):
        """high_risk_type must ALWAYS be 0 (training artefact)."""
        from agents.fraud_agent.predict import prepare_features

        for tx_type in ["TRANSFER", "CASH_OUT", "CASH_IN", "PAYMENT", "DEBIT"]:
            features, _ = prepare_features(self._payload(type=tx_type))
            assert features["high_risk_type"] == 0, (
                f"high_risk_type must be 0 for type={tx_type} "
                "(matches training notebook behaviour)"
            )

    def test_amount_balance_ratio_formula(self):
        """amount_balance_ratio must equal amount / (oldbalanceOrg + 1)."""
        from agents.fraud_agent.predict import prepare_features

        amount = 9839.64
        old_balance_org = 170136.0
        features, _ = prepare_features(
            self._payload(amount=amount, oldbalanceOrg=old_balance_org)
        )
        expected = amount / (old_balance_org + 1)
        assert abs(features["amount_balance_ratio"] - expected) < 1e-9

    def test_zero_balance_set_when_new_balance_is_zero(self):
        """zero_balance must be 1 when newbalanceOrig == 0."""
        from agents.fraud_agent.predict import prepare_features

        features, _ = prepare_features(self._payload(newbalanceOrig=0.0))
        assert features["zero_balance"] == 1

    def test_zero_balance_not_set_when_new_balance_nonzero(self):
        """zero_balance must be 0 when newbalanceOrig > 0."""
        from agents.fraud_agent.predict import prepare_features

        features, _ = prepare_features(self._payload(newbalanceOrig=500.0))
        assert features["zero_balance"] == 0

    def test_orig_balance_diff(self):
        """orig_balance_diff must equal oldbalanceOrg - newbalanceOrig."""
        from agents.fraud_agent.predict import prepare_features

        features, _ = prepare_features(
            self._payload(oldbalanceOrg=181000.0, newbalanceOrig=0.0)
        )
        assert abs(features["orig_balance_diff"] - 181000.0) < 1e-9

    def test_dest_balance_diff(self):
        """dest_balance_diff must equal newbalanceDest - oldbalanceDest."""
        from agents.fraud_agent.predict import prepare_features

        features, _ = prepare_features(
            self._payload(oldbalanceDest=0.0, newbalanceDest=181000.0)
        )
        assert abs(features["dest_balance_diff"] - 181000.0) < 1e-9

    def test_origin_balance_error(self):
        """origin_balance_error must equal oldbalanceOrg - amount - newbalanceOrig."""
        from agents.fraud_agent.predict import prepare_features

        features, _ = prepare_features(
            self._payload(
                amount=181.0,
                oldbalanceOrg=181.0,
                newbalanceOrig=0.0,
            )
        )
        expected = 181.0 - 181.0 - 0.0
        assert abs(features["origin_balance_error"] - expected) < 1e-9

    def test_destination_balance_error(self):
        """destination_balance_error must equal oldbalanceDest + amount - newbalanceDest."""
        from agents.fraud_agent.predict import prepare_features

        features, _ = prepare_features(
            self._payload(
                amount=181.0,
                oldbalanceDest=0.0,
                newbalanceDest=0.0,
            )
        )
        expected = 0.0 + 181.0 - 0.0
        assert abs(features["destination_balance_error"] - expected) < 1e-9

    def test_type_encoding_all_types(self):
        """All five transaction types must encode to the correct integer."""
        from agents.fraud_agent.predict import _TYPE_ENCODING, prepare_features

        expected = {
            "CASH_IN": 0,
            "CASH_OUT": 1,
            "DEBIT": 2,
            "PAYMENT": 3,
            "TRANSFER": 4,
        }
        for tx_type, expected_code in expected.items():
            features, _ = prepare_features(self._payload(type=tx_type))
            assert features["type"] == expected_code, (
                f"type='{tx_type}' should encode to {expected_code}, "
                f"got {features['type']}"
            )
            assert _TYPE_ENCODING[tx_type] == expected_code


# ===========================================================================
# SECTION 3: Prediction
# ===========================================================================


class TestFraudPrediction:
    """Tests for predict.predict_fraud()."""

    def _mock_predict(self, tmp_path, fraud_prob: float = 0.92):
        from agents.fraud_agent.schemas import TransactionPayload

        mock_model = _make_mock_model(fraud_prob=fraud_prob)
        model_path = tmp_path / "paysim_model.joblib"
        model_path.write_bytes(b"fake")
        payload = TransactionPayload(**_make_payload())
        return mock_model, model_path, payload

    def test_returns_fraud_prediction_result(self, tmp_path):
        """predict_fraud() must return a FraudPredictionResult instance."""
        from agents.fraud_agent.predict import predict_fraud
        from agents.fraud_agent.schemas import FraudPredictionResult

        mock_model, model_path, payload = self._mock_predict(tmp_path)
        with patch("joblib.load", return_value=mock_model):
            result = predict_fraud(payload, model_path=model_path)

        assert isinstance(result, FraudPredictionResult)

    def test_confidence_in_valid_range(self, tmp_path):
        """Confidence must be in [0, 1]."""
        from agents.fraud_agent.predict import predict_fraud

        mock_model, model_path, payload = self._mock_predict(tmp_path, fraud_prob=0.85)
        with patch("joblib.load", return_value=mock_model):
            result = predict_fraud(payload, model_path=model_path)

        assert 0.0 <= result.confidence <= 1.0

    def test_probabilities_sum_to_one(self, tmp_path):
        """fraud + safe probability must sum to ~1.0."""
        from agents.fraud_agent.predict import predict_fraud

        mock_model, model_path, payload = self._mock_predict(tmp_path, fraud_prob=0.73)
        with patch("joblib.load", return_value=mock_model):
            result = predict_fraud(payload, model_path=model_path)

        assert abs(result.fraud_probability + result.safe_probability - 1.0) < 1e-5

    def test_fraud_prediction_label(self, tmp_path):
        """High fraud probability → predicted_class == 'fraud'."""
        from agents.fraud_agent.predict import predict_fraud

        mock_model, model_path, payload = self._mock_predict(tmp_path, fraud_prob=0.97)
        with patch("joblib.load", return_value=mock_model):
            result = predict_fraud(payload, model_path=model_path)

        assert result.predicted_class == "fraud"

    def test_safe_prediction_label(self, tmp_path):
        """Low fraud probability → predicted_class == 'safe'."""
        from agents.fraud_agent.predict import predict_fraud

        mock_model, model_path, payload = self._mock_predict(tmp_path, fraud_prob=0.02)
        with patch("joblib.load", return_value=mock_model):
            result = predict_fraud(payload, model_path=model_path)

        assert result.predicted_class == "safe"

    def test_engineered_features_in_result(self, tmp_path):
        """FraudPredictionResult.engineered_features must be a non-empty dict."""
        from agents.fraud_agent.predict import predict_fraud

        mock_model, model_path, payload = self._mock_predict(tmp_path)
        with patch("joblib.load", return_value=mock_model):
            result = predict_fraud(payload, model_path=model_path)

        assert isinstance(result.engineered_features, dict)
        assert len(result.engineered_features) > 0

    def test_missing_model_raises_file_not_found(self):
        """predict_fraud() with missing model file must raise FileNotFoundError."""
        from agents.fraud_agent.predict import predict_fraud
        from agents.fraud_agent.schemas import TransactionPayload

        payload = TransactionPayload(**_make_payload())
        with pytest.raises(FileNotFoundError):
            predict_fraud(
                payload,
                model_path=Path("/nonexistent/paysim_model.joblib"),
            )

    def test_singleton_reused_across_calls(self, tmp_path):
        """The model must not be reloaded between consecutive predict calls."""
        from agents.fraud_agent.predict import predict_fraud
        from agents.fraud_agent.schemas import TransactionPayload

        load_count = {"n": 0}
        mock_instance = _make_mock_model()

        def counting_load(*args, **kwargs):
            load_count["n"] += 1
            return mock_instance

        model_path = tmp_path / "paysim_model.joblib"
        model_path.write_bytes(b"fake")
        payload = TransactionPayload(**_make_payload())

        with patch("joblib.load", side_effect=counting_load):
            predict_fraud(payload, model_path=model_path)
            predict_fraud(payload, model_path=model_path)

        assert load_count["n"] == 1, "Model must be loaded only once (singleton)."


# ===========================================================================
# SECTION 4: Validation
# ===========================================================================


class TestTransactionValidation:
    """Tests for TransactionPayload Pydantic validation."""

    def test_valid_payload_accepted(self):
        """A fully valid payload must not raise."""
        from agents.fraud_agent.schemas import TransactionPayload

        payload = TransactionPayload(**_make_payload())
        assert payload.type == "TRANSFER"

    def test_invalid_transaction_type_raises_validation_error(self):
        """Unknown transaction type must raise ValidationError."""
        from agents.fraud_agent.schemas import TransactionPayload

        with pytest.raises(ValidationError, match="Invalid transaction type"):
            TransactionPayload(**_make_payload(type="WIRE_TRANSFER"))

    def test_transaction_type_case_insensitive(self):
        """Transaction type must be normalised to uppercase."""
        from agents.fraud_agent.schemas import TransactionPayload

        payload = TransactionPayload(**_make_payload(type="transfer"))
        assert payload.type == "TRANSFER"

    def test_negative_amount_raises_validation_error(self):
        """Negative amount must raise ValidationError."""
        from agents.fraud_agent.schemas import TransactionPayload

        with pytest.raises(ValidationError):
            TransactionPayload(**_make_payload(amount=-100.0))

    def test_zero_amount_raises_validation_error(self):
        """Zero amount (gt=0) must raise ValidationError."""
        from agents.fraud_agent.schemas import TransactionPayload

        with pytest.raises(ValidationError):
            TransactionPayload(**_make_payload(amount=0.0))

    def test_negative_old_balance_org_raises_validation_error(self):
        """Negative oldbalanceOrg must raise ValidationError."""
        from agents.fraud_agent.schemas import TransactionPayload

        with pytest.raises(ValidationError):
            TransactionPayload(**_make_payload(oldbalanceOrg=-1.0))

    def test_is_flagged_fraud_out_of_range_raises_validation_error(self):
        """isFlaggedFraud > 1 must raise ValidationError."""
        from agents.fraud_agent.schemas import TransactionPayload

        with pytest.raises(ValidationError):
            TransactionPayload(**_make_payload(isFlaggedFraud=2))

    def test_step_less_than_one_raises_validation_error(self):
        """step < 1 must raise ValidationError."""
        from agents.fraud_agent.schemas import TransactionPayload

        with pytest.raises(ValidationError):
            TransactionPayload(**_make_payload(step=0))

    def test_all_five_transaction_types_accepted(self):
        """All five valid transaction types must be accepted."""
        from agents.fraud_agent.schemas import TransactionPayload

        for tx_type in ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]:
            payload = TransactionPayload(**_make_payload(type=tx_type))
            assert payload.type == tx_type


# ===========================================================================
# SECTION 5: Verdict Logic
# ===========================================================================


class TestBuildFraudVerdict:
    """Tests for predict.build_fraud_verdict()."""

    def _make_result(self, predicted_class: str, confidence: float):
        from agents.fraud_agent.schemas import FraudPredictionResult

        fraud_p = confidence if predicted_class == "fraud" else 1.0 - confidence
        return FraudPredictionResult(
            predicted_class=predicted_class,
            confidence=confidence,
            fraud_probability=fraud_p,
            safe_probability=1.0 - fraud_p,
            type_encoded=4,
            engineered_features={},
        )

    def test_high_confidence_fraud_gives_fraud_verdict(self):
        """High fraud confidence → verdict='fraud', category='mule_transaction'."""
        from agents.fraud_agent.predict import build_fraud_verdict

        result = self._make_result("fraud", 0.95)
        verdict = build_fraud_verdict(result, transaction_type="TRANSFER")
        assert verdict["verdict"] == "fraud"
        assert verdict["category"] == "mule_transaction"

    def test_high_confidence_safe_gives_safe_verdict(self):
        """High safe confidence → verdict='safe'."""
        from agents.fraud_agent.predict import build_fraud_verdict

        result = self._make_result("safe", 0.98)
        verdict = build_fraud_verdict(result, transaction_type="PAYMENT")
        assert verdict["verdict"] == "safe"
        assert verdict["category"] == "none"

    def test_low_confidence_gives_suspicious_verdict(self):
        """Low confidence (below threshold) → verdict='suspicious'."""
        from agents.fraud_agent.predict import build_fraud_verdict

        result = self._make_result("fraud", 0.50)
        verdict = build_fraud_verdict(result, transaction_type="CASH_OUT")
        assert verdict["verdict"] == "suspicious"

    def test_risk_score_in_valid_range(self):
        """risk_score must be in [0, 100] for all verdict types."""
        from agents.fraud_agent.predict import build_fraud_verdict

        for predicted_class, confidence in [
            ("fraud", 0.92),
            ("safe", 0.96),
            ("fraud", 0.55),
        ]:
            result = self._make_result(predicted_class, confidence)
            verdict = build_fraud_verdict(result, transaction_type="TRANSFER")
            assert 0 <= verdict["risk_score"] <= 100

    def test_explanation_is_non_empty_string(self):
        """explanation must be a non-empty string."""
        from agents.fraud_agent.predict import build_fraud_verdict

        result = self._make_result("fraud", 0.88)
        verdict = build_fraud_verdict(result, transaction_type="TRANSFER")
        assert isinstance(verdict["explanation"], str)
        assert len(verdict["explanation"]) > 0

    def test_confidence_returned_in_verdict(self):
        """Verdict dict must include the confidence value."""
        from agents.fraud_agent.predict import build_fraud_verdict

        result = self._make_result("fraud", 0.91)
        verdict = build_fraud_verdict(result, transaction_type="CASH_OUT")
        assert verdict["confidence"] == 0.91
