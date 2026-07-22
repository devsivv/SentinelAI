import type { TimelineEvent } from '../types/case';
import { Clock } from 'lucide-react';

interface InvestigationTimelineProps {
  timeline: TimelineEvent[];
}

export default function InvestigationTimeline({ timeline }: InvestigationTimelineProps) {
  return (
    <div className="glass-card border border-white/10 rounded-2xl p-4 sm:p-6 bg-[#111827]/70 backdrop-blur-md shadow-xl h-full">
      <div className="flex items-center gap-2 mb-5 border-b border-white/10 pb-4">
        <Clock className="h-5 w-5 text-blue-400 shrink-0" aria-hidden="true" />
        <h3 className="text-base sm:text-lg font-bold leading-6 text-white">
          Investigation Timeline
        </h3>
      </div>

      {timeline.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-8 text-center">
          <div className="mb-3 p-3 bg-slate-900/80 border border-slate-800 rounded-full">
            <Clock className="h-5 w-5 text-gray-400" aria-hidden="true" />
          </div>
          <p className="text-sm font-bold text-white mb-1">No activity yet</p>
          <p className="text-xs text-gray-400">Investigation timeline events will appear here.</p>
        </div>
      ) : (
        <div className="flow-root">
          <ul role="list" className="-mb-8">
            {timeline.map((eventItem, eventIdx) => (
              <li key={eventItem.id}>
                <div className="relative pb-8">
                  {eventIdx !== timeline.length - 1 && (
                    <span
                      className="absolute left-4 top-4 -ml-px h-full w-0.5 bg-white/10"
                      aria-hidden="true"
                    />
                  )}
                  <div className="relative flex items-start gap-3 sm:gap-4">
                    <div className="shrink-0 mt-0.5">
                      <span className="h-8 w-8 rounded-full bg-slate-900 flex items-center justify-center ring-8 ring-[#111827] border border-white/10">
                        <div className="h-2.5 w-2.5 rounded-full bg-blue-500" aria-hidden="true" />
                      </span>
                    </div>
                    <div className="flex flex-col gap-0.5 min-w-0 flex-1 pt-1">
                      <p className="text-sm text-gray-300 break-words">
                        {eventItem.event}{' '}
                        <span className="font-bold text-white break-words">
                          by {eventItem.actor}
                        </span>
                      </p>
                      <time
                        dateTime={eventItem.timestamp}
                        className="text-xs text-gray-400 shrink-0 mt-1"
                      >
                        {new Date(eventItem.timestamp).toLocaleString()}
                      </time>
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
