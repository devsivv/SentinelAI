import type { ReactNode } from 'react';

interface PlaceholderCardProps {
  title: string;
  description: string;
  icon?: ReactNode;
}

export default function PlaceholderCard({ title, description, icon }: PlaceholderCardProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-gray-300 bg-white p-8 sm:p-12 text-center shadow-sm">
      {icon && <div className="mb-4 text-gray-400">{icon}</div>}
      <h3 className="text-base sm:text-lg font-medium text-gray-900">{title}</h3>
      <p className="mt-2 text-sm text-gray-500 max-w-sm break-words">
        {description}
      </p>
    </div>
  );
}
