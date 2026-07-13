export const EvidenceType = {
  SMS: 'sms',
  URL: 'url',
  TRANSACTION: 'transaction',
  IMAGE: 'image',
} as const;

export type EvidenceTypeString = typeof EvidenceType[keyof typeof EvidenceType];

export interface EvidenceItem {
  input_type: string; // Typically from EvidenceType
  payload: Record<string, unknown>;
}

export interface InvestigateRequest {
  case_id: string;
  evidence: EvidenceItem[];
}

export interface AgentResult {
  agent: string;
  case_id: string;
  verdict: string;
  confidence: number;
  risk_score: number;
  category: string;
  evidence: Record<string, unknown>;
}

export interface AggregatedRiskResponse {
  agent: string;
  case_id: string;
  final_verdict: string;
  overall_risk: number;
  narrative: string;
  recommended_action: string[];
  evidence: Record<string, unknown>;
  processed_at: string;
}
