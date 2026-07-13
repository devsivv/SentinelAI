interface FusionVerdictCardProps {
  verdict: string;
  narrative: string;
}

export default function FusionVerdictCard({ verdict, narrative }: FusionVerdictCardProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 h-full">
      <h3 className="text-sm font-medium text-gray-500 uppercase tracking-wider mb-2">Fusion Verdict</h3>
      <p className="text-2xl font-bold text-gray-900 mb-4 capitalize">{verdict.replace(/_/g, ' ')}</p>
      
      <div className="mt-4 pt-4 border-t border-gray-100">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Narrative</h4>
        <p className="text-gray-600 text-sm leading-relaxed whitespace-pre-wrap">
          {narrative || 'No narrative provided.'}
        </p>
      </div>
    </div>
  );
}
