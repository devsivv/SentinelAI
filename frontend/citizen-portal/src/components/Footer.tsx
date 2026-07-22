import SentinelAILogo from './SentinelAILogo';

const LANDING_URL = import.meta.env.VITE_LANDING_URL || '#';
const POLICE_URL = import.meta.env.VITE_POLICE_URL || '#';

export default function Footer() {
  return (
    <footer className="border-t border-blue-900/30 bg-[#080E1A] text-gray-400 py-12 px-4 sm:px-6 lg:px-8 relative mt-auto" role="contentinfo">
      <div className="mx-auto max-w-7xl">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 pb-10 border-b border-gray-800">
          {/* Col 1: Brand & Bio */}
          <div className="md:col-span-2 space-y-3">
            <SentinelAILogo size="lg" showIcon />
            <p className="text-sm text-gray-400 max-w-md leading-relaxed">
              AI-Powered Digital Safety Platform protecting citizens, empowering law enforcement investigators, and accelerating cybercrime intelligence.
            </p>
            <div className="pt-1">
              <p className="text-xs font-semibold text-gray-300">
                Built by <span className="text-blue-400">Team Riyal Intelligence</span> for the <span className="text-blue-400">ET AI Hackathon</span>.
              </p>
            </div>
          </div>

          {/* Col 2: Navigation & Portals */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-gray-300">Portals & Navigation</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href={LANDING_URL} className="hover:text-white transition-colors">
                  SentinelAI Home
                </a>
              </li>
              <li>
                <a href="/investigate" className="hover:text-white transition-colors">
                  Citizen Investigation
                </a>
              </li>
              <li>
                <a href={POLICE_URL} target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">
                  Police Dashboard
                </a>
              </li>
            </ul>
          </div>

          {/* Col 3: Tech Stack Highlights */}
          <div className="space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-gray-300">Technology Stack</h4>
            <ul className="space-y-1.5 text-xs text-gray-400">
              <li>React 19 & TypeScript</li>
              <li>Tailwind CSS v4 & Vite</li>
              <li>FastAPI & Python 3.14</li>
              <li>PostgreSQL & AI Models</li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-gray-500">
          <div>
            &copy; 2026 SentinelAI. All rights reserved.
          </div>
          <div className="flex items-center gap-6">
            <span>Version 1.0.0</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
