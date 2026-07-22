import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import {
  Globe, Shield, Server, Database, Cpu, Bot, Merge, FileText, Lock, KeyRound, Activity
} from 'lucide-react';

interface ArchNode {
  icon: React.ElementType;
  label: string;
  sublabel?: string;
  variant: 'primary' | 'secondary' | 'agent' | 'output' | 'future';
  isFuture?: boolean;
}

interface ArchRow {
  nodes: ArchNode[];
  label?: string;
}

const rows: ArchRow[] = [
  {
    nodes: [
      { icon: Globe, label: 'Landing Page & Identity Portal', variant: 'primary' },
    ],
  },
  {
    nodes: [
      { icon: Shield, label: 'Citizen Dashboard', variant: 'secondary' },
      { icon: Shield, label: 'Police Dashboard', variant: 'secondary' },
    ],
    label: 'Entry Points',
  },
  {
    nodes: [
      { icon: Server, label: 'FastAPI Backend', sublabel: 'Python 3.14 REST API', variant: 'primary' },
      { icon: Lock, label: 'Authentication', sublabel: 'OAuth2 / JWT', variant: 'future', isFuture: true },
      { icon: KeyRound, label: 'RBAC & Audit Logs', sublabel: 'Access Governance', variant: 'future', isFuture: true },
    ],
    label: 'API Core & Security',
  },
  {
    nodes: [
      { icon: Database, label: 'PostgreSQL Database', sublabel: 'Neon • Alembic Migrations', variant: 'secondary' },
      { icon: Activity, label: 'System Monitoring', sublabel: 'Telemetry & Logs', variant: 'future', isFuture: true },
    ],
  },
  {
    nodes: [
      { icon: Cpu, label: 'Intelligent Orchestrator', sublabel: 'Dynamic Agent Dispatcher', variant: 'primary' },
    ],
  },
  {
    nodes: [
      { icon: Bot, label: 'Fraud Agent', variant: 'agent' },
      { icon: Bot, label: 'Scam Comm.', variant: 'agent' },
      { icon: Bot, label: 'Graph Agent', variant: 'agent' },
      { icon: Bot, label: 'Geo Agent', variant: 'agent' },
      { icon: Bot, label: 'Currency Agent', variant: 'future', isFuture: true },
      { icon: Bot, label: 'Voice Agent', variant: 'future', isFuture: true },
    ],
    label: 'Specialized Multi-Agent AI Suite',
  },
  {
    nodes: [
      { icon: Merge, label: 'Fusion Agent', sublabel: 'Meta-Intelligence Risk Evaluator', variant: 'primary' },
    ],
  },
  {
    nodes: [
      { icon: FileText, label: 'Final Investigation Report', sublabel: 'SHAP Explainability & Threat Score', variant: 'output' },
    ],
  },
];

const variantStyles: Record<ArchNode['variant'], string> = {
  primary: 'glass-card border-blue-600/30 bg-blue-950/40',
  secondary: 'glass-card border-gray-700/50 bg-gray-800/30',
  agent: 'rounded-xl border border-blue-800/40 bg-blue-950/30 backdrop-blur-sm',
  output: 'glass-card border-green-600/40 bg-green-950/30',
  future: 'rounded-xl border border-dashed border-gray-700 bg-slate-900/40 opacity-80',
};

const variantIconBg: Record<ArchNode['variant'], string> = {
  primary: 'bg-blue-600/20 text-blue-400',
  secondary: 'bg-gray-600/20 text-gray-400',
  agent: 'bg-blue-800/30 text-blue-300',
  output: 'bg-green-600/20 text-green-400',
  future: 'bg-gray-800/40 text-gray-500',
};

function ArchNodeCard({ node }: { node: ArchNode }) {
  return (
    <div className={`flex flex-col items-center gap-2 p-3 sm:p-4 text-center ${variantStyles[node.variant]} min-w-[110px] flex-1 relative`}>
      {node.isFuture && (
        <span className="absolute -top-2.5 right-2 px-2 py-0.5 text-[9px] font-bold uppercase tracking-wider bg-slate-800 text-blue-400 border border-blue-500/30 rounded-full shadow-sm">
          Planned
        </span>
      )}
      <div className={`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 ${variantIconBg[node.variant]}`}>
        <node.icon className="h-4 w-4" aria-hidden="true" />
      </div>
      <div>
        <p className="text-xs sm:text-sm font-semibold text-white leading-tight">{node.label}</p>
        {node.sublabel && (
          <p className="text-[10px] sm:text-xs text-gray-400 mt-0.5">{node.sublabel}</p>
        )}
      </div>
    </div>
  );
}

export default function ArchitectureSection() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });

  return (
    <section
      id="architecture"
      ref={ref}
      className="py-24 sm:py-32 px-4 sm:px-6 lg:px-8 relative"
      aria-labelledby="architecture-heading"
    >
      <div className="mx-auto max-w-5xl relative">
        {/* Heading */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-14 sm:mb-18"
        >
          <p className="text-blue-400 font-semibold text-sm tracking-widest uppercase mb-3">System Architecture</p>
          <h2
            id="architecture-heading"
            className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight"
          >
            End-to-End Multi-Agent Pipeline
          </h2>
          <p className="mt-4 text-gray-400 text-base max-w-xl mx-auto">
            Operational intelligence architecture combining real-time core engines with planned roadmap capabilities.
          </p>
          <div className="mt-5 mx-auto w-16 h-0.5 bg-gradient-to-r from-transparent via-blue-500 to-transparent rounded-full" aria-hidden="true" />
        </motion.div>

        {/* Desktop / Tablet visual flow */}
        <div className="hidden sm:flex flex-col items-center gap-0">
          {rows.map((row, rowIdx) => (
            <motion.div
              key={rowIdx}
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.5, delay: rowIdx * 0.07 }}
              className="w-full flex flex-col items-center"
            >
              {row.label && (
                <p className="text-[10px] font-semibold text-gray-400 uppercase tracking-widest mb-2 mt-1">
                  {row.label}
                </p>
              )}

              <div className="flex flex-wrap justify-center gap-2 sm:gap-3 w-full max-w-4xl">
                {row.nodes.map((node) => (
                  <motion.div
                    key={node.label}
                    whileHover={{ y: -3, boxShadow: '0 0 24px rgba(37,99,235,0.2)' }}
                    transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                    className="flex-1"
                    style={{
                      minWidth: row.nodes.length > 3 ? '100px' : '150px',
                      maxWidth: row.nodes.length === 1 ? '380px' : '260px',
                    }}
                  >
                    <ArchNodeCard node={node} />
                  </motion.div>
                ))}
              </div>

              {rowIdx < rows.length - 1 && (
                <div className="arch-connector my-1" aria-hidden="true" />
              )}
            </motion.div>
          ))}
        </div>

        {/* Mobile Vertical Timeline */}
        <div className="sm:hidden space-y-4">
          {rows.flatMap((r) => r.nodes).map((node, idx) => (
            <div key={idx} className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 bg-blue-600/20 text-blue-400 border border-blue-500/30">
                <node.icon className="h-4 w-4" />
              </div>
              <div className="flex-1 min-w-0 glass-card p-3 flex items-center justify-between">
                <div>
                  <p className="text-xs font-bold text-white">{node.label}</p>
                  {node.sublabel && <p className="text-[10px] text-gray-400">{node.sublabel}</p>}
                </div>
                {node.isFuture && (
                  <span className="text-[9px] font-bold text-blue-400 uppercase bg-blue-950 px-2 py-0.5 rounded border border-blue-500/30">
                    Planned
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
