import { Bell, User, Menu, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

const LANDING_URL = import.meta.env.VITE_LANDING_URL || '#';

interface HeaderProps {
  onMenuClick: () => void;
}

export default function Header({ onMenuClick }: HeaderProps) {
  return (
    <header
      className="flex h-16 shrink-0 items-center justify-between border-b border-gray-200 bg-white px-4 sm:px-6 shadow-sm gap-2"
      role="banner"
    >
      {/* Left: hamburger — mobile/tablet only */}
      <div className="flex items-center gap-2 lg:hidden">
        <button
          type="button"
          onClick={onMenuClick}
          className="inline-flex items-center justify-center h-11 w-11 rounded-md text-gray-500 hover:text-gray-700 hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 transition-colors"
          aria-label="Open navigation menu"
          aria-haspopup="dialog"
        >
          <Menu className="h-5 w-5" aria-hidden="true" />
        </button>
      </div>

      {/* Spacer / Navigation links */}
      <div className="flex items-center gap-3 min-w-0">
        <a
          href={LANDING_URL}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs sm:text-sm font-semibold text-gray-700 hover:text-blue-600 border border-gray-300 hover:border-blue-400 rounded-lg hover:bg-blue-50 transition-all focus-visible:outline-blue-500 min-h-[38px]"
          aria-label="Return to SentinelAI Main Platform"
        >
          <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          <span className="hidden sm:inline">Platform Home</span>
          <span className="sm:hidden">Landing</span>
        </a>
      </div>

      {/* Right: notification + profile */}
      <div className="flex items-center gap-1 sm:gap-3 shrink-0">
        {/* Bell */}
        <Link
          to="/alerts"
          className="inline-flex items-center justify-center h-11 w-11 rounded-full text-gray-400 hover:text-gray-600 hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 transition-colors"
          aria-label="View system alerts"
        >
          <Bell className="h-5 w-5" aria-hidden="true" />
        </Link>

        {/* Divider */}
        <div className="hidden sm:block h-6 w-px bg-gray-200 mx-1" aria-hidden="true" />

        {/* Profile link */}
        <Link
          to="/profile"
          className="inline-flex items-center gap-2.5 h-11 px-2 rounded-lg text-gray-700 hover:bg-gray-100 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 transition-colors"
          aria-label="Go to profile settings"
        >
          {/* Avatar */}
          <div
            className="h-8 w-8 rounded-full bg-slate-800 flex items-center justify-center text-white border border-slate-700 shrink-0"
            aria-hidden="true"
          >
            <User className="h-4 w-4" />
          </div>
          {/* Name label — shown sm+ only */}
          <span className="hidden sm:block text-sm font-semibold text-gray-800 whitespace-nowrap">
            Investigator
          </span>
        </Link>
      </div>
    </header>
  );
}
