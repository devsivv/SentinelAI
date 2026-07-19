export type CaseStatus = 'Open' | 'Under Review' | 'Closed';
export type RiskLevel = 'Low' | 'Medium' | 'High' | 'Critical';

export interface InvestigationCase {
  case_id: string;
  title: string;
  victim_name: string;
  created_at: string; // ISO format
  risk_level: RiskLevel;
  status: CaseStatus;
  assigned_officer: string;
}

export interface AgentResult {
  agent_name: string;
  verdict: RiskLevel | 'Clean' | 'Suspicious' | 'Fraudulent';
  risk_score: number;
  confidence: number;
  explanation: string;
}

export interface EvidenceItem {
  id: string;
  type: 'SMS' | 'URL' | 'Transaction' | 'Image';
  preview: string;
  status: 'Analyzed' | 'Pending' | 'Flagged';
}

export interface TimelineEvent {
  id: string;
  event: string;
  timestamp: string;
  actor: string;
}

export interface CaseDetailsData extends InvestigationCase {
  updated_at: string;
  fusion_verdict: string;
  overall_risk_score: number;
  confidence_score: number;
  investigation_summary: string;
  agent_results: AgentResult[];
  evidence: EvidenceItem[];
  recommended_actions: string[];
  timeline: TimelineEvent[];
}
