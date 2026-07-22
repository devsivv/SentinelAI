import { Lightbulb, CheckCircle2 } from 'lucide-react';

interface RecommendedActionsProps {
  actions: string[];
}

export default function RecommendedActions({ actions }: RecommendedActionsProps) {
  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 shadow-sm ring-1 ring-blue-100 rounded-lg p-4 sm:p-6">
      <div className="flex items-center gap-2 mb-4">
        <Lightbulb className="h-5 w-5 text-blue-600 flex-shrink-0" aria-hidden="true" />
        <h3 className="text-base sm:text-lg font-semibold leading-6 text-blue-900">
          Recommended Actions
        </h3>
      </div>

      {actions.length > 0 ? (
        <ul className="space-y-2.5" role="list" aria-label="Recommended investigative actions">
          {actions.map((action, index) => (
            <li
              key={index}
              className="flex items-start gap-3 bg-white/60 p-3 rounded-md border border-blue-100 shadow-sm"
            >
              <CheckCircle2 className="h-5 w-5 text-blue-500 flex-shrink-0 mt-0.5" aria-hidden="true" />
              <span className="text-sm text-gray-800 leading-relaxed break-words flex-1 min-w-0">
                {action}
              </span>
            </li>
          ))}
        </ul>
      ) : (
        <div className="flex flex-col items-center justify-center py-6 text-center">
          <Lightbulb className="h-6 w-6 text-blue-300 mb-2" aria-hidden="true" />
          <p className="text-sm font-medium text-blue-800 mb-0.5">No actions recommended yet</p>
          <p className="text-xs text-blue-600/70">
            Run a live analysis to generate investigative action recommendations.
          </p>
        </div>
      )}
    </div>
  );
}
