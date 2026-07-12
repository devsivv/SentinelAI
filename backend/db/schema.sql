-- backend/db/schema.sql — see docs/database.md for the documented version
CREATE TABLE IF NOT EXISTS cases (
  case_id      TEXT PRIMARY KEY,
  input_type   TEXT NOT NULL,
  submitted_by TEXT,
  submitted_at TIMESTAMPTZ DEFAULT now(),
  status       TEXT DEFAULT 'processing'
);

CREATE TABLE IF NOT EXISTS agent_results (
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

CREATE TABLE IF NOT EXISTS fusion_reports (
  case_id            TEXT PRIMARY KEY REFERENCES cases(case_id),
  final_verdict      TEXT,
  overall_risk       INT,
  narrative          TEXT,
  recommended_action TEXT[],
  created_at         TIMESTAMPTZ DEFAULT now()
);
