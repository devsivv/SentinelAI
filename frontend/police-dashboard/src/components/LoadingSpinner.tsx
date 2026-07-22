import { Loader2 } from 'lucide-react';

interface LoadingSpinnerProps {
  message?: string;
}

export default function LoadingSpinner({ message = 'Loading...' }: LoadingSpinnerProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-gray-400">
      <Loader2 className="w-8 h-8 animate-spin text-blue-500 mb-3" aria-hidden="true" />
      <p className="text-sm font-medium text-gray-300" role="status" aria-live="polite">
        {message}
      </p>
    </div>
  );
}
