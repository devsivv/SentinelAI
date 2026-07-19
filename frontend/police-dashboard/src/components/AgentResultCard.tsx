import type { AgentResult } from '../types/case';
import { ShieldAlert, ShieldCheck, ShieldQuestion, Activity } from 'lucide-react';

interface AgentResultCardProps {
  result: AgentResult;
}

export default function AgentResultCard({ result }: AgentResultCardProps) {
  const getIconAndColor = () => {
    switch (result.verdict) {
      case 'Fraudulent':
      case 'Critical':
      case 'High':
        return { icon: <ShieldAlert className="h-5 w-5 text-red-600" />, bg: 'bg-red-50', border: 'border-red-200' };
      case 'Suspicious':
      case 'Medium':
        return { icon: <ShieldQuestion className="h-5 w-5 text-amber-600" />, bg: 'bg-amber-50', border: 'border-amber-200' };
      case 'Clean':
      case 'Low':
        return { icon: <ShieldCheck className="h-5 w-5 text-green-600" />, bg: 'bg-green-50', border: 'border-green-200' };
      default:
        return { icon: <Activity className="h-5 w-5 text-gray-600" />, bg: 'bg-gray-50', border: 'border-gray-200' };
    }
  };

  const { icon, bg, border } = getIconAndColor();

  return (
    <div className={`rounded-lg border p-5 flex flex-col h-full ${bg} ${border}`}>
      <div className="flex flex-wrap items-start justify-between gap-3 mb-4">
        <div className="flex items-center gap-2 min-w-0">
          <div className="shrink-0">{icon}</div>
          <h4 className="font-semibold text-gray-900 break-words">{result.agent_name}</h4>
        </div>
        <div className="text-sm font-medium px-2 py-1 bg-white rounded-md shadow-sm border border-gray-200 shrink-0">
          {result.verdict}
        </div>
      </div>
      
      <p className="text-sm text-gray-700 mb-5 bg-white/60 p-3 rounded-md border border-white">
        {result.explanation}
      </p>

      <div className="mt-auto flex flex-wrap items-center gap-x-4 gap-y-2 text-xs font-medium text-gray-600 bg-white px-3 py-2.5 rounded-md shadow-sm border border-gray-200">
        <div className="flex items-center gap-1">
          <span>Risk:</span>
          <span className="text-gray-900">{result.risk_score}/100</span>
        </div>
        <div className="w-px h-4 bg-gray-300 hidden sm:block"></div>
        <div className="flex items-center gap-1">
          <span>Confidence:</span>
          <span className="text-gray-900">{result.confidence}%</span>
        </div>
      </div>
    </div>
  );
}
