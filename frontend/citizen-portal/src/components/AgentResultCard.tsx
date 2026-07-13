import type { AgentResult } from '../types';

interface AgentResultCardProps {
  result: AgentResult;
}

export default function AgentResultCard({ result }: AgentResultCardProps) {
  if (!result) return null;

  // Determine badge color based on verdict
  let badgeColor = 'bg-gray-100 text-gray-800';
  if (result.verdict === 'safe') {
    badgeColor = 'bg-green-100 text-green-800';
  } else if (result.verdict === 'suspicious') {
    badgeColor = 'bg-amber-100 text-amber-800';
  } else if (result.verdict === 'fraud') {
    badgeColor = 'bg-red-100 text-red-800';
  }

  return (
    <div className="bg-white p-5 rounded-lg shadow-sm border border-gray-200">
      <div className="flex justify-between items-start mb-4">
        <div>
          <h4 className="text-lg font-medium text-gray-900 capitalize">
            {result.agent.replace(/_/g, ' ')}
          </h4>
          {result.category && result.category !== 'none' && (
            <span className="text-xs text-gray-500 uppercase tracking-wider">
              Category: {result.category.replace(/_/g, ' ')}
            </span>
          )}
        </div>
        <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium uppercase ${badgeColor}`}>
          {result.verdict}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <span className="block text-xs font-medium text-gray-500 uppercase">Risk Score</span>
          <span className="block text-xl font-semibold text-gray-900">{result.risk_score}</span>
        </div>
        {result.confidence !== undefined && (
          <div>
            <span className="block text-xs font-medium text-gray-500 uppercase">Confidence</span>
            <span className="block text-xl font-semibold text-gray-900">
              {Math.round(result.confidence * 100)}%
            </span>
          </div>
        )}
      </div>

      {result.evidence && Object.keys(result.evidence).length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <span className="block text-xs font-medium text-gray-700 mb-2">Extracted Evidence</span>
          <pre className="bg-gray-50 p-3 rounded-md text-xs text-gray-600 overflow-x-auto whitespace-pre-wrap">
            {JSON.stringify(result.evidence, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
