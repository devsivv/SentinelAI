import { useLocation, useParams, Navigate, Link } from 'react-router-dom';
import type { AggregatedRiskResponse, AgentResult } from '../types';
import RiskScoreCard from '../components/RiskScoreCard';
import FusionVerdictCard from '../components/FusionVerdictCard';
import RecommendedActions from '../components/RecommendedActions';
import AgentResultCard from '../components/AgentResultCard';
import { ArrowLeft, ShieldCheck } from 'lucide-react';

export default function Results() {
  const { caseId } = useParams();
  const location = useLocation();
  const responseData = location.state?.response as AggregatedRiskResponse | undefined;

  if (!responseData) {
    return <Navigate to="/investigate" replace />;
  }

  const agentKeys = Object.keys(responseData.evidence || {});

  return (
    <div className="max-w-5xl mx-auto pb-12 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-white/10 pb-5">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-300 text-xs font-semibold uppercase tracking-wider mb-2">
            <ShieldCheck className="h-3.5 w-3.5" aria-hidden="true" />
            Intelligence Fusion Output
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Investigation Results
          </h1>
          <p className="text-sm font-mono text-gray-400 mt-1">Case ID: {caseId}</p>
        </div>

        <Link
          to="/investigate"
          className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold text-gray-300 hover:text-white border border-gray-700 hover:border-gray-500 bg-white/5 hover:bg-white/10 transition-all min-h-[44px] self-start sm:self-auto"
        >
          <ArrowLeft className="w-4 h-4" aria-hidden="true" />
          <span>New Investigation</span>
        </Link>
      </div>

      {/* Top Section: Fusion Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-1">
          <RiskScoreCard score={responseData.overall_risk} />
        </div>
        <div className="md:col-span-2">
          <FusionVerdictCard
            verdict={responseData.final_verdict}
            narrative={responseData.narrative}
          />
        </div>
      </div>

      {/* Recommended Actions */}
      {responseData.recommended_action && responseData.recommended_action.length > 0 && (
        <div>
          <RecommendedActions actions={responseData.recommended_action} />
        </div>
      )}

      {/* Agent Breakdown */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-white border-b border-white/10 pb-3">
          Agent Breakdown
        </h3>

        {agentKeys.length === 0 ? (
          <div className="glass-card p-8 text-center text-gray-400">
            No individual agent results were returned for this investigation.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {agentKeys.map((key) => {
              const agentResult = responseData.evidence[key] as AgentResult;
              return <AgentResultCard key={key} result={agentResult} />;
            })}
          </div>
        )}
      </div>
    </div>
  );
}
