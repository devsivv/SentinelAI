interface FusionVerdictCardProps {
  verdict: string;
  narrative: string;
}

export default function FusionVerdictCard({ verdict, narrative }: FusionVerdictCardProps) {
  return (
    <div className="glass-card p-6 sm:p-8 flex flex-col h-full bg-[#111827]/70 backdrop-blur-md border border-white/10 rounded-2xl">
      <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Fusion Verdict</h3>
      <p className="text-2xl sm:text-3xl font-extrabold text-white capitalize mb-4">
        {verdict.replace(/_/g, ' ')}
      </p>

      <div className="mt-auto pt-4 border-t border-white/10 space-y-2">
        <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider">Investigation Narrative</h4>
        <p className="text-gray-300 text-sm leading-relaxed whitespace-pre-wrap bg-[#0F172A] p-4 rounded-xl border border-white/10">
          {narrative || 'No narrative provided by the fusion engine.'}
        </p>
      </div>
    </div>
  );
}
