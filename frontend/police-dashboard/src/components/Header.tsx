import { Bell, User } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Header() {
  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-gray-200 bg-white px-6 shadow-sm">
      <div className="flex flex-1">
        {/* Placeholder for global search or breadcrumbs if needed in future */}
      </div>
      <div className="flex items-center gap-x-4 lg:gap-x-6">
        <Link 
          to="/alerts" 
          className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-50 rounded-full focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 transition-all duration-200"
        >
          <span className="sr-only">View notifications</span>
          <Bell className="h-5 w-5" aria-hidden="true" />
        </Link>
        <div className="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-200" aria-hidden="true" />
        <div className="flex items-center gap-x-4">
          <Link 
            to="/profile" 
            className="flex items-center gap-x-3 rounded-full focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 pr-2 hover:bg-gray-50 transition-all duration-200"
          >
            <div className="h-8 w-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 border border-slate-200">
              <User className="h-4 w-4" />
            </div>
            <span className="hidden lg:flex lg:items-center">
              <span className="text-sm font-semibold leading-6 text-gray-700" aria-hidden="true">
                Officer Smith
              </span>
            </span>
          </Link>
        </div>
      </div>
    </header>
  );
}
