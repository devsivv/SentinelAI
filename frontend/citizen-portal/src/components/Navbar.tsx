import { Link } from 'react-router-dom';
import { Shield } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex-shrink-0 flex items-center gap-2">
              <Shield className="h-8 w-8 text-indigo-600" />
              <span className="font-bold text-xl text-gray-900">SentinelAI</span>
            </Link>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              <Link
                to="/"
                className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                Home
              </Link>
              <Link
                to="/investigate"
                className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                Investigation
              </Link>
            </div>
          </div>
          {/* Mobile menu (simplified for MVP) */}
          <div className="flex items-center sm:hidden">
             <Link
                to="/investigate"
                className="text-indigo-600 font-medium text-sm"
              >
                Investigate
              </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
