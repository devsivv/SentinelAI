import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { Brain, Shield, Zap } from 'lucide-react';

const paragraphs = [
  {
    icon: Brain,
    title: 'Multi-Agent Artificial Intelligence',
    body: 'SentinelAI deploys a coordinated ensemble of specialized AI agents — each trained on distinct fraud vectors — and fuses their intelligence through a meta-layer Fusion Engine. This architecture achieves detection accuracy that no single model can match, while maintaining full explainability through SHAP-based attribution.',
  },
  {
    icon: Shield,
    title: 'Cyber Fraud & Financial Crime Detection',
    body: 'From SMS scam interception and phishing URL classification to counterfeit currency verification and transaction fraud analysis, SentinelAI covers the full spectrum of digital financial crime. The platform processes both citizen reports and law enforcement case data in real time, delivering actionable intelligence in milliseconds.',
  },
  {
    icon: Zap,
    title: 'Law Enforcement Grade Intelligence',
    body: 'Every investigation generates a comprehensive report fusing geospatial intelligence, network graph analysis, and behavioral pattern recognition. Officers receive ranked threat assessments, patrol recommendations, and evidence trails — purpose-built for prosecution readiness and compliance with national cybercrime directives.',
  },
];

export default function PlatformOverview() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: '-80px' });

  return (
    <section
      id="overview"
      ref={ref}
      className="py-24 sm:py-32 px-4 sm:px-6 lg:px-8 relative"
      aria-labelledby="overview-heading"
    >
      <div className="mx-auto max-w-7xl">
        {/* Section heading */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="text-center mb-16 sm:mb-20"
        >
          <p className="text-blue-400 font-semibold text-sm tracking-widest uppercase mb-3">Platform Overview</p>
          <h2
            id="overview-heading"
            className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight"
          >
            Built for the Scale of Modern Cybercrime
          </h2>
          <div className="mt-4 mx-auto w-16 h-0.5 bg-gradient-to-r from-transparent via-blue-500 to-transparent rounded-full" aria-hidden="true" />
        </motion.div>

        {/* Cards grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
          {paragraphs.map((p, i) => (
            <motion.div
              key={p.title}
              initial={{ opacity: 0, y: 32 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1], delay: i * 0.12 }}
            >
              <motion.div
                whileHover={{ y: -4, boxShadow: '0 0 40px rgba(37,99,235,0.18)' }}
                transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                className="glass-card h-full p-7 sm:p-8 flex flex-col gap-5"
              >
                <div className="w-12 h-12 rounded-xl bg-blue-600/15 border border-blue-600/30 flex items-center justify-center shrink-0">
                  <p.icon className="h-6 w-6 text-blue-400" aria-hidden="true" />
                </div>
                <h3 className="text-lg font-bold text-white leading-snug">{p.title}</h3>
                <p className="text-sm text-gray-400 leading-relaxed flex-1">{p.body}</p>
              </motion.div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
