import { Lightbulb, CheckCircle2 } from 'lucide-react';

interface RecommendedActionsProps {
  actions: string[];
}

export default function RecommendedActions({ actions }: RecommendedActionsProps) {
  if (!actions || actions.length === 0) {
    return null;
  }

  return (
    <div className="glass-card p-6 sm:p-8 bg-gradient-to-br from-blue-950/40 to-slate-900/60 border border-blue-500/20 rounded-2xl">
      <div className="flex items-center gap-2 mb-4">
        <Lightbulb className="w-5 h-5 text-blue-400 shrink-0" aria-hidden="true" />
        <h3 className="text-lg font-bold text-white">Recommended Actions</h3>
      </div>
      <ul className="space-y-3" role="list">
        {actions.map((action, index) => (
          <li key={index} className="flex items-start gap-3 bg-[#0F172A]/80 p-3.5 rounded-xl border border-white/10">
            <CheckCircle2 className="h-5 w-5 text-blue-400 shrink-0 mt-0.5" aria-hidden="true" />
            <span className="text-sm text-gray-200 leading-relaxed flex-1 min-w-0">{action}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
