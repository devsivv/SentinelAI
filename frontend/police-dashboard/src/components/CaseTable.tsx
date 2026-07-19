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
      <div className="min-w-full divide-y divide-gray-300">
        <div className="hidden md:grid md:grid-cols-7 gap-6 bg-gray-50 px-6 py-4 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
          <div>Case ID</div>
          <div className="col-span-2">Title / Victim</div>
          <div>Risk</div>
          <div>Status</div>
          <div>Date</div>
          <div className="text-right">Actions</div>
        </div>
        <div className="divide-y divide-gray-200 bg-white">
          {cases.map((c) => (
            <div key={c.case_id} className="grid grid-cols-1 md:grid-cols-7 gap-6 px-6 py-5 items-center hover:bg-gray-50 transition-colors">
              {/* Mobile View Labeling + Data, Desktop View just Data */}
              <div className="md:col-span-1 text-sm font-medium text-gray-900">
                <span className="md:hidden text-gray-500 uppercase text-xs mr-2">ID:</span>
                {c.case_id}
              </div>
              <div className="md:col-span-2 text-sm text-gray-500">
                <Link 
                  to={`/cases/${c.case_id}`}
                  className="font-semibold text-gray-900 hover:text-blue-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-1 rounded-sm block truncate"
                  title={c.title}
                >
                  {c.title}
                </Link>
                <div className="mt-0.5">{c.victim_name}</div>
              </div>
              <div className="md:col-span-1 mt-2 md:mt-0">
                 <span className="md:hidden text-gray-500 uppercase text-xs mr-2">Risk:</span>
                 <Badge type="risk" value={c.risk_level} />
              </div>
              <div className="md:col-span-1 mt-2 md:mt-0">
                 <span className="md:hidden text-gray-500 uppercase text-xs mr-2">Status:</span>
                 <Badge type="status" value={c.status} />
              </div>
              <div className="md:col-span-1 text-sm text-gray-500 mt-2 md:mt-0">
                 <span className="md:hidden text-gray-500 uppercase text-xs mr-2">Date:</span>
                 {new Date(c.created_at).toLocaleDateString()}
              </div>
              <div className="md:col-span-1 mt-4 md:mt-0 md:text-right">
                <Link
                  to={`/cases/${c.case_id}`}
                  className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-800 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 rounded-sm"
                >
                  <Eye className="mr-1.5 h-4 w-4" /> View
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
