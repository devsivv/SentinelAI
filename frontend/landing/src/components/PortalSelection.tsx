import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { Users, Shield, ArrowRight, CheckCircle2 } from 'lucide-react';

const CITIZEN_URL = import.meta.env.VITE_CITIZEN_URL || '#';
const POLICE_URL = import.meta.env.VITE_POLICE_URL || '#';

const portals = [
  {
    id: 'citizen',
    title: 'Citizen Portal',
    badge: 'Public Interface',
    description: 'Empowers citizens to quickly report digital fraud, scan suspicious messages and links, and track complaint statuses in real time.',
    icon: Users,
    url: CITIZEN_URL,
    buttonText: 'Open Citizen Portal',
    accentColor: 'from-blue-600/20 to-indigo-600/10 border-blue-500/30',
    buttonColor: 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-900/40',
    iconColor: 'text-blue-400 bg-blue-600/20 border-blue-500/30',
    features: [
      'Report financial fraud & scams',
      'Instant SMS & URL threat scanner',
      'Track investigation status by Case ID',
      'Privacy-first evidence submission',
    ],
  },
  {
    id: 'police',
    title: 'Police Dashboard',
    badge: 'Law Enforcement Workspace',
    description: 'Central intelligence hub for law enforcement to manage cases, view multi-agent fusion reports, and access geospatial threat maps.',
    icon: Shield,
    url: POLICE_URL,
    buttonText: 'Open Police Dashboard',
    accentColor: 'from-slate-800/60 to-blue-950/40 border-blue-600/40',
    buttonColor: 'bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-900/40',
    iconColor: 'text-blue-400 bg-blue-600/20 border-blue-500/30',
    features: [
      'Multi-agent fusion reports & risk scoring',
      'SHAP explainability & feature attributions',
      'Geospatial crime density & patrol routing',
      'Graph intelligence for suspect networks',
    ],
  },
];

export default function PortalSelection() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });

  return (
    <section
      id="portals"
      ref={ref}
      className="py-24 sm:py-32 px-4 sm:px-6 lg:px-8 relative"
      aria-labelledby="portals-heading"
    >
      <div className="mx-auto max-w-7xl relative">
        {/* Heading */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-16 sm:mb-20"
        >
          <p className="text-blue-400 font-semibold text-sm tracking-widest uppercase mb-3">Workspace Selection</p>
          <h2
            id="portals-heading"
            className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight"
          >
            Access the SentinelAI Platform
          </h2>
          <p className="mt-4 text-gray-400 text-base max-w-xl mx-auto">
            Select a specialized portal tailored for public reporting or law enforcement intelligence.
          </p>
          <div className="mt-5 mx-auto w-16 h-0.5 bg-gradient-to-r from-transparent via-blue-500 to-transparent rounded-full" aria-hidden="true" />
        </motion.div>

        {/* Portal Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-10 max-w-5xl mx-auto">
          {portals.map((portal, idx) => (
            <motion.div
              key={portal.id}
              initial={{ opacity: 0, y: 32 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: idx * 0.15 }}
            >
              <motion.div
                whileHover={{ y: -6, boxShadow: '0 0 40px rgba(37,99,235,0.22)' }}
                transition={{ type: 'spring', stiffness: 280, damping: 20 }}
                className={`glass-card p-8 sm:p-10 flex flex-col h-full bg-gradient-to-br ${portal.accentColor} relative overflow-hidden group`}
              >
                {/* Header info */}
                <div className="flex items-center justify-between gap-4 mb-6">
                  <div className={`w-14 h-14 rounded-2xl border flex items-center justify-center shrink-0 ${portal.iconColor}`}>
                    <portal.icon className="h-7 w-7" aria-hidden="true" />
                  </div>
                  <span className="text-xs font-semibold px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-300 uppercase tracking-wider">
                    {portal.badge}
                  </span>
                </div>

                <h3 className="text-2xl font-bold text-white mb-3">{portal.title}</h3>
                <p className="text-sm text-gray-300 leading-relaxed mb-6 flex-1">
                  {portal.description}
                </p>

                {/* Features list */}
                <div className="space-y-3 mb-8 pt-4 border-t border-gray-800">
                  {portal.features.map((feat) => (
                    <div key={feat} className="flex items-start gap-3 text-sm text-gray-300">
                      <CheckCircle2 className="h-4 w-4 text-blue-400 mt-0.5 shrink-0" aria-hidden="true" />
                      <span>{feat}</span>
                    </div>
                  ))}
                </div>

                {/* Action button */}
                <a
                  href={portal.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`inline-flex items-center justify-center gap-2.5 px-6 py-4 rounded-xl font-bold text-sm transition-all duration-200 min-h-[52px] ${portal.buttonColor} focus-visible:outline-blue-500`}
                  aria-label={`${portal.buttonText} (opens in new tab)`}
                >
                  <span>{portal.buttonText}</span>
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" aria-hidden="true" />
                </a>
              </motion.div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
