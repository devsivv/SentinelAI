import { LayoutDashboard } from 'lucide-react';
import PlaceholderCard from '../components/PlaceholderCard';

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-5">
        <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:tracking-tight">
          Dashboard
        </h2>
      </div>
      <PlaceholderCard 
        title="System Intelligence Overview"
        description="Comprehensive analytics, charts, and aggregated intelligence visualizations."
        icon={<LayoutDashboard className="h-10 w-10" />}
      />
    </div>
  );
}
