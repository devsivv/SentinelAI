# Graph Intelligence Agent

NetworkX-based in-memory entity relationship and linkage analysis agent.

---

## Overview

The Graph Intelligence Agent maps multi-modal evidence across cases, victims, suspects, and specific communication/financial identifiers to detect fraud rings, mule accounts, shared devices, and repeated identities.

It exposes a standardized `POST /analyze` API endpoint that returns an `AgentResult`-compliant response containing structural graph metrics under `evidence`.

---

## Module Structure

| Module | Responsibility |
|---|---|
| `__init__.py` | Package entrypoint, exposing public service functions and Pydantic schemas. |
| `main.py` | FastAPI application and router exposing `/analyze` and `/graph/analyze` endpoints. |
| `service.py` | Coordinates extraction, graph population, analysis, and verdict aggregation. |
| `model.py` | Singleton thread-safe wrapper around the global in-memory NetworkX MultiDiGraph. |
| `graph_builder.py` | Builds case nodes/edges and inserts them into the global NetworkX model. |
| `entity_extractor.py` | Handles extracting structured nodes/edges and normalizing identifiers (phone, URL, etc.). |
| `analyzer.py` | Implements structural network algorithms (connected components, centralities, clusters, risk). |
| `schemas.py` | Compliant Pydantic request/response models. |
| `config.py` | Handles environment variables and YAML settings. |
| `logging.py` | Sets up a rotating file logger at `logs/agents/graph_agent.log`. |

---

## Supported Entities and Relationships

**Entities:**
- `Case`, `Victim`, `Phone Number`, `Email`, `Bank Account`, `UPI ID`, `Device ID`, `IP Address`, `URL`, `Merchant`, `Transaction`, `Suspect`

**Relationships:**
- `USED`, `CONNECTED_TO`, `TRANSFERRED_TO`, `SHARES_PHONE`, `SHARES_DEVICE`, `SHARES_ACCOUNT`, `SHARES_URL`, `INVOLVES`, `LINKED_WITH`

---

## Normalization Standards

The agent automatically standardizes identifiers before graph construction:
- **Phone Numbers**: Normalizes to digits only (retains prefix `+`).
- **URLs**: Lowercases, removes protocol (http/https), query parameters, and trailing slashes.
- **Emails / UPI IDs**: Lowercases and strips whitespaces.
- **Bank Accounts / Devices**: Uppercases and removes spaces.

---

## Analysis Algorithms

1. **Connected Component Detection**: Identifies groups of connected nodes bridging multiple victims or cases.
2. **Repeated Entity Detection**: Flag entities appearing across different case contexts.
3. **Degree Centrality**: Computes degree centrality to highlight primary broker nodes/hubs.
4. **Suspicious Cluster (Fraud Ring) Detection**: Detects sub-graphs with high density, multiple victims, and known suspects.
5. **Network Risk Estimation**: Computes an aggregate risk score [0, 100] based on connectivity features.

---

## API Contract (Response Evidence)

All network intelligence findings are housed within `evidence` to avoid violating the top-level Agent Contract:

```json
{
  "agent": "graph_agent",
  "case_id": "c-2026-0001",
  "verdict": "fraud",
  "confidence": 0.9,
  "risk_score": 75,
  "category": "fraud_ring",
  "explanation": "Organized fraud ring or suspicious cluster detected...",
  "evidence": {
    "num_nodes": 12,
    "num_edges": 14,
    "connected_components": [
      ["c-2026-0001", "suspect-99", "+919999999999"]
    ],
    "repeated_entities": {
      "+919999999999": ["c-2026-0001", "c-2026-0002"]
    },
    "shared_phones": [],
    "shared_urls": [],
    "shared_upis": [],
    "shared_accounts": [],
    "shared_devices": [],
    "repeated_identities": [],
    "degree_centrality": {
      "+919999999999": 0.5
    },
    "suspicious_clusters": [],
    "network_risk_score": 75.0
  }
}
```

---

## Integration with Orchestrator and Fusion

### 1. Orchestrator Parallel Execution
- The Orchestrator runs all active agents (Currency, Scam SMS, Scam URL, Fraud, and Graph) concurrently.
- If raw evidence (e.g. transactional, communication logs) is processed, the Orchestrator dynamically formats and fans out all case evidence to the Graph Agent to build and check connection history in parallel.

### 2. Fusion Agent Aggregate Reasoning
- The Fusion Agent receives the Graph Agent output as a canonical `AgentResult` object.
- Network fraud rings detected by the Graph Agent (verdict = `fraud`) are counted as fraud flags. If a case features both social engineering (scam flag) and graph-correlated linkages (fraud flag), Fusion escalates the final verdict to `high_risk_fraud`.

---

## Limitations
- **In-Memory Volatility**: Since the NetworkX MultiDiGraph resides purely in the application's RAM, restarting the server clears the graph history. (Neo4j database persistence is scheduled for Phase 7).
- **Scale Limits**: Because the graph is evaluated in memory, analyzing millions of nodes can lead to elevated garbage collection and execution latency. Performance-critical sub-graph queries should transition to a dedicated graph DB as data grows.
