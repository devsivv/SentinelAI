import type { EvidenceItem } from '../types/case';
import { MessageSquare, Link as LinkIcon, DollarSign, Image as ImageIcon, Paperclip } from 'lucide-react';

interface EvidencePanelProps {
  evidence: EvidenceItem[];
}

const evidenceIcons: Record<string, React.ReactNode> = {
  SMS: <MessageSquare className="h-5 w-5 text-blue-400" aria-hidden="true" />,
  URL: <LinkIcon className="h-5 w-5 text-purple-400" aria-hidden="true" />,
  Transaction: <DollarSign className="h-5 w-5 text-green-400" aria-hidden="true" />,
  Image: <ImageIcon className="h-5 w-5 text-orange-400" aria-hidden="true" />,
};

const statusColors: Record<string, string> = {
  Analyzed: 'bg-green-500/20 text-green-300 border-green-500/30',
  Flagged: 'bg-red-500/20 text-red-300 border-red-500/30',
  Pending: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
};

export default function EvidencePanel({ evidence }: EvidencePanelProps) {
  return (
    <div className="glass-card rounded-2xl border border-white/10 overflow-hidden bg-[#111827]/70 backdrop-blur-md shadow-xl">
      <div className="px-4 sm:px-6 py-4 border-b border-white/10 bg-[#080E1A] flex items-center gap-2">
        <Paperclip className="h-4 w-4 text-blue-400" aria-hidden="true" />
        <h3 className="text-base sm:text-lg font-bold leading-6 text-white">
          Evidentiary Items
        </h3>
      </div>

      {evidence.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 px-6 text-center">
          <div className="mb-3 p-3 bg-slate-900/80 border border-slate-800 rounded-full">
            <Paperclip className="h-6 w-6 text-gray-400" aria-hidden="true" />
          </div>
          <p className="text-sm font-bold text-white mb-1">No evidence attached</p>
          <p className="text-xs text-gray-400">No evidence artifacts have been attached to this case.</p>
        </div>
      ) : (
        <ul role="list" className="divide-y divide-white/10">
          {evidence.map((item) => (
            <li key={item.id} className="px-4 sm:px-6 py-4 sm:py-5 flex items-start gap-3 sm:gap-4 hover:bg-blue-600/10 transition-colors">
              <div className="flex-shrink-0 mt-1">
                {evidenceIcons[item.type] ?? (
                  <MessageSquare className="h-5 w-5 text-gray-400" aria-hidden="true" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
                  <p className="text-sm font-bold text-white min-w-0 break-words">
                    {item.type}{' '}
                    <span className="text-gray-400 font-normal font-mono text-xs">{item.id}</span>
                  </p>
                  <span
                    className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-bold uppercase tracking-wider border whitespace-nowrap ${
                      statusColors[item.status] ?? 'bg-gray-800 text-gray-400 border-gray-700'
                    }`}
                  >
                    {item.status}
                  </span>
                </div>
                <p className="text-sm text-gray-300 break-words bg-[#0F172A] p-3 rounded-xl border border-white/10 mt-2 font-mono whitespace-pre-wrap text-xs sm:text-sm">
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
