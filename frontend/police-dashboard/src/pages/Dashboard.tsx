import { LayoutDashboard, TrendingUp, Shield, Activity } from 'lucide-react';

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="border-b border-white/10 pb-5">
        <h2 className="text-xl sm:text-2xl font-extrabold leading-7 text-white tracking-tight break-words">
          Dashboard
        </h2>
        <p className="mt-1 text-sm text-gray-400">
          System-wide intelligence metrics and aggregated analytics.
        </p>
      </div>

      {/* Summary stat cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {[
          { label: 'Active Cases', value: '10', icon: <Shield className="h-5 w-5 text-blue-400" />, bg: 'bg-blue-600/20 border-blue-500/30' },
          { label: 'High Risk Cases', value: '4', icon: <TrendingUp className="h-5 w-5 text-red-400" />, bg: 'bg-red-600/20 border-red-500/30' },
          { label: 'Analyses Today', value: '28', icon: <Activity className="h-5 w-5 text-green-400" />, bg: 'bg-green-600/20 border-green-500/30' },
        ].map((stat) => (
          <div key={stat.label} className="glass-card p-5 flex items-center gap-4 border border-white/10 rounded-2xl bg-[#111827]/70 backdrop-blur-md shadow-xl hover:border-blue-500/30 transition-all">
            <div className={`p-3 rounded-xl border shrink-0 ${stat.bg}`} aria-hidden="true">
              {stat.icon}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-bold text-gray-400 uppercase tracking-wide">{stat.label}</p>
              <p className="text-3xl font-black text-white">{stat.value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Main panel */}
      <div className="glass-card flex flex-col items-center justify-center p-12 sm:p-16 text-center border border-white/10 rounded-2xl bg-[#111827]/70 backdrop-blur-md shadow-xl">
        <div className="mb-4 p-4 bg-slate-900/80 border border-slate-800 rounded-full">
          <LayoutDashboard className="h-8 w-8 text-blue-400" aria-hidden="true" />
        </div>
        <h3 className="text-lg font-bold text-white mb-1">
          Intelligence Overview
        </h3>
        <p className="text-sm text-gray-400 max-w-sm leading-relaxed">
          Aggregated threat intelligence, crime clusters, and multi-agent trend analytics.
        </p>
      </div>
    </div>
  );
}
