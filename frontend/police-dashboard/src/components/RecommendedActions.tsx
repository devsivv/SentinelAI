import { Lightbulb, CheckCircle2 } from 'lucide-react';

interface RecommendedActionsProps {
  actions: string[];
}

export default function RecommendedActions({ actions }: RecommendedActionsProps) {
  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 shadow-sm ring-1 ring-blue-100 rounded-lg p-6">
      <div className="flex items-center gap-2 mb-4">
        <Lightbulb className="h-5 w-5 text-blue-600 flex-shrink-0" />
        <h3 className="text-lg font-semibold leading-6 text-blue-900 break-words">
          Recommended Actions
        </h3>
      </div>
      
      {actions.length > 0 ? (
        <ul className="space-y-3">
          {actions.map((action, index) => (
            <li key={index} className="flex items-start gap-3 bg-white/60 p-3 rounded-md border border-blue-100 shadow-sm">
              <CheckCircle2 className="h-5 w-5 text-blue-500 flex-shrink-0 mt-0.5" />
              <span className="text-sm text-gray-800 leading-6 break-words flex-1 min-w-0">{action}</span>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-gray-500">No actions recommended at this time.</p>
      )}
    </div>
  );
}
