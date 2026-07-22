import { AlertCircle, WifiOff, Clock, ServerCrash, ShieldOff } from 'lucide-react';
import { Link } from 'react-router-dom';

type ErrorVariant = 'default' | 'timeout' | 'network' | 'not_found' | 'unavailable' | 'server_error';

interface ErrorStateProps {
  title?: string;
  message?: string;
  variant?: ErrorVariant;
  onRetry?: () => void;
  onBack?: () => void;
  backLabel?: string;
  backTo?: string;
}

const variantConfig: Record<
  ErrorVariant,
  { icon: React.ReactNode; defaultTitle: string; defaultMessage: string; colorClasses: string }
> = {
  default: {
    icon: <AlertCircle className="h-6 w-6 text-red-400" aria-hidden="true" />,
    defaultTitle: 'An error occurred',
    defaultMessage: 'Something went wrong. Please try again.',
    colorClasses: 'bg-red-950/40 border-red-800/50 text-red-200',
  },
  timeout: {
    icon: <Clock className="h-6 w-6 text-amber-400" aria-hidden="true" />,
    defaultTitle: 'Request timed out',
    defaultMessage:
      'SentinelAI analysis is taking longer than expected. This may be due to cold-start inference. Please retry.',
    colorClasses: 'bg-amber-950/40 border-amber-800/50 text-amber-200',
  },
  network: {
    icon: <WifiOff className="h-6 w-6 text-red-400" aria-hidden="true" />,
    defaultTitle: 'Network disconnected',
    defaultMessage:
      'Unable to reach the SentinelAI backend. Please check your connection and retry.',
    colorClasses: 'bg-red-950/40 border-red-800/50 text-red-200',
  },
  not_found: {
    icon: <ShieldOff className="h-6 w-6 text-gray-400" aria-hidden="true" />,
    defaultTitle: 'Resource not found',
    defaultMessage:
      'The requested resource or Case ID does not exist or may have been removed.',
    colorClasses: 'bg-gray-900/60 border-gray-700/50 text-gray-200',
  },
  unavailable: {
    icon: <WifiOff className="h-6 w-6 text-red-400" aria-hidden="true" />,
    defaultTitle: 'Backend unavailable',
    defaultMessage:
      'Unable to reach the SentinelAI backend. The service may be starting up. Please retry in a moment.',
    colorClasses: 'bg-red-950/40 border-red-800/50 text-red-200',
  },
  server_error: {
    icon: <ServerCrash className="h-6 w-6 text-red-400" aria-hidden="true" />,
    defaultTitle: 'Server error',
    defaultMessage:
      'The SentinelAI backend returned an unexpected error. Please retry or contact support.',
    colorClasses: 'bg-red-950/40 border-red-800/50 text-red-200',
  },
};

export default function ErrorState({
  title,
  message,
  variant = 'default',
  onRetry,
  onBack,
  backLabel = 'Back',
  backTo,
}: ErrorStateProps) {
  const config = variantConfig[variant];
  const displayTitle = title || config.defaultTitle;
  const displayMessage = message || config.defaultMessage;

  return (
    <div
      className={`rounded-xl border p-6 backdrop-blur-md shadow-xl ${config.colorClasses}`}
      role="alert"
      aria-live="assertive"
    >
      <div className="flex flex-col sm:flex-row gap-4 items-start">
        <div className="p-2 rounded-lg bg-black/20 shrink-0">{config.icon}</div>
        <div className="flex-1 min-w-0">
          <h3 className="text-base font-semibold">{displayTitle}</h3>
          <p className="mt-1 text-sm opacity-90 break-words leading-relaxed">{displayMessage}</p>

          {(onRetry || onBack || backTo) && (
            <div className="mt-5 flex flex-wrap gap-3">
              {onRetry && (
                <button
                  type="button"
                  onClick={onRetry}
                  className="inline-flex items-center justify-center rounded-lg bg-white/10 hover:bg-white/20 border border-white/20 px-4 py-2 text-sm font-semibold text-white transition-colors min-h-[44px]"
                >
                  Retry
                </button>
              )}
              {onBack && (
                <button
                  type="button"
                  onClick={onBack}
                  className="inline-flex items-center justify-center rounded-lg bg-white/10 hover:bg-white/20 border border-white/20 px-4 py-2 text-sm font-semibold text-white transition-colors min-h-[44px]"
                >
                  {backLabel}
                </button>
              )}
              {backTo && !onBack && (
                <Link
                  to={backTo}
                  className="inline-flex items-center justify-center rounded-lg bg-white/10 hover:bg-white/20 border border-white/20 px-4 py-2 text-sm font-semibold text-white transition-colors min-h-[44px]"
                >
                  {backLabel}
                </Link>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
