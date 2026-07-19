import type { ReactNode } from 'react';

interface PlaceholderCardProps {
  title: string;
  description: string;
  icon?: ReactNode;
}

export default function PlaceholderCard({ title, description, icon }: PlaceholderCardProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-gray-300 bg-white p-12 text-center shadow-sm">
      {icon && <div className="mb-4 text-gray-400">{icon}</div>}
      <h3 className="text-lg font-medium text-gray-900">{title}</h3>
      <p className="mt-2 text-sm text-gray-500 max-w-sm">
        {description}
      </p>
      <div className="mt-6 inline-flex items-center rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10">
        Coming in later phase
      </div>
    </div>
  );
}
