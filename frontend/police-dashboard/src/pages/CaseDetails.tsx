import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { mockCaseDetails } from '../data/mockCaseDetails';
import Badge from '../components/Badge';
import InvestigationSummaryCard from '../components/InvestigationSummaryCard';
import AgentResultCard from '../components/AgentResultCard';
import EvidencePanel from '../components/EvidencePanel';
import RecommendedActions from '../components/RecommendedActions';
import InvestigationTimeline from '../components/InvestigationTimeline';
import PlaceholderCard from '../components/PlaceholderCard';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorState from '../components/ErrorState';
import { investigationService, caseService } from '../services/api';
import GeoIntelligencePanel from '../components/GeoIntelligencePanel';
import type { AggregatedRiskResponse, BackendAgentEvidence, InvestigateRequest, GeoAgentEvidenceData } from '../types/api';
import type { AgentResult } from '../types/case';

export default function CaseDetails() {
  const { id } = useParams<{ id: string }>();
  const [fusionData, setFusionData] = useState<AggregatedRiskResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const details = mockCaseDetails[id || ''] ?? null;

  useEffect(() => {
    let isMounted = true;
    if (!id) return;

    // Attempt to load from PostgreSQL backend first
    caseService.getCaseById(id)
      .then((dbCase) => {
        if (!isMounted || !dbCase || !dbCase.fusion_report) return;
        setFusionData({
          agent: 'fusion_agent',
          case_id: dbCase.case_id,
          final_verdict: dbCase.fusion_report.final_verdict || 'safe',
          overall_risk: dbCase.fusion_report.overall_risk || 0,
          narrative: dbCase.fusion_report.explanation || '',
          recommended_action: dbCase.fusion_report.recommended_action || [],
          evidence: (dbCase.agent_results || []).reduce((acc: any, ar: any) => {
            acc[ar.agent_name] = {
              agent: ar.agent_name,
              case_id: dbCase.case_id,
              verdict: ar.verdict,
              confidence: ar.confidence,
              risk_score: ar.risk_score,
              category: ar.explanation,
              evidence: ar.raw_output,
            };
            return acc;
          }, {}),
          processed_at: dbCase.fusion_report.created_at || new Date().toISOString(),
        });
      })
      .catch(() => {
        // Mock fallback if case not found in DB
      });

    return () => {
      isMounted = false;
    };
  }, [id]);

  useEffect(() => {
    // Resolve details inside the effect using the stable id string.
    // Using [details] as dependency causes re-runs on every render because
    // the merged displayDetails object has a new reference each render cycle.
    const caseDetails = mockCaseDetails[id || ''] ?? null;
    if (!caseDetails) return;

    let isMounted = true;
    
    const fetchLiveAnalysis = async () => {
      setIsLoading(true);
      setFusionData(null);
      setError(null);
      try {
        const request: InvestigateRequest = {
          case_id: caseDetails.case_id,
          evidence: caseDetails.evidence
            .filter(e => e.type === 'SMS' || e.type === 'URL' || e.type === 'Location')
            .map(e => {
              if (e.type === 'SMS') return { input_type: 'sms', payload: { text: e.preview } };
              if (e.type === 'URL') return { input_type: 'url', payload: { url: e.preview } };
              if (e.type === 'Location') {
                try {
                  return { input_type: 'location', payload: JSON.parse(e.preview) };
                } catch {
                  return { input_type: 'location', payload: { latitude: 12.9716, longitude: 77.5946, radius_km: 5.0 } };
                }
              }
              return { input_type: e.type.toLowerCase(), payload: { text: e.preview } };
            })
        };
        const result = await investigationService.submitInvestigation(request);
        if (isMounted) {
          setFusionData(result);
        }
      } catch (err) {
        if (isMounted) {
          setError(err instanceof Error ? err.message : 'Unknown error occurred.');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    fetchLiveAnalysis();

    return () => {
      isMounted = false;
    };
  }, [id]);  // Stable string primitive — only re-run when navigating to a different case

  if (!details) {
    return (
      <div className="space-y-6">
        <div className="mb-2">
          <Link to="/cases" className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 rounded-sm">
            <ArrowLeft className="mr-1.5 h-4 w-4" aria-hidden="true" /> Back to Cases
          </Link>
        </div>
        <PlaceholderCard title="Case Not Found" description="The requested case details could not be loaded." />
      </div>
    );
  }

  const displayDetails = { ...details };
  if (fusionData) {
    displayDetails.fusion_verdict = fusionData.final_verdict;
    displayDetails.overall_risk_score = fusionData.overall_risk;
    displayDetails.investigation_summary = fusionData.narrative;
    displayDetails.recommended_actions = fusionData.recommended_action;

    // Map backend 'evidence' dictionary to agent_results.
    // BackendAgentEvidence matches backend/fusion_agent/schemas.py AgentResult exactly.
    const backendAgents = Object.values(fusionData.evidence) as BackendAgentEvidence[];
    if (backendAgents.length > 0) {
      displayDetails.agent_results = backendAgents.map((ar: BackendAgentEvidence) => ({
        agent_name: ar.agent || 'Unknown Agent',
        verdict: ar.verdict ? (ar.verdict.charAt(0).toUpperCase() + ar.verdict.slice(1)) as AgentResult['verdict'] : 'Unknown' as AgentResult['verdict'],
        risk_score: ar.risk_score || 0,
        confidence: ar.confidence ? Math.round(ar.confidence * 100) : 0,
        explanation: ar.category ? `Category: ${ar.category}` : 'No explanation provided.'
      }));

      // Derive overall confidence by averaging raw agent confidence floats
      const confidences = backendAgents.map((ar: BackendAgentEvidence) => ar.confidence || 0);
      displayDetails.confidence_score = Math.round((confidences.reduce((a, b) => a + b, 0) / confidences.length) * 100);
    } else {
      displayDetails.agent_results = [];
      displayDetails.confidence_score = 0;
    }
  }

  // Extract Geo Agent data if available from backend live analysis or fallback
  const geoAgentOutput = fusionData?.evidence?.geo_agent;
  let geoData: GeoAgentEvidenceData | null = null;
  let geoVerdict = 'safe';
  let geoRiskScore = 0;

  if (geoAgentOutput) {
    geoData = (geoAgentOutput.evidence as unknown) as GeoAgentEvidenceData;
    geoVerdict = geoAgentOutput.verdict || 'safe';
    geoRiskScore = geoAgentOutput.risk_score || 0;
  } else {
    const locItem = displayDetails.evidence.find(e => e.type === 'Location');
    if (locItem) {
      try {
        const parsed = JSON.parse(locItem.preview);
        const lat = parsed.latitude || 12.9716;
        const lon = parsed.longitude || 77.5946;
        const radius = parsed.radius_km || 5.0;
        geoVerdict = 'fraud';
        geoRiskScore = 90;
        geoData = {
          input_coords: [lat, lon],
          valid_coords: true,
          district: parsed.district || 'Bengaluru Urban',
          state: parsed.state || 'Karnataka',
          nearby_incidents_count: 4,
          nearby_incidents: [
            { id: 'inc-blr-001', latitude: lat, longitude: lon, district: parsed.district || 'Bengaluru Urban', state: parsed.state || 'Karnataka', category: 'crypto_fraud', timestamp: '2026-07-01T10:00:00Z', distance_km: 0.0 },
            { id: 'inc-blr-002', latitude: lat + 0.006, longitude: lon - 0.003, district: parsed.district || 'Bengaluru Urban', state: parsed.state || 'Karnataka', category: 'phishing', timestamp: '2026-07-02T14:30:00Z', distance_km: 0.75 },
            { id: 'inc-blr-003', latitude: lat - 0.007, longitude: lon + 0.006, district: parsed.district || 'Bengaluru Urban', state: parsed.state || 'Karnataka', category: 'crypto_fraud', timestamp: '2026-07-05T18:15:00Z', distance_km: 1.1 },
            { id: 'inc-blr-004', latitude: lat + 0.01, longitude: lon + 0.013, district: parsed.district || 'Bengaluru Urban', state: parsed.state || 'Karnataka', category: 'theft', timestamp: '2026-07-10T12:00:00Z', distance_km: 1.85 }
          ],
          district_aggregation: { 'Bengaluru Urban': 4, 'Central Delhi': 3, 'Mumbai City': 2 },
          state_aggregation: { 'Karnataka': 4, 'Delhi': 3, 'Maharashtra': 2 },
          relative_crime_density: 0.0509,
          hotspots: [
            { center_latitude: lat, center_longitude: lon, incident_count: 4, radius_km: radius, risk_level: 'high' }
          ],
          clusters: [
            { cluster_id: 1, center_latitude: lat + 0.002, center_longitude: lon + 0.002, node_count: 4, incidents: ['inc-blr-001', 'inc-blr-002', 'inc-blr-003', 'inc-blr-004'], typical_category: 'crypto_fraud' }
          ],
          patrol_recommendations: {
            priority: 'high',
            patrol_frequency: 'hourly',
            suggested_hubs: ['crypto_fraud', 'phishing'],
            narrative: 'High density crime hotspot detected near target coordinates. Immediate hourly patrols recommended focusing on crypto fraud and phishing hubs.'
          }
        };
      } catch {
        // Handle JSON parse error
      }
    }
  }

  return (
    <div className="space-y-8 pb-10">
      {/* 1. Header Section */}
      <div>
        <div className="mb-4">
          <Link 
            to="/cases" 
            className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 rounded-sm"
          >
            <ArrowLeft className="mr-1.5 h-4 w-4" aria-hidden="true" /> Back to Cases
          </Link>
        </div>
        <div className="bg-white shadow-sm ring-1 ring-black ring-opacity-5 rounded-lg p-6">
          <div className="flex flex-col md:flex-row md:items-start justify-between gap-6">
            <div className="flex-1 min-w-0">
              <div className="flex flex-wrap items-center gap-3 mb-2">
                <h2 className="text-2xl font-bold leading-7 text-gray-900 break-words">
                  {displayDetails.title}
                </h2>
                <span className="text-sm font-mono text-gray-500 bg-gray-100 px-2 py-0.5 rounded border border-gray-200 flex-shrink-0">
                  {displayDetails.case_id}
                </span>
              </div>
              <p className="text-sm text-gray-500 break-words">
                Victim: <span className="font-medium text-gray-900">{displayDetails.victim_name}</span> &bull; Assigned to: <span className="font-medium text-gray-900">{displayDetails.assigned_officer}</span>
              </p>
            </div>
            <div className="flex flex-col items-start md:items-end gap-2 shrink-0">
              <div className="flex flex-wrap items-center gap-2">
                <Badge type="status" value={displayDetails.status} />
                <Badge type="risk" value={displayDetails.risk_level} />
              </div>
              <div className="text-xs text-gray-500 mt-1 flex flex-col md:items-end">
                <div>Created: {new Date(displayDetails.created_at).toLocaleString()}</div>
                <div>Updated: {new Date(displayDetails.updated_at).toLocaleString()}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {isLoading && (
        <div className="flex justify-center p-12 bg-white rounded-lg shadow-sm border border-gray-200">
          <LoadingSpinner message="Running live multi-agent analysis..." />
        </div>
      )}

      {error && !isLoading && (
        <ErrorState message={error} onRetry={() => window.location.reload()} />
      )}

      {!isLoading && !error && (
        <>
          {/* 2. Investigation Summary */}
          <InvestigationSummaryCard details={displayDetails} />

          {/* 3. Agent Results */}
          <div>
            <h3 className="text-lg font-semibold leading-6 text-gray-900 mb-4">Agent Results</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {displayDetails.agent_results.map((result, idx) => (
                <AgentResultCard key={idx} result={result} />
              ))}
            </div>
          </div>

          {/* 4. Geo Intelligence Section */}
          <GeoIntelligencePanel
            geoData={geoData}
            agentVerdict={geoVerdict}
            agentRiskScore={geoRiskScore}
            isLoading={isLoading}
          />
        </>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          {/* 4. Evidence Panel */}
          <EvidencePanel evidence={displayDetails.evidence} />
          
          {/* 5. Recommended Actions */}
          <RecommendedActions actions={displayDetails.recommended_actions} />
        </div>

        <div className="lg:col-span-1">
          {/* 6. Investigation Timeline */}
          <InvestigationTimeline timeline={displayDetails.timeline} />
        </div>
      </div>
    </div>
  );
}
