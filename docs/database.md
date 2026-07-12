# Database

## PostgreSQL — core tables

```sql
CREATE TABLE cases (
  case_id      TEXT PRIMARY KEY,
  input_type   TEXT NOT NULL,
  submitted_by TEXT,
  submitted_at TIMESTAMPTZ DEFAULT now(),
  status       TEXT DEFAULT 'processing'
);

CREATE TABLE agent_results (
  id           SERIAL PRIMARY KEY,
  case_id      TEXT REFERENCES cases(case_id),
  agent        TEXT NOT NULL,
  verdict      TEXT,
  confidence   NUMERIC,
  risk_score   INT,
  category     TEXT,
  explanation  TEXT,
  evidence     JSONB,
  processed_at TIMESTAMPTZ
);

CREATE TABLE fusion_reports (
  case_id            TEXT PRIMARY KEY REFERENCES cases(case_id),
  final_verdict      TEXT,
  overall_risk       INT,
  narrative          TEXT,
  recommended_action TEXT[],
  created_at         TIMESTAMPTZ DEFAULT now()
);
```

This lives at `backend/db/schema.sql` in the repo root — apply it with `psql -f backend/db/schema.sql`.

## Neo4j — graph model (Phase 7 only)

```
(:Person)-[:OWNS]->(:BankAccount)
(:Person)-[:USES]->(:Device)
(:BankAccount)-[:TRANSFERRED_TO]->(:BankAccount)
(:Person)-[:REPORTED]->(:Case)
```

## Fallback — NetworkX (no Neo4j install required)

If Neo4j setup consumes too much build time, model the same nodes/edges in-memory:

```python
import networkx as nx

G = nx.DiGraph()
G.add_edge("person:1", "account:1", rel="OWNS")
G.add_edge("account:1", "account:2", rel="TRANSFERRED_TO")
```

Render with `pyvis` or `matplotlib` for the demo. Have this ready *before* you need it — don't discover mid-build that Neo4j setup is eating your Day 4.

Graph relationships are intentionally excluded from PostgreSQL because graph intelligence belongs to the Graph Agent (Phase 7).