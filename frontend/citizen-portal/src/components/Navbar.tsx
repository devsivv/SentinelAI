import { Link, useLocation } from 'react-router-dom';
import { ArrowLeft, Home, FileSearch } from 'lucide-react';
import SentinelAILogo from './SentinelAILogo';

const LANDING_URL = import.meta.env.VITE_LANDING_URL || '#';

export default function Navbar() {
  const location = useLocation();

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#0B1220]/95 backdrop-blur-md border-b border-blue-900/30 text-white" role="banner">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Left: Brand Logo + Portal Badge */}
          <div className="flex items-center gap-3">
            <Link to="/" className="flex items-center gap-2 focus-visible:outline-blue-500 rounded-md">
              <SentinelAILogo size="md" showIcon />
            </Link>
            <span className="hidden sm:inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/10 border border-blue-500/30 text-blue-400 uppercase tracking-wider">
              Citizen Portal
            </span>
          </div>

          {/* Center: Internal Navigation */}
          <div className="flex items-center gap-2 sm:gap-6">
            <Link
              to="/"
              className={`inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                location.pathname === '/'
                  ? 'bg-blue-600/20 text-white border border-blue-500/30'
                  : 'text-gray-300 hover:text-white hover:bg-white/5'
              }`}
            >
              <Home className="h-4 w-4" aria-hidden="true" />
              <span className="hidden sm:inline">Home</span>
            </Link>
            <Link
              to="/investigate"
              className={`inline-flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                location.pathname === '/investigate'
                  ? 'bg-blue-600/20 text-white border border-blue-500/30'
                  : 'text-gray-300 hover:text-white hover:bg-white/5'
              }`}
            >
              <FileSearch className="h-4 w-4" aria-hidden="true" />
              <span>Report & Scan</span>
            </Link>
          </div>

          {/* Right: Back to Landing button */}
          <div className="flex items-center">
            <a
              href={LANDING_URL}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs sm:text-sm font-semibold text-gray-300 hover:text-white border border-gray-700 hover:border-gray-500 rounded-lg hover:bg-white/5 transition-all focus-visible:outline-blue-500 min-h-[44px]"
              aria-label="Return to SentinelAI Main Platform"
            >
              <ArrowLeft className="h-4 w-4" aria-hidden="true" />
              <span className="hidden sm:inline">Platform Home</span>
              <span className="sm:hidden">Landing</span>
            </a>
          </div>

        </div>
      </div>
    </header>
  );
}
