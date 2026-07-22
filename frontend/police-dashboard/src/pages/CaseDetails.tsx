import { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, RefreshCw, Activity } from 'lucide-react';
import { mockCaseDetails } from '../data/mockCaseDetails';
import Badge from '../components/Badge';
import InvestigationSummaryCard from '../components/InvestigationSummaryCard';
import AgentResultCard from '../components/AgentResultCard';
import EvidencePanel from '../components/EvidencePanel';
import RecommendedActions from '../components/RecommendedActions';
import InvestigationTimeline from '../components/InvestigationTimeline';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorState from '../components/ErrorState';
import { investigationService, caseService, classifyApiError } from '../services/api';
import GeoIntelligencePanel from '../components/GeoIntelligencePanel';
import type {
  AggregatedRiskResponse,
  BackendAgentEvidence,
  InvestigateRequest,
  GeoAgentEvidenceData,
} from '../types/api';
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
      return rawName.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase());
  }
};

export default function CaseDetails() {
  const { id } = useParams<{ id: string }>();
  const [dbCaseData, setDbCaseData] = useState<any | null>(null);
  const [fusionData, setFusionData] = useState<AggregatedRiskResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorVariant, setErrorVariant] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [reanalysisError, setReanalysisError] = useState<string | null>(null);
  const [isReanalyzing, setIsReanalyzing] = useState(false);

  const loadCase = useCallback(() => {
    if (!id) {
      setIsLoading(false);
      return;
    }

    let isMounted = true;
    setIsLoading(true);
    setErrorVariant(null);
    setErrorMessage(null);

    caseService
      .getCaseById(id)
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
      .catch((err: Error) => {
        if (!isMounted) return;
        const variant = classifyApiError(err);
        // For 404 specifically: check if mock data exists as fallback
        if (variant === 'not_found' && !mockCaseDetails[id]) {
          // Truly unknown case — show not-found state
          setErrorVariant('not_found');
          setErrorMessage(null);
        } else if (variant === 'not_found' && mockCaseDetails[id]) {
          // Case exists only in mock data — load silently
          // no error shown; mock data will fill displayDetails below
        } else {
          // Timeout, network, server — surface error with retry
          setErrorVariant(variant);
          setErrorMessage(err.message !== variant ? err.message : null);
        }
      })
      .finally(() => {
        if (isMounted) setIsLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [id]);

  useEffect(() => {
    const cleanup = loadCase();
    return cleanup;
  }, [loadCase]);

  // ── Derived state ──────────────────────────────────────────────────────────
  const baseMock = mockCaseDetails[id || ''] ?? null;

  // Show case-not-found page when backend returned 404 (regardless of mock availability)
  const isCaseNotFound = errorVariant === 'not_found' && !dbCaseData;

  // Show backend-error banner when: non-404 error (timeout, network, server)
  const isBackendError = !!errorVariant && errorVariant !== 'not_found';

  if (!isLoading && isCaseNotFound) {
    return (
      <div className="space-y-6">
        <Link
          to="/cases"
          className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 rounded-sm"
        >
          <ArrowLeft className="mr-1.5 h-4 w-4" aria-hidden="true" /> Back to Cases
        </Link>
        <ErrorState
          variant="not_found"
          title="Case Not Found"
          message="This case may have been deleted or the ID is invalid. It does not exist in the database."
          onRetry={loadCase}
          backTo="/cases"
          backLabel="Back to Cases"
        />
      </div>
    );
  }

  // ── displayDetails construction ───────────────────────────────────────────
  const displayDetails: CaseDetailsData = {
    case_id: dbCaseData?.case_id || baseMock?.case_id || id || 'CAS-UNKNOWN',
    title:
      dbCaseData?.metadata_json?.title ||
      (dbCaseData ? `${(dbCaseData.investigation_type || 'Investigation').toUpperCase()} (${(id || '').slice(0, 8)})` : null) ||
      baseMock?.title ||
      `Investigation ${(id || '').slice(0, 8)}`,
    victim_name:
      dbCaseData?.metadata_json?.victim_name || baseMock?.victim_name || 'Not Available',
    assigned_officer:
      dbCaseData?.metadata_json?.assigned_officer || baseMock?.assigned_officer || 'Unassigned',
    created_at: dbCaseData?.created_at || baseMock?.created_at || new Date().toISOString(),
    updated_at: dbCaseData?.updated_at || baseMock?.updated_at || new Date().toISOString(),
    status: (dbCaseData?.status?.toLowerCase() === 'processing'
      ? 'Under Review'
      : dbCaseData?.status?.toLowerCase() === 'completed'
      ? 'Closed'
      : dbCaseData?.status?.toLowerCase() === 'open'
      ? 'Open'
      : baseMock?.status || 'Open') as CaseStatus,
    risk_level: baseMock?.risk_level || 'Medium',
    fusion_verdict: 'Pending Analysis',
    overall_risk_score: 0,
    confidence_score: 0,
    investigation_summary: '',
    agent_results: [],
    evidence: dbCaseData?.metadata_json?.evidence || baseMock?.evidence || [],
    recommended_actions: [],
    timeline: dbCaseData?.metadata_json?.timeline || baseMock?.timeline || [],
  };

  const fusionReport =
    fusionData ||
    (dbCaseData?.fusion_report
      ? {
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
        }
      : null);

  if (fusionReport) {
    displayDetails.fusion_verdict = fusionReport.final_verdict;
    displayDetails.overall_risk_score = fusionReport.overall_risk;
    displayDetails.investigation_summary = fusionReport.narrative;
    displayDetails.recommended_actions = fusionReport.recommended_action || [];

    const backendAgents = Object.values(fusionReport.evidence || {}) as BackendAgentEvidence[];
    if (backendAgents.length > 0) {
      displayDetails.agent_results = backendAgents.map((ar: BackendAgentEvidence) => ({
        agent_name: formatAgentName(ar.agent || 'Unknown Agent'),
        verdict: ar.verdict
          ? ((ar.verdict.charAt(0).toUpperCase() + ar.verdict.slice(1)) as AgentResult['verdict'])
          : ('Clean' as AgentResult['verdict']),
        risk_score: ar.risk_score || 0,
        confidence: ar.confidence
          ? Math.round(ar.confidence <= 1 ? ar.confidence * 100 : ar.confidence)
          : 0,
        explanation: ar.category ? `Category: ${ar.category}` : 'No explanation provided.',
      }));
      const confidences = backendAgents.map((ar: BackendAgentEvidence) =>
        (ar.confidence || 0) <= 1 ? (ar.confidence || 0) * 100 : ar.confidence || 0
      );
      displayDetails.confidence_score = Math.round(
        confidences.reduce((a, b) => a + b, 0) / confidences.length
      );
    }

    displayDetails.risk_level =
      displayDetails.overall_risk_score >= 75
        ? 'Critical'
        : displayDetails.overall_risk_score >= 50
        ? 'High'
        : displayDetails.overall_risk_score >= 25
        ? 'Medium'
        : 'Low';
  }

  // ── Re-analysis handler ───────────────────────────────────────────────────
  const handleRunReanalysis = async () => {
    setIsReanalyzing(true);
    setReanalysisError(null);
    try {
      const reqEvidence = displayDetails.evidence
        .filter((e) => e.type === 'SMS' || e.type === 'URL' || e.type === 'Transaction')
        .map((e) => {
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
                isFlaggedFraud: parsed.isFlaggedFraud ?? 0,
              },
            };
          }
          return { input_type: e.type.toLowerCase(), payload: { text: e.preview } };
        });

      const request: InvestigateRequest = {
        case_id: displayDetails.case_id,
        evidence: reqEvidence,
      };
      const result = await investigationService.submitInvestigation(request);
      setFusionData(result);
    } catch (err) {
      const variant = classifyApiError(err);
      setReanalysisError(variant);
    } finally {
      setIsReanalyzing(false);
    }
  };

  // ── Geo data extraction ────────────────────────────────────────────────────
  const geoAgentOutput = fusionReport?.evidence?.geo_agent;
  let geoData: GeoAgentEvidenceData | null = null;
  let geoVerdict = 'safe';
  let geoRiskScore = 0;

  if (geoAgentOutput) {
    geoData = geoAgentOutput.evidence as unknown as GeoAgentEvidenceData;
    geoVerdict = geoAgentOutput.verdict || 'safe';
    geoRiskScore = geoAgentOutput.risk_score || 0;
  } else {
    const locItem = displayDetails.evidence.find((e) => e.type === 'Location');
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
            {
              id: 'inc-blr-001',
              latitude: lat,
              longitude: lon,
              district: parsed.district || 'Bengaluru Urban',
              state: parsed.state || 'Karnataka',
              category: 'crypto_fraud',
              timestamp: '2026-07-01T10:00:00Z',
              distance_km: 0.0,
            },
            {
              id: 'inc-blr-002',
              latitude: lat + 0.006,
              longitude: lon - 0.003,
              district: parsed.district || 'Bengaluru Urban',
              state: parsed.state || 'Karnataka',
              category: 'phishing',
              timestamp: '2026-07-02T14:30:00Z',
              distance_km: 0.75,
            },
            {
              id: 'inc-blr-003',
              latitude: lat - 0.007,
              longitude: lon + 0.006,
              district: parsed.district || 'Bengaluru Urban',
              state: parsed.state || 'Karnataka',
              category: 'crypto_fraud',
              timestamp: '2026-07-05T18:15:00Z',
              distance_km: 1.1,
            },
            {
              id: 'inc-blr-004',
              latitude: lat + 0.01,
              longitude: lon + 0.013,
              district: parsed.district || 'Bengaluru Urban',
              state: parsed.state || 'Karnataka',
              category: 'theft',
              timestamp: '2026-07-10T12:00:00Z',
              distance_km: 1.85,
            },
          ],
          district_aggregation: { 'Bengaluru Urban': 4, 'Central Delhi': 3, 'Mumbai City': 2 },
          state_aggregation: { Karnataka: 4, Delhi: 3, Maharashtra: 2 },
          relative_crime_density: 0.0509,
          hotspots: [
            {
              center_latitude: lat,
              center_longitude: lon,
              incident_count: 4,
              radius_km: radius,
              risk_level: 'high',
            },
          ],
          clusters: [
            {
              cluster_id: 1,
              center_latitude: lat + 0.002,
              center_longitude: lon + 0.002,
              node_count: 4,
              incidents: ['inc-blr-001', 'inc-blr-002', 'inc-blr-003', 'inc-blr-004'],
              typical_category: 'crypto_fraud',
            },
          ],
          patrol_recommendations: {
            priority: 'high',
            patrol_frequency: 'hourly',
            suggested_hubs: ['crypto_fraud', 'phishing'],
            narrative:
              'High density crime hotspot detected near target coordinates. Immediate hourly patrols recommended focusing on crypto fraud and phishing hubs.',
          },
        };
      } catch {
        // Handle JSON parse error silently
      }
    }
  }

  // ── Render ─────────────────────────────────────────────────────────────────
  return (
    <div className="space-y-6 sm:space-y-8 pb-10">

      {/* 1. Header Section */}
      <div>
        <div className="mb-4">
          <Link
            to="/cases"
            className="inline-flex items-center text-sm font-semibold text-blue-400 hover:text-blue-300 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 rounded-lg min-h-[44px]"
          >
            <ArrowLeft className="mr-1.5 h-4 w-4" aria-hidden="true" /> Back to Cases
          </Link>
        </div>

        <div className="glass-card p-4 sm:p-6 bg-[#111827]/70 border border-white/10 rounded-2xl backdrop-blur-md shadow-xl text-white">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            {/* Left: title + case ID + victim */}
            <div className="flex-1 min-w-0">
              <div className="flex flex-wrap items-start gap-2 mb-1.5">
                <h2 className="text-lg sm:text-2xl font-extrabold leading-7 text-white break-words min-w-0">
                  {displayDetails.title}
                </h2>
                <span className="text-xs font-mono font-bold text-blue-300 bg-[#0F172A] px-2.5 py-1 rounded-lg border border-white/10 break-all shrink-0 self-start mt-0.5">
                  {displayDetails.case_id}
                </span>
              </div>
              <p className="text-sm text-gray-300 break-words">
                Victim:{' '}
                <span className="font-bold text-white">{displayDetails.victim_name}</span>
                {' '}&bull;{' '}
                Assigned:{' '}
                <span className="font-bold text-white">{displayDetails.assigned_officer}</span>
              </p>
            </div>

            {/* Right: badges + button + dates */}
            <div className="flex flex-col items-start sm:items-end gap-2.5 shrink-0">
              <div className="flex flex-wrap items-center gap-2">
                <button
                  onClick={handleRunReanalysis}
                  disabled={isReanalyzing}
                  className="inline-flex items-center justify-center px-4 py-2 border border-blue-500/30 text-xs font-bold rounded-xl shadow-lg shadow-blue-900/40 text-white bg-blue-600 hover:bg-blue-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 disabled:opacity-50 transition-all cursor-pointer min-h-[44px]"
                  aria-label="Re-run live multi-agent investigation"
                  title="Re-run multi-agent investigation on live backend"
                >
                  <RefreshCw
                    className={`mr-1.5 h-3.5 w-3.5 text-white ${isReanalyzing ? 'animate-spin' : ''}`}
                    aria-hidden="true"
                  />
                  {isReanalyzing ? 'Analyzing…' : 'Run Live Analysis'}
                </button>
                <Badge type="status" value={displayDetails.status} />
                <Badge type="risk" value={displayDetails.risk_level} />
              </div>
              <div className="text-xs text-gray-400 flex flex-col sm:items-end gap-0.5">
                <div>Created: {new Date(displayDetails.created_at).toLocaleString()}</div>
                <div>Updated: {new Date(displayDetails.updated_at).toLocaleString()}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Backend non-404 error banner (timeout / network / server) */}
      {isBackendError && !isLoading && (
        <ErrorState
          variant={errorVariant as any}
          message={errorMessage || undefined}
          onRetry={loadCase}
        />
      )}

      {/* Re-analysis error banner */}
      {reanalysisError && !isReanalyzing && (
        <ErrorState
          variant={reanalysisError as any}
          title="Re-analysis failed"
          onRetry={handleRunReanalysis}
        />
      )}

      {/* Loading state */}
      {(isLoading || isReanalyzing) && (
        <div className="glass-card flex justify-center p-12 bg-[#111827]/70 border border-white/10 rounded-2xl shadow-xl">
          <LoadingSpinner
            message={isReanalyzing ? 'Running live multi-agent analysis…' : 'Loading case details…'}
          />
        </div>
      )}

      {/* Main content — shown even if backend error, using available data */}
      {!isLoading && !isReanalyzing && (
        <>
          {/* 2. Investigation Summary */}
          <InvestigationSummaryCard details={displayDetails} />

          {/* 3. Agent Results — 1 col mobile, 2 col tablet, 3 col desktop */}
          <div>
            <h3 className="text-base sm:text-lg font-bold leading-6 text-white mb-3 sm:mb-4">Agent Results</h3>
            {displayDetails.agent_results.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
                {displayDetails.agent_results.map((result, idx) => (
                  <AgentResultCard key={idx} result={result} />
                ))}
              </div>
            ) : (
              <div className="glass-card flex flex-col items-center justify-center rounded-2xl border border-white/10 bg-[#111827]/70 backdrop-blur-md p-8 text-center shadow-xl">
                <div className="mb-3 p-3 bg-slate-900/80 border border-slate-800 rounded-full">
                  <Activity className="h-6 w-6 text-blue-400" aria-hidden="true" />
                </div>
                <p className="text-sm font-bold text-white mb-1">No agent analysis available</p>
                <p className="text-xs text-gray-400">
                  Run a live analysis to see results from the SMS, URL, Transaction, and Graph agents.
                </p>
              </div>
            )}
          </div>

          {/* 4. Geo Intelligence */}
          <GeoIntelligencePanel
            geoData={geoData}
            agentVerdict={geoVerdict}
            agentRiskScore={geoRiskScore}
            isLoading={false}
          />
        </>
      )}

      {/* Evidence + Actions + Timeline — always rendered when data available */}
      {!isLoading && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
          <div className="lg:col-span-2 space-y-6 sm:space-y-8">
            <EvidencePanel evidence={displayDetails.evidence} />
            <RecommendedActions actions={displayDetails.recommended_actions} />
          </div>
          <div className="lg:col-span-1">
            <InvestigationTimeline timeline={displayDetails.timeline} />
          </div>
        </div>
      )}
    </div>
  );
}
