import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { Target, Eye, ShieldCheck, Award } from 'lucide-react';

const pillars = [
  {
    icon: Target,
    title: 'Mission',
    description: 'Democratizing AI-powered digital safety to protect every citizen from financial fraud while empowering law enforcement with explainable intelligence.',
  },
  {
    icon: Eye,
    title: 'Vision',
    description: 'Building the nation’s premier multi-agent cybercrime intelligence platform that unites public reporting with advanced AI investigation models.',
  },
  {
    icon: ShieldCheck,
    title: 'Responsible AI',
    description: 'Enforcing complete model explainability (SHAP), strict data privacy, and ethical AI auditing for prosecution-ready evidence standards.',
  },
  {
    icon: Award,
    title: 'Hackathon Innovation',
    description: 'Developed by Team Riyal Intelligence during the ET AI Hackathon to address real-world cybercrime challenges across India.',
  },
];

export default function AboutSection() {
  const ref = useRef<HTMLElement>(null);
  const inView = useInView(ref, { once: true, margin: '-60px' });

  return (
    <section
      id="about"
      ref={ref}
      className="py-24 sm:py-32 px-4 sm:px-6 lg:px-8 relative bg-slate-950/60"
      aria-labelledby="about-heading"
    >
      <div className="mx-auto max-w-7xl relative">
        {/* Heading */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-16 sm:mb-20"
        >
          <p className="text-blue-400 font-semibold text-sm tracking-widest uppercase mb-3">About Platform</p>
          <h2
            id="about-heading"
            className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight"
          >
            Securing Digital India Through AI
          </h2>
          <p className="mt-4 text-gray-400 text-base max-w-2xl mx-auto leading-relaxed">
            SentinelAI bridges the gap between public reporting and police investigation, delivering real-time multi-agent threat intelligence for national cyber safety.
          </p>
          <div className="mt-5 mx-auto w-16 h-0.5 bg-gradient-to-r from-transparent via-blue-500 to-transparent rounded-full" aria-hidden="true" />
        </motion.div>

        {/* Pillars Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {pillars.map((pillar, idx) => (
            <motion.div
              key={pillar.title}
              initial={{ opacity: 0, y: 28 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.55, delay: idx * 0.1 }}
            >
              <motion.div
                whileHover={{ y: -4, boxShadow: '0 0 32px rgba(37,99,235,0.16)' }}
                transition={{ type: 'spring', stiffness: 280, damping: 20 }}
                className="glass-card h-full p-6 flex flex-col gap-4"
              >
                <div className="w-12 h-12 rounded-xl bg-blue-600/15 border border-blue-600/30 flex items-center justify-center shrink-0">
                  <pillar.icon className="h-6 w-6 text-blue-400" aria-hidden="true" />
                </div>
                <h3 className="text-lg font-bold text-white">{pillar.title}</h3>
                <p className="text-sm text-gray-400 leading-relaxed flex-1">{pillar.description}</p>
              </motion.div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
