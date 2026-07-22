import type { CaseDetailsData } from '../types/case';
import { Activity } from 'lucide-react';

interface InvestigationSummaryCardProps {
  details: CaseDetailsData;
}

const isPending = (details: CaseDetailsData) =>
  !details.overall_risk_score &&
  !details.confidence_score &&
  (!details.fusion_verdict || details.fusion_verdict === 'Pending Analysis');

export default function InvestigationSummaryCard({ details }: InvestigationSummaryCardProps) {
  if (isPending(details)) {
    return (
      <div className="bg-white shadow-sm ring-1 ring-black ring-opacity-5 rounded-lg p-6 sm:p-8">
        <h3 className="text-base sm:text-lg font-semibold leading-6 text-gray-900 border-b border-gray-200 pb-4 mb-6">
          Fusion Summary
        </h3>
        <div className="flex flex-col items-center justify-center py-8 text-center">
          <div className="mb-3 p-3 bg-gray-100 rounded-full">
            <Activity className="h-6 w-6 text-gray-400" aria-hidden="true" />
          </div>
          <p className="text-sm font-medium text-gray-700 mb-1">No fusion analysis available</p>
          <p className="text-xs text-gray-500 max-w-sm">
            Run a live investigation using the button above to generate a multi-agent fusion report.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white shadow-sm ring-1 ring-black ring-opacity-5 rounded-lg p-4 sm:p-6">
      <h3 className="text-base sm:text-lg font-semibold leading-6 text-gray-900 border-b border-gray-200 pb-4 mb-4">
        Fusion Summary
      </h3>

      {/* Metric cards: 1 col on phones, 2 on sm, 4 on lg */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-5">
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 flex flex-col justify-center">
          <div className="text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">Overall Risk</div>
          <div className="text-2xl font-bold text-gray-900">{details.overall_risk_score}<span className="text-sm font-normal text-gray-500">/100</span></div>
        </div>
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 flex flex-col justify-center">
          <div className="text-xs font-medium text-gray-500 mb-1 uppercase tracking-wide">Confidence</div>
          <div className="text-2xl font-bold text-gray-900">{details.confidence_score}<span className="text-sm font-normal text-gray-500">%</span></div>
        </div>
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 sm:col-span-2 flex flex-col justify-center">
          <div className="text-xs font-medium text-gray-500 mb-1.5 uppercase tracking-wide">Fusion Verdict</div>
          <div className="text-sm sm:text-base font-semibold text-gray-900 break-words">{details.fusion_verdict}</div>
        </div>
      </div>

      <div>
        <h4 className="text-sm font-medium text-gray-900 mb-2">Investigation Summary</h4>
        {details.investigation_summary && details.investigation_summary !== 'No summary available.' ? (
          <p className="text-sm text-gray-600 leading-relaxed bg-blue-50/50 p-4 rounded-md border border-blue-100 break-words">
            {details.investigation_summary}
          </p>
        ) : (
          <p className="text-sm text-gray-400 italic">No narrative summary generated yet.</p>
        )}
      </div>
    </div>
  );
}
