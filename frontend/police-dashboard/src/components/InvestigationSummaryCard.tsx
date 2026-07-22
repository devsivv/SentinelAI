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
      <div className="glass-card border border-white/10 rounded-2xl p-6 sm:p-8 bg-[#111827]/70 backdrop-blur-md shadow-xl">
        <h3 className="text-base sm:text-lg font-bold leading-6 text-white border-b border-white/10 pb-4 mb-6">
          Fusion Summary
        </h3>
        <div className="flex flex-col items-center justify-center py-8 text-center">
          <div className="mb-3 p-3 bg-slate-900/80 border border-slate-800 rounded-full">
            <Activity className="h-6 w-6 text-blue-400" aria-hidden="true" />
          </div>
          <p className="text-sm font-bold text-white mb-1">No fusion analysis available</p>
          <p className="text-xs text-gray-400 max-w-sm">
            Run a live investigation using the button above to generate a multi-agent fusion report.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-card border border-white/10 rounded-2xl p-4 sm:p-6 bg-[#111827]/70 backdrop-blur-md shadow-xl">
      <h3 className="text-base sm:text-lg font-bold leading-6 text-white border-b border-white/10 pb-4 mb-4">
        Fusion Summary
      </h3>

      {/* Metric cards: 1 col on phones, 2 on sm, 4 on lg */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-5">
        <div className="bg-[#0F172A] rounded-xl p-4 border border-white/10 flex flex-col justify-center">
          <div className="text-xs font-bold text-gray-400 mb-1 uppercase tracking-wide">Overall Risk</div>
          <div className="text-3xl font-black text-white">{details.overall_risk_score}<span className="text-sm font-normal text-gray-400">/100</span></div>
        </div>
        <div className="bg-[#0F172A] rounded-xl p-4 border border-white/10 flex flex-col justify-center">
          <div className="text-xs font-bold text-gray-400 mb-1 uppercase tracking-wide">Confidence</div>
          <div className="text-3xl font-black text-white">{details.confidence_score}<span className="text-sm font-normal text-gray-400">%</span></div>
        </div>
        <div className="bg-[#0F172A] rounded-xl p-4 border border-white/10 sm:col-span-2 flex flex-col justify-center">
          <div className="text-xs font-bold text-gray-400 mb-1.5 uppercase tracking-wide">Fusion Verdict</div>
          <div className="text-base sm:text-lg font-bold text-white break-words capitalize">{details.fusion_verdict}</div>
        </div>
      </div>

      <div>
        <h4 className="text-sm font-bold text-white mb-2">Investigation Summary</h4>
        {details.investigation_summary && details.investigation_summary !== 'No summary available.' ? (
          <p className="text-sm text-gray-300 leading-relaxed bg-[#0F172A] p-4 rounded-xl border border-white/10 break-words">
            {details.investigation_summary}
          </p>
        ) : (
          <p className="text-sm text-gray-400 italic">No narrative summary generated yet.</p>
        )}
      </div>
    </div>
  );
}
