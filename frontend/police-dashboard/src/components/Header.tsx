import { Bell, User, Menu, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

const LANDING_URL = import.meta.env.VITE_LANDING_URL || '#';

interface HeaderProps {
  onMenuClick: () => void;
}

export default function Header({ onMenuClick }: HeaderProps) {
  return (
    <header
      className="flex h-16 shrink-0 items-center justify-between border-b border-white/10 bg-[#0B1220]/90 backdrop-blur-md px-4 sm:px-6 gap-2 text-white"
      role="banner"
    >
      {/* Left: hamburger — mobile/tablet only */}
      <div className="flex items-center gap-2 lg:hidden">
        <button
          type="button"
          onClick={onMenuClick}
          className="inline-flex items-center justify-center h-11 w-11 rounded-xl text-gray-300 hover:text-white hover:bg-white/10 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 transition-colors"
          aria-label="Open navigation menu"
          aria-haspopup="dialog"
        >
          <Menu className="h-5 w-5" aria-hidden="true" />
        </button>
      </div>

      {/* Spacer / Platform Home link */}
      <div className="flex items-center gap-3 min-w-0">
        <a
          href={LANDING_URL}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs sm:text-sm font-semibold text-gray-300 hover:text-white border border-white/10 hover:border-gray-500 rounded-xl hover:bg-white/5 transition-all focus-visible:outline-blue-500 min-h-[38px]"
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
          className="inline-flex items-center justify-center h-11 w-11 rounded-full text-gray-300 hover:text-blue-400 hover:bg-white/5 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 transition-colors"
          aria-label="View system alerts"
        >
          <Bell className="h-5 w-5" aria-hidden="true" />
        </Link>

        {/* Divider */}
        <div className="hidden sm:block h-6 w-px bg-white/10 mx-1" aria-hidden="true" />

        {/* Profile link */}
        <Link
          to="/profile"
          className="inline-flex items-center gap-2.5 h-11 px-2.5 rounded-xl text-gray-300 hover:text-white hover:bg-white/5 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 transition-colors"
          aria-label="Go to profile settings"
        >
          {/* Avatar */}
          <div
            className="h-8 w-8 rounded-full bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400 shrink-0"
            aria-hidden="true"
          >
            <User className="h-4 w-4" />
          </div>
          {/* Name label */}
          <span className="hidden sm:block text-sm font-semibold text-white whitespace-nowrap">
            Investigator
          </span>
        </Link>
      </div>
    </header>
  );
}
