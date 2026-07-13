import { useLocation, useParams, Navigate, Link } from 'react-router-dom';
import type { AggregatedRiskResponse, AgentResult } from '../types';
import RiskScoreCard from '../components/RiskScoreCard';
import FusionVerdictCard from '../components/FusionVerdictCard';
import RecommendedActions from '../components/RecommendedActions';
import AgentResultCard from '../components/AgentResultCard';
import { ArrowLeft } from 'lucide-react';

export default function Results() {
  const { caseId } = useParams();
  const location = useLocation();
  const responseData = location.state?.response as AggregatedRiskResponse | undefined;

  if (!responseData) {
    // If accessed directly without form submission state, redirect back to investigate
    return <Navigate to="/investigate" replace />;
  }

  const agentKeys = Object.keys(responseData.evidence || {});

  return (
    <div className="max-w-5xl mx-auto pb-12">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Investigation Results</h2>
          <p className="text-sm text-gray-500 mt-1">Case ID: {caseId}</p>
        </div>
        <Link 
          to="/investigate" 
          className="inline-flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-800"
        >
          <ArrowLeft className="w-4 h-4 mr-1" />
          New Investigation
        </Link>
      </div>

      {/* Top Section: Fusion Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
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
        <div className="mb-8">
          <RecommendedActions actions={responseData.recommended_action} />
        </div>
      )}

      {/* Agent Breakdown */}
      <div>
        <h3 className="text-xl font-bold text-gray-900 mb-4 border-b border-gray-200 pb-2">
          Agent Breakdown
        </h3>
        
        {agentKeys.length === 0 ? (
          <div className="bg-gray-50 p-6 rounded-lg border border-gray-200 text-center text-gray-500">
            No individual agent results were returned for this investigation.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {agentKeys.map(key => {
              const agentResult = responseData.evidence[key] as AgentResult;
              return <AgentResultCard key={key} result={agentResult} />;
            })}
          </div>
        )}
      </div>
    </div>
  );
}
