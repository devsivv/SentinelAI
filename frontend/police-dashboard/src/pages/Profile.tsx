import { UserCircle } from 'lucide-react';
import PlaceholderCard from '../components/PlaceholderCard';

export default function Profile() {
  return (
    <div className="space-y-6">
      <div className="border-b border-gray-200 pb-5">
        <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:tracking-tight">
          Profile Settings
        </h2>
      </div>
      <PlaceholderCard 
        title="Officer Preferences"
        description="User settings, authentication management, and dashboard customization options."
        icon={<UserCircle className="h-10 w-10" />}
      />
    </div>
  );
}
