interface RiskScoreCardProps {
  score: number;
}

export default function RiskScoreCard({ score }: RiskScoreCardProps) {
  let colorClasses = 'text-green-400 bg-green-950/30 border-green-800/40 shadow-green-950/30';
  let badgeLabel = 'Low Risk';

  if (score >= 75) {
    colorClasses = 'text-red-400 bg-red-950/30 border-red-800/40 shadow-red-950/30';
    badgeLabel = 'Critical Risk';
  } else if (score >= 40) {
    colorClasses = 'text-amber-400 bg-amber-950/30 border-amber-800/40 shadow-amber-950/30';
    badgeLabel = 'High Risk';
  }

  return (
    <div className={`flex flex-col items-center justify-center p-8 rounded-2xl border backdrop-blur-md shadow-xl h-full ${colorClasses}`}>
      <span className="text-xs font-bold uppercase tracking-widest text-gray-300 mb-2">Overall Risk Score</span>
      <span className="text-6xl font-black tracking-tight my-2">{score}</span>
      <span className="text-xs font-medium opacity-80 uppercase tracking-wider">Out of 100 &bull; {badgeLabel}</span>
    </div>
  );
}
