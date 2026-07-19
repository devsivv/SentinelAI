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

export interface GeoIncident {
  id: string;
  latitude: number;
  longitude: number;
  district: string;
  state: string;
  category: string;
  timestamp: string;
  distance_km?: number;
}

export interface GeoHotspot {
  center_latitude: number;
  center_longitude: number;
  incident_count: number;
  radius_km: number;
  risk_level: string; // 'low' | 'medium' | 'high'
}

export interface GeoCluster {
  cluster_id: number;
  center_latitude: number;
  center_longitude: number;
  node_count: number;
  incidents: string[];
  typical_category: string;
}

export interface GeoPatrolRecommendation {
  priority: 'low' | 'medium' | 'high' | string;
  patrol_frequency: 'none' | 'weekly' | 'daily' | 'hourly' | string;
  suggested_hubs: string[];
  narrative: string;
}

export interface GeoAgentEvidenceData {
  input_coords: [number, number];
  valid_coords: boolean;
  district: string;
  state: string;
  nearby_incidents_count: number;
  nearby_incidents: GeoIncident[];
  district_aggregation: Record<string, number>;
  state_aggregation: Record<string, number>;
  relative_crime_density: number;
  hotspots: GeoHotspot[];
  clusters: GeoCluster[];
  patrol_recommendations: GeoPatrolRecommendation;
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
