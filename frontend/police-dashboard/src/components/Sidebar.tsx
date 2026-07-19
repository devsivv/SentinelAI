import { LayoutDashboard, FolderOpen, AlertTriangle } from 'lucide-react';
import { NavLink } from 'react-router-dom';

export default function Sidebar() {
  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Cases', path: '/cases', icon: FolderOpen },
    { name: 'Alerts', path: '/alerts', icon: AlertTriangle },
  ];

  return (
    <div className="flex h-full w-64 flex-col bg-slate-900 text-slate-300">
      <div className="flex h-16 items-center px-6 bg-slate-950">
        <h1 className="text-xl font-bold text-white tracking-tight">Sentinel<span className="text-blue-500">AI</span> <span className="text-slate-500 text-sm font-normal">Police</span></h1>
      </div>
      <nav className="flex-1 space-y-2 px-4 py-6">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center rounded-md px-3 py-2.5 text-sm font-medium transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-900 ${
                isActive
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white'
              }`
            }
          >
            <item.icon className="mr-3 h-5 w-5 flex-shrink-0" aria-hidden="true" />
            {item.name}
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-slate-800">
        <p className="text-xs text-slate-500 text-center">Sprint 05 MVP</p>
      </div>
    </div>
  );
}
