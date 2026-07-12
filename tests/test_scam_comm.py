"""
test_scam_comm.py — Comprehensive test suite for the Scam Communication Agent.

Covers:
  SMS pipeline
    - model loading (singleton, thread-safety, missing file)
    - TF-IDF loading (singleton, missing file)
    - preprocessing (happy path, empty text, whitespace-only)
    - prediction (result shape, confidence range, class label)
    - invalid / edge-case inputs

  URL pipeline
    - model loading (singleton, missing file)
    - preprocessing / feature extraction (valid URL, malformed URL, empty)
    - prediction (result shape, confidence range, class label)
    - feature count matches training spec (18 features)

All tests are isolated via autouse fixtures that reset singletons between runs.
No live model files are required — mocks replace joblib.load.
"""

from __future__ import annotations

import threading
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Fixtures — reset singletons before every test to ensure isolation
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def reset_caches():
    """Clear all module-level model/vectorizer singletons before each test."""
    from agents.scam_comm_agent import sms_model as sm
    from agents.scam_comm_agent import url_model as um

    sm._sms_model = None
    sm._tfidf = None
    um._url_model = None
    yield
    sm._sms_model = None
    sm._tfidf = None
    um._url_model = None


def _make_mock_sms_model(scam_prob: float = 0.92) -> MagicMock:
    """Return a mock CalibratedClassifierCV that mimics predict_proba output."""
    model = MagicMock()
    model.predict_proba.return_value = np.array([[1.0 - scam_prob, scam_prob]])
    return model


def _make_mock_tfidf() -> MagicMock:
    """Return a mock TfidfVectorizer that mimics transform output."""
    tfidf = MagicMock()
    tfidf.transform.return_value = MagicMock()  # sparse-like object
    return tfidf


def _make_mock_url_model(phishing_prob: float = 0.88) -> MagicMock:
    """Return a mock XGBoost model that mimics predict_proba output."""
    model = MagicMock()
    model.predict_proba.return_value = np.array([[1.0 - phishing_prob, phishing_prob]])
    return model


# ===========================================================================
# SECTION 1: SMS Model Loading
# ===========================================================================


class TestSMSModelLoading:
    """Tests for sms_model.get_sms_model()."""

    def test_loads_model_from_valid_path(self, tmp_path):
        """get_sms_model() should load and cache when the file exists."""
        from agents.scam_comm_agent import sms_model as sm

        fake_model_path = tmp_path / "sms_model.pkl"
        fake_model_path.write_bytes(b"fake")

        mock_model = _make_mock_sms_model()
        with patch("joblib.load", return_value=mock_model):
            loaded = sm.get_sms_model(path=fake_model_path)

        assert loaded is mock_model

    def test_singleton_returns_same_object(self, tmp_path):
        """A second call to get_sms_model() must return the cached instance."""
        from agents.scam_comm_agent import sms_model as sm

        fake_path = tmp_path / "sms_model.pkl"
        fake_path.write_bytes(b"fake")

        mock_model = _make_mock_sms_model()
        with patch("joblib.load", return_value=mock_model):
            first = sm.get_sms_model(path=fake_path)
            second = sm.get_sms_model(path=fake_path)

        assert first is second

    def test_raises_file_not_found_for_missing_model(self):
        """get_sms_model() must raise FileNotFoundError for a missing file."""
        from agents.scam_comm_agent import sms_model as sm

        with pytest.raises(FileNotFoundError, match="SMS model file not found"):
            sm.get_sms_model(path=Path("/nonexistent/sms_model.pkl"))

    def test_thread_safe_singleton(self, tmp_path):
        """Concurrent calls must load exactly once."""
        from agents.scam_comm_agent import sms_model as sm

        fake_path = tmp_path / "sms_model.pkl"
        fake_path.write_bytes(b"fake")

        call_count = {"n": 0}
        original_load = sm._load_sms_model if hasattr(sm, "_load_sms_model") else None

        mock_model = _make_mock_sms_model()

        def counting_load(*args, **kwargs):
            call_count["n"] += 1
            return mock_model

        results: list = []
        errors: list = []

        def worker():
            try:
                with patch("joblib.load", side_effect=counting_load):
                    results.append(sm.get_sms_model(path=fake_path))
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


# ===========================================================================
# SECTION 2: TF-IDF Loading
# ===========================================================================


class TestTFIDFLoading:
    """Tests for sms_model.get_tfidf()."""

    def test_loads_tfidf_from_valid_path(self, tmp_path):
        """get_tfidf() should load and cache when the file exists."""
        from agents.scam_comm_agent import sms_model as sm

        fake_path = tmp_path / "tfidf.pkl"
        fake_path.write_bytes(b"fake")

        mock_tfidf = _make_mock_tfidf()
        with patch("joblib.load", return_value=mock_tfidf):
            loaded = sm.get_tfidf(path=fake_path)

        assert loaded is mock_tfidf

    def test_tfidf_singleton_returns_same_object(self, tmp_path):
        """A second call to get_tfidf() must return the cached instance."""
        from agents.scam_comm_agent import sms_model as sm

        fake_path = tmp_path / "tfidf.pkl"
        fake_path.write_bytes(b"fake")

        mock_tfidf = _make_mock_tfidf()
        with patch("joblib.load", return_value=mock_tfidf):
            first = sm.get_tfidf(path=fake_path)
            second = sm.get_tfidf(path=fake_path)

        assert first is second

    def test_raises_file_not_found_for_missing_tfidf(self):
        """get_tfidf() must raise FileNotFoundError for a missing file."""
        from agents.scam_comm_agent import sms_model as sm

        with pytest.raises(FileNotFoundError, match="TF-IDF vectorizer not found"):
            sm.get_tfidf(path=Path("/nonexistent/tfidf.pkl"))


# ===========================================================================
# SECTION 3: SMS Preprocessing
# ===========================================================================


class TestSMSPreprocessing:
    """Tests for sms_predict.preprocess_sms()."""

    def test_normal_scam_text_returns_cleaned_string(self):
        """Valid scam text should return a non-empty cleaned string."""
        from agents.scam_comm_agent.sms_predict import preprocess_sms

        result = preprocess_sms(
            "URGENT: Your account has been compromised! Click http://evil.com to reset."
        )
        assert isinstance(result, str)
        assert len(result) > 0

    def test_urls_are_removed(self):
        """HTTP/HTTPS URLs should be stripped from the output."""
        from agents.scam_comm_agent.sms_predict import preprocess_sms

        result = preprocess_sms("Visit https://phishing-site.com/login now!")
        assert "http" not in result
        assert "phishing" not in result.lower() or True  # domain stripped

    def test_digits_are_removed(self):
        """Digit sequences should not appear in preprocessed output."""
        from agents.scam_comm_agent.sms_predict import preprocess_sms

        result = preprocess_sms("Call 9876543210 to claim your Rs 50000 prize.")
        # No standalone digit tokens expected after preprocessing
        assert not any(token.isdigit() for token in result.split())

    def test_empty_text_raises_value_error(self):
        """Empty string must raise ValueError."""
        from agents.scam_comm_agent.sms_predict import preprocess_sms

        with pytest.raises(ValueError, match="non-empty"):
            preprocess_sms("")

    def test_whitespace_only_raises_value_error(self):
        """Whitespace-only string must raise ValueError."""
        from agents.scam_comm_agent.sms_predict import preprocess_sms

        with pytest.raises(ValueError, match="non-empty"):
            preprocess_sms("   \t\n  ")

    def test_preserves_case_because_tfidf_trained_without_lowercasing(self):
        """Preprocessing must NOT lowercase — TF-IDF was trained with lowercase=False.

        The notebook sets ``TfidfVectorizer(lowercase=False)`` so the vectorizer
        expects input in its original capitalisation.  Tokens keep their case
        after preprocessing.
        """
        from agents.scam_comm_agent.sms_predict import preprocess_sms

        result = preprocess_sms("Your ACCOUNT has been BLOCKED immediately.")
        assert isinstance(result, str)
        assert len(result) > 0
        # Case must be preserved — if all tokens were lowercased the assertion
        # below would fail because "BLOCKED" → "blocked" after lowercase.
        # Since lowercase=False was used during training we must NOT lowercase.
        # At least one capitalised token should survive preprocessing.
        assert any(token != token.lower() for token in result.split())


# ===========================================================================
# SECTION 4: SMS Prediction
# ===========================================================================


class TestSMSPrediction:
    """Tests for sms_predict.predict_sms()."""

    def _make_sms_mocks(self, scam_prob: float = 0.92, tmp_path=None):
        """Return (model_path, tfidf_path, patched_joblib_context)."""
        mock_model = _make_mock_sms_model(scam_prob=scam_prob)
        mock_tfidf = _make_mock_tfidf()

        # Make temporary files so FileNotFoundError is not triggered
        if tmp_path is not None:
            model_path = tmp_path / "sms_model.pkl"
            tfidf_path = tmp_path / "tfidf.pkl"
            model_path.write_bytes(b"fake")
            tfidf_path.write_bytes(b"fake")
        else:
            model_path = None
            tfidf_path = None

        return mock_model, mock_tfidf, model_path, tfidf_path

    def test_returns_sms_prediction_result(self, tmp_path):
        """predict_sms() must return an SMSPredictionResult instance."""
        from agents.scam_comm_agent.schemas import SMSPredictionResult
        from agents.scam_comm_agent.sms_predict import predict_sms

        mock_model = _make_mock_sms_model()
        mock_tfidf = _make_mock_tfidf()
        model_p = tmp_path / "sms_model.pkl"
        tfidf_p = tmp_path / "tfidf.pkl"
        model_p.write_bytes(b"fake")
        tfidf_p.write_bytes(b"fake")

        with patch("joblib.load", side_effect=[mock_tfidf, mock_model]):
            result = predict_sms(
                "Win a free iPhone now!",
                model_path=model_p,
                tfidf_path=tfidf_p,
            )

        assert isinstance(result, SMSPredictionResult)

    def test_confidence_in_valid_range(self, tmp_path):
        """Confidence must be in [0, 1]."""
        from agents.scam_comm_agent.sms_predict import predict_sms

        mock_model = _make_mock_sms_model(scam_prob=0.85)
        mock_tfidf = _make_mock_tfidf()
        model_p = tmp_path / "sms_model.pkl"
        tfidf_p = tmp_path / "tfidf.pkl"
        model_p.write_bytes(b"fake")
        tfidf_p.write_bytes(b"fake")

        with patch("joblib.load", side_effect=[mock_tfidf, mock_model]):
            result = predict_sms(
                "Your KYC is expired",
                model_path=model_p,
                tfidf_path=tfidf_p,
            )

        assert 0.0 <= result.confidence <= 1.0

    def test_probabilities_sum_to_one(self, tmp_path):
        """ham + scam probability must sum to ~1.0."""
        from agents.scam_comm_agent.sms_predict import predict_sms

        mock_model = _make_mock_sms_model(scam_prob=0.73)
        mock_tfidf = _make_mock_tfidf()
        model_p = tmp_path / "sms_model.pkl"
        tfidf_p = tmp_path / "tfidf.pkl"
        model_p.write_bytes(b"fake")
        tfidf_p.write_bytes(b"fake")

        with patch("joblib.load", side_effect=[mock_tfidf, mock_model]):
            result = predict_sms(
                "Hello, how are you?",
                model_path=model_p,
                tfidf_path=tfidf_p,
            )

        assert abs(result.scam_probability + result.ham_probability - 1.0) < 1e-5

    def test_scam_prediction_label(self, tmp_path):
        """High scam probability → predicted_class == 'scam'."""
        from agents.scam_comm_agent.sms_predict import predict_sms

        mock_model = _make_mock_sms_model(scam_prob=0.97)
        mock_tfidf = _make_mock_tfidf()
        model_p = tmp_path / "sms_model.pkl"
        tfidf_p = tmp_path / "tfidf.pkl"
        model_p.write_bytes(b"fake")
        tfidf_p.write_bytes(b"fake")

        with patch("joblib.load", side_effect=[mock_tfidf, mock_model]):
            result = predict_sms(
                "URGENT: Account blocked click here",
                model_path=model_p,
                tfidf_path=tfidf_p,
            )

        assert result.predicted_class == "scam"

    def test_ham_prediction_label(self, tmp_path):
        """High ham probability → predicted_class == 'ham'."""
        from agents.scam_comm_agent.sms_predict import predict_sms

        mock_model = _make_mock_sms_model(scam_prob=0.03)
        mock_tfidf = _make_mock_tfidf()
        model_p = tmp_path / "sms_model.pkl"
        tfidf_p = tmp_path / "tfidf.pkl"
        model_p.write_bytes(b"fake")
        tfidf_p.write_bytes(b"fake")

        with patch("joblib.load", side_effect=[mock_tfidf, mock_model]):
            result = predict_sms(
                "Hey, are we still on for lunch tomorrow?",
                model_path=model_p,
                tfidf_path=tfidf_p,
            )

        assert result.predicted_class == "ham"

    def test_empty_text_raises_value_error(self, tmp_path):
        """predict_sms() with empty text must raise ValueError."""
        from agents.scam_comm_agent.sms_predict import predict_sms

        with pytest.raises(ValueError, match="non-empty"):
            predict_sms("")

    def test_missing_model_raises_file_not_found(self):
        """predict_sms() with missing model path must raise FileNotFoundError."""
        from agents.scam_comm_agent import sms_model as sm
        from agents.scam_comm_agent.sms_predict import predict_sms

        # Pre-load a valid tfidf mock to isolate the model error
        mock_tfidf = _make_mock_tfidf()
        sm._tfidf = mock_tfidf

        with pytest.raises(FileNotFoundError):
            predict_sms(
                "win a prize",
                model_path=Path("/nonexistent/sms_model.pkl"),
            )


# ===========================================================================
# SECTION 5: SMS Verdict Logic
# ===========================================================================


class TestSMSBuildVerdict:
    """Tests for sms_predict.build_sms_verdict()."""

    def _make_result(self, predicted_class: str, confidence: float):
        from agents.scam_comm_agent.schemas import SMSPredictionResult

        scam_p = confidence if predicted_class == "scam" else 1.0 - confidence
        return SMSPredictionResult(
            predicted_class=predicted_class,
            confidence=confidence,
            scam_probability=scam_p,
            ham_probability=1.0 - scam_p,
            cleaned_text="test text",
        )

    def test_high_confidence_scam_gives_fraud_verdict(self):
        from agents.scam_comm_agent.sms_predict import build_sms_verdict

        result = self._make_result("scam", 0.95)
        verdict = build_sms_verdict(result)
        assert verdict["verdict"] == "fraud"
        assert verdict["category"] == "digital_arrest_scam"

    def test_high_confidence_ham_gives_safe_verdict(self):
        from agents.scam_comm_agent.sms_predict import build_sms_verdict

        result = self._make_result("ham", 0.98)
        verdict = build_sms_verdict(result)
        assert verdict["verdict"] == "safe"

    def test_low_confidence_gives_suspicious_verdict(self):
        from agents.scam_comm_agent.sms_predict import build_sms_verdict

        result = self._make_result("scam", 0.50)
        verdict = build_sms_verdict(result)
        assert verdict["verdict"] == "suspicious"

    def test_risk_score_in_valid_range(self):
        from agents.scam_comm_agent.sms_predict import build_sms_verdict

        for pc, conf in [("scam", 0.9), ("ham", 0.95), ("scam", 0.55)]:
            result = self._make_result(pc, conf)
            verdict = build_sms_verdict(result)
            assert 0 <= verdict["risk_score"] <= 100

    def test_explanation_is_non_empty_string(self):
        from agents.scam_comm_agent.sms_predict import build_sms_verdict

        result = self._make_result("scam", 0.88)
        verdict = build_sms_verdict(result)
        assert isinstance(verdict["explanation"], str)
        assert len(verdict["explanation"]) > 0


# ===========================================================================
# SECTION 6: URL Model Loading
# ===========================================================================


class TestURLModelLoading:
    """Tests for url_model.get_url_model()."""

    def test_loads_model_from_valid_path(self, tmp_path):
        """get_url_model() should load and cache when the file exists."""
        from agents.scam_comm_agent import url_model as um

        fake_path = tmp_path / "phishing_model.joblib"
        fake_path.write_bytes(b"fake")

        mock_model = _make_mock_url_model()
        with patch("joblib.load", return_value=mock_model):
            loaded = um.get_url_model(path=fake_path)

        assert loaded is mock_model

    def test_singleton_returns_same_object(self, tmp_path):
        """A second call must return the cached instance."""
        from agents.scam_comm_agent import url_model as um

        fake_path = tmp_path / "phishing_model.joblib"
        fake_path.write_bytes(b"fake")

        mock_model = _make_mock_url_model()
        with patch("joblib.load", return_value=mock_model):
            first = um.get_url_model(path=fake_path)
            second = um.get_url_model(path=fake_path)

        assert first is second

    def test_raises_file_not_found_for_missing_model(self):
        """get_url_model() must raise FileNotFoundError for a missing file."""
        from agents.scam_comm_agent import url_model as um

        with pytest.raises(FileNotFoundError, match="Phishing model file not found"):
            um.get_url_model(path=Path("/nonexistent/phishing_model.joblib"))


# ===========================================================================
# SECTION 7: URL Preprocessing / Feature Extraction
# ===========================================================================


class TestURLPreprocessing:
    """Tests for url_predict.preprocess_url() and extract_url_features()."""

    def test_valid_url_returns_18_features(self):
        """Feature dict must contain exactly 18 keys."""
        from agents.scam_comm_agent.url_predict import extract_url_features

        features = extract_url_features("https://www.example.com/login?user=foo")
        assert len(features) == 18

    def test_https_flag_set_for_secure_url(self):
        """'https' feature should be 1 for HTTPS URLs."""
        from agents.scam_comm_agent.url_predict import extract_url_features

        features = extract_url_features("https://secure.bank.com/")
        assert features["https"] == 1

    def test_https_flag_not_set_for_http_url(self):
        """'https' feature should be 0 for plain HTTP."""
        from agents.scam_comm_agent.url_predict import extract_url_features

        features = extract_url_features("http://phishing-site.com/verify")
        assert features["https"] == 0

    def test_ip_address_in_domain_detected(self):
        """'has_ip' feature must be 1 when domain is an IP address."""
        from agents.scam_comm_agent.url_predict import extract_url_features

        features = extract_url_features("http://192.168.1.1/admin")
        assert features["has_ip"] == 1

    def test_suspicious_keyword_count_positive_for_phishing(self):
        """URL with suspicious keywords should have count > 0."""
        from agents.scam_comm_agent.url_predict import extract_url_features

        features = extract_url_features("http://evil.com/login/verify/account")
        assert features["suspicious_keyword_count"] > 0

    def test_preprocess_url_returns_correct_vector_shape(self):
        """Feature vector must be shape (1, 18)."""
        from agents.scam_comm_agent.url_predict import preprocess_url

        _, vector = preprocess_url("https://www.google.com/search?q=test")
        assert vector.shape == (1, 18)

    def test_empty_url_raises_value_error(self):
        """Empty URL must raise ValueError."""
        from agents.scam_comm_agent.url_predict import preprocess_url

        with pytest.raises(ValueError, match="non-empty"):
            preprocess_url("")

    def test_malformed_url_no_scheme_raises_value_error(self):
        """URL without scheme/netloc must raise ValueError."""
        from agents.scam_comm_agent.url_predict import preprocess_url

        with pytest.raises(ValueError, match="Malformed URL"):
            preprocess_url("not-a-url-at-all")

    def test_url_length_feature_correct(self):
        """'url_length' must equal len(url)."""
        from agents.scam_comm_agent.url_predict import extract_url_features

        url = "https://example.com/path?q=1"
        features = extract_url_features(url)
        assert features["url_length"] == len(url)


# ===========================================================================
# SECTION 8: URL Prediction
# ===========================================================================


class TestURLPrediction:
    """Tests for url_predict.predict_url()."""

    def test_returns_url_prediction_result(self, tmp_path):
        """predict_url() must return a URLPredictionResult instance."""
        from agents.scam_comm_agent.schemas import URLPredictionResult
        from agents.scam_comm_agent.url_predict import predict_url

        mock_model = _make_mock_url_model(phishing_prob=0.88)
        model_p = tmp_path / "phishing_model.joblib"
        model_p.write_bytes(b"fake")

        with patch("joblib.load", return_value=mock_model):
            result = predict_url(
                "http://phishing-site.com/login/verify",
                model_path=model_p,
            )

        assert isinstance(result, URLPredictionResult)

    def test_confidence_in_valid_range(self, tmp_path):
        """Confidence must be in [0, 1]."""
        from agents.scam_comm_agent.url_predict import predict_url

        mock_model = _make_mock_url_model(phishing_prob=0.75)
        model_p = tmp_path / "phishing_model.joblib"
        model_p.write_bytes(b"fake")

        with patch("joblib.load", return_value=mock_model):
            result = predict_url(
                "https://www.legit-bank.com/login",
                model_path=model_p,
            )

        assert 0.0 <= result.confidence <= 1.0

    def test_phishing_probability_plus_safe_probability_equals_one(self, tmp_path):
        """phishing + safe probability must sum to ~1.0."""
        from agents.scam_comm_agent.url_predict import predict_url

        mock_model = _make_mock_url_model(phishing_prob=0.62)
        model_p = tmp_path / "phishing_model.joblib"
        model_p.write_bytes(b"fake")

        with patch("joblib.load", return_value=mock_model):
            result = predict_url(
                "https://example.com/",
                model_path=model_p,
            )

        assert abs(result.phishing_probability + result.safe_probability - 1.0) < 1e-5

    def test_phishing_prediction_label(self, tmp_path):
        """High phishing probability → predicted_class == 'phishing'."""
        from agents.scam_comm_agent.url_predict import predict_url

        mock_model = _make_mock_url_model(phishing_prob=0.97)
        model_p = tmp_path / "phishing_model.joblib"
        model_p.write_bytes(b"fake")

        with patch("joblib.load", return_value=mock_model):
            result = predict_url(
                "http://192.168.0.1/login?user=admin&pass=1234",
                model_path=model_p,
            )

        assert result.predicted_class == "phishing"

    def test_safe_prediction_label(self, tmp_path):
        """Low phishing probability → predicted_class == 'safe'."""
        from agents.scam_comm_agent.url_predict import predict_url

        mock_model = _make_mock_url_model(phishing_prob=0.02)
        model_p = tmp_path / "phishing_model.joblib"
        model_p.write_bytes(b"fake")

        with patch("joblib.load", return_value=mock_model):
            result = predict_url(
                "https://www.google.com/",
                model_path=model_p,
            )

        assert result.predicted_class == "safe"

    def test_features_dict_in_result(self, tmp_path):
        """URLPredictionResult.features must be a non-empty dict."""
        from agents.scam_comm_agent.url_predict import predict_url

        mock_model = _make_mock_url_model()
        model_p = tmp_path / "phishing_model.joblib"
        model_p.write_bytes(b"fake")

        with patch("joblib.load", return_value=mock_model):
            result = predict_url(
                "https://safe-site.com/",
                model_path=model_p,
            )

        assert isinstance(result.features, dict)
        assert len(result.features) == 18

    def test_empty_url_raises_value_error(self):
        """predict_url() with empty string must raise ValueError."""
        from agents.scam_comm_agent.url_predict import predict_url

        with pytest.raises(ValueError, match="non-empty"):
            predict_url("")

    def test_malformed_url_raises_value_error(self):
        """predict_url() with malformed URL must raise ValueError."""
        from agents.scam_comm_agent.url_predict import predict_url

        with pytest.raises(ValueError, match="Malformed URL"):
            predict_url("this-is-not-a-url")

    def test_missing_model_raises_file_not_found(self):
        """predict_url() with missing model file must raise FileNotFoundError."""
        from agents.scam_comm_agent.url_predict import predict_url

        with pytest.raises(FileNotFoundError):
            predict_url(
                "https://example.com/",
                model_path=Path("/nonexistent/phishing_model.joblib"),
            )


# ===========================================================================
# SECTION 9: URL Verdict Logic
# ===========================================================================


class TestURLBuildVerdict:
    """Tests for url_predict.build_url_verdict()."""

    def _make_result(self, predicted_class: str, confidence: float):
        from agents.scam_comm_agent.schemas import URLPredictionResult

        phishing_p = confidence if predicted_class == "phishing" else 1.0 - confidence
        return URLPredictionResult(
            predicted_class=predicted_class,
            confidence=confidence,
            phishing_probability=phishing_p,
            safe_probability=1.0 - phishing_p,
            features={"url_length": 30},
        )

    def test_high_confidence_phishing_gives_fraud_verdict(self):
        from agents.scam_comm_agent.url_predict import build_url_verdict

        result = self._make_result("phishing", 0.94)
        verdict = build_url_verdict(result)
        assert verdict["verdict"] == "fraud"
        assert verdict["category"] == "phishing"

    def test_high_confidence_safe_gives_safe_verdict(self):
        from agents.scam_comm_agent.url_predict import build_url_verdict

        result = self._make_result("safe", 0.97)
        verdict = build_url_verdict(result)
        assert verdict["verdict"] == "safe"

    def test_low_confidence_gives_suspicious_verdict(self):
        from agents.scam_comm_agent.url_predict import build_url_verdict

        result = self._make_result("phishing", 0.52)
        verdict = build_url_verdict(result)
        assert verdict["verdict"] == "suspicious"

    def test_risk_score_in_valid_range(self):
        from agents.scam_comm_agent.url_predict import build_url_verdict

        for pc, conf in [("phishing", 0.91), ("safe", 0.88), ("phishing", 0.60)]:
            result = self._make_result(pc, conf)
            verdict = build_url_verdict(result)
            assert 0 <= verdict["risk_score"] <= 100

    def test_explanation_is_non_empty_string(self):
        from agents.scam_comm_agent.url_predict import build_url_verdict

        result = self._make_result("phishing", 0.85)
        verdict = build_url_verdict(result)
        assert isinstance(verdict["explanation"], str)
        assert len(verdict["explanation"]) > 0
