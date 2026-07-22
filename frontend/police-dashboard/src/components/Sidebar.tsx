import { useEffect } from 'react';
import { LayoutDashboard, FolderOpen, AlertTriangle, X } from 'lucide-react';
import { NavLink } from 'react-router-dom';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const navItems = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'Cases', path: '/cases', icon: FolderOpen },
  { name: 'Alerts', path: '/alerts', icon: AlertTriangle },
];

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  `flex items-center rounded-md px-3 py-2.5 text-sm font-medium transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900 min-h-[44px] ${
    isActive
      ? 'bg-blue-600 text-white shadow-sm'
      : 'text-slate-300 hover:bg-slate-800 hover:text-white'
  }`;

function SidebarContent({ onClose }: { onClose: () => void }) {
  return (
    <div className="flex h-full w-64 flex-col bg-slate-900 text-slate-300">
      {/* Brand header */}
      <div className="flex h-16 items-center justify-between px-6 bg-slate-950 shrink-0">
        <h1 className="text-xl font-bold text-white tracking-tight">
          Sentinel<span className="text-blue-500">AI</span>{' '}
          <span className="text-slate-500 text-sm font-normal">Police</span>
        </h1>
        {/* Close button — only visible on mobile */}
        <button
          onClick={onClose}
          className="lg:hidden p-1 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 transition-colors"
          aria-label="Close navigation menu"
        >
          <X className="h-5 w-5" aria-hidden="true" />
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-4 py-6" aria-label="Main navigation">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={navLinkClass}
            onClick={onClose}
            end={item.path === '/'}
          >
            <item.icon className="mr-3 h-5 w-5 flex-shrink-0" aria-hidden="true" />
            {item.name}
          </NavLink>
        ))}
      </nav>

      {/* Footer — production-neutral, no sprint/phase text */}
      <div className="p-4 border-t border-slate-800 shrink-0">
        <p className="text-xs text-slate-500 text-center">
          © {new Date().getFullYear()} SentinelAI
        </p>
      </div>
    </div>
  );
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  // Lock body scroll while mobile drawer is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  return (
    <>
      {/* ── Desktop: always-visible fixed sidebar ── */}
      <div className="hidden lg:flex lg:flex-shrink-0" aria-hidden="false">
        <SidebarContent onClose={onClose} />
      </div>

      {/* ── Mobile: off-canvas overlay drawer ── */}
      {/* Backdrop */}
      <div
        className={`fixed inset-0 z-40 bg-slate-900/60 transition-opacity duration-300 lg:hidden ${
          isOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
        }`}
        aria-hidden="true"
        onClick={onClose}
      />

      {/* Drawer panel */}
      <div
        className={`fixed inset-y-0 left-0 z-50 flex flex-col transition-transform duration-300 ease-in-out lg:hidden ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
        role="dialog"
        aria-modal="true"
        aria-label="Navigation menu"
      >
        <SidebarContent onClose={onClose} />
      </div>
    </>
  );
}
