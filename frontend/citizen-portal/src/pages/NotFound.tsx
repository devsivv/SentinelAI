import { Link } from 'react-router-dom';
import { ShieldOff, ArrowLeft } from 'lucide-react';

const LANDING_URL = import.meta.env.VITE_LANDING_URL || '#';

export default function NotFound() {
  return (
    <div
      className="flex flex-col items-center justify-center min-h-[65vh] px-4 py-12 text-center"
      role="main"
      aria-labelledby="not-found-heading"
    >
      <div className="mb-6 p-5 bg-slate-900/80 border border-slate-800 rounded-full shadow-lg">
        <ShieldOff className="h-12 w-12 text-blue-500" aria-hidden="true" />
      </div>
      <h1
        id="not-found-heading"
        className="text-6xl font-extrabold text-white mb-2 tracking-tight"
        aria-label="404 — Page not found"
      >
        404
      </h1>
      <p className="text-xl font-semibold text-gray-200 mb-2">Page Not Found</p>
      <p className="text-sm text-gray-400 max-w-sm mb-8 leading-relaxed">
        The requested page does not exist or may have been moved.
      </p>
      <div className="flex flex-col sm:flex-row items-center gap-3">
        <Link
          to="/"
          className="inline-flex items-center justify-center rounded-xl bg-blue-600 hover:bg-blue-500 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-blue-900/40 transition-all min-h-[44px] w-full sm:w-auto"
        >
          Return to Workspace Home
        </Link>
        <a
          href={LANDING_URL}
          className="inline-flex items-center justify-center gap-2 rounded-xl border border-gray-700 hover:border-gray-500 bg-white/5 hover:bg-white/10 px-6 py-3 text-sm font-semibold text-gray-300 hover:text-white transition-all min-h-[44px] w-full sm:w-auto"
        >
          <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          <span>SentinelAI Platform</span>
        </a>
      </div>
    </div>
  );
}
