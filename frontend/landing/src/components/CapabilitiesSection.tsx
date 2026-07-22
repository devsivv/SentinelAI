import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import {
  MessageSquare, Link, CreditCard, Mic,
  GitBranch, MapPin, Layers, Eye
} from 'lucide-react';

const capabilities = [
  {
    icon: MessageSquare,
    title: 'Scam Communication Detection',
    description: 'Deep learning NLP classifier trained on SMS phishing datasets. Detects social engineering, urgency manipulation, and fraudulent communication patterns in real time.',
    color: 'text-blue-400',
    bg: 'bg-blue-600/10',
    border: 'border-blue-600/20',
  },
  {
    icon: Link,
    title: 'Phishing URL Classification',
    description: 'Ensemble model analyzing URL structure, domain reputation, SSL validity, and redirect chains to classify malicious links with high precision.',
    color: 'text-purple-400',
    bg: 'bg-purple-600/10',
    border: 'border-purple-600/20',
  },
  {
    icon: CreditCard,
    title: 'Transaction Fraud Detection',
    description: 'XGBoost-powered financial fraud engine trained on large-scale transaction datasets. Detects anomalous transfer patterns, money mules, and layering schemes.',
    color: 'text-green-400',
    bg: 'bg-green-600/10',
    border: 'border-green-600/20',
  },
  {
    icon: CreditCard,
    title: 'Counterfeit Currency Detection',
    description: 'Computer vision model (EfficientNet/MobileNetV2) identifying counterfeit banknotes via pixel-level texture, micro-print, and security feature analysis.',
    color: 'text-yellow-400',
    bg: 'bg-yellow-600/10',
    border: 'border-yellow-600/20',
  },
  {
    icon: Mic,
    title: 'Voice Scam Detection',
    description: 'Audio signal processing pipeline detecting synthetic voices, deepfake audio, and telephone fraud patterns through spectral and prosodic feature analysis.',
    color: 'text-red-400',
    bg: 'bg-red-600/10',
    border: 'border-red-600/20',
  },
  {
    icon: GitBranch,
    title: 'Graph Intelligence Agent',
    description: 'Network graph engine mapping relationships between suspects, victims, accounts, and devices. Surfaces criminal rings, money flow networks, and hidden connections.',
    color: 'text-cyan-400',
    bg: 'bg-cyan-600/10',
    border: 'border-cyan-600/20',
  },
  {
    icon: MapPin,
    title: 'Geospatial Intelligence',
    description: 'Crime hotspot analysis engine using geographic clustering, district-level risk scoring, and patrol recommendation algorithms based on incident proximity data.',
    color: 'text-orange-400',
    bg: 'bg-orange-600/10',
    border: 'border-orange-600/20',
  },
  {
    icon: Layers,
    title: 'AI Fusion Engine',
    description: 'Meta-intelligence layer aggregating all agent outputs into a single weighted risk verdict. Resolves conflicts between agents and generates narrative investigation reports.',
    color: 'text-blue-300',
    bg: 'bg-blue-500/10',
    border: 'border-blue-500/20',
  },
  {
    icon: Eye,
    title: 'Explainability (SHAP)',
    description: 'Full SHAP attribution for every prediction. Officers receive feature-level explanations that identify exactly why a case was flagged — prosecution-ready evidence.',
    color: 'text-indigo-400',
    bg: 'bg-indigo-600/10',
    border: 'border-indigo-600/20',
  },
];

export default function CapabilitiesSection() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: '-80px' });

  return (
    <section
      id="capabilities"
      ref={ref}
      className="py-24 sm:py-32 px-4 sm:px-6 lg:px-8 relative"
      aria-labelledby="capabilities-heading"
    >
      {/* Subtle background accent */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: 'radial-gradient(ellipse 70% 40% at 50% 50%, rgba(37,99,235,0.04) 0%, transparent 70%)',
        }}
        aria-hidden="true"
      />

      <div className="mx-auto max-w-7xl relative">
        {/* Heading */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="text-center mb-16 sm:mb-20"
        >
          <p className="text-blue-400 font-semibold text-sm tracking-widest uppercase mb-3">Core Capabilities</p>
          <h2
            id="capabilities-heading"
            className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight"
          >
            Nine Specialized Intelligence Modules
          </h2>
          <p className="mt-4 text-gray-400 text-base max-w-2xl mx-auto">
            Each module operates independently and contributes to a unified, explainable investigation verdict.
          </p>
          <div className="mt-5 mx-auto w-16 h-0.5 bg-gradient-to-r from-transparent via-blue-500 to-transparent rounded-full" aria-hidden="true" />
        </motion.div>

        {/* Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 lg:gap-6">
          {capabilities.map((cap, i) => (
            <motion.div
              key={cap.title}
              initial={{ opacity: 0, y: 28 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1], delay: i * 0.06 }}
            >
              <motion.div
                whileHover={{ y: -5, boxShadow: '0 0 36px rgba(37,99,235,0.15)' }}
                transition={{ type: 'spring', stiffness: 280, damping: 20 }}
                className="glass-card h-full p-6 flex flex-col gap-4 group"
                role="article"
                aria-label={cap.title}
              >
                <div className={`w-11 h-11 rounded-xl ${cap.bg} border ${cap.border} flex items-center justify-center shrink-0 transition-transform duration-200 group-hover:scale-105`}>
                  <cap.icon className={`h-5 w-5 ${cap.color}`} aria-hidden="true" />
                </div>
                <h3 className="text-base font-bold text-white leading-snug">{cap.title}</h3>
                <p className="text-sm text-gray-400 leading-relaxed flex-1">{cap.description}</p>
              </motion.div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
