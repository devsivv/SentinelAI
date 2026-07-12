# Fraud Agent

Production inference layer for financial transaction fraud detection using the PaySim-trained XGBoost model.

## Pipeline

```
TransactionPayload
    → validate fields (Pydantic)
    → prepare_features() — 18 hand-engineered features matching training notebook
    → XGBoost predict_proba()
    → verdict / risk score / explanation
    → FraudPredictionResult
```

## Usage

```python
from agents.fraud_agent import TransactionPayload, predict_fraud, build_fraud_verdict

payload = TransactionPayload(
    step=1,
    type="TRANSFER",
    amount=181000.00,
    oldbalanceOrg=181000.0,
    newbalanceOrig=0.0,
    oldbalanceDest=0.0,
    newbalanceDest=0.0,
    isFlaggedFraud=0,
)

result = predict_fraud(payload, case_id="case-001")
verdict = build_fraud_verdict(result, transaction_type=payload.type, case_id="case-001")
```

## Required Model File

| Path | Description |
|------|-------------|
| `models/transactions/paysim_model.joblib` | Trained XGBoost classifier (joblib) |

## Transaction Types

| Type | Description |
|------|-------------|
| `CASH_IN` | Deposit into account |
| `CASH_OUT` | Withdrawal from account |
| `DEBIT` | Debit card payment |
| `PAYMENT` | Bill or merchant payment |
| `TRANSFER` | Account-to-account transfer |

## Features (18 total — must match training notebook exactly)

| # | Feature | Description |
|---|---------|-------------|
| 1 | `step` | Simulation step (hour) |
| 2 | `type` | LabelEncoded type: CASH_IN=0, CASH_OUT=1, DEBIT=2, PAYMENT=3, TRANSFER=4 |
| 3 | `amount` | Transaction amount |
| 4 | `oldbalanceOrg` | Origin balance before |
| 5 | `newbalanceOrig` | Origin balance after |
| 6 | `oldbalanceDest` | Destination balance before |
| 7 | `newbalanceDest` | Destination balance after |
| 8 | `isFlaggedFraud` | Legacy system flag (0/1) |
| 9 | `log_amount` | log(amount + 1) |
| 10 | `orig_balance_diff` | oldbalanceOrg − newbalanceOrig |
| 11 | `large_transaction` | 1 if amount > 95th-pctile threshold |
| 12 | `receiver_balance_unchanged` | 1 if oldbalanceDest == newbalanceDest |
| 13 | `high_risk_type` | Always 0 (training artefact — see predict.py docstring) |
| 14 | `amount_balance_ratio` | amount / (oldbalanceOrg + 1) |
| 15 | `zero_balance` | 1 if newbalanceOrig == 0 |
| 16 | `dest_balance_diff` | newbalanceDest − oldbalanceDest |
| 17 | `origin_balance_error` | oldbalanceOrg − amount − newbalanceOrig |
| 18 | `destination_balance_error` | oldbalanceDest + amount − newbalanceDest |

## Configuration

All paths are configurable via environment variables (prefix: `FRAUD_`):

| Variable | Default |
|----------|---------|
| `FRAUD_MODEL_PATH` | `models/transactions/paysim_model.joblib` |
| `FRAUD_CONFIDENCE_THRESHOLD` | `0.70` |
| `FRAUD_LARGE_TRANSACTION_THRESHOLD` | `1200000.0` |
| `FRAUD_LOG_LEVEL` | `INFO` |

## Dependencies

- `xgboost` — XGBoost classifier
- `joblib` — model serialization/deserialization
- `pydantic` / `pydantic-settings` — schema validation and configuration
- `numpy` — feature vector construction
