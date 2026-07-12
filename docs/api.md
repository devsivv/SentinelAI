# API

## Agent Contract — `POST /analyze`

Every agent (Fraud, Scam Comm., Currency, Voice, Graph, Geo) implements this exact shape.

**Request:**
```json
{
  "case_id": "c-2026-0001",
  "input_type": "sms | url | transaction | image | audio",
  "payload": { "...": "agent-specific fields" }
}
```

**Response:**
```json
{
  "agent": "scam_sms_agent",
  "case_id": "c-2026-0001",
  "verdict": "safe | suspicious | fraud",
  "confidence": 0.0,
  "risk_score": 0,
  "category": "digital_arrest_scam | phishing | counterfeit_note | mule_transaction | none",
  "explanation": "short human-readable reason",
  "evidence": { "...": "raw features/snippets used" },
  "processed_at": "ISO8601 timestamp"
}
```

## Orchestrator — `POST /investigate`

**Request:**
```json
{
  "case_id": "c-2026-0001",
  "evidence": [
    { "input_type": "sms", "payload": { "text": "..." } },
    { "input_type": "transaction", "payload": { "amount": 50000, "...": "..." } }
  ]
}
```

**Behavior:** fans out to all active agents matching the submitted `input_type`s in parallel, writes each result to `agent_results`, then calls the Fusion Agent.

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