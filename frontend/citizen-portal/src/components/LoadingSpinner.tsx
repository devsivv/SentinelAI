import { Loader2 } from 'lucide-react';

interface LoadingSpinnerProps {
  message?: string;
}

export default function LoadingSpinner({ message = 'Loading...' }: LoadingSpinnerProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-gray-500">
      <Loader2 className="w-8 h-8 animate-spin text-indigo-600 mb-4" aria-hidden="true" />
      <p className="text-sm font-medium" role="status" aria-live="polite">{message}</p>
    </div>
  );
}
