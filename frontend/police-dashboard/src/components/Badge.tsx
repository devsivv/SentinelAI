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
          return 'bg-blue-500/20 text-blue-300 border-blue-500/30';
        case 'Under Review':
          return 'bg-amber-500/20 text-amber-300 border-amber-500/30';
        case 'Closed':
          return 'bg-gray-800 text-gray-400 border-gray-700';
        default:
          return 'bg-gray-800 text-gray-400 border-gray-700';
      }
    } else {
      switch (value as RiskLevel) {
        case 'Low':
          return 'bg-green-500/20 text-green-300 border-green-500/30';
        case 'Medium':
          return 'bg-amber-500/20 text-amber-300 border-amber-500/30';
        case 'High':
          return 'bg-orange-500/20 text-orange-300 border-orange-500/30';
        case 'Critical':
          return 'bg-red-500/20 text-red-300 border-red-500/30';
        default:
          return 'bg-gray-800 text-gray-400 border-gray-700';
      }
    }
  };

  return (
    <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-bold uppercase tracking-wider border whitespace-nowrap ${getStyles()}`}>
      {value}
    </span>
  );
}
