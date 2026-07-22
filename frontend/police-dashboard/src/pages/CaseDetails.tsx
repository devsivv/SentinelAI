import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, RefreshCw } from 'lucide-react';
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
import type { AgentResult, CaseStatus, CaseDetailsData } from '../types/case';

const formatAgentName = (rawName: string) => {
  switch (rawName) {
    case 'scam_comm_agent_sms':
    case 'scam_sms':
      return 'SMS Scam Agent';
    case 'scam_comm_agent_url':
    case 'scam_url':
      return 'Phishing URL Agent';
    case 'fraud_agent':
    case 'fraud':
      return 'Transaction Fraud Agent';
    case 'currency_agent':
    case 'currency':
      return 'Currency Agent';
    case 'graph_agent':
    case 'graph':
      return 'Graph Intelligence Agent';
    case 'geo_agent':
    case 'geo':
      return 'Geo Intelligence Agent';
    default:
      return rawName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  }
};

export default function CaseDetails() {
  const { id } = useParams<{ id: string }>();
  const [dbCaseData, setDbCaseData] = useState<any | null>(null);
  const [fusionData, setFusionData] = useState<AggregatedRiskResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    if (!id) {
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    setError(null);

    // Single source of truth: Load case details from backend PostgreSQL database
    caseService.getCaseById(id)
      .then((dbCase) => {
        if (!isMounted) return;
        setDbCaseData(dbCase);
        if (dbCase?.fusion_report) {
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
        }
      })
      .catch((err) => {
        if (!isMounted) return;
        // Fallback to mock dataset if case is not yet created in live DB
        const fallbackMock = mockCaseDetails[id];
        if (!fallbackMock) {
          setError(err instanceof Error ? err.message : 'Failed to load case details.');
        }
      })
      .finally(() => {
        if (isMounted) {
          setIsLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [id]);

  const baseMock = mockCaseDetails[id || ''] ?? null;
  const hasCase = dbCaseData || baseMock;

  if (!isLoading && !hasCase && !error) {
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

  // Construct display details prioritized by live DB case over mock fallback
  const displayDetails: CaseDetailsData = {
    case_id: dbCaseData?.case_id || baseMock?.case_id || id || 'CAS-UNKNOWN',
    title: dbCaseData?.metadata_json?.title || baseMock?.title || `${(dbCaseData?.investigation_type || 'Investigation').toUpperCase()} (${(id || '').slice(0, 8)})`,
    victim_name: dbCaseData?.metadata_json?.victim_name || baseMock?.victim_name || 'Reported Victim',
    assigned_officer: dbCaseData?.metadata_json?.assigned_officer || baseMock?.assigned_officer || 'Unassigned',
    created_at: dbCaseData?.created_at || baseMock?.created_at || new Date().toISOString(),
    updated_at: dbCaseData?.updated_at || baseMock?.updated_at || new Date().toISOString(),
    status: (dbCaseData?.status?.toLowerCase() === 'processing' ? 'Under Review' : dbCaseData?.status?.toLowerCase() === 'completed' ? 'Closed' : baseMock?.status || 'Open') as CaseStatus,
    risk_level: baseMock?.risk_level || 'Medium',
    fusion_verdict: baseMock?.fusion_verdict || 'Pending Analysis',
    overall_risk_score: baseMock?.overall_risk_score || 0,
    confidence_score: baseMock?.confidence_score || 0,
    investigation_summary: baseMock?.investigation_summary || 'No summary available.',
    agent_results: baseMock?.agent_results || [],
    evidence: dbCaseData?.metadata_json?.evidence || baseMock?.evidence || [],
    recommended_actions: baseMock?.recommended_actions || [],
    timeline: dbCaseData?.metadata_json?.timeline || baseMock?.timeline || []
  };

  const fusionReport = fusionData || (dbCaseData?.fusion_report ? {
    agent: 'fusion_agent',
    case_id: dbCaseData.case_id,
    final_verdict: dbCaseData.fusion_report.final_verdict || 'safe',
    overall_risk: dbCaseData.fusion_report.overall_risk || 0,
    narrative: dbCaseData.fusion_report.explanation || '',
    recommended_action: dbCaseData.fusion_report.recommended_action || [],
    evidence: (dbCaseData.agent_results || []).reduce((acc: any, ar: any) => {
      acc[ar.agent_name] = {
        agent: ar.agent_name,
        case_id: dbCaseData.case_id,
        verdict: ar.verdict,
        confidence: ar.confidence,
        risk_score: ar.risk_score,
        category: ar.explanation,
        evidence: ar.raw_output,
      };
      return acc;
    }, {}),
    processed_at: dbCaseData.fusion_report.created_at || new Date().toISOString(),
  } : null);

  if (fusionReport) {
    displayDetails.fusion_verdict = fusionReport.final_verdict;
    displayDetails.overall_risk_score = fusionReport.overall_risk;
    displayDetails.investigation_summary = fusionReport.narrative;
    displayDetails.recommended_actions = fusionReport.recommended_action || [];

    const backendAgents = Object.values(fusionReport.evidence || {}) as BackendAgentEvidence[];
    if (backendAgents.length > 0) {
      displayDetails.agent_results = backendAgents.map((ar: BackendAgentEvidence) => ({
        agent_name: formatAgentName(ar.agent || 'Unknown Agent'),
        verdict: ar.verdict ? (ar.verdict.charAt(0).toUpperCase() + ar.verdict.slice(1)) as AgentResult['verdict'] : 'Clean' as AgentResult['verdict'],
        risk_score: ar.risk_score || 0,
        confidence: ar.confidence ? Math.round(ar.confidence <= 1 ? ar.confidence * 100 : ar.confidence) : 0,
        explanation: ar.category ? `Category: ${ar.category}` : 'No explanation provided.'
      }));

      const confidences = backendAgents.map((ar: BackendAgentEvidence) => (ar.confidence || 0) <= 1 ? (ar.confidence || 0) * 100 : (ar.confidence || 0));
      displayDetails.confidence_score = Math.round(confidences.reduce((a, b) => a + b, 0) / confidences.length);
    }

    displayDetails.risk_level = displayDetails.overall_risk_score >= 75 ? 'Critical' : displayDetails.overall_risk_score >= 50 ? 'High' : displayDetails.overall_risk_score >= 25 ? 'Medium' : 'Low';
  }

  const handleRunReanalysis = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const reqEvidence = displayDetails.evidence
        .filter(e => e.type === 'SMS' || e.type === 'URL' || e.type === 'Transaction')
        .map(e => {
          if (e.type === 'SMS') {
            return { input_type: 'sms', payload: { text: e.preview } };
          }
          if (e.type === 'URL') {
            return { input_type: 'url', payload: { url: e.preview } };
          }
          if (e.type === 'Transaction') {
            let parsed: any = {};
            try {
              parsed = JSON.parse(e.preview);
            } catch {
              parsed = {};
            }
            return {
              input_type: 'transaction',
              payload: {
                step: parsed.step ?? 1,
                type: parsed.type ?? 'TRANSFER',
                amount: parsed.amount ?? 50000.0,
                oldbalanceOrg: parsed.oldbalanceOrg ?? 50000.0,
                newbalanceOrig: parsed.newbalanceOrig ?? 0.0,
                oldbalanceDest: parsed.oldbalanceDest ?? 0.0,
                newbalanceDest: parsed.newbalanceDest ?? 50000.0,
                isFlaggedFraud: parsed.isFlaggedFraud ?? 0
              }
            };
          }
          return { input_type: e.type.toLowerCase(), payload: { text: e.preview } };
        });

      const request: InvestigateRequest = {
        case_id: displayDetails.case_id,
        evidence: reqEvidence
      };
      const result = await investigationService.submitInvestigation(request);
      setFusionData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Re-analysis failed.');
    } finally {
      setIsLoading(false);
    }
  };

  const geoAgentOutput = fusionReport?.evidence?.geo_agent;
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
                <button
                  onClick={handleRunReanalysis}
                  disabled={isLoading}
                  className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 transition-colors cursor-pointer mr-2"
                  title="Re-run multi-agent investigation on live backend"
                >
                  <RefreshCw className={`mr-1.5 h-3.5 w-3.5 text-gray-500 ${isLoading ? 'animate-spin' : ''}`} />
                  {isLoading ? 'Analyzing...' : 'Run Live Analysis'}
                </button>
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
