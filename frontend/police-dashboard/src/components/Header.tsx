import { Bell, User, Menu } from 'lucide-react';
import { Link } from 'react-router-dom';

interface HeaderProps {
  onMenuClick: () => void;
}

export default function Header({ onMenuClick }: HeaderProps) {
  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-gray-200 bg-white px-4 sm:px-6 shadow-sm gap-2">
      {/* Left: hamburger (mobile only) */}
      <div className="flex items-center gap-2 lg:hidden">
        <button
          type="button"
          onClick={onMenuClick}
          className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-md focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 transition-all duration-200 min-h-[44px] min-w-[44px] flex items-center justify-center"
          aria-label="Open navigation menu"
          aria-haspopup="true"
        >
          <Menu className="h-5 w-5" aria-hidden="true" />
        </button>
      </div>

      {/* Center / spacer (desktop: breadcrumbs area, currently empty) */}
      <div className="flex flex-1 min-w-0" />

      {/* Right: actions */}
      <div className="flex items-center gap-2 sm:gap-4 shrink-0">
        <Link
          to="/alerts"
          className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-full focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 transition-all duration-200 min-h-[44px] min-w-[44px] flex items-center justify-center"
          aria-label="View system alerts"
        >
          <Bell className="h-5 w-5" aria-hidden="true" />
        </Link>

        <div className="hidden sm:block h-6 w-px bg-gray-200" aria-hidden="true" />

        <Link
          to="/profile"
          className="flex items-center gap-2 rounded-full focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 pr-1 hover:bg-gray-50 transition-all duration-200 min-h-[44px]"
          aria-label="Go to profile settings"
        >
          <div className="h-8 w-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 border border-slate-200 shrink-0">
            <User className="h-4 w-4" aria-hidden="true" />
          </div>
          {/* Name — hidden below sm to save space; no hardcoded name */}
          <span className="hidden sm:block text-sm font-semibold leading-6 text-gray-700 max-w-[120px] truncate">
            Officer
          </span>
        </Link>
      </div>
    </header>
  );
}
