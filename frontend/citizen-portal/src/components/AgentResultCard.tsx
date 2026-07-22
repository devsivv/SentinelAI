import type { AgentResult } from '../types';
import { ShieldAlert, ShieldCheck, ShieldQuestion, Activity } from 'lucide-react';

interface AgentResultCardProps {
  result: AgentResult;
}

export default function AgentResultCard({ result }: AgentResultCardProps) {
  if (!result) return null;

  const getVerdictStyle = () => {
    switch (result.verdict?.toLowerCase()) {
      case 'fraud':
      case 'fraudulent':
      case 'critical':
      case 'high':
        return {
          icon: <ShieldAlert className="h-5 w-5 text-red-400" aria-hidden="true" />,
          badge: 'bg-red-500/20 text-red-300 border-red-500/30',
          bg: 'bg-red-950/20 border-red-800/30',
        };
      case 'suspicious':
      case 'medium':
        return {
          icon: <ShieldQuestion className="h-5 w-5 text-amber-400" aria-hidden="true" />,
          badge: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
          bg: 'bg-amber-950/20 border-amber-800/30',
        };
      case 'safe':
      case 'clean':
      case 'low':
        return {
          icon: <ShieldCheck className="h-5 w-5 text-green-400" aria-hidden="true" />,
          badge: 'bg-green-500/20 text-green-300 border-green-500/30',
          bg: 'bg-green-950/20 border-green-800/30',
        };
      default:
        return {
          icon: <Activity className="h-5 w-5 text-gray-400" aria-hidden="true" />,
          badge: 'bg-gray-500/20 text-gray-300 border-gray-500/30',
          bg: 'bg-slate-900/60 border-gray-800',
        };
    }
  };

  const { icon, badge, bg } = getVerdictStyle();

  return (
    <div className={`glass-card p-6 rounded-2xl border backdrop-blur-md flex flex-col justify-between ${bg}`}>
      <div className="flex items-start justify-between gap-3 mb-4">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="shrink-0">{icon}</div>
          <div>
            <h4 className="font-bold text-white capitalize text-base break-words">
              {result.agent.replace(/_/g, ' ')}
            </h4>
            {result.category && result.category !== 'none' && (
              <span className="text-[11px] text-gray-400 font-mono block mt-0.5">
                Category: {result.category.replace(/_/g, ' ')}
              </span>
            )}
          </div>
        </div>

        <span className={`px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider border shrink-0 ${badge}`}>
          {result.verdict}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-4 p-3 rounded-xl bg-[#0F172A] border border-white/10">
        <div>
          <span className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider">Risk Score</span>
          <span className="block text-xl font-bold text-white">{result.risk_score}/100</span>
        </div>
        {result.confidence !== undefined && (
          <div>
            <span className="block text-[10px] font-bold text-gray-400 uppercase tracking-wider">Confidence</span>
            <span className="block text-xl font-bold text-white">
              {Math.round(result.confidence <= 1 ? result.confidence * 100 : result.confidence)}%
            </span>
          </div>
        )}
      </div>

      {result.evidence && Object.keys(result.evidence).length > 0 && (
        <div className="pt-3 border-t border-white/10">
          <span className="block text-xs font-semibold text-gray-300 mb-2">Extracted Evidence</span>
          <pre className="bg-[#0F172A] p-3 rounded-xl text-xs font-mono text-gray-300 border border-white/10 overflow-x-auto whitespace-pre-wrap max-h-40">
            {JSON.stringify(result.evidence, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
