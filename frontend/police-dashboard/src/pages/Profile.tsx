import { UserCircle, User } from 'lucide-react';

export default function Profile() {
  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-5">
        <h2 className="text-xl sm:text-2xl font-bold leading-7 text-gray-900 break-words">
          Profile Settings
        </h2>
        <p className="mt-1 text-sm text-gray-500">
          Manage your officer account and dashboard preferences.
        </p>
      </div>

      {/* Profile card */}
      <div className="bg-white shadow-sm ring-1 ring-black ring-opacity-5 rounded-lg p-6 sm:p-8 flex flex-col sm:flex-row items-center sm:items-start gap-6">
        <div className="h-16 w-16 rounded-full bg-slate-800 flex items-center justify-center text-white shrink-0" aria-hidden="true">
          <User className="h-8 w-8" />
        </div>
        <div className="text-center sm:text-left min-w-0">
          <h3 className="text-lg font-semibold text-gray-900">Investigator</h3>
          <p className="text-sm text-gray-500 mt-1">SentinelAI Police Dashboard</p>
          <span className="inline-flex items-center mt-2 rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10">
            Active Session
          </span>
        </div>
      </div>

      {/* Settings placeholder */}
      <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-gray-300 bg-white p-10 sm:p-12 text-center shadow-sm">
        <div className="mb-3 p-4 bg-gray-100 rounded-full">
          <UserCircle className="h-7 w-7 text-gray-400" aria-hidden="true" />
        </div>
        <h3 className="text-base font-semibold text-gray-900 mb-1">Account Settings</h3>
        <p className="text-sm text-gray-500 max-w-sm">
          Officer authentication, notification preferences, and dashboard customization will be available here.
        </p>
      </div>
    </div>
  );
}
