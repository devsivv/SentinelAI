import { Link } from 'react-router-dom';
import type { InvestigationCase } from '../types/case';
import Badge from './Badge';
import { Eye, FolderSearch } from 'lucide-react';

interface CaseTableProps {
  cases: InvestigationCase[];
  emptyMessage?: string;
}

function CaseIdCell({ id }: { id: string }) {
  const truncated = id.length > 20 ? `${id.slice(0, 20)}…` : id;
  return (
    <>
      <span
        className="hidden md:inline font-mono text-xs text-blue-300 font-semibold cursor-default"
        title={id}
        aria-label={`Case ID: ${id}`}
      >
        {truncated}
      </span>
      <span className="md:hidden font-mono text-xs text-blue-300 font-semibold break-all">
        {id}
      </span>
    </>
  );
}

export default function CaseTable({ cases, emptyMessage }: CaseTableProps) {
  if (cases.length === 0) {
    return (
      <div className="glass-card flex flex-col items-center justify-center p-10 sm:p-12 text-center border border-white/10 rounded-2xl bg-[#111827]/70 shadow-xl">
        <div className="mb-3 p-3 bg-slate-900/80 border border-slate-800 rounded-full">
          <FolderSearch className="h-6 w-6 text-blue-400" aria-hidden="true" />
        </div>
        <h3 className="text-base font-bold text-white mb-1">No investigations found</h3>
        <p className="text-sm text-gray-400 leading-relaxed">
          {emptyMessage || 'Try adjusting your search or filter criteria.'}
        </p>
      </div>
    );
  }

  return (
    <div className="glass-card overflow-hidden bg-[#111827]/70 border border-white/10 rounded-2xl shadow-xl backdrop-blur-md">
      {/* Desktop column header */}
      <div className="hidden md:grid md:grid-cols-[minmax(0,1fr)_minmax(0,2fr)_auto_auto_auto_auto] gap-x-4 bg-[#080E1A] px-4 sm:px-6 py-3.5 text-left text-xs font-bold uppercase tracking-widest text-gray-400 border-b border-white/10">
        <div>Case ID</div>
        <div>Title / Victim</div>
        <div>Risk</div>
        <div>Status</div>
        <div>Date</div>
        <div className="text-right">Actions</div>
      </div>

      <div className="divide-y divide-white/10">
        {cases.map((c) => (
          <div
            key={c.case_id}
            className="flex flex-col md:grid md:grid-cols-[minmax(0,1fr)_minmax(0,2fr)_auto_auto_auto_auto] gap-2 md:gap-x-4 px-4 sm:px-6 py-4 items-start md:items-center hover:bg-blue-600/10 transition-colors"
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
                className="font-bold text-sm text-white hover:text-blue-400 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 rounded-sm block break-words leading-snug transition-colors"
                title={c.title}
              >
                {c.title}
              </Link>
              <div className="text-xs text-gray-400 mt-0.5 break-words">{c.victim_name}</div>
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
            <div className="text-xs text-gray-400 whitespace-nowrap">
              <span className="md:hidden text-[10px] text-gray-400 uppercase tracking-wide mr-1">Date: </span>
              {new Date(c.created_at).toLocaleDateString()}
            </div>

            {/* View action */}
            <div className="md:text-right">
              <Link
                to={`/cases/${c.case_id}`}
                className="inline-flex items-center justify-center text-sm font-semibold text-blue-400 hover:text-blue-300 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 rounded-lg min-h-[44px] gap-1.5"
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
