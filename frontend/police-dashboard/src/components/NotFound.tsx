import { Link } from 'react-router-dom';
import { ShieldOff } from 'lucide-react';

export default function NotFound() {
  return (
    <div
      className="flex flex-col items-center justify-center min-h-[60vh] px-4 text-center"
      role="main"
      aria-labelledby="not-found-heading"
    >
      <div className="mb-6 p-5 bg-gray-100 rounded-full">
        <ShieldOff className="h-12 w-12 text-gray-400" aria-hidden="true" />
      </div>
      <h1
        id="not-found-heading"
        className="text-6xl font-extrabold text-gray-900 mb-2"
        aria-label="404 — Page not found"
      >
        404
      </h1>
      <p className="text-xl font-semibold text-gray-700 mb-2">Page Not Found</p>
      <p className="text-sm text-gray-500 max-w-sm mb-8">
        The page you requested does not exist or may have been moved. Please navigate using the
        links below.
      </p>
      <div className="flex flex-col sm:flex-row items-center gap-3">
        <Link
          to="/"
          className="inline-flex items-center justify-center rounded-md bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 transition-colors min-h-[44px] w-full sm:w-auto"
        >
          Return to Dashboard
        </Link>
        <Link
          to="/cases"
          className="inline-flex items-center justify-center rounded-md bg-white px-5 py-2.5 text-sm font-semibold text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 transition-colors min-h-[44px] w-full sm:w-auto"
        >
          Return to Cases
        </Link>
      </div>
    </div>
  );
}
