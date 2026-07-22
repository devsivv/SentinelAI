import type { EvidenceItem } from '../types/case';
import { MessageSquare, Link as LinkIcon, DollarSign, Image as ImageIcon, Paperclip } from 'lucide-react';

interface EvidencePanelProps {
  evidence: EvidenceItem[];
}

const evidenceIcons: Record<string, React.ReactNode> = {
  SMS: <MessageSquare className="h-5 w-5 text-blue-500" aria-hidden="true" />,
  URL: <LinkIcon className="h-5 w-5 text-purple-500" aria-hidden="true" />,
  Transaction: <DollarSign className="h-5 w-5 text-green-500" aria-hidden="true" />,
  Image: <ImageIcon className="h-5 w-5 text-orange-500" aria-hidden="true" />,
};

const statusColors: Record<string, string> = {
  Analyzed: 'bg-green-50 text-green-700 ring-green-600/20',
  Flagged: 'bg-red-50 text-red-700 ring-red-600/10',
  Pending: 'bg-yellow-50 text-yellow-800 ring-yellow-600/20',
};

export default function EvidencePanel({ evidence }: EvidencePanelProps) {
  return (
    <div className="bg-white shadow-sm ring-1 ring-black ring-opacity-5 rounded-lg overflow-hidden">
      <div className="px-4 sm:px-6 py-4 border-b border-gray-200 bg-gray-50 flex items-center gap-2">
        <Paperclip className="h-4 w-4 text-gray-400" aria-hidden="true" />
        <h3 className="text-base sm:text-lg font-semibold leading-6 text-gray-900">
          Evidentiary Items
        </h3>
      </div>

      {evidence.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 px-6 text-center">
          <div className="mb-3 p-3 bg-gray-100 rounded-full">
            <Paperclip className="h-6 w-6 text-gray-400" aria-hidden="true" />
          </div>
          <p className="text-sm font-medium text-gray-700 mb-1">No evidence attached</p>
          <p className="text-xs text-gray-500">No evidence artifacts have been attached to this case.</p>
        </div>
      ) : (
        <ul role="list" className="divide-y divide-gray-200">
          {evidence.map((item) => (
            <li key={item.id} className="px-4 sm:px-6 py-4 sm:py-5 flex items-start gap-3 sm:gap-4 hover:bg-gray-50 transition-colors">
              <div className="flex-shrink-0 mt-1">
                {evidenceIcons[item.type] ?? (
                  <MessageSquare className="h-5 w-5 text-gray-400" aria-hidden="true" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
                  <p className="text-sm font-medium text-gray-900 min-w-0 break-words">
                    {item.type}{' '}
                    <span className="text-gray-400 font-normal font-mono text-xs">{item.id}</span>
                  </p>
                  <span
                    className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset whitespace-nowrap ${
                      statusColors[item.status] ?? 'bg-gray-50 text-gray-600 ring-gray-500/10'
                    }`}
                  >
                    {item.status}
                  </span>
                </div>
                <p className="text-sm text-gray-600 break-words bg-gray-100 p-2.5 rounded border border-gray-200 mt-2 font-mono whitespace-pre-wrap text-xs sm:text-sm">
                  {item.preview}
                </p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
