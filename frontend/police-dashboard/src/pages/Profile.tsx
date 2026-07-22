import { UserCircle, User } from 'lucide-react';

export default function Profile() {
  return (
    <div className="space-y-6">
      <div className="border-b border-white/10 pb-5">
        <h2 className="text-xl sm:text-2xl font-extrabold leading-7 text-white tracking-tight break-words">
          Profile Settings
        </h2>
        <p className="mt-1 text-sm text-gray-400">
          Manage your officer account and dashboard preferences.
        </p>
      </div>

      {/* Profile card */}
      <div className="glass-card border border-white/10 rounded-2xl p-6 sm:p-8 bg-[#111827]/70 backdrop-blur-md shadow-xl flex flex-col sm:flex-row items-center sm:items-start gap-6">
        <div className="h-16 w-16 rounded-full bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400 shrink-0" aria-hidden="true">
          <User className="h-8 w-8" />
        </div>
        <div className="text-center sm:text-left min-w-0">
          <h3 className="text-xl font-extrabold text-white">Investigator</h3>
          <p className="text-sm text-gray-400 mt-1">SentinelAI Law Enforcement Intelligence Workspace</p>
          <span className="inline-flex items-center mt-3 rounded-full bg-blue-500/20 border border-blue-500/30 px-3 py-1 text-xs font-bold text-blue-300 uppercase tracking-wider">
            Active Session
          </span>
        </div>
      </div>

      {/* Settings placeholder */}
      <div className="glass-card flex flex-col items-center justify-center rounded-2xl border border-white/10 bg-[#111827]/70 backdrop-blur-md p-10 sm:p-12 text-center shadow-xl">
        <div className="mb-3 p-4 bg-slate-900/80 border border-slate-800 rounded-full">
          <UserCircle className="h-7 w-7 text-blue-400" aria-hidden="true" />
        </div>
        <h3 className="text-lg font-bold text-white mb-1">Account Settings</h3>
        <p className="text-sm text-gray-400 max-w-sm leading-relaxed">
          Officer authentication, notification preferences, and dashboard customization will be available here.
        </p>
      </div>
    </div>
  );
}
