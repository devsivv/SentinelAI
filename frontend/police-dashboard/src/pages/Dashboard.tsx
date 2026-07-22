import { LayoutDashboard, TrendingUp, Shield, Activity } from 'lucide-react';

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-5">
        <h2 className="text-xl sm:text-2xl font-bold leading-7 text-gray-900 break-words">
          Dashboard
        </h2>
        <p className="mt-1 text-sm text-gray-500">
          System-wide intelligence metrics and aggregated analytics.
        </p>
      </div>

      {/* Summary stat cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {[
          { label: 'Active Cases', value: '—', icon: <Shield className="h-5 w-5 text-blue-500" />, bg: 'bg-blue-50' },
          { label: 'High Risk Cases', value: '—', icon: <TrendingUp className="h-5 w-5 text-red-500" />, bg: 'bg-red-50' },
          { label: 'Analyses Today', value: '—', icon: <Activity className="h-5 w-5 text-green-500" />, bg: 'bg-green-50' },
        ].map((stat) => (
          <div key={stat.label} className="bg-white rounded-lg shadow-sm ring-1 ring-black ring-opacity-5 p-5 flex items-center gap-4">
            <div className={`p-3 rounded-lg shrink-0 ${stat.bg}`} aria-hidden="true">
              {stat.icon}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">{stat.label}</p>
              <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Main panel */}
      <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-gray-300 bg-white p-12 sm:p-16 text-center shadow-sm">
        <div className="mb-4 p-4 bg-gray-100 rounded-full">
          <LayoutDashboard className="h-8 w-8 text-gray-400" aria-hidden="true" />
        </div>
        <h3 className="text-base font-semibold text-gray-900 mb-1">
          Intelligence Overview
        </h3>
        <p className="text-sm text-gray-500 max-w-sm">
          Aggregated charts, trend analysis, and investigation statistics will be displayed here.
        </p>
      </div>
    </div>
  );
}
