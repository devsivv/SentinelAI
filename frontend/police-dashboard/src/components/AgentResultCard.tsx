import type { AgentResult } from '../types/case';
import { ShieldAlert, ShieldCheck, ShieldQuestion, Activity } from 'lucide-react';

interface AgentResultCardProps {
  result: AgentResult;
}

export default function AgentResultCard({ result }: AgentResultCardProps) {
  const getVerdictStyle = () => {
    switch (result.verdict) {
      case 'Fraudulent':
      case 'Critical':
      case 'High':
        return {
          icon: <ShieldAlert className="h-5 w-5 text-red-400" aria-hidden="true" />,
          badge: 'bg-red-500/20 text-red-300 border-red-500/30',
          bg: 'bg-red-950/20 border-red-800/30',
        };
      case 'Suspicious':
      case 'Medium':
        return {
          icon: <ShieldQuestion className="h-5 w-5 text-amber-400" aria-hidden="true" />,
          badge: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
          bg: 'bg-amber-950/20 border-amber-800/30',
        };
      case 'Clean':
      case 'Low':
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
    <div className={`glass-card rounded-2xl border backdrop-blur-md p-6 flex flex-col justify-between h-full ${bg}`}>
      <div className="flex flex-wrap items-start justify-between gap-3 mb-4">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="shrink-0">{icon}</div>
          <h4 className="font-bold text-white text-base break-words">{result.agent_name}</h4>
        </div>
        <div className={`text-xs font-bold px-2.5 py-1 rounded-full uppercase tracking-wider border shrink-0 ${badge}`}>
          {result.verdict}
        </div>
      </div>
      
      <p className="text-sm text-gray-300 mb-5 bg-[#0F172A] p-4 rounded-xl border border-white/10 leading-relaxed">
        {result.explanation}
      </p>

      <div className="mt-auto flex flex-wrap items-center gap-x-4 gap-y-2 text-xs font-semibold text-gray-400 bg-[#0F172A] px-4 py-3 rounded-xl border border-white/10">
        <div className="flex items-center gap-1.5">
          <span>Risk:</span>
          <span className="text-white font-bold">{result.risk_score}/100</span>
        </div>
        <div className="w-px h-4 bg-white/10 hidden sm:block"></div>
        <div className="flex items-center gap-1.5">
          <span>Confidence:</span>
          <span className="text-white font-bold">{result.confidence}%</span>
        </div>
      </div>
    </div>
  );
}
