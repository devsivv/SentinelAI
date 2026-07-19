import type { CaseDetailsData } from '../types/case';

interface InvestigationSummaryCardProps {
  details: CaseDetailsData;
}

export default function InvestigationSummaryCard({ details }: InvestigationSummaryCardProps) {
  return (
    <div className="bg-white shadow-sm ring-1 ring-black ring-opacity-5 rounded-lg p-6">
      <h3 className="text-lg font-semibold leading-6 text-gray-900 border-b border-gray-200 pb-4 mb-4">
        Fusion Summary
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 flex flex-col h-full justify-center">
          <div className="text-sm font-medium text-gray-500 mb-1">Overall Risk</div>
          <div className="text-2xl font-bold text-gray-900">{details.overall_risk_score}/100</div>
        </div>
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 flex flex-col h-full justify-center">
          <div className="text-sm font-medium text-gray-500 mb-1">Confidence</div>
          <div className="text-2xl font-bold text-gray-900">{details.confidence_score}%</div>
        </div>
        <div className="bg-gray-50 rounded-lg p-4 border border-gray-200 lg:col-span-2 flex flex-col justify-center items-start h-full">
          <div className="text-sm font-medium text-gray-500 mb-2">Fusion Verdict</div>
          <div className="text-lg font-semibold text-gray-900 break-words">{details.fusion_verdict}</div>
        </div>
      </div>

      <div>
        <h4 className="text-sm font-medium text-gray-900 mb-2">Investigation Summary</h4>
        <p className="text-sm text-gray-600 leading-relaxed bg-blue-50/50 p-4 rounded-md border border-blue-100 break-words">
          {details.investigation_summary}
        </p>
      </div>
    </div>
  );
}
