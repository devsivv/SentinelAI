import { Shield } from 'lucide-react';

interface SentinelAILogoProps {
  /** Font size class for the wordmark, e.g. 'text-xl' or 'text-2xl' */
  size?: 'sm' | 'md' | 'lg' | 'xl';
  /** Whether to show the shield icon */
  showIcon?: boolean;
  /** Whether to show the subtitle beneath */
  subtitle?: string;
}

const sizeMap = {
  sm: { text: 'text-lg', icon: 16, gap: 'gap-1.5' },
  md: { text: 'text-xl', icon: 20, gap: 'gap-2' },
  lg: { text: 'text-2xl', icon: 24, gap: 'gap-2.5' },
  xl: { text: 'text-4xl', icon: 36, gap: 'gap-3' },
} as const;

/**
 * Canonical SentinelAI branding component.
 * "Sentinel" in white, "AI" in #2563EB (blue-600).
 * Used identically on Landing Page, Citizen Dashboard, and Police Dashboard.
 */
export default function SentinelAILogo({
  size = 'md',
  showIcon = true,
  subtitle,
}: SentinelAILogoProps) {
  const { text, icon, gap } = sizeMap[size];

  return (
    <div className="flex flex-col items-start gap-0.5">
      <div className={`flex items-center ${gap}`}>
        {showIcon && (
          <Shield
            size={icon}
            className="text-blue-500 shrink-0"
            aria-hidden="true"
            strokeWidth={2}
          />
        )}
        <span
          className={`font-bold tracking-tight leading-none ${text}`}
          aria-label="SentinelAI"
        >
          <span className="text-white">Sentinel</span>
          <span className="text-blue-500">AI</span>
        </span>
      </div>
      {subtitle && (
        <span className="text-xs font-medium text-gray-400 tracking-widest uppercase pl-0.5">
          {subtitle}
        </span>
      )}
    </div>
  );
}
