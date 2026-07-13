"""
test_api.py — Unit tests for the FastAPI layer using TestClient.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health endpoints
# ---------------------------------------------------------------------------


def test_get_status():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "SentinelAI"
    assert data["status"] == "operational"


def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


# ---------------------------------------------------------------------------
# Currency endpoints
# ---------------------------------------------------------------------------


@patch("api.routers.currency.predict")
def test_currency_analyze_success(mock_predict):
    from agents.currency_agent.schemas import PredictionResult

    mock_predict.return_value = PredictionResult(
        predicted_class="fake",
        confidence=0.95,
        probabilities={"fake": 0.95, "real": 0.05},
        image_size=(224, 224),
    )

    response = client.post(
        "/currency/analyze",
        data={"case_id": "c-test-01"},
        files={"image": ("test.jpg", b"fake_image_bytes", "image/jpeg")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == "c-test-01"
    assert data["verdict"] == "fraud"
    assert data["category"] == "counterfeit_note"


@patch("api.routers.currency.predict")
def test_currency_analyze_missing_file(mock_predict):
    response = client.post(
        "/currency/analyze",
        data={"case_id": "c-test-01"},
        # No files payload
    )
    # Pydantic missing required field (Validation error)
    assert response.status_code == 422


@patch("api.routers.currency.predict")
def test_currency_analyze_inference_failure(mock_predict):
    mock_predict.side_effect = RuntimeError("Model forward pass failed")

    response = client.post(
        "/currency/analyze",
        data={"case_id": "c-test-01"},
        files={"image": ("test.jpg", b"fake_image_bytes", "image/jpeg")},
    )
    # RuntimeError is mapped to 500
    assert response.status_code == 500
    assert "failed" in response.json()["detail"]


# ---------------------------------------------------------------------------
# Scam SMS endpoints
# ---------------------------------------------------------------------------


@patch("api.routers.scam.predict_sms")
def test_scam_sms_success(mock_predict_sms):
    from agents.scam_comm_agent.schemas import SMSPredictionResult

    mock_predict_sms.return_value = SMSPredictionResult(
        predicted_class="scam",
        confidence=0.99,
        scam_probability=0.99,
        ham_probability=0.01,
        cleaned_text="test scam",
    )

    response = client.post(
        "/scam/sms",
        json={
            "case_id": "s-test-01",
            "input_type": "sms",
            "payload": {"text": "You won a lottery!"},
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == "s-test-01"
    assert data["verdict"] == "fraud"


def test_scam_sms_wrong_input_type():
    response = client.post(
        "/scam/sms",
        json={
            "case_id": "s-test-01",
            "input_type": "url",
            "payload": {"url": "http://evil.com"},
        },
    )
    # Our custom validation in the router returns 400
    assert response.status_code == 400


@patch("api.routers.scam.predict_sms")
def test_scam_sms_value_error(mock_predict_sms):
    mock_predict_sms.side_effect = ValueError("SMS text must be a non-empty string.")

    response = client.post(
        "/scam/sms",
        json={"case_id": "s-test-01", "input_type": "sms", "payload": {"text": "   "}},
    )
    # ValueError mapped to 400
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# Scam URL endpoints
# ---------------------------------------------------------------------------


@patch("api.routers.scam.predict_url")
def test_scam_url_success(mock_predict_url):
    from agents.scam_comm_agent.schemas import URLPredictionResult

    mock_predict_url.return_value = URLPredictionResult(
        predicted_class="phishing",
        confidence=0.92,
        phishing_probability=0.92,
        safe_probability=0.08,
        features={"url_length": 15},
    )

    response = client.post(
        "/scam/url",
        json={
            "case_id": "u-test-01",
            "input_type": "url",
            "payload": {"url": "http://evil.com/login"},
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == "u-test-01"
    assert data["verdict"] == "fraud"


@patch("api.routers.scam.predict_url")
def test_scam_url_file_not_found(mock_predict_url):
    mock_predict_url.side_effect = FileNotFoundError(
        "xgboost_phishing.joblib not found"
    )

    response = client.post(
        "/scam/url",
        json={
            "case_id": "u-test-01",
            "input_type": "url",
            "payload": {"url": "http://evil.com"},
        },
    )
    # FileNotFoundError mapped to 404
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Fraud endpoints
# ---------------------------------------------------------------------------


@patch("api.routers.fraud.predict_fraud")
def test_fraud_analyze_success(mock_predict_fraud):
    from agents.fraud_agent.schemas import FraudPredictionResult

    mock_predict_fraud.return_value = FraudPredictionResult(
        predicted_class="fraud",
        confidence=0.88,
        fraud_probability=0.88,
        safe_probability=0.12,
        type_encoded=4,
        engineered_features={"amount_balance_ratio": 0.5},
    )

    response = client.post(
        "/fraud/analyze",
        json={
            "case_id": "f-test-01",
            "input_type": "transaction",
            "payload": {
                "step": 1,
                "type": "TRANSFER",
                "amount": 50000.0,
                "oldbalanceOrg": 100000.0,
                "newbalanceOrig": 50000.0,
                "oldbalanceDest": 0.0,
                "newbalanceDest": 50000.0,
                "isFlaggedFraud": 0,
            },
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["case_id"] == "f-test-01"
    assert data["verdict"] == "fraud"


def test_fraud_analyze_validation_error():
    response = client.post(
        "/fraud/analyze",
        json={
            "case_id": "f-test-01",
            "input_type": "transaction",
            "payload": {
                "step": 1,
                "type": "INVALID_TYPE",
                "amount": 50000.0,
                "oldbalanceOrg": 100000.0,
                "newbalanceOrig": 50000.0,
                "oldbalanceDest": 0.0,
                "newbalanceDest": 50000.0,
            },
        },
    )
    # Pydantic validator catches INVALID_TYPE
    assert response.status_code == 422
