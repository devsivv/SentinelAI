import { ShieldAlert } from 'lucide-react';

interface RecommendedActionsProps {
  actions: string[];
}

export default function RecommendedActions({ actions }: RecommendedActionsProps) {
  if (!actions || actions.length === 0) {
    return null;
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <div className="flex items-center gap-2 mb-4">
        <ShieldAlert className="w-5 h-5 text-indigo-600" />
        <h3 className="text-lg font-medium text-gray-900">Recommended Actions</h3>
      </div>
      <ul className="space-y-3">
        {actions.map((action, index) => (
          <li key={index} className="flex items-start">
            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center text-sm font-medium mr-3">
              {index + 1}
            </span>
            <span className="text-gray-700 mt-0.5">{action}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
