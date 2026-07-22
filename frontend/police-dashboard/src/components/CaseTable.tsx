import { Link } from 'react-router-dom';
import type { InvestigationCase } from '../types/case';
import Badge from './Badge';
import { Eye } from 'lucide-react';

interface CaseTableProps {
  cases: InvestigationCase[];
}

export default function CaseTable({ cases }: CaseTableProps) {
  if (cases.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-gray-300 bg-white p-12 text-center shadow-sm">
        <h3 className="text-lg font-medium text-gray-900">No investigations found.</h3>
        <p className="mt-2 text-sm text-gray-500">
          Try adjusting your search or filters.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden bg-white shadow-sm ring-1 ring-black ring-opacity-5 sm:rounded-lg">
      {/* Desktop column header — hidden on mobile */}
      <div className="hidden md:grid md:grid-cols-[1fr_2fr_auto_auto_auto_auto] gap-x-4 bg-gray-50 px-4 sm:px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 border-b border-gray-200">
        <div>Case ID</div>
        <div>Title / Victim</div>
        <div>Risk</div>
        <div>Status</div>
        <div>Date</div>
        <div className="text-right">Actions</div>
      </div>

      <div className="divide-y divide-gray-200">
        {cases.map((c) => (
          <div
            key={c.case_id}
            className="flex flex-col md:grid md:grid-cols-[1fr_2fr_auto_auto_auto_auto] gap-2 md:gap-x-4 px-4 sm:px-6 py-4 items-start md:items-center hover:bg-gray-50 transition-colors"
          >
            {/* Case ID */}
            <div className="text-xs font-mono text-gray-700 break-all min-w-0 w-full md:w-auto">
              <span className="md:hidden text-gray-400 uppercase text-[10px] mr-1 tracking-wide">ID: </span>
              {c.case_id}
            </div>

            {/* Title + Victim */}
            <div className="min-w-0 w-full md:w-auto">
              <Link
                to={`/cases/${c.case_id}`}
                className="font-semibold text-sm text-gray-900 hover:text-blue-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-1 rounded-sm block break-words leading-snug"
                title={c.title}
              >
                {c.title}
              </Link>
              <div className="text-sm text-gray-500 mt-0.5 break-words">{c.victim_name}</div>
            </div>

            {/* Risk badge */}
            <div className="flex items-center gap-1.5">
              <span className="md:hidden text-[10px] text-gray-400 uppercase tracking-wide">Risk: </span>
              <Badge type="risk" value={c.risk_level} />
            </div>

            {/* Status badge */}
            <div className="flex items-center gap-1.5">
              <span className="md:hidden text-[10px] text-gray-400 uppercase tracking-wide">Status: </span>
              <Badge type="status" value={c.status} />
            </div>

            {/* Date */}
            <div className="text-sm text-gray-500 whitespace-nowrap">
              <span className="md:hidden text-[10px] text-gray-400 uppercase tracking-wide mr-1">Date: </span>
              {new Date(c.created_at).toLocaleDateString()}
            </div>

            {/* View action */}
            <div className="md:text-right">
              <Link
                to={`/cases/${c.case_id}`}
                className="inline-flex items-center justify-center text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 rounded-sm min-h-[44px] gap-1.5"
                aria-label={`View case ${c.case_id}`}
              >
                <Eye className="h-4 w-4" aria-hidden="true" /> View
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
