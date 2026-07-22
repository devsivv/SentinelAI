import { AlertCircle, WifiOff, Clock, ServerCrash, ShieldOff } from 'lucide-react';
import { Link } from 'react-router-dom';

type ErrorVariant = 'default' | 'timeout' | 'network' | 'not_found' | 'unavailable' | 'server_error';

interface ErrorStateProps {
  title?: string;
  message?: string;
  /** One of the classified error types from classifyApiError */
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
    colorClasses: 'bg-red-50 border-red-200 text-red-800',
  },
  timeout: {
    icon: <Clock className="h-6 w-6 text-amber-400" aria-hidden="true" />,
    defaultTitle: 'Request timed out',
    defaultMessage:
      'SentinelAI analysis is taking longer than expected. This may be due to cold-start inference. Please retry.',
    colorClasses: 'bg-amber-50 border-amber-200 text-amber-800',
  },
  network: {
    icon: <WifiOff className="h-6 w-6 text-red-400" aria-hidden="true" />,
    defaultTitle: 'Network disconnected',
    defaultMessage:
      'Unable to reach the SentinelAI backend. Please check your connection and retry.',
    colorClasses: 'bg-red-50 border-red-200 text-red-800',
  },
  not_found: {
    icon: <ShieldOff className="h-6 w-6 text-gray-400" aria-hidden="true" />,
    defaultTitle: 'Case not found',
    defaultMessage:
      'This case may have been deleted or the ID is invalid. It does not exist in the database.',
    colorClasses: 'bg-gray-50 border-gray-200 text-gray-800',
  },
  unavailable: {
    icon: <WifiOff className="h-6 w-6 text-red-400" aria-hidden="true" />,
    defaultTitle: 'Backend unavailable',
    defaultMessage:
      'Unable to reach the SentinelAI backend. The service may be starting up. Please retry in a moment.',
    colorClasses: 'bg-red-50 border-red-200 text-red-800',
  },
  server_error: {
    icon: <ServerCrash className="h-6 w-6 text-red-400" aria-hidden="true" />,
    defaultTitle: 'Server error',
    defaultMessage:
      'The SentinelAI backend returned an unexpected error. Please retry or contact support.',
    colorClasses: 'bg-red-50 border-red-200 text-red-800',
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
      className={`rounded-lg border p-5 ${config.colorClasses}`}
      role="alert"
      aria-live="assertive"
    >
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-shrink-0">{config.icon}</div>
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-semibold">{displayTitle}</h3>
          <p className="mt-1 text-sm opacity-90 break-words">{displayMessage}</p>

          {(onRetry || onBack || backTo) && (
            <div className="mt-4 flex flex-wrap gap-3">
              {onRetry && (
                <button
                  type="button"
                  onClick={onRetry}
                  className="inline-flex items-center justify-center rounded-md bg-white border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 transition-colors min-h-[44px]"
                >
                  Retry
                </button>
              )}
              {onBack && (
                <button
                  type="button"
                  onClick={onBack}
                  className="inline-flex items-center justify-center rounded-md bg-white border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 transition-colors min-h-[44px]"
                >
                  {backLabel}
                </button>
              )}
              {backTo && !onBack && (
                <Link
                  to={backTo}
                  className="inline-flex items-center justify-center rounded-md bg-white border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 transition-colors min-h-[44px]"
                >
                  {backLabel}
                </Link>
              )}
              <Link
                to="/cases"
                className="inline-flex items-center justify-center rounded-md bg-white border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 transition-colors min-h-[44px]"
              >
                Back to Cases
              </Link>
              <Link
                to="/"
                className="inline-flex items-center justify-center rounded-md bg-white border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 transition-colors min-h-[44px]"
              >
                Dashboard
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
