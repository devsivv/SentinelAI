import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import {
  FileText, CheckCircle, Cpu, Bot, Merge, ShieldCheck
} from 'lucide-react';

const steps = [
  {
    number: '01',
    title: 'Citizen Submits Evidence',
    description: 'Citizens submit SMS texts, phishing URLs, transaction details, or suspicious communication via the Citizen Portal.',
    icon: FileText,
  },
  {
    number: '02',
    title: 'Backend Validation & Ingestion',
    description: 'FastAPI backend validates inputs, sanitizes evidence payloads, and establishes real-time investigation tracking.',
    icon: CheckCircle,
  },
  {
    number: '03',
    title: 'Orchestrator Routing',
    description: 'Intelligent Orchestrator parses input types and dynamically dispatches payloads to specialized model pipelines.',
    icon: Cpu,
  },
  {
    number: '04',
    title: 'AI Multi-Agent Analysis',
    description: 'Fraud, Scam Comm, Graph, and Geo agents run parallel inference to produce domain-specific risk signals.',
    icon: Bot,
  },
  {
    number: '05',
    title: 'Fusion Engine Intelligence',
    description: 'Meta-intelligence Fusion Agent aggregates weighted agent outputs into a unified, explainable risk assessment.',
    icon: Merge,
  },
  {
    number: '06',
    title: 'Investigation Report Generated',
    description: 'Law enforcement receives a comprehensive report with SHAP attributions, threat scores, and actionable recommendations.',
    icon: ShieldCheck,
  },
];

export default function HowItWorksSection() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });

  return (
    <section
      id="how-it-works"
      ref={ref}
      className="py-24 sm:py-32 px-4 sm:px-6 lg:px-8 relative bg-slate-950/40"
      aria-labelledby="how-it-works-heading"
    >
      <div className="mx-auto max-w-7xl">
        {/* Heading */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-16 sm:mb-20"
        >
          <p className="text-blue-400 font-semibold text-sm tracking-widest uppercase mb-3">Workflow</p>
          <h2
            id="how-it-works-heading"
            className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight"
          >
            How SentinelAI Works
          </h2>
          <p className="mt-4 text-gray-400 text-base max-w-xl mx-auto">
            From raw digital evidence to actionable law enforcement intelligence in six automated steps.
          </p>
          <div className="mt-5 mx-auto w-16 h-0.5 bg-gradient-to-r from-transparent via-blue-500 to-transparent rounded-full" aria-hidden="true" />
        </motion.div>

        {/* Steps Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          {steps.map((step, idx) => (
            <motion.div
              key={step.number}
              initial={{ opacity: 0, y: 28 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.55, delay: idx * 0.08 }}
            >
              <motion.div
                whileHover={{ y: -4, boxShadow: '0 0 32px rgba(37,99,235,0.15)' }}
                transition={{ type: 'spring', stiffness: 280, damping: 20 }}
                className="glass-card h-full p-6 sm:p-7 flex flex-col relative overflow-hidden group"
              >
                {/* Step Number Background Accent */}
                <span className="absolute top-4 right-4 text-4xl font-black text-blue-500/10 group-hover:text-blue-500/20 transition-colors pointer-events-none">
                  {step.number}
                </span>

                <div className="w-12 h-12 rounded-xl bg-blue-600/15 border border-blue-600/30 flex items-center justify-center mb-5 shrink-0">
                  <step.icon className="h-6 w-6 text-blue-400" aria-hidden="true" />
                </div>

                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs font-bold text-blue-400 tracking-wider uppercase">Step {step.number}</span>
                </div>

                <h3 className="text-lg font-bold text-white mb-2 leading-snug">{step.title}</h3>
                <p className="text-sm text-gray-400 leading-relaxed flex-1">{step.description}</p>
              </motion.div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
