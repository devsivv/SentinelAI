import type { EvidenceItem } from '../types/case';
import { MessageSquare, Link as LinkIcon, DollarSign, Image as ImageIcon } from 'lucide-react';

interface EvidencePanelProps {
  evidence: EvidenceItem[];
}

export default function EvidencePanel({ evidence }: EvidencePanelProps) {
  const getEvidenceIcon = (type: string) => {
    switch (type) {
      case 'SMS': return <MessageSquare className="h-5 w-5 text-blue-500" />;
      case 'URL': return <LinkIcon className="h-5 w-5 text-purple-500" />;
      case 'Transaction': return <DollarSign className="h-5 w-5 text-green-500" />;
      case 'Image': return <ImageIcon className="h-5 w-5 text-orange-500" />;
      default: return <MessageSquare className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Analyzed': return 'bg-green-50 text-green-700 ring-green-600/20';
      case 'Flagged': return 'bg-red-50 text-red-700 ring-red-600/10';
      case 'Pending': return 'bg-yellow-50 text-yellow-800 ring-yellow-600/20';
      default: return 'bg-gray-50 text-gray-600 ring-gray-500/10';
    }
  };

  return (
    <div className="bg-white shadow-sm ring-1 ring-black ring-opacity-5 rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <h3 className="text-lg font-semibold leading-6 text-gray-900">
          Evidentiary Items
        </h3>
      </div>
      <ul role="list" className="divide-y divide-gray-200">
        {evidence.map((item) => (
          <li key={item.id} className="px-6 py-5 flex items-start gap-4 hover:bg-gray-50 transition-colors">
            <div className="flex-shrink-0 mt-1">
              {getEvidenceIcon(item.type)}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
                <p className="text-sm font-medium text-gray-900 min-w-0 break-words">
                  {item.type} <span className="text-gray-400 font-normal ml-2">{item.id}</span>
                </p>
                <span className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ring-1 ring-inset whitespace-nowrap ${getStatusColor(item.status)}`}>
                  {item.status}
                </span>
              </div>
              <p className="text-sm text-gray-600 break-words bg-gray-100 p-2.5 rounded border border-gray-200 mt-2 font-mono whitespace-pre-wrap">
                {item.preview}
              </p>
            </div>
          </li>
        ))}
        {evidence.length === 0 && (
          <li className="px-6 py-8 text-center text-sm text-gray-500">
            No evidence artifacts attached to this case.
          </li>
        )}
      </ul>
    </div>
  );
}
