// Matches the backend EvidencePayload Pydantic schema (backend/orchestrator/schemas.py)
export interface EvidencePayload {
  input_type: string;
  payload: Record<string, unknown>;
}

// Matches the backend InvestigateRequest Pydantic schema
export interface InvestigateRequest {
  case_id?: string;
  evidence: EvidencePayload[];
}

/**
 * Matches a single agent entry inside AggregatedRiskResponse.evidence dict.
 * Each key is the AgentType string (e.g. "scam_comm_agent_sms").
 * Mirrors backend/fusion_agent/schemas.py AgentResult.
 */
export interface BackendAgentEvidence {
  agent: string;
  case_id: string;
  verdict: string;
  confidence: number;  // raw float in [0, 1]
  risk_score: number;
  category: string;
  evidence: Record<string, unknown>;
}

/**
 * Matches the backend AggregatedRiskResponse Pydantic schema exactly.
 * Source of truth: backend/fusion_agent/schemas.py
 *
 * NOTE: confidence_score and agent_results do NOT exist on the backend response.
 *       The frontend derives them from the 'evidence' dictionary.
 */
export interface AggregatedRiskResponse {
  agent: string;
  case_id: string;
  final_verdict: string;           // backend field — NOT fusion_verdict
  overall_risk: number;            // backend field — NOT overall_risk_score
  narrative: string;               // backend field — NOT investigation_summary
  recommended_action: string[];    // backend field — NOT agent_results array
  evidence: Record<string, BackendAgentEvidence>; // typed agent outputs
  processed_at: string;
}
