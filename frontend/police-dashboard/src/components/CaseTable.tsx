import { Link } from 'react-router-dom';
import type { InvestigationCase } from '../types/case';
import Badge from './Badge';
import { Eye, FolderSearch } from 'lucide-react';

interface CaseTableProps {
  cases: InvestigationCase[];
  /** Called when the search/filter yields no results (not a fetch error) */
  emptyMessage?: string;
}

/**
 * Truncates a Case ID or UUID for display.
 * Full value always preserved in title tooltip.
 * Desktop: show first 26 chars + ellipsis.
 * Mobile: break-all wrapping.
 */
function CaseIdCell({ id }: { id: string }) {
  const truncated = id.length > 20 ? `${id.slice(0, 20)}…` : id;
  return (
    <>
      {/* Desktop: truncated with tooltip */}
      <span
        className="hidden md:inline font-mono text-xs text-gray-700 cursor-default"
        title={id}
        aria-label={`Case ID: ${id}`}
      >
        {truncated}
      </span>
      {/* Mobile: full ID, break-all */}
      <span className="md:hidden font-mono text-xs text-gray-700 break-all">
        {id}
      </span>
    </>
  );
}

export default function CaseTable({ cases, emptyMessage }: CaseTableProps) {
  if (cases.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-gray-300 bg-white p-10 sm:p-12 text-center shadow-sm">
        <div className="mb-3 p-3 bg-gray-100 rounded-full">
          <FolderSearch className="h-6 w-6 text-gray-400" aria-hidden="true" />
        </div>
        <h3 className="text-base font-semibold text-gray-900 mb-1">No investigations found</h3>
        <p className="text-sm text-gray-500">
          {emptyMessage || 'Try adjusting your search or filter criteria.'}
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden bg-white shadow-sm ring-1 ring-black ring-opacity-5 sm:rounded-lg">
      {/* Desktop column header */}
      <div className="hidden md:grid md:grid-cols-[minmax(0,1fr)_minmax(0,2fr)_auto_auto_auto_auto] gap-x-4 bg-gray-50 px-4 sm:px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 border-b border-gray-200">
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
            className="flex flex-col md:grid md:grid-cols-[minmax(0,1fr)_minmax(0,2fr)_auto_auto_auto_auto] gap-2 md:gap-x-4 px-4 sm:px-6 py-4 items-start md:items-center hover:bg-gray-50 transition-colors"
          >
            {/* Case ID */}
            <div className="min-w-0 w-full md:w-auto">
              <span className="md:hidden text-[10px] text-gray-400 uppercase tracking-wide mr-1">ID: </span>
              <CaseIdCell id={c.case_id} />
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
              <div className="text-xs text-gray-500 mt-0.5 break-words">{c.victim_name}</div>
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
            <div className="text-xs text-gray-500 whitespace-nowrap">
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
