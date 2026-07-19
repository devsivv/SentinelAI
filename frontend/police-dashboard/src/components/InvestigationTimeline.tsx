import type { TimelineEvent } from '../types/case';
import { Clock } from 'lucide-react';

interface InvestigationTimelineProps {
  timeline: TimelineEvent[];
}

export default function InvestigationTimeline({ timeline }: InvestigationTimelineProps) {
  return (
    <div className="bg-white shadow-sm ring-1 ring-black ring-opacity-5 rounded-lg p-6">
      <div className="flex items-center gap-2 mb-6 border-b border-gray-200 pb-4">
        <Clock className="h-5 w-5 text-gray-400" />
        <h3 className="text-lg font-semibold leading-6 text-gray-900">
          Investigation Timeline
        </h3>
      </div>
      
      <div className="flow-root">
        <ul role="list" className="-mb-8">
          {timeline.map((eventItem, eventIdx) => (
            <li key={eventItem.id}>
              <div className="relative pb-8">
                {eventIdx !== timeline.length - 1 ? (
                  <span className="absolute left-4 top-4 -ml-px h-full w-0.5 bg-gray-200" aria-hidden="true" />
                ) : null}
                <div className="relative flex items-start gap-4">
                  <div className="shrink-0 mt-0.5">
                    <span className="h-8 w-8 rounded-full bg-slate-100 flex items-center justify-center ring-8 ring-white border border-gray-200">
                      <div className="h-2.5 w-2.5 rounded-full bg-blue-500" />
                    </span>
                  </div>
                  <div className="flex flex-col md:flex-row md:items-start justify-between gap-1 md:gap-4 min-w-0 flex-1 pt-1.5">
                    <div className="min-w-0 flex-1">
                      <p className="text-sm text-gray-600 break-words">
                        {eventItem.event} <span className="font-medium text-gray-900 break-words block sm:inline">by {eventItem.actor}</span>
                      </p>
                    </div>
                    <div className="text-sm text-gray-500 shrink-0 mt-1 md:mt-0">
                      <time dateTime={eventItem.timestamp}>{new Date(eventItem.timestamp).toLocaleString()}</time>
                    </div>
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
