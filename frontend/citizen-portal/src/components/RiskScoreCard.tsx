interface RiskScoreCardProps {
  score: number;
}

export default function RiskScoreCard({ score }: RiskScoreCardProps) {
  let colorClass = 'text-green-600 bg-green-50 border-green-200';
  if (score >= 75) {
    colorClass = 'text-red-600 bg-red-50 border-red-200';
  } else if (score >= 40) {
    colorClass = 'text-amber-600 bg-amber-50 border-amber-200';
  }

  return (
    <div className={`flex flex-col items-center justify-center p-6 rounded-lg border ${colorClass}`}>
      <span className="text-sm font-semibold uppercase tracking-wider mb-2">Overall Risk Score</span>
      <span className="text-5xl font-extrabold">{score}</span>
      <span className="text-xs mt-2 opacity-80">Out of 100</span>
    </div>
  );
}
