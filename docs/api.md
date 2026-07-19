# API

## Agent Contract — `POST /analyze`

Every agent (Currency, Scam Comm SMS/URL, Fraud, Graph, Geo) implements this exact shape.

**Request Envelope:**
```json
{
  "case_id": "c-2026-0001",
  "input_type": "sms | url | transaction | image | graph_data | location",
  "payload": { "...": "agent-specific fields" }
}
```

**Response Envelope:**
```json
{
  "agent": "scam_comm_agent_sms | scam_comm_agent_url | fraud_agent | currency_agent | graph_agent | geo_agent",
  "case_id": "c-2026-0001",
  "verdict": "safe | suspicious | fraud",
  "confidence": 0.95,
  "risk_score": 90,
  "category": "digital_arrest | phishing | mule_transaction | counterfeit_note | fraud_ring | crime_hotspot | none",
  "explanation": "short human-readable reason",
  "evidence": { "...": "raw features/snippets used" },
  "processed_at": "ISO8601 timestamp"
}
```

## Agent Endpoints

### 1. Currency Agent — `POST /currency/analyze`
Analyzes currency images for counterfeit features.
```json
{
  "case_id": "c-2026-0001",
  "input_type": "currency",
  "payload": {
    "image_bytes": "base64_encoded_string=="
  }
}
```

### 2. Scam Communication SMS — `POST /scam/sms`
Classifies SMS text content using Linear SVM text classifier.
```json
{
  "case_id": "c-2026-0001",
  "input_type": "sms",
  "payload": {
    "text": "URGENT: Your bank account is locked. Verify at http://scam-link.com"
  }
}
```

### 3. Scam Communication URL — `POST /scam/url`
Evaluates domain/URL features for phishing risk using XGBoost.
```json
{
  "case_id": "c-2026-0001",
  "input_type": "url",
  "payload": {
    "url": "http://crypto-secure-auth-update.net/login"
  }
}
```

### 4. Transaction Fraud Agent — `POST /fraud/analyze`
Evaluates financial transfer records for anomaly/mule behavior.
```json
{
  "case_id": "c-2026-0001",
  "input_type": "transaction",
  "payload": {
    "amount": 500000.0,
    "oldbalanceOrg": 500000.0,
    "newbalanceOrig": 0.0,
    "oldbalanceDest": 0.0,
    "newbalanceDest": 500000.0,
    "type": "TRANSFER"
  }
}
```

### 5. Graph Intelligence Agent — `POST /graph/analyze`
Analyzes structural node/edge relationships in memory using NetworkX.
```json
{
  "case_id": "c-2026-0001",
  "input_type": "graph_data",
  "payload": {
    "entities": [
      { "type": "Phone Number", "id": "+919999988888" },
      { "type": "Victim", "id": "victim-01" }
    ],
    "relationships": [
      {
        "source_type": "Victim",
        "source_id": "victim-01",
        "target_type": "Phone Number",
        "target_id": "+919999988888",
        "type": "USED"
      }
    ]
  }
}
```

### 6. Geo Intelligence Agent — `POST /geo/analyze`
Evaluates geographical coordinates for spatial crime density, hotspot boundaries, and patrol planning.
```json
{
  "case_id": "c-2026-0001",
  "input_type": "location",
  "payload": {
    "latitude": 12.9716,
    "longitude": 77.5946,
    "radius_km": 5.0
  }
}
```

## Orchestrator — `POST /investigate`

**Request:**
```json
{
  "case_id": "c-2026-0001",
  "evidence": [
    { "input_type": "sms", "payload": { "text": "..." } },
    { "input_type": "transaction", "payload": { "amount": 50000, "...": "..." } },
    { "input_type": "graph_data", "payload": { "entities": [], "relationships": [] } }
  ]
}
```

**Behavior:** fans out to all active agents matching the submitted `input_type`s in parallel, writes each result to `agent_results`, then calls the Fusion Agent. If no explicit `graph_data` is supplied, raw evidence items are dynamically parsed into the Graph Agent as well.

**Response:** the `fusion_reports` row for this `case_id` (see `database.md`).

## Fusion Agent — `POST /fuse`

**Request:** `{ "case_id": "c-2026-0001" }` — pulls all rows from `agent_results` for that case.

**Response:**
```json
{
  "case_id": "c-2026-0001",
  "final_verdict": "Organized Digital Arrest Scam",
  "overall_risk": 93,
  "narrative": "...",
  "recommended_action": ["Freeze account", "Notify Cyber Cell", "Alert bank", "Generate FIR draft"]
}
```

Fusion logic: weighted aggregation of `risk_score` across agents + a small rules layer (e.g. "if 2+ agents report fraud with risk_score > 80, escalate to organized-scam verdict"). No ML model required for this to be a legitimate reasoning engine.

## Data Sources by Agent

| Agent | Dataset / Source | Notes |
|---|---|---|
| Fraud (transaction) | Kaggle "Credit Card Fraud Detection" (ULB) or "IEEE-CIS Fraud Detection" | Imbalanced — report PR-AUC/recall, not accuracy |
| Scam SMS | Kaggle "SMS Spam Collection" + UCI SMS Spam, plus 100–200 hand-labeled India-specific scam messages | Hand-labeled set matters more than volume |
| Phishing URL | Kaggle "Phishing Website Dataset" (UCI) or PhishTank export | Feature-based XGBoost is enough — no transformer needed |
| Currency [stretch] | "Indian currency dataset" (Kaggle/Roboflow) | Fallback: rule-based watermark-region check instead of full YOLO |
| Voice [stretch] | Common Voice (STT), ASVspoof (spoof detection) | Use pretrained Whisper-small + pretrained ASVspoof checkpoint — do not train from scratch |

General principle: prefer fine-tuning or calling a pretrained model over training from scratch.

HTTP Status Codes

200 OK
400 Invalid Request
422 Validation Error
500 Internal Error
503 Agent Unavailable
504 Agent Timeout