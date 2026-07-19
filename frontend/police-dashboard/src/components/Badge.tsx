import type { CaseStatus, RiskLevel } from '../types/case';

interface BadgeProps {
  type: 'status' | 'risk';
  value: CaseStatus | RiskLevel;
}

export default function Badge({ type, value }: BadgeProps) {
  const getStyles = () => {
    if (type === 'status') {
      switch (value as CaseStatus) {
        case 'Open':
          return 'bg-blue-50 text-blue-700 ring-blue-700/10';
        case 'Under Review':
          return 'bg-amber-50 text-amber-800 ring-amber-600/20';
        case 'Closed':
          return 'bg-gray-50 text-gray-600 ring-gray-500/10';
        default:
          return 'bg-gray-50 text-gray-600 ring-gray-500/10';
      }
    } else {
      switch (value as RiskLevel) {
        case 'Low':
          return 'bg-green-50 text-green-700 ring-green-600/20';
        case 'Medium':
          return 'bg-yellow-50 text-yellow-800 ring-yellow-600/20';
        case 'High':
          return 'bg-orange-50 text-orange-700 ring-orange-600/20';
        case 'Critical':
          return 'bg-red-50 text-red-700 ring-red-600/10';
        default:
          return 'bg-gray-50 text-gray-600 ring-gray-500/10';
      }
    }
  };

  return (
    <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset ${getStyles()}`}>
      {value}
    </span>
  );
}
