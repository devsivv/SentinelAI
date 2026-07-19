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
import { investigationService } from '../services/api';
import type { AggregatedRiskResponse, BackendAgentEvidence, InvestigateRequest } from '../types/api';
import type { AgentResult } from '../types/case';

export default function CaseDetails() {
  const { id } = useParams<{ id: string }>();
  const [fusionData, setFusionData] = useState<AggregatedRiskResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Base details are still sourced locally (no GET /cases API exists on backend).
  // No fallback to CAS-2026-001: unknown IDs must show the Case Not Found placeholder.
  const details = mockCaseDetails[id || ''] ?? null;

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
            .filter(e => e.type === 'SMS' || e.type === 'URL')
            .map(e => ({
              input_type: e.type.toLowerCase(),
              payload: e.type === 'SMS' ? { text: e.preview } : { url: e.preview }
            }))
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
