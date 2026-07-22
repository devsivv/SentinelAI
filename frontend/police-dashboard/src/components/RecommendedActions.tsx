import { Lightbulb, CheckCircle2 } from 'lucide-react';

interface RecommendedActionsProps {
  actions: string[];
}

export default function RecommendedActions({ actions }: RecommendedActionsProps) {
  return (
    <div className="glass-card bg-gradient-to-br from-blue-950/40 to-slate-900/60 border border-blue-500/20 rounded-2xl p-4 sm:p-6 shadow-xl">
      <div className="flex items-center gap-2 mb-4">
        <Lightbulb className="h-5 w-5 text-blue-400 shrink-0" aria-hidden="true" />
        <h3 className="text-base sm:text-lg font-bold leading-6 text-white">
          Recommended Actions
        </h3>
      </div>

      {actions.length > 0 ? (
        <ul className="space-y-2.5" role="list" aria-label="Recommended investigative actions">
          {actions.map((action, index) => (
            <li
              key={index}
              className="flex items-start gap-3 bg-[#0F172A] p-3.5 rounded-xl border border-white/10"
            >
              <CheckCircle2 className="h-5 w-5 text-blue-400 shrink-0 mt-0.5" aria-hidden="true" />
              <span className="text-sm text-gray-200 leading-relaxed break-words flex-1 min-w-0">
                {action}
              </span>
            </li>
          ))}
        </ul>
      ) : (
        <div className="flex flex-col items-center justify-center py-6 text-center">
          <Lightbulb className="h-6 w-6 text-blue-400/60 mb-2" aria-hidden="true" />
          <p className="text-sm font-bold text-white mb-0.5">No actions recommended yet</p>
          <p className="text-xs text-gray-400">
            Run a live analysis to generate investigative action recommendations.
          </p>
        </div>
      )}
    </div>
  );
}
